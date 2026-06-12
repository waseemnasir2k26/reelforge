# Contributing to ReelForge

Thanks for helping make ReelForge better. PRs and issues welcome.

## Quick start for contributors

```bash
git clone https://github.com/waseemnasir2k26/reelforge.git
cd reelforge
pip install -r requirements.txt
# ensure ffmpeg is on PATH
python auto_reel.py sample.mp4 --model tiny
```

## Good first issues

- Auto silence-trim using `ffmpeg silencedetect`
- Karaoke / word-highlight caption style (per-word ASS animation)
- Brand preset file (logo overlay, handle, color theme)
- Batch mode: process a whole folder
- Additional caption styles (Hormozi, minimal, boxed)

## Guidelines

- Keep the **one-command, zero-config** philosophy — no required API keys.
- Preserve the **NVENC → libx264 fallback** so it runs without a GPU.
- Test on at least one clip before opening a PR; include the command you ran.
- Match the existing code style (stdlib + `faster-whisper` + `ffmpeg` only).

## Reporting bugs

Open an issue with: OS, Python version, `ffmpeg -version` first line, the exact command, and the error output.
