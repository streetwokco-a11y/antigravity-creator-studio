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

    -- 3-Agent Mission Control DAG state machine (v2 schema)
    CREATE TABLE IF NOT EXISTS dag_runs (
        mission_id  TEXT PRIMARY KEY,
        workflow_name TEXT NOT NULL,
        current_state TEXT NOT NULL DEFAULT 'PENDING'
            CHECK(current_state IN
                ('PENDING','PLANNED','BUILT','AUDITING','SUCCESS','FAILED_DLQ','CRASHED')),
        retry_count   INTEGER DEFAULT 0,
        plan_hash     TEXT,
        started_at    TEXT NOT NULL,
        updated_at    TEXT NOT NULL,
        error_summary TEXT
    );

    CREATE TABLE IF NOT EXISTS plan_contracts (
        plan_hash  TEXT PRIMARY KEY,
        mission_id TEXT NOT NULL,
        plan_json  TEXT NOT NULL,
        locked_at  TEXT NOT NULL,
        FOREIGN KEY (mission_id) REFERENCES dag_runs(mission_id) ON DELETE CASCADE
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
# Mission Control DAG Persistence Layer (v2)
# ─────────────────────────────────────────────────────────────────────────────

def update_dag_state(
    mission_id: str,
    new_state: str,
    retry_count: Optional[int] = None,
    error: Optional[str] = None,
):
    """Atomically transition a DAG run to new_state, optionally recording retry
    count and error summary.  All writes go through this single function to
    keep state transitions auditable and crash-safe.
    """
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    if retry_count is not None:
        conn.execute(
            """UPDATE dag_runs
               SET current_state = ?, retry_count = ?, error_summary = ?, updated_at = ?
               WHERE mission_id = ?""",
            (new_state, retry_count, error, now, mission_id),
        )
    else:
        conn.execute(
            "UPDATE dag_runs SET current_state = ?, updated_at = ? WHERE mission_id = ?",
            (new_state, now, mission_id),
        )
    conn.commit()
    conn.close()


def store_plan_contract(mission_id: str, plan_hash: str, plan_dict: Dict[str, Any]):
    """Persist the Architect's frozen plan contract and advance state to PLANNED.
    INSERT OR IGNORE on plan_hash makes the operation idempotent.
    """
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    conn.execute(
        """INSERT OR IGNORE INTO plan_contracts
           (plan_hash, mission_id, plan_json, locked_at)
           VALUES (?, ?, ?, ?)""",
        (plan_hash, mission_id, json.dumps(plan_dict), now),
    )
    conn.execute(
        """UPDATE dag_runs
           SET plan_hash = ?, current_state = 'PLANNED', updated_at = ?
           WHERE mission_id = ?""",
        (plan_hash, now, mission_id),
    )
    conn.commit()
    conn.close()


def get_dag_checkpoint(mission_id: str) -> Optional[Dict[str, Any]]:
    """JOIN dag_runs + plan_contracts to produce a single re-hydration record.
    Returns None if the mission_id does not exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT d.*, p.plan_json
        FROM dag_runs d
        LEFT JOIN plan_contracts p ON d.plan_hash = p.plan_hash
        WHERE d.mission_id = ?
        """,
        (mission_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def fetch_dag_runs(limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieve recent DAG runs ordered newest-first (dashboard telemetry)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM dag_runs ORDER BY started_at DESC LIMIT ?", (limit,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


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
