import discord
from agents import FunctionTool

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
        print("チャンネルが見つからないか、TextChannelではありません。")
        return []
    return channel.threads

async def create_list_threads_tool(client: discord.Client):
    return FunctionTool(
        name="list_threads",
        description="指定されたテキストチャンネル内のアクティブなスレッド一覧を取得します。",
        params_json_schema={
            "channel_id": int,
        },
        on_invoke_tool=lambda channel_id: list_threads_in_channel(client, channel_id)
    ) 