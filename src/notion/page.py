from notion_client import Client

def get_notion_pages(client: Client, database_id: str, page_size: int) -> dict:
    response = client.databases.query(database_id=database_id, page_size=page_size)
    return response

def create_notion_page(client: Client, database_id: str, title: str) -> dict:
    new_page = client.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }
    )
    return new_page