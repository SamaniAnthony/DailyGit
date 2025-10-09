#!/bin/bash

# News Curator Startup Script

echo "🚀 Starting News Curator..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Installing locally instead..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Please install Python 3.9+"
        exit 1
    fi

    # Install dependencies
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt

    # Create directories
    mkdir -p data logs

    # Run application
    echo "✅ Starting application..."
    cd app
    python3 main.py

else
    # Docker is available
    echo "🐳 Using Docker..."

    # Check if docker-compose is installed
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
    else
        docker compose up -d
    fi

    echo ""
    echo "✅ News Curator is running!"
    echo ""
    echo "📱 Open in browser: http://localhost:8080"
    echo "📊 View logs: docker-compose logs -f"
    echo "🛑 Stop: docker-compose down"
    echo ""
fi
