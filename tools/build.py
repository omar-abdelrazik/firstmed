#!/usr/bin/env python3
"""Build the First Medical website.

    pip install jinja2 pillow
    python3 tools/build.py

Writes English pages to the repository root and Arabic pages to /ar/.
Both languages live side by side in the templates as t("English", "عربي").
"""
import hashlib
import json
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, pass_context
from PIL import Image

import site_data as D

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "tools" / "templates"

# slug, template, nav id, in sitemap
PAGES = [
    ("index.html", "pages/home.html", "home", True),
    ("products.html", "pages/products.html", "products", True),
    ("manufacturing.html", "pages/manufacturing.html", "manufacturing", True),
    ("about.html", "pages/about.html", "about", True),
    ("services/index.html", "pages/services.html", "services", True),
    ("services/enterprises.html", "pages/service-enterprises.html", "services", True),
    ("services/government.html", "pages/service-government.html", "services", True),
    ("services/partners.html", "pages/service-partners.html", "services", True),
    ("services/oem.html", "pages/service-oem.html", "services", True),
    ("faq.html", "pages/faq.html", "faq", True),
    ("contact.html", "pages/contact.html", "contact", True),
]

_dims = {}


def dims(rel):
    if rel not in _dims:
        with Image.open(ROOT / "assets" / rel) as im:
            _dims[rel] = im.size
    return _dims[rel]


def version():
    h = hashlib.sha1()
    for p in ["assets/css/site.css", "assets/js/site.js"]:
        h.update((ROOT / p).read_bytes())
    return h.hexdigest()[:8]


@pass_context
def t(ctx, en, ar):
    return ar if ctx["lang"] == "ar" else en


@pass_context
def tt(ctx, pair):
    return pair[1] if ctx["lang"] == "ar" else pair[0]


def public_url(out_rel):
    path = out_rel[:-len("index.html")] if out_rel.endswith("index.html") else out_rel
    return f"{D.SITE_URL}/{path}"


def org_jsonld():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "First Medical",
        "alternateName": ["1st MED", "فيرست ميديكال"],
        "url": D.SITE_URL + "/",
        "logo": D.SITE_URL + "/assets/img/brand/logo.png",
        "slogan": "Making quality accessible.",
        "address": {"@type": "PostalAddress", "addressLocality": "Tala", "addressRegion": "Menoufia", "addressCountry": "EG"},
        "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "telephone": D.CONTACT["sales_phone"].replace(" ", "-"),
                          "email": D.CONTACT["sales_email"], "availableLanguage": ["Arabic", "English"]}],
    }, ensure_ascii=False)


def build():
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False,
                      trim_blocks=True, lstrip_blocks=True)
    env.globals.update(t=t, tt=tt, dims=dims, C=D.CONTACT, SERVICES=D.SERVICES, PRODUCTS=D.PRODUCTS,
                       CATEGORIES=D.CATEGORIES, SIZES=D.RIGHT_PRO_SIZES, SITE_URL=D.SITE_URL)
    ver = version()
    written = []
    for lang in ("en", "ar"):
        other = "ar" if lang == "en" else "en"
        only = os.environ.get("ONLY")
        for slug, tpl, nav_id, _ in PAGES:
            if only and slug not in only.split(","):
                continue
            out_rel = ("ar/" if lang == "ar" else "") + slug
            prefix = "../" * out_rel.count("/")

            def link(target, l=lang, prefix=prefix):
                return prefix + ("ar/" if l == "ar" else "") + target

            def asset(p, prefix=prefix):
                return prefix + "assets/" + p

            def img(p, alt, cls="", lazy=True, extra=""):
                w, h = dims(p)
                load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
                c = f' class="{cls}"' if cls else ""
                return f'<img src="{asset(p)}" width="{w}" height="{h}" alt="{alt}"{c}{load}{extra}>'

            html = env.get_template(tpl).render(
                lang=lang, other=other, dir="rtl" if lang == "ar" else "ltr", slug=slug, page_id=nav_id,
                link=link, asset=asset, img=img, alt_link=link(slug, other),
                canonical=public_url(out_rel), href_en=public_url(slug), href_ar=public_url("ar/" + slug),
                version=ver, org_jsonld=org_jsonld(),
            )
            dest = ROOT / out_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(html, encoding="utf-8")
            written.append(out_rel)

    # sitemap + robots
    urls = []
    for slug, _, _, in_map in PAGES:
        if not in_map:
            continue
        for l in ("en", "ar"):
            rel = ("ar/" if l == "ar" else "") + slug
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{public_url(("ar/" if x == "ar" else "") + slug)}"/>' for x in ("en", "ar"))
            urls.append(f"<url><loc>{public_url(rel)}</loc>{alts}</url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {D.SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(written)} pages (version {ver})")


if __name__ == "__main__":
    build()
