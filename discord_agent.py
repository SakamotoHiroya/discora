import asyncio
import discord
from agents import Agent
from discord_tools.fetch_messages import create_fetch_messages_tool
from discord_tools.list_text_channels import create_list_text_channels_tool
from discord_tools.list_threads import create_list_threads_tool

async def create_discord_agent(client: discord.Client, guild_id: int):
    agent = Agent(
        name="discord seacher",
        instructions="ユーザの指示に忠実に従い、discord内を検索したり、メッセージの要約を取得してください。",
        # tools=[
        #     await create_fetch_messages_tool(client),
        #     await create_list_text_channels_tool(client, guild_id),
        #     await create_list_threads_tool(client)
        # ]
    )
    
    return agent
