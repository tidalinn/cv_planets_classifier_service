#!/bin/bash
set -ue

echo "Stopping containers..."
TARGET_STAGE=prod docker compose down
