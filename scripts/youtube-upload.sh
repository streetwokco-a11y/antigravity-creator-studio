#!/usr/bin/env bash
set -eo pipefail

VIDEO_NUM="${1:-1}"
VIDEO_FILE="${2:-}"
PRIVACY="unlisted"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --privacy)
      PRIVACY="$2"
      shift 2
      ;;
    *)
      if [[ -z "$VIDEO_NUM_SET" ]]; then
        VIDEO_NUM="$1"
        VIDEO_NUM_SET=1
      elif [[ -z "$VIDEO_FILE_SET" ]]; then
        VIDEO_FILE="$1"
        VIDEO_FILE_SET=1
      fi
      shift
      ;;
  esac
done

if [[ -z "$VIDEO_FILE" || ! -f "$VIDEO_FILE" ]]; then
  echo "Usage: ./scripts/youtube-upload.sh <video-number (1..5)> <path-to-video.mp4> [--privacy unlisted|public]"
  exit 1
fi

PACKAGING_KIT="video_0${VIDEO_NUM}_packaging_kit.md"

if [ ! -f "$PACKAGING_KIT" ]; then
  echo "Packaging kit $PACKAGING_KIT not found!"
  exit 1
fi

echo -e "\033[1;34m[YouTube Automated Uploader]\033[0m Processing Video #$VIDEO_NUM..."
python3 scripts/youtube-upload.py \
  --file "$VIDEO_FILE" \
  --title "Google Antigravity Video #$VIDEO_NUM" \
  --description "$PACKAGING_KIT" \
  --privacy "$PRIVACY"
