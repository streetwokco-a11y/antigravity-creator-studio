---
name: db-sharding-orchestrator
description: PostgreSQL zero-downtime database sharding and migration orchestrator. Automates declarative table partitioning, replication lag monitoring, pg_dump/pg_restore verification, and schema propagation across database fleets.
---

# DB Sharding Orchestrator (`/db-sharding-orchestrator`)

## Overview
This skill automates zero-downtime database sharding, table partitioning, and multi-node replication verification for PostgreSQL databases.

---

## 1. Sharding Protocol

When invoked, the agent MUST execute the following checks:

1. **Partition Key & Index Audit:**
   - Scan target tables for declarative partition keys (e.g. `tenant_id`, `created_at`).
   - Verify index alignment across primary and secondary shard nodes.

2. **Replication Lag & Zero-Downtime Migration:**
   - Monitor replication slot lag before cutover.
   - Verify dual-write shadow migration pipelines.

---

## 2. Usage Instructions

Run in Mission Control:
```bash
/db-sharding-orchestrator
```
