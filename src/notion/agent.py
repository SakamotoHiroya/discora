import asyncio
from notion_client import AsyncClient
from agents import Agent, function_tool, RunContextWrapper
from dataclasses import dataclass
from typing import Optional, List
from notion.page import create_notion_page

@dataclass
class NotionContext:
    client : AsyncClient
    database_id: str

    def __init__(self, client: AsyncClient, database_id: str):
        self.client = client
        self.database_id = database_id

@function_tool(strict_mode=False)
def create_notion_page_tool(
    context: RunContextWrapper[NotionContext],
    title: str,
    content_blocks: Optional[List[dict]] = None,
    icon_url: str = "",
    cover_url: str = ""
) -> dict:
    print("YEAH!")
    return create_notion_page(context.context.client,context.context.database_id,title,content_blocks=content_blocks, icon_url=icon_url, cover_url=cover_url)

def create_agent() -> Agent[NotionContext]:
    return Agent(
        name="Notion Page Creator",
        instructions=(
            "Create new pages in Notion based on user requests. "
            "Generate content_blocks strictly following Notion API block object format described here: "
            "https://developers.notion.com/reference/block. "
            "For example, a paragraph block must look like: "
            "{'object': 'block', 'type': 'paragraph', 'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': 'your text here'}}]}}. "
            "Ensure accuracy and proper structure of blocks according to the official Notion API documentation."
        ),
        model="gpt-4o",
        tools=[create_notion_page_tool],
    )
