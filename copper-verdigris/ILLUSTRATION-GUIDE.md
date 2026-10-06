# Copper Verdigris illustration guide

Status: proposal. Companion to [`palette.json`](palette.json), [`tokens.css`](tokens.css) and the [usage guide](USAGE-GUIDE.md), which covers brand moments, product UI and email.

Isomer plates are drawn like instrument readouts. They are rectilinear, measured and labelled. Copper marks the risk, verdigris marks Isomer acting on it, and everything else is ink on paper.

## For agents

1. Read [`palette.json`](palette.json) for color values and meanings. Use only those hex values.
2. Read this guide end to end before drawing anything.
3. To reuse an existing plate, take it from [`illustrations/index.json`](illustrations/index.json). Each entry has an annotated SVG, a clean SVG (no frame, for web placement) and a 2x PNG.
4. To make a new plate, build it with the primitives in [`source/plates.py`](source/plates.py) (`r`, `ln`, `path`, `t`, `sq`, `doc`, `status`, `person`, `frame`). Copy the closest existing plate function and change the content, not the vocabulary.
5. Run the checklist at the bottom before you hand anything back.

## Principles

1. **Figures, not illustrations.** Every plate encodes a real quantity or a real mechanism. If it would read the same with the labels removed and nothing measured, it is decoration. Cut it.
2. **Right angles, fewest bends.** Figures are built from straight lines and sharp corners. 45° appears only as hatching. Lay nodes out on shared rows and columns so connectors run straight. One bend is a compromise; two is a layout problem.
3. **Color is a verb.** Neutrals draw the apparatus. Copper means risk was found or time ran out. Verdigris means Isomer acted. One meaning per color, one color per element.
4. **Show the source.** Every number traces to a cited source in the plate footer or the surrounding copy. Unknowns are written as `[BRACKETED]` placeholders, never invented.
5. **One idea per plate.** A plate makes one comparison or shows one mechanism. If it needs two headlines, it is two plates.

## Color on plates

| Role | Color | Use |
| --- | --- | --- |
| Structure | Ink `#141416` | Lines, primary labels, central nodes |
| Secondary | Muted `#6E6E75` | Ticks, rulers, secondary labels, source traces |
| Grid | Hairline `#E3E3E5` | Grid lines, table rules |
| Apparatus | Section gray `#ECECEA` | Detector planes, gates, bands |
| Ground | Paper `#F6F6F5` | Default background |
| Objects | White `#FFFFFF` | Documents and entities on paper |
| Signal | Copper `#B4602F`, tint `#F2DCCB`, label `#8E4720` | Risk found, flagged, too late, plaintiff side |
| Action | Verdigris `#3F8A85`, tint `#E9F2F1`, mist `#D3E6E4`, label `#1F4F4C` | Isomer acting, scan line, outcomes, window-to-act |
| Critical | Oxide red `#B4232F`, tint `#F8DEE0` | Status tag only. Suit filed, limits opened, deadline blown |
| OK | Cobalt `#2F5D99`, tint `#E3ECF7` | Status tag only. Healthy, clear, info |

Rules:

- Copper and verdigris never sit on the same element and never appear as a decorative pair. Plates are the work, not a brand moment; the pair as identity belongs to the brand devices on covers, slides and mastheads (see the [usage guide](USAGE-GUIDE.md#brand-moments)).
- Copper is the only color that may be hatched. Hatching means excess, unreviewed or at-risk volume.
- Red and cobalt work as they do in the app: status, sparingly. They appear only as a tag (square dot + the word OK or CRITICAL + a label), never as a fill area or chart series. At most one of each per plate; most plates have none.
- Warning stays copper. Don't put red on problem-statement plates (verdicts, funding); that's risk, which is copper's job.
- No full-bleed copper. The largest copper fill is a single element.
- On graphite grounds use Copper light `#E09C6B`, Verdigris light `#8CC2BC`, `#A4A9AA` for muted text and white for ink.
- Rough share on any plate: neutrals about 82%, ink 8%, copper and verdigris about 4.5% each, status 1% or less.

## Construction

- **Grid.** Build on 8px. Graph fields use a 24px dot grid. Content sits 48px in from the plate edge; the ruler sits at 24px.
- **Line weight carries meaning.** 0.75 for ticks, grid and traces. 1 for structure. 1.25 for semantic (copper, verdigris) outlines. 1.5 for emphasis and the scan line.
- **Dash pattern carries meaning.** 3/3 is a source trace. 6/3 is a threshold or limit. 8/4 is a boundary such as a tenant.
- **Connectors.** Straight first. A 5px junction square marks a branch point only, never a plain bend. Square caps, miter joins.
- **Corners.** Radius 0 on every box, node, bar and tag.
- **Arrangement.** Boxes that sit together form one rectangle: shared outer edges, each row at one height, each column at one width, gutters on the 8px grid. When two boxes are close in size, make them identical, and use as few sizes as possible. The same rule holds on slides and pages; see Layout in the [usage guide](USAGE-GUIDE.md).
- **Circles and curves.** Circles are allowed occasionally (a point marker, a dial). Curves are allowed inside icons, such as the person figure for a claimant, counsel or adjuster (`person()` in `plates.py`: circle head, curved shoulders, flat base so it sits on the diagram baseline), and where the curve is the figure: the flow bands of a Sankey, which show volume moving from one split to another. Use them only when the chart type needs them, never as decoration or to soften a connector.
- **Fills.** White for objects, section gray for apparatus, tints for semantic fills. No gradients, shadows, glows or transparency stacks.

## Components

- **Entity node.** White fill, ink 1px. Title in mono 600, id below in muted.
- **Signal node.** Copper tint fill, copper 1.25px, copper-dark label.
- **Action node.** Verdigris tint fill, verdigris 1.25px, verdigris-dark label.
- **Document.** White rectangle with a folded corner square and gray text strokes; one strike may be copper to show where the risk is.
- **Apparatus and scan line.** Section-gray plane with cells; a 1.5px verdigris line with square terminals.
- **Dimension bracket.** Muted 1px bracket with the measured value centered below.
- **Threshold.** Ink 1.25px, 6/3 dash, label right-aligned above.
- **Axis.** Ink 1px with minor and major ticks (every 5th major).
- **Markers.** 8px squares. Verdigris for t₀ or arrival, copper for late.
- **Status tag.** Tint fill, 1px outline, square dot, the word, then the label.

## Type

- **Annotation: IBM Plex Mono.** Uppercase, 7 to 10px, tracking 0.8 to 1.4. Weight 400 for description, 500 for axis and column labels, 600 for the one label that carries the point. Labels sit outside shapes, or top-left inside with a 10px inset.
- **Hero value: Fustat 600.** At most one per plate, 12 to 18px (32px only on covers), in the semantic color of what it measures. Never a sentence. Headlines live on the page, not in the plate, set in Fustat with body text in Inter (see Type in the [usage guide](USAGE-GUIDE.md)).

## Staying distinct

Other claims-AI brands use the same base vocabulary: off-white paper, hairlines, a grotesk with uppercase mono labels, a dark evidence panel, red and green dots. On that base alone we look like the category. What makes it ours:

- **Copper and verdigris do the work.** Inside the work they are verbs, and their scarcity is what makes them land. As identity they appear through a few brand devices on ink or paper (the oxidation band, the short oxidation bar, the bar and pixel), never as a small accent everywhere. See [Two registers](USAGE-GUIDE.md#two-registers).
- **The apparatus travels.** Rulers, plate codes and the scan line appear in page UI too, not only inside plates. In UI they stay quiet: gray ticks at low opacity, no copper. Copper hatching stays inside figures, where it measures something.
- **Time is the subject.** Prefer plates that show when something was caught (t₀, d23, the window to act) over plates that show what a file contains.
- **Fustat, not a generic grotesk.** Keep the brand face for titles and values, Inter for body text, IBM Plex Mono for annotation.
- **Avoid** big-number tiles over a mono caption row, dark "extraction" text panels, numbered section eyebrows (01, 02...), and status dots without a word. Show values to scale on an axis instead of as tiles.

## Formats

| Code | Format | Size | Use |
| --- | --- | --- | --- |
| PL | Plate | 480 × 480 | Section feature, stat |
| PL | Feature | 720 × 720 | System mechanism |
| PL | Hero | 480 × 720 | Tall hero beside a headline |
| PL | Strip | 1440 × 400 | Prefooter, wide band |
| AC | Glyph | 320 × 320 | Playbook or card icon |
| ST | Story | 720 × 480 | Pitch narrative sections |
| BL | Cover | 960 × 540 | Blog header, social card |
| AN | Animation | 1080 × 1080 or 1920 × 1080 | Social, decks, site |

The annotated version carries the FIG number and title, plate code, rulers, crosshair and footer. Use the `clean/` SVG for web placement; keep the annotated version for decks, reports and blog covers.

## Animation

Animations are the same plates rendered frame by frame. The scene is a function of time, so nothing is hand-keyed. See [`source/anim.py`](source/anim.py), [`source/anim2.py`](source/anim2.py) and [`source/anim3.py`](source/anim3.py).

- **Beats, not motion for its own sake.** Three or four beats, each with a mono caption at the bottom (`01 · ARRIVES`, `02 · EVERY PAGE READ`, ...). A thin verdigris progress rule runs under the caption.
- **Easing.** Smoothstep on every move. Fades 0.3 to 0.6s. Elements enter by fading or by drawing their stroke; nothing bounces, scales or spins.
- **Color changes are the story.** An element turns copper at the moment risk is found and a verdigris element appears at the moment Isomer acts.
- **Connectors draw on**, straight, from source to target.
- **Length** 8 to 10s, with the final frame held for 1s before the loop.
- **Output.** MP4 (H.264, 1080 px, CRF 18) for LinkedIn, decks and the site. GIF (720 px, 15 fps, 64 colors) for Slack and email. On LinkedIn post the MP4; it autoplays muted and stays sharp.

## Don't

- Rounded corners on any box, node, bar or tag.
- Organic blobs, waves, freeform or curved connectors, or curves a figure does not need (a Sankey flow band is the exception, not a license).
- Connectors with two or more bends, or junction squares on plain corners.
- Gradients, shadows, glows, glass, isometric 3D.
- Stock metaphors (shields, locks, lightbulbs, rockets), faces or hands. Person icons are fine.
- Third-party logos, customer names, or vendor marks.
- Stat-tile rows (big number over a mono caption) and dark evidence-panel mockups. Put the values on an axis instead.
- Status color as a fill or a series, or without its word. Emoji. Decorative copper or verdigris.

## Before it ships

1. Does it measure something or show a real mechanism?
2. Are all boxes square-cornered, with curves only in icons or where the figure needs them (Sankey flows), and does every connector run straight or with one bend?
3. Does copper only mark risk, verdigris only Isomer acting, and status color only a labelled tag?
4. Is every number sourced, and every unknown in [brackets]?
5. Does it still read with annotations off?
6. Is there exactly one idea?
7. Does each group of boxes form one rectangle, with no near-equal sizes?

## Known placeholders in the samples

- `st-04-window-to-act` and `window-to-act-1x1` assume 7 caught on arrival and 3 late in the Isomer lane; the pitch gives only the 70% total.
- `bl-06-fnol-not-day-1` uses `[N] days` and an arbitrary 9-day gap.
- `pl-02-claim-graph` uses an invented claim number, WC-2026-04417, and a 30-day clock.
