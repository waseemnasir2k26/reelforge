#!/usr/bin/env python3
"""
SkynetLabs — AI Auto-Edit Reel Pipeline
www.skynetjoe.com

Record ONE take -> auto-captioned, hook-carded, vertical 9:16 reel.
Zero human editor: transcription drives the captions, ffmpeg does the rest.

Usage:
    python auto_reel.py input.mp4 \
        --hook "THIS REEL EDITED ITSELF" \
        --sub  "FULLY AI / ZERO HUMAN EDITOR" \
        --out  reel.mp4

Requires: ffmpeg on PATH, and `pip install -r requirements.txt`.
"""
import argparse, os, shutil, subprocess, sys, tempfile


def need(binname):
    if shutil.which(binname) is None:
        sys.exit(f"[x] '{binname}' not found on PATH. Install it, then retry.")


def ass_time(t):
    # ASS wants H:MM:SS.cc  (centiseconds)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def transcribe(path, model_size):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("[x] faster-whisper missing. Run: pip install -r requirements.txt")
    print(f"[*] Transcribing with faster-whisper ({model_size}, local, $0)…")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(path, word_timestamps=True)
    words = []
    for seg in segments:
        if not seg.words:
            continue
        for w in seg.words:
            tok = w.word.strip()
            if tok:
                words.append((w.start, w.end, tok))
    if not words:
        sys.exit("[x] No speech detected. Is there audio in the clip?")
    print(f"[*] {len(words)} words timestamped.")
    return words


def build_ass(words, ass_path, words_per_line=3):
    head = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, "
        "Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Cap, Arial, 66, &H00FFFFFF, &H00101010, &H80000000, "
        "-1, 1, 5, 2, 2, 70, 70, 300, 1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    rows = [head]
    for i in range(0, len(words), words_per_line):
        chunk = words[i:i + words_per_line]
        start = chunk[0][0]
        end = chunk[-1][1]
        text = " ".join(w[2] for w in chunk).upper().replace("\n", " ")
        rows.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Cap,,0,0,0,,{text}"
        )
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))


def ff_escape(text):
    # escape for ffmpeg drawtext
    return (text.replace("\\", "\\\\").replace(":", "\\:")
                .replace("'", "’").replace("%", "\\%"))


def render(src, ass_name, hook, sub, out_path, hook_len, workdir):
    base = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1,"
        f"subtitles={ass_name}"
    )
    if hook:
        hk = ff_escape(hook)
        base += (
            f",drawtext=text='{hk}':fontcolor=white:fontsize=78:box=1:"
            f"boxcolor=black@0.55:boxborderw=22:x=(w-text_w)/2:y=h*0.40:"
            f"enable='lt(t,{hook_len})'"
        )
    if sub:
        sb = ff_escape(sub)
        base += (
            f",drawtext=text='{sb}':fontcolor=0xE8B84B:fontsize=42:"
            f"x=(w-text_w)/2:y=h*0.40+110:enable='lt(t,{hook_len})'"
        )

    def encode(vcodec, extra):
        cmd = ["ffmpeg", "-y", "-i", src, "-vf", base,
               "-c:v", vcodec, *extra, "-c:a", "aac", "-b:a", "160k",
               os.path.basename(out_path)]
        return subprocess.run(cmd, cwd=workdir, capture_output=True, text=True)

    print("[*] Rendering (NVENC GPU)…")
    r = encode("h264_nvenc", ["-preset", "p5", "-cq", "23"])
    if r.returncode != 0:
        print("[!] NVENC unavailable — falling back to libx264 (CPU).")
        r = encode("libx264", ["-preset", "medium", "-crf", "20"])
    if r.returncode != 0:
        sys.exit("[x] ffmpeg failed:\n" + r.stderr[-1500:])


def main():
    p = argparse.ArgumentParser(description="SkynetLabs AI Auto-Edit Reel Pipeline")
    p.add_argument("input", help="raw clip (mp4/mov)")
    p.add_argument("--hook", default="THIS REEL EDITED ITSELF", help="on-screen hook card")
    p.add_argument("--sub", default="FULLY AI / ZERO HUMAN EDITOR", help="hook subline (gold)")
    p.add_argument("--out", default="reel.mp4", help="output file")
    p.add_argument("--hook-len", type=float, default=2.5, help="hook card seconds")
    p.add_argument("--model", default="base", help="whisper size: tiny|base|small|medium")
    p.add_argument("--wpl", type=int, default=3, help="words per caption line")
    args = p.parse_args()

    need("ffmpeg")
    src = os.path.abspath(args.input)
    if not os.path.exists(src):
        sys.exit(f"[x] input not found: {src}")
    out = os.path.abspath(args.out)

    words = transcribe(src, args.model)

    work = tempfile.mkdtemp(prefix="skynetreel_")
    ass = os.path.join(work, "cap.ass")
    build_ass(words, ass, args.wpl)
    # copy output into workdir then move out (keeps ffmpeg paths simple on Windows)
    tmp_out = os.path.join(work, os.path.basename(out))
    render(src, "cap.ass", args.hook, args.sub, tmp_out, args.hook_len, work)
    shutil.move(tmp_out, out)
    shutil.rmtree(work, ignore_errors=True)

    print(f"\n[OK] Reel ready -> {out}")
    print("     Built by SkynetLabs auto-edit pipeline — www.skynetjoe.com")


if __name__ == "__main__":
    main()
