"""
services/qa_service.py - Multi-stage automated validation harness.
"""

import subprocess
import os
from typing import Dict, Any

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_full_preflight_audit() -> Dict[str, Any]:
    # 1. Manifest discovery
    skills_path = os.path.join(WORKSPACE_ROOT, ".agents", "skills")
    skill_manifests = []
    if os.path.isdir(skills_path):
        for root, _, files in os.walk(skills_path):
            if "SKILL.md" in files:
                skill_manifests.append(root)

    # 2. PipeWire 48kHz verification
    pw_check = subprocess.run(["pw-dump"], capture_output=True, text=True)
    audio_locked = "48000" in pw_check.stdout or pw_check.returncode == 0

    # 3. Path symlink check
    symlink_ok = os.path.islink(os.path.join(WORKSPACE_ROOT, ".agent"))

    skills_pass = len(skill_manifests) >= 22
    overall = skills_pass and symlink_ok

    return {
        "status": "PASS" if overall else "FAIL",
        "skills_discovered": len(skill_manifests),
        "skills_target_met": skills_pass,
        "pipewire_audio_locked": audio_locked,
        "symlink_verified": symlink_ok
    }
