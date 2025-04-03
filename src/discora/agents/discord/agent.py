from agents import Agent
import discora.agents.discord.tools as tools
from discora.agents import DiscordContext

def create_agent() -> Agent[DiscordContext]:
    agent = Agent[DiscordContext](
        name="discord seacher",
        instructions="ユーザの指示に忠実に従い、discord内を検索したり、メッセージの要約を取得してください。",
        tools=[
            tools.channels.list_text_channels,
            tools.threads.list_threads_in_channel,
            tools.messages.fetch_channel_messages,
            tools.messages.fetch_thread_messages,
            tools.messages.search_messages_in_guild,
            tools.messages.search_messages_in_channel,
        ]
    )
    
    return agent
