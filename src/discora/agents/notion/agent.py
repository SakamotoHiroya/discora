from agents import Agent
from discora.agents.notion.context import NotionContext
from discora.agents.notion.tools.page import create_notion_page, delete_notion_page, get_notion_pages

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
        tools=[
            create_notion_page,
            delete_notion_page,
            get_notion_pages,
        ],
    )
