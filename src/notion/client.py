from notion_client import AsyncClient

async def init_notion_client(token: str) -> AsyncClient:
    """
    Initialize a Notion client with the provided token.

    Args:
        token (str): The authentication token for Notion API.

    Returns:
        AsyncClient: An instance of the Notion AsyncClient.

    Raises:
        ValueError: If the token is invalid or authentication fails.
    """
    if not token:
        raise ValueError("Token must be provided.")
    try:
        return AsyncClient(auth=token)
    except Exception as e:
        raise ValueError(f"Failed to initialize Notion client: {e}")
