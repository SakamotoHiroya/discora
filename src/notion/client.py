from notion_client import Client

def init_notion_client(token: str) -> Client:
    """
    Initialize a Notion client with the provided token.

    Args:
        token (str): The authentication token for Notion API.

    Returns:
        Client: An instance of the Notion Client.

    Raises:
        ValueError: If the token is invalid or authentication fails.
    """
    if not token:
        raise ValueError("Token must be provided.")
    try:
        return Client(auth=token)
    except Exception as e:
        raise ValueError(f"Failed to initialize Notion client: {e}")
