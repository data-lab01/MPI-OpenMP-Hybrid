#!/bin/bash
# TransForgeX1 Development Mode with Auto-Reload

echo "🔧 Starting TransForgeX1 in Development Mode..."
echo "📝 Auto-reload enabled - changes will be detected automatically"
echo "🌐 Visit: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop"

# Kill existing process
lsof -ti:5000 | xargs kill -9 2>/dev/null

# Run with auto-reload (debug=True already in app.py)
python3 app.py
