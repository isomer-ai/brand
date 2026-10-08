"""Build the hidden illustrations page from the isomer.ai site repo.

    python3 scripts/build_illustrations.py [path/to/www-isomer]

Copies every illustration, Isomer icon and background pattern from
www-isomer/client/src/assets into illustrations/, records where each one is
used on the site, and writes illustrations/index.json and illustrations/index.html.
The page carries noindex and is not linked from the brand site, brand.json or llms.txt.
"""
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "illustrations"
PAGES = "https://isomer-ai.github.io/brand/illustrations/"
WWW = Path(sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/repos/www-isomer")).resolve()
ASSETS = WWW / "client" / "src" / "assets"
SRC = WWW / "client" / "src"

# Group: (source folder, published folder, title, description)
GROUPS = [
    ("illustrations", "svg", "Illustrations", "Spot and hero illustrations from isomer.ai."),
    ("icons", "icons", "Icons", "Signal category and capability icons, drawn on a 24px grid."),
    ("patterns", "patterns", "Patterns", "Cross patterns that frame page heroes and sections."),
]
# Other companies' marks live in the site's icons folder too; they are not ours to publish.
THIRD_PARTY = {"gmail-icon", "linkedin-icon", "microsoft-icon"}
TITLES = {"40-percentage-of-adjuser-time": "40% of adjuster time", "soc-2": "SOC 2", "404": "404 page",
          "isomer-approach-1": "Isomer approach 1", "isomer-approach-2": "Isomer approach 2",
          "isomer-approach-3": "Isomer approach 3", "no-ai-training": "No AI training",
          "fnol-intake": "FNOL intake", "bad-faith-exposure": "Bad-faith exposure",
          "cross-claim-patterns": "Cross-claim patterns", "time-limited-demand": "Time-limited demand"}


def title(stem):
    if stem in TITLES:
        return TITLES[stem]
    t = re.sub(r"-icon$", "", stem).replace("-", " ")
    return t[:1].upper() + t[1:]


def view_box(svg):
    m = re.search(r'viewBox="([\d.\s-]+)"', svg)
    if not m:
        return None, None
    _, _, w, h = (float(v) for v in m.group(1).split())
    return round(w), round(h)


def size_class(group, w):
    if group != "illustrations":
        return None
    if w >= 400:
        return "Hero · 480"
    if w >= 300:
        return "Band · 320"
    if w >= 200:
        return "Feature · 240"
    if w >= 140:
        return "Card · 160"
    return "Small · 80"


def used_on(group, stem):
    """Site pages that reference the asset, from a grep of the site source."""
    needle = f"{group}/{stem}.svg"
    r = subprocess.run(["rg", "-l", "--fixed-strings", needle, str(SRC), "-g", "!assets/**"],
                       capture_output=True, text=True)
    pages = set()
    for line in r.stdout.splitlines():
        p = Path(line).relative_to(SRC).with_suffix("")
        parts = [x for x in p.parts if x not in ("pages", "components", "data", "-components")]
        name = "/".join(parts)
        name = re.sub(r"/(hero|index)$", "", name)
        if name in ("platform-apa", "platform/agentic-process-automation"):
            name = "platform/agentic-process-automation"
        pages.add(name or "home")
    return sorted(pages)


def build():
    if not ASSETS.is_dir():
        sys.exit(f"Not found: {ASSETS}")
    if OUT.exists():
        for sub in ("svg", "icons", "patterns"):
            shutil.rmtree(OUT / sub, ignore_errors=True)
    items = []
    for src, dst, _, _ in GROUPS:
        (OUT / dst).mkdir(parents=True, exist_ok=True)
        for f in sorted((ASSETS / src).glob("*.svg")):
            stem = f.stem
            if src == "icons" and stem in THIRD_PARTY:
                continue
            svg = f.read_text()
            if re.search(r"<script|<foreignObject|href=\"https?:", svg, re.I):
                sys.exit(f"Refusing {f}: script, foreignObject or external reference")
            shutil.copyfile(f, OUT / dst / f.name)
            w, h = view_box(svg)
            items.append({
                "id": stem, "group": src, "title": title(stem),
                "width": w, "height": h, "size_class": size_class(src, w),
                "used_on": used_on(src, stem),
                "dark_preview": stem.endswith("-light"),
                "path": f"{dst}/{f.name}", "url": PAGES + f"{dst}/{f.name}",
            })
    # Drawn in this repo by scripts/draw_illustrations.py; not on isomer.ai yet.
    for f in sorted((OUT / "new").glob("*.svg")):
        svg = f.read_text()
        w, h = view_box(svg)
        items.append({
            "id": f.stem, "group": "new",
            "title": html.unescape(m.group(1)) if (m := re.search(r"<title>(.*?)</title>", svg)) else title(f.stem),
            "width": w, "height": h, "size_class": size_class("illustrations", w),
            "used_on": [], "new": True, "generated_by": "Claude (Anthropic AI)", "dark_preview": False,
            "path": f"new/{f.name}", "url": PAGES + f"new/{f.name}",
        })
    commit = subprocess.run(["git", "-C", str(WWW), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    manifest = {
        "name": "Isomer illustrations",
        "base_url": PAGES,
        "source": {"repo": "www-isomer", "path": "client/src/assets", "commit": commit},
        "synced": datetime.date.today().isoformat(),
        "groups": [{"id": s, "title": t, "description": d, "folder": o} for s, o, t, d in GROUPS] + [
            {"id": "new", "title": "Generated by Claude", "folder": "new",
             "description": "AI-generated by Claude (Anthropic) in the isomer.ai style, for topics the site doesn't cover yet. Not drawn by a designer and not on isomer.ai."}],
        "count": len(items),
        "items": items,
    }
    (OUT / "index.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (OUT / "index.html").write_text(page(manifest))
    print(f"illustrations/: {len(items)} assets from www-isomer@{commit}")


def card(it):
    e = html.escape
    pages = it["used_on"]
    used = ", ".join(pages) if pages else ("Generated by Claude · not on isomer.ai" if it.get("new") else "Not used on the site")
    shown = used if len(pages) <= 4 else ", ".join(pages[:3]) + f" and {len(pages) - 3} more"
    tags = [it["size_class"]] if it["size_class"] else []
    if it.get("new"):
        tags.extend(["New", "AI-generated", "Claude"])
    elif not it["used_on"]:
        tags.append("Unused")
    search = " ".join([it["id"], it["title"], used, *tags]).lower()
    return (
        f'<figure class="card{" on-dark" if it["dark_preview"] else ""}{" ai" if it.get("new") else ""}" data-group="{it["group"]}" '
        f'data-size="{e(it["size_class"] or "")}" data-unused="{"1" if not it["used_on"] and not it.get("new") else "0"}" data-q="{e(search)}">'
        f'<a class="pv" href="{e(it["path"])}" aria-label="Open {e(it["title"])} SVG">'
        f'<img src="{e(it["path"])}" alt="{e(it["title"])}" width="{it["width"]}" height="{it["height"]}" loading="lazy"></a>'
        f'<figcaption>{"<span class=ai-tag>Generated by Claude</span>" if it.get("new") else ""}<b>{e(it["title"])}</b><code>{e(it["id"])}.svg</code>'
        f'<span class="meta">{it["width"]} × {it["height"]}{" · " + e(it["size_class"]) if it["size_class"] else ""}</span>'
        f'<span class="used{" none" if not it["used_on"] else ""}" title="{e(used)}">{e(shown)}</span>'
        f'<span class="acts"><a href="{e(it["path"])}" download>Download SVG</a>'
        f'<button type="button" data-url="{e(it["url"])}">Copy URL</button></span></figcaption></figure>'
    )


def page(m):
    e = html.escape
    sections = ""
    for g in m["groups"]:
        its = [i for i in m["items"] if i["group"] == g["id"]]
        sections += (f'<section class="grp" id="{g["id"]}" data-group="{g["id"]}"><div class="grp-h"><h2>{e(g["title"])}</h2>'
                     f'<p>{e(g["description"])} {len(its)} files.</p></div>'
                     f'<div class="grid {g["id"]}">{"".join(card(i) for i in its)}</div></section>')
    sizes = sorted({i["size_class"] for i in m["items"] if i["size_class"]}, key=lambda s: -int(s.split("· ")[1]))
    chips = '<button type="button" data-f="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-f="{e(s)}" aria-pressed="false">{e(s)}</button>' for s in sizes) + \
        '<button type="button" data-f="icons" aria-pressed="false">Icons</button>' \
        '<button type="button" data-f="patterns" aria-pressed="false">Patterns</button>' \
        '<button type="button" data-f="new" aria-pressed="false">Generated by Claude</button>' \
        '<button type="button" data-f="unused" aria-pressed="false">Unused</button>'
    n_ill = sum(1 for i in m["items"] if i["group"] == "illustrations")
    n_new = sum(1 for i in m["items"] if i["group"] == "new")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Isomer Illustrations</title>
<meta name="description" content="Every illustration, icon and pattern from isomer.ai, as SVG.">
<link rel="stylesheet" href="../tokens.css">
<style>
:root{{color-scheme:light;--ink:var(--isomer-blue);--muted:var(--isomer-blue-70);--line:#E4E1F7;--bg:var(--isomer-light-gray);--surface:var(--isomer-white);--purple:var(--isomer-accent-purple);--pv:#FFFFFF}}
body[data-pv="gray"]{{--pv:var(--isomer-light-gray)}}
body[data-pv="dark"]{{--pv:var(--isomer-blue)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.55 var(--isomer-font-body);-webkit-font-smoothing:antialiased}}
h1,h2,b{{font-family:var(--isomer-font-display)}}
a{{color:var(--purple)}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 16px}}
@media (min-width:720px){{.wrap{{padding:0 32px}}}}
header{{padding:48px 0 24px}}
.flag{{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:4px 10px}}
h1{{font-size:clamp(34px,5vw,52px);line-height:1.05;letter-spacing:-.02em;margin:16px 0 12px;font-weight:700}}
header p{{max-width:720px;color:var(--muted);font-size:17px;margin:0}}
header .links{{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:16px;font-size:14px;font-weight:600}}
.bar{{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 0}}
.bar .wrap{{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}}
.bar input{{flex:1 1 220px;min-width:0;font:inherit;font-size:15px;padding:9px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)}}
.chips,.pvs{{display:flex;flex-wrap:wrap;gap:4px}}
.chips button,.pvs button{{font:600 13px var(--isomer-font-body);border:1px solid var(--line);background:var(--surface);color:var(--muted);border-radius:999px;padding:6px 11px;cursor:pointer}}
.chips button[aria-pressed=true],.pvs button[aria-pressed=true]{{background:var(--ink);border-color:var(--ink);color:#fff}}
.pvs span{{font-size:13px;color:var(--muted);align-self:center;margin-right:4px}}
.grp{{padding:36px 0 8px}}
.grp-h{{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;margin-bottom:16px}}
.grp-h h2{{margin:0;font-size:26px;letter-spacing:-.01em}}
.grp-h p{{margin:0;color:var(--muted);font-size:14px}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}}

.card{{margin:0;display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.pv{{flex:none;display:flex;align-items:center;justify-content:center;height:200px;background:var(--pv);border-bottom:1px solid var(--line);padding:18px}}
.icons .pv{{height:120px}}
.card.on-dark .pv{{background:var(--isomer-blue)}}
.pv img{{max-width:100%;max-height:100%;width:auto;height:auto}}
.icons .pv img{{width:56px;height:56px}}
.patterns .pv img{{max-height:164px}}
figcaption{{flex:1;display:flex;flex-direction:column;gap:3px;padding:12px 14px 14px;font-size:13px}}
figcaption b{{font-size:15px;line-height:1.3}}
figcaption code{{color:var(--muted);word-break:break-all}}
.meta{{color:var(--muted)}}
.used{{color:var(--ink)}}.used.none{{color:var(--isomer-blue-60);font-style:italic}}
.acts{{display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:auto;padding-top:8px;font-weight:600;white-space:nowrap}}
.acts a{{text-decoration:none}}
.ai-tag{{align-self:flex-start;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--purple);border:1px solid var(--purple);border-radius:999px;padding:2px 8px;margin-bottom:4px}}
.card.ai{{border-style:dashed;border-color:var(--purple)}}
.grp#new .grp-h p{{color:var(--ink)}}
.acts button{{font:inherit;font-weight:600;color:var(--purple);background:none;border:0;padding:0;cursor:pointer}}
.empty{{display:none;padding:48px 0;color:var(--muted)}}
footer{{border-top:1px solid var(--line);margin-top:40px;padding:24px 0 48px;color:var(--muted);font-size:13px}}
.toast{{position:fixed;left:50%;bottom:20px;transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;font-size:13px;padding:8px 14px;border-radius:8px;opacity:0;transition:.2s;pointer-events:none}}
.toast.on{{opacity:1;transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){{.toast{{transition:none}}}}
</style>
</head>
<body data-pv="white">
<header class="wrap">
<span class="flag">Unlisted · not linked from the brand site</span>
<h1>Isomer illustrations</h1>
<p>Every illustration, icon and background pattern on isomer.ai, as SVG: {n_ill} illustrations, plus icons and patterns. The {n_new} in the last section are AI-generated by Claude in the same style; they are marked on every card and are not on isomer.ai. Each card shows where the asset is used on the site. Open an SVG to view it full size, or download it.</p>
<div class="links"><a href="index.json">index.json</a><a href="#illustrations">Illustrations</a><a href="#icons">Icons</a><a href="#patterns">Patterns</a><a href="#new">Generated by Claude</a></div>
</header>
<div class="bar"><div class="wrap">
<input type="search" id="q" placeholder="Search by name or page" aria-label="Search illustrations">
<div class="chips" role="group" aria-label="Filter">{chips}</div>
<div class="pvs" role="group" aria-label="Preview background"><span>Preview on</span><button type="button" data-pv="white" aria-pressed="true">White</button><button type="button" data-pv="gray" aria-pressed="false">Light gray</button><button type="button" data-pv="dark" aria-pressed="false">Isomer Blue</button></div>
</div></div>
<main class="wrap">
{sections}
<p class="empty" id="empty">Nothing matches that search.</p>
</main>
<footer class="wrap">The Generated by Claude section is AI-generated by <code>scripts/draw_illustrations.py</code>. Synced {m["synced"]} from <code>www-isomer/client/src/assets</code> at <code>{e(m["source"]["commit"])}</code>. Regenerate with <code>python3 scripts/build_illustrations.py</code>. Third-party marks in the site's icons folder are left out.</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const cards=$$(".card"),q=$("#q");let f="all";
function apply(){{const t=q.value.trim().toLowerCase();let shown=0;
 cards.forEach(c=>{{const g=c.dataset.group;
  const okF=f==="all"||(f==="unused"&&c.dataset.unused==="1")||(f===g)||(c.dataset.size===f);
  const ok=okF&&(!t||c.dataset.q.includes(t));c.hidden=!ok;if(ok)shown++}});
 $$(".grp").forEach(s=>s.hidden=!s.querySelector(".card:not([hidden])"));
 $("#empty").style.display=shown?"none":"block"}}
q.addEventListener("input",apply);
$$(".chips button").forEach(b=>b.addEventListener("click",()=>{{f=b.dataset.f;$$(".chips button").forEach(x=>x.setAttribute("aria-pressed",x===b));apply()}}));
$$(".pvs button").forEach(b=>b.addEventListener("click",()=>{{document.body.dataset.pv=b.dataset.pv;$$(".pvs button").forEach(x=>x.setAttribute("aria-pressed",x===b))}}));
const toast=$("#toast");let tt;function say(m){{toast.textContent=m;toast.classList.add("on");clearTimeout(tt);tt=setTimeout(()=>toast.classList.remove("on"),1400)}}
$$("[data-url]").forEach(b=>b.addEventListener("click",()=>{{const u=b.dataset.url;
 try{{navigator.clipboard.writeText(u).then(()=>say("Copied URL"),()=>say(u))}}catch(e){{say(u)}}}}));
</script>
</body>
</html>
'''


if __name__ == "__main__":
    build()
