---
name: api-contract-sync
description: Automated OpenAPI and TypeScript API contract synchronizer. Validates backend Pydantic/FastAPI request and response schemas against frontend Next.js TypeScript interfaces to catch drift and type mismatches.
---

# API Contract Synchronizer (`/api-contract-sync`)

## Overview
This skill ensures zero type drift between backend API route schemas (FastAPI / Express / NestJS) and frontend client interfaces (Next.js App Router / React / TypeScript).

---

## 1. Synchronization Audit Protocol

When invoked, the agent MUST perform the following contract validation steps:

1. **Schema Extraction:**
   - Parse backend Pydantic models (e.g., `LeadCreate`, `LeadResponse`, `TriageRunResponse`) from `backend/main.py`.
   - Parse frontend TypeScript interfaces (e.g., `interface Lead`) from `frontend/app/page.tsx`.

2. **Field Mismatch & Type Drift Detection:**
   - Verify matching field names (e.g., `createdAt` vs `created_at`).
   - Verify matching data types (e.g., `number` in TypeScript vs `float` in Python).
   - Report any missing or optional fields.

3. **OpenAPI Schema Generation:**
   - Export OpenAPI `openapi.json` from the running backend engine.
   - Verify client fetch endpoints against path parameters.

---

## 2. Usage Instructions

Run this skill in Mission Control:
```bash
/api-contract-sync
```

Or prompt the agent:
> *"Audit backend FastAPI endpoints and frontend Next.js TypeScript interfaces for schema drift."*
