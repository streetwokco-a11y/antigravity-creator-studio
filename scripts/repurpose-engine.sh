#!/usr/bin/env bash
set -eo pipefail

VIDEO_NUM="${1:-1}"
OUTPUT_DIR="repurposed/video_0${VIDEO_NUM}"

echo -e "\033[1;35m========================================================\033[0m"
echo -e "\033[1;35m  MULTI-PLATFORM REPURPOSING ENGINE (VIDEO #$VIDEO_NUM) \033[0m"
echo -e "\033[1;35m========================================================\033[0m"

mkdir -p "$OUTPUT_DIR"

# 1. Generate X & LinkedIn 10-Slide Terminal Carousel Outline
cat << EOF > "${OUTPUT_DIR}/x_linkedin_carousel.md"
# 10-Slide Technical Terminal Carousel (Video #$VIDEO_NUM)

Slide 1: Hook -> "Stop writing boilerplate by hand in 2026."
Slide 2: System Architecture Diagram (Next.js 15 + FastAPI + SQLite).
Slide 3: Prisma Schema definition & relational foreign keys.
Slide 4: FastAPI REST route handlers & CORS middleware setup.
Slide 5: SQLite leads database connection pool.
Slide 6: Live curl test command output (HTTP 201 Created).
Slide 7: Next.js 15 App Router client state binding.
Slide 8: Dockerfile non-root USER appuser & HEALTHCHECK probes.
Slide 9: Hadolint security audit score (100% Pass).
Slide 10: Call to Action -> Clone starter code: https://github.com/yourusername/antigravity-demo
EOF

# 2. Generate Developer Newsletter Markdown Summary
cat << EOF > "${OUTPUT_DIR}/developer_newsletter.md"
# Developer Newsletter Issue #0${VIDEO_NUM}

Hey Engineers,

In this issue, we dive into building autonomous AI agent workflows using Google Antigravity on Ubuntu Linux.

### Key Highlights:
- Scaffolding Next.js 15 + FastAPI applications in under 60 seconds.
- Enforcing non-root container security with Hadolint rules.
- Broadcast audio compliance (-14.0 LUFS) and PipeWire 60 fps capture.

[Read full tutorial & watch video](#)
[Clone GitHub Starter Repository](https://github.com/yourusername/antigravity-demo)
EOF

# 3. Create GitHub Release Tag Manifest
cat << EOF > "${OUTPUT_DIR}/github_release_notes.md"
## Release v1.0.${VIDEO_NUM} - Video #$VIDEO_NUM Release Assets

### Features Included:
- Complete .agent/skills/ canonical manifests.
- Pre-configured SQLite schema and FastAPI route templates.
- Production-grade Dockerfile with non-root appuser execution.

### Installation:
\`\`\`bash
git clone https://github.com/yourusername/antigravity-demo.git
cd antigravity-demo
./scripts/master-pipeline.sh
\`\`\`
EOF

# 4. Generate Monetization & Affiliate Kit
cat << EOF > "${OUTPUT_DIR}/monetization_pack.md"
# Monetization & Affiliate Pack (Video #$VIDEO_NUM)

### 1. High-RPM Affiliate & Partner Links
- Cloud Compute / VPS: [Hetzner / Cloudflare Workers](https://your-affiliate-link)
- AI Model Inference: [Groq / Together AI](https://your-affiliate-link)
- Hardware & Mic: [Shure MV7+ / Elgato Cam Link](https://your-affiliate-link)

*FTC Disclosure: Some links above are affiliate links. If you sign up through them, I earn a small commission at zero cost to you.*

### 2. Digital Product & Code Access
- Clone Complete Starter Template: https://gumroad.com/l/antigravity-starter
- Support on GitHub Sponsors: https://github.com/sponsors/yourusername

### 3. Pinned Comment Copy (High-CTR Engagement)
\`\`\`text
⭐ Grab the complete code & .agents/skills/ repository pack from this video:
👉 Starter Repository: https://github.com/yourusername/antigravity-demo
👉 Commercial Enterprise Template: https://gumroad.com/l/antigravity-starter

Drop a comment below: What is the biggest bottleneck in your current coding workflow? I respond to all questions in the first 24 hours!
\`\`\`
EOF

echo -e "\n\033[1;32m[SUCCESS]\033[0m Multi-platform repurposing assets generated in \033[1;34m${OUTPUT_DIR}/\033[0m:"
echo -e "  - ${OUTPUT_DIR}/x_linkedin_carousel.md (10-Slide Carousel)"
echo -e "  - ${OUTPUT_DIR}/developer_newsletter.md (Substack / Dev.to Newsletter)"
echo -e "  - ${OUTPUT_DIR}/github_release_notes.md (GitHub Open-Source Release)"
echo -e "  - ${OUTPUT_DIR}/monetization_pack.md (Affiliates, Pinned Comment & Digital Products)"

