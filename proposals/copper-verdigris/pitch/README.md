# Pitch (reference build)

A static rebuild of the [isomer.ai/pitch-patina](https://isomer.ai/pitch-patina) minisite that follows the Copper Verdigris [palette](../palette.json) and [illustration guide](../ILLUSTRATION-GUIDE.md). Use it as the worked example of the proposal on a full page. Like the rest of the proposal, it is not linked from the brand site and carries `noindex`.

Page: https://isomer-ai.github.io/brand/proposals/copper-verdigris/pitch/

The live minisite is the original Isomer pitch page with a runtime skin that swaps its colors for Copper Verdigris. The colors are right, but the shapes, type and charts are still the original page's. This build keeps the copy, sources, numbers and interactions (the inbox and claim graph, the X-ray, the window-to-act scenario, Model your book, shareable `#v=1` links) and changes how the page is drawn.

## What changed, by guide rule

| Guide rule | Live minisite | Reference build |
| --- | --- | --- |
| Radius 0 on every box, node, bar and tag | 10 to 22px cards, pill tags and buttons, rounded bars | Square everywhere |
| No gradients, shadows, glows or transparency stacks | Drop shadows on panels, glowing nodes and scan line, radial glow in the claim graph, gradient progress bar | Flat fills; 1px rules; dot grid in the claim graph |
| Graphite is for product screens | Graphite also behind the result, savings, benefits, deliverables, fee and Isomer cards | Graphite only on the inbox and the X-ray file |
| Right angles, at most one bend; junction squares at branch points | Claim graph connectors run diagonally from the center | Trunk-and-branch routing, vertical then horizontal, 5px junction squares |
| Curves only where the figure needs them | Loss chart is a Sankey with rounded bars and a gradient fade | Square bars, flat curved flow bands kept because the Sankey needs them, copper hatching on the at-risk volume |
| Markers are 8px squares | Round dots on the window track, rail and adjuster grid | Squares |
| Copper marks risk, verdigris marks Isomer acting | Verdigris on plaintiff vendor claims, funding amounts, source links and "flagged after entry" (rules and adjusters) | Copper or ink for plaintiff-side figures; neutral for rules and adjusters; verdigris only where Isomer acts or delivers |
| Red is a labelled status tag, used rarely | Red glow on the hit row's rail marker | No red; detected severity (critical, high, medium) stays copper |
| Values to scale on an axis, not stat tiles | Three big-number tiles in In production; bars without scales | Each figure measured: a log time axis for 30 minutes, grids for 7 in 10 and 1 in 16, axes under the severity and savings bars, payment bars scaled to the annual fee, a 100-cell strip for the 71% plaintiff share |
| No numbered section eyebrows | Contents numbered 01 to 08 | Unnumbered; plate codes (ST-03, ST-04 ...) tie figures to the story plates |
| No stock metaphors | Building, robot and megaphone icons on the problem cards | Removed |
| Unknowns as `[BRACKETED]` placeholders | Dashed rounded blanks | `[ ]` in verdigris |
| Animation: smoothstep, fade or draw on, nothing bounces or scales | Overshoot easing, scale-in nodes, bump and ping scales | Fades and draw-on only |
| Fustat for display and values, IBM Plex Mono for annotation | Geist and Geist Mono (the skin swaps Fustat out) | Fustat and IBM Plex Mono, from [`tokens.css`](../tokens.css) |

Headline accents follow the same split: copper where the phrase names risk ("buried in the file", "most of the loss"), verdigris where it names Isomer's outcome ("before the suit", "a point of combined ratio").

## Notes

- Colors come only from `palette.json`, through `../tokens.css`. The page has no other hex values except white and the copper hatch in the inline SVG.
- The logo is inlined from `logos/web/svg/isomer-logo-horiz-solid-dark.svg` and drawn in ink, because the logo files are still in the old palette.
- Figures are drawn from the page's own numbers, so they can differ from the sample story plates in `../illustrations/` (for example ST-03 there uses placeholder values).
- Everything is in `index.html`, with no build step. The calculator logic (`IsomerModel`) is the live page's, plus one field so the payment bars can be drawn to scale.
