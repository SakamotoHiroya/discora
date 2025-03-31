from agents import function_tool, RunContextWrapper
from discora.agents.discord.context import DiscordContext
import discord
from discora.service.discord.messages import fetch_channel_messages, fetch_thread_messages, search_messages_in_channel, search_messages_in_guild

@function_tool
async def fetch_channel_messages(context: RunContextWrapper[DiscordContext], channel_id: int, from_index: int, quantity: int) -> list[str]:
    """
    指定されたチャンネルIDから、最新メッセージのうち、from_index 番目から quantity 件分のメッセージ内容を取得して返します。

    Parameters:
        channel_id (int): 対象のチャンネルまたはスレッドのID
        from_index (int): 最新のメッセージから何件目（0が最新）から取得するか
        quantity (int): 取得するメッセージの件数

    Returns:
        list[str]: メッセージ内容のリスト
    """
    return fetch_channel_messages(context.context.client, channel_id, from_index, quantity)

@function_tool
async def fetch_thread_messages(context: RunContextWrapper[DiscordContext], thread_id: int, from_index: int, quantity: int) -> list[str]:
    """
    指定されたスレッドIDから、最新メッセージのうち、from_index 番目から quantity 件分のメッセージ内容を取得して返します。

    Parameters:
        thread_id (int): 対象のスレッドのID
        from_index (int): 最新のメッセージから何件目（0が最新）から取得するか
        quantity (int): 取得するメッセージの件数

    Returns:
        list[str]: メッセージ内容のリスト
    """
    return fetch_thread_messages(context.context.client, thread_id, from_index, quantity)

@function_tool
async def search_messages_in_channel(context: RunContextWrapper[DiscordContext], channel_id: int, keyword: str, limit: int) -> list[tuple[int, str]]:
    """
    指定されたチャンネルでキーワード検索を行い、該当するメッセージを返します。

    Parameters:
        channel_id (int): 対象のチャンネルのID
        keyword (str): 検索するキーワード
        limit (int): 検索結果の最大件数

    Returns:
        list[tuple[int, str]]: (スレッドID, メッセージ内容) のリスト
    """
    return search_messages_in_channel(context.context.client, channel_id, keyword, limit)

@function_tool
async def search_messages_in_guild(context: RunContextWrapper[DiscordContext], keyword: str, limit: int) -> list[tuple[int, int, str]]:
    """
    サーバー全体でキーワード検索を行い、該当するメッセージを返します。

    Parameters:
        keyword (str): 検索するキーワード
        limit (int): 検索結果の最大件数

    Returns:
        list[tuple[int, int, str]]: (チャンネルID, スレッドID, メッセージ内容) のリスト
    """
    return search_messages_in_guild(context.context.client, keyword, limit)