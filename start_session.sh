#!/bin/bash

# Saga Engine Session Starter
# This script creates a new game session and starts an interactive MCP session

set -e  # Exit on any error

# Configuration
GO_SERVER_URL="http://localhost:8080"
API_KEY="${OPENAI_API_KEY}"
MODEL="openai:gpt-4o"
DEMO_JSON_PATH="server/internal/testdata/demo.json"

# Check if API key is set
if [ -z "$API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set it with: export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

# Check if Go server is running
echo "🔍 Checking if Go server is running..."
if ! curl -s "$GO_SERVER_URL/api/v1/sessions" > /dev/null 2>&1; then
    echo "Error: Go server is not running at $GO_SERVER_URL"
    echo "Please start the Go server first"
    exit 1
fi

# Check if demo.json exists
if [ ! -f "$DEMO_JSON_PATH" ]; then
    echo "Error: Demo JSON file not found at $DEMO_JSON_PATH"
    echo "Make sure the server submodule is properly initialized"
    exit 1
fi

# Create a new session with demo.json
echo "🎮 Creating new game session with demo level..."
SESSION_RESPONSE=$(curl -s -X POST "$GO_SERVER_URL/api/v1/sessions" \
    -H "Content-Type: application/json" \
    -d "{\"level\": $(cat "$DEMO_JSON_PATH")}")

# Extract session ID from response
SESSION_ID=$(echo "$SESSION_RESPONSE" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$SESSION_ID" ]; then
    echo "Error: Failed to create session"
    echo "Response: $SESSION_RESPONSE"
    exit 1
fi

echo "✅ Created session: $SESSION_ID"

# Generate local.json from template
echo "📝 Generating local.json with session ID..."
sed "s/{{SESSION_ID}}/$SESSION_ID/g" local.json.template > local.json

# Start the interactive session
echo "🤖 Starting interactive session..."
mcphost \
    --model "$MODEL" \
    --provider-api-key "$API_KEY" \
    --compact \
    --config local.json \
    --system-prompt prompt.txt \
    --save-session session.json