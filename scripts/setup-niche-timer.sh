#!/usr/bin/env bash
set -eo pipefail

USER_SYSTEMD_DIR="$HOME/.config/systemd/user"
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_FILE="$USER_SYSTEMD_DIR/antigravity-niche-sync.service"
TIMER_FILE="$USER_SYSTEMD_DIR/antigravity-niche-sync.timer"

mkdir -p "$USER_SYSTEMD_DIR"
mkdir -p "$WORKSPACE_DIR/logs"

# 1. Define the Execution Service
cat << SERVICE_EOF > "$SERVICE_FILE"
[Unit]
Description=Daily YouTube Niche Ingestion & Swipe File Sync
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=%h
ExecStart=/bin/bash -c "cd '$WORKSPACE_DIR' && ./scripts/collect-niche.sh >> logs/niche-sync.log 2>&1"

[Install]
WantedBy=default.target
SERVICE_EOF

# 2. Define the 06:00 AM Daily Timer
cat << TIMER_EOF > "$TIMER_FILE"
[Unit]
Description=Trigger Niche Ingestion daily at 06:00 AM

[Timer]
OnCalendar=*-*-* 06:00:00
Persistent=true

[Install]
WantedBy=timers.target
TIMER_EOF

# 3. Reload, Enable & Arm the Timer
systemctl --user daemon-reload
systemctl --user enable --now antigravity-niche-sync.timer

echo -e "\033[1;32m[SUCCESS]\033[0m Daily niche ingestion timer armed for 06:00 AM."
echo -e "\033[1;34m[INFO]\033[0m Timer status:"
systemctl --user list-timers antigravity-niche-sync.timer --no-pager
