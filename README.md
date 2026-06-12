<div align="center">

# 🤖 AI Auto-Edit Reel Pipeline

**The reel that edited itself.** Record one take → captioned, hook-carded, vertical reel.
Zero human editor.

Built by **[SkynetLabs](https://www.skynetjoe.com)** · `www.skynetjoe.com`

</div>

---

## What this does

You hit record. A script does the rest:

- 🎙️ **Transcribes** locally with `faster-whisper` (word-level, free, no API key)
- ✂️ **Burns captions** synced to the exact word
- 🪧 **Drops a hook card** (`THIS REEL EDITED ITSELF`) on the first 2.5s
- 📐 **Scales + crops** to vertical `1080×1920`
- ⚡ **Exports** via NVENC GPU (auto-falls back to CPU `libx264`)

One command. No timeline. No 3am editing.

---

## Quickstart (with Claude Code)

**1. Install Claude Code** (if you don't have it):

```bash
npm install -g @anthropic-ai/claude-code
```

**2. Clone this repo:**

```bash
git clone https://github.com/waseemnasir2k26/skynet-reel-autoedit.git
cd skynet-reel-autoedit
```

**3. Open Claude Code in the folder:**

```bash
claude
```

**4. Run the command** (Claude installs deps + drives the pipeline for you):

```
/reel myclip.mp4 "THIS REEL EDITED ITSELF"
```

That's it. Claude installs `faster-whisper`, checks `ffmpeg`, runs the edit, and hands you `reel.mp4`.

---

## Or run it raw (no Claude Code)

```bash
pip install -r requirements.txt        # faster-whisper
# ffmpeg must be installed and on PATH

python auto_reel.py myclip.mp4 \
  --hook "THIS REEL EDITED ITSELF" \
  --sub  "FULLY AI / ZERO HUMAN EDITOR" \
  --out  reel.mp4
```

### Flags

| Flag         | Default                        | What                                         |
| ------------ | ------------------------------ | -------------------------------------------- |
| `--hook`     | `THIS REEL EDITED ITSELF`      | on-screen hook card                          |
| `--sub`      | `FULLY AI / ZERO HUMAN EDITOR` | gold subline                                 |
| `--model`    | `base`                         | whisper size: `tiny`/`base`/`small`/`medium` |
| `--hook-len` | `2.5`                          | seconds the hook shows                       |
| `--wpl`      | `3`                            | words per caption line                       |

---

## Requirements

- **Python 3.9+**
- **ffmpeg** on PATH — [download](https://ffmpeg.org/download.html)
- `faster-whisper` (installed via `requirements.txt`)
- GPU optional (NVENC) — CPU works, just slower

---

## Want this wired into your brand?

This is the giveaway version. **SkynetLabs** builds full AI content pipelines —
tuned to your voice, your platforms, auto-publishing daily — so your team stops
editing by hand.

👉 **[www.skynetjoe.com](https://www.skynetjoe.com)** · DM **"SKILL"**

---

<div align="center">

© 2026 SkynetLabs · Free to use & share · `www.skynetjoe.com`

</div>
