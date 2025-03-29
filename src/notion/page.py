from notion_client import AsyncClient

async def get_notion_pages(client: AsyncClient, database_id: str, page_size: int) -> dict:
    """
    Retrieve pages from a Notion database.

    Args:
        client (AsyncClient): The Notion client instance.
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
        response = await client.databases.query(database_id=database_id, page_size=page_size)
    except Exception as e:
        raise ValueError(f"Failed to retrieve pages: {e}")
    return response

async def create_notion_page(
    client: AsyncClient,
    database_id: str,
    title: str,
    content_blocks: list = None,
    icon_url: str = "",
    cover_url: str = ""
) -> dict:
    """
    Create a new page in a Notion database with structured content, icon, and cover image.

    Args:
        client (AsyncClient): The Notion client instance.
        database_id (str): The ID of the Notion database.
        title (str): The title of the new page.
        content_blocks (list, optional): List of Notion block dictionaries for structured content. Defaults to None.
        icon_url (str, optional): URL for the icon of the page. Defaults to "".
        cover_url (str, optional): URL for the cover image of the page. Defaults to "".

    Returns:
        dict: The response from the Notion API containing the new page details.

    Raises:
        ValueError: If the request fails or mandatory fields are missing.
    """

    if not database_id:
        raise ValueError("Database ID must be provided.")
    if not title:
        raise ValueError("Title must be provided.")

    properties = {
        "Name": {
            "title": [{"text": {"content": title}}]
        }
    }

    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    if content_blocks:
        new_page_data["children"] = content_blocks

    if icon_url:
        new_page_data["icon"] = {"type": "external", "external": {"url": icon_url}}

    if cover_url:
        new_page_data["cover"] = {"type": "external", "external": {"url": cover_url}}

    new_page = await client.pages.create(**new_page_data)
    
    return new_page

async def delete_notion_page(client: AsyncClient, page_id: str) -> dict:
    if not page_id:
        raise ValueError("Page ID must be provided.")
    try:
        deleted_page = await client.pages.update(page_id=page_id, archived=True)
    except Exception as e:
        raise ValueError(f"Failed to delete page: {e}")
    return deleted_page