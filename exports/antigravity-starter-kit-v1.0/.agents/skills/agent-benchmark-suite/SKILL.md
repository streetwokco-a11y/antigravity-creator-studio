---
name: agent-benchmark-suite
description: Autonomous benchmark runner comparing single-turn AI IDE completion against multi-agent Google Antigravity workflows across speed, test coverage, type safety, and security linting.
---

# Agent Benchmark Suite (`/agent-benchmark-suite`)

## Overview
This skill provides standard head-to-head benchmarking metrics comparing single-turn AI inline completion against autonomous multi-agent orchestration.

---

## 1. Benchmark Execution Protocol

When invoked, the agent MUST evaluate and report metrics across 4 core engineering categories:

1. **Fullstack Scaffolding Velocity (Time-to-Green):**
   - Measure seconds elapsed to generate Prisma schema, REST API routes, and React UI components.
   - Record compilation errors requiring manual human intervention.

2. **Security & Hadolint Compliance Rate:**
   - Scan container Dockerfiles for `USER appuser` non-root enforcement and `HEALTHCHECK` directives.
   - Score security posture out of 100.

3. **Type Safety & Schema Synchronization:**
   - Audit Pydantic backend models against TypeScript frontend interfaces.
   - Flag any missing attributes or type mismatches.

4. **Parallel Execution Efficiency:**
   - Measure CPU/RAM efficiency and task completion across multi-agent background tasks vs single-threaded loopers.

---

## 2. Usage Instructions

Run this skill in Mission Control:
```bash
/agent-benchmark-suite
```

Or prompt the agent:
> *"Run the side-by-side agent benchmark suite and output comparative performance metrics."*
