import os

W, H = 1080, 1920


def ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_color(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}".upper()


def build_subtitles(voice_path, sub, ass_path):
    """Transkriberer stemmen (ord for ord) og lager en ASS-fil der ordet som sies nå er uthevet."""
    from faster_whisper import WhisperModel
    model = WhisperModel(os.environ.get("WHISPER_MODEL", "small.en"), device="cpu", compute_type="int8")
    segments, _ = model.transcribe(voice_path, word_timestamps=True, language="en", vad_filter=False)
    words = []
    for seg in segments:
        for w in (seg.words or []):
            txt = w.word.strip()
            if txt:
                words.append((w.start, w.end, txt))
    maxlen = int(sub.get("transcript_maximum_length", 24) or 24)
    groups, cur = [], []
    for w in words:
        test = " ".join(x[2] for x in cur + [w])
        if cur and (len(test) > maxlen or cur[-1][2][-1:] in ".!?"):
            groups.append(cur); cur = []
        cur.append(w)
    if cur:
        groups.append(cur)

    fill = ass_color(sub.get("fill_color", "#ffffff"))
    hl = ass_color(sub.get("transcript_color", "#ff654f"))
    stroke = ass_color(sub.get("stroke_color", "#000000"))
    font = sub.get("font_family", "Montserrat")
    # 7 vmin av 1080 = ca. 76 px; strek 1 vmin = ca. 11 px
    size = int(round(0.07 * min(W, H)))
    outline = max(2, int(round(0.01 * min(W, H) * 0.6)))
    y_pct = float(str(sub.get("y", "78%")).rstrip("%")) / 100.0
    margin_v = int(H * (1 - y_pct)) - size // 2
    margin_lr = int(W * (1 - float(str(sub.get("width", "84%")).rstrip("%")) / 100.0) / 2)
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Sub,{font},{size},{fill},{fill},{stroke},&H64000000,-1,0,0,0,100,100,0,0,1,{outline},0,2,{margin_lr},{margin_lr},{margin_v},1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for g in groups:
        gstart, gend = g[0][0], g[-1][1]
        for i, (ws, we, wt) in enumerate(g):
            s = gstart if i == 0 else ws
            e = g[i + 1][0] if i + 1 < len(g) else gend
            if e <= s:
                e = s + 0.05
            parts = []
            for j, (_, _, t2) in enumerate(g):
                t2 = t2.replace("{", "(").replace("}", ")").upper()
                parts.append(("{\\c" + hl + "}" + t2 + "{\\c" + fill + "}") if j == i else t2)
            lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Sub,,0,0,0,,{' '.join(parts)}")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Undertekster: {len(words)} ord i {len(groups)} grupper", flush=True)


