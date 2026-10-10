#!/usr/bin/env bash
# scripts/nightly-orchestrator.sh - Headless overnight batch runner for YouTube channel automation
set -eo pipefail

EPISODE="${1:-2}"
WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WORKSPACE"

PYTHON_BIN="$WORKSPACE/video_02_lead_triage/venv/bin/python3"
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

echo -e "\033[1;36m=================================================================\033[0m"
echo -e "\033[1;36m   ANTIGRAVITY AUTONOMOUS OVERNIGHT PIPELINE RUNNER (EP #$EPISODE) \033[0m"
echo -e "\033[1;36m=================================================================\033[0m"

"$PYTHON_BIN" -c "
import asyncio
from services.scheduler_service import scheduler
res = asyncio.run(scheduler.execute_hands_off_pipeline($EPISODE))
print('Pipeline Verdict:', res.get('verdict'))
print('Phases Executed:', list(res.get('phases', {}).keys()))
"

echo -e "\n\033[1;32m[SUCCESS]\033[0m Overnight autonomous batch complete."
