import discord
import config
from discord_agent import create_discord_agent
from agents import Runner, trace

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ ログイン完了: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.guild is None:
        await message.channel.send("DMでは使えません。サーバー内で使ってください。")
        return

    if client.user in message.mentions:
        guild_id = message.guild.id
        agent = await create_discord_agent(client, guild_id)

        result = await Runner.run(
            starting_agent=agent, input=message.content
        )
        await message.channel.send(result.final_output)

# Bot起動
client.run(config.DISCORD_TOKEN)