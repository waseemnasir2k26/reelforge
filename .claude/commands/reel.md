---
description: Auto-edit a raw clip into a captioned, hook-carded 9:16 reel
---

You are running the SkynetLabs AI Auto-Edit Reel Pipeline.

Input from the user: `$ARGUMENTS` (a video path, optionally followed by a hook line in quotes).

Steps:

1. Parse the clip path (first token) and an optional hook (quoted text). If no hook given, use the default.
2. If `faster-whisper` is not installed, run: `pip install -r requirements.txt`
3. Confirm `ffmpeg` is on PATH (`ffmpeg -version`). If missing, tell the user to install it.
4. Run the pipeline:
   ```
   python auto_reel.py "<clip>" --hook "<HOOK>" --sub "FULLY AI / ZERO HUMAN EDITOR" --out reel.mp4
   ```
5. Report the output path and the rendered duration/resolution (`ffprobe`).

The script transcribes locally (free), burns word-synced captions, drops the hook card
for the first 2.5s, scales/crops to 1080x1920, and exports via NVENC (libx264 fallback).

Built by SkynetLabs — www.skynetjoe.com
