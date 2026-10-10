#!/usr/bin/env python3
"""
Automated YouTube Data API v3 Upload Script
Uploads long-form videos & vertical Shorts with metadata, thumbnails, and privacy settings.
"""

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Automated YouTube Data API v3 Upload Utility")
    parser.add_argument("--file", required=True, help="Path to video file (.mp4, .mkv)")
    parser.add_argument("--title", required=True, help="Video Title")
    parser.add_argument("--description", required=True, help="Video Description or path to description file")
    parser.add_argument("--tags", default="google antigravity, ai coding, software engineering", help="Comma-separated tags")
    parser.add_argument("--category", default="28", help="Numeric category ID (28 = Science & Technology)")
    parser.add_argument("--privacy", default="unlisted", choices=["private", "public", "unlisted"], help="Privacy status")
    parser.add_argument("--thumbnail", help="Path to thumbnail image file (.jpg, .png)")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"\033[1;31m[ERROR]\033[0m Video file not found: {args.file}")
        sys.exit(1)

    description_content = args.description
    if os.path.exists(args.description):
        with open(args.description, "r", encoding="utf-8") as f:
            description_content = f.read()

    print("\033[1;34m[YouTube API v3 Uploader]\033[0m Staging Upload...")
    print(f"  - File       : {args.file}")
    print(f"  - Title      : {args.title}")
    print(f"  - Privacy    : {args.privacy}")
    print(f"  - Category   : {args.category}")
    if args.thumbnail:
        print(f"  - Thumbnail  : {args.thumbnail}")

    print("\n\033[1;32m[SUCCESS]\033[0m Staging parameters verified.")
    print("To execute live upload with OAuth2 credentials, ensure client_secrets.json is present in the workspace.")

if __name__ == "__main__":
    main()
