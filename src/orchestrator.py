import asyncio
import logging
from typing import Optional, Dict, Any
from agents import Agent, function_tool, RunContextWrapper
from dataclasses import dataclass
from notion.agent import NotionContext
from discord_bot.disord_tools import DiscordContext
from agents import Runner

logger = logging.getLogger(__name__)

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

@function_tool
async def instract_notion_agent(context: RunContextWrapper[OrchestratorContext], message: str):
    """
    Notionページの作成を行うエージェントに指示を出します。
    messageに指定された指示をエージェントに渡します
    命令の中には、実際に作成するページの内容や、情報を事細かに指定してください

    Args:
        context: 実行コンテキスト
        message: エージェントに渡す指示メッセージ

    Returns:
        str: エージェントからの応答

    Raises:
        Exception: エージェントの実行中にエラーが発生した場合
    """
    try:
        result = await Runner.run(
            starting_agent=context.context.notion_agent,
            input=message,
            context=context.context.notion_context
        )
        return result.final_output
    except Exception as e:
        logger.error(f"Error in Notion agent: {e}")
        raise

@function_tool
async def instract_discord_agent(context: RunContextWrapper[OrchestratorContext], message: str):
    """
    Discordの情報にアクセスするエージェントに指示を出します。
    messageに指定された指示をエージェントに渡します
    このエージェントはDiscordサーバ上の情報をキーワード検索したり特定のチャンネル、スレッドのメッセージを一覧取得したりできます

    Args:
        context: 実行コンテキスト
        message: エージェントに渡す指示メッセージ

    Returns:
        str: エージェントからの応答

    Raises:
        Exception: エージェントの実行中にエラーが発生した場合
    """
    try:
        result = await Runner.run(
            starting_agent=context.context.discord_agent,
            input=message,
            context=context.context.discord_context
        )
        return result.final_output
    except Exception as e:
        logger.error(f"Error in Discord agent: {e}")
        raise

def create_orchestrator() -> Agent[OrchestratorContext]:
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