---
name: youtube-dev-demo-prep
description: Prepares codebases for screen recordings. Resets databases, seeds mock data, sets large readable terminal fonts (18px), cleans git history, and stages parallel agent demo tasks.
---
# YouTube Dev Demo Preparer

## Goal
Seed and sanitize the workspace environment specifically for recording clean, high-impact YouTube video demonstrations without permission errors or leftover artifacts.

## Step-by-Step Instructions

1. **Environment Reset & Mock Seeding:**
   - Reset local test databases and populate realistic, high-contrast mock data.
   - Scrub sensitive credentials and replace `.env` files with safe demo defaults.

2. **IDE & Terminal Formatting:**
   - Configure terminal font size to minimum **18px** (JetBrains Mono / Fira Code).
   - Set editor tab size to 2, hide status bars, sidebars, and unnecessary notification clutter.

3. **Staged Demo Task Queue:**
   - Stage 3 parallel subagent tasks in Mission Control (e.g. Backend API builder, Frontend UI assembler, Docker deploy validator).
   - Generate initial demo plan artifact in `.gemini/antigravity/brain/` without permission errors.

## Constraints
- Must complete workspace staging cleanly without requiring root privileges.
