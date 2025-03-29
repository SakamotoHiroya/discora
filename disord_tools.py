from dataclasses import dataclass
import discord
from agents import RunContextWrapper, function_tool

@dataclass
class DiscordContext:
    client: discord.Client
    guild_id: int

    def __init__(self, client: discord.Client, guild_id: int):
        self.client = client
        self.guild_id = guild_id

@function_tool
async def fetch_messages(context: RunContextWrapper[DiscordContext], channel_id: int, from_index: int, quantity: int) -> list[str]:
    """
    指定されたチャンネルIDから、最新メッセージのうち、from_index 番目から quantity 件分のメッセージ内容を取得して返します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        channel_id (int): 対象のチャンネルまたはスレッドのID
        from_index (int): 最新のメッセージから何件目（0が最新）から取得するか
        quantity (int): 取得するメッセージの件数

    Returns:
        list[str]: メッセージ内容のリスト
    """
    channel = context.context.client.get_channel(channel_id)
    if channel is None:
        print("チャンネルが見つかりません。")
        return []

    messages = []
    i = 0
    async for message in channel.history(limit=from_index + quantity):
        if i >= from_index:
            messages.append(message.content)
        if len(messages) >= quantity:
            break
        i += 1

    return messages

@function_tool
async def list_text_channels(context: RunContextWrapper[DiscordContext]) -> list[discord.TextChannel]:
    """
    指定されたギルドIDのテキストチャンネル一覧を取得します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        guild_id (int): 対象のギルド（サーバー）のID

    Returns:
        list[discord.TextChannel]: テキストチャンネルのリスト
    """
    guild = context.context.client.get_guild(context.context.guild_id)
    if guild is None:
        print("ギルドが見つかりません。")
        return []
    return list(guild.text_channels)

@function_tool
async def list_threads_in_channel(context: RunContextWrapper[DiscordContext], channel_id: int) -> list[discord.Thread]:
    """
    指定されたテキストチャンネル内のアクティブなスレッド一覧を取得します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        channel_id (int): 対象のテキストチャンネルのID

    Returns:
        list[discord.Thread]: スレッドのリスト
    """
    channel = context.context.client.get_channel(channel_id)
    if channel is None or not isinstance(channel, discord.TextChannel):
        print("チャンネルが見つからないか、TextChannelではありません。")
        return []
    return channel.threads

@function_tool
async def fetch_thread_messages(context: RunContextWrapper[DiscordContext], thread_id: int, from_index: int, quantity: int) -> list[str]:
    """
    指定されたスレッドIDから、最新メッセージのうち、from_index 番目から quantity 件分のメッセージ内容を取得して返します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        thread_id (int): 対象のスレッドのID
        from_index (int): 最新のメッセージから何件目（0が最新）から取得するか
        quantity (int): 取得するメッセージの件数

    Returns:
        list[str]: メッセージ内容のリスト
    """
    thread = context.context.client.get_channel(thread_id)
    if thread is None or not isinstance(thread, discord.Thread):
        print("スレッドが見つかりません。")
        return []

    messages = []
    i = 0
    async for message in thread.history(limit=from_index + quantity):
        if i >= from_index:
            messages.append(message.content)
        if len(messages) >= quantity:
            break
        i += 1

    return messages

@function_tool
async def search_messages_in_guild(context: RunContextWrapper[DiscordContext], keyword: str, limit: int) -> list[tuple[int, int, str]]:
    """
    サーバー全体でキーワード検索を行い、該当するメッセージを返します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        guild_id (int): 対象のギルド（サーバー）のID
        keyword (str): 検索するキーワード
        limit (int): 検索結果の最大件数

    Returns:
        list[tuple[int, int, str]]: (チャンネルID, スレッドID, メッセージ内容) のリスト
    """
    guild = context.context.client.get_guild(context.context.guild_id)
    if guild is None:
        print("ギルドが見つかりません。")
        return []

    results = []
    for channel in guild.text_channels:
        try:
            async for message in channel.history(limit=limit):
                if keyword.lower() in message.content.lower():
                    thread_id = message.thread.id if message.thread else 0
                    results.append((channel.id, thread_id, message.content))
                    if len(results) >= limit:
                        return results
        except discord.Forbidden:
            continue

    return results

@function_tool
async def search_messages_in_channel(context: RunContextWrapper[DiscordContext], channel_id: int, keyword: str, limit: int) -> list[tuple[int, str]]:
    """
    指定されたチャンネルでキーワード検索を行い、該当するメッセージを返します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        channel_id (int): 対象のチャンネルのID
        keyword (str): 検索するキーワード
        limit (int): 検索結果の最大件数

    Returns:
        list[tuple[int, str]]: (スレッドID, メッセージ内容) のリスト
    """
    channel = context.context.client.get_channel(channel_id)
    if channel is None or not isinstance(channel, discord.TextChannel):
        print("チャンネルが見つからないか、TextChannelではありません。")
        return []

    results = []
    try:
        async for message in channel.history(limit=limit):
            if keyword.lower() in message.content.lower():
                thread_id = message.thread.id if message.thread else 0
                results.append((thread_id, message.content))
                if len(results) >= limit:
                    break
    except discord.Forbidden:
        print("チャンネルへのアクセス権限がありません。")

    return results
