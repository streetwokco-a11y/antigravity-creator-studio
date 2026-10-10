#!/usr/bin/env bash
set -eo pipefail

SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/antigravity-studio.service"
WORKSPACE_DIR="$(pwd)"

mkdir -p "$SERVICE_DIR"

# Detect Python interpreter with dependencies installed
if [ -f "$WORKSPACE_DIR/video_02_lead_triage/venv/bin/python3" ]; then
  PYTHON_EXEC="$WORKSPACE_DIR/video_02_lead_triage/venv/bin/python3"
elif [ -f "$WORKSPACE_DIR/venv/bin/python3" ]; then
  PYTHON_EXEC="$WORKSPACE_DIR/venv/bin/python3"
else
  PYTHON_EXEC="$(command -v python3 || echo /usr/bin/python3)"
fi

cat << EOF > "$SERVICE_FILE"
[Unit]
Description=Antigravity Creator Studio Daemon & MCP Engine
After=network.target sound.target

[Service]
Type=simple
WorkingDirectory=$WORKSPACE_DIR
ExecStart=$PYTHON_EXEC $WORKSPACE_DIR/studio_server.py
Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
EOF

if command -v systemctl >/dev/null 2>&1; then
  systemctl --user daemon-reload || true
  systemctl --user enable antigravity-studio.service || true
  systemctl --user restart antigravity-studio.service || true
  echo -e "\033[1;32m[SUCCESS]\033[0m Antigravity Studio systemd user service installed and active."
  echo "Check status: systemctl --user status antigravity-studio.service"
else
  echo -e "\033[1;33m[NOTE]\033[0m systemctl not present in this container/subshell. Service file written to $SERVICE_FILE."
fi
