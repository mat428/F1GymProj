#!/usr/bin/env bash
set -e

echo "Building Docker image..."

docker compose build --no-cache

echo ""
echo "Done."