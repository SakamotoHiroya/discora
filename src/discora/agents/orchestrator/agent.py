import logging
from agents import Agent, function_tool, RunContextWrapper, Runner
from dataclasses import dataclass
from discora.agents.notion.context import NotionContext
from discora.agents.discord.context import DiscordContext
from discora.agents.orchestrator.context import OrchestratorContext
from discora.agents.orchestrator.tools.subagent import instract_notion_agent, instract_discord_agent

logger = logging.getLogger(__name__)


def create_agent() -> Agent[OrchestratorContext]:
    """
    オーケストレーターエージェントを作成します。

    Returns:
        Agent: オーケストレーターエージェント
    """
    return Agent(
        name="Orchestrator",
        instructions="あなたはNotionページの作成を行うエージェントとDiscordの情報にアクセスするエージェントを用いながら、ユーザの要望に応えるエージェントです",
        tools=[instract_notion_agent, instract_discord_agent]
    )