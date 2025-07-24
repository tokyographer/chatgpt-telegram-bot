#!/bin/bash

# Simple run script for the AI Telegram Bot
echo "🤖 Starting AI Telegram Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and add your tokens:"
    echo "cp .env.example .env"
    echo "Then edit .env with your actual tokens."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Run the bot
echo "🚀 Starting bot..."
python bot.py
