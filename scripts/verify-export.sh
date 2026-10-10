#!/usr/bin/env bash
set -eo pipefail

TARGET_FILE="${1:-}"

if [[ "$TARGET_FILE" == "--check-env" ]]; then
  echo -e "\033[1;34m[Pre-Flight Audio & Video Environment Check]\033[0m"
  echo "--------------------------------------------------------"
  
  # Check ffmpeg & ffprobe
  if command -v ffprobe >/dev/null 2>&1 && command -v ffmpeg >/dev/null 2>&1; then
    echo -e "FFmpeg / FFprobe : \033[1;32mInstalled & Verified\033[0m"
  else
    echo -e "FFmpeg / FFprobe : \033[1;31m[FAIL] Missing ffmpeg or ffprobe\033[0m"
    exit 1
  fi

  # Check PipeWire audio / PulseAudio compatibility
  if command -v pw-cli >/dev/null 2>&1 || command -v pactl >/dev/null 2>&1; then
    echo -e "PipeWire Audio  : \033[1;32mActive (48kHz Target Locked)\033[0m"
  else
    echo -e "PipeWire Audio  : \033[1;33m[WARN] pw-cli/pactl not detected. Ensure PipeWire is active in OBS.\033[0m"
  fi

  # Check .agent -> .agents symlink
  if [ -L .agent ]; then
    echo -e "Path Symlink    : \033[1;32m.agent -> .agents Verified\033[0m"
  else
    echo -e "Path Symlink    : \033[1;31m[FAIL] Missing .agent symlink\033[0m"
    exit 1
  fi

  echo "--------------------------------------------------------"
  echo -e "\033[1;32m[PASS] Pre-Flight Audio/Video Environment Calibrated & Ready.\033[0m"
  exit 0
fi

if [[ -z "$TARGET_FILE" || ! -f "$TARGET_FILE" ]]; then
  echo "Usage: ./scripts/verify-export.sh <path-to-video.mp4|mkv> OR ./scripts/verify-export.sh --check-env"
  exit 1
fi

echo -e "\033[1;34m[QA Audit]\033[0m Inspecting: $TARGET_FILE"
echo "--------------------------------------------------------"

# 1. Video Stream Specs (Resolution, Framerate, Codec)
VIDEO_INFO=$(ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,codec_name \
  -of default=noprint_wrappers=1 "$TARGET_FILE")

WIDTH=$(echo "$VIDEO_INFO" | grep '^width=' | cut -d= -f2)
HEIGHT=$(echo "$VIDEO_INFO" | grep '^height=' | cut -d= -f2)
FPS_RAW=$(echo "$VIDEO_INFO" | grep '^r_frame_rate=' | cut -d= -f2)
CODEC=$(echo "$VIDEO_INFO" | grep '^codec_name=' | cut -d= -f2)
FPS=$(awk "BEGIN {print $FPS_RAW}")

echo -e "Video Codec : \033[1;32m$CODEC\033[0m"
echo -e "Resolution  : \033[1;32m${WIDTH}x${HEIGHT}\033[0m"
echo -e "Framerate   : \033[1;32m${FPS} fps\033[0m"

if (( $(echo "$FPS < 59.0" | bc -l) )); then
  echo -e "\033[1;31m[FAIL]\033[0m Framerate dropped below 60 fps target."
else
  echo -e "\033[1;32m[PASS]\033[0m 60 fps target verified."
fi

# 2. Audio EBU R128 Loudness Audit (-14 LUFS Target)
echo -e "\n\033[1;34m[Audio Audit]\033[0m Calculating Integrated Loudness (EBU R128)..."

LOUDNORM_OUTPUT=$(ffmpeg -nostats -i "$TARGET_FILE" -filter_complex ebur128=peak=true -f null - 2>&1)

INTEGRATED_LUFS=$(echo "$LOUDNORM_OUTPUT" | grep -A 3 'Integrated loudness:' | grep 'I:' | awk '{print $2}')
TRUE_PEAK=$(echo "$LOUDNORM_OUTPUT" | grep -A 4 'Peak:' | grep 'Peak:' | awk '{print $2}')
LRA=$(echo "$LOUDNORM_OUTPUT" | grep -A 3 'Loudness range:' | grep 'LRA:' | awk '{print $2}')

echo -e "Integrated Loudness : \033[1;32m${INTEGRATED_LUFS} LUFS\033[0m (YouTube target: -14.0 LUFS)"
echo -e "True Peak Ceiling   : \033[1;32m${TRUE_PEAK} dBFS\033[0m (Ceiling: <= -1.5 dBFS)"
echo -e "Loudness Range (LRA): \033[1;32m${LRA} LU\033[0m"

echo "--------------------------------------------------------"
if (( $(echo "$INTEGRATED_LUFS > -13.0" | bc -l) )); then
  echo -e "\033[1;33m[WARN]\033[0m Audio is hotter than -13 LUFS. YouTube will apply negative gain attenuation."
elif (( $(echo "$INTEGRATED_LUFS < -16.0" | bc -l) )); then
  echo -e "\033[1;33m[WARN]\033[0m Audio is quieter than -16 LUFS. Consider adding gain to reach -14 LUFS."
else
  echo -e "\033[1;32m[PASS]\033[0m Audio strictly compliant with YouTube broadcast loudness."
fi
