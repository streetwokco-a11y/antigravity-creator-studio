#!/usr/bin/env bash
set -eo pipefail

PROJECT_DIR="video_02_lead_triage"
echo -e "\033[1;34m[Step 1/4]\033[0m Initializing Python virtual environment..."
cd "$PROJECT_DIR"
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r backend/requirements.txt

echo -e "\033[1;34m[Step 2/4]\033[0m Seeding live SQLite database..."
python3 -c "import sys; sys.path.append('backend'); from database import init_db; init_db()"

echo -e "\033[1;34m[Step 3/4]\033[0m Starting background FastAPI engine..."
export PYTHONPATH=backend:$PYTHONPATH
uvicorn backend.main:app --port 8000 --log-level warning &
API_PID=$!

sleep 2

echo -e "\033[1;34m[Step 4/4]\033[0m Executing live endpoint tests..."
HEALTH=$(curl -s http://localhost:8000/api/health)
echo -e "Health Probe: \033[1;32m$HEALTH\033[0m"

# Seed a test lead
INSERTED=$(curl -s -X POST http://localhost:8000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"Elon Vance","company":"X-Dynamics","email":"elon@xdynamics.io","budget":12000.0}')
echo -e "Live Lead Ingestion: \033[1;32m$INSERTED\033[0m"

# Run triage
TRIAGE_RES=$(curl -s -X POST http://localhost:8000/api/triage/execute)
echo -e "Triage Engine Execution: \033[1;32m$TRIAGE_RES\033[0m"

echo "--------------------------------------------------------"
echo -e "\033[1;32m[SUCCESS]\033[0m Demo backend verified and ready for live screen capture."
echo "FastAPI PID is $API_PID. Kill when filming finishes using: kill $API_PID"
