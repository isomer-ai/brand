#!/usr/bin/env python3
"""Regenerate brand.json from the files under logos/, colors/, and guidelines/.

Run from the repo root after adding or renaming assets:  python3 scripts/build_manifest.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = "https://isomer-ai.github.io/brand/"
RAW = "https://raw.githubusercontent.com/isomer-ai/brand/main/"

COLORS = [
    {"name": "Isomer Blue", "token": "isomer-blue", "role": "primary",
     "hex": "#000441", "rgb": [0, 4, 65], "cmyk": [97, 99, 38, 45], "pantone": "2766 C"},
    {"name": "Accent Purple", "token": "accent-purple", "role": "accent",
     "hex": "#776DEB", "rgb": [119, 109, 235], "cmyk": [70, 60, 0, 0], "pantone": "7456 C"},
    {"name": "Light Purple", "token": "light-purple", "role": "accent",
     "hex": "#9188F5", "rgb": [145, 136, 245], "cmyk": [48, 48, 0, 0], "pantone": "7446 C"},
    {"name": "Secondary Orange", "token": "secondary-orange", "role": "secondary",
     "hex": "#FFA574", "rgb": [255, 165, 116], "cmyk": [0, 45, 61, 0], "pantone": "1565 C"},
    {"name": "Light Gray", "token": "light-gray", "role": "background",
     "hex": "#F8F6FF", "rgb": [248, 246, 255], "cmyk": [2, 2, 0, 0], "pantone": "663 C"},
    {"name": "White", "token": "white", "role": "background",
     "hex": "#FFFFFF", "rgb": [255, 255, 255], "cmyk": [0, 0, 0, 0], "pantone": "1-1 C"},
]

TINTS = {
    "isomer-blue": {"100": "#000441", "70": "#4D507A", "60": "#66688D", "50": "#8082A0", "40": "#999BB3"},
    "accent-purple": {"100": "#776DEB", "80": "#9188F5", "60": "#ADA7F3", "45": "#C2BDF6"},
}

TYPOGRAPHY = {
    "family": "Fustat",
    "source": "Google Fonts",
    "url": "https://fonts.google.com/specimen/Fustat",
    "css_import": "https://fonts.googleapis.com/css2?family=Fustat:wght@200..800&display=swap",
    "fallback": "system-ui, -apple-system, 'Segoe UI', sans-serif",
}

NAME = re.compile(r"isomer-(logo-horiz|logo-vert|logomark)-(color|solid|monochrome)-(.+)")
LAYOUT = {"logo-horiz": "horizontal", "logo-vert": "vertical", "logomark": "mark"}
USE_ON = {"dark-bg": "dark", "transp-dark-bg": "dark", "white-bg": "light",
          "transp-white-bg": "light", "dark": "light", "light": "dark"}


def logos():
    out = {}
    for f in sorted((ROOT / "logos" / "web" / "svg").glob("*.svg")):
        m = NAME.fullmatch(f.stem)
        layout, style, rest = m.groups()
        variant = {
            "id": f.stem,
            "layout": LAYOUT[layout],
            "style": style,
            "transparency": rest.startswith("transp-") or style == "monochrome",
            "use_on": USE_ON[rest],
            "files": {},
        }
        for medium in ("web", "print"):
            for ext in ("svg", "png", "pdf", "ai"):
                p = ROOT / "logos" / medium / ext / f"{f.stem}.{ext}"
                if p.exists():
                    rel = p.relative_to(ROOT).as_posix()
                    variant["files"].setdefault(medium, {})[ext] = PAGES + rel
        out[f.stem] = variant
    return list(out.values())


manifest = {
    "name": "Isomer",
    "legal_name": "Isomer AI, Inc.",
    "website": "https://isomer.ai",
    "tagline": "Built for insurance.",
    "base_url": PAGES,
    "raw_base_url": RAW,
    "colors": COLORS,
    "tints": TINTS,
    "typography": TYPOGRAPHY,
    "logo_defaults": {
        "light_background": "isomer-logo-horiz-color-white-bg",
        "dark_background": "isomer-logo-horiz-color-dark-bg",
        "favicon_or_avatar": "isomer-logomark-color-white-bg",
    },
    "logos": logos(),
    "palette_files": {
        "rgb": {"ase": PAGES + "colors/rgb/isomer-colors-rgb.ase", "ai": PAGES + "colors/rgb/isomer-colors-rgb.ai"},
        "cmyk": {"ase": PAGES + "colors/cmyk/isomer-colors-cmyk.ase", "ai": PAGES + "colors/cmyk/isomer-colors-cmyk.ai"},
    },
    "guideline_pdf": PAGES + "guidelines/isomer-design-guideline.pdf",
    "tokens_css": PAGES + "tokens.css",
}

(ROOT / "brand.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"brand.json: {len(manifest['logos'])} logo variants")
