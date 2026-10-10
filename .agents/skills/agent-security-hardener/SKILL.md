---
name: agent-security-hardener
description: Zero-trust AI agent security and sandbox hardener. Audits agent system prompts against jailbreaks and prompt injection vulnerabilities, enforces gVisor/firecracker sandbox boundaries, and inspects egress network rules.
---

# Agent Security Hardener (`/agent-security-hardener`)

## Overview
This skill hardens autonomous AI agents against prompt injection attacks, privilege escalation, and unintended system commands.

---

## 1. Zero-Trust Security Audit

When invoked, the agent MUST run:

1. **Prompt Injection & Jailbreak Defense Scan:**
   - Scan agent system prompts for delimiter enforcement and instruction override defenses.

2. **Sandbox & Egress Network Policy Check:**
   - Verify non-root execution (`BypassSandbox: false` enforcement).
   - Audit outbound network egress rules.

---

## 2. Usage Instructions

Run in Mission Control:
```bash
/agent-security-hardener
```
