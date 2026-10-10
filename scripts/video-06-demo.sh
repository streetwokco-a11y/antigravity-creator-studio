#!/usr/bin/env bash
# scripts/video-06-demo.sh - Demo Environment Stager for Episode #6 (Hardcore DevOps)
set -eo pipefail

WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WORKSPACE"

echo -e "\033[1;35m=================================================================\033[0m"
echo -e "\033[1;35m  STAGING LIVE DEMO ENVIRONMENT: EPISODE #6 (HARDCORE DEVOPS)    \033[0m"
echo -e "\033[1;35m=================================================================\033[0m"

# 1. Ensure logs directory and initialize agent-mission.log
mkdir -p logs
MISSION_LOG="$WORKSPACE/logs/agent-mission.log"
cat << 'EOF' > "$MISSION_LOG"
[2026-10-10 12:54:01] [BOOT] Google Antigravity autonomous mission monitor initialized.
[2026-10-10 12:54:02] [AUDIT] Inspecting pg_stat_activity on postgres:5432...
[2026-10-10 12:54:03] [DETECT] CRITICAL: Exclusive lock detected on relation 'customer_transactions'.
[2026-10-10 12:54:04] [METRICS] Blocked backend PID: 4102 | State: 'active' | Duration: 44.8s
[2026-10-10 12:54:06] [DISPATCH] Invoking subagent: .agents/skills/db-migration-guard
[2026-10-10 12:54:09] [ACTION] Executing zero-loss cancellation: SELECT pg_cancel_backend(4102);
[2026-10-10 12:54:12] [PATCH] Re-routing connection pool pool_size=50 max_overflow=20.
[2026-10-10 12:54:15] [RECOVERY] Query timeout policy patched. Database latency restored to 12ms.
[2026-10-10 12:54:18] [DISARM] Triggering root kill-switch cancellation via /tmp/disarm_cron...
[2026-10-10 12:54:19] [SUCCESS] All 50,000 active sockets healthy. HTTP 200 OK across cluster.
EOF

echo -e "\033[1;34m[PANE 1]\033[0m Armed root countdown timer: \033[1;32m./scripts/arm-countdown.sh 60\033[0m"
echo -e "\033[1;34m[PANE 2]\033[0m Live agent telemetry stream: \033[1;32mtail -f logs/agent-mission.log\033[0m"
echo -e "\033[1;34m[PANE 3]\033[0m System telemetry / lock monitor ready."
echo ""
echo -e "\033[1;32m[READY FOR FILMING]\033[0m Multi-pane tmux layout ready for 1080p60 capture."
