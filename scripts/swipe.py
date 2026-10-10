#!/usr/bin/env python3
"""
YouTube Outlier Analyzer & Swipe File Engine (swipe.py)
Ranks videos by multiples over their own channel's median view count and classifies
titles against 21 proven viral title formulas.
"""

import sys
import os
import json
import re
import argparse
from statistics import median
from pathlib import Path

def resolve_hooks_path(custom_path=None):
    """Locate hooks.json across supported directory paths."""
    candidates = []
    if custom_path:
        candidates.append(Path(custom_path))
    candidates.extend([
        Path(".agents/skills/yt-script/hooks.json"),
        Path(".agents/skills/yt-viral/hooks.json"),
        Path("../yt-script/hooks.json"),
        Path("hooks.json"),
        Path(__file__).parent / "../.agents/skills/yt-script/hooks.json",
        Path(__file__).parent / ".agents/skills/yt-script/hooks.json",
        Path(__file__).parent / "hooks.json"
    ])
    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None

def load_formulas(hooks_path):
    if not hooks_path:
        return []
    try:
        with open(hooks_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Could not load formulas from {hooks_path}: {e}", file=sys.stderr)
        return []

def classify_title(title, formulas):
    """Match a video title against the 21 viral formulas using regex patterns."""
    for item in formulas:
        pattern = item.get("regex_pattern")
        if pattern and re.search(pattern, title):
            return item.get("name", "Unknown Formula")
    return "Custom Tactical / Direct"

def analyze_outliers(data, min_multiple=2.0, formulas=None):
    if formulas is None:
        formulas = []

    # Group by channel
    channel_videos = {}
    for entry in data:
        channel = entry.get("channel", "Unknown Channel")
        views = entry.get("views", 0)
        title = entry.get("title", "")
        url = entry.get("url", "")
        
        # Coerce view count to integer
        try:
            views = int(views)
        except (ValueError, TypeError):
            continue

        if channel not in channel_videos:
            channel_videos[channel] = []
        channel_videos[channel].append({
            "title": title,
            "views": views,
            "url": url,
            "channel": channel
        })

    outliers = []
    skipped_channels = []

    for channel, vids in channel_videos.items():
        if len(vids) < 4:
            skipped_channels.append((channel, len(vids)))
            continue

        view_counts = [v["views"] for v in vids]
        ch_median = median(view_counts)

        if ch_median <= 0:
            ch_median = 1  # Guard against division by zero

        for v in vids:
            mult = round(v["views"] / ch_median, 2)
            if mult >= min_multiple:
                formula_name = classify_title(v["title"], formulas)
                outliers.append({
                    "title": v["title"],
                    "url": v["url"],
                    "channel": channel,
                    "views": v["views"],
                    "median": ch_median,
                    "multiple": mult,
                    "formula": formula_name
                })

    # Sort descending by outlier multiple
    outliers.sort(key=lambda x: x["multiple"], reverse=True)
    return outliers, skipped_channels

def format_terminal(outliers, skipped_channels, min_multiple):
    lines = []
    lines.append("=" * 72)
    lines.append("  YOUTUBE OUTLIER ANALYZER & SWIPE FILE ENGINE (yt-viral)")
    lines.append("=" * 72)

    if skipped_channels:
        lines.append("\n[CHANNEL SAMPLE AUDIT]")
        for ch, count in skipped_channels:
            lines.append(f"  [SKIP] Channel '{ch}' has only {count} videos (minimum 4 required for statistical median).")

    lines.append(f"\n[RANKED OUTLIERS: >={min_multiple}x Channel Median]")
    if not outliers:
        lines.append("  No videos met the multiplier threshold.")
    else:
        top5 = outliers[:5]
        for i, o in enumerate(top5, 1):
            lines.append(f"\n  #{i}  [{o['multiple']}x MULTIPLE]  {o['title']}")
            lines.append(f"      Channel : {o['channel']} (Views: {o['views']:,} vs Median: {int(o['median']):,})")
            lines.append(f"      Formula : {o['formula']}")
            if o['url']:
                lines.append(f"      URL     : {o['url']}")

        # Extract common structural pattern
        formulas_seen = [o["formula"] for o in top5]
        most_common = max(set(formulas_seen), key=formulas_seen.count) if formulas_seen else "Direct Utility"

        lines.append("\n" + "-" * 72)
        lines.append("### The Structural Pattern")
        lines.append(f"  Top performers cluster around: '{most_common}'.")
        lines.append("  They replace broad conceptual promises with sharp constraints and clear negative framing.")
        lines.append("\n### Feasible Execution This Week")
        lines.append(f"  - Recommended Angle: Adapt the #{top5[0]['multiple']}x breakout pattern for your stack.")
        lines.append(f"  - Target Formula: {top5[0]['formula']}")
        lines.append("-" * 72)

    lines.append("\nship it, or change it?")
    return "\n".join(lines)

def format_markdown(outliers, skipped_channels, min_multiple):
    lines = []
    lines.append("# YouTube Niche Outlier Report: Top 5 Swipe File\n")
    if skipped_channels:
        lines.append("> **Sample Warnings:**")
        for ch, count in skipped_channels:
            lines.append(f"> - *[SKIP]* Channel `{ch}` had only {count} videos (minimum 4 required for statistical median).")
        lines.append("")

    lines.append(f"Ranking videos with $\\ge {min_multiple}\\times$ views over channel median baseline.\n")
    lines.append("| Rank | Multiple | Video Title | Channel Baseline | Matched Formula |")
    lines.append("|:---:|:---:|---|:---:|---|")

    top5 = outliers[:5]
    for i, o in enumerate(top5, 1):
        url_linked = f"[{o['title']}]({o['url']})" if o['url'] else o['title']
        lines.append(f"| **#{i}** | **{o['multiple']}x** | {url_linked} | {o['views']:,} vs {int(o['median']):,} med | {o['formula']} |")

    if top5:
        formulas_seen = [o["formula"] for o in top5]
        most_common = max(set(formulas_seen), key=formulas_seen.count)
        lines.append("\n### The Structural Pattern")
        lines.append(f"The top-performing videos cluster heavily around **{most_common}**.")
        lines.append("They avoid generic titles in favor of sharp negative constraints, quantifiable timeframe benchmarks, or high-stakes trade-offs.")
        lines.append("\n### Feasible Execution This Week")
        lines.append(f"- **Suggested Angle:** Adapt `{top5[0]['title']}` to your Antigravity / Agentic workflow.")
        lines.append(f"- **Framework Formula:** {top5[0]['formula']}")

    lines.append("\n---\nship it, or change it?")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="YouTube Outlier Analyzer & Swipe File Engine")
    parser.add_argument("file", help="Path to collected JSON video metadata file")
    parser.add_argument("--min", type=float, default=2.0, help="Minimum multiple over median (default: 2.0)")
    parser.add_argument("--hooks", type=str, default=None, help="Custom path to hooks.json")
    parser.add_argument("--format", choices=["terminal", "markdown", "json"], default="terminal", help="Output format")

    args = parser.parse_args()

    input_path = Path(args.file)
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse input JSON: {e}", file=sys.stderr)
        sys.exit(1)

    hooks_path = resolve_hooks_path(args.hooks)
    formulas = load_formulas(hooks_path)

    outliers, skipped = analyze_outliers(raw_data, min_multiple=args.min, formulas=formulas)

    if args.format == "json":
        print(json.dumps({"outliers": outliers, "skipped": skipped, "gate": "ship it, or change it?"}, indent=2))
    elif args.format == "markdown":
        print(format_markdown(outliers, skipped, args.min))
    else:
        print(format_terminal(outliers, skipped, args.min))

if __name__ == "__main__":
    main()
