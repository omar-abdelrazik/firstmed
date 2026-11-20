# First Medical (1st MED) website

Bilingual static website for First Medical, a medical-consumables factory in Tala, Menoufia, Egypt.
English pages live at the root and Arabic pages under `/ar/`. Each language is written for its own reader, not translated.

## What's where

| Path | What it is |
|---|---|
| `index.html`, `products.html`, `services/…`, `ar/…` | Generated pages. **Don't edit by hand**: change the templates and rebuild. |
| `tools/templates/` | Page templates. Both languages sit side by side: `t("English", "عربي")`. |
| `tools/site_data.py` | Products, sizes, contacts and the Services menu (English/Arabic pairs). |
| `tools/build.py` | The generator. Also writes `sitemap.xml` and `robots.txt`. |
| `assets/css/site.css` | Design system: colours from the logo, Alexandria + IBM Plex type, light/dark themes, RTL through logical properties. |
| `assets/js/site.js` | Theme toggle, menus, size switcher, and the quote form (it composes a WhatsApp/email message and stores nothing). |
| `assets/img/` | Brand, hero, product cut-outs and real floor photos. |
| `assets/fonts/` | Self-hosted fonts (SIL Open Font License). |
| `docs/brand-voice.md` | How we write in English and Arabic. |
| `docs/to-confirm.md` | Facts the owners still need to confirm before anything new is claimed. |

## Edit and rebuild

```bash
pip install jinja2 pillow
python3 tools/build.py
```

Commit the generated pages together with the template change.

## Publish

The live site is deployed from `main` (Vercel). Pushing to `main` updates it.
Canonical links, hreflang and the sitemap use `SITE_URL` in `tools/site_data.py` (currently `https://www.1st-medical.com`). Change it if the site lives elsewhere, then rebuild.

## Content rules (they apply to every edit)

1. Only publish numbers we can prove. Write goals as targets ("targeted for 2027").
2. No certificate badges. Documents are sent for the specific product and market.
3. If a detail isn't confirmed, write "on request". Don't guess it.
4. Don't write about the website itself or about our own honesty, and don't publish internal plans as weaknesses.
5. Each language page is written entirely in its own language. Never put a translation next to a title.
6. Arabic sizes follow normal right-to-left order (write «10 × 18 سم»; don't force it left-to-right).
