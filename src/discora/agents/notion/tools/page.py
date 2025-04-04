from agents import function_tool, RunContextWrapper
from discora.agents.notion.context import NotionContext
import discora.service.notion.page as page

@function_tool
async def get_notion_pages(context: RunContextWrapper[NotionContext], page_size: int) -> dict:
    """
    Notionからページを取得します
    NotionDatabaseはコンテキストによって自動決定するため設定する必要はありません

    Args:
        page_size (int): 取得するページ数

    Returns:
        dict: NotionAPIのレスポンス1
    """
    return await page.get_notion_pages(context.context.client, context.context.database_id, page_size)

@function_tool
async def create_notion_page(context: RunContextWrapper[NotionContext], title: str, content_blocks: list = None, icon_url: str = "", cover_url: str = "") -> dict:
    """
    Create a new page in a Notion database with structured content, icon, and cover image.

    Args:
        title (str): The title of the new page.
        content_blocks (list, optional): List of Notion block dictionaries for structured content. Defaults to None.
        icon_url (str, optional): URL for the icon of the page. Defaults to "".
        cover_url (str, optional): URL for the cover image of the page. Defaults to "".

    Returns:
        dict: The response from the Notion API containing the new page details.

    Raises:
        ValueError: If the request fails or mandatory fields are missing.
    """
    return await page.create_notion_page(context.context.client, context.database_id, title, content_blocks, icon_url, cover_url)

@function_tool
async def delete_notion_page(context: RunContextWrapper[NotionContext], page_id: str) -> dict:
    """
    Archives (deletes) a Notion page using the provided AsyncClient.

    Args:
        page_id (str): The ID of the Notion page to be archived (deleted).

    Returns:
        dict: A dictionary representing the archived page object returned by the Notion API.

    Raises:
        ValueError: If the page_id is not provided or if the deletion fails.
    """
    return await page.delete_notion_page(context.context.client, page_id)
