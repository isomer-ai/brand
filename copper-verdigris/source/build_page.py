"""Build ../index.html from palette.json and illustrations/index.json.   python3 build_page.py"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
pal = json.load(open(os.path.join(ROOT, "palette.json")))
plates = json.load(open(os.path.join(ROOT, "illustrations", "index.json")))
e = html.escape


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


def chip(c):
    h = c["hex"]
    dark = lum(h) < .35
    on_white = contrast(h, "#FFFFFF")
    on_ink = contrast(h, "#141416")
    best, ratio = ("white", on_white) if on_white >= on_ink else ("ink", on_ink)
    grade = "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "AA large" if ratio >= 3 else "decor"
    edge = " edge" if h in ("#FFFFFF", "#F6F6F5", "#ECECEA", "#E9F2F1") else ""
    return (f'<button type="button" class="chip{" lead" if c["primary"] else ""}" data-hex="{h}" aria-label="{e(c["name"])} {h}. Copy hex">'
            f'<span class="sw{edge}" style="background:{h};color:{"rgba(255,255,255,.8)" if dark else "rgba(20,20,22,.6)"}">'
            f'<span>rgb {", ".join(map(str, c["rgb"]))}</span></span>'
            f'<span class="meta"><b>{e(c["name"])}</b><code>{h}</code><span class="use">{e(c["use"])}</span>'
            f'<span class="ct">{grade} text vs {best} · {ratio:.1f}:1</span></span></button>')


fams = "".join(
    f'<section class="fam" id="{f["id"]}"><div class="fam-h"><h3>{e(f["title"])}</h3><p>{e(f["description"])}</p></div>'
    f'<div class="chips">{"".join(chip(c) for c in f["colors"])}</div></section>' for f in pal["families"])

groups = [("plate", "Plates", "Section features and stats for the site."), ("strip", "Strip", "Prefooter band."),
          ("glyph", "Playbook glyphs", "Card icons for Actions."), ("story", "Story", "One per section of the pitch narrative."),
          ("cover", "Blog covers", "Headers and social cards, one per post.")]
gal = ""
for fam, title, desc in groups:
    items = [p for p in plates if p["family"] == fam]
    cards = "".join(
        f'<figure class="pl {fam}"><a href="{p["svg"]}" aria-label="Open {e(p["title"])} SVG"><img src="{p["png_2x"]}" alt="{e(p["title"])}" '
        f'width="{p["width"]}" height="{p["height"]}" loading="lazy"></a><figcaption><b>{e(p["title"])}</b>'
        f'<span>{p["id"][:5].upper()} · {p["width"]}×{p["height"]}</span>'
        f'<span class="dl"><a href="{p["svg"]}">SVG</a><a href="{p["svg_clean"]}">Clean SVG</a><a href="{p["png_2x"]}">PNG</a></span></figcaption></figure>'
        for p in items)
    gal += f'<div class="gal-h"><h3>{title}</h3><p>{desc}</p></div><div class="gal {fam}">{cards}</div>'

anims = [("point-of-receipt-1x1", "Point of receipt", "1:1", "Every page read on arrival; the buried deadline turns copper, drops to a signal, and Isomer acts."),
         ("window-to-act-1x1", "Window to act", "1:1", "Ten high-risk claims, today vs with Isomer: 50% to 70% caught in time."),
         ("claim-graph-1x1", "Claim graph", "1:1", "Sources arrive, entities draw in on straight edges, risk surfaces, Isomer acts."),
         ("elastic-1x1", "Elastic", "1:1", "Landfall spikes volume 20x past adjuster capacity; Isomer coverage sweeps across."),
         ("point-of-receipt-16x9", "Point of receipt", "16:9", "Wide cut for decks and the site.")]
vids = "".join(
    f'<figure class="an{" wide" if r == "16:9" else ""}"><video src="animations/{n}.mp4" poster="animations/{n}-poster.png" autoplay muted loop playsinline preload="metadata" aria-label="{e(t)} animation"></video>'
    f'<figcaption><b>{e(t)}</b><span>{r} · MP4 + GIF</span><p>{e(d)}</p><span class="dl"><a href="animations/{n}.mp4">MP4</a><a href="animations/{n}.gif">GIF</a></span></figcaption></figure>'
    for n, t, r, d in anims)

principles = [("Figures, not illustrations", "Every plate encodes a real quantity or a real mechanism. If it reads the same with the labels removed, it's decoration."),
              ("Right angles, fewest bends", "Straight lines and sharp corners. Lay nodes on shared rows and columns so connectors run straight. Circles occasionally; curves only inside icons or where the figure needs them, like Sankey flows."),
              ("Color is a verb", "Neutrals draw the apparatus. Copper means risk was found or time ran out. Verdigris means Isomer acted. One meaning per color."),
              ("Show the source", "Every number traces to a source. Unknowns are [BRACKETED], never invented."),
              ("One idea per plate", "One comparison or one mechanism. Two headlines means two plates.")]
pr = "".join(f'<div class="pr"><h4>{a}</h4><p>{b}</p></div>' for a, b in principles)

files = [("palette.json", "Every color with hex, RGB, role, use and the semantic rules"), ("tokens.css", "CSS custom properties, prefixed --cv-, plus semantic aliases"),
         ("USAGE-GUIDE.md", "Brand moments vs the work, product UI in light and dark, email, porting an app"),
         ("ILLUSTRATION-GUIDE.md", "The full illustration and animation rules, written for agents"),
         ("logos/", "Logo board: black and white logos in SVG and PNG, one download at a time"),
         ("illustrations/index.json", "Every plate: id, title, family, size, and SVG / clean SVG / PNG paths"),
         ("../pitch-cv/", "Reference page: the palette and illustration rules applied to the full pitch; its README.md lists every change"),
         ("source/plates.py", "Drawing primitives and every plate as a function; export.py writes the SVGs"),
         ("source/anim2.py", "Frame-by-frame animation renderer (cairosvg + ffmpeg)")]
fl = "".join(f'<li><a href="{f}"><code>{f}</code></a><span>{d}</span></li>' for f, d in files)


hexof = {c["token"]: c["hex"] for f in pal["families"] for c in f["colors"]}
names = {c["token"]: c["name"] for f in pal["families"] for c in f["colors"]}
TEXTISH = {"heading", "text", "meta", "signal-text", "action-text", "critical", "ok", "focus"}
ROLE = {"ground": "Page ground", "surface": "Panels and cards", "surface-2": "Section bands, raised rows", "rule": "Panel borders",
        "grid": "Grid and table rules", "heading": "Headings", "text": "Running and secondary text", "meta": "Dates, sources, footers",
        "signal": "Risk marks", "signal-text": "Risk text", "signal-tint": "Risk fill", "action": "Action marks",
        "action-text": "Links, selection, controls", "action-tint": "Action fill", "critical": "Critical, with its word",
        "critical-tint": "Critical fill", "ok": "OK, with its word", "ok-tint": "OK fill", "focus": "Focus ring"}
th = pal["product"]["themes"]


def tok_cell(theme, key):
    t = th[theme][key]
    h = hexof[t]
    ratio = ""
    if key in TEXTISH:
        ratio = f'<span class="tr">{contrast(h, hexof[th[theme]["surface"]]):.1f}:1</span>'
    return f'<td><span class="tsw" style="background:{h}"></span>{e(names[t])} <code>{h}</code>{ratio}</td>'


tok_rows = "".join(f'<tr><td><code>--cv-ui-{k}</code><span class="trole">{ROLE[k]}</span></td>{tok_cell("light", k)}{tok_cell("dark", k)}</tr>' for k in th["light"])
tok_table = f'<div class="tbl"><table class="toks"><thead><tr><th>Token</th><th>Light</th><th>Dark</th></tr></thead><tbody>{tok_rows}</tbody></table></div>'

APP = """<div class="app"{attr}>
<div class="app-nav"><span class="app-logo" role="img" aria-label="Isomer"></span><span class="app-tabs"><a class="on">Signals</a><a>Claims</a><a>Actions</a></span><span class="app-me">JB</span></div>
<div class="app-ruler" aria-hidden="true"></div>
<div class="app-filters"><span class="app-lab">Filter</span><span class="f on">Attorney rep</span><span class="f">Deadlines</span><span class="f">All</span></div>
<article class="app-panel">
<div class="app-meta"><span>WC-[NNNN] · Received today · p. 4 of 12</span><span class="app-tag risk"><i></i>High impact</span></div>
<h4 class="app-h">Demand letter sets a 30-day window to settle within limits</h4>
<div class="story3">
<div><span class="lab">What's happening</span><p>Claimant's counsel sent a time-limited demand, buried on page 4 of a letter that arrived this morning.</p></div>
<div><span class="lab risk"><i></i>Why it matters</span><p>Missing the window can expose the policy limits. <b class="risk-t">29 days left.</b></p></div>
<div><span class="lab act"><i></i>What you can do</span><p>Calendar the deadline and assign defense counsel. <a href="#at-work">Open the claim</a></p></div>
</div>
<div class="app-foot"><span class="app-tag ok"><i></i>OK</span><span class="app-m">ClaimCenter synced 2 min ago</span><span class="follow">Follow</span></div>
</article>
<div class="app-chart"><div class="app-ch"><span class="app-lab">Time-limited demands · 8 weeks</span><span class="app-lab risk-t">Rising</span></div>
<div class="bars">{bars}</div></div>
</div>"""
_b = [3, 4, 3, 5, 4, 6, 8, 11]
bars = "".join(f'<i style="height:{v * 8}%"{" class=" + chr(34) + "up" + chr(34) if i >= 6 else ""}></i>' for i, v in enumerate(_b))
app_light = APP.format(attr="", bars=bars)
app_dark = APP.format(attr=' data-cv-theme="dark"', bars=bars)

MAIL = """<div class="mail"{attr}><div class="mail-card">
<div class="mail-top"><img class="mail-logo" src="logos/png/isomer-logo-horiz-ink.png" alt="Isomer" width="120" height="44"><span>Daily brief · 2 Oct</span></div>
<div class="mail-pt"><span>Needs attention · 3</span><a href="#at-work">View all</a></div>
<p class="mail-h">Demand letter sets a 30-day window to settle within limits</p>
<p class="mail-l">What's happening</p>
<p class="mail-p">Claimant's counsel sent a time-limited demand on page 4 of a letter received today.</p>
<p class="mail-l"><span class="cu">&#9632;</span> Why it matters</p>
<p class="mail-p">Missing the window can expose the policy limits. 29 days left.</p>
<p class="mail-l"><span class="ve">&#9632;</span> What you can do</p>
<p class="mail-p">Calendar the deadline and assign counsel. <a href="#at-work">Open the claim</a></p>
<span class="mail-btn">Open in Isomer &#8599;&#65038;</span>
</div><div class="mail-foot">You get this because you follow attorney-represented claims. <a href="#at-work">Manage alerts</a></div></div>"""
mail_light = MAIL.format(attr="")
mail_dark = MAIL.format(attr=' style="filter:invert(1) hue-rotate(180deg)"')

port = [("Brand accent: eyebrows, section labels, story and step numbers, index columns, the dot after a wordmark", "Ink or muted. Not copper."),
        ("Selected, today, current, active", "Verdigris deep, or ink"),
        ("Links, hover, focus, controls", "Verdigris deep"),
        ("High, hot, rising, overdue, a verdict, a loss", "Copper for the mark, copper dark for the text"),
        ("Pending, invited, requested, new", "An ink outline tag"),
        ("One color per category or role", "Grays, with copper on the one series that is the risk"),
        ("Live, current, healthy", "Cobalt only as a status with its word; otherwise ink"),
        ("Faint or secondary text", "Body, unless it is a date, source or footer")]
port_rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in port)


def dodont(do, dont):
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return (f'<div class="rules"><div class="card do"><h4><i></i>Do</h4><ul>{li(do)}</ul></div>'
            f'<div class="card dont"><h4><i></i>Don\'t</h4><ul>{li(dont)}</ul></div></div>')


app_dd = dodont(
    ["Put copper only where something is risky. If nothing on the screen is, the screen has no copper.",
     "Use verdigris deep for links, the selected filter, Follow, form controls and focus rings.",
     "Set risk text in copper dark and action text in verdigris deep; keep the base colors for marks.",
     "Rule panels with <code>#DDDDDA</code> and grids with <code>#E3E3E5</code>.",
     "Set running text in body <code>#47474D</code>.",
     "Build on <code>--cv-ui-*</code> tokens so <code>data-cv-theme=\"dark\"</code> works everywhere."],
    ["Copper on a title slash, the rule under a title, a bar across a lead panel, chart bars, a tab underline or ruler ticks. It reads as decoration and pushes verdigris out of sight.",
     "Copper on eyebrows, story numbers, index columns, “new” or “pending”.",
     "A 1px ink border around content panels; it is too harsh. Use the rule color.",
     "Left- or top-border accent cards, or dark blocks behind prose.",
     "Running text in muted <code>#6E6E75</code>, or <code>#A4A9AA</code> anywhere on white.",
     "Status color as a category or chart series."])
mail_dd = dodont(
    ["Use the full stacks: <code>Fustat, Arial, Helvetica</code> and <code>'IBM Plex Mono', Menlo, Consolas, 'Courier New'</code>. Design for the fallback.",
     "Keep mono labels at 10px or more and body at 14px or more.",
     "Set footer text on section gray in body <code>#47474D</code>.",
     "Name positions in captions (“the lower part of each bar”).",
     "Draw markers as characters: <span style=\"color:#B4602F\">&#9632;</span> in copper or verdigris.",
     "Lay out one column in the app's order; ink button, verdigris-deep links."],
    ["Courier New alone. It renders thin and gray and made labels illegible on iPhone Gmail.",
     "8 or 9px mono labels. They failed on phones.",
     "Captions that name a shade (“the darker part”). Gmail's dark mode inverts it anyway.",
     "Bare ↗ arrows. iOS turns them into blue emoji; append <code>&amp;#65038;</code>.",
     "Small sized table cells as markers. Some apps stretch them into tall bars.",
     "Narrow side-by-side meta cells. They wrap into stacks on a phone."])

DEV_MARK = {"oxidation-band": '<span class="dv-band"></span>', "short-oxidation-bar": '<span class="dv-short"></span>',
            "bar-and-pixel": '<span class="dv-bar"></span><span class="dv-px"></span>', "ruler": '<span class="dv-ruler"></span>',
            "ruler-and-band": '<span class="dv-ruler"></span><span class="dv-band"></span>'}


def dev_card(d):
    tiles = "".join(f'<div class="bt sm {g}">{DEV_MARK[d["id"]]}<span class="bt-e">Report</span><span class="bt-h">Built for insurance.</span></div>' for g in ("dk", "lt"))
    return (f'<figure class="dev"><div class="bpair">{tiles}</div><figcaption><b>{e(d["name"])}</b>'
            f'<p>{e(d["use"])}</p><span>{e(d["size"])}</span></figcaption></figure>')


devs = "".join(dev_card(d) for d in pal["registers"]["brand"]["devices"])

work_more = f"""
<div class="sub" id="registers"><h3>Two registers</h3><p>Copper and verdigris do two jobs, and they need separate surfaces. As <b>brand</b> they are identity, the patina story of copper becoming verdigris. In <b>the work</b> they are verbs. Most mistakes come from mixing the two: brand color spread into the work turns every number and label copper, and then copper no longer means risk.</p></div>
<div class="use-grid">
<div class="card"><span class="cap">Brand · ink and paper, with devices</span>
<div class="bpair"><div class="bt dk"><span class="dv-ruler"></span><img class="bt-logo" src="logos/svg/isomer-logo-horiz-white.svg" alt="Isomer"><span class="bt-e">Title slide</span><span class="bt-h">Built for insurance.</span><span class="dv-band"></span></div>
<div class="bt lt"><img class="bt-logo" src="logos/svg/isomer-logo-horiz-ink.svg" alt="Isomer"><span class="bt-e">Section slide</span><span class="bt-h">Where the loss is</span><span class="dv-short"></span></div></div>
<ul class="plain"><li>Ink or paper is the field. Copper is the metal; verdigris is only the patina trace at the end.</li>
<li>Covers, slides, mastheads, footers, social cards, event and print. Product screens carry no devices.</li>
<li>One colored device per view, in the frame, never touching data.</li>
<li>Light shades on ink, deep shades on paper.</li>
<li>Logos: ink on paper, white on ink. Download them one at a time from the <a href="logos/">logo board</a>.</li></ul></div>
<div class="card"><span class="cap">The work · verbs, sparingly</span>
<div class="worktile"><div><span class="wt-l">Open demands</span><b>14</b></div><div><span class="wt-l">Past window</span><b class="risk-t">2</b></div><div><span class="wt-l">Assigned</span><b>12</b></div><a href="#at-work">Review the two</a></div>
<ul class="plain"><li>Plates, animations, product UI, email, and any section that shows data.</li>
<li>Copper only where something is risky; verdigris only where something is done or can be.</li>
<li>Ink and gray carry every frame: rules, panels, tabs, chart bars, numbers, eyebrows, the ruler.</li>
<li>The brand shows through form here: Fustat, mono labels, square corners, the quiet ruler, the logo.</li></ul></div>
</div>

<div class="sub" id="brand-devices"><h3>Brand devices</h3><p>One system, used with discretion. Pick the device by context: the full ruler and band on a title slide, the short bar on the section slide after it, the bar and pixel in an email signature. Every band runs copper first, about 70 / 20 / 10, in flat segments. Sizes and rules are in <code>palette.json</code> under <code>registers.brand</code> and in the <a href="USAGE-GUIDE.md#brand-moments">usage guide</a>.</p></div>
<div class="devs">{devs}</div>
<div class="sub" id="in-an-app"><h3>In an app</h3><p>The same fragment on the light and dark themes. Nothing on it is copper except the risk: the impact tag, the deadline and the rising weeks. Verdigris marks what the reader can do: the selected filter, the link, Follow. Every color comes from a <code>--cv-ui-*</code> token, so the dark version is the same markup with <code>data-cv-theme="dark"</code>.</p></div>
<div class="use-grid">{app_light}{app_dark}</div>
<div class="story-key">
<div><span class="lab">What's happening</span><p>The facts, neutrally. Muted mono label, no marker.</p></div>
<div><span class="lab risk"><i></i>Why it matters</span><p>The risk and its size. Copper-dark label, 8px copper square.</p></div>
<div><span class="lab act"><i></i>What you can do</span><p>The action, or what Isomer already did. Verdigris-deep label, 8px verdigris square.</p></div>
</div>
<p class="note">The house pattern for any analysis, alert or record. The labels teach the reader the colors.</p>
<div class="rules">
<div class="card"><h4 class="rh">Color</h4><ul>
<li>Copper is risk found or gaining ground: high impact, rising, a verdict, a deadline. Copper for the mark, copper dark for text, because copper is only 4.5:1 on white.</li>
<li>Verdigris is what the reader can do. Verdigris deep for text and outlines, because verdigris is 4.0:1 on white and fails as text.</li>
<li>Selection, the active tab and “new” are not risk: verdigris or ink, never copper.</li>
<li>Status stays status. Oxide red for failure or critical, cobalt for healthy or info, always with the word. Warning reuses copper.</li></ul></div>
<div class="card"><h4 class="rh">Surfaces and type</h4><ul>
<li>Content panels are white on paper, ruled with <code>#DDDDDA</code>. Grids and table rules use hairline <code>#E3E3E5</code>.</li>
<li>Running text in body <code>#47474D</code>; muted only for dates, sources and footers. Muted fails on section gray (4.3:1).</li>
<li>Headlines in Fustat 800, sentence case, tracking about −0.035em. Fustat is wide; don't bring condensed all-caps habits.</li>
<li>Plex Mono, uppercase and tracked, for labels and counts only. The ruler stays gray and quiet.</li>
<li>Groups of boxes form one rectangle on a modular grid: shared outer edges, rows at one height, near-equal sizes made equal.</li></ul></div>
</div>
{tok_table}
<p class="note">Ratios are each text token against its theme's surface. Tints become graphite raised in dark: a copper tint on graphite reads muddy, and the light text carries the meaning alone.</p>
{app_dd}

<div class="sub" id="in-email"><h3>In email</h3><p>Mail clients mostly ignore web fonts and many recolor the message, so email is designed for the fallback. Below is the same story as a daily brief, set the way most clients render it, in Arial and Menlo. On the right is roughly what Gmail's dark mode does to it: the copper and verdigris markers survive, while ink-versus-gray contrast flattens.</p></div>
<div class="use-grid mails"><figure class="mailfig">{mail_light}<figcaption><span>As sent · Arial, Menlo</span></figcaption></figure><figure class="mailfig">{mail_dark}<figcaption><span>Gmail dark mode · approximate inversion</span></figcaption></figure></div>
<div class="tbl"><table class="toks"><thead><tr><th>Email</th><th>Value</th></tr></thead><tbody>
<tr><td>Sans stack</td><td><code>Fustat, Arial, Helvetica, sans-serif</code></td></tr>
<tr><td>Mono stack</td><td><code>'IBM Plex Mono', Menlo, Consolas, 'Courier New', monospace</code></td></tr>
<tr><td>Minimum sizes</td><td>Mono labels 10px · body 14px · meta 10px</td></tr>
<tr><td>Text</td><td>Headings ink · body and secondary <code>#47474D</code> · least important meta <code>#6E6E75</code> at 10px or more · never <code>#A4A9AA</code> on white</td></tr>
<tr><td>Ground · card · rule</td><td>Section gray <code>#ECECEA</code> · white · <code>#DDDDDA</code>. Footer text on section gray in <code>#47474D</code></td></tr>
<tr><td>Links · button</td><td>Verdigris deep <code>#2E6B68</code> · ink fill with white text</td></tr>
<tr><td>Layout</td><td>One column, 600px max, in the app's order: main content, then the sidebar panels. Panel titles as ink mono labels with a quieter link at the right.</td></tr>
</tbody></table></div>
{mail_dd}

<div class="sub" id="porting"><h3>Porting an existing app</h3><p>Swapping the old tokens one for one is how most of these mistakes happen. The old accent becomes copper, copper lands on every number, eyebrow and badge, and verdigris disappears. Map by meaning instead. When you're done, count: if the copper token is used many times as often as the verdigris one, copper is decorating.</p></div>
<div class="tbl"><table class="toks"><thead><tr><th>The old color was doing</th><th>Use</th></tr></thead><tbody>{port_rows}</tbody></table></div>
<p class="note">The full rules, with checks to run before shipping, are in <a href="USAGE-GUIDE.md">USAGE-GUIDE.md</a>.</p>
"""

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Copper Verdigris · Isomer palette proposal</title>
<meta name="description" content="Proposal: Copper Verdigris palette, illustration rules, sample plates and animations for Isomer.">
<link rel="alternate" type="application/json" href="palette.json" title="Copper Verdigris palette">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fustat:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<link rel="stylesheet" href="tokens.css">
<style>
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--cv-paper);color:var(--cv-ink);font:400 16px/1.55 var(--cv-font);-webkit-font-smoothing:antialiased}}
a{{color:var(--cv-verdigris-deep)}}a:hover{{color:var(--cv-verdigris-dark)}}
code,.mono{{font-family:var(--cv-mono)}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 32px}}
.top{{border-bottom:1px solid var(--cv-ink);display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 0}}
.top .brand{{display:block}}.top .brand img{{display:block;height:44px;width:auto;margin:-10px 0 -10px -12px}}
.top nav{{display:flex;gap:20px;flex-wrap:wrap}}
.top nav a,.eyebrow,.cap{{font:500 11px/1.2 var(--cv-mono);letter-spacing:1.2px;text-transform:uppercase;color:var(--cv-muted);text-decoration:none}}
.top nav a:hover{{color:var(--cv-ink)}}
.flag{{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--cv-ink);background:var(--cv-white);color:var(--cv-ink);font:600 11px/1 var(--cv-mono);letter-spacing:1.2px;text-transform:uppercase;padding:7px 10px}}
.flag i{{width:7px;height:7px;background:var(--cv-ink)}}
header.hero{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:48px;align-items:center;padding:56px 0 56px}}
h1{{font:800 clamp(44px,6.4vw,84px)/.98 var(--cv-font);letter-spacing:-2.4px;margin:22px 0 22px;text-wrap:balance}}
h1 em{{font-style:normal;color:var(--cv-verdigris-deep)}}
h1 span{{color:var(--cv-copper)}}
h1 .cu{{color:var(--cv-copper-deep)}}
.hero-fig{{margin:0;border:1px solid var(--cv-ink);background:var(--cv-paper)}}
.hero-fig video{{display:block;width:100%;height:auto}}
.hero-fig figcaption{{border-top:1px solid var(--cv-ink);flex-direction:row;justify-content:space-between;gap:12px;padding:10px 12px}}
.topruler{{height:10px;opacity:.7;background:repeating-linear-gradient(90deg,var(--cv-muted) 0 1px,transparent 1px 8px) top left/100% 4px no-repeat,repeating-linear-gradient(90deg,var(--cv-muted) 0 1px,transparent 1px 40px) top left/100% 10px no-repeat}}
.lede{{max-width:760px;font-size:19px;color:var(--cv-body);margin:0}}
.links{{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}}
.links a{{border:1px solid var(--cv-ink);padding:10px 14px;font:500 12px/1 var(--cv-mono);letter-spacing:.8px;text-decoration:none;color:var(--cv-ink);background:var(--cv-white)}}
.links a:hover{{background:var(--cv-ink);color:var(--cv-white)}}
.links a.pri{{background:var(--cv-ink);color:var(--cv-white)}}
.links a.pri:hover{{background:var(--cv-verdigris-deep);border-color:var(--cv-verdigris-deep)}}
.hero-files{{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;margin-top:18px;font:500 11.5px/1.4 var(--cv-mono);letter-spacing:.4px}}
.hero-files span{{text-transform:uppercase;letter-spacing:1px;color:var(--cv-muted)}}
.hero-files a{{color:var(--cv-ink);text-decoration:none;border-bottom:1px solid var(--cv-hairline)}}
.hero-files a:hover{{border-bottom-color:var(--cv-ink)}}
section.part{{padding:0 0 56px}}
.ruler{{position:relative;height:22px;border-top:1px solid var(--cv-ink);margin-bottom:28px;
 background:repeating-linear-gradient(90deg,var(--cv-muted) 0 1px,transparent 1px 8px) top left/100% 4px no-repeat,
 repeating-linear-gradient(90deg,var(--cv-ink) 0 1px,transparent 1px 40px) top left/100% 9px no-repeat}}
.ruler span{{position:absolute;right:0;top:12px;font:500 10px/1 var(--cv-mono);letter-spacing:1.2px;color:var(--cv-muted)}}
.part-h{{display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;margin-bottom:32px}}
.part-h h2{{font:700 32px/1.1 var(--cv-font);letter-spacing:-.6px;margin:0;text-wrap:balance}}
.part-h p{{margin:0;color:var(--cv-body);max-width:720px}}
.fam{{display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;padding:28px 0;border-top:1px solid var(--cv-hairline)}}
.fam-h h3{{font:600 17px/1.25 var(--cv-font);margin:0 0 8px}}
.fam-h p{{margin:0;font-size:14px;color:var(--cv-muted)}}
.chips{{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:12px}}
.chip{{all:unset;cursor:pointer;display:flex;flex-direction:column;background:var(--cv-white);border:1px solid var(--cv-hairline);text-align:left}}
.chip:hover{{border-color:var(--cv-ink)}}
.chip:focus-visible{{outline:2px solid var(--cv-verdigris);outline-offset:2px}}
.chip.lead{{grid-column:span 2}}
.sw{{height:88px;display:flex;align-items:flex-end;padding:8px 10px;font:500 10px/1 var(--cv-mono);letter-spacing:.4px}}
.chip.lead .sw{{height:120px}}
.sw.edge{{border-bottom:1px solid var(--cv-hairline)}}
.meta{{display:flex;flex-direction:column;gap:2px;padding:10px 12px 12px}}
.meta b{{font:600 14px/1.3 var(--cv-font)}}
.meta code{{font-size:12px;color:var(--cv-muted)}}
.meta .use{{font-size:12.5px;line-height:1.4;color:var(--cv-body);margin-top:4px}}
.meta .ct{{font:500 10px/1.3 var(--cv-mono);color:var(--cv-muted);letter-spacing:.3px;margin-top:6px}}
.ratio{{display:flex;height:40px;border:1px solid var(--cv-hairline)}}
.ratio i{{display:block}}
.legend{{display:flex;flex-wrap:wrap;gap:16px;margin:12px 0 28px;font:500 11px/1 var(--cv-mono);color:var(--cv-muted);letter-spacing:.6px;text-transform:uppercase}}
.legend span{{display:inline-flex;align-items:center;gap:6px}}.legend i{{width:10px;height:10px;display:inline-block}}
.use-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}
.card{{padding:24px;border:1px solid var(--cv-hairline);background:var(--cv-white)}}
.card.dark{{background:var(--cv-graphite);border-color:var(--cv-graphite-deep);color:#fff}}
.card .cap{{display:block;margin-bottom:14px}}
.card.dark .cap{{color:var(--cv-on-graphite-muted)}}
.scr{{position:relative;padding-top:34px}}
.scr .scan{{position:absolute;left:0;right:0;top:0;height:14px;border-bottom:1px solid var(--cv-graphite-raised);
 background:repeating-linear-gradient(90deg,var(--cv-on-graphite-muted) 0 1px,transparent 1px 8px) top left/100% 4px no-repeat}}
.scr .scan::after{{content:"";position:absolute;top:0;bottom:-400px;left:28%;width:2px;background:var(--cv-verdigris-light);opacity:.55}}
.scr{{overflow:hidden}}
.type{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px}}
.type .card p{{margin:0}}
.spec-d{{font:800 44px/1 var(--cv-font);letter-spacing:-1.2px}}
.spec-m{{font:500 13px/1.6 var(--cv-mono);letter-spacing:1px;text-transform:uppercase}}
.big{{font:600 24px/1.25 var(--cv-font);letter-spacing:-.4px;margin:0 0 16px}}
.row{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:14px;margin-top:8px}}
.dots{{display:inline-flex;gap:4px}}.dots i{{width:10px;height:10px;display:block}}
.tag{{font:600 10px/1 var(--cv-mono);letter-spacing:1px;text-transform:uppercase;padding:5px 7px;border:1px solid}}
.st{{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--cv-hairline);margin-top:8px;font-size:14px}}
.st .tag{{display:inline-flex;align-items:center;gap:6px}}.st .tag i{{width:6px;height:6px;display:block}}
.card.dark .st{{border-color:var(--cv-graphite-raised);background:var(--cv-graphite-raised)}}
.inaction{{margin-top:16px}}
.inaction .links{{margin-top:18px}}
.prs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));border-left:1px solid var(--cv-hairline);border-top:1px solid var(--cv-hairline)}}
.pr{{padding:18px 20px 22px;border-right:1px solid var(--cv-hairline);border-bottom:1px solid var(--cv-hairline);background:var(--cv-white)}}
.pr h4{{font:700 17px/1.25 var(--cv-font);margin:0 0 6px}}.pr p{{margin:0;font-size:14px;color:var(--cv-body)}}
.rules{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:24px}}
.rules .card h4{{font:600 11px/1 var(--cv-mono);letter-spacing:1.4px;text-transform:uppercase;margin:0 0 12px}}
.rules ul{{margin:0;padding-left:18px;font-size:14px;color:var(--cv-body)}}.rules li{{margin:4px 0}}
.rules h4{{display:flex;align-items:center;gap:8px}}.rules h4 i{{width:8px;height:8px;display:block}}
.do h4{{color:var(--cv-verdigris-deep)}}.do h4 i{{background:var(--cv-verdigris)}}
.dont h4{{color:var(--cv-copper-dark)}}.dont h4 i{{background:var(--cv-copper)}}
.rules h4.rh{{color:var(--cv-ink)}}
.sub{{display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;margin:56px 0 20px;padding-top:28px;border-top:1px solid var(--cv-hairline)}}
.sub h3{{font:700 22px/1.2 var(--cv-font);letter-spacing:-.4px;margin:0}}.sub p{{margin:0;color:var(--cv-body);max-width:720px}}
.note{{font-size:13.5px;color:var(--cv-body);margin:12px 0 0}}
ul.plain{{margin:16px 0 0;padding-left:18px;font-size:14px;color:var(--cv-body)}}ul.plain li{{margin:4px 0}}
.bpair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.bt{{position:relative;aspect-ratio:16/10;padding:16px 16px 22px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;border:1px solid var(--cv-rule)}}
.bt.dk{{background:var(--cv-ink);border-color:var(--cv-ink);color:#fff;--m1:var(--cv-copper-light);--m2:var(--cv-verdigris-light);--band:var(--cv-band-on-ink);--tk:var(--cv-on-graphite-muted)}}
.bt.lt{{background:var(--cv-paper);color:var(--cv-ink);--m1:var(--cv-copper-deep);--m2:var(--cv-verdigris-deep);--band:var(--cv-band-on-paper);--tk:var(--cv-muted)}}
.bt-e{{font:500 9.5px/1 var(--cv-mono);letter-spacing:1.1px;text-transform:uppercase;color:var(--tk);position:relative;padding-top:4px}}
.bt-h{{font:800 22px/1.02 var(--cv-font);letter-spacing:-.6px;max-width:14ch;position:relative;margin-bottom:12px}}
.bt-logo{{position:absolute;right:8px;top:4px;height:32px;width:auto}}
.bt.sm .bt-h{{font-size:17px;max-width:11ch}}
.dv-band{{position:absolute;left:0;right:0;bottom:0;height:8px;background:var(--band)}}
.dv-short{{position:absolute;left:16px;bottom:16px;width:52px;height:4px;background:var(--band)}}
.dv-bar{{position:absolute;left:16px;bottom:16px;width:34px;height:4px;background:var(--m1)}}
.dv-px{{position:absolute;left:54px;bottom:16px;width:4px;height:4px;background:var(--m2)}}
.dv-ruler{{position:absolute;left:0;right:0;top:0;height:6px;opacity:.7;background:repeating-linear-gradient(90deg,var(--tk) 0 1px,transparent 1px 8px) top left/100% 3px no-repeat,repeating-linear-gradient(90deg,var(--tk) 0 1px,transparent 1px 40px) top left/100% 6px no-repeat}}
.devs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.dev{{padding:12px}}.dev figcaption{{padding:12px 2px 2px}}
.worktile{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid var(--cv-rule);background:var(--cv-white)}}
.worktile>div{{padding:14px;border-right:1px solid var(--cv-hairline)}}.worktile>div:nth-child(3){{border-right:0}}
.worktile b{{display:block;font:800 28px/1.1 var(--cv-font);letter-spacing:-.8px;margin-top:6px}}
.worktile a{{grid-column:1/-1;border-top:1px solid var(--cv-hairline);padding:10px 14px;font-size:14px;font-weight:600}}
.wt-l,.app-lab{{font:500 10px/1.2 var(--cv-mono);letter-spacing:1px;text-transform:uppercase;color:var(--cv-muted)}}
.risk-t{{color:var(--cv-ui-signal-text)!important}}
.app{{background:var(--cv-ui-ground);color:var(--cv-ui-text);border:1px solid var(--cv-ui-rule);padding:0 18px 18px;font-size:14px;min-width:0}}
.app .app-lab{{color:var(--cv-ui-meta)}}
.app-nav{{display:flex;align-items:center;gap:18px;border-bottom:1px solid var(--cv-ui-rule);height:48px}}
.app-logo{{display:block;width:104px;height:38px;margin-left:-10px;background:var(--cv-ui-heading);-webkit-mask:url(logos/svg/isomer-logo-horiz-ink.svg) left center/contain no-repeat;mask:url(logos/svg/isomer-logo-horiz-ink.svg) left center/contain no-repeat}}
.app-tabs{{display:flex;gap:16px;height:100%}}.app-tabs a{{display:flex;align-items:center;color:var(--cv-ui-meta);font-weight:600;font-size:13.5px;border-bottom:2px solid transparent;text-decoration:none}}
.app-tabs a.on{{color:var(--cv-ui-heading);border-bottom-color:var(--cv-ui-heading)}}
.app-me{{margin-left:auto;font:500 10px/1 var(--cv-mono);letter-spacing:1px;border:1px solid var(--cv-ui-rule);padding:6px;color:var(--cv-ui-meta)}}
.app-ruler{{height:8px;opacity:.7;background:repeating-linear-gradient(90deg,var(--cv-ui-meta) 0 1px,transparent 1px 8px) top left/100% 4px no-repeat}}
.app-filters{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:12px 0}}
.f{{font:500 11px/1 var(--cv-mono);letter-spacing:.6px;padding:6px 8px;border:1px solid var(--cv-ui-rule);color:var(--cv-ui-text);background:var(--cv-ui-surface)}}
.f.on{{border-color:var(--cv-ui-action-text);color:var(--cv-ui-action-text);background:var(--cv-ui-action-tint)}}
.app-panel{{background:var(--cv-ui-surface);border:1px solid var(--cv-ui-rule);padding:16px}}
.app-meta{{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font:500 10.5px/1.3 var(--cv-mono);letter-spacing:.6px;color:var(--cv-ui-meta)}}
.app-tag{{display:inline-flex;align-items:center;gap:6px;font:600 10px/1 var(--cv-mono);letter-spacing:1px;text-transform:uppercase;padding:4px 6px;border:1px solid}}
.app-tag i{{width:6px;height:6px;display:block}}
.app-tag.risk{{color:var(--cv-ui-signal-text);border-color:var(--cv-ui-signal);background:var(--cv-ui-signal-tint)}}.app-tag.risk i{{background:var(--cv-ui-signal)}}
.app-tag.ok{{color:var(--cv-ui-ok);border-color:var(--cv-ui-ok);background:var(--cv-ui-ok-tint)}}.app-tag.ok i{{background:var(--cv-ui-ok)}}
.app-h{{font:800 19px/1.2 var(--cv-font);letter-spacing:-.035em;color:var(--cv-ui-heading);margin:10px 0 14px}}
.story3{{display:grid;gap:12px}}.story3 p,.story-key p{{margin:4px 0 0;color:var(--cv-ui-text)}}
.lab{{display:inline-flex;align-items:center;gap:7px;font:500 10.5px/1 var(--cv-mono);letter-spacing:1px;text-transform:uppercase;color:var(--cv-ui-meta)}}
.lab i{{width:8px;height:8px;display:block}}
.lab.risk{{color:var(--cv-ui-signal-text)}}.lab.risk i{{background:var(--cv-ui-signal)}}
.lab.act{{color:var(--cv-ui-action-text)}}.lab.act i{{background:var(--cv-ui-action)}}
.app a{{color:var(--cv-ui-action-text);font-weight:600}}
.app .app-tabs a{{color:var(--cv-ui-meta)}}.app .app-tabs a.on{{color:var(--cv-ui-heading)}}
.app-foot{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:14px;padding-top:12px;border-top:1px solid var(--cv-ui-grid)}}
.app-m{{font-size:12.5px;color:var(--cv-ui-meta)}}
.follow{{margin-left:auto;font:600 13px/1 var(--cv-font);padding:8px 12px;border:1px solid var(--cv-ui-action-text);color:var(--cv-ui-action-text)}}
.app-chart{{margin-top:12px;background:var(--cv-ui-surface);border:1px solid var(--cv-ui-rule);padding:12px 16px}}
.app-ch{{display:flex;justify-content:space-between}}
.bars{{display:flex;align-items:flex-end;gap:6px;height:72px;margin-top:10px;border-bottom:1px solid var(--cv-ui-heading)}}
.bars i{{flex:1;background:var(--cv-ui-meta);opacity:.55}}.bars i.up{{background:var(--cv-ui-signal);opacity:1}}
.story-key{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:16px;padding:16px;border:1px solid var(--cv-rule);background:var(--cv-white);font-size:14px}}
.tbl{{overflow-x:auto;margin-top:20px}}
table.toks{{width:100%;border-collapse:collapse;background:var(--cv-white);border:1px solid var(--cv-rule);font-size:13.5px}}
.toks th{{text-align:left;font:500 10.5px/1.2 var(--cv-mono);letter-spacing:1px;text-transform:uppercase;color:var(--cv-muted);padding:10px 12px;border-bottom:1px solid var(--cv-rule)}}
.toks td{{padding:8px 12px;border-bottom:1px solid var(--cv-hairline);vertical-align:top;color:var(--cv-body)}}
.toks code{{font-size:12px;color:var(--cv-ink)}}
.tsw{{display:inline-block;width:12px;height:12px;border:1px solid rgba(20,20,22,.15);vertical-align:-2px;margin-right:6px}}
.tr{{margin-left:8px;font:500 10.5px/1 var(--cv-mono);color:var(--cv-muted)}}
.trole{{display:block;font-size:12px;color:var(--cv-muted)}}
.mailfig{{border:0;background:none}}
.mailfig figcaption{{padding:8px 0 0}}
.mail{{background:#ECECEA;padding:20px 16px;font-family:Arial,Helvetica,sans-serif}}
.mail-card{{background:#fff;max-width:600px;margin:0 auto;padding:20px 20px 22px}}
.mail-top{{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #141416;padding-bottom:10px}}
.mailfig img.mail-logo{{display:block;width:120px;height:44px;background:none;margin:-12px 0 -12px -12px}}
.mail-top b{{font:700 22px/1 Arial,Helvetica,sans-serif;letter-spacing:-1px;color:#141416}}
.mail-top span,.mail-pt span,.mail-l{{font:400 10.5px/1.4 Menlo,Consolas,'Courier New',monospace;letter-spacing:.8px;text-transform:uppercase}}
.mail-top span{{color:#6E6E75}}
.mail-pt{{display:flex;justify-content:space-between;margin:16px 0 8px;padding-bottom:6px;border-bottom:1px solid #DDDDDA}}
.mail-pt span{{color:#141416}}.mail-pt a{{font-size:12px;color:#2E6B68}}
.mail-h{{font:700 17px/1.3 Arial,Helvetica,sans-serif;color:#141416;margin:0 0 10px}}
.mail-l{{color:#47474D;margin:12px 0 2px}}.mail-l .cu{{color:#B4602F}}.mail-l .ve{{color:#3F8A85}}
.mail-p{{font:400 14px/1.6 Arial,Helvetica,sans-serif;color:#47474D;margin:0}}.mail-p a{{color:#2E6B68}}
.mail-btn{{display:inline-block;margin-top:16px;background:#141416;color:#fff;font:700 14px/1 Arial,Helvetica,sans-serif;padding:12px 16px}}
.mail-foot{{max-width:600px;margin:12px auto 0;font:400 12px/1.5 Arial,Helvetica,sans-serif;color:#47474D}}.mail-foot a{{color:#47474D}}
.gal-h{{display:flex;align-items:baseline;gap:16px;margin:40px 0 16px;flex-wrap:wrap}}
.gal-h h3{{font:600 20px/1.2 var(--cv-font);margin:0}}.gal-h p{{margin:0;color:var(--cv-muted);font-size:14px}}
.gal{{display:grid;gap:16px}}
.gal.plate{{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}}
.gal.strip{{grid-template-columns:1fr}}
.gal.glyph{{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}}
.gal.story{{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}}
.gal.cover{{grid-template-columns:repeat(auto-fill,minmax(400px,1fr))}}
figure{{margin:0;background:var(--cv-white);border:1px solid var(--cv-hairline);display:flex;flex-direction:column}}
figure img,figure video{{display:block;width:100%;height:auto;background:var(--cv-paper)}}
figure > a{{display:block;border-bottom:1px solid var(--cv-hairline)}}
figcaption{{padding:10px 12px 12px;display:flex;flex-direction:column;gap:3px}}
figcaption b{{font:600 14px/1.3 var(--cv-font)}}
figcaption span{{font:500 10.5px/1.3 var(--cv-mono);color:var(--cv-muted);letter-spacing:.4px}}
figcaption p{{margin:4px 0 0;font-size:13.5px;color:var(--cv-body)}}
.dl{{display:flex;gap:12px;margin-top:6px}}.dl a{{font:500 11px/1 var(--cv-mono);letter-spacing:.6px}}
.anims{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px}}
.an.wide{{grid-column:1/-1}}
.an.wide video{{max-height:640px;object-fit:contain}}
.files{{list-style:none;margin:0;padding:0;border-top:1px solid var(--cv-hairline)}}
.files li{{display:grid;grid-template-columns:280px minmax(0,1fr);gap:24px;padding:12px 0;border-bottom:1px solid var(--cv-hairline);font-size:14px;color:var(--cv-body)}}
.files code{{font-size:13px}}
pre{{background:var(--cv-graphite);color:#fff;padding:16px 18px;overflow:auto;font:400 13px/1.6 var(--cv-mono)}}
pre .c{{color:var(--cv-on-graphite-muted)}}pre .k{{color:var(--cv-verdigris-light)}}
footer{{border-top:1px solid var(--cv-ink);padding:20px 0 48px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}
.toast{{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);background:var(--cv-ink);color:#fff;font:500 12px/1 var(--cv-mono);padding:12px 16px;opacity:0;transition:.2s;pointer-events:none}}
.toast.on{{opacity:1;transform:translateX(-50%)}}
@media (max-width:820px){{
 .wrap{{padding:0 16px}}
 .part-h,.fam,header.hero{{grid-template-columns:1fr;gap:12px}}
 .use-grid,.rules,.type,.story-key,.sub{{grid-template-columns:1fr}}
 .devs{{grid-template-columns:1fr}}
 .sub{{gap:8px}}
 .chip.lead{{grid-column:span 1}}
 .files li{{grid-template-columns:1fr;gap:4px}}
 .gal.cover,.gal.story{{grid-template-columns:1fr}}
 .top nav{{display:none}}
}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
</style>
</head>
<body>
<div class="wrap">
<div class="top"><a class="brand" href="../" aria-label="Isomer brand site"><img src="logos/svg/isomer-logo-horiz-ink.svg" alt="Isomer" height="44"></a>
<nav aria-label="Sections"><a href="#palette">Palette</a><a href="#at-work">At work</a><a href="#in-an-app">App &amp; email</a><a href="#illustration">Illustration</a><a href="#samples">Samples</a><a href="#animation">Animation</a><a href="#agents">For agents</a></nav></div>

<div class="topruler" aria-hidden="true"></div>
<header class="hero">
<div>
<span class="flag"><i></i>Proposal · not adopted · not linked from the brand site</span>
<h1><span class="cu">Copper</span> <span>signals.</span><br>Verdigris <em>acts.</em></h1>
<p class="lede">A proposed replacement for Isomer's blue and purple palette. Black, white and gray carry the page. Copper marks risk and the moment something is flagged. Verdigris, the patina copper becomes, marks Isomer acting on it. Graphite is reserved for product screens; oxide red and cobalt for status.</p>
<div class="links hero-cta"><a class="pri" href="../pitch-cv/">See it on a full page &rarr;</a><a href="ILLUSTRATION-GUIDE.md">Illustration guide</a><a href="USAGE-GUIDE.md">Usage guide</a></div>
<p class="hero-files"><span>Files</span><a href="palette.json">palette.json</a><a href="tokens.css">tokens.css</a><a href="logos/">Logo board</a><a href="illustrations/index.json">illustrations/index.json</a><a href="#agents">All files &darr;</a></p>
</div>
<figure class="hero-fig"><video src="animations/point-of-receipt-1x1.mp4" poster="animations/point-of-receipt-1x1-poster.png" autoplay muted loop playsinline preload="metadata" aria-label="Point of receipt animation: a buried deadline turns copper and Isomer acts"></video>
<figcaption><span>FIG. A1 · POINT OF RECEIPT</span><span>AN-01</span></figcaption></figure>
</header>

<section class="part" id="palette" aria-labelledby="h-pal">
<div class="ruler" aria-hidden="true"><span>CV-PAL</span></div>
<div class="part-h"><div><h2 id="h-pal">Palette</h2></div>
<p>{sum(len(f['colors']) for f in pal['families'])} colors in four families. Click any chip to copy its hex. Each chip shows its best text pairing and the contrast grade, so you can tell at a glance which colors can carry type.</p></div>
{fams}
</section>

<section class="part" id="at-work" aria-labelledby="h-work">
<div class="ruler" aria-hidden="true"><span>CV-USE</span></div>
<div class="part-h"><div><h2 id="h-work">At work</h2></div>
<p>Roughly how much of each appears on a page, how the pairs read on paper and on a graphite screen, and how to use them in brand moments, in an app and in email.</p></div>
<div class="ratio" role="img" aria-label="Approximate share: paper and section gray 77 percent, ink 8, graphite 8, copper 4, verdigris 3">
<i style="flex:62;background:#F6F6F5"></i><i style="flex:15;background:#ECECEA"></i><i style="flex:8;background:#141416"></i><i style="flex:8;background:#3A3E3F"></i><i style="flex:4;background:#B4602F"></i><i style="flex:3;background:#3F8A85"></i></div>
<div class="legend"><span><i style="background:#F6F6F5;border:1px solid #E3E3E5"></i>Paper and section gray</span><span><i style="background:#141416"></i>Ink</span><span><i style="background:#3A3E3F"></i>Graphite screens</span><span><i style="background:#B4602F"></i>Copper</span><span><i style="background:#3F8A85"></i>Verdigris</span></div>
<div class="use-grid">
<div class="card"><span class="cap">On paper</span>
<p class="big">Catching these claims in time is <span style="color:#9A5634">a point of combined ratio</span></p>
<div class="row"><span class="dots"><i style="background:#2E6B68"></i><i style="background:#2E6B68"></i><i style="background:#3F8A85"></i></span>flagged in time<span class="dots" style="margin-left:12px"><i style="background:#B4602F"></i><i style="background:#B4602F"></i></span>too late</div>
<div class="st"><span class="tag" style="color:#234878;border-color:#2F5D99;background:#E3ECF7"><i style="background:#2F5D99"></i>OK</span>All 214 open claims checked today</div>
<div class="st"><span class="tag" style="color:#8E4720;border-color:#B4602F;background:#F2DCCB"><i style="background:#B4602F"></i>Warning</span>Reserve review due on 6 claims</div>
<div class="st"><span class="tag" style="color:#8F1B25;border-color:#B4232F;background:#F8DEE0"><i style="background:#B4232F"></i>Critical</span>EEOC response deadline in 2 days</div>
</div>
<div class="card dark scr"><div class="scan" aria-hidden="true"></div><span class="cap">On a graphite screen · Day 23 demand letter</span>
<div class="row"><span class="tag" style="color:#E09C6B;border-color:#E09C6B">Critical</span><b>Spoliation risk</b><span class="mono" style="color:#A4A9AA;font-size:12px">p. 9</span></div>
<div class="row"><span class="tag" style="color:#8CC2BC;border-color:#8CC2BC">Act</span>Litigation hold drafted</div>
<div class="st"><span class="tag" style="color:#8FB4E3;border-color:#8FB4E3"><i style="background:#8FB4E3"></i>OK</span>ClaimCenter sync healthy</div>
<div class="st"><span class="tag" style="color:#E09C6B;border-color:#E09C6B"><i style="background:#E09C6B"></i>Warning</span>3 documents still OCR-ing</div>
<div class="st"><span class="tag" style="color:#F08A92;border-color:#F08A92"><i style="background:#F08A92"></i>Critical</span>Mailbox connector disconnected</div>
</div>
</div>
<div class="type">
<div class="card"><span class="cap">Display and values · Fustat</span><p class="spec-d">$10.0M <span style="color:var(--cv-copper)">d23</span></p><p style="margin-top:12px;color:var(--cv-body);font-size:14px">The current Isomer brand face, kept on purpose. Bold and tight for headlines; 600 for the one hero value on a plate.</p></div>
<div class="card"><span class="cap">Annotation · IBM Plex Mono</span><p class="spec-m">Fig. 04 · Immediate · manual triage d23<br><span style="color:var(--cv-copper-dark)">TLD · ATT-3 · p.4</span> → <span style="color:var(--cv-verdigris-dark)">ACT · deadline calendared</span></p><p style="margin-top:12px;color:var(--cv-body);font-size:14px">Uppercase, tracked, small. Labels, axes, plate codes and captions.</p></div>
</div>
{work_more}
<div class="card inaction"><span class="cap">In action · full page</span>
<p class="big">The Isomer pitch for commercial claims leaders, drawn in Copper Verdigris.</p>
<ul style="margin:0;padding-left:18px;color:var(--cv-body);font-size:15px;max-width:76ch">
<li>A live inbox and claim graph on a graphite screen: messages arrive, facts branch off the claim, risks turn copper and actions land in verdigris.</li>
<li>An X-ray of four claim files (EPL, GL, auto, WC) with a scroll-driven scan line and a claim-graph rail.</li>
<li>A Sankey of where the loss is, with copper hatching on claims that have an attorney.</li>
<li>A window-to-act chart and savings model that recompute from Model your book, with shareable links.</li>
<li>Production results as measured figures: a log time axis, square grids, and bars on axes instead of stat tiles.</li>
<li>Rulers, plate codes and the scan line carried into the page UI, and an appendix on plaintiff AI and its funding.</li>
</ul>
<div class="links"><a class="pri" href="../pitch-cv/">Open the pitch page &rarr;</a></div>
</div>
</section>

<section class="part" id="illustration" aria-labelledby="h-ill">
<div class="ruler" aria-hidden="true"><span>CV-ILL</span></div>
<div class="part-h"><div><h2 id="h-ill">Illustration</h2></div>
<p>Figures, not illustrations. Plates are drawn like instrument readouts: rectilinear, measured and labelled. The full rules, with construction specs and a pre-ship checklist, are in <a href="ILLUSTRATION-GUIDE.md">ILLUSTRATION-GUIDE.md</a>.</p></div>
<div class="prs">{pr}</div>
<div class="rules">
<div class="card do"><h4>Do</h4><ul>
<li>Pick the form from the claim: compare, bars; time, an axis; flow, routed boxes; share, stacked or a grid.</li>
<li>Put the number where the eye lands, in the color of its meaning.</li>
<li>Use real vocabulary: TLD, CRN, CMS entry, d23, p.4.</li>
<li>Use red and cobalt the way the app does: one labelled status tag, rarely.</li>
<li>Use person icons (circle head, curved shoulders) for claimants, counsel and adjusters.</li>
<li>Arrange boxes as one rectangle on a modular grid; make near-equal sizes equal.</li>
</ul></div>
<div class="card dont"><h4>Don't</h4><ul>
<li>Rounded corners on any box, node, bar or tag.</li>
<li>Blobs, waves, curved connectors, or curves the figure does not need.</li>
<li>Connectors with two or more bends.</li>
<li>Gradients, shadows, glows, isometric 3D, stock metaphors.</li>
<li>Status color as a fill or series, or without its word.</li>
</ul></div>
</div>
</section>

<section class="part" id="samples" aria-labelledby="h-sam">
<div class="ruler" aria-hidden="true"><span>CV-SAM</span></div>
<div class="part-h"><div><h2 id="h-sam">Samples</h2></div>
<p>Thirty-two plates covering the homepage, the pitch story and every blog post. Each comes as an annotated SVG, a clean SVG for web placement and a 2x PNG. Some carry placeholder values, listed at the end of the guide.</p></div>
{gal}
</section>

<section class="part" id="animation" aria-labelledby="h-ani">
<div class="ruler" aria-hidden="true"><span>CV-ANI</span></div>
<div class="part-h"><div><h2 id="h-ani">Animation</h2></div>
<p>The same plates rendered frame by frame. Three or four beats, each with a caption; smoothstep easing; elements fade or draw on; color changes carry the story. 8 to 10 seconds with a one-second hold. Post the MP4 on LinkedIn; use the GIF in Slack and email.</p></div>
<div class="anims">{vids}</div>
</section>

<section class="part" id="agents" aria-labelledby="h-ag">
<div class="ruler" aria-hidden="true"><span>CV-AGT</span></div>
<div class="part-h"><div><h2 id="h-ag">For agents</h2></div>
<p>Everything on this page comes from files in this folder, each at a stable URL. Read <code>palette.json</code> for values and meaning, and the guide before drawing.</p></div>
<ul class="files">{fl}</ul>
<pre><span class="c"># palette values and semantics</span>
<span class="k">curl</span> -s https://isomer-ai.github.io/brand/copper-verdigris/palette.json | jq '.families[].colors[] | {{token, hex}}'

<span class="c"># regenerate plates, then animations</span>
<span class="k">cd</span> copper-verdigris/source
./render_all.sh</pre>
</section>

<footer><span class="cap">Isomer · Copper Verdigris · proposal v1 · 2026-10</span><a class="cap" href="../">Current brand site</a></footer>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const toast=document.getElementById('toast');let tt;
function say(m){{toast.textContent=m;toast.classList.add('on');clearTimeout(tt);tt=setTimeout(()=>toast.classList.remove('on'),1400)}}
document.querySelectorAll('.chip').forEach(b=>b.addEventListener('click',()=>{{const h=b.dataset.hex;
 try{{navigator.clipboard.writeText(h).then(()=>say('Copied '+h),()=>say(h))}}catch(e){{say(h)}}}}));
</script>
</body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(page)
print("index.html", len(page))
