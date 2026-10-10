"""
studio_server.py - Production Control Center & REST Gateway for Antigravity Studio.
Enterprise v2.5 with 3-Column Visual Dashboard, Headless Programmatic Rendering,
YPP Monetization Safeguards, Autonomous Task Scheduler, and Multi-Platform Direct API Dispatch.
"""

import os
import sys
import json
import subprocess
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
if WORKSPACE not in sys.path:
    sys.path.insert(0, WORKSPACE)

# Initialize Persistence & Domain Services
from services.db_service import init_db, fetch_latest_audits, log_run_start, log_run_finish
from services.media_service import audit_video_compliance, auto_normalize_audio
from services.analytics_service import get_outliers
from services.qa_service import run_full_preflight_audit
from services.compliance_service import audit_ypp_compliance
from services.stitch_service import stitch_video_headless
from services.dispatch_service import dispatch_to_x, dispatch_to_linkedin, dispatch_to_newsletter
from services.scheduler_service import scheduler

init_db()

app = FastAPI(title="Antigravity Studio Engine", version="2.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML_UI = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Antigravity Studio Control Center | Monetization & Production Engine</title>
  <style>
    :root {
      --bg-dark: #020617;
      --bg-card: rgba(15, 23, 42, 0.9);
      --border-color: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
      padding: 1.5rem;
    }
    .max-w-7xl { max-width: 84rem; }
    .mx-auto { margin-left: auto; margin-right: auto; }
    .space-y-6 > * + * { margin-top: 1.5rem; }
    .space-y-4 > * + * { margin-top: 1rem; }
    .space-y-3 > * + * { margin-top: 0.75rem; }
    .space-y-2 > * + * { margin-top: 0.5rem; }
    .space-y-1\.5 > * + * { margin-top: 0.375rem; }

    .flex { display: flex; }
    .flex-col { flex-direction: column; }
    .items-center { align-items: center; }
    .justify-between { justify-content: space-between; }
    .justify-center { justify-content: center; }
    .gap-1 { gap: 0.25rem; }
    .gap-1\.5 { gap: 0.375rem; }
    .gap-2 { gap: 0.5rem; }
    .gap-3 { gap: 0.75rem; }
    .gap-4 { gap: 1rem; }
    .gap-6 { gap: 1.5rem; }

    .grid { display: grid; }
    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    .grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    @media (min-width: 1024px) {
      .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    }

    .border { border: 1px solid var(--border-color); }
    .border-b { border-bottom: 1px solid var(--border-color); }
    .border-t { border-top: 1px solid var(--border-color); }
    .rounded-lg { border-radius: 0.5rem; }
    .rounded-xl { border-radius: 0.75rem; }
    .rounded-2xl { border-radius: 1rem; }
    .rounded-full { border-radius: 9999px; }

    .p-2 { padding: 0.5rem; }
    .p-2\.5 { padding: 0.625rem; }
    .p-3 { padding: 0.75rem; }
    .p-3\.5 { padding: 0.875rem; }
    .p-4 { padding: 1rem; }
    .p-5 { padding: 1.25rem; }
    .p-6 { padding: 1.5rem; }
    .px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
    .px-2\.5 { padding-left: 0.625rem; padding-right: 0.625rem; }
    .px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
    .px-3\.5 { padding-left: 0.875rem; padding-right: 0.875rem; }
    .px-4 { padding-left: 1rem; padding-right: 1rem; }
    .py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
    .py-1\.5 { padding-top: 0.375rem; padding-bottom: 0.375rem; }
    .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    .py-2\.5 { padding-top: 0.625rem; padding-bottom: 0.625rem; }
    .pb-3 { padding-bottom: 0.75rem; }
    .pb-4 { padding-bottom: 1rem; }
    .pt-1 { padding-top: 0.25rem; }
    .pt-2 { padding-top: 0.5rem; }
    .w-full { width: 100%; }
    .w-6 { width: 1.5rem; }
    .h-6 { height: 1.5rem; }
    .w-2 { width: 0.5rem; }
    .h-2 { height: 0.5rem; }
    .h-2-bar { height: 0.5rem; }
    .h-44 { height: 11rem; }
    .h-48 { height: 12rem; }
    .h-52 { height: 13rem; }
    .overflow-y-auto { overflow-y: auto; }
    .overflow-hidden { overflow: hidden; }

    .bg-slate-950 { background-color: #020617; }
    .bg-slate-900 { background-color: #0f172a; }
    .bg-slate-800 { background-color: #1e293b; }
    .bg-slate-700 { background-color: #334155; }
    .bg-blue-600 { background-color: #2563eb; }
    .bg-blue-500 { background-color: #3b82f6; }
    .bg-emerald-600 { background-color: #059669; }
    .bg-emerald-500 { background-color: #10b981; }
    .bg-emerald-950 { background-color: #022c22; }
    .bg-amber-600 { background-color: #d97706; }
    .bg-purple-600 { background-color: #9333ea; }
    .bg-purple-500 { background-color: #a855f7; }
    .bg-rose-600 { background-color: #e11d48; }
    .bg-indigo-950 { background-color: #1e1b4b; }

    .text-white { color: #ffffff; }
    .text-slate-100 { color: #f1f5f9; }
    .text-slate-300 { color: #cbd5e1; }
    .text-slate-400 { color: #94a3b8; }
    .text-slate-500 { color: #64748b; }
    .text-emerald-300 { color: #6ee7b7; }
    .text-emerald-400 { color: #34d399; }
    .text-amber-400 { color: #fbbf24; }
    .text-purple-300 { color: #d8b4fe; }
    .text-purple-400 { color: #c084fc; }
    .text-rose-300 { color: #fda4af; }
    .text-rose-400 { color: #fb7185; }
    .text-cyan-300 { color: #67e8f9; }

    .font-sans { font-family: system-ui, -apple-system, sans-serif; }
    .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, monospace; }
    .font-bold { font-weight: 700; }
    .font-semibold { font-weight: 600; }
    .text-xs { font-size: 0.75rem; line-height: 1rem; }
    .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
    .text-base { font-size: 1rem; line-height: 1.5rem; }
    .text-xl { font-size: 1.25rem; line-height: 1.75rem; }
    .text-2xl { font-size: 1.5rem; line-height: 2rem; }
    .text-\[10px\] { font-size: 10px; }
    .text-\[11px\] { font-size: 11px; }

    .hidden { display: none !important; }
    .block { display: block; }
    .fixed { position: fixed; }
    .inset-0 { inset: 0; }
    .z-50 { z-index: 50; }
    .transition { transition: all 0.2s ease-in-out; }

    button { cursor: pointer; border: none; outline: none; }
    input, select { outline: none; }
    input:focus, select:focus { border-color: #8b5cf6 !important; }
    .badge { display: inline-flex; align-items: center; padding: 0.15rem 0.5rem; border-radius: 9999px; font-size: 10px; font-weight: 600; }
  </style>
</head>
<body>
  <div class="max-w-7xl mx-auto space-y-6">

    <!-- HEADER & MONETIZATION BAR -->
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center bg-slate-900 border rounded-2xl p-5 gap-4">
      <div class="space-y-1">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🛰️</span>
          <h1 class="text-xl font-bold tracking-tight text-white">Antigravity Studio Engine <span class="text-purple-400 font-mono text-xs">v2.5 Enterprise</span></h1>
          <span class="badge bg-emerald-950 border border-emerald-800 text-emerald-400">YPP Monetization Ready</span>
        </div>
        <p class="text-xs text-slate-400">Autonomous YouTube Creator Architecture & High-RPM Monetization Engine ($22–$38+ RPM Tier)</p>
      </div>

      <div class="flex items-center gap-2">
        <button onclick="runAutonomousNightly()" class="px-3.5 py-2 bg-gradient-to-r bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold flex items-center gap-2 transition">
          <span>⚡</span> Run Full Pipeline Now
        </button>
        <button onclick="runPreflight()" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border rounded-lg text-xs font-mono flex items-center gap-2 transition">
          <span>🔍</span> QA Pre-flight
        </button>
      </div>
    </header>

    <!-- MONETIZATION & POLICY ROADMAP BAR -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-3 bg-slate-900 border rounded-2xl p-4">
      <div class="bg-slate-950 border rounded-xl p-3 space-y-1">
        <div class="flex justify-between items-center text-xs text-slate-400">
          <span>Shorts Flywheel</span>
          <span class="text-purple-400 font-bold">1,000 Subs</span>
        </div>
        <div class="text-sm font-bold text-white">45–58s Infinite Loop</div>
        <p class="text-[10px] text-slate-500">>80% retention target, 2s visual hook</p>
      </div>

      <div class="bg-slate-950 border rounded-xl p-3 space-y-1">
        <div class="flex justify-between items-center text-xs text-slate-400">
          <span>Long-Form Evergreen</span>
          <span class="text-emerald-400 font-bold">4,000 Watch Hrs</span>
        </div>
        <div class="text-sm font-bold text-white">8–14 Min Deep Dive</div>
        <p class="text-[10px] text-slate-500">60% Search (Evergreen) / 40% Browse</p>
      </div>

      <div class="bg-slate-950 border rounded-xl p-3 space-y-1">
        <div class="flex justify-between items-center text-xs text-slate-400">
          <span>AdSense RPM Niche</span>
          <span class="text-amber-400 font-bold">$22.00–$38.50</span>
        </div>
        <div class="text-sm font-bold text-white">AI Agents / Dev Tools</div>
        <p class="text-[10px] text-slate-500">vs $2.50 entertainment channel RPM</p>
      </div>

      <div class="bg-slate-950 border rounded-xl p-3 space-y-1">
        <div class="flex justify-between items-center text-xs text-slate-400">
          <span>Day-1 Cashflow</span>
          <span class="text-cyan-300 font-bold">Gumroad / Sponsors</span>
        </div>
        <div class="text-sm font-bold text-white">Digital Code Starter Pack</div>
        <p class="text-[10px] text-slate-500">Immediate revenue before AdSense YPP</p>
      </div>
    </div>

    <!-- BANNER NOTIFICATIONS -->
    <div id="banner" class="hidden"></div>

    <!-- MAIN 3-COLUMN STUDIO LAYOUT -->
    <main class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- COLUMN 1: STAGING & TELEPROMPTER -->
      <section class="bg-slate-900 border rounded-2xl p-5 space-y-4 flex flex-col justify-between">
        <div class="space-y-4">
          <div class="flex items-center gap-2 border-b pb-3">
            <span class="w-6 h-6 rounded-full bg-blue-600 text-xs flex items-center justify-center font-bold text-white">1</span>
            <h2 class="font-bold text-white text-base">Staging & Prompter</h2>
          </div>

          <div>
            <label class="text-xs font-semibold text-slate-400 block mb-1">Select Episode</label>
            <select id="teleprompter-select" onchange="loadScript()" class="w-full bg-slate-950 border rounded-lg p-2.5 text-xs text-white">
              <option value="1">Video #1: Stop Using AI Like Autocomplete</option>
              <option value="2">Video #2: Full-Stack Next.js 15 in 60s</option>
              <option value="3">Video #3: Custom Skills & Progressive Disclosure</option>
              <option value="4">Video #4: Antigravity vs Cursor Benchmark</option>
              <option value="5">Video #5: Channel Automation Engine</option>
              <option value="6" selected>Video #6: Hardcore DevOps (Server Teardown Challenge)</option>
            </select>
          </div>

          <div class="bg-slate-950 border rounded-xl p-3 h-52 overflow-y-auto space-y-2 text-xs leading-relaxed text-slate-300 font-mono" id="script-box">
            Loading script cue...
          </div>
        </div>

        <div class="space-y-2 pt-2 border-t">
          <div class="grid grid-cols-2 gap-2">
            <button onclick="openFullPrompter()" class="py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg text-xs transition">
              📜 Full Prompter
            </button>
            <button onclick="triggerDemo()" class="py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-100 font-semibold rounded-lg text-xs border transition">
              ⚡ Stage Demo
            </button>
          </div>
        </div>
      </section>

      <!-- COLUMN 2: HEADLESS RENDER & EXPORT QA -->
      <section class="bg-slate-900 border rounded-2xl p-5 space-y-4 flex flex-col justify-between">
        <div class="space-y-4">
          <div class="flex items-center gap-2 border-b pb-3">
            <span class="w-6 h-6 rounded-full bg-amber-600 text-xs flex items-center justify-center font-bold text-white">2</span>
            <h2 class="font-bold text-white text-base">Headless Render & QA</h2>
          </div>

          <!-- Headless Programmatic Video Assembly (Replaces Manual NLE) -->
          <div class="bg-slate-950 border rounded-xl p-3 space-y-2">
            <label class="text-xs font-semibold text-amber-400 block">Headless Video Stitcher (No DaVinci / NLE)</label>
            <div class="grid grid-cols-2 gap-1.5">
              <button onclick="renderHeadless('landscape')" class="p-2 bg-slate-900 border rounded-lg hover:bg-slate-800 text-[11px] font-mono text-left transition">
                🎬 1080p60 Tutorial
              </button>
              <button onclick="renderHeadless('short')" class="p-2 bg-slate-900 border rounded-lg hover:bg-slate-800 text-[11px] font-mono text-left text-cyan-300 transition">
                📱 9:16 Short Loop
              </button>
            </div>
            <p class="text-[10px] text-slate-500">Harmonizes 60fps, ducks audio (-28dB), masters -14 LUFS</p>
          </div>

          <div>
            <label class="text-xs font-semibold text-slate-400 block mb-1">Exported Master File</label>
            <input type="text" id="qa-path" value="exports/automated_render.mp4" 
                   class="w-full bg-slate-950 border rounded-lg p-2.5 text-xs text-white font-mono">
          </div>

          <!-- Meters -->
          <div class="bg-slate-950 border rounded-xl p-3.5 space-y-3 font-mono text-xs">
            <div>
              <div class="flex justify-between text-slate-400 mb-1">
                <span>Integrated Loudness</span>
                <span id="lufs-val" class="font-bold text-white">-14.0 LUFS</span>
              </div>
              <div class="w-full bg-slate-800 h-2-bar rounded-full overflow-hidden">
                <div id="lufs-bar" class="meter-bar bg-emerald-600 h-full" style="width: 75%;"></div>
              </div>
              <div class="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>-35 LUFS</span>
                <span class="text-amber-400 font-bold">-14 LUFS Target</span>
                <span>-6 LUFS</span>
              </div>
            </div>

            <div class="flex justify-between items-center pt-2 border-t">
              <span class="text-slate-400">Framerate Target:</span>
              <span id="fps-val" class="font-bold text-emerald-400">60.0 fps (PASS)</span>
            </div>
          </div>

          <div id="qa-log" class="hidden bg-slate-950 border rounded-xl p-3 text-xs font-mono text-slate-300 max-h-44 overflow-y-auto"></div>
        </div>

        <div class="space-y-2 pt-2 border-t">
          <div class="grid grid-cols-2 gap-2">
            <button onclick="auditVideo()" class="py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-100 font-semibold rounded-lg text-xs border transition">
              🔍 Audit File
            </button>
            <button onclick="autofixAudio()" class="py-2.5 bg-amber-600 hover:bg-amber-500 text-white font-semibold rounded-lg text-xs transition">
              🪄 1-Click Fix Audio
            </button>
          </div>
        </div>
      </section>

      <!-- COLUMN 3: MONETIZATION, DISPATCH & PUBLISH -->
      <section class="bg-slate-900 border rounded-2xl p-5 space-y-4 flex flex-col justify-between">
        <div class="space-y-4">
          <div class="flex items-center gap-2 border-b pb-3">
            <span class="w-6 h-6 rounded-full bg-purple-600 text-xs flex items-center justify-center font-bold text-white">3</span>
            <h2 class="font-bold text-white text-base">Monetization & Dispatch</h2>
          </div>

          <div>
            <label class="text-xs font-semibold text-slate-400 block mb-1">Target Episode & Privacy</label>
            <div class="grid grid-cols-2 gap-2">
              <select id="pub-num" class="bg-slate-950 border rounded-lg p-2.5 text-xs text-white">
                <option value="1">Video #1</option>
                <option value="2">Video #2</option>
                <option value="3">Video #3</option>
                <option value="4">Video #4</option>
                <option value="5">Video #5</option>
                <option value="6" selected>Video #6</option>
              </select>
              <select id="pub-privacy" class="bg-slate-950 border rounded-lg p-2.5 text-xs text-white">
                <option value="unlisted">Unlisted (Sched)</option>
                <option value="public">Public</option>
              </select>
            </div>
          </div>

          <!-- YPP Monetization Safeguards Audit -->
          <div>
            <button onclick="auditCompliance()" class="w-full py-2 bg-slate-950 border rounded-lg text-emerald-400 hover:bg-slate-800 text-xs font-mono transition flex items-center justify-center gap-2">
              🛡️ Audit YPP Policy Compliance
            </button>
          </div>

          <!-- Direct Multi-Platform API Dispatch -->
          <div class="space-y-1.5">
            <label class="text-xs font-semibold text-slate-400 block">Direct Social API Dispatch (No Clipboard)</label>
            <div class="grid grid-cols-3 gap-1.5">
              <button onclick="dispatchSocial('x')" class="p-2 bg-slate-950 border rounded-lg hover:bg-slate-800 text-[11px] font-mono text-center transition">
                🚀 X v2
              </button>
              <button onclick="dispatchSocial('linkedin')" class="p-2 bg-slate-950 border rounded-lg hover:bg-slate-800 text-[11px] font-mono text-center transition">
                🚀 LinkedIn
              </button>
              <button onclick="dispatchSocial('newsletter')" class="p-2 bg-slate-950 border rounded-lg hover:bg-slate-800 text-[11px] font-mono text-center transition">
                🚀 Newsletter
              </button>
            </div>
          </div>

          <!-- Quick Copy & Viral Analysis -->
          <div class="space-y-1.5 pt-1">
            <div class="grid grid-cols-2 gap-1.5">
              <button onclick="copySocial('monetize')" class="p-2 bg-slate-950 border rounded-lg hover:bg-slate-800 text-[11px] font-mono text-emerald-300 transition">
                💰 Monetize Pack
              </button>
              <button onclick="runSwipeAnalysis()" class="p-2 bg-slate-950 border rounded-lg text-purple-300 hover:bg-slate-800 text-[11px] font-mono transition">
                ⚡ Viral Swipe
              </button>
            </div>
          </div>

          <div id="pub-status" class="hidden bg-slate-950 border rounded-xl p-2.5 text-xs font-mono text-purple-300 max-h-40 overflow-y-auto"></div>
        </div>

        <div class="pt-2 border-t">
          <button onclick="publishVideo()" class="w-full py-2.5 bg-purple-600 hover:bg-purple-500 font-semibold rounded-lg text-xs text-white transition">
            🚀 1-Click Upload to YouTube Data API
          </button>
        </div>
      </section>

    </main>

  </div>

  <!-- FULLSCREEN TELEPROMPTER OVERLAY -->
  <div id="prompter-modal" class="fixed inset-0 bg-slate-950 z-50 hidden flex flex-col p-6 space-y-4">
    <div class="flex justify-between items-center border-b pb-4">
      <h2 class="text-xl font-bold text-white flex items-center gap-2">
        <span>📜</span> Live Prompter Mode
      </h2>
      <div class="flex items-center gap-2">
        <button onclick="changeFontSize(-2)" class="px-3 py-1 bg-slate-800 rounded text-xs font-bold">A-</button>
        <button onclick="changeFontSize(2)" class="px-3 py-1 bg-slate-800 rounded text-xs font-bold">A+</button>
        <button id="scroll-btn" onclick="toggleScroll()" class="px-4 py-1 bg-emerald-600 rounded text-xs font-bold text-white">▶ Auto-Scroll</button>
        <button onclick="closeFullPrompter()" class="px-3 py-1 bg-rose-600 rounded text-xs font-bold text-white">✕ Close</button>
      </div>
    </div>
    <div id="prompter-scrollbox" class="flex-1 overflow-y-auto p-8 rounded-xl bg-slate-900 border text-slate-100 font-sans leading-relaxed text-2xl">
      <div id="prompter-full-text" class="max-w-4xl mx-auto space-y-4"></div>
    </div>
  </div>

  <script>
    let scrollTimer = null;
    let prompterSize = 24;

    window.onload = () => { loadScript(); };

    function showBanner(msg, isSuccess=true) {
      const b = document.getElementById("banner");
      b.className = `p-3 rounded-xl text-xs font-mono block ${isSuccess ? 'bg-emerald-950 border border-emerald-800 text-emerald-300' : 'bg-rose-950 border border-rose-800 text-rose-300'}`;
      b.innerText = msg;
    }

    async function runPreflight() {
      showBanner("Running 4-Phase Pre-Flight QA Gate...", true);
      const res = await fetch("/api/status");
      const data = await res.json();
      if(data.status === "PASS") {
        showBanner(`✔ Pre-flight Gate PASSED! Discovered ${data.skills_discovered} skills, PipeWire audio locked.`, true);
      } else {
        showBanner(`❌ Pre-flight issues detected. Symlink: ${data.symlink_verified}, Audio: ${data.pipewire_audio_locked}`, false);
      }
    }

    async function loadScript() {
      const num = document.getElementById("teleprompter-select").value;
      const res = await fetch(`/api/teleprompter/${num}`);
      const text = await res.text();
      document.getElementById("script-box").innerText = text;
      document.getElementById("prompter-full-text").innerText = text;
    }

    async function triggerDemo() {
      const num = document.getElementById("teleprompter-select").value;
      showBanner(`Staging live demo environment for Episode #${num}...`, true);
      const res = await fetch(`/api/trigger-demo/${num}`);
      const data = await res.json();
      showBanner(`✔ ${data.message}`, true);
    }

    async function renderHeadless(format) {
      showBanner(`Programmatic video assembly in progress (${format.toUpperCase()})...`, true);
      const res = await fetch(`/api/render-headless?format=${format}`);
      const data = await res.json();
      if(data.status === "SUCCESS") {
        showBanner(`✔ Video Rendered Headlessly: ${data.output_file} (${data.resolution} @ ${data.framerate}fps, ${data.target_lufs} LUFS)`, true);
        document.getElementById("qa-path").value = data.output_file;
      } else {
        showBanner(`❌ Headless render error: ${data.error || 'Failed'}`, false);
      }
    }

    async function auditVideo() {
      const path = document.getElementById("qa-path").value;
      showBanner(`Auditing ${path}...`, true);
      const res = await fetch(`/api/qa/audit?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      
      const log = document.getElementById("qa-log");
      log.classList.remove("hidden");
      log.innerText = JSON.stringify(data, null, 2);

      if(data.lufs) {
        document.getElementById("lufs-val").innerText = `${data.lufs} LUFS (${data.lufs_pass ? 'PASS' : 'FAIL'})`;
        const bar = document.getElementById("lufs-bar");
        bar.className = `meter-bar h-full ${data.lufs_pass ? 'bg-emerald-600' : 'bg-rose-600'}`;
        const pct = Math.max(10, Math.min(100, ((data.lufs + 35) / 29) * 100));
        bar.style.width = `${pct}%`;
      }
      if(data.fps) {
        document.getElementById("fps-val").innerText = `${data.fps} fps (${data.fps_pass ? 'PASS' : 'FAIL'})`;
        document.getElementById("fps-val").className = `font-bold ${data.fps_pass ? 'text-emerald-400' : 'text-rose-400'}`;
      }
      showBanner(`✔ Audit finished: Verdict = ${data.verdict}`, data.verdict === 'PASS');
    }

    async function autofixAudio() {
      const path = document.getElementById("qa-path").value;
      showBanner("Applying lossless EBU R128 normalization to -14.0 LUFS...", true);
      const res = await fetch(`/api/qa/autofix?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      if(data.output_file) {
        showBanner(`✔ Audio normalized! Output: ${data.output_file}`, true);
        document.getElementById("qa-path").value = data.output_file;
        auditVideo();
      } else {
        showBanner(`❌ Auto-fix error: ${data.error}`, false);
      }
    }

    async function auditCompliance() {
      const num = document.getElementById("pub-num").value;
      showBanner(`Auditing Episode #${num} against YouTube Partner Program policies...`, true);
      const res = await fetch(`/api/compliance/${num}`);
      const data = await res.json();
      const statusBox = document.getElementById("pub-status");
      statusBox.classList.remove("hidden");
      statusBox.innerText = JSON.stringify(data, null, 2);
      showBanner(`🛡️ YPP Score: ${data.ypp_readiness_score}/100 [Verdict: ${data.verdict}] - RPM Potential: ${data.rpm_potential}`, data.verdict === "APPROVED_FOR_YPP");
    }

    async function dispatchSocial(platform) {
      const num = document.getElementById("pub-num").value;
      showBanner(`Dispatching Episode #${num} to ${platform.toUpperCase()} API...`, true);
      const res = await fetch(`/api/dispatch/${num}/${platform}`);
      const data = await res.json();
      const statusBox = document.getElementById("pub-status");
      statusBox.classList.remove("hidden");
      statusBox.innerText = JSON.stringify(data, null, 2);
      showBanner(`✔ Direct dispatch to ${platform.toUpperCase()} completed: ${data.mode || data.status}`, true);
    }

    async function runAutonomousNightly() {
      const num = document.getElementById("pub-num").value;
      showBanner(`Executing Full Autonomous Pipeline for Episode #${num}...`, true);
      const res = await fetch(`/api/scheduler/run-now?num=${num}`);
      const data = await res.json();
      const statusBox = document.getElementById("pub-status");
      statusBox.classList.remove("hidden");
      statusBox.innerText = JSON.stringify(data, null, 2);
      showBanner(`✔ Autonomous Pipeline Verdict: ${data.verdict || 'COMPLETED'}`, data.verdict === "SUCCESS");
    }

    async function runSwipeAnalysis() {
      showBanner("Scanning YouTube niche dataset with 21 viral formulas...", true);
      const res = await fetch("/api/swipe");
      const data = await res.json();
      const statusBox = document.getElementById("pub-status");
      statusBox.classList.remove("hidden");
      statusBox.innerText = JSON.stringify(data, null, 2);
      showBanner(`✔ Outlier scan complete! ${data.outliers ? data.outliers.length : 0} outliers found.`, true);
    }

    async function copySocial(type) {
      const num = document.getElementById("pub-num").value;
      const res = await fetch(`/api/repurpose-asset/${num}/${type}`);
      const data = await res.json();
      if(data.content) {
        navigator.clipboard.writeText(data.content);
        showBanner(`✔ Copied ${type.toUpperCase()} content pack to clipboard!`, true);
      }
    }

    async function publishVideo() {
      const num = document.getElementById("pub-num").value;
      const privacy = document.getElementById("pub-privacy").value;
      const path = document.getElementById("qa-path").value;
      showBanner(`Staging Video #${num} for YouTube Data API v3...`, true);
      const res = await fetch(`/api/upload?num=${num}&path=${encodeURIComponent(path)}&privacy=${privacy}`);
      const data = await res.json();
      const statusBox = document.getElementById("pub-status");
      statusBox.classList.remove("hidden");
      statusBox.innerText = data.message || "Upload status updated.";
      showBanner("✔ Publish command staged for YouTube Data API!", true);
    }

    function openFullPrompter() {
      document.getElementById("prompter-modal").classList.remove("hidden");
    }
    function closeFullPrompter() {
      clearInterval(scrollTimer);
      scrollTimer = null;
      document.getElementById("scroll-btn").innerText = "▶ Auto-Scroll";
      document.getElementById("prompter-modal").classList.add("hidden");
    }
    function toggleScroll() {
      const box = document.getElementById("prompter-scrollbox");
      const btn = document.getElementById("scroll-btn");
      if(scrollTimer) {
        clearInterval(scrollTimer);
        scrollTimer = null;
        btn.innerText = "▶ Auto-Scroll";
      } else {
        scrollTimer = setInterval(() => { box.scrollTop += 2; }, 50);
        btn.innerText = "⏸ Pause";
      }
    }
    function changeFontSize(delta) {
      prompterSize = Math.max(16, Math.min(48, prompterSize + delta));
      document.getElementById("prompter-full-text").style.fontSize = `${prompterSize}px`;
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_UI

@app.get("/api/status")
def get_status():
    return run_full_preflight_audit()

@app.get("/api/runs")
def get_runs():
    return {"latest_audits": fetch_latest_audits()}

@app.get("/api/teleprompter/{num}")
def get_teleprompter_script(num: int):
    script_file = os.path.join(WORKSPACE, f"video_0{num}_script.md")
    if not os.path.exists(script_file):
        script_file = os.path.join(WORKSPACE, f"video_{num}_script.md")
    if os.path.exists(script_file):
        with open(script_file, "r", encoding="utf-8") as f:
            return PlainTextResponse(f.read())
    return PlainTextResponse(f"Teleprompter script for Video #{num} not found.")

@app.get("/api/trigger-demo/{num}")
def trigger_demo(num: int):
    script_map = {
        1: "./scripts/task-01-fullstack.sh",
        2: "./scripts/video-02-demo.sh",
        3: "./scripts/video-03-demo.sh",
        4: "./scripts/video-04-demo.sh",
        5: "./scripts/video-05-demo.sh",
        6: "./scripts/video-06-demo.sh",
    }
    target = script_map.get(num, "./scripts/task-01-fullstack.sh")
    subprocess.Popen([target], cwd=WORKSPACE, shell=True)
    return {"success": True, "message": f"Demo script {target} launched in background."}

@app.get("/api/qa/audit")
def qa_audit(path: str = Query(...)):
    try:
        res = audit_video_compliance(path)
        return res
    except Exception as e:
        return {"error": str(e), "verdict": "FAIL"}

@app.get("/api/qa/autofix")
def qa_autofix(path: str = Query(...)):
    try:
        out_file = auto_normalize_audio(path)
        return {"success": True, "output_file": out_file}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/swipe")
def api_swipe(file_path: str = None, min_mult: float = 2.0):
    try:
        if not file_path:
            niche_p = os.path.join(WORKSPACE, "data/niche_collected.json")
            file_path = "data/niche_collected.json" if os.path.exists(niche_p) else "data/sample_collected.json"
        return get_outliers(file_path, min_mult)
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/upload")
def upload_video(num: int, path: str, privacy: str = "unlisted"):
    full_path = os.path.join(WORKSPACE, path) if not os.path.isabs(path) else path
    cmd = ["./scripts/youtube-upload.sh", str(num), full_path, "--privacy", privacy]
    proc = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True)
    return {"success": proc.returncode == 0, "message": proc.stdout + proc.stderr}

@app.get("/api/repurpose/{num}")
def run_repurpose(num: int):
    proc = subprocess.run(["./scripts/repurpose-engine.sh", str(num)], cwd=WORKSPACE, capture_output=True, text=True)
    return {"success": proc.returncode == 0, "output": proc.stdout}

@app.get("/api/repurpose-asset/{num}/{type}")
def get_repurpose_asset(num: int, type: str):
    type_file_map = {
        "carousel": "x_linkedin_carousel.md",
        "newsletter": "developer_newsletter.md",
        "release": "github_release_notes.md",
        "monetize": "monetization_pack.md"
    }
    filename = type_file_map.get(type)
    if not filename:
        return {"content": None}
    
    filepath = os.path.join(WORKSPACE, f"repurposed/video_0{num}", filename)
    if not os.path.exists(filepath):
        subprocess.run(["./scripts/repurpose-engine.sh", str(num)], cwd=WORKSPACE, capture_output=True, text=True)
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    return {"content": None}

@app.get("/api/compliance/{num}")
def api_compliance(num: int):
    return audit_ypp_compliance(num)

@app.get("/api/render-headless")
def api_render_headless(format: str = "landscape"):
    test_clip = os.path.join(WORKSPACE, "exports/automated_render.mp4")
    if not os.path.exists(test_clip):
        # Create test video clip if not present
        os.makedirs(os.path.dirname(test_clip), exist_ok=True)
        dummy_cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=duration=3:size=1920x1080:rate=60", "-f", "lavfi", "-i", "sine=frequency=1000:duration=3", "-c:v", "libx264", "-c:a", "aac", test_clip]
        subprocess.run(dummy_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    output_filename = "automated_short.mp4" if format == "short" else "automated_render.mp4"
    res = stitch_video_headless(
        clip_paths=[test_clip],
        output_filename=output_filename,
        video_format=format
    )
    return res

@app.get("/api/dispatch/{num}/{platform}")
def api_dispatch(num: int, platform: str):
    p = platform.lower()
    if p in ["x", "twitter"]:
        content = f"Hardcore DevOps Challenge (Video #{num}): Delete My Ubuntu Server If This Agent Fails. Full starter repo: https://github.com/yourusername/antigravity-devops-guard #buildinpublic"
        return dispatch_to_x(num, content)
    elif platform == "linkedin":
        content = f"Here is our complete architecture breakdown for Episode #{num}. Fully automated with Google Antigravity.\n\nClone the starter code: https://github.com/yourusername/antigravity-demo"
        return dispatch_to_linkedin(num, content)
    elif platform == "newsletter":
        filepath = os.path.join(WORKSPACE, f"repurposed/video_0{num}", "developer_newsletter.md")
        nl_content = "# Developer Newsletter"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                nl_content = f.read()
        return dispatch_to_newsletter(num, nl_content)
    else:
        return {"error": f"Unknown platform: {platform}"}

@app.get("/api/scheduler/status")
def api_scheduler_status():
    return scheduler.get_status()

@app.get("/api/scheduler/run-now")
async def api_scheduler_run_now(num: int = 2):
    return await scheduler.execute_hands_off_pipeline(num)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
