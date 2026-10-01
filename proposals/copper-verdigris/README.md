# Copper Verdigris (proposal)

A proposed replacement for the Isomer palette, with illustration rules, sample plates and animations. Not adopted. This folder is deliberately not linked from the brand site, `brand.json` or `llms.txt`, and the page carries `noindex`.

Page: https://isomer-ai.github.io/brand/proposals/copper-verdigris/

In use: the [isomer.ai/pitch-patina](https://isomer.ai/pitch-patina) minisite applies this palette to a live page. It uses the colors only; the illustration style here is not used there.

| File | What it is |
| --- | --- |
| `index.html` | The shareable page: palette, at-work samples, illustration rules, plates, animations |
| `palette.json` | Every color with hex, RGB, role and use, plus the semantic rules |
| `tokens.css` | CSS custom properties (`--cv-*`) and semantic aliases |
| `ILLUSTRATION-GUIDE.md` | Full illustration and animation rules, written for agents and people |
| `illustrations/` | 32 plates as annotated SVG, clean SVG (`clean/`) and 2x PNG; `index.json` lists them |
| `animations/` | MP4 (1080 px) and GIF (720 px) loops plus poster frames |
| `source/` | `plates.py` (primitives and every plate), `export.py`, `anim*.py`, `build_page.py` |

Regenerate everything from `source/`:

```bash
pip install cairosvg          # needs Geist + Geist Mono installed for PNG/video type, and ffmpeg
python3 export.py             # illustrations/
python3 anim.py && python3 anim2.py && python3 anim3.py   # animations/
python3 build_page.py         # index.html
```

If the team adopts it, the next steps are to fold `palette.json` into `scripts/build_manifest.py`, replace `tokens.css` at the root, decide Geist vs Fustat, and redraw the logo files in the new palette.
