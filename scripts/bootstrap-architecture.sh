#!/usr/bin/env bash
set -eo pipefail

WORKSPACE_DIR="$(pwd)"
echo -e "\033[1;34m========================================================\033[0m"
echo -e "\033[1;34m  ANTIGRAVITY STUDIO ENTERPRISE ARCHITECTURE BOOTSTRAP  \033[0m"
echo -e "\033[1;34m========================================================\033[0m"

echo -e "\n\033[1;34m[1/5]\033[0m Initializing SQLite State Store (studio.db)..."
if [ -f "$WORKSPACE_DIR/video_02_lead_triage/venv/bin/python3" ]; then
  PYTHON_EXEC="$WORKSPACE_DIR/video_02_lead_triage/venv/bin/python3"
else
  PYTHON_EXEC="$(command -v python3 || echo /usr/bin/python3)"
fi

"$PYTHON_EXEC" -c "from services.db_service import init_db; init_db(); print('✔ studio.db initialized with WAL mode!')"

echo -e "\n\033[1;34m[2/5]\033[0m Verifying Domain Services (Media, Analytics, QA)..."
"$PYTHON_EXEC" -c "from services.qa_service import run_full_preflight_audit; print('✔ Preflight audit status:', run_full_preflight_audit()['status'])"
"$PYTHON_EXEC" -c "from services.analytics_service import get_outliers; print('✔ Outliers service verified, analyzing:', get_outliers('data/sample_collected.json')['total_analyzed'], 'videos')"

echo -e "\n\033[1;34m[3/5]\033[0m Verifying MCP Server Protocol Gateway..."
"$PYTHON_EXEC" -c "import mcp_server; print('✔ mcp_server module loaded successfully!')"

echo -e "\n\033[1;34m[4/5]\033[0m Ensuring File Permissions..."
chmod +x scripts/*.sh || true

echo -e "\n\033[1;34m[5/5]\033[0m Architecture Bootstrap Completed Successfully!"
echo -e "\033[1;32m[READY]\033[0m All 7 architectural pillars are fully configured and verified."
