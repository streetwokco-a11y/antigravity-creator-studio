"""
services/media_service.py - EBU R128 audio analysis and lossless FFmpeg normalization.
"""

import subprocess
import os
import re
from typing import Dict, Any, Tuple
from services.db_service import record_qa_audit
from services.resilience import resilient_job

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def audit_video_compliance(file_path: str) -> Dict[str, Any]:
    full_path = os.path.join(WORKSPACE_ROOT, file_path) if not os.path.isabs(file_path) else file_path
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"Target video file not found: {full_path}")

    # 1. Video Stream Probing (ffprobe)
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,codec_name",
        "-of", "default=noprint_wrappers=1", full_path
    ]
    probe_out = subprocess.check_output(probe_cmd, text=True)
    width = re.search(r"width=(\d+)", probe_out)
    height = re.search(r"height=(\d+)", probe_out)
    fps_raw = re.search(r"r_frame_rate=([0-9/]+)", probe_out)
    codec = re.search(r"codec_name=(\w+)", probe_out)

    fps = 0.0
    if fps_raw:
        parts = fps_raw.group(1).split("/")
        fps = round(float(parts[0]) / float(parts[1]), 2) if len(parts) == 2 else float(parts[0])

    res = f"{width.group(1)}x{height.group(1)}" if width and height else "Unknown"
    codec_str = codec.group(1) if codec else "Unknown"

    # 2. Audio Stream EBU R128 Analysis (ffmpeg)
    loudnorm_cmd = [
        "ffmpeg", "-nostats", "-i", full_path,
        "-filter_complex", "ebur128=peak=true", "-f", "null", "-"
    ]
    proc = subprocess.run(loudnorm_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = proc.stderr

    i_match = re.search(r"Integrated loudness:\s+I:\s+([-\d.]+)\s+LUFS", out)
    tp_match = re.search(r"Peak:\s+Peak:\s+([-\d.]+)\s+dBFS", out)
    lra_match = re.search(r"Loudness range:\s+LRA:\s+([-\d.]+)\s+LU", out)

    lufs = float(i_match.group(1)) if i_match else -99.0
    peak = float(tp_match.group(1)) if tp_match else -99.0
    lra = float(lra_match.group(1)) if lra_match else 0.0

    verdict = "PASS"
    if fps < 59.0 or lufs < -16.0 or lufs > -13.0 or peak > -1.5:
        verdict = "FAIL"

    record_qa_audit(file_path, codec_str, res, fps, lufs, peak, lra, verdict)

    return {
        "file_path": file_path,
        "codec": codec_str,
        "resolution": res,
        "fps": fps,
        "lufs": lufs,
        "peak": peak,
        "lra": lra,
        "verdict": verdict,
        "fps_pass": fps >= 59.0,
        "lufs_pass": -16.0 <= lufs <= -13.0,
        "peak_pass": peak <= -1.5
    }


@resilient_job(service_name="media_normalizer", max_retries=2)
def auto_normalize_audio(file_path: str) -> str:
    full_path = os.path.join(WORKSPACE_ROOT, file_path) if not os.path.isabs(file_path) else file_path
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"Input file not found: {full_path}")

    dir_name = os.path.dirname(full_path)
    base_name = os.path.basename(full_path)
    name, ext = os.path.splitext(base_name)
    output_path = os.path.join(dir_name, f"{name}_normalized{ext}")

    # Lossless video stream copy + high-definition AAC audio filter
    cmd = [
        "ffmpeg", "-y", "-i", full_path,
        "-c:v", "copy",
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7.0",
        "-c:a", "aac", "-b:a", "320k",
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.relpath(output_path, WORKSPACE_ROOT)
