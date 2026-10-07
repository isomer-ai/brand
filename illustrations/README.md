# Illustrations (unlisted)

Every illustration, Isomer icon and background pattern from isomer.ai, as SVG. The page carries `noindex` and is not linked from the brand site, `brand.json` or `llms.txt`.

Page: <https://isomer-ai.github.io/brand/illustrations/>

| Path | What it is |
| --- | --- |
| `index.html` | The browsable page: search, size filters, preview background, download and copy URL |
| `index.json` | Every asset with its title, group, size, size class, the site pages that use it and its URL |
| `svg/` | The 53 illustrations |
| `icons/` | Signal category and capability icons |
| `patterns/` | Cross patterns used behind page heroes and sections |

The files are copied from `www-isomer/client/src/assets`. Third-party marks in the site's icons folder (Gmail, LinkedIn, Microsoft) are left out. To resync after the site changes:

```bash
python3 scripts/build_illustrations.py ~/repos/www-isomer
```
