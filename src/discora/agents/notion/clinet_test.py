import os
import unittest
from notion_client import Client
from src.discora.service.notion.client import init_notion_client

class TestInitNotionClient(unittest.TestCase):
    def setUp(self):
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is not set.")
        
    def test_client_with_token(self):
        client = init_notion_client(self.token)
        self.assertIsInstance(client, Client)

    def test_client_invalid_token(self):
        client = init_notion_client("invalid_token")
        self.assertIsInstance(client, Client)

if __name__ == "__main__":
    unittest.main()