# Changelog

All notable changes to this project are documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.10] - 2026-10-12

- Free, local, MIT-licensed CLI (`auto_reel.py`, `faster-whisper` + `ffmpeg`) that turns one raw talking-head take into a captioned, hook-carded 9:16 reel, with a Claude Code `/reel` command and skill under `.claude/`.
- October 2026 review: tree, README and history re-checked; no pipeline, skill or asset changes. Last functional commit is still 2026-06-12 (SEO relaunch as ReelForge).
- The footer section was converted to the standard Work with SkynetLabs links; README links (ffmpeg, python.org, badges, skynetjoe.com) resolve.
- Known gaps: no tests, CI or packaging (clone-and-run only, no package manifest so no version bump); every README roadmap item (silence-trim, karaoke captions, brand preset, batch mode, per-platform caption packs) is still unchecked.

## [2026.09] - 2026-09-16

- Maintenance review of reelforge — a free, local, open-source CLI that turns one raw talking-head take into a captioned, hook-carded vertical 9:16 reel using `faster-whisper` for local transcription and `ffmpeg` for the edit.
- Status: a single 156-line `auto_reel.py` entry point (`--hook`, `--sub`, `--out`) plus a Claude Code integration — `.claude/commands/reel.md` and `.claude/skills/reel/SKILL.md` — so the same pipeline runs as a `/reel` command. MIT licensed, with CONTRIBUTING.md, an `llms.txt` and an SEO-oriented README carrying a rendered `assets/hero.png`.
- Stack: Python 3.9+, one pinned dependency (`faster-whisper>=1.0.0`), ffmpeg required on PATH; no API key and no cloud call.
- Reviewed September 2026: docs refreshed, versioned as v2026.09. The pipeline script, skill files and assets were not changed; there is no package manifest, so no version bump applied.
- Known gaps: no CHANGELOG before this release (now created); no tests, CI or packaging (no `setup.py`/`pyproject.toml`, so it is clone-and-run only); the README roadmap is entirely unstarted — silence-trim, karaoke captions, brand preset file, batch mode and per-platform caption packs are all unchecked.
