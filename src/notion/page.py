from notion_client import Client

def get_notion_pages(client: Client, database_id: str, page_size: int) -> dict:
    """
    Retrieve pages from a Notion database.

    Args:
        client (Client): The Notion client instance.
        database_id (str): The ID of the Notion database.
        page_size (int): The number of pages to retrieve.

    Returns:
        dict: The response from the Notion API containing the pages.

    Raises:
        ValueError: If the request fails or the response is invalid.
    """
    if not database_id:
        raise ValueError("Database ID must be provided.")
    if page_size <= 0:
        raise ValueError("Page size must be greater than zero.")
    try:
        response = client.databases.query(database_id=database_id, page_size=page_size)
    except Exception as e:
        raise ValueError(f"Failed to retrieve pages: {e}")
    return response

def create_notion_page(client: Client, database_id: str, title: str) -> dict:
    """
    Create a new page in a Notion database.

    Args:
        client (Client): The Notion client instance.
        database_id (str): The ID of the Notion database.
        title (str): The title of the new page.

    Returns:
        dict: The response from the Notion API containing the new page details.

    Raises:
        ValueError: If the request fails or the response is invalid.
    """
    if not database_id:
        raise ValueError("Database ID must be provided.")
    if not title:
        raise ValueError("Title must be provided.")
    new_page = client.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }
    )
    return new_page
