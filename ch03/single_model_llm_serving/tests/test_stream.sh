#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    if [ ! -z "$SERVER_PID" ]; then
        # First try graceful shutdown
        kill -TERM $SERVER_PID 2>/dev/null || true
        # Wait a bit for graceful shutdown
        sleep 2
        # If still running, force kill
        if kill -0 $SERVER_PID 2>/dev/null; then
            kill -9 $SERVER_PID 2>/dev/null || true
        fi
    fi
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Start the web service in the background
echo "Starting web service..."
cd "$PROJECT_ROOT" && python main.py &
SERVER_PID=$!

# Wait for the server to start
echo "Waiting for server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000 > /dev/null; then
        echo "Server is up!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Server failed to start after 30 seconds"
        exit 1
    fi
    echo "Waiting... ($i/30)"
    sleep 1
done

# Send streaming request and process the response
echo "Sending streaming request..."
curl -N -H "Accept: text/event-stream" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, I am"}' \
     http://localhost:8000/generate_stream | while read -r line; do
    if [[ $line == data:* ]]; then
        # Extract and print the token
        token=$(echo $line | sed 's/^data: //' | jq -r '.token')
        echo "Received token: $token"
    fi
done 