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
         ("ILLUSTRATION-GUIDE.md", "The full illustration and animation rules, written for agents"),
         ("illustrations/index.json", "Every plate: id, title, family, size, and SVG / clean SVG / PNG paths"),
         ("pitch/", "Reference page: the palette and illustration rules applied to the full pitch; pitch/README.md lists every change"),
         ("source/plates.py", "Drawing primitives and every plate as a function; export.py writes the SVGs"),
         ("source/anim2.py", "Frame-by-frame animation renderer (cairosvg + ffmpeg)")]
fl = "".join(f'<li><a href="{f}"><code>{f}</code></a><span>{d}</span></li>' for f, d in files)

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
.top .brand{{font:600 15px/1 var(--cv-font);letter-spacing:-.2px}}
.top nav{{display:flex;gap:20px;flex-wrap:wrap}}
.top nav a,.eyebrow,.cap{{font:500 11px/1.2 var(--cv-mono);letter-spacing:1.2px;text-transform:uppercase;color:var(--cv-muted);text-decoration:none}}
.top nav a:hover{{color:var(--cv-ink)}}
.flag{{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--cv-copper);background:var(--cv-copper-tint);color:var(--cv-copper-dark);font:600 11px/1 var(--cv-mono);letter-spacing:1.2px;text-transform:uppercase;padding:7px 10px}}
.flag i{{width:7px;height:7px;background:var(--cv-copper)}}
header.hero{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:48px;align-items:center;padding:56px 0 56px}}
h1{{font:800 clamp(44px,6.4vw,84px)/.98 var(--cv-font);letter-spacing:-2.4px;margin:22px 0 22px;text-wrap:balance}}
h1 em{{font-style:normal;color:var(--cv-verdigris-deep)}}
h1 span{{color:var(--cv-copper)}}
h1 .cu{{color:var(--cv-copper-deep)}}
.hero-fig{{margin:0;border:1px solid var(--cv-ink);background:var(--cv-paper)}}
.hero-fig video{{display:block;width:100%;height:auto}}
.hero-fig figcaption{{border-top:1px solid var(--cv-ink);flex-direction:row;justify-content:space-between;gap:12px;padding:10px 12px}}
.topruler{{height:10px;background:repeating-linear-gradient(90deg,var(--cv-muted) 0 1px,transparent 1px 8px) top left/100% 4px no-repeat,repeating-linear-gradient(90deg,var(--cv-copper) 0 1px,transparent 1px 40px) top left/100% 10px no-repeat}}
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
.inaction{{margin-top:16px;border-top:3px solid var(--cv-verdigris)}}
.inaction .links{{margin-top:18px}}
.prs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));border-left:1px solid var(--cv-hairline);border-top:1px solid var(--cv-hairline)}}
.pr{{padding:18px 20px 22px;border-right:1px solid var(--cv-hairline);border-bottom:1px solid var(--cv-hairline);background:var(--cv-white)}}
.pr h4{{font:700 17px/1.25 var(--cv-font);margin:0 0 6px}}.pr p{{margin:0;font-size:14px;color:var(--cv-body)}}
.rules{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:24px}}
.rules .card h4{{font:600 11px/1 var(--cv-mono);letter-spacing:1.4px;text-transform:uppercase;margin:0 0 12px}}
.rules ul{{margin:0;padding-left:18px;font-size:14px;color:var(--cv-body)}}.rules li{{margin:4px 0}}
.do{{border-top:3px solid var(--cv-verdigris)}}.do h4{{color:var(--cv-verdigris-dark)}}
.dont{{border-top:3px solid var(--cv-copper)}}.dont h4{{color:var(--cv-copper-dark)}}
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
 .use-grid,.rules,.type{{grid-template-columns:1fr}}
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
<div class="top"><span class="brand">Isomer brand</span>
<nav aria-label="Sections"><a href="#palette">Palette</a><a href="#at-work">At work</a><a href="#illustration">Illustration</a><a href="#samples">Samples</a><a href="#animation">Animation</a><a href="#agents">For agents</a></nav></div>

<div class="topruler" aria-hidden="true"></div>
<header class="hero">
<div>
<span class="flag"><i></i>Proposal · not adopted · not linked from the brand site</span>
<h1><span class="cu">Copper</span> <span>signals.</span><br>Verdigris <em>acts.</em></h1>
<p class="lede">A proposed replacement for Isomer's blue and purple palette. Black, white and grey carry the page. Copper marks risk and the moment something is flagged. Verdigris, the patina copper becomes, marks Isomer acting on it. Graphite is reserved for product screens; oxide red and cobalt for status.</p>
<div class="links hero-cta"><a class="pri" href="pitch/">See it on a full page &rarr;</a><a href="ILLUSTRATION-GUIDE.md">Read the illustration guide</a></div>
<p class="hero-files"><span>Files</span><a href="palette.json">palette.json</a><a href="tokens.css">tokens.css</a><a href="illustrations/index.json">illustrations/index.json</a><a href="#agents">All files &darr;</a></p>
</div>
<figure class="hero-fig"><video src="animations/point-of-receipt-1x1.mp4" poster="animations/point-of-receipt-1x1-poster.png" autoplay muted loop playsinline preload="metadata" aria-label="Point of receipt animation: a buried deadline turns copper and Isomer acts"></video>
<figcaption><span>FIG. A1 · POINT OF RECEIPT</span><span>AN-01</span></figcaption></figure>
</header>

<section class="part" id="palette" aria-labelledby="h-pal">
<div class="ruler" aria-hidden="true"><span>CV-PAL</span></div>
<div class="part-h"><div><h2 id="h-pal">Palette</h2></div>
<p>Thirty colors in four families. Click any chip to copy its hex. Each chip shows its best text pairing and the contrast grade, so you can tell at a glance which colors can carry type.</p></div>
{fams}
</section>

<section class="part" id="at-work" aria-labelledby="h-work">
<div class="ruler" aria-hidden="true"><span>CV-USE</span></div>
<div class="part-h"><div><h2 id="h-work">At work</h2></div>
<p>Roughly how much of each appears on a page, how the pairs read on paper and on a graphite screen.</p></div>
<div class="ratio" role="img" aria-label="Approximate share: paper and section grey 77 percent, ink 8, graphite 8, copper 4, verdigris 3">
<i style="flex:62;background:#F6F6F5"></i><i style="flex:15;background:#ECECEA"></i><i style="flex:8;background:#141416"></i><i style="flex:8;background:#3A3E3F"></i><i style="flex:4;background:#B4602F"></i><i style="flex:3;background:#3F8A85"></i></div>
<div class="legend"><span><i style="background:#F6F6F5;border:1px solid #E3E3E5"></i>Paper and section grey</span><span><i style="background:#141416"></i>Ink</span><span><i style="background:#3A3E3F"></i>Graphite screens</span><span><i style="background:#B4602F"></i>Copper</span><span><i style="background:#3F8A85"></i>Verdigris</span></div>
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
<div class="card inaction"><span class="cap">In action · full page</span>
<p class="big">See the palette, the plates and the page rules working together.</p>
<p style="color:var(--cv-body);font-size:15px;max-width:72ch">A reference rebuild of the <a href="https://isomer.ai/pitch-patina">isomer.ai/pitch-patina</a> minisite: square corners, graphite only on product screens, orthogonal claim-graph connectors, figures drawn to scale, and copper and verdigris used only for risk and action. Its README lists every change against this guide.</p>
<div class="links"><a href="pitch/">Open the pitch page</a><a href="pitch/README.md">What changed</a></div>
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
<span class="k">curl</span> -s https://isomer-ai.github.io/brand/proposals/copper-verdigris/palette.json | jq '.families[].colors[] | {{token, hex}}'

<span class="c"># regenerate plates, then animations</span>
<span class="k">cd</span> proposals/copper-verdigris/source
./render_all.sh</pre>
</section>

<footer><span class="cap">Isomer · Copper Verdigris · proposal v1 · 2026-10</span><a class="cap" href="../../">Current brand site</a></footer>
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
