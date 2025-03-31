from agents import function_tool, RunContextWrapper
from discora.agents.discord.context import DiscordContext
from discora.service.discord.threads import list_threads_in_channel
import discord

@function_tool
async def list_threads_in_channel(context: RunContextWrapper[DiscordContext], channel_id: int) -> list[discord.Thread]:
    """
    指定されたテキストチャンネル内のアクティブなスレッド一覧を取得します。

    Parameters:
        channel_id (int): 対象のテキストチャンネルのID

    Returns:
        list[discord.Thread]: スレッドのリスト
    """
    return list_threads_in_channel(context.context.client, channel_id)

