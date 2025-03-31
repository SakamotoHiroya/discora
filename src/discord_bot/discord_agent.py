import asyncio
import discord
from agents import Agent
from discord_bot.disord_tools import DiscordContext, fetch_messages, list_text_channels, list_threads_in_channel, fetch_thread_messages, search_messages_in_guild, search_messages_in_channel

def create_discord_agent():
    agent = Agent(
        name="discord seacher",
        instructions="ユーザの指示に忠実に従い、discord内を検索したり、メッセージの要約を取得してください。",
        tools=[
            fetch_messages,
            list_text_channels,
            list_threads_in_channel,
            fetch_thread_messages,
            search_messages_in_guild,
            search_messages_in_channel,
        ]
    )
    
    return agent
