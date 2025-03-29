#!/bin/bash

# 仮想環境のディレクトリ名
ENV_DIR="notion_env"

# 仮想環境が存在するか確認
if [ ! -d "$ENV_DIR" ]; then
    echo "仮想環境が見つかりません。setup_env.sh を実行してください。"
    exit 1
fi

# 仮想環境をアクティベート
source $ENV_DIR/bin/activate

# pytestがインストールされているか確認
if ! pip list | grep -q pytest; then
    echo "pytestをインストールしています..."
    pip install pytest pytest-cov
fi

# テストを実行
echo "テストを実行しています..."
python -m pytest tests/notion -v

# カバレッジレポートを生成
echo "カバレッジレポートを生成しています..."
python -m pytest tests/notion --cov=src.notion --cov-report=term --cov-report=html

echo "テスト完了！"
echo "カバレッジレポートは htmlcov/index.html で確認できます。"
