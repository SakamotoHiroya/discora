from dataclasses import dataclass
from agents import Agent
from discora.agents.notion.context import NotionContext
from discora.agents.discord.context import DiscordContext

@dataclass
class OrchestratorContext:
    notion_agent: Agent
    discord_agent: Agent
    notion_context: NotionContext
    discord_context: DiscordContext

    def __init__(
        self,
        notion_agent: Agent,
        discord_agent: Agent,
        notion_context: NotionContext,
        discord_context: DiscordContext
    ) -> None:
        self.notion_agent = notion_agent
        self.discord_agent = discord_agent
        self.notion_context = notion_context
        self.discord_context = discord_context
