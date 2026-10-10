# Video #3 Production Script: Dual-Column A/B-Roll

**Target Video Runtime:** 11:30  
**Title:** How to Build Custom Autonomous Skills in Google Antigravity  
**Tone:** Masterclass, Authoritative, Code-First  
**Primary Visual:** Antigravity TUI + JetBrains Mono 18px Font  

| Timestamp | Spoken Dialogue (Voiceover / A-Roll) | Visual Cut / Screen Action / SFX |
| :--- | :--- | :--- |
| **0:00 – 0:18** | **The Retention Hook**<br>"Stop copying and pasting the same prompt into AI over and over again. Today, we're building custom, version-controlled autonomous AI skills natively inside Google Antigravity." | **A-Roll:** Eye-level camera delivery.<br>**SFX:** Mechanical keyboard stroke + UI chime. |
| **0:18 – 0:45** | **The Live Guard Demonstration**<br>"Watch what happens when an agent encounters a destructive SQL migration. Our custom skill /db-migration-guard intercepts the action, flags the missing index, and halts execution before any data is lost." | **Screen Capture:** Terminal running Mission Control. Red warning badge flashes: `[CRITICAL: Destructive DROP TABLE intercepted]`. |
| **00:45 – 02:30** | **Act 1: Anatomy of a Custom Skill Manifest**<br>"Every Antigravity skill lives inside .agents/skills/<skill-name>/SKILL.md. It requires YAML frontmatter defining name and description, followed by deterministic instruction sets." | **Editor Cut:** Zoom into `.agents/skills/db-migration-guard/SKILL.md`. Highlight YAML header lines 1–4. |
| **02:30 – 05:45** | **Act 2: Building `/api-contract-sync`**<br>"Next, let's create a skill that synchronizes backend Python FastAPI models with frontend Next.js TypeScript interfaces. No more silent runtime type mismatches." | **Screen Capture:** Creator types `mkdir -p .agents/skills/api-contract-sync` and drafts `SKILL.md`. Run slash command `/api-contract-sync`. |
| **05:45 – 08:30** | **Act 3: Building `/pr-readiness-audit`**<br>"Before pushing to GitHub, our third skill executes a 4-step quality gate: secret hygiene, Hadolint container audit, TypeScript compilation, and live health checks." | **Terminal Cut:** Execute `/pr-readiness-audit`. Watch green pass checkmarks populate pane. |
| **08:30 – 11:30** | **Act 4: Testing & Open-Source Download**<br>"We run our master pipeline check, verify our .agent symlink, and release all three custom skills open-source. Clone the repo from the link in the description, subscribe, and build your agent fleet." | **A-Roll:** Final sign-off with on-screen thumbnail end cards. |
