import discord
from agents import FunctionTool

async def fetch_messages(client: discord.Client, channel_id: int, from_index: int, quantity: int) -> list[str]:
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
    channel = client.get_channel(channel_id)
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


async def create_fetch_messages_tool(client: discord.Client):
    return FunctionTool(
        name="fetch_messages",
        description="指定されたチャンネルIDから、最新メッセージのうち、from_index 番目から quantity 件分のメッセージ内容を取得して返します。",
        params_json_schema={
            "channel_id": int,
            "from_index": int,
            "quantity": int,
        },
        on_invoke_tool=lambda channel_id, from_index, quantity: fetch_messages(client, channel_id, from_index, quantity)
    )
