import unittest
from notion_client import AsyncClient
from discora.service.notion.page import get_notion_pages, create_notion_page, delete_notion_page
from discora.service.notion.client import init_notion_client
from discora.core.config import config


class TestNotionPages(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.database_id = config.NOTION_DATABASE_ID
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID environment variable is not set.")

        self.token = config.NOTION_TOKEN
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is not set.")

        self.client = await init_notion_client(self.token)

        if not isinstance(self.client, AsyncClient):
            raise ValueError("Failed to initialize Notion client.")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_get_notion_pages(self):
        result = await get_notion_pages(self.client, self.database_id, page_size=2)
        self.assertIsInstance(result, dict)
        self.assertIn("results", result)
        self.assertLessEqual(len(result["results"]), 2)

    async def test_create_notion_page_success(self):
        new_page_title = "Unit Test Page"
        new_page = await create_notion_page(self.client, self.database_id, new_page_title)
        self.assertIsInstance(new_page, dict)
        self.assertIn("id", new_page)
        self.assertEqual(
            new_page["properties"]["Name"]["title"][0]["text"]["content"],
            new_page_title,
        )
        deleted_page = await delete_notion_page(self.client, new_page["id"])
        self.assertTrue(deleted_page.get("archived", False))

    async def test_create_notion_page_optional_fields(self):
        new_page_title = "Unit Test Page with Options"
        content_blocks = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Test content"}}]},
            }
        ]
        icon_url = "https://example.com/icon.png"
        cover_url = "https://example.com/cover.png"
        new_page = await create_notion_page(
            self.client,
            self.database_id,
            new_page_title,
            content_blocks=content_blocks,
            icon_url=icon_url,
            cover_url=cover_url,
        )
        self.assertIsInstance(new_page, dict)
        self.assertIn("id", new_page)
        self.assertEqual(
            new_page["properties"]["Name"]["title"][0]["text"]["content"],
            new_page_title,
        )
        if "icon" in new_page:
            self.assertEqual(new_page["icon"]["external"]["url"], icon_url)
        if "cover" in new_page:
            self.assertEqual(new_page["cover"]["external"]["url"], cover_url)
        deleted_page = await delete_notion_page(self.client, new_page["id"])
        self.assertTrue(deleted_page.get("archived", False))

    async def test_create_notion_page_missing_title(self):
        with self.assertRaises(ValueError) as context:
            await create_notion_page(self.client, self.database_id, "")
        self.assertIn("Title must be provided", str(context.exception))

    async def test_create_notion_page_missing_database_id(self):
        with self.assertRaises(ValueError) as context:
            await create_notion_page(self.client, "", "Unit Test Page")
        self.assertIn("Database ID must be provided", str(context.exception))


if __name__ == "__main__":
    unittest.main()
