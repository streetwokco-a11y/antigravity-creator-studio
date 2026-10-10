"""
scripts/render-automated-video.py - Headless Video Assembly & Mastering CLI Engine.
Supports programmatic rendering of raw screen captures, landscape tutorials, and vertical Shorts
without an NLE editor.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKSPACE)

from services.stitch_service import stitch_video_headless
from services.db_service import log_run_start, log_run_finish


def ensure_asset_fixtures(assets_dir: str):
    """Generates broadcast test clips in assets directory if none exist."""
    os.makedirs(assets_dir, exist_ok=True)
    clips = sorted([str(p) for p in Path(assets_dir).glob("*.mp4")])
    if not clips:
        c1 = os.path.join(assets_dir, "take_01_face.mp4")
        c2 = os.path.join(assets_dir, "take_01_screen.mp4")
        for idx, clip in enumerate([c1, c2], 1):
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"testsrc=duration=3:size=1920x1080:rate=60",
                "-f", "lavfi", "-i", f"sine=frequency={440 * idx}:duration=3",
                "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
                clip
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips = [c1, c2]
    return clips


def main():
    parser = argparse.ArgumentParser(description="Headless Video Assembly & Mastering Engine")
    parser.add_argument("--assets", default=None, help="Directory containing raw screen captures & assets")
    parser.add_argument("--clips", nargs="*", default=None, help="List of video clips in order of playback")
    parser.add_argument("--format", choices=["landscape", "short", "all"], default="landscape", help="Output format: landscape, short, or all")
    parser.add_argument("--lufs", type=float, default=-14.0, help="EBU R128 target loudness (default: -14.0)")
    parser.add_argument("--fps", type=float, default=60.0, help="Target framerate (default: 60.0)")
    parser.add_argument("--output", default="automated_render.mp4", help="Output filename inside exports/")
    parser.add_argument("--voiceover", default=None, help="Optional separate voiceover audio track")
    parser.add_argument("--music", default=None, help="Optional background music track")
    parser.add_argument("--skip-post-ingest", action="store_true", help="Skip automatic verify & youtube staging")

    args = parser.parse_args()

    run_id = log_run_start("headless_render_engine", {"format": args.format, "assets": args.assets})

    # Determine source clips
    if args.assets:
        resolved_assets = os.path.join(WORKSPACE, args.assets) if not os.path.isabs(args.assets) else args.assets
        clips = ensure_asset_fixtures(resolved_assets)
    elif args.clips:
        clips = args.clips
    else:
        sample_path = os.path.join(WORKSPACE, "exports", "automated_render.mp4")
        if not os.path.exists(sample_path):
            sample_path = ensure_asset_fixtures(os.path.join(WORKSPACE, "assets", "episode_06"))[0]
        clips = [sample_path]

    formats_to_render = ["landscape", "short"] if args.format == "all" else [args.format]

    print(f"\033[1;35m=================================================================\033[0m")
    print(f"\033[1;35m  HEADLESS VIDEO ASSEMBLY ENGINE (TARGET: {args.format.upper()}) \033[0m")
    print(f"\033[1;35m=================================================================\033[0m")
    print(f"[INFO] Source clips: {len(clips)} files")
    print(f"[INFO] Target Loudness: {args.lufs} LUFS | Target Framerate: {args.fps} fps")

    for fmt in formats_to_render:
        out_name = "automated_short.mp4" if fmt == "short" else args.output
        print(f"\n[STITCHING] Rendering format '{fmt}' -> exports/{out_name}...")
        try:
            res = stitch_video_headless(
                clip_paths=clips,
                output_filename=out_name,
                voiceover_path=args.voiceover,
                bg_music_path=args.music,
                video_format=fmt
            )
            print(f"✔ Render complete: \033[1;32m{res['output_file']}\033[0m")
            print(f"  Resolution: {res['resolution']} @ {res['framerate']} fps | Audio Mastered to {res['target_lufs']} LUFS")
        except Exception as e:
            print(f"\033[1;31m[ERROR]\033[0m Render failed for {fmt}: {e}", file=sys.stderr)
            log_run_finish(run_id, "FAILED")
            sys.exit(1)

    print(f"\n\033[1;32m[SUCCESS]\033[0m All requested formats rendered headlessly.")

    # Automated Post-Capture Ingestion (Zero-Edit Workflow)
    if not args.skip_post_ingest:
        print(f"\n\033[1;34m[POST-CAPTURE INGESTION]\033[0m Executing automated verification & staging...")
        master_file = os.path.join(WORKSPACE, "exports", "automated_render.mp4")
        if os.path.exists(master_file):
            # 1. Run verify-export.sh
            subprocess.run(["./scripts/verify-export.sh", master_file], cwd=WORKSPACE)
            # 2. Stage to YouTube Data API v3 as Unlisted
            upload_cmd = [
                "./scripts/youtube-upload.py",
                "--file", master_file,
                "--title", "Hardcore DevOps: Delete My Server If This Agent Fails",
                "--description", "repurposed/video_06/monetization_pack.md",
                "--privacy", "unlisted"
            ]
            subprocess.run(upload_cmd, cwd=WORKSPACE)
            log_run_finish(run_id, "COMPLETED")
            print(f"\033[1;32m[DONE]\033[0m Studio run #{run_id} marked COMPLETED in studio.db.")
        else:
            log_run_finish(run_id, "SUCCESS")


if __name__ == "__main__":
    main()
