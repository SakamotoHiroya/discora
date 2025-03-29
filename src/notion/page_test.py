import os
import unittest
from notion_client import Client
from page import get_notion_pages, create_notion_page
from client import init_notion_client

class TestNotionPages(unittest.TestCase):
    def setUp(self):
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID environment variable is not set.")
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is not set.")
        self.client = init_notion_client(self.token)
        if not isinstance(self.client, Client):
            raise ValueError("Failed to initialize Notion client.")
        
    def test_get_notion_pages(self):
        result = get_notion_pages(self.client, self.database_id, page_size=2)
        
        self.assertIsInstance(result, dict)
        self.assertIn("results", result)
        self.assertLessEqual(len(result["results"]), 2)

    def test_create_notion_page(self):
        new_page_title = "Unit Test Page"
        new_page = create_notion_page(self.client, self.database_id, new_page_title)

        self.assertIsInstance(new_page, dict)
        self.assertIn("id", new_page)
        self.assertEqual(
            new_page["properties"]["Name"]["title"][0]["text"]["content"],
            new_page_title
        )

if __name__ == "__main__":
    unittest.main()