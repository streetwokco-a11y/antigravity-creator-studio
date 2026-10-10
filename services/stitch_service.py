"""
services/stitch_service.py - Headless Programmatic Video Assembly & Stitching Engine.
Assembles raw screen captures, intro hooks, and outro bumpers into broadcast-ready exports.
Supports both 16:9 Long-Form tutorials and 9:16 Vertical YouTube Shorts.
"""

import os
import subprocess
from typing import List, Optional, Dict, Any
from services.resilience import resilient_job

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXPORTS_DIR = os.path.join(WORKSPACE_ROOT, "exports")


@resilient_job(service_name="headless_stitcher", max_retries=2)
def stitch_video_headless(
    clip_paths: List[str],
    output_filename: str,
    voiceover_path: Optional[str] = None,
    bg_music_path: Optional[str] = None,
    bg_music_volume: float = 0.04,  # -28dB background bed
    video_format: str = "landscape"  # "landscape" (1920x1080) or "short" (1080x1920)
) -> Dict[str, Any]:
    """
    Headlessly concatenates video clips, harmonizes resolution (1080p60 landscape or vertical short),
    ducks background audio beneath voiceover, and masters audio to -14.0 LUFS.
    """
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    output_path = os.path.join(EXPORTS_DIR, output_filename)
    
    # Resolve absolute paths
    full_clips = [
        os.path.join(WORKSPACE_ROOT, c) if not os.path.isabs(c) else c
        for c in clip_paths
    ]
    for c in full_clips:
        if not os.path.isfile(c):
            raise FileNotFoundError(f"Source clip not found: {c}")

    concat_list_file = os.path.join(EXPORTS_DIR, f"concat_manifest_{os.getpid()}.txt")
    with open(concat_list_file, "w") as f:
        for c in full_clips:
            f.write(f"file '{c}'\n")

    # FFmpeg command builder
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_list_file,
    ]

    extra_inputs = 0
    if voiceover_path and os.path.isfile(voiceover_path):
        cmd.extend(["-i", voiceover_path])
        extra_inputs += 1
        vo_idx = extra_inputs

    if bg_music_path and os.path.isfile(bg_music_path):
        cmd.extend(["-i", bg_music_path])
        extra_inputs += 1
        music_idx = extra_inputs

    # Filter graph construction
    filter_chains = []
    
    # 1. Video scaling and format harmonization
    if video_format == "short":
        # 1080x1920 vertical format for YouTube Shorts
        target_res = "1080x1920"
        filter_chains.append("[0:v]fps=60,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v_out]")
    else:
        # Standard 1920x1080 landscape format for long-form tutorials
        target_res = "1920x1080"
        filter_chains.append("[0:v]fps=60,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v_out]")

    # 2. Audio mix & loudnorm (-14.0 LUFS)
    if extra_inputs == 0:
        filter_chains.append("[0:a]loudnorm=I=-14.0:TP=-1.5:LRA=7.0[a_out]")
    elif extra_inputs == 1 and voiceover_path:
        filter_chains.append(f"[{vo_idx}:a]loudnorm=I=-14.0:TP=-1.5:LRA=7.0[a_out]")
    elif extra_inputs == 2 and voiceover_path and bg_music_path:
        filter_chains.append(f"[{music_idx}:a]volume={bg_music_volume}[music_ducked]")
        filter_chains.append(f"[{vo_idx}:a][music_ducked]amix=inputs=2:duration=first[mixed_audio]")
        filter_chains.append("[mixed_audio]loudnorm=I=-14.0:TP=-1.5:LRA=7.0[a_out]")

    cmd.extend([
        "-filter_complex", ";".join(filter_chains),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-movflags", "+faststart",
        output_path
    ])

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Cleanup temp manifest
    if os.path.exists(concat_list_file):
        os.remove(concat_list_file)

    rel_output = os.path.relpath(output_path, WORKSPACE_ROOT)
    return {
        "status": "SUCCESS",
        "output_file": rel_output,
        "format": video_format,
        "resolution": target_res,
        "framerate": 60.0,
        "target_lufs": -14.0
    }
