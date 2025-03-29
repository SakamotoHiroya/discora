import discord
import config
from discord_bot.discord_agent import create_discord_agent
from notion.agent import create_agent as create_notion_agent, NotionContext
from orchestrator import create_orchestrator, OrchestratorContext
from agents import Runner, trace
from discord_bot.disord_tools import DiscordContext, fetch_messages, list_text_channels, list_threads_in_channel, fetch_thread_messages, search_messages_in_guild, search_messages_in_channel
from notion_client import AsyncClient

async def init_notion_client(token: str) -> AsyncClient:
    return AsyncClient(auth=token)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("ログイン完了: ", client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.guild is None:
        await message.channel.send("DMでは使えません。サーバー内で使ってください。")
        return

    if client.user in message.mentions:
        guild_id = message.guild.id
        notion_agent = create_notion_agent()
        discord_agent = create_discord_agent()
        orchestrator = create_orchestrator()

        notion_client = await init_notion_client(config.NOTION_TOKEN)
        notion_context = NotionContext(client=notion_client, database_id=config.NOTION_DATABASE_ID)
        discord_context = DiscordContext(client=client, guild_id=guild_id)

        orchestrator_context = OrchestratorContext(
            notion_agent=notion_agent,
            discord_agent=discord_agent,
            notion_context=notion_context,
            discord_context=discord_context
        )

        result = await Runner.run(
            starting_agent=orchestrator, input=message.content,
            context=orchestrator_context
        )
        await message.channel.send(result.final_output)

# Bot起動
client.run(config.DISCORD_TOKEN)