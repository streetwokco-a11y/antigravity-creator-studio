#!/usr/bin/env bash
# scripts/bundle-starter-pack.sh - Bundles the Gumroad & GitHub Sponsors Day-1 Digital Product
set -eo pipefail

WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WORKSPACE"

BUNDLE_DIR="$WORKSPACE/exports/antigravity-starter-kit-v1.0"
rm -rf "$BUNDLE_DIR"
mkdir -p "$BUNDLE_DIR"

echo -e "\033[1;35m=================================================================\033[0m"
echo -e "\033[1;35m  BUNDLING DAY-1 DIGITAL PRODUCT: ANTIGRAVITY STARTER KIT v1.0   \033[0m"
echo -e "\033[1;35m=================================================================\033[0m"

# 1. Copy canonical .agents/skills
echo "[1/4] Packaging canonical skill manifests..."
cp -r "$WORKSPACE/.agents" "$BUNDLE_DIR/.agents"

# 2. Copy fullstack Next.js + FastAPI + Docker templates
echo "[2/4] Packaging fullstack reference architecture..."
mkdir -p "$BUNDLE_DIR/template"
cp -r "$WORKSPACE/video_02_lead_triage/backend" "$BUNDLE_DIR/template/backend"
cp -r "$WORKSPACE/video_02_lead_triage/frontend" "$BUNDLE_DIR/template/frontend"
cp "$WORKSPACE/video_02_lead_triage/Dockerfile" "$BUNDLE_DIR/template/Dockerfile"
cp "$WORKSPACE/video_02_lead_triage/docker-compose.yml" "$BUNDLE_DIR/template/docker-compose.yml" 2>/dev/null || true

# 3. Add Commercial License & Gumroad Welcome Guide
echo "[3/4] Adding commercial license and setup guide..."
cat << 'EOF' > "$BUNDLE_DIR/README.md"
# Google Antigravity Production Starter Kit v1.0
### Commercial Developer Template & Autonomous Agent Skills Fleet

Thank you for downloading the official Antigravity Production Starter Kit!
This kit includes everything you need to deploy autonomous multi-agent coding workflows on Ubuntu Linux:

## 📦 What's Included:
1. `.agents/skills/` - 24 Production-grade canonical agent skill manifests.
2. `template/backend/` - FastAPI asynchronous backend with SQLite/Postgres connection pooling.
3. `template/frontend/` - Next.js 15 App Router dashboard with clean Tailwind/CSS binding.
4. `template/Dockerfile` - Non-root containerized deployment with healthchecks.

## 🚀 Quickstart:
```bash
# 1. Clone into your project root
cp -r .agents /path/to/your/project/

# 2. Launch your Antigravity agent CLI
agy

# 3. Trigger autonomous scaffolding
/autonomous-fullstack-builder
```

## 📜 Commercial License:
Permitted for use in commercial client projects, personal SaaS applications, and enterprise microservices.
EOF

# 4. Generate Archive Archives
echo "[4/4] Compressing into release archives..."
cd "$WORKSPACE/exports"
tar -czf "antigravity-starter-kit-v1.0.tar.gz" "antigravity-starter-kit-v1.0"
if command -v zip >/dev/null 2>&1; then
    zip -rq "antigravity-starter-kit-v1.0.zip" "antigravity-starter-kit-v1.0"
fi

echo -e "\n\033[1;32m[SUCCESS]\033[0m Digital product ready for Gumroad & GitHub Sponsors upload:"
echo -e "  - \033[1;36mexports/antigravity-starter-kit-v1.0.tar.gz\033[0m"
if [ -f "$WORKSPACE/exports/antigravity-starter-kit-v1.0.zip" ]; then
    echo -e "  - \033[1;36mexports/antigravity-starter-kit-v1.0.zip\033[0m"
fi
