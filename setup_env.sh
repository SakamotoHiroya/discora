#!/bin/bash

# 仮想環境のディレクトリ名
ENV_DIR="notion_env"

# 仮想環境が存在するか確認
if [ -d "$ENV_DIR" ]; then
    echo "仮想環境 '$ENV_DIR' はすでに存在します。"
else
    echo "仮想環境 '$ENV_DIR' を作成しています..."
    python3 -m venv $ENV_DIR
    echo "仮想環境が作成されました。"
fi

# 仮想環境をアクティベート
echo "仮想環境をアクティベートしています..."
source $ENV_DIR/bin/activate

# 必要なライブラリをインストール
echo "必要なライブラリをインストールしています..."
pip install -r requirements.txt

echo "セットアップが完了しました。"
echo "仮想環境を使用するには、以下のコマンドを実行してください："
echo "source $ENV_DIR/bin/activate"

# .envファイルの作成または更新
echo "環境変数を設定します..."

# 既存の.envファイルがあれば読み込む
if [ -f ".env" ]; then
    source .env
fi

# Notion APIキーの設定
read -p "Notion APIキーを入力してください（既存: $NOTION_API_KEY）: " notion_key
if [ -n "$notion_key" ]; then
    NOTION_API_KEY=$notion_key
fi

# OpenAI APIキーの設定
read -p "OpenAI APIキーを入力してください（既存: $OPENAI_API_KEY）: " openai_key
if [ -n "$openai_key" ]; then
    OPENAI_API_KEY=$openai_key
fi

# .envファイルに書き込む
cat > .env << EOL
# Notion API設定
NOTION_API_KEY=$NOTION_API_KEY

# OpenAI API設定
OPENAI_API_KEY=$OPENAI_API_KEY
EOL

echo ".envファイルが更新されました。"

echo ""
echo "使用方法："
echo "1. 仮想環境をアクティベート: source $ENV_DIR/bin/activate"
echo "2. .envファイルにAPIキーを設定"
echo "3. サンプルを実行: python -c 'from src.notion import example; example.simple_example()'"
