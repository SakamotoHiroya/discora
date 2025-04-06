import os
import unittest
from notion_client import AsyncClient
from discora.service.notion.client import init_notion_client

class TestInitNotionClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is not set.")

    async def test_client_with_token(self):
        client = await init_notion_client(self.token)
        self.assertIsInstance(client, AsyncClient)

    async def test_client_invalid_token(self):
        client = await init_notion_client("invalid_token")
        self.assertIsInstance(client, AsyncClient)

if __name__ == "__main__":
    unittest.main()