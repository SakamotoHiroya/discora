import discord

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
        raise ValueError("ギルドが見つかりません。")
    return list(guild.text_channels)