import os
import asyncio
from discora.agents.notion.context import NotionContext
from src.discora.service.notion.client import init_notion_client
from discora.agents.notion.agent import create_agent
from agents import Runner
from core.config import config
async def main(user_request: str):
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        raise ValueError("NOTION_TOKEN environment variable must be set.")
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not database_id:
        raise ValueError("NOTION_DATABASE_ID environment variable must be set.")
    
    notion_client = await init_notion_client(notion_token)

    context = NotionContext(
        client=notion_client,
        database_id=config.NOTION_DATABASE_ID,
    )

    agent = create_agent()

    await Runner.run(
        starting_agent=agent,
        input=user_request,
        context=context
    )

if __name__ == "__main__":
    user_request = (
        "In recent game development projects, the team has been enthusiastically discussing new character "
        "and map designs, and there has been a lively exchange of ideas, especially regarding game balance adjustments. "
        "In addition, several new ideas for event planning have been proposed, and innovations to encourage user "
        "participation are being considered. As for technical issues, some members are working on optimization to reduce "
        "server load, and positive progress is being made to improve performance."
    )
    asyncio.run(main(user_request))
