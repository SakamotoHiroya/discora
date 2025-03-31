import discord
import logging
import asyncio
from typing import Optional
from discora.core.config import config
from discora.agents.discord.agent import create_agent as create_discord_agent
from discora.agents.notion.agent import create_agent as create_notion_agent, NotionContext
from discora.agents.orchestrator import create_agent as create_orchestrator, OrchestratorContext
from agents import Runner
from discora.agents.discord.context import DiscordContext
from notion_client import AsyncClient

# ログ設定
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DiscordBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.notion_client: Optional[AsyncClient] = None

    async def setup_hook(self):
        """初期化処理"""
        try:
            self.notion_client = await init_notion_client(config.NOTION_TOKEN)
            logger.info("Notion client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Notion client: {e}")
            raise

    async def close(self):
        """クリーンアップ処理"""
        if self.notion_client:
            await self.notion_client.aclose()
        await super().close()

async def init_notion_client(token: str) -> AsyncClient:
    return AsyncClient(auth=token)

client = DiscordBot()

@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user}")

@client.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Error in {event}: {args} {kwargs}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.guild is None:
        await message.channel.send("DMでは使えません。サーバー内で使ってください。")
        return

    if client.user in message.mentions:
        try:
            guild_id = message.guild.id
            notion_agent = create_notion_agent()
            discord_agent = create_discord_agent()
            orchestrator = create_orchestrator()

            notion_context = NotionContext(client=client.notion_client, database_id=config.NOTION_DATABASE_ID)
            discord_context = DiscordContext(client=client, guild_id=guild_id)

            orchestrator_context = OrchestratorContext(
                notion_agent=notion_agent,
                discord_agent=discord_agent,
                notion_context=notion_context,
                discord_context=discord_context
            )

            async with message.channel.typing():
                result = await Runner.run(
                    starting_agent=orchestrator,
                    input=message.content,
                    context=orchestrator_context
                )
                await message.channel.send(result.final_output)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await message.channel.send("申し訳ありません。エラーが発生しました。しばらく時間をおいて再度お試しください。")

def main():
    try:
        client.run(config.DISCORD_TOKEN)
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()