import discord

async def list_threads_in_channel(client: discord.Client, channel_id: int) -> list[discord.Thread]:
    """
    指定されたテキストチャンネル内のアクティブなスレッド一覧を取得します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        channel_id (int): 対象のテキストチャンネルのID

    Returns:
        list[discord.Thread]: スレッドのリスト
    """
    channel = client.get_channel(channel_id)
    if channel is None or not isinstance(channel, discord.TextChannel):
        raise ValueError("チャンネルが見つからないか、TextChannelではありません。")
    return channel.threads

