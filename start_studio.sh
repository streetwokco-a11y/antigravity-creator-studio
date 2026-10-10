#!/usr/bin/env bash
set -e

WORKSPACE="/home/rockyy/oct catalog/youtube channel"
cd "$WORKSPACE"

# Detect Python binary with FastAPI / Uvicorn installed
if [ -f "$WORKSPACE/video_02_lead_triage/venv/bin/python3" ]; then
  PYTHON_BIN="$WORKSPACE/video_02_lead_triage/venv/bin/python3"
elif [ -f "$WORKSPACE/venv/bin/python3" ]; then
  PYTHON_BIN="$WORKSPACE/venv/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "[ERROR] Python 3 not found!"
  exit 1
fi

echo "Using Python: $PYTHON_BIN"

# Check if already running on port 8000
if ss -tulpn 2>/dev/null | grep -q ":8000 " || lsof -i :8000 2>/dev/null | grep -q LISTEN; then
  echo "Studio server already running on port 8000."
else
  echo "Starting Antigravity Creator Studio server..."
  nohup "$PYTHON_BIN" studio_server.py > studio.log 2>&1 &
  
  # Wait up to 5 seconds for port 8000 to become active
  for i in {1..10}; do
    if ss -tulpn 2>/dev/null | grep -q ":8000 " || curl -s http://127.0.0.1:8000/ >/dev/null 2>&1; then
      echo "Server is live on http://localhost:8000"
      break
    fi
    sleep 0.5
  done
fi

# Launch browser
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open http://localhost:8000 >/dev/null 2>&1 &
elif command -v firefox >/dev/null 2>&1; then
  firefox http://localhost:8000 >/dev/null 2>&1 &
fi
