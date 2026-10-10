#!/usr/bin/env bash
set -eo pipefail

echo -e "\033[1;34m[1/5]\033[0m Setting up skill directory structures..."
mkdir -p .agents/skills/yt-script
mkdir -p .agents/skills/yt-viral
mkdir -p data
mkdir -p scripts

echo -e "\033[1;34m[2/5]\033[0m Establishing relative hooks.json link..."
cd .agents/skills/yt-viral
[ ! -L hooks.json ] && ln -sf ../yt-script/hooks.json hooks.json || true
cd - > /dev/null

echo -e "\033[1;34m[3/5]\033[0m Setting executable permissions..."
chmod +x swipe.py scripts/swipe.py || true

echo -e "\033[1;34m[4/5]\033[0m Running live swipe.py test on test dataset..."
python3 swipe.py data/sample_collected.json --min 2.0

echo -e "\n\033[1;34m[5/5]\033[0m Running Master Pipeline Health Check..."
./scripts/master-pipeline.sh

echo -e "\n\033[1;32m[SUCCESS]\033[0m yt-viral skill and swipe.py engine 100% operational!"
