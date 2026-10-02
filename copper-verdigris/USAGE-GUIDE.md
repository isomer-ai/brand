# Copper Verdigris usage guide

Status: proposal. Companion to [`palette.json`](palette.json), [`tokens.css`](tokens.css) and the [illustration guide](ILLUSTRATION-GUIDE.md).

The illustration guide covers plates. This guide covers everything else: brand moments, product UI and email. It comes from taking the palette into the first web app and daily email built on it, where most of the mistakes below were made once.

## For agents

1. Decide the register first: is this surface a brand moment or the work? The rules differ, and most mistakes come from mixing them.
2. In product UI, build on the `--cv-ui-*` tokens in [`tokens.css`](tokens.css), not the raw colors. The dark theme then comes from one attribute.
3. In email, use the stacks and minimum sizes in `palette.json` under `email`, and design for the fallback fonts.
4. Run the checks at the bottom before you hand anything back.

## Two registers

Copper and verdigris do two jobs. Keep them on separate surfaces.

| Register | What the colors are | Where |
| --- | --- | --- |
| Brand | Identity. The patina story: copper becoming verdigris. | Logo and app icon, covers (decks, reports, blog headers, social cards), title and closing slides, event and print, one hero moment per marketing page |
| Signal | Verbs. Copper is risk; verdigris is action. | Plates, animations, product UI, email, and any page section that shows data or claims |

### Brand moments

- **One per view.** A page, screen or slide gets at most one brand moment. Two compete, and the second one reads as decoration.
- **No data inside.** Once a figure, table or product screen appears, color means something, and the brand moment ends.
- **The pair lives here, and only here.** In a brand moment copper and verdigris may sit together: verdigris as the field, copper as the smaller, brighter metal. It is the one place the "never a decorative pair" rule does not apply, because here the pair *is* the subject.
- **Pick the shade by ground.** On paper or white use copper deep `#9A5634` and verdigris deep `#2E6B68`. On ink or verdigris dark `#1F4F4C` fields use copper light `#E09C6B` and verdigris light `#8CC2BC`.
- **A hero headline word** may be copper deep when the page is about risk, or verdigris deep when it is about acting. Only the hero, only one word or phrase.

### The work

- **Copper appears only where something is risky.** If nothing on a screen is, the screen has no copper.
- **Verdigris appears only where something is being done, or can be.** In a figure that is Isomer acting; in a product it is what the reader can do.
- **Ink and grey carry every frame:** rules, panels, plates, tabs, chart bars, numbers, dates, eyebrows, the ruler.
- **The brand shows through form, not color.** Fustat, mono labels, square corners, the quiet ruler and the logo make a product screen ours. It does not need copper to look like Isomer.

## In an app

### Color

- **Copper is risk found or gaining ground:** high impact, rising, a verdict, a deadline, a figure that should worry the reader. Copper for the mark, copper dark `#8E4720` for text, because plain copper is 4.5:1 on white and only just passes.
- **Verdigris is what the reader can do:** links, hover, a selected filter or tab, Follow, form controls, focus rings, "what you can do" advice. Verdigris deep `#2E6B68` for text and outlines, because plain verdigris is 4.0:1 on white and fails as text.
- **"New" is not risk.** A new item gets an ink or outline tag unless the new thing is itself a risk.
- **Status stays status.** Oxide red only for failure or critical, always with its word. Cobalt for healthy or info, always with its word. Warning reuses copper. Never use status color as a category ("live", "current") or a chart series.
- **Selection is verdigris or ink, never copper.** The selected day in a chart, the active tab, the chosen filter are the reader acting.

### Surfaces

- **Content panels are white on paper, ruled with a hairline.** Rule `#DDDDDA` for panel borders, hairline `#E3E3E5` for grids and table rules. A 1px ink border on a panel is too harsh; keep ink for the one rule under the masthead.
- **No accent borders.** No left-border or top-border accent cards in copper or verdigris. Mark a part with a labelled 8px square instead.
- **No dark blocks behind prose.** Graphite is for screens of data and for the dark theme.

### Text

| Use | Light | On white | Dark | On graphite |
| --- | --- | --- | --- | --- |
| Headings | Ink `#141416` | 18.4:1 | White `#FFFFFF` | 10.8:1 |
| Running and secondary text | Body `#47474D` | 9.2:1 | Paper `#F6F6F5` | 10.0:1 |
| Meta: dates, sources, footers | Muted `#6E6E75` | 5.1:1 | On-graphite muted `#A4A9AA` | 4.6:1 |
| Risk text | Copper dark `#8E4720` | 6.8:1 | Copper light `#E09C6B` | 4.7:1 |
| Action text, links | Verdigris deep `#2E6B68` | 6.1:1 | Verdigris light `#8CC2BC` | 5.4:1 |

- **Body text is body, never muted.** Muted is for meta only. Text set in muted because it "feels secondary" is the most common contrast failure.
- **Never put `#A4A9AA` on white** (2.4:1). It exists for graphite.
- **Muted fails on section grey** (4.3:1). Text on section grey uses body.

### Type

- **Headlines in Fustat 800, sentence case, tracking about -0.035em.** Fustat is wide; condensed, all-caps headline habits from other faces don't carry over.
- **IBM Plex Mono, uppercase and tracked, for labels and counts only.** Never for sentences.

### Dark theme

Set `data-cv-theme="dark"` on `<html>` and every `--cv-ui-*` token swaps. The mapping, also in `palette.json` under `product.themes`:

| Token | Light | Dark |
| --- | --- | --- |
| `--cv-ui-ground` | Paper `#F6F6F5` | Graphite deep `#303435` |
| `--cv-ui-surface` | White `#FFFFFF` | Graphite `#3A3E3F` |
| `--cv-ui-rule` | Rule `#DDDDDA` | Graphite raised `#45494A` |
| `--cv-ui-heading` | Ink `#141416` | White `#FFFFFF` |
| `--cv-ui-text` | Body `#47474D` | Paper `#F6F6F5` |
| `--cv-ui-meta` | Muted `#6E6E75` | On-graphite muted `#A4A9AA` |
| `--cv-ui-signal` | Copper `#B4602F` | Copper light `#E09C6B` |
| `--cv-ui-action-text` | Verdigris deep `#2E6B68` | Verdigris light `#8CC2BC` |
| `--cv-ui-critical` | Oxide red `#B4232F` | Red light `#F08A92` |
| `--cv-ui-ok` | Cobalt `#2F5D99` | Cobalt light `#8FB4E3` |

Tints become graphite raised in dark. A copper tint on graphite reads muddy; the light copper text on a raised surface carries the meaning on its own.

### Apparatus

The ruler works under the navigation and over the footer only when it is quiet: grey ticks, about 70% opacity, no copper. Copper ticks are one more piece of decoration.

## The story pattern

Any analysis, alert or record reads in three labelled parts. The labels line up with the palette, so the reader learns the colors from the content.

| Part | Label | Marker | Holds |
| --- | --- | --- | --- |
| What's happening | Muted mono | None | The facts, neutrally |
| Why it matters | Copper dark mono | 8px copper square | The risk and its size |
| What you can do | Verdigris deep mono | 8px verdigris square | The action, or what Isomer already did |

When Isomer has already acted, the third label can read "What Isomer did". Keep the verdigris either way: it is action, whoever takes it.

## In email

- **Fonts mostly don't load** (the Gmail app, Outlook). Use the stacks and design for the fallback: Fustat falls back to Arial, so check that headlines still fit at Arial's width.
- **The mono stack needs Menlo and Consolas before Courier New.** Courier New alone renders thin and grey, and labels became illegible on iPhone Gmail.
- **Minimum sizes:** mono labels 10px, body 14px, meta 10px. Labels at 8 or 9px failed on phones.
- **Contrast:** body and secondary text in body `#47474D`. Muted only for the least important meta, at 10px or more. Never `#A4A9AA` or lighter on white. Footer text on section grey in body.
- **Gmail's dark mode inverts colors whatever the email declares.** Name positions, not shades, in captions ("the lower part of each bar", not "the darker part"). Prefer copper and verdigris marks, which survive inversion, over ink-versus-grey distinctions.
- **Glyphs:** arrows such as ↗ render as blue emoji tiles on iOS. Append the text variation selector (`&#8599;&#65038;`) or use a plain character.
- **Markers as characters.** Small sized table cells (a 7×7 square) render as tall bars in some apps. Draw a marker as `■` in copper or verdigris.
- **Layout:** one column, at most 600px, in the same order as the app: main content first, then the sidebar panels in the sidebar's order. Panel titles are mono labels in ink, with a quieter note or link at the right. Avoid narrow side-by-side meta cells; they wrap into stacks on a phone.
- **Controls:** the primary button is ink with white text. Links are verdigris deep.

| Email token | Value |
| --- | --- |
| Sans stack | `Fustat, Arial, Helvetica, sans-serif` |
| Mono stack | `'IBM Plex Mono', Menlo, Consolas, 'Courier New', monospace` |
| Ground / card / rule | Section grey `#ECECEA` / white / rule `#DDDDDA` |
| Heading / text / meta | Ink / body `#47474D` / muted `#6E6E75` |
| Link / button | Verdigris deep `#2E6B68` / ink fill, white text |
| Minimum sizes | Mono label 10px, body 14px, meta 10px |

## Porting an existing app

Swapping tokens one for one is how most of the mistakes above happened. The old palette's accent became copper, so copper landed on every number, eyebrow and badge, and verdigris disappeared. Map by meaning instead:

| Old token was used for | Map to |
| --- | --- |
| Brand accent: eyebrows, section labels, story and step numbers, index columns, a dot after the wordmark | Ink or muted. Not copper. |
| Selected, today, current, active | Verdigris deep, or ink |
| Links, hover, focus, controls | Verdigris deep |
| High, hot, rising, overdue, a verdict, a loss | Copper (mark) and copper dark (text) |
| Pending, invited, requested, teaching, new | Ink outline tag |
| Categorical series (one color per role or type) | Greys, with copper on the one series that is the risk |
| Live, current, healthy | Cobalt only if it is a status with its word; otherwise ink |
| "Faint" or secondary text | Body, unless it is meta |

After the port, count: if the copper token is used more than a few times as often as the verdigris token, copper is decorating.

## Do

- Decide the register before choosing a color.
- Keep one brand moment per view, and keep data out of it.
- Use `--cv-ui-*` tokens in product code so the dark theme works.
- Use copper dark and verdigris deep for text on light grounds; keep the base colors for marks.
- Label analysis with What's happening, Why it matters and What you can do.
- Write status with its word, every time.
- Rule panels with `#DDDDDA`; grid with `#E3E3E5`.
- In email, use the full font stacks and the minimum sizes, and check on an iPhone in the Gmail app.

## Don't

- Copper on a title slash, the rule under a title, a bar across a lead panel, chart bars, a tab underline or ruler ticks. That was the first pass of the app, and it read as decoration and pushed verdigris out of sight.
- Copper on eyebrows, section labels, story numbers or index columns.
- Copper for selection, "new", pending or invited.
- A 1px ink border on content panels.
- Left-border or top-border accent cards.
- Dark blocks behind prose.
- Running text in muted `#6E6E75`, or `#A4A9AA` anywhere on white.
- Status colors as categories or chart series.
- Copper and verdigris side by side outside a brand moment.
- In email: Courier New alone, labels under 10px, body under 14px, captions that name a shade, bare ↗ arrows, or sized empty cells as markers.

## Before it ships

1. Which register is each surface in, and is there at most one brand moment per view?
2. Does every copper element mark something risky? Would the screen still make sense if you removed the ones that don't?
3. Does every verdigris element mark something done or doable?
4. Is all running text body or darker, and all meta at least 10px?
5. Does the dark theme come from `--cv-ui-*` tokens, with light copper and light verdigris?
6. In email: fallback fonts checked, minimum sizes met, nothing that depends on a shade surviving inversion?
