---
name: yt-viral
description: Find what is actually working in the user's niche on YouTube and rank it by how far each video beat its own channel, then name the formula. Use for "what's working right now", "find viral videos in my niche", "why did this blow up", competitor research, or a swipe file.
version: 1.0.0
tags: [youtube, viral, research, outliers, swipe-file, analytics]
---

# YouTube Outlier Analyzer & Swipe File Engine (`yt-viral`)

Detect breakout outlier videos in any target niche by ranking videos based on multiples over each channel's own median views rather than raw vanity view counts. Identifies disproportionate resonance regardless of channel subscriber scale.

## Core Math & Baseline Rules

1. **Median Baseline Requirement:**
   - A channel must contain at least **4 videos** in the input dataset to establish a statistically defensible median baseline.
   - Any channel with $< 4$ videos must be skipped with an explicit warning log:
     ```text
     [SKIP] Channel '<name>' has only N videos (minimum 4 required for statistical median).
     ```

2. **Outlier Multiple Formula:**
   $$\text{Multiple} = \frac{\text{Video Views}}{\text{Channel Median Views}}$$
   *(Rounded to two decimal places).*

3. **Formula Classification:**
   - Every video with $\text{Multiple} \ge \text{threshold}$ (default: $2.0\times$) is evaluated against the 21 viral title formulas defined in `../yt-script/hooks.json`.

---

## Operational Workflow

1. **Ingest Public Metadata:**
   - Ingest JSON list format containing `title`, `views` (integer), `channel`, and `url`.
   - Data can be generated using public dumps or CLI tools:
     ```bash
     yt-dlp --flat-playlist -J "https://www.youtube.com/@channel/videos" > dump.json
     ```

2. **Execute Engine:**
   ```bash
   python3 swipe.py data/collected.json --min 2.0
   ```

3. **Analyze Structural Commonalities:**
   - Identify the single structural element shared across the top outliers (e.g., negative framing, concrete numerical time constraints, or named authority contrasts).

4. **Formulate Weekly Execution Recommendation:**
   - Translate top-performing patterns into a runnable, production-ready video concept matching the creator's tech stack.

5. **Mandatory Closing Gate:**
   - Every output report must strictly terminate with:
     ```text
     ship it, or change it?
     ```

---

## Output Report Specification

The tool outputs a structured Top 5 report:

```markdown
# YouTube Niche Outlier Report: Top 5 Swipe File

| Rank | Outlier Multiple | Video Title | Channel Baseline | Matched Formula |
|:---:|:---:|---|:---:|---|
| **#1** | **4.82x** | Title Here | 48.2k vs 10.0k med | Formula Name |
| **#2** | **3.50x** | Title Here | 35.0k vs 10.0k med | Formula Name |
...

### The Structural Pattern
[The ONE core structural mechanism uniting the top outliers]

### Feasible Execution This Week
- **Proposed Title:** ...
- **Angle / Concept:** ...
- **Core Hook:** ...

---
ship it, or change it?
```
