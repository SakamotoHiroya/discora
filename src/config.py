import os

class Config:
    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        if not self.discord_token:
            raise ValueError("DISCORD_TOKEN environment variable must be set.")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set.")
        if not self.notion_token:
            raise ValueError("NOTION_TOKEN environment variable must be set.")
        if not self.notion_database_id:
            raise ValueError("NOTION_DATABASE_ID environment variable must be set.")
        
config = Config()