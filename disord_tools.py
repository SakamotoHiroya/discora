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
