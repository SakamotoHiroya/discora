# Discora - Discord & Notion Integration for OpenAI Agent SDK

このプロジェクトは、OpenAIのAgent SDKを活用して、DiscordとNotionを連携させるエージェントシステムを提供します。エージェントが自動的に必要なツールを使用して、DiscordメッセージやNotionデータベースの操作を行えるようにする機能を実装しています。

## 機能

### Discord機能
- Discordボットとの連携
- チャンネルとスレッドの一覧取得
- メッセージの取得と検索
- 構造化ログ出力（INFO、ERROR、DEBUG）

### Notion機能
- Notion APIを使用した認証と接続
- データベースの取得、作成、更新、クエリ
- ページの取得、作成、更新、削除
- ブロックの取得、作成、更新、削除

### 共通機能
- OpenAI Agent SDKのツールとしての統合
- オーケストレーターによるエージェント間連携
- 構成可能な環境設定

## セットアップ

### 環境構築

1. リポジトリをクローン
```bash
git clone <repository-url>
cd discora
```

2. 仮想環境のセットアップと依存関係のインストール

   **Poetry を使用する場合（推奨）:**
   ```bash

   # 依存関係のインストール
   poetry install
   ```

3. 環境変数の設定
   - `.env`ファイルを作成して、必要なAPIキーを設定
   ```
   DISCORD_TOKEN=your_discord_bot_token
   NOTION_TOKEN=your_notion_api_key
   NOTION_DATABASE_ID=your_notion_database_id
   LOG_LEVEL=INFO
   ```

### 実行

以下のコマンド実行します
```shell
poetry run python -m discora.core.main
```

### Discord APIの設定

1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセスし、新しいアプリケーションを作成
2. Botセクションでボットを作成し、トークンを取得
3. OAuth2セクションで適切な権限を設定し、ボットをサーバーに招待

### Notion APIの設定

1. [Notion Developers](https://developers.notion.com/) にアクセスし、アカウントを作成
2. 新しい統合を作成し、APIキーを取得
3. 統合をNotionワークスペースに接続し、適切なページへのアクセス権を付与

## 使用方法

### Discordボットの起動

```bash
# 仮想環境が有効化されていることを確認してから実行
python -m src.discora.core.main
```

### Notion操作の例

```python
import asyncio
from notion_client import AsyncClient
from src.discora.service.notion.client import init_notion_client
from src.discora.service.notion.page import get_notion_pages, create_notion_page

async def main():
    # Notionクライアントを初期化
    client = await init_notion_client("your_notion_token")
    
    # データベースからページを取得
    pages = await get_notion_pages(client, "your_database_id", 10)
    print(f"取得したページ数: {len(pages['results'])}")
    
    # 新しいページを作成
    new_page = await create_notion_page(
        client,
        database_id="your_database_id",
        title="新しいページ",
        description="これは新しく作成されたページです",
        tags=["テスト", "サンプル"]
    )
    print(f"作成されたページID: {new_page['id']}")
    
    await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())
```

### Discord操作の例

```python
import asyncio
import discord
from src.discora.service.discord.channels import list_text_channels
from src.discora.service.discord.messages import fetch_channel_messages

async def main():
    # Discordクライアントを初期化
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")
        
        # サーバーのテキストチャンネル一覧を取得
        guild_id = 123456789012345678  # あなたのサーバーID
        channels = await list_text_channels(client, guild_id)
        print(f"チャンネル数: {len(channels)}")
        
        # 特定のチャンネルからメッセージを取得
        if channels:
            messages = await fetch_channel_messages(client, channels[0].id, 0, 5)
            print(f"取得したメッセージ: {messages}")
        
        await client.close()
    
    await client.start("your_discord_token")

if __name__ == "__main__":
    asyncio.run(main())
```

### オーケストレーターの使用例

```python
import asyncio
from src.discora.agents.discord.agent import create_agent as create_discord_agent
from src.discora.agents.notion.agent import create_agent as create_notion_agent
from src.discora.agents.orchestrator import create_agent as create_orchestrator
from src.discora.agents.discord.context import DiscordContext
from src.discora.agents.notion.context import NotionContext
from src.discora.agents.orchestrator.context import OrchestratorContext

async def main():
    # 各エージェントを作成
    discord_agent = create_discord_agent()
    notion_agent = create_notion_agent()
    orchestrator = create_orchestrator()
    
    # コンテキストを設定
    discord_context = DiscordContext(client=discord_client, guild_id=guild_id)
    notion_context = NotionContext(client=notion_client, database_id=database_id)
    
    # オーケストレーターコンテキストを設定
    orchestrator_context = OrchestratorContext(
        notion_agent=notion_agent,
        discord_agent=discord_agent,
        notion_context=notion_context,
        discord_context=discord_context
    )
    
    # オーケストレーターを実行
    result = await Runner.run(
        starting_agent=orchestrator,
        input="Discordの最新メッセージをNotionに保存して",
        context=orchestrator_context
    )
    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## ディレクトリ構造

```
discora/
├── .env.sample          # 環境変数サンプルファイル
├── requirements.txt     # 依存関係リスト
├── poetry.lock          # Poetry依存関係ロックファイル
├── pyproject.toml       # Poetryプロジェクト設定
├── README.md            # このファイル
└── src/                 # ソースコード
    ├── __init__.py
    └── discora/         # メインパッケージ
        ├── agents/      # エージェント定義
        │   ├── discord/ # Discordエージェント
        │   ├── notion/  # Notionエージェント
        │   └── orchestrator/ # オーケストレーター
        ├── core/        # コア機能
        │   ├── config.py # 設定管理
        │   └── main.py  # メインエントリーポイント
        └── service/     # サービス層
            ├── discord/ # Discord API操作
            └── notion/  # Notion API操作
```

## 注意点

- 仮想環境内でプロジェクトを実行することを強く推奨します
- Discord APIを使用するには、Discordボットの作成とトークンの取得が必要です
- Notion APIを使用するには、Notion統合の作成とAPIキーの取得が必要です
- 統合をそれぞれのプラットフォームに接続し、適切なアクセス権を付与する必要があります
- APIキーは環境変数または`.env`ファイルを通じて提供することを推奨します
- ログレベルは環境変数`LOG_LEVEL`で設定可能です（デフォルトは`INFO`）

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
