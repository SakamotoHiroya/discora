from dataclasses import dataclass
from notion_client import AsyncClient

@dataclass
class NotionContext:
    client : AsyncClient
    database_id: str

    def __init__(self, client: AsyncClient, database_id: str):
        self.client = client
        self.database_id = database_id