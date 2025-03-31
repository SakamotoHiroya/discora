from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    DISCORD_TOKEN: str
    NOTION_TOKEN: str
    NOTION_DATABASE_ID: str
    LOG_LEVEL: str = "INFO"

    @classmethod
    def from_env(cls) -> 'Config':
        required_vars = {
            'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN'),
            'NOTION_TOKEN': os.getenv('NOTION_TOKEN'),
            'NOTION_DATABASE_ID': os.getenv('NOTION_DATABASE_ID'),
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return cls(
            DISCORD_TOKEN=required_vars['DISCORD_TOKEN'],
            NOTION_TOKEN=required_vars['NOTION_TOKEN'],
            NOTION_DATABASE_ID=required_vars['NOTION_DATABASE_ID'],
            LOG_LEVEL=os.getenv('LOG_LEVEL', 'INFO')
        )

config = Config.from_env()
