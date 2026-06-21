#!/bin/bash

# Script for running the bot

echo "🚀 Starting Telegram Shop Bot..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

# Build and start containers
docker-compose up -d --build

echo "✅ Bot is running!"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop bot:"
echo "   docker-compose down"
