import discord
from agents import FunctionTool

async def list_text_channels(client: discord.Client, guild_id: int) -> list[discord.TextChannel]:
    """
    指定されたギルドIDのテキストチャンネル一覧を取得します。

    Parameters:
        client (discord.Client): Discord のクライアントインスタンス
        guild_id (int): 対象のギルド（サーバー）のID

    Returns:
        list[discord.TextChannel]: テキストチャンネルのリスト
    """
    guild = client.get_guild(guild_id)
    if guild is None:
        print("ギルドが見つかりません。")
        return []
    return list(guild.text_channels)

async def create_list_text_channels_tool(client: discord.Client, guild_id: int):
    return FunctionTool(
        name="list_text_channels",
        description="指定されたギルドIDのテキストチャンネル一覧を取得します。",
        params_json_schema={
            "guild_id": int,
        },
        on_invoke_tool=lambda: list_text_channels(client, guild_id)
    )