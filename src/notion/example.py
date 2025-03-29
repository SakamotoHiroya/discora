from agents import Runner
from agent import NotionContext
from client import init_notion_client
import asyncio
import os
from agent import create_agent

async def main(user_request: str):
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        raise ValueError("NOTION_TOKEN environment variable must be set.")
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not database_id:
        raise ValueError("NOTION_DATABASE_ID environment variable must be set.")
    
    notion_client = init_notion_client(notion_token)

    context = NotionContext(
        client=notion_client,
        database_id=database_id
    )

    agent = create_agent()

    await Runner.run(agent, user_request, context=context)

if __name__ == "__main__":
    user_request = (
        "In recent game development projects, the team has been enthusiastically discussing new character "
        "and map designs, and there has been a lively exchange of ideas, especially regarding game balance adjustments. "
        "In addition, several new ideas for event planning have been proposed, and innovations to encourage user "
        "participation are being considered. As for technical issues, some members are working on optimization to reduce "
        "server load, and positive progress is being made to improve performance."
    )
    asyncio.run(main(user_request))