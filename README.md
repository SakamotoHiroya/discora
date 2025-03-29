# Notion操作機能 for OpenAI Agent SDK

このプロジェクトは、OpenAIのAgent SDKにNotionにアクセスする関数をツールとして持たせ、エージェントが自動的に必要なツールを使用してNotionの操作を行えるようにする機能を提供します。

## 機能

- Notion APIを使用した認証と接続
- データベースの取得、作成、更新、クエリ
- ページの取得、作成、更新、削除
- ブロックの取得、作成、更新、削除
- OpenAI Agent SDKのツールとしての統合
- エージェントによる自動Notion操作

## セットアップ

### 環境構築

1. リポジトリをクローン
```bash
git clone <repository-url>
cd discora
```

2. 環境のセットアップ
   - Linux/macOS:
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```
   
   - Windows:
   ```bash
   setup_env.bat
   ```

3. 環境変数の設定
   - `.env`ファイルを編集して、APIキーを設定
   ```
   NOTION_API_KEY=your_notion_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Notion APIの設定

1. [Notion Developers](https://developers.notion.com/) にアクセスし、アカウントを作成
2. 新しい統合を作成し、APIキーを取得
3. 統合をNotionワークスペースに接続し、適切なページへのアクセス権を付与

## 使用方法

### 基本的な使用例

```python
from src.notion import NotionAuth, NotionClient, load_env_vars, get_notion_api_key

# 環境変数を読み込む
load_env_vars()

# Notionクライアントを初期化
notion_api_key = get_notion_api_key()
notion_auth = NotionAuth(api_key=notion_api_key)
notion_client = NotionClient(auth=notion_auth)

# データベース操作の例
from src.notion import DatabaseOperations
db_ops = DatabaseOperations(notion_client)

# データベース一覧を取得
databases = db_ops.list_databases()
print(f"データベース数: {len(databases)}")
```

### OpenAI Agent SDKとの統合例

```python
from openai import OpenAI
from src.notion import (
    NotionAuth, NotionClient, register_notion_tools,
    load_env_vars, get_notion_api_key, get_openai_api_key
)

# 環境変数を読み込む
load_env_vars()

# APIキーを取得
openai_api_key = get_openai_api_key()
notion_api_key = get_notion_api_key()

# クライアントを初期化
openai_client = OpenAI(api_key=openai_api_key)
notion_auth = NotionAuth(api_key=notion_api_key)
notion_client = NotionClient(auth=notion_auth)

# Notionツールを登録
notion_tools = register_notion_tools(notion_client)

# アシスタントを作成
assistant = openai_client.beta.assistants.create(
    name="Notionアシスタント",
    instructions="あなたはNotionを操作できるアシスタントです。",
    model="gpt-4-turbo",
    tools=notion_tools
)
```

詳細な使用例は `src/notion/example.py` を参照してください。

## ディレクトリ構造

```
src/notion/
├── __init__.py          # パッケージ初期化、便利なインポート
├── auth.py              # 認証関連の機能
├── client.py            # Notionクライアントのラッパー
├── database.py          # データベース操作機能
├── page.py              # ページ操作機能
├── block.py             # ブロック操作機能
├── tools.py             # OpenAI Agent SDKツール定義
├── utils.py             # ユーティリティ関数
└── example.py           # 使用例
```

## 注意点

- Notion APIを使用するには、Notion統合の作成とAPIキーの取得が必要です
- 統合をワークスペースに接続し、適切なアクセス権を付与する必要があります
- APIキーは環境変数または`.env`ファイルを通じて提供することを推奨します

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
