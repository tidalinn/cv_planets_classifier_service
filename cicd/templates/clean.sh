#!/bin/bash
set -ue

echo "Removing containers..."
TARGET_STAGE=prod docker compose down --volumes --remove-orphans
