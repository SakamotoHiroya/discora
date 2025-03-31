from agents import function_tool, RunContextWrapper
from discora.agents.notion.context import NotionContext
from discora.service.notion.page import get_notion_pages, create_notion_page, delete_notion_page

@function_tool
async def get_notion_pages(context: RunContextWrapper[NotionContext], database_id: str, page_size: int) -> dict:
    return get_notion_pages(context.context.client, database_id, page_size)

@function_tool
async def create_notion_page(context: RunContextWrapper[NotionContext], database_id: str, title: str, content_blocks: list = None, icon_url: str = "", cover_url: str = "") -> dict:
    return create_notion_page(context.context.client, database_id, title, content_blocks, icon_url, cover_url)

@function_tool
async def delete_notion_page(context: RunContextWrapper[NotionContext], page_id: str) -> dict:
    return delete_notion_page(context.context.client, page_id)
