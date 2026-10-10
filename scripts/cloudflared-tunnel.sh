#!/usr/bin/env bash
# ==============================================================================
# ANTIGRAVITY CREATOR STUDIO - CLOUDFLARE QUICK TUNNEL RUNNER
# Zero-config secure tunneling without touching any production DNS records.
# ==============================================================================
set -euo pipefail

PORT="${1:-8000}"

echo "================================================================="
echo "  ANTIGRAVITY CREATOR STUDIO: CLOUDFLARE TUNNEL DISPATCH"
echo "================================================================="
echo "[INFO] Forwarding local Studio Engine (http://127.0.0.1:${PORT}) to Cloudflare Edge..."
echo "[INFO] Running isolated tunnel (safe: never touches custom DNS)..."

exec cloudflared tunnel --url "http://127.0.0.1:${PORT}"
