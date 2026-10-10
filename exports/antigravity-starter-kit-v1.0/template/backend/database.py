import sqlite3
from typing import Generator
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "leads.db"))

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Lead (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        budget REAL NOT NULL,
        score INTEGER DEFAULT 0,
        status TEXT DEFAULT 'PENDING',
        createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS TriageRule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        minBudget REAL NOT NULL,
        category TEXT NOT NULL,
        action TEXT NOT NULL,
        active INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS AuditLog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        leadId INTEGER,
        details TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (leadId) REFERENCES Lead (id)
    );
    """)
    
    # Seed baseline triage rules if table is empty
    cursor.execute("SELECT COUNT(*) FROM TriageRule")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO TriageRule (minBudget, category, action, active)
        VALUES (?, ?, ?, 1)
        """, [
            (5000.0, "ENTERPRISE", "ROUTE_TO_FOUNDER"),
            (1500.0, "MID_MARKET", "AUTO_SCHEDULE"),
            (0.0,    "SELF_SERVE", "STANDARD_NURTURE")
        ])
    conn.commit()
    conn.close()
