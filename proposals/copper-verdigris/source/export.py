"""Export every Copper Verdigris plate as a standalone SVG (+ 2x PNG) into ../illustrations/.

    pip install cairosvg   # PNG only; needs Geist + Geist Mono installed locally for correct type
    python3 export.py
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
P = {"__file__": os.path.join(HERE, "plates.py"), "__name__": "plates"}
exec(open(os.path.join(HERE, "plates.py")).read(), P)
OUT = os.path.join(HERE, "..", "illustrations")

# (id, function, w, h, family, title)
PLATES = [
    ("pl-01-point-of-receipt", "plate_hero", 480, 720, "plate", "Point of receipt"),
    ("pl-02-claim-graph", "plate_graph", 720, 720, "plate", "Claim graph"),
    ("pl-03-detector-array", "plate_detectors", 720, 720, "plate", "Detector array"),
    ("pl-04-immediate", "plate_immediate", 480, 480, "plate", "Immediate"),
    ("pl-05-continuous", "plate_continuous", 480, 480, "plate", "Continuous"),
    ("pl-06-elastic", "plate_elastic", 480, 480, "plate", "Elastic"),
    ("pl-07-signal-not-noise", "plate_signal", 480, 480, "plate", "Signal, not noise"),
    ("pl-08-nuclear-verdicts", "plate_verdicts", 480, 480, "plate", "Nuclear verdicts"),
    ("pl-09-litigation-funding", "plate_funding", 480, 480, "plate", "Litigation funding"),
    ("pl-10-industrialized", "plate_industrial", 480, 480, "plate", "Industrialized"),
    ("pl-11-receipt-to-record", "plate_pipeline", 1440, 400, "strip", "Receipt to record"),
    ("ac-01-time-limited-demand", "icon_tld", 320, 320, "glyph", "Time-limited demand"),
    ("ac-02-bad-faith", "icon_badfaith", 320, 320, "glyph", "Bad-faith allegation"),
    ("ac-03-florida-crn", "icon_crn", 320, 320, "glyph", "Florida CRN"),
    ("ac-04-attorney-rep", "icon_attorney", 320, 320, "glyph", "Attorney representation"),
    ("st-01-counsel-before-the-call", "st_lawyer", 720, 480, "story", "Counsel before the call"),
    ("st-02-buried-deadline", "st_buried", 720, 480, "story", "The buried deadline"),
    ("st-03-where-the-loss-is", "st_concentration", 720, 480, "story", "Where the loss is"),
    ("st-04-window-to-act", "st_window", 720, 480, "story", "Window to act"),
    ("st-05-one-point", "st_point", 720, 480, "story", "One point of combined ratio"),
    ("st-06-three-paths", "st_paths", 720, 480, "story", "Three paths to one point"),
    ("st-07-plaintiff-ai-funding", "st_funding", 720, 480, "story", "Who is building plaintiff AI"),
    ("st-08-thirty-minutes", "st_thirty", 720, 480, "story", "To the handler in 30 minutes"),
    ("st-09-four-week-assessment", "st_assessment", 720, 480, "story", "The 4-week assessment"),
    ("st-10-pricing", "st_pricing", 720, 480, "story", "Priced at 10% of target"),
    ("bl-01-sovereign", "bl_sovereign", 960, 540, "cover", "Sovereign claims AI"),
    ("bl-02-pfnol", "bl_pfnol", 960, 540, "cover", "Do we need a PFNOL?"),
    ("bl-03-signals-1h", "bl_narrative", 960, 540, "cover", "Signals are real (1H)"),
    ("bl-04-vendor-ai", "bl_vendor", 960, 540, "cover", "Your vendor's AI is yours"),
    ("bl-05-two-adjusters", "bl_two", 960, 540, "cover", "Two adjusters, same email"),
    ("bl-06-fnol-not-day-1", "bl_fnol", 960, 540, "cover", "FNOL is not day 1"),
    ("bl-07-decided-in-the-inbox", "bl_inbox", 960, 540, "cover", "Decided in the inbox"),
]
FONT = ('<style>@import url("https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600'
        '&amp;family=Geist+Mono:wght@400;500;600&amp;display=swap");</style>')


def svg(fid, fn, w, h, i, title, annotations=True):
    body, ftitle, code = P[fn](fid.replace("-", ""), w, h)
    fr = P["frame"](w, h, f"{i:02d}", ftitle.upper().replace("&", "&amp;"), code) if annotations else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<title>{title.replace("&", "&amp;")}</title>{FONT}<rect width="{w}" height="{h}" fill="{P["PAPER"]}"/>'
            f'{P["defs"](fid.replace("-", ""))}<g shape-rendering="crispEdges">{fr}</g>{body}</svg>')


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "clean"), exist_ok=True)
    try:
        import cairosvg
    except ImportError:
        cairosvg = None
    index = []
    for i, (fid, fn, w, h, fam, title) in enumerate(PLATES, 1):
        for sub, ann in (("", True), ("clean", False)):
            s = svg(fid, fn, w, h, i, title, ann)
            path = os.path.join(OUT, sub, f"{fid}.svg")
            open(path, "w").write(s)
            if cairosvg and ann:
                cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, f"{fid}.png"), output_width=w * 2, output_height=h * 2)
        index.append({"id": fid, "title": title, "family": fam, "width": w, "height": h, "function": fn,
                      "svg": f"illustrations/{fid}.svg", "svg_clean": f"illustrations/clean/{fid}.svg", "png_2x": f"illustrations/{fid}.png"})
    json.dump(index, open(os.path.join(OUT, "index.json"), "w"), indent=1)
    print(len(index), "plates")
