import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from database import get_db_connection, init_db
import sqlite3

app = FastAPI(title="Lead Triage & Analytics Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

class LeadCreate(BaseModel):
    name: str
    company: str
    email: str
    budget: float

class LeadResponse(BaseModel):
    id: int
    name: str
    company: str
    email: str
    budget: float
    score: int
    status: str
    createdAt: str

class TriageRunResponse(BaseModel):
    processed_count: int
    qualified_count: int
    status: str

@app.get("/api/health", status_code=status.HTTP_200_OK)
def health_check():
    conn = get_db_connection()
    try:
        conn.execute("SELECT 1")
        return {"status": "healthy", "database": "connected", "engine": "SQLite"}
    finally:
        conn.close()

@app.get("/api/leads", response_model=List[LeadResponse])
def get_leads():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Lead ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        LeadResponse(
            id=row["id"],
            name=row["name"],
            company=row["company"],
            email=row["email"],
            budget=row["budget"],
            score=row["score"],
            status=row["status"],
            createdAt=str(row["createdAt"])
        ) for row in rows
    ]

@app.post("/api/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Lead (name, company, email, budget, status) VALUES (?, ?, ?, ?, 'PENDING')",
            (payload.name, payload.company, payload.email, payload.budget)
        )
        lead_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO AuditLog (action, leadId, details) VALUES ('LEAD_INGESTED', ?, ?)",
            (lead_id, f"Inbound lead received with budget ${payload.budget}")
        )
        conn.commit()
        
        cursor.execute("SELECT * FROM Lead WHERE id = ?", (lead_id,))
        new_row = cursor.fetchone()
        return LeadResponse(
            id=new_row["id"],
            name=new_row["name"],
            company=new_row["company"],
            email=new_row["email"],
            budget=new_row["budget"],
            score=new_row["score"],
            status=new_row["status"],
            createdAt=str(new_row["createdAt"])
        )
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Lead with this email already exists.")
    finally:
        conn.close()

@app.post("/api/triage/execute", response_model=TriageRunResponse)
def execute_triage():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Lead WHERE status = 'PENDING'")
    pending_leads = cursor.fetchall()
    
    processed = 0
    qualified = 0
    
    for lead in pending_leads:
        score = 50
        budget = lead["budget"]
        if budget >= 5000:
            score = 95
            status_val = "QUALIFIED"
            action = "ROUTE_TO_FOUNDER"
            qualified += 1
        elif budget >= 1500:
            score = 75
            status_val = "QUALIFIED"
            action = "AUTO_SCHEDULE"
            qualified += 1
        else:
            score = 30
            status_val = "DISQUALIFIED"
            action = "STANDARD_NURTURE"
            
        cursor.execute(
            "UPDATE Lead SET score = ?, status = ? WHERE id = ?",
            (score, status_val, lead["id"])
        )
        cursor.execute(
            "INSERT INTO AuditLog (action, leadId, details) VALUES (?, ?, ?)",
            (f"TRIAGE_{status_val}", lead["id"], f"Scored {score}/100. Action: {action}")
        )
        processed += 1
        
    conn.commit()
    conn.close()
    
    return TriageRunResponse(
        processed_count=processed,
        qualified_count=qualified,
        status="COMPLETE"
    )
