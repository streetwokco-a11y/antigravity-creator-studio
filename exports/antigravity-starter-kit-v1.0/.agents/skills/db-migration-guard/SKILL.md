---
name: db-migration-guard
description: Automated SQL and Prisma database migration safety auditor. Scans migration scripts for destructive DROP TABLE/COLUMN operations, missing indexes on foreign keys, and un-migrated schema drift before deployment.
---

# Database Migration Guard (`/db-migration-guard`)

## Overview
This skill provides automated safety checks for database migrations (Prisma, SQL, Alembic, or TypeORM) before they are executed in production environments.

---

## 1. Safety Audit Checklist

When invoked, the agent MUST perform the following security & safety checks:

1. **Destructive SQL Operations Check:**
   - Scan migration files for `DROP TABLE`, `DROP COLUMN`, or `TRUNCATE`.
   - Flag any destructive operation as a **CRITICAL WARNING** requiring explicit developer confirmation.

2. **Foreign Key Indexing Audit:**
   - Verify that all foreign key columns (e.g., `leadId`, `userId`, `orgId`) have corresponding indexes defined (`CREATE INDEX` / `@index`).
   - Flag un-indexed foreign keys to prevent full table scans in production.

3. **Schema Drift Verification:**
   - Compare `schema.prisma` or migration files against the current SQLite/PostgreSQL schema.
   - Output diff analysis highlighting un-applied migrations.

---

## 2. Usage Instructions

Run this skill in Mission Control:
```bash
/db-migration-guard
```

Or prompt the agent:
> *"Audit our database migrations for destructive SQL operations and missing foreign key indexes."*
