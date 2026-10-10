---
name: pr-readiness-audit
description: Automated pre-PR readiness auditor. Executes static analysis, Hadolint Docker security checks, unit test pass verification, and git secret scanning before creating a GitHub pull request.
---

# PR Readiness Auditor (`/pr-readiness-audit`)

## Overview
This skill acts as a automated quality gate before opening a Pull Request or pushing code to main repositories.

---

## 1. Quality Gate Inspection Criteria

When invoked, the agent MUST run the following 4-step QA audit:

1. **Secret & Hygiene Scan:**
   - Verify that no `.env`, API keys, or raw passwords are stage in git commit history.
   - Confirm `.gitignore` includes `venv/`, `node_modules/`, and SQLite `.db` files.

2. **Docker & Container Security:**
   - Execute Hadolint checks on `Dockerfile`.
   - Verify non-root `USER appuser` execution and mandatory `HEALTHCHECK` directive.

3. **Type Checking & Static Analysis:**
   - Execute TypeScript compiler check (`tsc --noEmit`).
   - Run Python static analysis (`flake8` / `ruff`).

4. **Test Pass Rate Verification:**
   - Run API health check probe and backend test suite (`pytest` / `curl`).

---

## 2. Usage Instructions

Run this skill in Mission Control:
```bash
/pr-readiness-audit
```

Or prompt the agent:
> *"Audit workspace readiness for a GitHub Pull Request."*
