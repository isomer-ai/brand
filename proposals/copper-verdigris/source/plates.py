"""Isomer Copper Verdigris plates: drawing primitives and every plate as a function.

Each plate function has the signature fn(pid, w, h) -> (svg_body, title, code).
Run `python3 export.py` to write standalone SVG and PNG files to ../illustrations/.
Rules: ../ILLUSTRATION-GUIDE.md
"""
import json, math, os, datetime


INK = "#141416"; BODY = "#47474D"; MUTED = "#6E6E75"; HAIR = "#E3E3E5"
SECTION = "#ECECEA"; PAPER = "#F6F6F5"; WHITE = "#FFFFFF"; GRAPHITE = "#3A3E3F"
CU = "#B4602F"; CU_DEEP = "#9A5634"; CU_DARK = "#8E4720"; CU_LIGHT = "#E09C6B"; CU_TINT = "#F2DCCB"
VG = "#3F8A85"; VG_DEEP = "#2E6B68"; VG_DARK = "#1F4F4C"; VG_LIGHT = "#8CC2BC"; VG_MIST = "#D3E6E4"; VG_TINT = "#E9F2F1"
RED = "#B4232F"; RED_DEEP = "#8F1B25"; RED_TINT = "#F8DEE0"
COB = "#2F5D99"; COB_DEEP = "#234878"; COB_TINT = "#E3ECF7"
MONO = "'Geist Mono', ui-monospace, monospace"
SANS = "'Geist', system-ui, sans-serif"


def t(x, y, s, size=10, fill=MUTED, anchor="start", weight=400, ls=0.8, family=MONO):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" letter-spacing="{ls}">{s}</text>')


def r(x, y, w, h, fill="none", stroke=INK, sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def ln(x1, y1, x2, y2, stroke=INK, sw=1, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def path(d, stroke=INK, sw=1, fill="none", extra=""):
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="miter" stroke-linecap="square" {extra}/>'


def sq(cx, cy, s=6, fill=INK, stroke="none"):
    return r(cx - s / 2, cy - s / 2, s, s, fill=fill, stroke=stroke, sw=1)


def defs(pid):
    return f'''<defs>
<pattern id="{pid}-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{CU}" stroke-width="1.2"/></pattern>
<pattern id="{pid}-hatchv" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{VG}" stroke-width="1.2"/></pattern>
<pattern id="{pid}-dots" width="24" height="24" patternUnits="userSpaceOnUse"><rect x="11.5" y="11.5" width="1" height="1" fill="{MUTED}" opacity="0.45"/></pattern>
<pattern id="{pid}-micro" width="4" height="4" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="3" height="3" fill="{MUTED}" opacity="0.55"/></pattern>
</defs>'''


def frame(w, h, fig, title, code):
    o = []
    o.append(t(24, 28, f"FIG. {fig}", 10, INK, weight=500, ls=1.4))
    o.append(t(84, 28, title, 10, MUTED, ls=1.2))
    o.append(t(w - 24, 28, code, 10, MUTED, "end", ls=1.2))
    o.append(ln(24, 40, w - 24, 40, MUTED, 0.75))
    x = 24
    while x <= w - 24:
        hgt = 6 if (x - 24) % 40 == 0 else 3
        o.append(ln(x, 40, x, 40 + hgt, MUTED, 0.75))
        x += 8
    y = 40
    while y <= h - 24:
        wd = 6 if (y - 40) % 40 == 0 else 3
        o.append(ln(24, y, 24 + wd, y, MUTED, 0.75))
        y += 8
    o.append(ln(24, 40, 24, h - 24, MUTED, 0.75))
    for (cx, cy) in [(w - 24, h - 24)]:
        o.append(ln(cx - 6, cy, cx + 6, cy, INK, 0.75)); o.append(ln(cx, cy - 6, cx, cy + 6, INK, 0.75))
    o.append(t(40, h - 20, "ISOMER · COPPER VERDIGRIS", 8, MUTED, ls=1.4))
    o.append(t(w - 40, h - 20, "SCALE 1:1", 8, MUTED, "end", ls=1.4))
    return "\n".join(o)


def doc(x, y, w, h, fill=WHITE, stroke=INK, lines=None, hl=None, hlc=CU, sw=1):
    o = [r(x, y, w, h, fill, stroke, sw)]
    o.append(r(x + w - 10, y, 10, 10, SECTION, stroke, sw))
    widths = lines or [0.7, 0.85, 0.6, 0.8, 0.5, 0.75, 0.65, 0.4]
    ly = y + 18
    for i, f in enumerate(widths):
        if ly + 2 > y + h - 8:
            break
        c = hlc if hl is not None and i in hl else "#C9C9CC"
        o.append(r(x + 8, ly, round((w - 16) * f, 1), 2.5, c, "none", 0))
        ly += 9
    return "\n".join(o)


def jn(points, stroke=INK, sw=1, extra="", junctions=False, js=5):
    d = "M" + " L".join(f"{a} {b}" for a, b in points)
    o = [path(d, stroke, sw, extra=extra)]
    if junctions:
        for a, b in points[1:-1]:
            o.append(sq(a, b, js, stroke if stroke != MUTED else MUTED))
    return "\n".join(o)


def status(x, y, kind, label):
    fill, stroke, tc = (COB_TINT, COB, COB_DEEP) if kind == "ok" else (RED_TINT, RED, RED_DEEP)
    word = "OK" if kind == "ok" else "CRITICAL"
    wpx = len(word) * 6 + 22
    return "\n".join([r(x, y - 11, wpx, 16, fill, stroke, 1), sq(x + 8, y - 3, 6, stroke),
                      t(x + 15, y + 1, word, 8, tc, weight=600), t(x + wpx + 8, y + 1, label, 8, tc, weight=500)])


def person(cx, top, s, stroke=INK, fill=WHITE, sw=1):
    """Icon figure: circle head, curved shoulders, flat base. Curves are allowed in icons only."""
    hr = round(s * 0.2, 1)
    hy = round(top + hr + 0.5, 1)
    sy = round(top + s * 0.56, 1)
    rx, ry = round(s * 0.42, 1), round(s * 0.3, 1)
    by = round(top + s, 1)
    return (f'<circle cx="{cx}" cy="{hy}" r="{hr}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<path d="M{cx - rx} {by} V{round(sy + ry, 1)} A{rx} {ry} 0 0 1 {cx + rx} {round(sy + ry, 1)} V{by} Z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="miter"/>')


# ---------- plates ----------

def plate_hero(pid, w, h):
    c = []
    # incoming stack
    for i in range(4, -1, -1):
        c.append(doc(96 + i * 8, 76 + i * 10, 120, 150))
    c.append(t(96, 72, "INBOUND · 214", 9, MUTED))
    c.append(jn([(164, 266), (164, 352)], INK, 1, junctions=False))
    c.append(path("M159 344 L164 352 L169 344", INK, 1))
    # detector plane
    c.append(r(48, 360, 384, 44, SECTION, INK, 1))
    for i in range(24):
        fill = WHITE
        if i in (5, 6):
            fill = VG_MIST
        if i == 15:
            fill = CU_TINT
        c.append(r(56 + i * 15.5, 368, 11, 28, fill, MUTED, 0.75))
    c.append(ln(40, 382, 440, 382, VG, 1.5))
    c.append(sq(40, 382, 6, VG)); c.append(sq(440, 382, 6, VG))
    c.append(t(440, 352, "SCAN · t₀", 9, VG_DEEP, "end"))
    c.append(t(48, 352, "DETECTOR PLANE · 85", 9, MUTED))
    # clear lane
    c.append(jn([(118, 404), (118, 448)], MUTED, 1, junctions=False))
    for row in range(6):
        for col in range(6):
            c.append(r(78 + col * 14, 456 + row * 14, 10, 10, WHITE if (row + col) % 3 else SECTION, MUTED, 0.75))
    c.append(status(78, 558, "ok", "213 CLEAR"))
    # signal lane: straight drop from the firing detector cell
    sx = 56 + 15 * 15.5 + 5.5
    bx = sx - 60
    c.append(ln(sx, 404, sx, 456, CU, 1.25))
    c.append(r(bx, 456, 140, 92, CU_TINT, CU, 1.25))
    c.append(doc(bx + 12, 468, 44, 68, WHITE, CU_DEEP, [0.7, 0.5, 0.8, 0.6, 0.7, 0.4], hl={2}))
    c.append(t(bx + 68, 484, "SIGNAL", 9, CU_DARK, weight=500))
    c.append(t(bx + 68, 500, "TLD", 13, CU_DARK, weight=600, ls=0.4, family=SANS))
    c.append(t(bx + 68, 528, "p.4 · ¶2", 9, CU_DEEP))
    c.append(ln(sx, 548, sx, 604, VG, 1.25))
    c.append(path(f"M{sx-5} 596 L{sx} 604 L{sx+5} 596", VG, 1.25))
    c.append(r(bx, 608, 140, 44, VG_TINT, VG, 1.25))
    c.append(path(f"M{bx+14} 630 L{bx+20} 636 L{bx+32} 624", VG_DEEP, 1.5))
    c.append(t(bx + 42, 626, "ACT", 9, VG_DARK, weight=600))
    c.append(t(bx + 42, 641, "DEADLINE SET", 9, VG_DEEP))
    return "\n".join(c), "Point of receipt", "PL-01"


def plate_graph(pid, w, h):
    c = [r(48, 56, w - 96, h - 104, f"url(#{pid}-dots)", "none", 0)]
    def node(x, y, typ, nid, kind="e"):
        fill, stroke, tc, sc = WHITE, INK, INK, MUTED
        if kind == "s": fill, stroke, tc, sc = CU_TINT, CU, CU_DARK, CU_DEEP
        if kind == "a": fill, stroke, tc, sc = VG_TINT, VG, VG_DARK, VG_DEEP
        o = [r(x, y, 120, 48, fill, stroke, 1.25 if kind != "e" else 1)]
        o.append(t(x + 10, y + 20, typ, 10, tc, weight=600, ls=1))
        o.append(t(x + 10, y + 36, nid, 9, sc))
        return "\n".join(o)
    dash = 'stroke-dasharray="3 3"'
    # edges: all straight
    c.append(ln(360, 168, 360, 280, INK, 1))          # loss date - claim
    c.append(ln(192, 308, 288, 308, INK, 1))          # claimant - claim
    c.append(ln(432, 308, 552, 308, INK, 1))          # claim - policy
    c.append(ln(132, 332, 132, 432, INK, 1))          # claimant - counsel
    c.append(ln(192, 456, 300, 456, INK, 1))          # counsel - demand
    c.append(ln(360, 336, 360, 432, CU, 1.25))        # claim - demand
    c.append(ln(420, 456, 552, 456, CU, 1.25))        # demand - deadline
    c.append(ln(612, 480, 612, 576, VG, 1.25))        # deadline - act
    # source traces: straight
    c.append(ln(202, 144, 300, 144, MUTED, 1, dash))
    c.append(ln(132, 480, 132, 560, MUTED, 1, dash))
    c.append(ln(360, 480, 360, 560, MUTED, 1, dash))
    # nodes
    c.append(r(288, 280, 144, 56, WHITE, INK, 1.5))
    c.append(r(294, 286, 132, 44, "none", INK, 0.75))
    c.append(t(306, 306, "CLAIM", 11, INK, weight=600, ls=1.2))
    c.append(t(306, 322, "WC-2026-04417", 9, MUTED))
    c.append(node(300, 120, "LOSS DATE", "E-011"))
    c.append(node(72, 284, "CLAIMANT", "E-002")); c.append(person(170, 296, 24, INK, WHITE, 1))
    c.append(node(552, 284, "POLICY", "E-003 · LIMIT"))
    c.append(node(72, 432, "COUNSEL", "E-007")); c.append(person(170, 444, 24, INK, WHITE, 1))
    c.append(node(300, 432, "DEMAND", "S-014 · TLD", "s"))
    c.append(node(552, 432, "DEADLINE", "S-015 · 30d", "s"))
    c.append(node(552, 576, "ACT", "A-004 · HOLD", "a"))
    for i, (x, y, lab) in enumerate([(150, 110, "p.1"), (106, 560, "p.2"), (334, 560, "p.4")]):
        c.append(doc(x, y, 52, 68, WHITE, MUTED, [0.6, 0.8, 0.5, 0.7, 0.6]))
        c.append(t(x, y + 84, f"SRC-0{i+1} · {lab}", 9, MUTED))
    lx, ly = 432, 590
    items = [(WHITE, INK, "ENTITY"), (CU_TINT, CU, "SIGNAL"), (VG_TINT, VG, "ACTION")]
    for i, (f, s_, lab) in enumerate(items):
        c.append(r(lx, ly + i * 14 - 7, 8, 8, f, s_, 1))
        c.append(t(lx + 14, ly + i * 14, lab, 8, MUTED))
    c.append(ln(lx, ly + 37, lx + 10, ly + 37, MUTED, 1, dash))
    c.append(t(lx + 14, ly + 40, "SOURCE", 8, MUTED))
    return "\n".join(c), "Claim graph", "PL-02"


def plate_detectors(pid, w, h):
    c = []
    x0, y0, cs, g = 112, 136, 40, 8
    cols, rows = 10, 9
    for i in range(cols):
        c.append(t(x0 + i * (cs + g) + cs / 2, y0 - 12, f"{i+1:02d}", 8, MUTED, "middle"))
    groups = [("TAIL", 0, 1), ("SEVERITY", 2, 4), ("DEFENSE", 5, 6), ("LEAKAGE", 7, 8)]
    fire_cu = {(0, 3), (2, 7), (4, 1)}
    fire_vg = {(0, 4), (4, 2)}
    n = 0
    for rw in range(rows):
        for cl in range(cols):
            x = x0 + cl * (cs + g); y = y0 + rw * (cs + g)
            n += 1
            if n > 85:
                c.append(r(x, y, cs, cs, "none", MUTED, 0.75, 'stroke-dasharray="2 3"'))
                continue
            if (rw, cl) in fire_cu:
                c.append(r(x, y, cs, cs, CU_TINT, CU, 1.25))
                c.append(sq(x + cs / 2, y + cs / 2, 10, CU))
            elif (rw, cl) in fire_vg:
                c.append(r(x, y, cs, cs, VG_TINT, VG, 1.25))
                c.append(sq(x + cs / 2, y + cs / 2, 10, VG))
            else:
                c.append(r(x, y, cs, cs, WHITE, "#C9C9CC", 0.75))
                c.append(r(x + cs / 2 - 1.5, y + cs / 2 - 1.5, 3, 3, "#C9C9CC", "none", 0))
            c.append(t(x + 4, y + cs - 5, f"{n:02d}", 7, "#9A9AA0", ls=0.2))
    bx = x0 + cols * (cs + g) + 8
    for lab, a, b in groups:
        ya = y0 + a * (cs + g); yb = y0 + b * (cs + g) + cs
        c.append(path(f"M{bx} {ya} H{bx+8} V{yb} H{bx}", MUTED, 1))
        c.append(t(bx + 16, (ya + yb) / 2 + 3, lab, 9, INK, weight=500))
    # scan bar across row 4
    sy = y0 + 4 * (cs + g) + cs / 2
    c.append(ln(x0 - 24, sy, bx, sy, VG, 1.5, 'opacity="0.9"'))
    c.append(sq(x0 - 24, sy, 6, VG))
    c.append(t(x0 - 24, y0 + rows * (cs + g) + 20, "85 DETECTORS · EVALUATED AT RECEIPT · 3 FIRING · 2 ACTING", 9, MUTED))
    return "\n".join(c), "Detector array", "PL-03"


def plate_immediate(pid, w, h):
    c = []
    ax0, ax1, ay = 64, 432, 312
    px = (ax1 - ax0) / 30
    X = lambda d: round(ax0 + d * px, 1)
    # y axis
    c.append(ln(ax0, 88, ax0, ay, INK, 1))
    c.append(t(ax0 - 8, 84, "OPTIONS OPEN", 8, MUTED))
    steps = [(0, 112), (5, 140), (10, 170), (15, 200), (20, 230), (25, 260), (28, 284), (30, 304)]
    d = f"M{X(0)} {steps[0][1]}"
    for i in range(1, len(steps)):
        d += f" H{X(steps[i][0])} V{steps[i][1]}"
    # isomer window fill
    c.append(r(X(0), 112, X(1) - X(0), ay - 112, VG_MIST, "none", 0))
    c.append(path(d, INK, 1.5))
    # axis
    c.append(ln(ax0, ay, ax1, ay, INK, 1))
    for dd in range(31):
        hh = 8 if dd % 5 == 0 else 4
        c.append(ln(X(dd), ay, X(dd), ay + hh, INK, 0.75))
        if dd % 5 == 0:
            c.append(t(X(dd), ay + 22, f"d{dd}", 8, MUTED, "middle"))
    # demand window
    c.append(r(X(0), 344, X(30) - X(0), 22, CU_TINT, CU, 1))
    c.append(r(X(0), 344, X(30) - X(0), 22, f"url(#{pid}-hatch)", "none", 0, 'opacity="0.55"'))
    c.append(t(X(0), 384, "TIME-LIMITED DEMAND · 30-DAY CLOCK", 9, CU_DARK, weight=500))
    # markers
    c.append(ln(X(0), 72, X(0), 366, VG, 1.5))
    c.append(sq(X(0), 112, 8, VG))
    c.append(t(X(0) + 10, 76, "ISOMER · t₀", 9, VG_DEEP, weight=600))
    c.append(ln(X(23), 96, X(23), 366, CU, 1.25, 'stroke-dasharray="4 3"'))
    c.append(sq(X(23), 230, 8, CU))
    c.append(t(X(23) - 6, 100, "MANUAL TRIAGE · d23", 9, CU_DARK, "end", weight=600))
    c.append(path(f"M{X(0)} 412 V418 H{X(23)} V412", MUTED, 1))
    c.append(t((X(0) + X(23)) / 2, 432, "Δ 23 DAYS", 9, INK, "middle", weight=500))
    return "\n".join(c), "Immediate", "PL-04"


def plate_continuous(pid, w, h):
    c = []
    c.append(r(64, 72, 368, 14, VG_MIST, VG, 1))
    c.append(t(64, 104, "COVERAGE · EVERY CHANNEL · 24/7", 9, VG_DEEP, weight=500))
    lanes = ["EMAIL", "PORTAL", "MAIL · OCR", "API · EDI"]
    events = [[14, 40, 66, 118, 150, 210, 238, 300, 330], [30, 92, 170, 260, 318], [52, 140, 200, 280], [20, 70, 110, 160, 190, 250, 290, 340]]
    flags = {(0, 5), (2, 2)}
    x0 = 136
    for i, name in enumerate(lanes):
        y = 140 + i * 64
        c.append(t(64, y + 3, name, 8, INK, weight=500))
        c.append(ln(x0, y, 432, y, MUTED, 0.75))
        for j, e in enumerate(events[i]):
            x = x0 + e * 0.85
            if (i, j) in flags:
                c.append(r(x - 6, y - 14, 12, 18, CU_TINT, CU, 1.25))
                c.append(ln(x, y + 6, x, y + 16, CU, 1.25))
            else:
                c.append(r(x - 5, y - 12, 10, 14, WHITE, INK, 0.75))
                c.append(ln(x, y + 6, x, y + 12, VG, 1.25))
    ay = 400
    c.append(ln(x0, ay, 432, ay, INK, 1))
    for k in range(13):
        x = x0 + k * (432 - x0) / 12
        c.append(ln(x, ay, x, ay + (6 if k % 3 == 0 else 3), INK, 0.75))
        if k % 3 == 0:
            c.append(t(x, ay + 18, f"{k*2:02d}:00", 8, MUTED, "middle"))
    c.append(sq(64, 420, 6, VG)); c.append(t(74, 423, "EVALUATED", 8, MUTED))
    c.append(sq(156, 420, 6, CU)); c.append(t(166, 423, "FLAGGED", 8, MUTED))
    return "\n".join(c), "Continuous", "PL-05"


def plate_elastic(pid, w, h):
    c = []
    vals = [1, 1, 1.1, 0.9, 1, 1, 1.2, 20, 17, 13, 9, 6, 4, 3, 2.2, 1.6, 1.3, 1.1, 1, 1]
    x0, x1, base, top = 72, 432, 368, 96
    k = (base - top) / 20
    bw = (x1 - x0) / len(vals)
    for m in (1, 5, 10, 15, 20):
        y = base - m * k
        c.append(ln(x0, y, x1, y, HAIR, 1))
        c.append(t(x0 - 8, y + 3, f"{m}×", 8, MUTED, "end"))
    cap = 1.6
    capy = base - cap * k
    env = f"M{x0} {base}"
    for i, v in enumerate(vals):
        x = x0 + i * bw + 2
        bh = v * k
        c.append(r(round(x, 1), round(base - bh, 1), round(bw - 4, 1), round(bh, 1), WHITE, INK, 0.75))
        if v > cap:
            c.append(r(round(x, 1), round(base - bh, 1), round(bw - 4, 1), round(bh - cap * k, 1), f"url(#{pid}-hatch)", CU, 0.75))
        env += f" V{round(base - bh - 4, 1)} H{round(x0 + (i + 1) * bw, 1)}"
    env += f" V{base}"
    c.append(path(env, VG, 1.5))
    c.append(ln(x0, capy, x1, capy, INK, 1.25, 'stroke-dasharray="6 3"'))
    c.append(t(x1, capy - 6, "ADJUSTER CAPACITY", 8, INK, "end", weight=500))
    c.append(ln(x0, base, x1, base, INK, 1))
    lx = x0 + 7 * bw
    c.append(ln(lx, base, lx, base + 14, CU, 1.25))
    c.append(t(lx, base + 28, "LANDFALL", 8, CU_DARK, "middle", weight=600))
    c.append(t(x0 + 9 * bw + 8, 112, "ISOMER COVERAGE", 8, VG_DEEP, weight=600))
    c.append(ln(x0 + 9 * bw, 109, x0 + 9 * bw + 4, 109, VG, 1.5))
    c.append(r(x0, 420, 10, 10, f"url(#{pid}-hatch)", CU, 0.75)); c.append(t(x0 + 16, 429, "UNREVIEWED WITHOUT ISOMER", 8, MUTED))
    return "\n".join(c), "Elastic · CAT volume", "PL-06"


def plate_signal(pid, w, h):
    c = []
    x0, x1, base = 64, 432, 360
    n = 60
    bw = (x1 - x0) / n
    th = 200
    for i in range(n):
        v = 250 * math.exp(-i / 5.5) + 18 + 10 * ((i * 37) % 7) / 7
        x = x0 + i * bw
        y = base - v
        if y < th:
            c.append(r(round(x + 1, 1), round(y, 1), round(bw - 2, 1), round(v, 1), CU_TINT, CU, 1))
        else:
            c.append(r(round(x + 1, 1), round(y, 1), round(bw - 2, 1), round(v, 1), SECTION, "#B9B9BC", 0.5))
    c.append(ln(x0 - 8, th, x1, th, INK, 1.25))
    c.append(t(x1, th - 8, "INTERRUPT THRESHOLD", 8, INK, "end", weight=500))
    c.append(ln(x0, base, x1, base, INK, 1))
    c.append(t(x0, base + 18, "RANK →", 8, MUTED))
    c.append(t(x1, base + 18, "214 OPEN CLAIMS", 8, MUTED, "end"))
    c.append(path(f"M{x0} 92 V84 H{x0 + 4*bw} V92", CU, 1))
    c.append(t(x0 + 4 * bw + 8, 90, "4 ESCALATED · RANKED BY P&amp;L LINE", 8, CU_DARK, weight=600))
    c.append(status(x0, 412, "ok", "210 STAY QUIET"))
    return "\n".join(c), "Signal, not noise", "PL-07"


def plate_verdicts(pid, w, h):
    c = []
    base = 360
    k = 1.7
    for m in (50, 100, 150):
        y = base - m * k
        c.append(ln(96, y, 400, y, HAIR, 1)); c.append(t(88, y + 3, str(m), 8, MUTED, "end"))
    c.append(r(136, base - 89 * k, 88, 89 * k, WHITE, INK, 1))
    c.append(r(272, base - 135 * k, 88, 135 * k, CU_TINT, CU, 1.25))
    c.append(r(272, base - 135 * k, 88, 135 * k, f"url(#{pid}-hatch)", "none", 0, 'opacity="0.5"'))
    c.append(ln(96, base, 400, base, INK, 1))
    c.append(t(180, base + 20, "2023", 9, INK, "middle", weight=500))
    c.append(t(316, base + 20, "2024", 9, CU_DARK, "middle", weight=600))
    c.append(t(180, base - 89 * k - 8, "n=89", 8, MUTED, "middle"))
    c.append(t(316, base - 135 * k - 8, "n=135 · $31.3B", 8, CU_DARK, "middle"))
    y1 = base - 89 * k; y2 = base - 135 * k
    c.append(path(f"M232 {y1} H252 V{y2} H264", CU, 1, extra='stroke-dasharray="3 3"'))
    c.append(sq(252, y1, 5, CU)); c.append(sq(252, y2, 5, CU))
    c.append(t(244, (y1 + y2) / 2 + 4, "+52%", 12, CU_DARK, "end", 600, 0.2, SANS))
    c.append(t(64, 420, "NUCLEAR VERDICTS · SOURCE: MARATHON STRATEGIES", 8, MUTED))
    return "\n".join(c), "Nuclear verdicts", "PL-08"


def plate_funding(pid, w, h):
    c = []
    s, g = 26, 6
    x0, y0 = 72, 96
    for i in range(50):
        rw, cl = divmod(i, 10)
        x = x0 + cl * (s + g); y = y0 + rw * (s + g)
        c.append(r(x, y, s, s, CU_TINT, CU, 1))
        c.append(r(x + 9, y + 9, 8, 8, CU, "none", 0))
    yb = y0 + 5 * (s + g)
    xr = x0 + 10 * (s + g) - g
    c.append(path(f"M{x0} {yb + 6} V{yb + 12} H{xr} V{yb + 6}", MUTED, 1))
    c.append(t((x0 + xr) / 2, yb + 30, "$50B · THIRD-PARTY LITIGATION FUNDING · 5-YR", 9, CU_DARK, "middle", weight=500))
    c.append(r(x0, 380, s, s, CU_TINT, CU, 1)); c.append(r(x0 + 9, 389, 8, 8, CU, "none", 0))
    c.append(t(x0 + 36, 397, "= $1B", 9, INK))
    c.append(t(64, 432, "SOURCE: U.S. GAO · APCIA", 8, MUTED))
    return "\n".join(c), "Litigation funding", "PL-09"


def plate_industrial(pid, w, h):
    c = []
    x0, y0, size = 92, 76, 296
    c.append(r(x0, y0, size, size, f"url(#{pid}-micro)", "none", 0))
    c.append(r(x0 - 0.5, y0 - 0.5, size + 1, size + 1, "none", INK, 1))
    # highlight one cell
    hx, hy = x0 + 4 * 61, y0 + 4 * 17
    c.append(r(hx - 1, hy - 1, 5, 5, CU, "none", 0))
    c.append(r(hx - 6, hy - 6, 15, 15, "none", CU, 1.25))
    c.append(jn([(hx + 9, hy + 1), (420, hy + 1)], CU, 1, junctions=False))
    c.append(t(420, hy - 6, "1", 9, CU_DARK, "end", weight=600))
    # dimension lines
    c.append(path(f"M{x0} {y0 + size + 8} V{y0 + size + 14} H{x0 + size} V{y0 + size + 8}", MUTED, 1))
    c.append(t(x0 + size / 2, y0 + size + 28, "100", 8, MUTED, "middle"))
    c.append(path(f"M{x0 - 8} {y0} H{x0 - 14} V{y0 + size} H{x0 - 8}", MUTED, 1))
    c.append(t(x0 - 20, y0 + size / 2 + 3, "100", 8, MUTED, "end"))
    c.append(t(64, 424, "≈10,000 DEMAND PACKAGES / WEEK · PLAINTIFF-SIDE AI", 8, CU_DARK, weight=500))
    return "\n".join(c), "Industrialized", "PL-10"


def icon_tld(pid, w, h):
    c = [doc(56, 72, 104, 140, WHITE, INK, [0.7, 0.85, 0.6, 0.8, 0.5, 0.75, 0.6, 0.7, 0.5, 0.6, 0.7, 0.5], hl={3})]
    # square clock
    cx, cy = 200, 150
    c.append(r(cx - 40, cy - 40, 80, 80, CU_TINT, CU, 1.25))
    for k in range(12):
        a = k * 30
        # ticks on square perimeter at 12 positions
        pos = {0: (0, -1), 90: (1, 0), 180: (0, 1), 270: (-1, 0)}
    for (dx, dy) in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        c.append(ln(cx + dx * 40, cy + dy * 40, cx + dx * 32, cy + dy * 32, CU, 1.5))
    for (dx, dy) in [(-0.5, -1), (0.5, -1), (1, -0.5), (1, 0.5), (0.5, 1), (-0.5, 1), (-1, 0.5), (-1, -0.5)]:
        x1, y1 = cx + dx * 40, cy + dy * 40
        x2, y2 = cx + dx * 40 * (0.9 if abs(dx) == 1 else 1), cy + dy * 40 * (0.9 if abs(dy) == 1 else 1)
        c.append(ln(x1, y1, x2, y2, CU, 1))
    c.append(path(f"M{cx} {cy - 26} V{cy} H{cx + 20}", CU_DARK, 2))
    c.append(sq(cx, cy, 5, CU_DARK))
    # calendar
    gx, gy = 168, 216
    c.append(r(gx, gy, 96, 56, VG_TINT, VG, 1.25))
    for i in range(1, 6):
        c.append(ln(gx + i * 16, gy, gx + i * 16, gy + 56, VG_LIGHT, 0.75))
    for j in range(1, 3):
        c.append(ln(gx, gy + j * 18.67, gx + 96, gy + j * 18.67, VG_LIGHT, 0.75))
    c.append(r(gx + 64, gy + 18.67, 16, 18.67, VG, "none", 0))
    return "\n".join(c), "Time-limited demand", "AC-01"


def icon_badfaith(pid, w, h):
    c = []
    c.append(doc(80, 88, 96, 128, WHITE, MUTED, sw=0.75))
    c.append(doc(64, 72, 96, 128, WHITE, INK, [0.7, 0.85, 0.6, 0.8, 0.5, 0.75, 0.6, 0.7, 0.5, 0.6], hl={2, 3}))
    c.append(r(148, 60, 24, 24, CU, "none", 0))
    c.append(t(160, 76, "!", 14, WHITE, "middle", 700, 0, SANS))
    # viewfinder
    vx, vy, vs = 168, 144, 100
    for (x, y, dx, dy) in [(vx, vy, 1, 1), (vx + vs, vy, -1, 1), (vx, vy + vs, 1, -1), (vx + vs, vy + vs, -1, -1)]:
        c.append(path(f"M{x} {y + dy*18} V{y} H{x + dx*18}", VG, 2))
    c.append(r(vx + 22, vy + 22, vs - 44, vs - 44, VG_TINT, VG, 1))
    c.append(ln(vx + 22, vy + vs / 2, vx + vs - 22, vy + vs / 2, VG, 1.5))
    c.append(t(vx, vy + vs + 20, "AUDIT OPEN", 8, VG_DEEP, weight=600))
    return "\n".join(c), "Bad-faith allegation", "AC-02"


def icon_crn(pid, w, h):
    c = [doc(56, 64, 92, 120, WHITE, INK, [0.7, 0.85, 0.6, 0.8, 0.5, 0.75, 0.6, 0.7, 0.5])]
    c.append(r(104, 128, 64, 32, CU_TINT, CU, 1.25))
    c.append(t(136, 149, "CRN", 12, CU_DARK, "middle", 600, 1, SANS))
    x0, x1, y = 56, 264, 232
    c.append(ln(x0, y, x1, y, INK, 1))
    for i in range(13):
        x = x0 + i * (x1 - x0) / 12
        c.append(ln(x, y, x, y - (8 if i % 6 == 0 else 4), INK, 0.75))
    c.append(r(x0, y + 8, x1 - x0, 14, VG_MIST, VG, 1))
    c.append(r(x0, y + 8, (x1 - x0) * 0.25, 14, VG, "none", 0))
    c.append(t(x0, y + 40, "CURE PERIOD · 60d", 8, INK, weight=500))
    c.append(t(x1, y + 40, "DOI", 8, VG_DEEP, "end", weight=600))
    c.append(path(f"M{x1 - 14} 120 L{x1 - 8} 126 L{x1 + 4} 112", VG, 2))
    c.append(r(x1 - 22, 104, 32, 32, "none", VG, 1.25))
    return "\n".join(c), "Florida CRN", "AC-03"


def icon_attorney(pid, w, h):
    c = []
    c.append(r(48, 80, 72, 72, WHITE, INK, 1.25))
    c.append(person(84, 92, 48, INK, SECTION, 1.25))
    c.append(t(48, 172, "CLAIMANT", 8, INK, weight=500))
    c.append(r(200, 80, 72, 72, CU_TINT, CU, 1.25))
    c.append(person(236, 92, 48, CU, WHITE, 1.25))
    c.append(r(229, 128, 14, 8, CU, "none", 0))
    c.append(t(200, 172, "COUNSEL", 8, CU_DARK, weight=600))
    c.append(jn([(120, 116), (200, 116)], CU, 1.5, junctions=False))
    c.append(sq(160, 116, 8, CU))
    c.append(ln(236, 180, 236, 216, VG, 1.5))
    c.append(r(172, 216, 128, 44, VG_TINT, VG, 1.25))
    c.append(t(186, 236, "EARLY CONTACT", 8, VG_DARK, weight=600))
    c.append(t(186, 250, "EVAL BEFORE SUIT", 8, VG_DEEP))
    return "\n".join(c), "Attorney representation", "AC-04"


def plate_pipeline(pid, w, h):
    c = []
    y = 200
    # inbox
    for i in range(3, -1, -1):
        c.append(doc(72 + i * 6, 120 + i * 8, 84, 112, WHITE, INK, [0.7, 0.8, 0.6, 0.75, 0.5, 0.7, 0.6, 0.5, 0.6, 0.7]))
    c.append(t(72, 112, "01 · INBOUND", 9, INK, weight=600))
    c.append(jn([(180, y), (260, y)], INK, 1, junctions=False)); c.append(path(f"M252 {y-5} L260 {y} L252 {y+5}", INK, 1))
    # scan plane
    c.append(r(272, 112, 40, 176, SECTION, INK, 1))
    for i in range(10):
        c.append(r(280, 120 + i * 16.5, 24, 11, CU_TINT if i == 6 else WHITE, MUTED, 0.75))
    c.append(ln(292, 100, 292, 300, VG, 1.5))
    c.append(t(272, 100, "02 · SCAN", 9, INK, weight=600))
    c.append(jn([(312, y), (392, y)], INK, 1, junctions=False)); c.append(path(f"M384 {y-5} L392 {y} L384 {y+5}", INK, 1))
    # graph
    gx = 404
    c.append(r(gx, 112, 248, 176, f"url(#{pid}-dots)", MUTED, 0.75))
    cx, cy = gx + 104, 188
    spokes = [(gx + 24, cy, "e"), (gx + 184, cy, "s"), (cx, 128, "e"), (cx, 248, "s")]
    c.append(ln(gx + 64, cy + 12, cx, cy + 12, INK, 1))
    c.append(ln(cx + 40, cy + 12, gx + 184, cy + 12, CU, 1.25))
    c.append(ln(cx + 20, 152, cx + 20, cy, INK, 1))
    c.append(ln(cx + 20, cy + 24, cx + 20, 248, CU, 1.25))
    c.append(r(cx, cy, 40, 24, WHITE, INK, 1.5))
    for x, yy, k in spokes:
        c.append(r(x, yy, 40, 24, CU_TINT if k == "s" else WHITE, CU if k == "s" else INK, 1.25 if k == "s" else 1))
    c.append(t(gx, 100, "03 · CLAIM GRAPH", 9, INK, weight=600))
    c.append(jn([(652, y), (732, y)], INK, 1, junctions=False)); c.append(path(f"M724 {y-5} L732 {y} L724 {y+5}", INK, 1))
    # signals
    sx = 744
    c.append(t(sx, 100, "04 · SIGNALS", 9, CU_DARK, weight=600))
    for i, lab in enumerate(["TLD · p.4", "REPTILE · p.7", "SPOLIATION · p.9"]):
        yy = 120 + i * 56
        c.append(r(sx, yy, 168, 40, CU_TINT, CU, 1.25))
        c.append(sq(sx + 16, yy + 20, 8, CU))
        c.append(t(sx + 30, yy + 24, lab, 9, CU_DARK, weight=500))
    c.append(jn([(912, y), (992, y)], INK, 1, junctions=False)); c.append(path(f"M984 {y-5} L992 {y} L984 {y+5}", INK, 1))
    # actions
    ax = 1004
    c.append(t(ax, 100, "05 · ACTIONS", 9, VG_DEEP, weight=600))
    for i, lab in enumerate(["ACKNOWLEDGE", "CALENDAR DEADLINE", "RESERVE REVIEW"]):
        yy = 120 + i * 56
        c.append(r(ax, yy, 168, 40, VG_TINT, VG, 1.25))
        c.append(path(f"M{ax+12} {yy+20} L{ax+17} {yy+25} L{ax+26} {yy+15}", VG_DEEP, 1.5))
        c.append(t(ax + 34, yy + 24, lab, 9, VG_DARK, weight=500))
    c.append(jn([(1172, y), (1252, y)], INK, 1, junctions=False)); c.append(path(f"M1244 {y-5} L1252 {y} L1244 {y+5}", INK, 1))
    # authorize gate + SoR
    c.append(r(1264, 112, 104, 176, WHITE, INK, 1.25))
    for i in range(6):
        c.append(ln(1276, 136 + i * 22, 1356, 136 + i * 22, HAIR, 1))
    c.append(r(1276, 224, 80, 22, VG_MIST, VG, 1))
    c.append(t(1264, 100, "06 · RECORD", 9, INK, weight=600))
    c.append(t(1264, 308, "PERSON AUTHORIZES", 8, MUTED))
    c.append(t(1264, 320, "EVERY STATE CHANGE", 8, MUTED))
    # dimension band
    c.append(path(f"M72 336 V344 H652 V336", MUTED, 1)); c.append(t(362, 360, "ISOMER CORE · READ IN FULL AGAINST THE INSURANCE ONTOLOGY", 8, MUTED, "middle"))
    c.append(path(f"M744 336 V344 H1172 V336", MUTED, 1)); c.append(t(958, 360, "SIGNALS™ → ACTIONS™", 8, MUTED, "middle"))
    return "\n".join(c), "Receipt to record", "PL-11"




# ================= more plates =================

def arrow_r(x, y, c=INK, sw=1):
    return path(f"M{x-7} {y-5} L{x} {y} L{x-7} {y+5}", c, sw)


def arrow_d(x, y, c=INK, sw=1):
    return path(f"M{x-5} {y-7} L{x} {y} L{x+5} {y-7}", c, sw)


def bracket_h(x1, x2, y, c=MUTED, down=True):
    d = 6 if down else -6
    return path(f"M{x1} {y} V{y+d} H{x2} V{y}", c, 1)


def box(x, y, w, h, kind="e", title="", sub=""):
    fill, stroke, tc, sc, sw = WHITE, INK, INK, MUTED, 1
    if kind == "s": fill, stroke, tc, sc, sw = CU_TINT, CU, CU_DARK, CU_DEEP, 1.25
    if kind == "a": fill, stroke, tc, sc, sw = VG_TINT, VG, VG_DARK, VG_DEEP, 1.25
    if kind == "g": fill = SECTION
    o = [r(x, y, w, h, fill, stroke, sw)]
    if title: o.append(t(x + 10, y + 19, title, 9, tc, weight=600, ls=1))
    if sub: o.append(t(x + 10, y + 33, sub, 8, sc))
    return "\n".join(o)


# ================= STORY · pitch-patina =================

def st_lawyer(pid, w, h):
    c = []
    x0, x1 = 120, 664
    k = (x1 - x0) / 600
    X = lambda d: round(x0 + d * k, 1)
    for d in range(0, 601, 50):
        major = d % 100 == 0
        c.append(ln(X(d), 96, X(d), 352, HAIR if major else "none", 1))
    c.append(t(x0, 92, "FIRST NOTICE → LAWSUIT · DAYS", 8, MUTED))
    c.append(t(x0 - 12, 150, "2016", 9, INK, "end", 500))
    c.append(r(X(0), 132, X(550) - X(0), 28, WHITE, INK, 1))
    c.append(t(X(550) + 8, 150, "≈550", 9, INK, weight=500))
    c.append(t(x0 - 12, 222, "NOW", 9, CU_DARK, "end", 600))
    c.append(r(X(0), 204, X(120) - X(0), 28, CU_TINT, CU, 1.25))
    c.append(t(X(120) + 8, 222, "≈120", 9, CU_DARK, weight=600))
    c.append(path(f"M{X(120)} 240 V256 H{X(550)} V168", MUTED, 1, extra='stroke-dasharray="3 3"'))
    c.append(sq(X(120), 256, 5, MUTED)); c.append(sq(X(550), 256, 5, MUTED))
    c.append(t((X(120) + X(550)) / 2, 276, "−78%", 14, CU_DARK, "middle", 600, 0.2, SANS))
    c.append(t(x0 - 12, 316, "d14", 9, CU_DARK, "end", 600))
    c.append(r(X(0), 306, X(14) - X(0), 14, CU, "none", 0))
    c.append(t(X(14) + 10, 317, "70% OF GL INJURY CLAIMS HAVE COUNSEL BY DAY 14", 8, CU_DARK, weight=500))
    c.append(ln(x0, 352, x1, 352, INK, 1))
    for d in range(0, 601, 10):
        hh = 8 if d % 100 == 0 else (5 if d % 50 == 0 else 2.5)
        c.append(ln(X(d), 352, X(d), 352 + hh, INK, 0.75))
        if d % 100 == 0:
            c.append(t(X(d), 374, f"d{d}", 8, MUTED, "middle"))
    return "\n".join(c), "Counsel before the call", "ST-01"


def st_buried(pid, w, h):
    c = []
    # email
    c.append(r(72, 120, 160, 120, WHITE, INK, 1))
    c.append(r(72, 120, 160, 22, SECTION, INK, 1))
    c.append(t(82, 135, "INBOUND · 1 OF 214", 8, INK, weight=500))
    for i, f in enumerate([0.8, 0.6, 0.7, 0.4]):
        c.append(r(82, 156 + i * 10, 140 * f, 2.5, "#C9C9CC", "none", 0))
    for i in range(3):
        c.append(r(82 + i * 46, 206, 40, 22, CU_TINT if i == 2 else SECTION, CU if i == 2 else MUTED, 1 if i == 2 else 0.75))
        c.append(t(102 + i * 46, 221, f"A{i+1}", 8, CU_DARK if i == 2 else MUTED, "middle", 600 if i == 2 else 400))
    # attachments row
    xs = [296, 400, 504]
    for i, x in enumerate(xs):
        k = "s" if i == 2 else "e"
        c.append(doc(x, 96, 80, 104, CU_TINT if i == 2 else WHITE, CU if i == 2 else INK, hl={4} if i == 2 else None, hlc=CU))
        c.append(t(x, 216, f"ATT-{i+1} · {['3 pp','11 pp','9 pp'][i]}", 8, CU_DARK if i == 2 else MUTED, weight=600 if i == 2 else 400))
    c.append(ln(232, 148, 296, 148, INK, 1))
    c.append(jn([(376, 148), (400, 148)], INK, 1, junctions=False))
    c.append(jn([(480, 148), (504, 148)], INK, 1, junctions=False))
    # zoom callout
    zx, zy, zw, zh = 296, 268, 360, 136
    c.append(r(504 + 8, 96 + 18 + 4 * 9 - 3, 64, 9, "none", CU, 1))
    c.append(ln(544, 159, 544, zy, CU, 1))
    c.append(r(zx, zy, zw, zh, WHITE, CU, 1.25))
    c.append(t(zx + 12, zy + 20, "ATT-3 · p.6 · ¶4", 8, CU_DEEP, weight=500))
    for i, f in enumerate([0.9, 0.75, 0.85, 0.6, 0.8]):
        col = CU if i == 2 else "#C9C9CC"
        c.append(r(zx + 12, zy + 36 + i * 16, (zw - 24) * f, 5 if i == 2 else 3, col, "none", 0))
    c.append(t(zx + 12, zy + zh - 12, "DEADLINE · FOUND IN PILOT", 9, CU_DARK, weight=600))
    # scan line
    c.append(ln(56, 252, 280, 252, VG, 1.5))
    c.append(sq(56, 252, 6, VG))
    c.append(t(56, 276, "READ IN FULL ·", 8, VG_DEEP, weight=600))
    c.append(t(56, 288, "EVERY ATTACHMENT", 8, VG_DEEP, weight=600))
    return "\n".join(c), "The buried deadline", "ST-02"


def st_concentration(pid, w, h):
    c = []
    top, H = 96, 300
    ax, bx, cw = 96, 304, 80
    cut_a = top + 0.30 * H
    cut_b = top + 0.70 * H
    c.append(t(ax, 84, "CLAIMS", 9, INK, weight=600))
    c.append(t(bx, 84, "LOSS", 9, INK, weight=600))
    # band connecting copper portions
    c.append(f'<path d="M{ax+cw} {top} H{bx} V{cut_b} H{ax+cw+64} V{cut_a} H{ax+cw} Z" fill="{CU_TINT}" stroke="none" opacity="0.7"/>')
    c.append(f'<path d="M{ax+cw} {top} H{bx} V{cut_b} H{ax+cw+64} V{cut_a} H{ax+cw} Z" fill="url(#{pid}-hatch)" stroke="none" opacity="0.35"/>')
    c.append(path(f"M{ax+cw} {cut_a} H{ax+cw+64} V{cut_b} H{bx}", CU, 1))
    for x, cut in ((ax, cut_a), (bx, cut_b)):
        c.append(r(x, top, cw, cut - top, CU_TINT, CU, 1.25))
        c.append(r(x, cut, cw, top + H - cut, WHITE, INK, 1))
    c.append(t(ax + 10, top + 20, "30%", 13, CU_DARK, weight=600, ls=0.2, family=SANS))
    c.append(t(ax + 10, top + 34, "ATTORNEY", 8, CU_DEEP))
    c.append(t(ax + 10, cut_a + 20, "70%", 13, INK, weight=600, ls=0.2, family=SANS))
    c.append(t(bx + 10, top + 20, "70%", 13, CU_DARK, weight=600, ls=0.2, family=SANS))
    c.append(t(bx + 10, cut_b + 20, "30%", 13, INK, weight=600, ls=0.2, family=SANS))
    c.append(t(ax, top + H + 20, "COMMERCIAL AUTO", 8, MUTED))
    # table
    tx = 440
    rows = [("GL", "LITIGATED INJURY", "14× COST"), ("WC", "ATTORNEY CLAIM", "$78K vs $16K"),
            ("LIAB.", "3% LITIGATED", "50%+ OF PAID"), ("GL", "COUNSEL ≤ 24h", "71% OF LITIGATED")]
    c.append(ln(tx, top, 664, top, INK, 1))
    for i, (a, b, v) in enumerate(rows):
        y = top + 24 + i * 44
        c.append(t(tx, y, a, 8, MUTED))
        c.append(t(tx + 40, y, b, 8, INK, weight=500))
        c.append(t(664, y, v, 9, CU_DARK, "end", 600))
        c.append(ln(tx, y + 18, 664, y + 18, HAIR, 1))
    c.append(t(tx, top + H + 20, "SAME PATTERN, EVERY BOOK", 8, MUTED))
    return "\n".join(c), "Where the loss is", "ST-03"


def st_window(pid, w, h):
    c = []
    z0, z1, z2, z3 = 168, 312, 512, 664
    for (y, lab, ratio, plan) in [(112, "TODAY", "50% IN TIME", (0, 5, 5)), (288, "WITH ISOMER", "70% IN TIME", (7, 0, 3))]:
        c.append(t(72, y + 4, lab, 9, INK, weight=600))
        c.append(t(72, y + 18, ratio, 8, VG_DEEP if plan[0] else MUTED, weight=500))
        c.append(r(z0, y - 24, z1 - z0, 96, VG_TINT, "none", 0))
        c.append(r(z2, y - 24, z3 - z2, 96, f"url(#{pid}-hatch)", "none", 0, 'opacity="0.25"'))
        c.append(ln(z0, y + 72, z3, y + 72, INK, 1))
        for zx in (z0, z1, z2, z3):
            c.append(ln(zx, y - 24, zx, y + 78, MUTED if zx in (z1, z2) else INK, 0.75, 'stroke-dasharray="3 3"' if zx in (z1, z2) else ""))
        n_arr, n_after, n_late = plan
        def place(n, xa, xb, fill, stroke):
            o = []
            for i in range(n):
                col, row = i % 5, i // 5
                cx = xa + 20 + col * 22; cy = y + 8 + row * 24
                o.append(r(cx, cy, 14, 14, fill, stroke, 1.25))
            return "\n".join(o)
        c.append(place(n_arr, z0, z1, VG, VG_DARK))
        c.append(place(n_after, z1 + 30, z2, WHITE, INK))
        c.append(place(n_late, z2, z3, CU_TINT, CU))
    for (xa, xb, lab, col) in [(z0, z1, "FLAGGED ON ARRIVAL", VG_DEEP), (z1, z2, "FLAGGED AFTER ENTRY", INK), (z2, z3, "TOO LATE", CU_DARK)]:
        c.append(t(xa + 8, 72, lab, 8, col, weight=600))
    c.append(t(z1, 420, "CLAIMS SYSTEM ENTRY · MULTI-DAY LAG", 8, MUTED, "middle"))
    c.append(t(72, 420, "10 HIGH-RISK CLAIMS", 8, MUTED))
    return "\n".join(c), "Window to act", "ST-04"


def st_point(pid, w, h):
    c = []
    x0, x1 = 96, 624
    k = (x1 - x0) / 10
    X = lambda m: round(x0 + m * k, 1)
    c.append(t(x0, 92, "$1B COMMERCIAL BOOK · ONE YEAR OF CLAIMS · SAVINGS $M", 8, MUTED))
    c.append(r(X(0), 132, X(3.9) - X(0), 56, VG_MIST, VG, 1.25))
    c.append(r(X(3.9), 132, X(10) - X(3.9), 56, VG, VG_DARK, 1.25))
    c.append(t(X(0) + 10, 156, "DEFENSE COST", 8, VG_DARK, weight=600))
    c.append(t(X(0) + 10, 176, "$3.9M", 13, VG_DARK, weight=600, ls=0.2, family=SANS))
    c.append(t(X(3.9) + 10, 156, "SETTLEMENTS", 8, WHITE, weight=600))
    c.append(t(X(3.9) + 10, 176, "$6.1M", 13, WHITE, weight=600, ls=0.2, family=SANS))
    c.append(ln(x0, 216, x1, 216, INK, 1))
    for m in range(11):
        c.append(ln(X(m), 216, X(m), 216 + (8 if m % 5 == 0 else 4), INK, 0.75))
        c.append(t(X(m), 238, str(m), 8, MUTED, "middle"))
    c.append(bracket_h(X(0), X(10), 108, INK, down=True))
    c.append(t(X(10), 100, "$10.0M = 1 POINT OF COMBINED RATIO", 9, INK, "end", 600))
    # assumptions
    c.append(t(x0, 292, "WHEN A CLAIM IS CAUGHT IN TIME", 8, MUTED))
    cells = [("20%", "AVOID SUIT"), ("15%", "LOWER DEFENSE COST"), ("7.5%", "LOWER SETTLEMENT")]
    cw = (x1 - x0) / 3
    for i, (v, lab) in enumerate(cells):
        x = x0 + i * cw
        c.append(r(x, 304, cw, 72, WHITE, INK, 1))
        c.append(t(x + 12, 336, v, 18, VG_DEEP, weight=600, ls=0.2, family=SANS))
        c.append(t(x + 12, 360, lab, 8, INK, weight=500))
    c.append(t(x0, 404, "ILLUSTRATIVE · REPLACED BY YOUR ACTUALS IN THE ASSESSMENT", 8, MUTED))
    return "\n".join(c), "One point", "ST-05"


def st_paths(pid, w, h):
    c = []
    cols = [(232, 352, "WEEKS"), (352, 488, "MONTHS"), (488, 664, "YEARS")]
    for (a, b, lab) in cols:
        c.append(r(a, 96, b - a, 280, SECTION if lab == "MONTHS" else "none", HAIR, 1))
        c.append(t(a + 8, 88, lab, 8, MUTED))
    rows = [(140, "GROW THE BOOK", "+12% PREMIUM · CAPITAL"),
            (230, "CUT CLAIMS STAFF", "≈80 ADJUSTERS"),
            (320, "CATCH RISK IN TIME", "50% → 70% IN TIME")]
    for y, a, b in rows:
        c.append(t(72, y - 2, a, 9, INK if "CATCH" not in a else VG_DARK, weight=600))
        c.append(t(72, y + 12, b, 8, MUTED))
    # grow
    c.append(r(400, 124, 264, 28, WHITE, INK, 1))
    c.append(t(408, 142, "NEW BUSINESS SEASONS", 8, INK))
    # cut
    c.append(r(352, 214, 136, 28, WHITE, INK, 1))
    c.append(t(360, 232, "EXECUTE", 8, INK))
    c.append(r(488, 214, 176, 28, CU_TINT, CU, 1.25))
    c.append(r(488, 214, 176, 28, f"url(#{pid}-hatch)", "none", 0, 'opacity="0.4"'))
    c.append(t(496, 232, "REBUILD · LEAKAGE", 8, CU_DARK, weight=600))
    # catch
    c.append(r(240, 304, 56, 28, VG, VG_DARK, 1.25))
    c.append(t(246, 322, "4 WK", 8, WHITE, weight=600))
    c.append(r(296, 304, 248, 28, VG_MIST, VG, 1.25))
    c.append(t(304, 322, "SAVINGS WITHIN A YEAR", 8, VG_DARK, weight=600))
    c.append(t(72, 412, "SAME BOOK · SAME TEAM · NOTHING TO UNWIND", 8, VG_DEEP, weight=500))
    return "\n".join(c), "Three paths to one point", "ST-06"


def st_funding(pid, w, h):
    c = []
    X0, Y0, W, H = 72, 88, 456, 288
    tot = 775.0
    cells = []
    w1 = W * 385 / tot
    cells.append(("EVENUP", 385, X0, Y0, w1, H, True))
    rx, rw = X0 + w1, W - w1
    h2 = H * 164 / 390
    cells.append(("EVE", 164, rx, Y0, rw, h2, True))
    ry, rh = Y0 + h2, H - h2
    w3 = rw * 91 / 226
    cells.append(("SUPIO", 91, rx, ry, w3, rh, False))
    rx2, rw2 = rx + w3, rw - w3
    h4 = rh * 60 / 135
    cells.append(("DARROW", 60, rx2, ry, rw2, h4, False))
    ry2, rh2 = ry + h4, rh - h4
    w5 = rw2 * 55 / 75
    cells.append(("JUSTPOINT", 55, rx2, ry2, w5, rh2, False))
    cells.append(("FINCH", 20, rx2 + w5, ry2, rw2 - w5, rh2, False))
    for i, (name, v, x, y, cw, ch, uni) in enumerate(cells):
        c.append(r(round(x, 1), round(y, 1), round(cw, 1), round(ch, 1), CU_TINT, CU, 1.25))
        if uni:
            c.append(r(round(x, 1), round(y, 1), round(cw, 1), round(ch, 1), f"url(#{pid}-hatch)", "none", 0, 'opacity="0.3"'))
        c.append(t(round(x + 8, 1), round(y + 16, 1), f"{i+1:02d}", 8, CU_DARK, weight=600))
    lx = 552
    c.append(t(lx, 96, "$M RAISED", 8, MUTED))
    for i, (name, v, *_r) in enumerate(cells):
        y = 120 + i * 24
        c.append(t(lx, y, f"{i+1:02d}", 8, CU_DARK, weight=600))
        c.append(t(lx + 20, y, name, 8, INK, weight=500))
        c.append(t(664, y, str(v), 8, CU_DARK, "end", 600))
    c.append(ln(lx, 266, 664, 266, INK, 1))
    c.append(t(lx, 284, "TOTAL", 8, INK, weight=600)); c.append(t(664, 284, "775+", 9, CU_DARK, "end", 600))
    c.append(r(lx, 300, 10, 10, f"url(#{pid}-hatch)", CU, 1)); c.append(t(lx + 16, 309, "UNICORN", 8, MUTED))
    # 71% bar
    c.append(t(X0, 404, "DISCLOSED LITIGATION-AI FUNDING", 8, MUTED))
    for i in range(50):
        c.append(r(X0 + i * 9.12, 412, 7, 14, CU if i < 35.5 else WHITE, CU if i < 35.5 else MUTED, 0.75))
    c.append(t(X0 + W + 16, 424, "71% PLAINTIFF SIDE", 8, CU_DARK, weight=600))
    return "\n".join(c), "Who is building plaintiff AI", "ST-07"


def st_thirty(pid, w, h):
    c = []
    x0, x1 = 120, 664
    L = math.log10(43200)
    X = lambda m: round(x0 + math.log10(max(m, 1)) / L * (x1 - x0), 1)
    ticks = [(1, "1m"), (10, "10m"), (30, "30m"), (60, "1h"), (360, "6h"), (1440, "1d"), (4320, "3d"), (10080, "7d"), (43200, "30d")]
    for m, lab in ticks:
        c.append(ln(X(m), 96, X(m), 336, HAIR, 1))
    c.append(t(x0, 88, "TIME FROM ARRIVAL · LOG SCALE", 8, MUTED))
    c.append(t(x0 - 12, 156, "ISOMER", 9, VG_DARK, "end", 600))
    c.append(r(X(1), 140, X(30) - X(1), 24, VG, VG_DARK, 1.25))
    c.append(sq(X(30), 152, 8, VG_DARK))
    c.append(t(X(30) + 10, 148, "HANDLER HAS DEADLINE", 8, VG_DARK, weight=600))
    c.append(t(X(30) + 10, 160, "+ SEVERITY", 8, VG_DARK, weight=600))
    c.append(t(x0 - 12, 236, "TODAY", 9, INK, "end", 600))
    c.append(r(X(1), 220, X(1440) - X(1), 24, WHITE, INK, 1))
    c.append(r(X(1440), 220, X(4320) - X(1440), 24, SECTION, INK, 1))
    c.append(r(X(1440), 220, X(4320) - X(1440), 24, f"url(#{pid}-micro)", "none", 0, 'opacity="0.35"'))
    c.append(t(X(1) + 8, 236, "WAITING FOR ENTRY", 8, INK))
    c.append(sq(X(4320), 232, 8, INK))
    c.append(t(X(4320) + 10, 230, "CMS ENTRY", 8, INK, weight=600))
    c.append(t(X(4320) + 10, 242, "RULES FIRE", 8, MUTED))
    c.append(ln(X(1), 104, X(1), 336, VG, 1.5)); c.append(sq(X(1), 104, 6, VG))
    c.append(t(X(1) + 8, 108, "t₀ · ARRIVES", 8, VG_DEEP, weight=600))
    c.append(ln(x0, 336, x1, 336, INK, 1))
    for m, lab in ticks:
        c.append(ln(X(m), 336, X(m), 344, INK, 0.75))
        c.append(t(X(m), 360, lab, 8, MUTED, "middle"))
    c.append(path(f"M{X(30)} 280 V288 H{X(4320)} V280", MUTED, 1))
    c.append(t((X(30) + X(4320)) / 2, 306, "HEAD START · DAYS", 9, INK, "middle", 600))
    return "\n".join(c), "To the handler in 30 minutes", "ST-08"


def st_assessment(pid, w, h):
    c = []
    gx0, gx1 = 264, 664
    cw = (gx1 - gx0) / 4
    for i in range(4):
        x = gx0 + i * cw
        c.append(r(x, 104, cw, 272, SECTION if i % 2 else "none", HAIR, 1))
        c.append(t(x + 8, 96, f"WEEK {i+1}", 8, INK, weight=600))
    ins = ["READ-ONLY ACCESS", "LOSS RUNS", "ADJUSTER HOURS"]
    for i, s in enumerate(ins):
        y = 128 + i * 56
        c.append(r(72, y, 144, 32, WHITE, INK, 1))
        c.append(t(82, y + 20, s, 8, INK, weight=500))
    c.append(path("M224 128 H232 V272 H224", MUTED, 1))
    c.append(ln(232, 200, gx0 - 2, 200, INK, 1)); c.append(arrow_r(gx0 - 2, 200))
    c.append(t(72, 96, "INPUTS", 8, MUTED))
    rows = [("FLAGS ON LIVE CLAIMS", 0, 4, "a"), ("CAUGHT-IN-TIME BASELINE", 1, 4, "e"),
            ("RESERVE LAG BY CLAIM", 2, 4, "e"), ("BUSINESS CASE · $ AND POINTS", 3, 4, "s")]
    for i, (lab, a, b, k) in enumerate(rows):
        y = 124 + i * 60
        x = gx0 + a * cw + 6
        ww = (b - a) * cw - 12
        fill, stroke = {"a": (VG_TINT, VG), "e": (WHITE, INK), "s": (VG, VG_DARK)}[k]
        c.append(r(x, y, ww, 32, fill, stroke, 1.25 if k != "e" else 1))
        c.append(t(x + 10, y + 20, lab, 8, WHITE if k == "s" else (VG_DARK if k == "a" else INK), weight=600))
    c.append(t(gx0, 404, "ACTUALS REPLACE ASSUMPTIONS · FROM WEEK ONE", 8, VG_DEEP, weight=500))
    return "\n".join(c), "The 4-week assessment", "ST-09"


def st_pricing(pid, w, h):
    c = []
    base, top = 376, 96
    k = (base - top) / 1000
    Y = lambda v: round(base - v * k, 1)
    for v in (0, 250, 500, 750, 1000):
        c.append(ln(96, Y(v), 440, Y(v), HAIR, 1))
        c.append(t(88, Y(v) + 3, f"{v}K" if v < 1000 else "$1M", 8, MUTED, "end"))
    steps = [("ASSESS", 100, "4 WK"), ("SIGN", 100, "20% − CREDIT"), ("PRODUCTION", 200, "20%"), ("YEAR-END", 600, "60% · IF YOU STAY")]
    cum = 0
    bw = 64
    for i, (lab, v, sub) in enumerate(steps):
        x = 112 + i * 80
        dashed = 'stroke-dasharray="4 3"' if lab == "YEAR-END" else ""
        c.append(r(x, Y(cum + v), bw, round(v * k, 1), WHITE if lab != "YEAR-END" else VG_TINT, INK if lab != "YEAR-END" else VG, 1, dashed))
        if i < len(steps) - 1:
            c.append(ln(x + bw, Y(cum + v), x + 80, Y(cum + v), MUTED, 0.75, 'stroke-dasharray="2 2"'))
        cum += v
        c.append(t(x, base + 18, lab, 8, INK, weight=600))
        c.append(t(x, base + 30, sub, 7, MUTED, ls=0.4))
        c.append(t(x + bw / 2, Y(cum) - 6, f"{v}K", 8, INK, "middle", 500))
    c.append(ln(96, base, 440, base, INK, 1))
    # 10x panel
    px = 504
    c.append(t(px, 96, "$10M TARGETED SAVINGS", 8, VG_DEEP, weight=600))
    for i in range(10):
        y = 112 + i * 26
        fee = i == 9
        c.append(r(px, y, 160, 22, WHITE if fee else VG_MIST, INK if fee else VG, 1))
        c.append(t(px + 8, y + 15, "FEE $1M" if fee else f"${i+1}M", 8, INK if fee else VG_DARK, weight=500))
    c.append(path(f"M676 112 H684 V{112+9*26+22} H676", VG, 1))
    c.append(t(px, 404, "10× · 30 DAYS NOTICE, ANYTIME", 8, VG_DEEP, weight=600))
    return "\n".join(c), "Priced at 10% of target", "ST-10"


# ================= BLOG covers =================

def bl_sovereign(pid, w, h):
    c = []
    c.append(r(120, 104, 720, 352, f"url(#{pid}-dots)", INK, 1.25, 'stroke-dasharray="8 4"'))
    c.append(r(120, 104, 220, 22, INK, "none", 0))
    c.append(t(130, 119, "INSURER · AZURE TENANT", 9, WHITE, weight=600))
    for i in range(3, -1, -1):
        c.append(doc(176 + i * 8, 200 + i * 10, 92, 120, WHITE, INK))
    c.append(t(176, 192, "CLAIM DATA", 8, INK, weight=600))
    c.append(jn([(300, 270), (392, 270)], INK, 1, junctions=False)); c.append(arrow_r(392, 270))
    c.append(r(400, 196, 176, 148, WHITE, INK, 1.5))
    c.append(r(408, 204, 160, 132, "none", INK, 0.75))
    for i in range(4):
        for j in range(3):
            c.append(r(424 + i * 36, 228 + j * 30, 20, 16, CU_TINT if (i, j) == (2, 1) else SECTION, CU if (i, j) == (2, 1) else MUTED, 0.75))
    c.append(t(400, 188, "ISOMER CORE", 8, INK, weight=600))
    c.append(jn([(576, 240), (640, 240)], CU, 1.25, junctions=False)); c.append(arrow_r(640, 240, CU, 1.25))
    c.append(box(648, 220, 144, 40, "s", "SIGNALS"))
    c.append(jn([(576, 300), (640, 300)], VG, 1.25, junctions=False)); c.append(arrow_r(640, 300, VG, 1.25))
    c.append(box(648, 280, 144, 40, "a", "ACTIONS"))
    c.append(t(120, 488, "DEPLOYED IN YOUR TENANT · YOUR KEYS · YOUR BOUNDARY", 9, INK, weight=500))
    c.append(t(840, 488, "AZURE MARKETPLACE", 8, MUTED, "end"))
    return "\n".join(c), "Sovereign claims AI", "BL-01"


def bl_pfnol(pid, w, h):
    c = []
    vals = [1, 1.1, 0.9, 1, 1.05, 0.95, 1, 1, 12, 10, 8, 6, 4.5, 3.2, 2.4, 1.8, 1.4, 1.2, 1.1, 1, 1]
    x0, x1, base, top = 120, 840, 424, 112
    k = (base - top) / 13
    bw = (x1 - x0) / len(vals)
    c.append(r(x0, base - 1.3 * k, x1 - x0, 1.3 * k, SECTION, "none", 0))
    c.append(t(x0 + 8, base - 1.3 * k - 8, "NORMAL WEEK · WHAT THE WORKFLOW IS SIZED FOR", 8, INK, weight=500))
    backlog, cap = 0, 1.3
    bl = []
    for i, v in enumerate(vals):
        x = x0 + i * bw + 3
        c.append(r(round(x, 1), round(base - v * k, 1), round(bw - 6, 1), round(v * k, 1), WHITE, INK, 0.75))
        if v > cap:
            c.append(r(round(x, 1), round(base - v * k, 1), round(bw - 6, 1), round((v - cap) * k, 1), f"url(#{pid}-hatch)", CU, 0.75))
        backlog = max(0, backlog + v - cap)
        bl.append(backlog)
    m = max(bl)
    d = f"M{x0} {base}"
    for i, b in enumerate(bl):
        y = round(base - b / m * (base - top - 20), 1)
        d += f" V{y} H{round(x0 + (i + 1) * bw, 1)}"
    c.append(path(d, CU, 1.5))
    c.append(t(x0 + 13 * bw, top + 4, "QUEUE DEPTH", 8, CU_DARK, weight=600))
    c.append(ln(x0, base, x1, base, INK, 1))
    for i in range(len(vals) + 1):
        c.append(ln(x0 + i * bw, base, x0 + i * bw, base + (8 if i % 7 == 0 else 4), INK, 0.75))
        if i % 7 == 0:
            c.append(t(x0 + i * bw, base + 22, f"d{i}", 8, MUTED, "middle"))
    lx = x0 + 8 * bw
    c.append(ln(lx, base, lx, top - 8, CU, 1, 'stroke-dasharray="4 3"'))
    c.append(t(lx - 6, top - 4, "LANDFALL", 8, CU_DARK, "end", 600))
    return "\n".join(c), "Do we need a PFNOL?", "BL-02"


def bl_narrative(pid, w, h):
    c = []
    lanes = ["EMAIL", "PORTAL", "PHONE NOTE", "LETTER · OCR"]
    frags = [(0, 220), (0, 470), (1, 300), (1, 560), (2, 260), (2, 410), (3, 360), (3, 620), (0, 680)]
    for i, lab in enumerate(lanes):
        y = 120 + i * 56
        c.append(t(72, y + 4, lab, 8, INK, weight=500))
        c.append(ln(184, y, 760, y, HAIR, 1))
    ty = 400
    c.append(ln(184, ty, 840, ty, INK, 1.25))
    c.append(t(184, ty + 40, "ONE CLAIM NARRATIVE · ORDERED · SOURCED", 9, VG_DEEP, weight=600))
    for i, (lane, x) in enumerate(sorted(frags, key=lambda f: f[1])):
        y = 120 + lane * 56
        flagged = (lane, x) == (2, 410)
        c.append(ln(x, y + 16, x, ty - 6, CU if flagged else MUTED, 1.25 if flagged else 0.75, "" if flagged else 'stroke-dasharray="3 3"'))
        c.append(r(x - 12, y - 16, 24, 32, CU_TINT if flagged else WHITE, CU if flagged else INK, 1.25 if flagged else 1))
        c.append(sq(x, ty, 10, CU if flagged else INK))
        c.append(t(x, ty + 20, f"{i+1:02d}", 8, CU_DARK if flagged else MUTED, "middle", 600 if flagged else 400))
    c.append(ln(176, ty - 40, 176, ty + 8, VG, 1.5)); c.append(sq(176, ty, 6, VG))
    return "\n".join(c), "Signals are real · 1H", "BL-03"


def bl_vendor(pid, w, h):
    c = []
    xs = [(120, "CARRIER"), (408, "VENDOR"), (696, "MODEL")]
    for i, (x, lab) in enumerate(xs):
        c.append(box(x, 200, 144, 48, "e", lab, ["POLICYHOLDER-FACING", "RUNS THE WORKFLOW", "MAKES THE CALL"][i]))
        for j in range(5):
            c.append(r(x, 272 + j * 14, 144, 10, WHITE if j % 2 else SECTION, HAIR, 0.75))
        c.append(t(x, 352, "AUDIT LOG", 7, MUTED))
        if i < 2:
            c.append(jn([(x + 144, 224), (xs[i + 1][0] - 4, 224)], INK, 1, junctions=False)); c.append(arrow_r(xs[i + 1][0] - 4, 224))
    c.append(r(120, 104, 720, 32, CU_TINT, CU, 1.25))
    c.append(t(130, 124, "EXAMINER · WRITTEN PROGRAM REVIEW", 9, CU_DARK, weight=600))
    for x, _ in xs:
        c.append(ln(x + 72, 136, x + 72, 200, CU, 1, 'stroke-dasharray="4 3"'))
    c.append(ln(194, 420, 768, 420, INK, 1.25))
    c.append(path("M202 414 L194 420 L202 426", INK, 1.25))
    c.append(sq(768, 420, 6, INK))
    c.append(t(194, 444, "ACCOUNTABILITY RETURNS TO THE CARRIER", 9, INK, weight=600))
    return "\n".join(c), "Your vendor's AI is yours", "BL-04"


def bl_two(pid, w, h):
    c = []
    c.append(doc(72, 216, 88, 116, WHITE, INK, hl={3}))
    c.append(t(72, 208, "SAME EMAIL", 8, INK, weight=600))
    c.append(ln(160, 274, 192, 274, INK, 1))
    c.append(path("M224 156 H192 V392 H224", INK, 1))
    c.append(sq(192, 274, 6, INK))
    lanes = [(156, "ADJUSTER A", ["READ", "DEADLINE SET", "TENDER IN WINDOW"], "a", "SETTLED"),
             (392, "ADJUSTER B", ["READ", "FILED", "DEADLINE PASSES"], "s", "SUIT FILED")]
    for y, name, steps, k, out in lanes:
        c.append(person(232, y - 48, 18, INK, WHITE, 1))
        c.append(t(248, y - 34, name, 8, INK, weight=600))
        x = 224
        for i, s in enumerate(steps):
            kk = "e" if i == 0 or (k == "s" and i == 1) else k
            c.append(box(x, y - 20, 136, 40, kk, s))
            c.append(jn([(x + 136, y), (x + 160, y)], VG if k == "a" else CU, 1, junctions=False))
            x += 160
        if k == "a":
            c.append(r(x, y - 24, 136, 48, VG, VG_DARK, 1.25))
            c.append(t(x + 10, y + 4, out, 10, WHITE, weight=600, ls=1))
        else:
            c.append(r(x, y - 24, 136, 48, RED_TINT, RED, 1.25))
            c.append(sq(x + 14, y, 6, RED))
            c.append(t(x + 24, y - 2, "CRITICAL", 8, RED_DEEP, weight=600))
            c.append(t(x + 24, y + 12, out, 9, RED_DEEP, weight=600, ls=1))
    c.append(ln(224, 476, 840, 476, INK, 1))
    for i in range(0, 31):
        c.append(ln(224 + i * 20.5, 476, 224 + i * 20.5, 476 + (8 if i % 5 == 0 else 4), INK, 0.75))
    c.append(t(224, 500, "DAYS FROM RECEIPT", 8, MUTED))
    return "\n".join(c), "Two adjusters, same email", "BL-05"


def bl_fnol(pid, w, h):
    c = []
    x0, x1, ay = 120, 840, 360
    k = (x1 - x0) / 30
    X = lambda d: round(x0 + (d + 12) * k, 1)
    c.append(r(X(-9), 136, X(0) - X(-9), 224, CU_TINT, "none", 0, 'opacity="0.6"'))
    c.append(r(X(-9), 136, X(0) - X(-9), 224, f"url(#{pid}-hatch)", "none", 0, 'opacity="0.35"'))
    c.append(t(X(-9) + 8, 156, "UNTRACKED · UNRESERVED", 8, CU_DARK, weight=600))
    for d in (-8, -6.5, -5, -3, -1.5):
        c.append(r(X(d) - 9, 260, 18, 24, WHITE, INK, 1))
        c.append(ln(X(d), 284, X(d), ay, MUTED, 0.75, 'stroke-dasharray="2 2"'))
    c.append(t(X(-8) - 9, 252, "LETTERS · EMAILS · PHOTOS", 8, INK, weight=500))
    c.append(ln(X(-9), 112, X(-9), ay + 12, VG, 1.5)); c.append(sq(X(-9), 112, 8, VG))
    c.append(t(X(-9) + 10, 116, "FIRST RECEIPT · ACTUAL DAY 1", 9, VG_DEEP, weight=600))
    c.append(ln(X(0), 184, X(0), ay + 12, INK, 1.5)); c.append(sq(X(0), 184, 8, INK))
    c.append(t(X(0) + 10, 188, "FNOL ENTERED · RECORDED DAY 1", 9, INK, weight=600))
    c.append(ln(x0, ay, x1, ay, INK, 1))
    for d in range(-12, 19):
        c.append(ln(X(d), ay, X(d), ay + (8 if d % 3 == 0 else 4), INK, 0.75))
        if d % 3 == 0:
            c.append(t(X(d), ay + 22, ("+" if d > 0 else "") + str(d), 8, MUTED, "middle"))
    c.append(path(f"M{X(-9)} 404 V412 H{X(0)} V404", CU, 1))
    c.append(t((X(-9) + X(0)) / 2, 432, "[N] DAYS BEFORE THE CLAIM EXISTS ON PAPER", 8, CU_DARK, "middle", 600))
    return "\n".join(c), "FNOL is not day 1", "BL-06"


def bl_inbox(pid, w, h):
    c = []
    c.append(r(96, 104, 320, 304, WHITE, INK, 1))
    c.append(r(96, 104, 320, 24, SECTION, INK, 1))
    c.append(t(106, 120, "CLAIMS INBOX", 8, INK, weight=600))
    for i in range(8):
        y = 128 + i * 35
        flag = i == 2
        c.append(r(96, y, 320, 35, CU_TINT if flag else WHITE, HAIR, 1))
        c.append(r(108, y + 10, 14, 14, CU if flag else SECTION, "none", 0))
        c.append(r(132, y + 11, [150, 120, 170, 140, 110, 160, 130, 150][i], 3, CU_DEEP if flag else "#9A9AA0", "none", 0))
        c.append(r(132, y + 21, [200, 180, 160, 210, 190, 170, 200, 150][i], 2.5, "#C9C9CC", "none", 0))
        if flag:
            c.append(r(96, y, 320, 35, "none", CU, 1.25))
    c.append(ln(80, 128, 80, 408, VG, 1.5)); c.append(sq(80, 128, 6, VG))
    c.append(t(72, 96, "ISOMER READS HERE", 8, VG_DEEP, weight=600))
    c.append(jn([(416, 216), (600, 216)], CU, 1.25, junctions=False)); c.append(arrow_r(600, 216, CU, 1.25))
    c.append(path("M424 248 V256 H600 V248", MUTED, 1))
    c.append(t(512, 276, "Δ DAYS UNTIL ENTRY", 9, INK, "middle", 600))
    c.append(r(608, 96, 40, 320, SECTION, INK, 1))
    for i in range(12):
        c.append(r(616, 104 + i * 26, 24, 18, WHITE, MUTED, 0.75))
    c.append(t(608, 440, "CMS ENTRY", 8, INK, weight=600))
    c.append(jn([(648, 216), (704, 216)], INK, 1, junctions=False)); c.append(arrow_r(704, 216))
    c.append(box(712, 192, 128, 48, "e", "ADJUSTER", "OPENS THE FILE"))
    c.append(path("M96 440 V448 H416 V440", CU, 1.25))
    c.append(t(256, 472, "LOSS RATIO IS DECIDED HERE", 10, CU_DARK, "middle", 600))
    return "\n".join(c), "Decided in the inbox", "BL-07"


