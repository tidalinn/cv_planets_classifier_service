#!/bin/bash
set -ue

export PATH="$HOME/.local/bin:$PATH"

echo "Pulling files..."
dvc pull

echo "Building and running containers..."
TARGET_STAGE=prod docker compose up --build -d
