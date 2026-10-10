"""
services/analytics_service.py - Outlier calculation & 21-formula classification service.
"""

import os
import json
import re
from statistics import median
from typing import Dict, Any, List, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOOKS_PATH = os.path.join(WORKSPACE_ROOT, ".agents/skills/yt-script/hooks.json")


def load_hooks() -> List[Dict[str, Any]]:
    if os.path.isfile(HOOKS_PATH):
        with open(HOOKS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def classify_title(title: str, formulas: List[Dict[str, Any]]) -> str:
    for item in formulas:
        pattern = item.get("regex_pattern")
        if pattern and re.search(pattern, title):
            return item.get("name", "Custom")
    return "Custom Tactical / Direct"


def get_outliers(file_path: str, min_multiple: float = 2.0) -> Dict[str, Any]:
    full_path = os.path.join(WORKSPACE_ROOT, file_path) if not os.path.isabs(file_path) else file_path
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"Data file not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    formulas = load_hooks()
    by_channel = {}
    for entry in data:
        ch = entry.get("channel", "Unknown")
        by_channel.setdefault(ch, []).append(entry)

    outliers = []
    skipped = []

    for ch, vids in by_channel.items():
        if len(vids) < 4:
            skipped.append({"channel": ch, "count": len(vids)})
            continue

        counts = [int(v.get("views", 0)) for v in vids]
        ch_median = max(median(counts), 1)

        for v in vids:
            views = int(v.get("views", 0))
            mult = round(views / ch_median, 2)
            if mult >= min_multiple:
                outliers.append({
                    "title": v.get("title", ""),
                    "channel": ch,
                    "views": views,
                    "median": ch_median,
                    "multiple": mult,
                    "formula": classify_title(v.get("title", ""), formulas),
                    "url": v.get("url", "")
                })

    outliers.sort(key=lambda x: x["multiple"], reverse=True)
    return {
        "outliers": outliers[:10],
        "skipped": skipped,
        "total_analyzed": len(data),
        "gate": "ship it, or change it?"
    }
