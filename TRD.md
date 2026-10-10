# Technical Requirements Document (TRD) - Recording & Audio/Video Specs

## 1. Recording Architecture & Hardware Specs
- **Operating System:** Ubuntu Linux 22.04 / 24.04 LTS.
- **Display Server & Display Protocol:** Wayland with **PipeWire Audio/Video Server**.
- **Capture Software:** OBS Studio (v30.0+) with PipeWire Screen Capture plugin enabled.

---

## 2. Video Capture Specifications
- **Resolution:** 1920x1080 canvas & output resolution (or 3840x2160 native 4K scaling).
- **Framerate:** Locked **60.00 fps** for ultra-smooth terminal scrolling and code animations.
- **Encoder Settings:**
  - Encoder: VAAPI / NVENC / QSV hardware acceleration.
  - Rate Control: CQP (20-22) or CBR (12,000 kbps for 1080p60).
- **IDE & Terminal Formatting:**
  - Font Family: JetBrains Mono / Fira Code.
  - Minimum Font Size: **18px** for code readability at 1080p on mobile screens.
  - UI Cleanliness: Hide sidebar status bars, extra panels, and personal notification icons.

---

## 3. Audio Gain Staging & Loudness Standards
- **Microphone Channel Gain Staging:**
  - Nominal Voice Peak Window: **-18.0 dBFS to -6.0 dBFS** during standard speaking voice.
  - Microphone Headroom: Minimum 6 dB headroom to avoid digital clipping.
- **OBS Filter Chain Configuration:**
  1. **Noise Suppression:** RNNoise (AI noise suppression) or Speex (-30 dB).
  2. **Compressor Filter:**
     - Ratio: `3.0:1`
     - Attack: `6 ms`
     - Release: `60 ms`
     - Output Gain: Boost to achieve nominal -12 dB average.
  3. **Limiter Filter:**
     - Threshold: **-2.0 dBFS** (Strict ceiling catching sudden volume spikes).
- **YouTube Loudness Target:**
  - **Integrated Loudness:** **-14.0 LUFS** (±1.0 LUFS) compliant with YouTube Content ID normalization.
  - **Maximum True Peak:** **-1.0 dBTP** to prevent inter-sample clipping during AAC transcoding.

---

## 4. Sandbox & Docker Validation Specs
- **Container Base Images:** Minimal base images (`alpine`, `distroless`, `node:20-alpine`).
- **User Execution:** Non-root user enforcement inside containers (`USER appuser` / `USER node`).
- **Healthchecks:** Mandatory `HEALTHCHECK` directive in Dockerfiles.
- **Sandboxing Engine:** Antigravity standard sandbox mode (`BypassSandbox: false` default).

---

## 5. Quality Assurance Audit Matrix

| QA Metric | Acceptance Criteria | Tool / Verification |
| :--- | :--- | :--- |
| Video Framerate | Locked 60 fps without dropped frames | OBS Stats / ffmpeg probe |
| Audio Headroom | Peaks -18dB to -6dB, Limiter ceiling -2.0dB | OBS Audio Meter / ffmpeg ebur128 |
| YouTube Loudness | -14.0 LUFS integrated (±1 LUFS) | ffmpeg ebur128 filter |
| Font Readability | Crisp 18px text legible at 1080p mobile preview | Visual inspection |
| Audio Sync | 0ms audio-video drift across 2+ min recording | VLC / Audacity playback check |
