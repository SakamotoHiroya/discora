import discord
from discora.core.main import logger

async def fetch_channel_messages(client: discord.Client, channel_id: int, from_index: int, quantity: int) -> list[str]:
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
    logger.info(f"Fetching {quantity} messages")
    channel = client.get_channel(channel_id)
    if channel is None:
        logger.info("Channel not found.")
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

async def fetch_thread_messages(client: discord.Client, thread_id: int, from_index: int, quantity: int) -> list[str]:
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
    thread = client.get_channel(thread_id)
    if thread is None or not isinstance(thread, discord.Thread):
        logger.info("Thread not found.")
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

async def search_messages_in_channel(client: discord.Client, channel_id: int, keyword: str, limit: int) -> list[tuple[int, str]]:
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
    channel = client.get_channel(channel_id)
    if channel is None or not isinstance(channel, discord.TextChannel):
        logger.info("Channel not found or not a TextChannel.")
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
        logger.info("No permission to access the channel.")

    return results

async def search_messages_in_guild(client: discord.Client, guild_id: int,   keyword: str, limit: int) -> list[tuple[int, int, str]]:
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
    guild = client.get_guild(guild_id)
    if guild is None:
        raise ValueError("ギルドが見つかりません。")

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
