---
name: autonomous-fullstack-builder
description: End-to-end fullstack development workflow. Orchestrates database schema generation, API implementation, frontend UI assembly, and browser validation. Use when scaffolding new web apps or feature suites.
---
# Autonomous Fullstack Builder

## Goal
Scaffold and build a production-grade fullstack application or feature module from scratch with automated database models, REST/gRPC backend routes, reactive UI components, and browser verification.

## Step-by-Step Instructions

1. **Architecture Analysis & Plan Generation:**
   - Analyze user requirements and produce an architecture plan artifact detailing database schemas, API routes, and UI component hierarchy.

2. **Backend Data & API Layer:**
   - Scaffold models, migration scripts, and CRUD controllers.
   - Run local type checks and verify endpoints using `curl` or automated integration scripts.

3. **Frontend UI Layer:**
   - Build UI components with modern CSS, state management, and type safety.
   - Execute production bundle build (`npm run build` or framework equivalent) to verify compilation.

4. **E2E Browser Verification:**
   - Launch dev server and direct Antigravity browser tools to inspect pages, check console errors, and capture screenshot artifacts.

## Constraints
- Never commit unverified API signatures or broken types.
- Ensure all backend routes validate request body inputs cleanly.
