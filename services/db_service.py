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
        status TEXT NOT NULL,          -- SUCCESS, FAILED, RUNNING
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
        verdict TEXT NOT NULL,         -- PASS, FAIL, WARN
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
