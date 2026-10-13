#!/usr/bin/env python3
"""GENERATION_EXE renderer: bygger en ferdig kortfilm fra en Creatomate-lignende oppskrift med ffmpeg.

Bruk: python render.py recipe.json out.mp4
Oppskriften inneholder: ett lydspor (Voiceover), sju videoklipp (track 1) og et tekstelement (Subtitles).
"""
import json, os, subprocess, sys

from dl import download
from subs import build_subtitles

W, H, FPS = 1080, 1920, 25
WORK = "work"


def run(cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def probe_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", path]).decode().strip()
    return float(out)


def main(recipe_path, out_path):
    os.makedirs(WORK, exist_ok=True)
    with open(recipe_path, encoding="utf-8") as f:
        recipe = json.load(f)
    els = recipe["elements"]
    voice = next(e for e in els if e.get("type") == "audio")
    clips = [e for e in els if e.get("type") == "video"]
    sub = next((e for e in els if e.get("type") == "text"), {})
    if not clips:
        raise SystemExit("Oppskriften har ingen videoklipp")

    vpath = download(voice["source"], f"{WORK}/voice.mp3")
    vdur = probe_duration(vpath)
    total = vdur + 0.6  # litt luft etter siste ord
    share = total / len(clips)
    print(f"Stemme {vdur:.2f}s, {len(clips)} klipp à {share:.2f}s", flush=True)

    parts = []
    for i, c in enumerate(clips):
        src = download(c["source"], f"{WORK}/clip{i}.mp4")
        part = f"{WORK}/part{i}.mp4"
        cdur = probe_duration(src)
        loop = ["-stream_loop", "-1"] if cdur < share else []
        run(["ffmpeg", "-y", "-v", "error", *loop, "-i", src, "-t", f"{share:.3f}", "-an",
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", part])
        parts.append(part)

    with open(f"{WORK}/list.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt", "-c", "copy", f"{WORK}/video.mp4"])

    vf = "null"
    if sub:
        try:
            build_subtitles(vpath, sub, f"{WORK}/subs.ass")
            vf = f"ass={WORK}/subs.ass"
        except Exception as e:  # undertekster skal ikke stoppe hele filmen
            print(f"ADVARSEL: undertekster feilet: {e}", flush=True)

    run(["ffmpeg", "-y", "-v", "error", "-i", f"{WORK}/video.mp4", "-i", vpath,
         "-filter_complex", f"[0:v]{vf}[v];[1:a]apad,atrim=0:{total:.3f},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-maxrate", "4500k", "-bufsize", "9000k", "-g", "50", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-movflags", "+faststart", out_path])
    print(f"Ferdig: {out_path} ({os.path.getsize(out_path)/1e6:.1f} MB, {probe_duration(out_path):.1f}s)", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
