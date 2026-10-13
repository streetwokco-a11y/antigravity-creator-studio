# 🎬 Antigravity Creator Studio

> **The first autonomous production operating system combining cryptographic multi-agent orchestration with broadcast-grade DSP media compliance.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/protocol-FastMCP%20%7C%20JSON--RPC-emerald.svg)](https://modelcontextprotocol.io/)
[![Broadcast Compliance](https://img.shields.io/badge/audio-EBU%20R128%20(-14%20LUFS)-rose.svg)](https://tech.ebu.ch/loudness)
[![State Machine](https://img.shields.io/badge/persistence-SQLite%20WAL-amber.svg)](https://sqlite.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/streetwokco-a11y/antigravity-creator-studio?style=social)](https://github.com/streetwokco-a11y/antigravity-creator-studio)

---

## Why Antigravity Studio?

Most multi-agent frameworks either simulate a software firm in text buffers (MetaGPT, CrewAI) or provide raw graph primitives without media primitives (LangGraph).

**Antigravity Creator Studio combines both sides of the coin:**

| What Every Framework Has | What Only We Have |
|---|---|
| Multi-agent task delegation | **SHA-256 Immutability Gate** — cryptographic proof no agent mutated the Architect's contract |
| Retry loops | **Crash-resumable SQLite WAL** state machine with `CHECK`-constrained transitions |
| CI/test gates | **EBU R128 `-14 LUFS` + `60 fps` broadcast compliance** as a first-class Auditor gate |
| Workflow automation | **YouTube YPP monetization policy compliance** service before every upload |
| API server | **FastMCP JSON-RPC 2.0 stdio gateway** — your entire studio callable as an LLM tool suite |
| Content publishing | **Omni-channel dispatch** — YouTube + X + LinkedIn + Newsletter in one pipeline |

> *The only open-source creator studio with a cryptographic immutability gate, EBU R128 broadcast QA, and YPP compliance checks built into the same autonomous pipeline.*

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│              ANTIGRAVITY CREATOR STUDIO v2.6                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [MISSION TRIGGER]  ──►  studio_server.py  ──►  mcp_server.py     │
│          │                  FastAPI REST           FastMCP          │
│          │                  3-Col Dashboard        JSON-RPC 2.0     │
│          ▼                                                          │
│   ┌─────────────────────┐                                           │
│   │  AGENT 1: ARCHITECT │  SHA-256 FrozenPlan → plan_contracts      │
│   └──────────┬──────────┘                                           │
│              │ state: PLANNED (hash locked)                         │
│              ▼                                                      │
│   ┌─────────────────────┐                                           │
│   │  AGENT 2: BUILDER   │◄──── AuditorReport (remediation loop)    │
│   │  Immutability Gate  │      max 3 retries                        │
│   └──────────┬──────────┘                                           │
│              │ state: BUILT                                         │
│              ▼                                                      │
│   ┌─────────────────────┐  5-Check Sandboxed Audit:                │
│   │  AGENT 3: AUDITOR   │  hadolint → flake8 → bandit              │
│   │                     │  → pytest → verify-export.sh             │
│   └──────────┬──────────┘  (-14 LUFS / 60 fps gate)               │
│              │                                                      │
│       Pass? ─┴──────────────────────────────────┐                  │
│       ▼ Yes                                     ▼ No (×3)          │
│   [SUCCESS]                             [DEAD-LETTER QUEUE]        │
│   state: SUCCESS                        state: FAILED_DLQ          │
│   ↓                                     ↓                          │
│   YPP Compliance → Normalize → Stitch → Dispatch                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                          │
                    studio.db (SQLite WAL)
            dag_runs · plan_contracts · qa_audits
            runs · publications · dead_letter_queue
```

### State Machine Transitions

```
PENDING → PLANNED → BUILT ↔ AUDITING → SUCCESS
                                     ↘ FAILED_DLQ  (retries exhausted)
                                     ↘ CRASHED      (unhandled exception)
```

All transitions are persisted atomically to `studio.db` **before** yielding — enabling crash-resume from the exact boundary where a pipeline died.

---

## Feature Matrix

### 🤖 3-Agent Mission Control DAG (`scripts/mission_control_dag.py`)

| Mechanic | Implementation |
|---|---|
| **Immutability Gate** | `FrozenPlan(frozen=True)` — `compute_hash()` SHA-256 fingerprint verified before every Builder write |
| **Crash Resume** | `resume_from_checkpoint(mission_id)` — JOIN re-hydration from `studio.db` |
| **5-Check Sandboxed Auditor** | `hadolint` → `flake8` → `bandit` → `pytest` → `verify-export.sh` each in clean subprocess |
| **Structured Rejection** | `AuditorReport` dataclass — `verdict`, `check_name`, `failed_assertion`, `remediation_instruction` |
| **Dead-Letter Queue** | After `max_retries`, full diff → `dead_letter_queue` table + dashboard alert |

### 📡 MCP Gateway (`mcp_server.py`)

FastMCP + Stdio JSON-RPC 2.0 server — makes the entire studio callable as an LLM tool suite:

| Tool | Description |
|---|---|
| `video_audit` | EBU R128 loudness + framerate compliance check |
| `run_swipe_analysis` | Outlier detection against 21 viral formulas |
| `trigger_pipeline` | Full hands-off content pipeline (research → stitch → publish) |
| `get_dead_letter_queue` | Inspect failed missions |
| `resume_mission` | Crash-resume a DAG mission by ID |

### 🎚️ Broadcast-Grade DSP (`services/media_service.py`)

- **EBU R128 two-pass `loudnorm`** — targets `-14.0 LUFS` integrated, `-1.0 dBTP` true peak, `7.0 LRA`
- **Pre-flight loudness gate** before ffmpeg pass
- **60 fps frame-rate verification** via `ffprobe`
- All metrics written to `qa_audits` SQLite table for trend analysis

### 📊 Analytics Engine (`services/analytics_service.py`)

- **Outlier detection** — computes median-relative view multiples (threshold ≥ 2.0×)
- **21 viral formula classifier** — matches title against proven CTR formulas
- **Niche intelligence** — scans public video manifests from developer channels

### 🛡️ YPP Compliance (`services/compliance_service.py`)

Automated pre-upload policy audit:
- Reused/repetitious content detection
- Advertiser-friendliness score
- Commentary uniqueness verification
- Copyright flag risk assessment

### 🚀 Omni-Channel Dispatch (`services/dispatch_service.py`)

| Platform | Method |
|---|---|
| YouTube | Data API v3 — upload, set privacy, add chapters |
| X (Twitter) | REST API v2 — thread-formatted posts |
| LinkedIn | Share API — professional post with thumbnail |
| Newsletter | Email API — Markdown → HTML repurpose |

---

## Project Structure

```
antigravity-creator-studio/
├── studio.db                      # SQLite WAL state store
├── pyproject.toml                 # Deterministic dependency manifest
├── studio_server.py               # FastAPI server + 3-column dashboard
├── mcp_server.py                  # FastMCP JSON-RPC 2.0 gateway
│
├── scripts/
│   ├── mission_control_dag.py     # 3-agent DAG orchestrator ← START HERE
│   ├── swipe.py                   # Viral outlier analyzer
│   ├── verify-export.sh           # EBU R128 / 60fps QA gate
│   ├── collect-niche.sh           # Public metadata ingestion
│   ├── youtube-upload.sh          # YouTube Data API v3 uploader
│   └── master-pipeline.sh         # Full 6-phase automation
│
├── services/
│   ├── db_service.py              # SQLite persistence + DAG state machine
│   ├── media_service.py           # EBU R128 loudness + ffprobe QA
│   ├── analytics_service.py       # Outlier engine + viral classifier
│   ├── compliance_service.py      # YPP monetization policy auditor
│   ├── stitch_service.py          # Headless FFmpeg video assembly
│   ├── dispatch_service.py        # Multi-platform API distribution
│   ├── scheduler_service.py       # Autonomous task scheduler
│   ├── qa_service.py              # Pre-flight preflight harness
│   └── resilience.py              # Retry decorators + DLQ routing
│
├── .agents/skills/                # Antigravity slash-command skills
│   ├── yt-script/                 # 21-formula viral title taxonomy
│   ├── yt-viral/                  # Median-relative outlier ranker
│   ├── youtube-master-pipeline/   # 6-phase channel orchestrator
│   └── ...                        # 15 more production skills
│
└── data/
    └── niche_collected.json       # Aggregated public channel intelligence
```

---

## Quick Start

### Prerequisites

```bash
# Required system tools
sudo apt install ffmpeg sqlite3 python3.11

# Optional audit tools (Auditor checks gracefully skip if absent)
sudo apt install hadolint
pip install bandit flake8 pytest
```

### Installation

```bash
git clone https://github.com/streetwokco-a11y/antigravity-creator-studio.git
cd antigravity-creator-studio

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # or: pip install -e .
```

### Start the Studio Dashboard

```bash
python studio_server.py
# → http://localhost:8000
```

### Run a Mission Control DAG

```bash
# New mission — full 3-agent pipeline
python scripts/mission_control_dag.py \
    --task "Build lead triage FastAPI backend with schema validation" \
    --retries 3

# Crash-resume from last SQLite checkpoint
python scripts/mission_control_dag.py \
    --resume \
    --mission-id <UUID>

# Custom retry limit
python scripts/mission_control_dag.py --task "..." --retries 5
```

### Trigger via REST API

```bash
# Spawn a mission (non-blocking, runs in background)
curl -X POST "http://localhost:8000/api/mission/dag/trigger" \
     -G --data-urlencode "task=Build lead triage API" \
        --data-urlencode "retries=3"

# Check live mission state
curl http://localhost:8000/api/mission/dag/runs

# Resume a crashed mission
curl -X POST "http://localhost:8000/api/mission/dag/resume/<mission_id>"
```

### Inspect the State Machine

```bash
# Live DAG run state
sqlite3 studio.db \
  "SELECT mission_id, current_state, retry_count, plan_hash FROM dag_runs ORDER BY started_at DESC LIMIT 5;"

# Locked plan contracts
sqlite3 studio.db \
  "SELECT plan_hash, substr(plan_json,1,80) FROM plan_contracts LIMIT 5;"

# Dead-letter queue
sqlite3 studio.db \
  "SELECT service_name, retries_attempted, error_message FROM dead_letter_queue ORDER BY id DESC LIMIT 5;"
```

---

## REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | 3-column studio dashboard |
| `GET` | `/api/status` | Full preflight audit (skills, PipeWire, symlinks) |
| `GET` | `/api/runs` | Latest QA audit runs |
| `POST` | `/api/mission/dag/trigger` | Spawn new DAG mission (background) |
| `POST` | `/api/mission/dag/resume/{id}` | Crash-resume from DB checkpoint |
| `GET` | `/api/mission/dag/runs` | Live DAG telemetry feed |
| `GET` | `/api/qa/audit?path=…` | EBU R128 + framerate audit |
| `GET` | `/api/qa/autofix?path=…` | Auto-normalize audio to -14 LUFS |
| `GET` | `/api/swipe` | Viral outlier analysis on collected data |
| `GET` | `/api/compliance/{num}` | YPP policy audit for episode N |
| `GET` | `/api/render-headless` | Headless FFmpeg stitch (landscape/short) |
| `GET` | `/api/dispatch/{num}/{platform}` | Push episode to X / LinkedIn / Newsletter |
| `GET` | `/api/upload` | YouTube Data API v3 upload |
| `GET` | `/api/scheduler/run-now` | Trigger full hands-off pipeline |

---

## SQLite Schema

```sql
-- Crash-resumable DAG state machine
CREATE TABLE dag_runs (
    mission_id    TEXT PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    current_state TEXT NOT NULL DEFAULT 'PENDING'
        CHECK(current_state IN
            ('PENDING','PLANNED','BUILT','AUDITING','SUCCESS','FAILED_DLQ','CRASHED')),
    retry_count   INTEGER DEFAULT 0,
    plan_hash     TEXT,           -- SHA-256 Immutability Gate fingerprint
    started_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    error_summary TEXT
);

-- Locked Architect contracts (INSERT OR IGNORE — idempotent)
CREATE TABLE plan_contracts (
    plan_hash  TEXT PRIMARY KEY,
    mission_id TEXT NOT NULL,
    plan_json  TEXT NOT NULL,
    locked_at  TEXT NOT NULL,
    FOREIGN KEY (mission_id) REFERENCES dag_runs(mission_id) ON DELETE CASCADE
);

-- Broadcast-grade QA metrics per export
CREATE TABLE qa_audits (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path       TEXT NOT NULL,
    integrated_lufs REAL,   -- Target: -14.0
    true_peak       REAL,   -- Target: < -1.0 dBTP
    lra             REAL,
    framerate       REAL,   -- Target: 60.0
    verdict         TEXT NOT NULL,  -- PASS | FAIL | WARN
    created_at      TEXT NOT NULL
);

-- Permanent failure isolation
CREATE TABLE dead_letter_queue (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name      TEXT NOT NULL,
    payload_json      TEXT NOT NULL,
    error_message     TEXT NOT NULL,
    retries_attempted INTEGER NOT NULL,
    created_at        TEXT NOT NULL
);
```

---

## The 3-Agent DAG Explained

### Why Not LangGraph / CrewAI?

Those frameworks excel at agent *communication* but don't solve the **Context Degradation & Hallucination Drift** problem at the state-persistence layer. When a single model designs, writes, tests, and reviews in one long context stream, attention weights decay — constraints get forgotten, variable names drift, edge cases get bypassed.

Antigravity Studio decouples these concerns **architecturally**:

```python
# Agent 1: Architect — produces a cryptographically locked contract
plan = FrozenPlan(frozen=True)        # Python raises FrozenInstanceError on mutation
plan_hash = plan.compute_hash()       # SHA-256 fingerprint
store_plan_contract(mission_id, plan_hash, plan)   # Locked in plan_contracts table

# Agent 2: Builder — verified against the locked hash before every write
live_hash = self.plan.compute_hash()
if live_hash != self.plan_hash:
    raise RuntimeError("IMMUTABILITY GATE VIOLATION")   # Pipeline halts

# Agent 3: Auditor — 5 independent subprocess checks, never on host OS
checks = [hadolint, flake8, bandit, pytest, verify_export]
# Each check returns an AuditorReport with remediation_instruction
# Failure feeds back to Agent 2 as a targeted correction directive
# After max_retries → dead_letter_queue, never silent failure
```

### State Transition Guarantees

Every `update_dag_state()` call goes through a single function that:
1. Updates `current_state` + `updated_at` atomically
2. Records `retry_count` and `error_summary` on failure
3. Uses SQLite WAL mode — concurrent readers never block the writer
4. Enforces the `CHECK` constraint at the DB engine level — invalid state is physically impossible

---

## Available Slash Commands

When running inside the Antigravity IDE (`agy` TUI), all `.agents/skills/` are auto-exposed:

| Command | Description |
|---|---|
| `/youtube-master-pipeline` | Full 6-phase channel automation orchestrator |
| `/yt-viral` | Median-relative outlier analysis (≥ 2.0× threshold) |
| `/yt-script` | 21-formula viral title and hook taxonomy |
| `/youtube-scriptwriting` | Dual-column A/B-roll script with 60s retention hook |
| `/youtube-shorts-creator` | 45-second vertical Short with infinite loop design |
| `/youtube-packaging-seo` | Title variants, mobile thumbnail briefs, timestamps |
| `/youtube-channel-ops` | Audio normalization (-14 LUFS), OBS PipeWire checks |
| `/youtube-growth-analytics` | Retention curve audit, drop-off analysis |
| `/docker-deploy-validator` | Dockerfile security audit + Hadolint + Compose validation |

---

## Comparison vs. Top Open-Source Alternatives

| Feature | Antigravity | MetaGPT | CrewAI | LangGraph | MoneyPrinterTurbo |
|---|---|---|---|---|---|
| Multi-agent DAG | ✅ | ✅ | ✅ | ✅ | ❌ |
| SHA-256 Immutability Gate | ✅ | ❌ | ❌ | ❌ | ❌ |
| Crash-resume from SQLite | ✅ | ❌ | ❌ | ✅ | ❌ |
| EBU R128 inside CI gate | ✅ | ❌ | ❌ | ❌ | ❌ |
| YPP compliance service | ✅ | ❌ | ❌ | ❌ | ❌ |
| MCP JSON-RPC gateway | ✅ | ❌ | ❌ | ❌ | ❌ |
| Omni-channel dispatch | ✅ | ❌ | ❌ | ❌ | ❌ |
| Dead-letter queue | ✅ | ❌ | ❌ | Partial | ❌ |
| `CHECK`-constrained state | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## Environment Variables

```bash
# YouTube
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...

# Distribution
TWITTER_BEARER_TOKEN=...
LINKEDIN_ACCESS_TOKEN=...
NEWSLETTER_API_KEY=...

# AI (optional — pipeline runs in offline simulation mode without these)
GEMINI_API_KEY=...
ELEVENLABS_API_KEY=...
```

> **Never commit `.env` files.** All secrets are loaded from environment variables only.

---

## Roadmap

- [ ] **`AWAITING_APPROVAL` state** — human-in-the-loop gate between Auditor PASS and SUCCESS (`interrupt()` pattern)
- [ ] **Docker ephemeral Auditor** — replace subprocess with isolated container for zero environmental contamination
- [ ] **TTS provider abstraction** — `EdgeTTS` / `ElevenLabs` / `Chatterbox` pluggable without touching `stitch_service.py`
- [ ] **SSE real-time DAG events** — push live state transitions to dashboard Column 1 via `StreamingResponse`
- [ ] **Whisper SRT subtitle burn-in** — auto-timed captions baked into every export
- [ ] **Visual DAG renderer** — interactive graph view of pipeline state in the dashboard
- [ ] **LLM Root Cause Analysis** — feed FFmpeg/pytest stderr to a diagnostic agent → auto-suggest fix
- [ ] **Ken Burns `zoompan` FFmpeg filter** — dynamic motion for static B-roll images
- [ ] **Alembic migrations** — schema versioning for `studio.db` without manual SQL drops

---

## License

MIT — see [LICENSE](LICENSE).

---

## Acknowledgements

Built on the shoulders of:

- [FastMCP](https://github.com/jlowin/fastmcp) — Model Context Protocol server framework
- [FastAPI](https://fastapi.tiangolo.com/) — async Python API framework
- [FFmpeg](https://ffmpeg.org/) — multimedia processing engine
- [EBU R128](https://tech.ebu.ch/loudness) — broadcast loudness standard
- [SQLite WAL](https://sqlite.org/wal.html) — write-ahead logging for concurrent access

---

<div align="center">

**[Dashboard](http://localhost:8000)** · **[API Docs](http://localhost:8000/docs)** · **[GitHub](https://github.com/streetwokco-a11y/antigravity-creator-studio)**

*Built with Google Antigravity · Powered by the 3-agent DAG engine*

</div>
