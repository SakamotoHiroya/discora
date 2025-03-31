from agents import function_tool, RunContextWrapper
from discora.agents.discord.context import DiscordContext
from discora.service.discord.channels import list_text_channels
import discord


@function_tool
async def list_text_channels(context: RunContextWrapper[DiscordContext]) -> list[discord.TextChannel]:
    """
    指定されたギルドIDのテキストチャンネル一覧を取得します。

    Returns:
        list[discord.TextChannel]: テキストチャンネルのリスト
    """
    return list_text_channels(context.context.client, context.context.guild_id)