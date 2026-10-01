import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
L = {"__file__": os.path.join(HERE, "anim2.py"), "__name__": "lib2"}
exec(open(os.path.join(HERE, "anim2.py")).read(), L)
globals().update({k: L[k] for k in ("g", "r", "ln", "t", "sq", "doc", "path", "status", "clamp", "ease", "seg",
                                    "wrap", "cap", "grow", "fade", "render", "S")})
g = L["g"]
INK, MUTED, WHITE, SECTION, HAIR = g["INK"], g["MUTED"], g["WHITE"], g["SECTION"], g["HAIR"]
CU, CU_TINT, CU_DARK, CU_DEEP = g["CU"], g["CU_TINT"], g["CU_DARK"], g["CU_DEEP"]
VG, VG_TINT, VG_DARK, VG_DEEP, SANS = g["VG"], g["VG_TINT"], g["VG_DARK"], g["VG_DEEP"], g["SANS"]

N, FLAG = 12, 8
DW, DH = 48, 62
X0, XEND = 56, 470
PX, PW = 300, 40          # detector plane
PC = PX + PW / 2
XSTOP = PC - DW / 2       # flagged doc parks centred in the plane
CY = 200                  # doc top on the conveyor
T0, GAP, TRAVEL = 0.9, 0.18, 1.2
T_ARR = T0 + FLAG * GAP + TRAVEL * (XSTOP - X0) / (XEND - X0)
T_DROP = (T_ARR + 0.5, T_ARR + 1.2)
T_SIG = (T_DROP[1] - 0.1, T_DROP[1] + 0.4)
T_LINE = (T_SIG[1] + 0.3, T_SIG[1] + 0.8)
T_ACT = (T_LINE[1], T_LINE[1] + 0.5)
T_DONE = T_ACT[1] + 0.4
DUR = T_DONE + 1.6


def receipt(T):
    c = []
    a = seg(T, 0, 0.6)
    c.append(fade(a, ln(48, CY + DH + 10, 672, CY + DH + 10, HAIR, 1)
                  + t(56, 104, "INBOUND", 9, MUTED, weight=500)
                  + r(PX, 96, PW, 270, SECTION, INK, 1)
                  + t(PX - 8, 72, "DETECTOR PLANE · 85", 9, MUTED, weight=500)
                  + t(488, 104, "CLEAR", 9, MUTED, weight=500)))
    lit = T >= T_ARR
    for i in range(13):
        y = 104 + i * 20
        hot = lit and i == 6
        c.append(r(PX + 8, y, 24, 13, CU_TINT if hot else WHITE, CU if hot else MUTED, 1.25 if hot else 0.75))
    pulse = 0
    for k in range(N):
        tk = T0 + k * GAP + TRAVEL * (PC - DW / 2 - X0) / (XEND - X0)
        if abs(T - tk) < 0.18:
            pulse = max(pulse, 1 - abs(T - tk) / 0.18)
    c.append(fade(a, ln(PC, 86, PC, 380, VG, 1.5 + 1.5 * pulse) + sq(PC, 86, 7, VG) + sq(PC, 380, 7, VG)))
    c.append(fade(seg(T, 0.4, 0.9), t(PC + 14, 392, "READ IN FULL · T0", 9, VG_DEEP, weight=600)))
    # inbound stack
    remaining = sum(1 for k in range(N) if T < T0 + k * GAP)
    for i in range(min(remaining, 4) - 1, -1, -1):
        c.append(doc(56 + i * 5, 116 + i * 6, DW, DH, WHITE, INK))
    # moving docs
    for k in range(N):
        st = T0 + k * GAP
        if T < st:
            continue
        p = (T - st) / TRAVEL
        if k == FLAG:
            x = min(X0 + (XEND - X0) * p, XSTOP)
            y = CY + (436 - CY) * seg(T, *T_DROP)
            if T < T_SIG[1] + 0.15:
                c.append(doc(round(x, 1), round(y, 1), DW, DH, CU_TINT if lit else WHITE, CU if lit else INK, hl={3} if lit else None, hlc=CU))
            continue
        if p >= 1:
            continue
        x = X0 + (XEND - X0) * p
        c.append(fade(1 - clamp((p - 0.82) / 0.18), doc(round(x, 1), CY, DW, DH, WHITE, INK)))
    # clear tally
    cleared = sum(1 for k in range(N) if k != FLAG and T >= T0 + k * GAP + TRAVEL)
    for i in range(cleared):
        col, row = i % 6, i // 6
        c.append(r(488 + col * 24, 120 + row * 24, 16, 16, WHITE, MUTED, 0.75))
    if cleared:
        c.append(t(488, 190, f"{round(213 * cleared / (N - 1))} CLEAR", 11, INK, weight=600))
    if T > T_DONE:
        c.append(fade(seg(T, T_DONE, T_DONE + 0.4), status(488, 220, "ok", "NOTHING ELSE")))
    # signal -> act, one straight run
    c.append(grow(PC, 366, PC, 430, seg(T, T_DROP[0], T_DROP[0] + 0.4), CU, 1.25))
    if T > T_SIG[0]:
        c.append(fade(seg(T, *T_SIG), r(232, 430, 176, 120, CU_TINT, CU, 1.25)
                      + doc(244, 444, 52, 72, WHITE, CU_DEEP, [0.7, 0.5, 0.8, 0.6, 0.7, 0.4], hl={2})
                      + t(310, 462, "SIGNAL", 9, CU_DARK, weight=500)
                      + t(310, 488, "TLD", 20, CU_DARK, weight=600, ls=0.3, family=SANS)
                      + t(310, 514, "ATT-3 · p.4", 9, CU_DEEP)
                      + t(244, 538, "30-DAY CLOCK STARTED", 8, CU_DARK, weight=600)))
    if T > T_LINE[0]:
        p = seg(T, *T_LINE)
        c.append(grow(408, 490, 456, 490, p, VG, 1.5))
        if p > 0.98:
            c.append(path("M448 484 L456 490 L448 496", VG, 1.5))
    if T > T_ACT[0]:
        ck = seg(T, T_ACT[0] + 0.2, T_ACT[1] + 0.3)
        c.append(fade(seg(T, *T_ACT), r(460, 450, 212, 80, VG_TINT, VG, 1.25)
                      + f'<path d="M478 490 L486 498 L502 480" fill="none" stroke="{VG_DEEP}" stroke-width="2" stroke-dasharray="40" stroke-dashoffset="{round(40 * (1 - ck), 1)}"/>'
                      + t(514, 482, "ACT", 9, VG_DARK, weight=600)
                      + t(514, 500, "DEADLINE CALENDARED", 9, VG_DEEP, weight=500)
                      + t(514, 516, "RESERVE REVIEW OPENED", 9, VG_DEEP, weight=500)))
    caption = cap(T, [(0, "01 · ARRIVES"), (T0 + 0.6, "02 · EVERY PAGE READ"), (T_ARR, "03 · DEADLINE FOUND · ATT-3"),
                      (T_ACT[0], "04 · ACTED ON · SAME DAY")])
    return wrap("\n".join(c), "A1", "POINT OF RECEIPT", "AN-01", T, DUR, caption), DUR


if __name__ == "__main__":
    print(render("point-of-receipt-1x1", receipt))
