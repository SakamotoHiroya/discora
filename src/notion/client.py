from notion_client import Client

def init_notion_client(token) -> Client:
    return Client(auth=token)
