#!/bin/bash

VENV_PATH=$(poetry env info --path)
mkdir -p .vscode

cat <<EOF > .vscode/settings.json
{
    "python.defaultInterpreterPath": "$VENV_PATH"
}
EOF