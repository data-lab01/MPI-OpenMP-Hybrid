#!/bin/bash
# TransForgeX1 Restart Script

echo "🔄 Restarting TransForgeX1..."

# Kill existing process on port 5000
lsof -ti:5000 | xargs kill -9 2>/dev/null

# Wait a moment
sleep 1

# Start the server
cd /Users/reveal/Documents/transforgex1
python3 app.py &

echo "✅ TransForgeX1 restarted successfully!"
echo "🌐 Visit: http://127.0.0.1:5000"
