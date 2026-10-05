# Pitch

The long-form Isomer pitch for heads of claims at commercial carriers and TPAs, drawn in the Copper Verdigris [palette](../copper-verdigris/palette.json) and [illustration guide](../copper-verdigris/ILLUSTRATION-GUIDE.md). The live version is [isomer.ai/pitch-patina](https://isomer.ai/pitch-patina). Like the rest of the proposal, this page is not linked from the brand site and carries `noindex`.

Page: <https://isomer-ai.github.io/brand/pitch-cv/>

Next moves are in [`TODO.md`](TODO.md).

## The Story

The plaintiff side has industrialized: litigation funding, plaintiff AI and mass claimant advertising. The loss concentrates in the few claims that get a lawyer, and the warning signs for those claims arrive early but buried in attachments and long scans. Today's flags come from rules and adjusters working on claims-system data, so they fire after the claim is keyed in. Isomer reads every inbound message as it lands, so the handler knows while the deadline can still be met and before a suit is filed. Catching high-risk claims in time instead of late is worth about a point of combined ratio on a commercial book, the same as 12% premium growth with none of the capital or trade-offs. The buyer proves it on their own claims in a 4-week assessment, then pays 10% of the savings it targets, mostly contingent on a year of results.

Hero: "Find the claims that become the loss, the moment they arrive." Stage tags: Understand, Detect, Act.

## Beats

Each beat is one section of the page, in order: threat, where the loss is, mechanism, proof, value, perspective, the ask, price, close, then backup.

1. Hero. A live inbox for one EPL claim: messages arrive over 36 days, facts branch into a claim graph, risks turn copper, and a Detect/Act ticker shows each flag and the action taken. It ends on a combined litigation risk and the litigation team alerted.
2. The problem: "The other side has capital, AI, and a playbook." Litigation funding ($16.5B in commercial funds), plaintiff AI (10,000 cases a week on one platform) and claimant recruiting ($2.6B on legal ads in 2024). The result: 23 to 34% of booked losses in commercial auto and GL from legal system abuse beyond inflation, with settlements growing faster than verdicts. Who pays: households, policyholders and claimants.
3. Where the loss is: "A few claims become most of the loss." A Sankey for commercial auto: 30% of claims have an attorney and carry 87% of loss and LAE. The same pattern across GL, WC and liability.
4. X-ray: "Warning signs arrive early, buried in the file." A scroll-driven read of one claim file, message by message, showing what was detected and what was done. Tabs for EPL (a real, anonymized finding), GL premises, commercial auto and WC (representative).
5. In production: "The flag lands before the suit." Seven weeks of reading every new claim at a large commercial carrier: a 30-minute median from email to the handler's alert, 7 in 10 critical or high flags before any suit, 1 in 16 new liability claims carrying a critical deadline. A $500,000 limits demand flagged on part 1 of 16. Every flag cites its page and the handler decides.
6. The value: "Catching these claims in time is a point of combined ratio." The window to act: where high-risk claims are first flagged today (mostly after entry or too late) versus with Isomer (mostly on arrival). The savings scenario: $3.9M lower defense cost plus $6.1M lower settlements on a $1B book, one point off the combined ratio.
7. Perspective: "What one point of combined ratio is worth." Three ways to get a point: grow the book 12% (slow, needs capital), cut about 80 adjusters (painful), or catch risk in time (fast, nothing to unwind).
8. The assessment: "In 4 weeks, see which claims will drive your loss." Each assumption on the page is replaced by the buyer's own number, measured from their closed and live claims.
9. Pricing: "Priced at 10% of the savings we target." Assessment at $50K per $500M of premium, then 20% of the fee at signing (assessment credited), 20% in production and 60% at year end, paid only if they continue.
10. Close: "Which claims team would you want to run this with?" Security and deployment chips, book a time or email.
11. Appendix. A: six common concerns checked against data. B: plaintiff AI vendors' own claims on speed, scale and value. C: who is funding plaintiff AI ($775M+ across six startups).

## Model Your Book

The value, perspective and pricing sections recompute from twelve inputs (premium, loss ratio, defense cost share, high-risk share of loss and defense, caught in time today and with Isomer, the three in-time effects, growth per point, and adjuster cost) and write them to a shareable `#v=1&...` link. Presets cover $1B and $500M commercial, commercial auto, GL, WC and a TPA. The math is in `IsomerModel` inside `index.html`:

```text
losses  = premium × loss ratio
Δ       = caught with Isomer − caught today
defense = losses × defense share × high-risk defense share × Δ × (avoid suit + (1 − avoid suit) × cheaper defense)
settle  = losses × high-risk loss share × Δ × lower settlements
points  = (defense + settle) / premium × 100
fee     = 10% × (defense + settle)
```

## Design Notes

How the page applies the illustration guide, compared with the live minisite.


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
| Fustat for display and values, IBM Plex Mono for annotation | Geist and Geist Mono (the skin swaps Fustat out) | Fustat and IBM Plex Mono, from [`tokens.css`](../copper-verdigris/tokens.css) |

Headline accents follow the same split: copper where the phrase names risk ("buried in the file", "most of the loss"), verdigris where it names Isomer's outcome ("before the suit", "a point of combined ratio").

## Build Notes

- Colors come only from `palette.json`, through `../copper-verdigris/tokens.css`. The page has no other hex values except white and the copper hatch in the inline SVG.
- The logo is inlined from `logos/web/svg/isomer-logo-horiz-solid-dark.svg` and drawn in ink, because the logo files are still in the old palette.
- Figures are drawn from the page's own numbers, so they can differ from the sample story plates in `../copper-verdigris/illustrations/` (for example ST-03 there uses placeholder values).
- Everything is in `index.html`, with no build step. The calculator logic (`IsomerModel`) is the live page's, plus one field so the payment bars can be drawn to scale.
