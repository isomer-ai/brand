import os, math, subprocess, shutil
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
G = {"__file__": os.path.join(HERE, "plates.py"), "__name__": "anim"}
exec(open(os.path.join(HERE, "plates.py")).read().split("# ---------- plates ----------")[0], G)
g = G
INK, MUTED, WHITE, PAPER, SECTION, HAIR = g["INK"], g["MUTED"], g["WHITE"], g["PAPER"], g["SECTION"], g["HAIR"]
CU, CU_TINT, CU_DARK, CU_DEEP = g["CU"], g["CU_TINT"], g["CU_DARK"], g["CU_DEEP"]
VG, VG_TINT, VG_DARK, VG_DEEP, VG_MIST = g["VG"], g["VG_TINT"], g["VG_DARK"], g["VG_DEEP"], g["VG_MIST"]
COB, COB_TINT, COB_DEEP = g["COB"], g["COB_TINT"], g["COB_DEEP"]
r, ln, t, sq, doc, path, frame, defs, status = g["r"], g["ln"], g["t"], g["sq"], g["doc"], g["path"], g["frame"], g["defs"], g["status"]

W, H, FPS, DUR = 1280, 720, 30, 9.0
OUT = os.path.join(HERE, "..", "animations")
FR = os.path.join(OUT, "_frames", "point-of-receipt-16x9")


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def seg(T, a, b):
    return ease((T - a) / (b - a))


N = 14            # docs shown (stand-ins for 214)
FLAG = 9          # index of the doc that carries the deadline
X_START, X_PLANE, X_EXIT = 96, 492, 760
PLANE_X = 500
CONV_Y = 268
T0, GAP, TRAVEL = 1.0, 0.17, 1.2
T_FLAG_ARRIVE = T0 + FLAG * GAP + TRAVEL * (X_PLANE - X_START) / (X_EXIT - X_START)
T_DROP = (T_FLAG_ARRIVE + 0.5, T_FLAG_ARRIVE + 1.3)
T_SIG = (T_DROP[1], T_DROP[1] + 0.5)
T_LINE = (T_SIG[1] + 0.3, T_SIG[1] + 0.9)
T_ACT = (T_LINE[1], T_LINE[1] + 0.5)
T_DONE = T_ACT[1] + 0.4


def scene(T):
    c = []
    a_in = seg(T, 0.0, 0.6)
    # apparatus
    c.append(f'<g opacity="{a_in}">')
    c.append(ln(96, CONV_Y + 44, 1184, CONV_Y + 44, HAIR, 1))
    c.append(t(96, 132, "INBOUND", 9, MUTED, weight=500))
    c.append(r(PLANE_X, 120, 40, 330, SECTION, INK, 1))
    c.append(t(PLANE_X - 8, 112, "DETECTOR PLANE · 85", 9, MUTED, weight=500))
    c.append(t(820, 132, "CLEAR", 9, MUTED, weight=500))
    c.append('</g>')
    # detector cells, flagged cell lights when the flagged doc is in the plane
    lit = seg(T, T_FLAG_ARRIVE, T_FLAG_ARRIVE + 0.25)
    for i in range(16):
        y = 128 + i * 20
        fill = WHITE
        if i == 7 and lit > 0:
            fill = CU_TINT
        c.append(r(PLANE_X + 8, y, 24, 14, fill, CU if (i == 7 and lit > 0.5) else MUTED, 0.75 if not (i == 7 and lit > 0.5) else 1.25))
    # scan line pulses as each doc crosses
    pulse = 0
    for k in range(N):
        tk = T0 + k * GAP + TRAVEL * (PLANE_X - 20 - X_START) / (X_EXIT - X_START)
        pulse = max(pulse, 1 - abs(T - tk) / 0.18) if abs(T - tk) < 0.18 else pulse
    sw = 1.5 + 1.5 * clamp(pulse)
    c.append(f'<g opacity="{a_in}">' + ln(PLANE_X + 20, 104, PLANE_X + 20, 466, VG, sw) + sq(PLANE_X + 20, 104, 7, VG) + sq(PLANE_X + 20, 466, 7, VG) + '</g>')
    c.append(f'<g opacity="{seg(T, 0.4, 0.9)}">' + t(PLANE_X + 32, 480, "READ IN FULL · T0", 9, VG_DEEP, weight=600) + '</g>')
    # inbound stack shrinks
    remaining = sum(1 for k in range(N) if T < T0 + k * GAP)
    for i in range(min(remaining, 5) - 1, -1, -1):
        c.append(doc(96 + i * 5, 150 + i * 6, 56, 72, WHITE, INK))
    # tally grid
    cleared = 0
    for k in range(N):
        if k == FLAG:
            continue
        if T >= T0 + k * GAP + TRAVEL:
            cleared += 1
    count = 0 if cleared == 0 else min(213, round(213 * cleared / (N - 1)))
    for i in range(cleared):
        col, row = i % 7, i // 7
        c.append(r(820 + col * 22, 148 + row * 22, 16, 16, WHITE, MUTED, 0.75))
    if cleared:
        c.append(t(820, 218, f"{count} CLEAR", 10, INK, weight=600))
    if T > T_DONE:
        c.append(f'<g opacity="{seg(T, T_DONE, T_DONE + 0.4)}">' + status(980, 218, "ok", "NOTHING ELSE NEEDS A PERSON") + '</g>')
    # moving docs
    for k in range(N):
        start = T0 + k * GAP
        if T < start:
            continue
        p = (T - start) / TRAVEL
        if k == FLAG:
            x = X_START + (X_PLANE - X_START) * min(1, p / ((X_PLANE - X_START) / (X_EXIT - X_START)))
            y = CONV_Y - 36
            d = seg(T, *T_DROP)
            y = y + d * (500 - (CONV_Y - 36))
            if T < T_SIG[1] + 0.2:
                c.append(doc(round(x, 1), round(y, 1), 56, 72, CU_TINT if T > T_FLAG_ARRIVE else WHITE,
                             CU if T > T_FLAG_ARRIVE else INK, hl={3}, hlc=CU))
            continue
        if p >= 1:
            continue
        x = X_START + (X_EXIT - X_START) * ease(p) if False else X_START + (X_EXIT - X_START) * p
        op = 1 - clamp((p - 0.85) / 0.15)
        c.append(f'<g opacity="{round(op, 2)}">' + doc(round(x, 1), CONV_Y - 36, 56, 72, WHITE, INK) + '</g>')
    # signal box, straight drop path
    if T > T_DROP[0]:
        a = seg(T, T_DROP[0], T_DROP[0] + 0.3)
        c.append(f'<g opacity="{a}">' + ln(PLANE_X + 20, 450, PLANE_X + 20, 500, CU, 1.25) + '</g>')
    if T > T_SIG[0]:
        a = seg(T, *T_SIG)
        c.append(f'<g opacity="{a}">')
        c.append(r(420, 500, 200, 92, CU_TINT, CU, 1.25))
        c.append(doc(432, 510, 52, 72, WHITE, CU_DEEP, [0.7, 0.5, 0.8, 0.6, 0.7, 0.4], hl={2}))
        c.append(t(498, 526, "SIGNAL", 9, CU_DARK, weight=500))
        c.append(t(498, 548, "TLD", 18, CU_DARK, weight=600, ls=0.3, family=g["SANS"]))
        c.append(t(498, 576, "ATT-3 · p.4", 9, CU_DEEP))
        c.append('</g>')
    if T > T_LINE[0]:
        L = seg(T, *T_LINE)
        x2 = 620 + L * (720 - 620)
        c.append(ln(620, 546, round(x2, 1), 546, VG, 1.5))
        if L > 0.98:
            c.append(path("M712 540 L720 546 L712 552", VG, 1.5))
    if T > T_ACT[0]:
        a = seg(T, *T_ACT)
        c.append(f'<g opacity="{a}">')
        c.append(r(724, 516, 220, 60, VG_TINT, VG, 1.25))
        ck = seg(T, T_ACT[0] + 0.2, T_ACT[1] + 0.3)
        c.append(f'<path d="M742 546 L750 554 L766 536" fill="none" stroke="{VG_DEEP}" stroke-width="2" stroke-dasharray="40" stroke-dashoffset="{round(40 * (1 - ck), 1)}"/>')
        c.append(t(778, 540, "ACT", 9, VG_DARK, weight=600))
        c.append(t(778, 558, "DEADLINE CALENDARED", 9, VG_DEEP, weight=500))
        c.append('</g>')
    # step caption
    steps = [(0, "01 · ARRIVES"), (T0 + 0.6, "02 · EVERY PAGE READ"), (T_FLAG_ARRIVE, "03 · DEADLINE FOUND · ATT-3"),
             (T_ACT[0], "04 · ACTED ON · SAME DAY")]
    cap = [s for (ts, s) in steps if T >= ts][-1]
    c.append(t(96, 660, cap, 11, INK, weight=600, ls=1.4))
    # progress ruler
    c.append(ln(96, 676, 96 + (1184 - 96) * clamp(T / DUR), 676, VG, 1.5))
    return "\n".join(c)


def svg_for(T):
    body = scene(T)
    fr = frame(W, H, "A1", "POINT OF RECEIPT", "AN-01")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{PAPER}"/>{defs("an")}{fr}{body}</svg>')


if __name__ == "__main__":
    shutil.rmtree(FR, ignore_errors=True)
    os.makedirs(FR, exist_ok=True)
    n = int(DUR * FPS)
    for i in range(n):
        T = i / FPS
        cairosvg.svg2png(bytestring=svg_for(T).encode(), write_to=os.path.join(FR, f"f{i:04d}.png"), output_width=1920, output_height=1080)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FR, "f%04d.png"), "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", os.path.join(OUT, "point-of-receipt-16x9.mp4")], check=True)
    print("frames", n, "flag at", round(T_FLAG_ARRIVE, 2), "done at", round(T_DONE, 2))
