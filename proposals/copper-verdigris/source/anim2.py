import os, math, shutil, subprocess, sys
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
A = {"__file__": os.path.join(HERE, "anim.py"), "__name__": "anim_lib"}
exec(open(os.path.join(HERE, "anim.py")).read(), A)
g = A["g"]
for k in ("INK", "MUTED", "WHITE", "PAPER", "SECTION", "HAIR", "CU", "CU_TINT", "CU_DARK", "CU_DEEP", "VG", "VG_TINT",
          "VG_DARK", "VG_DEEP", "VG_MIST", "COB", "SANS"):
    globals()[k] = g[k]
r, ln, t, sq, doc, path, frame, defs, status, person = (g[k] for k in ("r", "ln", "t", "sq", "doc", "path", "frame", "defs", "status", "person"))
clamp, ease, seg = A["clamp"], A["ease"], A["seg"]

S = 720
FPS = 30


def wrap(body, fig, title, code, T, dur, caption):
    fr = frame(S, S, fig, title, code)
    extra = t(48, 652, caption, 11, INK, weight=600, ls=1.4) + ln(48, 668, 48 + (S - 96) * clamp(T / dur), 668, VG, 1.5)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">'
            f'<rect width="{S}" height="{S}" fill="{PAPER}"/>{defs("a2")}{fr}{body}{extra}</svg>')


def cap(T, steps):
    return [s for ts, s in steps if T >= ts][-1]


def grow(x1, y1, x2, y2, p, stroke, sw, extra=""):
    if p <= 0:
        return ""
    return ln(x1, y1, round(x1 + (x2 - x1) * p, 1), round(y1 + (y2 - y1) * p, 1), stroke, sw, extra)


def fade(p, inner):
    return f'<g opacity="{round(clamp(p), 3)}">{inner}</g>' if p > 0 else ""


# ---------------------------------------------------------------- 1 · window to act
def window(T):
    DUR = 9.5
    c = []
    Z = [(132, 272, "FLAGGED ON ARRIVAL", VG_DEEP), (272, 468, "FLAGGED AFTER ENTRY", INK), (468, 672, "TOO LATE", CU_DARK)]
    lanes = [(168, "TODAY", (0, 5, 5), 0.8), (408, "WITH ISOMER", (7, 0, 3), 4.2)]
    a = seg(T, 0, 0.6)
    hdr = ""
    for x0, x1, lab, col in Z:
        hdr += t(x0 + 8, 92, lab, 8, col, weight=600)
    c.append(fade(a, hdr))
    for li, (y0, name, plan, start) in enumerate(lanes):
        la = seg(T, start - 0.6, start)
        body = [t(48, y0 + 22, name, 9, INK, weight=600)]
        body.append(r(Z[0][0], y0, Z[0][1] - Z[0][0], 150, VG_TINT, "none", 0))
        body.append(r(Z[2][0], y0, Z[2][1] - Z[2][0], 150, f"url(#a2-hatch)", "none", 0, 'opacity="0.22"'))
        body.append(ln(Z[0][0], y0 + 150, Z[2][1], y0 + 150, INK, 1))
        for x0, x1, *_ in Z:
            body.append(ln(x0, y0 - 6, x0, y0 + 156, MUTED, 0.75, 'stroke-dasharray="3 3"'))
        body.append(ln(Z[2][1], y0 - 6, Z[2][1], y0 + 156, MUTED, 0.75, 'stroke-dasharray="3 3"'))
        c.append(fade(la, "".join(body)))
        # scan line on the Isomer lane
        if li == 1:
            pulse = 0.5 + 0.5 * math.sin(T * 9) if start <= T <= start + 2.4 else 0
            c.append(fade(la, ln(Z[0][0], y0 - 14, Z[0][0], y0 + 160, VG, 1.5 + 1.5 * pulse) + sq(Z[0][0], y0 - 14, 7, VG)))
        # claims
        targets = []
        n_arr, n_after, n_late = plan
        for zi, n in enumerate((n_arr, n_after, n_late)):
            for k in range(n):
                col, row = k % 5, k // 5
                targets.append((zi, Z[zi][0] + 24 + col * 34, y0 + 40 + row * 44))
        caught = 0
        for k, (zi, tx, ty) in enumerate(targets):
            st = start + k * 0.14
            if T < st:
                continue
            p = ease((T - st) / 1.3)
            x = 114 + (tx - 114) * p
            landed = p >= 0.999
            if landed and zi < 2:
                caught += 1
            if zi == 0:
                fill, stroke = (VG, VG_DARK) if x >= Z[0][0] + 4 else (WHITE, INK)
            elif zi == 2:
                fill, stroke = (CU_TINT, CU) if x >= Z[2][0] else (WHITE, INK)
            else:
                fill, stroke = WHITE, INK
            c.append(fade(min(1, p * 6), r(round(x, 1), ty, 18, 18, fill, stroke, 1.25)))
        if T >= start + 0.2:
            pct = caught * 10
            c.append(t(48, y0 + 44, f"{pct}%", 22, VG_DEEP if li == 1 else INK, weight=600, ls=0.2, family=SANS))
            c.append(t(48, y0 + 62, "IN TIME", 8, MUTED))
    # delta
    da = seg(T, 7.4, 7.9)
    c.append(fade(da, t(48, 612, "50% → 70%", 20, VG_DEEP, weight=600, ls=0.2, family=SANS) + t(170, 610, "OF HIGH-RISK CLAIMS CAUGHT IN TIME", 9, INK, weight=500)))
    caption = cap(T, [(0, "10 HIGH-RISK CLAIMS"), (0.8, "TODAY · RULES FIRE AFTER ENTRY"), (4.2, "WITH ISOMER · READ ON ARRIVAL"),
                      (7.4, "+20 POINTS CAUGHT IN TIME")])
    return wrap("\n".join(c), "A2", "WINDOW TO ACT", "AN-02", T, DUR, caption), DUR


# ---------------------------------------------------------------- 2 · claim graph assembles
def graph(T):
    DUR = 9.0
    c = [r(48, 56, S - 96, S - 168, "url(#a2-dots)", "none", 0)]

    def node(x, y, typ, nid, kind="e", icon=False):
        fill, stroke, tc, sc = WHITE, INK, INK, MUTED
        if kind == "s": fill, stroke, tc, sc = CU_TINT, CU, CU_DARK, CU_DEEP
        if kind == "a": fill, stroke, tc, sc = VG_TINT, VG, VG_DARK, VG_DEEP
        o = [r(x, y, 120, 48, fill, stroke, 1.25 if kind != "e" else 1), t(x + 10, y + 20, typ, 10, tc, weight=600, ls=1), t(x + 10, y + 36, nid, 9, sc)]
        if icon:
            o.append(person(x + 98, y + 12, 24, INK, WHITE, 1))
        return "".join(o)

    # sources arrive
    srcs = [(150, 110, "p.1"), (106, 520, "p.2"), (334, 520, "p.4")]
    for i, (x, y, lab) in enumerate(srcs):
        p = seg(T, 0.3 + i * 0.2, 0.8 + i * 0.2)
        c.append(fade(p, doc(x, y, 52, 68, WHITE, MUTED, [0.6, 0.8, 0.5, 0.7, 0.6]) + t(x, y + 84, f"SRC-0{i+1} · {lab}", 9, MUTED)))
    # claim
    pc = seg(T, 1.0, 1.4)
    c.append(fade(pc, r(288, 280, 144, 56, WHITE, INK, 1.5) + r(294, 286, 132, 44, "none", INK, 0.75) +
                  t(306, 306, "CLAIM", 11, INK, weight=600, ls=1.2) + t(306, 322, "WC-2026-04417", 9, MUTED)))
    dash = 'stroke-dasharray="3 3"'
    # (start, edge from, edge to, color, sw, trace, node args)
    steps = [
        (1.6, (360, 280), (360, 168), INK, 1, ((202, 144), (300, 144)), (300, 120, "LOSS DATE", "E-011", "e", False)),
        (2.2, (288, 308), (192, 308), INK, 1, None, (72, 284, "CLAIMANT", "E-002", "e", True)),
        (2.8, (432, 308), (552, 308), INK, 1, None, (552, 284, "POLICY", "E-003 · LIMIT", "e", False)),
        (3.4, (132, 332), (132, 432), INK, 1, ((132, 520), (132, 480)), (72, 432, "COUNSEL", "E-007", "e", True)),
        (4.2, (360, 336), (360, 432), CU, 1.25, ((360, 520), (360, 480)), (300, 432, "DEMAND", "S-014 · TLD", "s", False)),
        (5.0, (420, 456), (552, 456), CU, 1.25, None, (552, 432, "DEADLINE", "S-015 · 30d", "s", False)),
        (6.0, (612, 480), (612, 576 - 40), VG, 1.25, None, (552, 536, "ACT", "A-004 · HOLD", "a", False)),
    ]
    facts = risks = acts = 0
    for st, a_, b_, col, sw, trace, nd in steps:
        if T < st:
            continue
        if trace:
            c.append(grow(trace[0][0], trace[0][1], trace[1][0], trace[1][1], seg(T, st, st + 0.35), MUTED, 1, dash))
        c.append(grow(a_[0], a_[1], b_[0], b_[1], seg(T, st + 0.2, st + 0.6), col, sw))
        pn = seg(T, st + 0.5, st + 0.8)
        c.append(fade(pn, node(*nd)))
        if pn > 0.5:
            if nd[4] == "s": risks += 1
            elif nd[4] == "a": acts += 1
            else: facts += 1
    c.append(t(672, 80, f"FACTS {facts + risks}   RISKS {risks}   ACTIONS {acts}", 9, INK, "end", 600))
    if T > 7.0:
        c.append(fade(seg(T, 7.0, 7.4), status(440, 628, "ok", "EVERY FACT TRACED TO A PAGE")))
    caption = cap(T, [(0, "DOCUMENTS ARRIVE"), (1.0, "READ AGAINST THE INSURANCE ONTOLOGY"), (4.2, "RISK SURFACES IN THE GRAPH"), (6.0, "ISOMER ACTS · PERSON AUTHORIZES")])
    return wrap("\n".join(c), "A3", "CLAIM GRAPH", "AN-03", T, DUR, caption), DUR


# ---------------------------------------------------------------- 3 · elastic
def elastic(T):
    DUR = 9.0
    vals = [1, 1, 1.1, 0.9, 1, 1, 1.2, 20, 17, 13, 9, 6, 4, 3, 2.2, 1.6, 1.3, 1.1, 1, 1]
    x0, x1, base, top = 96, 672, 560, 120
    k = (base - top) / 20
    bw = (x1 - x0) / len(vals)
    cap_v = 1.6
    capy = base - cap_v * k
    c = []
    a = seg(T, 0, 0.6)
    grid = ""
    for m in (1, 5, 10, 15, 20):
        y = base - m * k
        grid += ln(x0, y, x1, y, HAIR, 1) + t(x0 - 10, y + 3, f"{m}×", 8, MUTED, "end")
    grid += ln(x0, base, x1, base, INK, 1)
    for i in range(len(vals) + 1):
        grid += ln(x0 + i * bw, base, x0 + i * bw, base + (8 if i % 7 == 0 else 4), INK, 0.75)
        if i % 7 == 0:
            grid += t(x0 + i * bw, base + 22, f"d{i}", 8, MUTED, "middle")
    c.append(fade(a, grid))
    c.append(fade(a, ln(x0, capy, x1, capy, INK, 1.25, 'stroke-dasharray="6 3"') + t(x1, capy - 8, "ADJUSTER CAPACITY", 8, INK, "end", 500)))
    t_bars0, per = 0.8, 0.17
    cover = seg(T, 5.2, 7.2)  # isomer envelope sweep
    xc = x0 + (x1 - x0) * cover
    backlog = 0
    for i, v in enumerate(vals):
        st = t_bars0 + i * per
        if T < st:
            continue
        p = ease((T - st) / 0.45)
        hv = v * p
        x = x0 + i * bw + 3
        c.append(r(round(x, 1), round(base - hv * k, 1), round(bw - 6, 1), round(hv * k, 1), WHITE, INK, 0.75))
        if hv > cap_v:
            covered = (x + bw - 6) <= xc
            op = 0.15 if covered else 1
            c.append(f'<g opacity="{op}">' + r(round(x, 1), round(base - hv * k, 1), round(bw - 6, 1), round((hv - cap_v) * k, 1), "url(#a2-hatch)", CU, 0.75) + '</g>')
            if not covered:
                backlog += (hv - cap_v)
    if T > t_bars0 + 7 * per:
        lx = x0 + 7 * bw
        c.append(fade(seg(T, t_bars0 + 7 * per, t_bars0 + 7 * per + 0.3), ln(lx, base, lx, top - 12, CU, 1, 'stroke-dasharray="4 3"') + t(lx - 6, top - 16, "LANDFALL", 8, CU_DARK, "end", 600)))
    if cover > 0:
        env = f"M{x0} {base}"
        for i, v in enumerate(vals):
            xa, xb = x0 + i * bw, x0 + (i + 1) * bw
            if xa >= xc:
                break
            env += f" V{round(base - v * k - 4, 1)} H{round(min(xb, xc), 1)}"
        c.append(path(env, VG, 1.75))
        c.append(t(x0 + 9 * bw + 8, top + 14, "ISOMER COVERAGE", 8, VG_DEEP, weight=600))
    if T > 2.4 and cover < 1:
        c.append(fade(seg(T, 2.4, 2.8), r(x0, 600, 10, 10, "url(#a2-hatch)", CU, 0.75) + t(x0 + 16, 609, "UNREVIEWED · WAITING FOR A PERSON", 8, CU_DARK, weight=600)))
    if cover >= 1:
        c.append(fade(seg(T, 7.3, 7.7), status(x0, 609, "ok", "EVERY DOCUMENT READ · SAME DAY")))
    caption = cap(T, [(0, "DAILY CLAIM VOLUME"), (t_bars0 + 7 * per, "LANDFALL · VOLUME UP 20×"), (5.2, "ISOMER SCALES WITH THE SURGE"), (7.3, "SAME COVERAGE ON DAY ONE OF A CAT")])
    return wrap("\n".join(c), "A4", "ELASTIC", "AN-04", T, DUR, caption), DUR


def render(name, fn):
    fr = os.path.join(HERE, "..", "animations", "_frames", name)
    shutil.rmtree(fr, ignore_errors=True)
    os.makedirs(fr, exist_ok=True)
    _, dur = fn(0)
    n = int(dur * FPS)
    for i in range(n):
        svg, _ = fn(i / FPS)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(fr, f"f{i:04d}.png"), output_width=1080, output_height=1080)
    # hold the last frame 1s
    last = os.path.join(fr, f"f{n-1:04d}.png")
    for j in range(FPS):
        shutil.copy(last, os.path.join(fr, f"f{n + j:04d}.png"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", os.path.join(HERE, "..", "animations", f"{name}.mp4")], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%04d.png"),
                    "-vf", "fps=15,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none",
                    os.path.join(HERE, "..", "animations", f"{name}.gif")], check=True)
    return n


if __name__ == "__main__":
    which = sys.argv[1:] or ["window-to-act-1x1", "claim-graph-1x1", "elastic-1x1"]
    fns = {"window-to-act-1x1": window, "claim-graph-1x1": graph, "elastic-1x1": elastic}
    for w in which:
        print(w, render(w, fns[w]))
