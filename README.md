# Isomer Brand Assets

Official logos, colors, and typography for [Isomer](https://isomer.ai). Browse them at [isomer-ai.github.io/brand](https://isomer-ai.github.io/brand/).

## For Agents

Start with [`brand.json`](https://isomer-ai.github.io/brand/brand.json). It lists every color, tint, and font, and every logo variant with direct URLs to each file format. Stylesheets can import [`tokens.css`](https://isomer-ai.github.io/brand/tokens.css) for the same values as CSS custom properties.

```bash
curl -s https://isomer-ai.github.io/brand/brand.json | jq '.logo_defaults'
```

Picking a logo:

- On a light or white background, use `isomer-logo-horiz-color-white-bg`
- On a dark background, use `isomer-logo-horiz-color-dark-bg`
- For a square slot such as a favicon, avatar, or app icon, use `isomer-logomark-color-white-bg`
- For screens, use files under `logos/web/` (RGB). For print, use `logos/print/` (CMYK-adjusted colors).
- Prefer SVG. Use PNG (2200 px wide) only when the target can't render SVG.

File URLs follow one pattern:

```text
https://isomer-ai.github.io/brand/logos/{web|print}/{svg|png|pdf|ai}/{variant}.{ext}
```

## Logo Variants

Each variant name is `isomer-{layout}-{style}-{background}`.

| Part | Values | Meaning |
| --- | --- | --- |
| Layout | `logo-horiz`, `logo-vert`, `logomark` | Mark beside the wordmark, mark above the wordmark, or the mark alone |
| Style | `color` | Full palette. The standard choice. |
| | `solid` | One flat color |
| | `monochrome` | One color in stepped opacities |
| Background | `white-bg`, `dark-bg` | Color logo drawn for a light or a dark background |
| | `transp-white-bg`, `transp-dark-bg` | Same, built with transparency rather than solid tints |
| | `dark` | Isomer Blue ink, for light backgrounds (solid and monochrome) |
| | `light` | White ink, for dark backgrounds (solid and monochrome) |

No file includes a filled background. The background suffix says what the logo is meant to sit on.

## Colors

| Name | Hex | RGB | CMYK | Pantone | Role |
| --- | --- | --- | --- | --- | --- |
| Isomer Blue | `#000441` | 0, 4, 65 | 97, 99, 38, 45 | 2766 C | Primary |
| Accent Purple | `#776DEB` | 119, 109, 235 | 70, 60, 0, 0 | 7456 C | Accent |
| Light Purple | `#9188F5` | 145, 136, 245 | 48, 48, 0, 0 | 7446 C | Accent |
| Secondary Orange | `#FFA574` | 255, 165, 116 | 0, 45, 61, 0 | 1565 C | Secondary |
| Light Gray | `#F8F6FF` | 248, 246, 255 | 2, 2, 0, 0 | 663 C | Background |
| White | `#FFFFFF` | 255, 255, 255 | 0, 0, 0, 0 | 1-1 C | Background |

Tints:

- Isomer Blue at 100 / 70 / 60 / 50 / 40%: `#000441` `#4D507A` `#66688D` `#8082A0` `#999BB3`
- Accent Purple at 100 / 80 / 60 / 45%: `#776DEB` `#9188F5` `#ADA7F3` `#C2BDF6`

Adobe swatch files (`.ase`) and Illustrator palettes are in [`colors/`](colors/).

## Typography

Titles and headlines are set in [Fustat](https://fonts.google.com/specimen/Fustat). Body text, UI, tables and captions are set in [Inter](https://fonts.google.com/specimen/Inter). Both are free from Google Fonts.

```html
<link href="https://fonts.googleapis.com/css2?family=Fustat:wght@200..800&family=Inter:wght@300..800&display=swap" rel="stylesheet">
```

In CSS, use `--isomer-font-display` for titles and `--isomer-font-body` for text, both in [`tokens.css`](tokens.css).

## Clear Space

The guideline measures clear space in units of `A`, the width of the mark. Leave at least `1/2A` around the horizontal lockup and `1/3A` around the mark by itself. The full construction and spacing rules are in the [design guideline](guidelines/isomer-design-guideline.pdf).

## Repository Layout

```text
brand.json                   Machine-readable manifest (generated)
tokens.css                   CSS custom properties
index.html                   The browsable site
guidelines/                  Design guideline PDF
colors/{rgb,cmyk}/           .ase swatches and .ai palettes
logos/{web,print}/{svg,png,pdf,ai}/
scripts/build_manifest.py    Regenerates brand.json
```

After adding, renaming, or recoloring anything, run `python3 scripts/build_manifest.py` and commit the updated `brand.json`.

## Usage

These assets identify Isomer AI, Inc. Use them to refer to Isomer, not in ways that suggest endorsement or affiliation. Don't recolor, stretch, or rearrange the logo.
