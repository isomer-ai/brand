# Copper Verdigris (proposal)

A proposed replacement for the Isomer palette, with illustration rules, sample plates and animations. Not adopted. This folder is deliberately not linked from the brand site, `brand.json` or `llms.txt`, and the page carries `noindex`.

Page: https://isomer-ai.github.io/brand/copper-verdigris/

| File | What it is |
| --- | --- |
| `index.html` | The shareable page: palette, at-work samples, illustration rules, plates, animations |
| `palette.json` | Every color with hex, RGB, role and use, plus the semantic rules |
| `tokens.css` | CSS custom properties (`--cv-*`) and semantic aliases |
| `USAGE-GUIDE.md` | Brand moments vs the work, product UI (light and dark), email, and porting an existing app |
| `ILLUSTRATION-GUIDE.md` | Full illustration and animation rules, written for agents and people |
| [`../pitch-cv/`](../pitch-cv/) | Reference rebuild of the isomer.ai/pitch-patina minisite, showing the palette and illustration rules on a full page: https://isomer-ai.github.io/brand/pitch-cv/ |
| `logos/` | Black (ink) and white logos to use with this palette, in SVG and PNG. Logo board: https://isomer-ai.github.io/brand/copper-verdigris/logos/ |
| `illustrations/` | 32 plates as annotated SVG, clean SVG (`clean/`) and 2x PNG; `index.json` lists them |
| `animations/` | MP4 (1080 px) and GIF (720 px) loops plus poster frames |
| `source/` | `plates.py` (primitives and every plate), `export.py`, `anim*.py`, `build_page.py` |

Regenerate everything from `source/`:

```bash
pip install cairosvg          # needs Fustat + IBM Plex Mono installed for PNG/video type, and ffmpeg
python3 export.py             # illustrations/
python3 anim.py && python3 anim2.py && python3 anim3.py   # animations/
python3 build_page.py         # index.html
```

If the team adopts it, the next steps are to fold `palette.json` into `scripts/build_manifest.py`, replace `tokens.css` at the root, adopt IBM Plex Mono as the annotation face, and decide whether the logo gets a Copper Verdigris version. Until then, use the black and white logos in `logos/`.
