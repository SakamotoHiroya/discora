from agents import function_tool, RunContextWrapper, Runner
from discora.agents.orchestrator.context import OrchestratorContext
import logging

logger = logging.getLogger(__name__)

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
