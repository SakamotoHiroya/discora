from agents import function_tool, RunContextWrapper
from discora.agents.discord import DiscordContext
import discora.service.discord.channels as channels
import discord
import logging

logger = logging.getLogger(__name__)

@function_tool
async def list_text_channels(context: RunContextWrapper[DiscordContext]) -> list[discord.TextChannel]:
    """
    指定されたギルドIDのテキストチャンネル一覧を取得します。

    Returns:
        list[discord.TextChannel]: テキストチャンネルのリスト
    """

    return await channels.list_text_channels(context.context.client, context.context.guild_id)