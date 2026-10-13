"""
services/db_service.py - SQLite state & transaction store for Antigravity Studio.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(WORKSPACE_ROOT, "studio.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workflow_name TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at TEXT NOT NULL,
        completed_at TEXT,
        metadata_json TEXT
    );

    CREATE TABLE IF NOT EXISTS qa_audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT NOT NULL,
        video_codec TEXT,
        resolution TEXT,
        framerate REAL,
        integrated_lufs REAL,
        true_peak REAL,
        lra REAL,
        verdict TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        episode_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        privacy_status TEXT NOT NULL,
        youtube_video_id TEXT,
        file_path TEXT NOT NULL,
        published_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS dead_letter_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        error_message TEXT NOT NULL,
        retries_attempted INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );

    -- 3-Agent Mission Control DAG state machine tables
    CREATE TABLE IF NOT EXISTS dag_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mission_id TEXT NOT NULL UNIQUE,   -- UUID key for idempotent resume
        task_description TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'PENDING',
        -- States: PENDING | PLANNED | BUILT | AUDITING | SUCCESS | FAILED_DLQ | CRASHED
        attempt_count INTEGER NOT NULL DEFAULT 0,
        max_retries INTEGER NOT NULL DEFAULT 3,
        last_failure_json TEXT,
        plan_hash TEXT,                    -- SHA-256 of frozen plan for integrity gate
        started_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        completed_at TEXT
    );

    CREATE TABLE IF NOT EXISTS plan_contracts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mission_id TEXT NOT NULL,
        plan_hash TEXT NOT NULL,           -- Immutability fingerprint
        plan_json TEXT NOT NULL,           -- Frozen change plan contract
        locked_at TEXT NOT NULL,
        FOREIGN KEY (mission_id) REFERENCES dag_runs(mission_id)
    );
    """)
    conn.commit()
    conn.close()


def log_run_start(workflow_name: str, metadata: Optional[Dict[str, Any]] = None) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO runs (workflow_name, status, started_at, metadata_json) VALUES (?, 'RUNNING', ?, ?)",
        (workflow_name, now, json.dumps(metadata or {}))
    )
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id


def log_run_finish(run_id: int, status: str):
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE runs SET status = ?, completed_at = ? WHERE id = ?",
        (status, now, run_id)
    )
    conn.commit()
    conn.close()


def record_qa_audit(file_path: str, codec: str, res: str, fps: float, lufs: float, peak: float, lra: float, verdict: str):
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    conn.execute(
        """INSERT INTO qa_audits 
           (file_path, video_codec, resolution, framerate, integrated_lufs, true_peak, lra, verdict, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (file_path, codec, res, fps, lufs, peak, lra, verdict, now)
    )
    conn.commit()
    conn.close()


def record_dead_letter(service_name: str, payload: Dict[str, Any], error: str, retries: int):
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    conn.execute(
        "INSERT INTO dead_letter_queue (service_name, payload_json, error_message, retries_attempted, created_at) VALUES (?, ?, ?, ?, ?)",
        (service_name, json.dumps(payload), error, retries, now)
    )
    conn.commit()
    conn.close()


def fetch_latest_audits(limit: int = 5) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qa_audits ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Mission Control DAG Persistence Layer
# ─────────────────────────────────────────────────────────────────────────────

def create_dag_run(mission_id: str, task_description: str, max_retries: int = 3) -> str:
    """Create a new DAG run record and return the mission_id.
    Idempotent: if mission_id already exists, returns it unchanged.
    """
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    try:
        conn.execute(
            """INSERT OR IGNORE INTO dag_runs
               (mission_id, task_description, state, attempt_count, max_retries, started_at, updated_at)
               VALUES (?, ?, 'PENDING', 0, ?, ?, ?)""",
            (mission_id, task_description, max_retries, now, now)
        )
        conn.commit()
    finally:
        conn.close()
    return mission_id


def update_dag_state(
    mission_id: str,
    state: str,
    attempt_count: Optional[int] = None,
    last_failure: Optional[Dict[str, Any]] = None,
    plan_hash: Optional[str] = None,
    completed: bool = False,
):
    """Atomically transition a DAG run to a new state and record metadata."""
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    fields = ["state = ?", "updated_at = ?"]
    params: list = [state, now]

    if attempt_count is not None:
        fields.append("attempt_count = ?")
        params.append(attempt_count)
    if last_failure is not None:
        fields.append("last_failure_json = ?")
        params.append(json.dumps(last_failure))
    if plan_hash is not None:
        fields.append("plan_hash = ?")
        params.append(plan_hash)
    if completed:
        fields.append("completed_at = ?")
        params.append(now)

    params.append(mission_id)
    conn.execute(f"UPDATE dag_runs SET {', '.join(fields)} WHERE mission_id = ?", params)
    conn.commit()
    conn.close()


def save_frozen_plan(mission_id: str, plan: Dict[str, Any], plan_hash: str):
    """Lock the Architect's change plan contract into plan_contracts and stamp the DAG run."""
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    conn.execute(
        """INSERT INTO plan_contracts (mission_id, plan_hash, plan_json, locked_at)
           VALUES (?, ?, ?, ?)""",
        (mission_id, plan_hash, json.dumps(plan), now)
    )
    conn.commit()
    conn.close()
    # Stamp hash on the dag_run row so integrity can be re-verified on resume
    update_dag_state(mission_id, "PLANNED", plan_hash=plan_hash)


def load_frozen_plan(mission_id: str) -> Optional[Dict[str, Any]]:
    """Load the most recently locked plan contract for a given mission."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT plan_json, plan_hash FROM plan_contracts WHERE mission_id = ? ORDER BY id DESC LIMIT 1",
        (mission_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"plan": json.loads(row["plan_json"]), "hash": row["plan_hash"]}
    return None


def get_dag_run(mission_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve the current state of a DAG run for crash-resume."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dag_runs WHERE mission_id = ?", (mission_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def fetch_dead_letter_items(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieve recent dead-letter queue entries for the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM dead_letter_queue ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def fetch_dag_runs(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieve recent DAG runs for the Mission Control dashboard panel."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM dag_runs ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
