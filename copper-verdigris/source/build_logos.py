"""Build ../logos/index.html, the logo board, from palette.json.   python3 build_logos.py"""
import html
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
LOGOS = os.path.join(ROOT, "logos")
pal = json.load(open(os.path.join(ROOT, "palette.json")))
logo = pal["registers"]["brand"]["logo"]
e = html.escape

LAYOUTS = [("logo-horiz", "Horizontal", "The default. Mastheads, slide corners, email headers, the site."),
           ("logo-vert", "Vertical", "Square and tall slots: covers, event signage, merchandise."),
           ("logomark", "Mark", "Small and square: app icon, favicon, avatar, slide footers.")]
COLORS = [("ink", "Ink", "For paper and white", "on-paper"), ("white", "White", "For ink and graphite", "on-ink")]


def png_size(path):
    with open(path, "rb") as f:
        f.read(16)
        return struct.unpack(">II", f.read(8))


def kb(path):
    return f"{os.path.getsize(path) / 1024:.0f} KB"


def card(lay, lay_name, color, color_name, ground, cls):
    name = f"isomer-{lay}-{color}"
    svg = f"svg/{name}.svg"
    png = f"png/{name}.png"
    w, h = png_size(os.path.join(LOGOS, png))
    return f'''<figure class="lg">
<div class="pv {cls}"><img src="{svg}" alt="Isomer {lay_name.lower()} logo, {color_name.lower()}" loading="lazy"></div>
<figcaption><div class="nm"><b>{lay_name} · {color_name}</b><span>{ground}</span></div>
<code>{name}</code>
<div class="dl"><a href="{svg}" download>SVG <i>{kb(os.path.join(LOGOS, svg))}</i></a><a href="{png}" download>PNG <i>{w} × {h} · {kb(os.path.join(LOGOS, png))}</i></a>
<button type="button" data-url="{svg}" aria-label="Copy the SVG link for {name}">Copy link</button></div></figcaption></figure>'''


rows = ""
for lay, lay_name, lay_use in LAYOUTS:
    cards = "".join(card(lay, lay_name, c, cn, g, cls) for c, cn, g, cls in COLORS)
    rows += f'<section class="row"><div class="rh"><h2>{lay_name}</h2><p>{lay_use}</p></div><div class="pair">{cards}</div></section>'

notes = "".join(f"<li>{e(n)}</li>" for n in logo["notes"])

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Isomer Logo Board</title>
<meta name="description" content="Black and white Isomer logos for the Copper Verdigris proposal, each downloadable on its own in SVG or PNG.">
<link rel="icon" type="image/svg+xml" href="svg/isomer-logomark-ink.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fustat:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<link rel="stylesheet" href="../tokens.css">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cv-paper);color:var(--cv-ink);font:400 16px/1.55 var(--cv-font);-webkit-font-smoothing:antialiased}}
a{{color:var(--cv-verdigris-deep)}}
code{{font-family:var(--cv-mono)}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 32px}}
.top{{border-bottom:1px solid var(--cv-ink);display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 0}}
.top img{{display:block;height:44px;width:auto;margin:-10px 0 -10px -12px}}
.top a.back{{font:500 11px/1.2 var(--cv-mono);letter-spacing:1.2px;text-transform:uppercase;color:var(--cv-muted);text-decoration:none}}
.top a.back:hover{{color:var(--cv-ink)}}
.ruler{{height:10px;opacity:.7;background:repeating-linear-gradient(90deg,var(--cv-muted) 0 1px,transparent 1px 8px) top left/100% 4px no-repeat,repeating-linear-gradient(90deg,var(--cv-muted) 0 1px,transparent 1px 40px) top left/100% 10px no-repeat}}
header.hd{{padding:48px 0 32px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;align-items:end}}
.eb{{font:500 11px/1.2 var(--cv-mono);letter-spacing:1.2px;text-transform:uppercase;color:var(--cv-muted)}}
h1{{font:800 clamp(36px,5vw,56px)/1 var(--cv-font);letter-spacing:-.035em;margin:12px 0 0}}
.lede{{margin:0;color:var(--cv-body);max-width:560px}}
.row{{display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;padding:28px 0;border-top:1px solid var(--cv-hairline)}}
.rh h2{{font:700 22px/1.2 var(--cv-font);letter-spacing:-.4px;margin:0 0 6px}}
.rh p{{margin:0;font-size:14px;color:var(--cv-body)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.lg{{margin:0;background:var(--cv-white);border:1px solid var(--cv-rule);display:flex;flex-direction:column}}
.pv{{height:240px;display:flex;align-items:center;justify-content:center;padding:20px}}
.pv img{{max-width:78%;max-height:100%;display:block}}
.on-paper{{background:var(--cv-paper);border-bottom:1px solid var(--cv-rule)}}
.on-ink{{background:var(--cv-ink)}}
figcaption{{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px}}
.nm{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}}
.nm b{{font:600 15px/1.3 var(--cv-font)}}
.nm span{{font:500 10.5px/1.2 var(--cv-mono);letter-spacing:1px;text-transform:uppercase;color:var(--cv-muted)}}
figcaption code{{font-size:12px;color:var(--cv-body)}}
.dl{{display:flex;flex-wrap:wrap;gap:8px;margin-top:2px}}
.dl a,.dl button{{display:inline-flex;align-items:baseline;gap:8px;border:1px solid var(--cv-ink);background:var(--cv-white);color:var(--cv-ink);padding:8px 12px;font:600 13px/1 var(--cv-font);text-decoration:none;cursor:pointer}}
.dl a:hover{{background:var(--cv-ink);color:var(--cv-white)}}
.dl a i{{font:400 11px/1 var(--cv-mono);font-style:normal;color:var(--cv-muted)}}
.dl a:hover i{{color:var(--cv-on-graphite-muted)}}
.dl button{{border-color:var(--cv-rule);color:var(--cv-verdigris-deep)}}
.dl button:hover{{border-color:var(--cv-verdigris-deep)}}
.dl a:focus-visible,.dl button:focus-visible{{outline:2px solid var(--cv-verdigris-deep);outline-offset:2px}}
.rules{{display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;padding:28px 0 56px;border-top:1px solid var(--cv-hairline)}}
.rules ul{{margin:0;padding-left:18px;color:var(--cv-body);font-size:15px;max-width:760px}}.rules li{{margin:6px 0}}
.dont{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:20px}}
.dont div{{background:var(--cv-white);border:1px solid var(--cv-rule);padding:14px;font-size:13.5px;color:var(--cv-body)}}
.dont b{{display:flex;align-items:center;gap:7px;font:500 10.5px/1 var(--cv-mono);letter-spacing:1px;text-transform:uppercase;color:var(--cv-copper-dark);margin-bottom:8px}}
.dont b i{{width:8px;height:8px;background:var(--cv-copper);display:block}}
footer{{border-top:1px solid var(--cv-ink);padding:20px 0 48px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font:500 11px/1.2 var(--cv-mono);letter-spacing:1.2px;text-transform:uppercase;color:var(--cv-muted)}}
footer a{{color:var(--cv-muted)}}
.toast{{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);background:var(--cv-ink);color:#fff;font:500 12px/1 var(--cv-mono);padding:12px 16px;opacity:0;transition:.2s;pointer-events:none}}
.toast.on{{opacity:1;transform:translateX(-50%)}}
@media (max-width:820px){{
 .wrap{{padding:0 16px}}
 header.hd,.row,.rules{{grid-template-columns:1fr;gap:12px}}
 .pair,.dont{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<div class="wrap">
<div class="top"><a href="../" aria-label="Copper Verdigris guide"><img src="svg/isomer-logo-horiz-ink.svg" alt="Isomer"></a><a class="back" href="../#brand-devices">&larr; Copper Verdigris guide</a></div>
<div class="ruler" aria-hidden="true"></div>
<header class="hd"><div><span class="eb">Copper Verdigris · Logo board</span><h1>Isomer logos</h1></div>
<p class="lede">Black and white logos for the Copper Verdigris palette, each shown on the ground it's made for. Every file has a transparent background, so the white logos can look blank until they're on a dark ground. Download one file at a time: SVG for screens and anything that scales, PNG where SVG isn't accepted.</p></header>
{rows}
<section class="rules"><div class="rh"><h2>Use</h2></div><div><ul>
<li>Ink on paper or white; white on ink or graphite. Never the color logos with this palette.</li>
{notes}
<li>The files already include the guideline's minimum clear space: about ½A around the horizontal logo and ⅓A beside the mark, where A is the mark's width. Don't crop it; give the logo more room where you can.</li></ul>
<div class="dont"><div><b><i></i>Don't</b>Recolor the logo copper, verdigris, or any color but ink and white.</div><div><b><i></i>Don't</b>Stretch, rotate, outline, or add a shadow or gradient.</div><div><b><i></i>Don't</b>Place the ink logo on ink or graphite, or the white logo on paper.</div></div></div></section>
<footer><span>Isomer · Copper Verdigris · proposal</span><a href="../../">Current brand site</a></footer>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const toast=document.getElementById('toast');let tt;
function say(m){{toast.textContent=m;toast.classList.add('on');clearTimeout(tt);tt=setTimeout(()=>toast.classList.remove('on'),1400)}}
document.querySelectorAll('button[data-url]').forEach(b=>b.addEventListener('click',()=>{{const u=new URL(b.dataset.url,location.href).href;
 try{{navigator.clipboard.writeText(u).then(()=>say('Link copied'),()=>say(u))}}catch(e){{say(u)}}}}));
</script>
</body>
</html>
'''
open(os.path.join(LOGOS, "index.html"), "w").write(page)
print("logos/index.html", len(page))
