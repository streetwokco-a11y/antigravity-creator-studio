# Video #1 Production Script: Dual-Column A/B-Roll

**Target Video Runtime:** 10:45  
**Title:** Stop Using AI Like an Autocomplete Toy (Google Antigravity)  
**Tone:** High-Energy, Contrarian, Technical Authority  
**Primary Visual:** Antigravity IDE (18px font) + PipeWire Terminal  

| Timestamp | Spoken Dialogue (Voiceover / A-Roll) | Visual Cut / Screen Action / SFX |
| :--- | :--- | :--- |
| **0:00 – 0:15** | **The Retention Hook**<br>"Stop treating AI like an autocomplete toy. If you're still typing every single line of code into VS Code, you're working in the past." | **A-Roll:** Direct camera eye contact. High energy.<br>**SFX:** Mechanical keyboard click stops with sub-bass drop. |
| **0:15 – 0:35** | **The Mission Control Proof**<br>"This is Google Antigravity running natively on Ubuntu Linux. Watch this: with one single command, three autonomous agents spin up in parallel." | **Screen Capture:** Zoom into Mission Control.<br>**Visual:** Execute `/youtube-dev-demo-prep`. 3 agent panes activate simultaneously. |
| **0:35 – 0:60** | **The Value Proposition**<br>"Agent one scaffolds our fullstack frontend and API routes. Agent two audits our Docker containers for security vulnerabilities. And Agent three validates our audio gain staging and production environment. Zero context switching. Zero manual glue code." | **Split-Screen:** 3-pane terminal execution running colored log streams (`scripts/task-01-fullstack.sh & scripts/task-02-docker.sh & scripts/task-03-ops.sh`). |
| **01:00 – 04:00** | **Act 1: Installing Antigravity on Ubuntu**<br>"Let's install Antigravity CLI natively on Ubuntu. We configure non-root Docker user permissions, set up the standard sandbox engine, and link our custom .agent/skills/ directory." | **Terminal Action:** Show `sudo snap install antigravity --classic`, `usermod -aG docker $USER`, and `ls -la .agent/skills/`. |
| **04:00 – 07:30** | **Act 2: Executing Parallel Multi-Agent Missions**<br>"Watch how Mission Control dispatches subagents without thread blocking. Agent Alpha scaffolds Prisma models while Agent Beta runs Hadolint static analysis on our Dockerfiles." | **Screen Capture:** Antigravity IDE with live progress indicators and parallel log outputs. |
| **07:30 – 09:45** | **Act 3: Live Verification & E2E Testing**<br>"We verify clean compilation with TypeScript, run health probes on FastAPI, and inspect our SQLite leads database with zero manual debugging." | **Browser Action:** Chromium UI rendering lead triage data live. |
| **09:45 – 10:45** | **Act 4: Outro & Repository Clone CTA**<br>"You can clone this complete .agent/skills/ repository pack from the link in the description. Hit subscribe, leave a comment with your current AI workflow, and let's automate your stack." | **A-Roll:** Final sign-off with end-card graphic links. |
