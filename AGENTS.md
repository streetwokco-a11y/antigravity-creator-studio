# AGENTS.md - Antigravity Agent Directives & System Rules

## Overview
This document specifies operational standards, system protocols, subagent invocation guidelines, and environment policies for all autonomous AI coding agents operating within the YouTube channel workspace.

---

## 1. Workspace & Directory Conventions
- **Root Directory:** Workspace root is `/home/rockyy/oct catalog/youtube channel`.
- **Skills Directory:** Canonical singular path for project-specific skills is `.agents/skills/<skill-name>/SKILL.md`.
- **Artifacts:** Store task plans, architecture specs, and walkthroughs under `.gemini/antigravity/brain/<conversation-id>/`.

---

## 2. Agent Execution Rules & Conventions
- **Never Guess Schemas or Paths:** Always use search and file reading tools to inspect source files before writing or editing code.
- **Obey Explicit Directives:** Enforce quantitative thresholds, audio/video specifications, and layout rules strictly as requested.
- **No Masking Runtime Errors:** Never silence exceptions, return dummy data, or comment out failing assertions to hide errors. Fix root causes.
- **Strict Linting & Build Verification:** After creating or updating code files, run static analysis and tests immediately to ensure clean compilation.

---

## 3. Subagent Delegation & Orchestration
- **Specialized Subagents:** Delegate complex sub-tasks (e.g. security audits, accessibility reviews, rules authoring) to domain-specific subagents.
- **Parallel Execution:** When executing multi-agent tasks (e.g., Mission Control B-roll demos), ensure separate task IDs and independent state tracking.
- **Reactive Messages:** Rely on system notifications when background tasks complete rather than polling status loops.

---

## 4. Environment & Security Sandboxing
- **Sandboxed Execution First:** Run shell commands inside standard sandbox environments (`BypassSandbox: false`) unless network access or system binaries explicitly require approval.
- **Non-Root & Security Audits:** Container deployment code must enforce non-root execution (`USER appuser`) and include HEALTHCHECK directives.
- **Secret Hygiene:** Never commit `.env` files, API keys, or raw credentials to repository history.

---

## 5. Available Slash Commands & Skills
All custom skills under `.agents/skills/` are automatically exposed as slash commands in the `agy` TUI:

| Slash Command | Purpose |
| :--- | :--- |
| `/autonomous-fullstack-builder` | End-to-end fullstack web application scaffolding and browser testing |
| `/docker-deploy-validator` | Dockerfile security audit, Hadolint checks, and docker compose validation |
| `/youtube-dev-demo-prep` | Seed workspace, reset test DB, format IDE fonts (18px), stage 3 parallel demo tasks |
| `/youtube-niche-research` | Phase 1: High RPM developer content niche analysis ($22–$38+ RPM target) |
| `/youtube-trend-research` | Phase 1: AI coding breakout trend tracking (Antigravity, Gemini 3, agentic tools) |
| `/youtube-ideation-strategy` | Phase 1: Search vs Browse video topic matrix mapping |
| `/youtube-scriptwriting` | Phase 2: Dual-column A/B-roll scriptwriting with 60s retention hooks |
| `/youtube-shorts-creator` | Phase 2: 45-second vertical Short creation with infinite loop design |
| `/youtube-ai-production` | Phase 3: AI thumbnail prompts (16:9 Midjourney/Flux) & ElevenLabs SSML direction |
| `/youtube-packaging-seo` | Phase 4: Title variants, mobile thumbnail briefs, timestamps, and tags |
| `/youtube-channel-ops` | Phase 5: Audio normalization (-14 LUFS), OBS PipeWire checks, Content ID safety |
| `/youtube-growth-analytics` | Phase 6: Retention curve audit, drop-off analysis, newsletter repurposing |
| `/youtube-master-pipeline` | Full end-to-end 6-phase channel automation orchestrator |
| `/yt-viral` | Computes median-relative view multiples (>= 2.0x) and matches titles against 21 formulas to output a swipe file |
| `/yt-script` | Proven 21-formula viral title and hook taxonomy for high-CTR video ideation and packaging |
