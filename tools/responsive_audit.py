"""Responsive audit for the First Medical site.

Loads every built page at real phone / tablet / laptop / monitor sizes and records
layout problems as structured issues. Usage:
    python3 resp_audit.py [out.json] [--quick]
Serve the built site first:  python3 -m http.server 8765 --bind 127.0.0.1
Needs Playwright (pip install playwright; playwright install chromium, or set CHROME=/path/to/chrome).
Prints a summary grouped by issue type; the full list goes to the JSON file.
"""
import asyncio, json, os, sys, pathlib, collections
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765/"
PAGES = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.html")
               if not ({"tools", "docs", "assets", "node_modules"} & set(p.parts)))

# name, width, height, dpr, touch
VIEWPORTS = [
    ("p280", 280, 653, 3, True),          # folded phone cover screen
    ("p320", 320, 568, 2, True),
    ("p360", 360, 780, 3, True),
    ("p375", 375, 667, 2, True),
    ("p390", 390, 844, 3, True),
    ("p412", 412, 915, 2.625, True),
    ("p430", 430, 932, 3, True),
    ("l568", 568, 320, 2, True),          # landscape phones
    ("l667", 667, 375, 2, True),
    ("l844", 844, 390, 3, True),
    ("l932", 932, 430, 3, True),
    ("t600", 600, 960, 2, True),          # small tablets, unfolded phones
    ("t712", 712, 1138, 2, True),
    ("t768", 768, 1024, 2, True),         # tablets portrait
    ("t810", 810, 1080, 2, True),
    ("t820", 820, 1180, 2, True),
    ("t834", 834, 1194, 2, True),
    ("t1024p", 1024, 1366, 2, True),
    ("t1024l", 1024, 768, 2, True),       # tablets landscape
    ("t1080l", 1080, 810, 2, True),
    ("t1180l", 1180, 820, 2, True),
    ("t1194l", 1194, 834, 2, True),
    ("t1366l", 1366, 1024, 2, True),
    ("e861", 861, 900, 1, False),         # just past each breakpoint
    ("e961", 961, 900, 1, False),
    ("e1001", 1001, 900, 1, False),
    ("e1101", 1101, 900, 1, False),
    ("d1280", 1280, 800, 1, False),       # laptops and monitors
    ("d1366", 1366, 768, 1, False),
    ("d1440", 1440, 900, 2, False),
    ("d1536", 1536, 864, 1.25, False),
    ("d1680", 1680, 1050, 1, False),
    ("d1920", 1920, 1080, 1, False),
    ("d2560", 2560, 1440, 1, False),
]

AUDIT_JS = r"""
(opts) => {
  const root = opts.root ? document.querySelector(opts.root) : document.body;
  const W = document.documentElement.clientWidth, H = innerHeight, DPR = devicePixelRatio;
  const res = { W, H, iw: innerWidth, docOverflow: document.documentElement.scrollWidth - W, issues: [] };
  const seen = new Set();
  const sel = (el) => {
    if (!el || el.nodeType !== 1) return '';
    const parts = [];
    for (let e = el, i = 0; e && e.nodeType === 1 && e !== document.body && i < 4; i++, e = e.parentElement) {
      let s = e.tagName.toLowerCase();
      if (e.id && !/^(main|site-nav)$/.test(e.id)) { parts.unshift(s + '#' + e.id); break; }
      const cls = [...e.classList].filter(c => !/^(open|is-)/.test(c)).slice(0, 2);
      if (cls.length) s += '.' + cls.join('.');
      parts.unshift(s);
    }
    return parts.join(' > ');
  };
  const add = (type, el, info = {}) => {
    const s = sel(el), k = type + '|' + s;
    if (seen.has(k)) return; seen.add(k);
    res.issues.push(Object.assign({ type, sel: s }, info));
  };
  const shown = (el) => {
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0.5 && r.height > 0.5;
  };
  const clips = (a) => { const cs = getComputedStyle(a); return cs.overflowX !== 'visible' || cs.overflowY !== 'visible' || /paint|strict|content/.test(cs.contain); };
  const clipAnc = (el) => { for (let a = el.parentElement; a && a !== document.body && a !== document.documentElement; a = a.parentElement) if (clips(a)) return a; return null; };
  const txt = (el) => (el.textContent || el.getAttribute('aria-label') || el.getAttribute('alt') || '').trim().replace(/\s+/g, ' ').slice(0, 32);
  const all = [...root.querySelectorAll('*')].filter(e => !(e.closest('svg') && e.tagName.toLowerCase() !== 'svg'));

  /* 1. anything past the viewport edge that no ancestor (other than body) clips */
  const flagged = new Set();
  for (const el of all) {
    const r = el.getBoundingClientRect();
    if (r.width < 0.5 || r.height < 0.5 || (r.right <= W + 1 && r.left >= -1)) continue;
    if (getComputedStyle(el).visibility === 'hidden') continue;
    const ca = clipAnc(el);
    if (ca) { const cr = ca.getBoundingClientRect(); if (cr.right <= W + 1 && cr.left >= -1) continue; }
    let dup = false; for (let p = el.parentElement; p; p = p.parentElement) if (flagged.has(p)) { dup = true; break; }
    flagged.add(el); if (!dup) add('offscreen-x', el, { l: Math.round(r.left), r: Math.round(r.right) });
  }

  /* 2. in-flow boxes wider than their parent's content box */
  for (const el of all) {
    const cs = getComputedStyle(el);
    if (/absolute|fixed/.test(cs.position) || cs.transform !== 'none' || /^(inline|contents)$/.test(cs.display)) continue;
    if (parseFloat(cs.marginLeft) < -0.5 || parseFloat(cs.marginRight) < -0.5) continue;
    if (el.matches('.dressing-label, .dressing svg')) continue;
    const p = el.parentElement; if (!p || p === document.body) continue;
    const pcs = getComputedStyle(p); if (/^(inline|contents)$/.test(pcs.display)) continue;
    const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    const pr = p.getBoundingClientRect();
    const pl = pr.left + parseFloat(pcs.borderLeftWidth) + parseFloat(pcs.paddingLeft);
    const prr = pr.right - parseFloat(pcs.borderRightWidth) - parseFloat(pcs.paddingRight);
    const over = Math.max(pl - r.left, r.right - prr);
    if (over <= 2) continue;
    if (/auto|scroll/.test(pcs.overflowX)) continue;
    add(clips(p) ? 'cut-by-parent' : 'overflows-parent', el, { over: Math.round(over), pw: Math.round(prr - pl), w: Math.round(r.width), t: txt(el) });
  }

  /* 3. text boxes: tiny type, text cut by a clipping box, text colliding with other text */
  const boxes = [];
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let n; (n = tw.nextNode());) {
    if (!n.nodeValue.trim()) continue;
    const el = n.parentElement;
    if (!el || el.closest('script,style,noscript,template,title') || !shown(el)) continue;
    const cd = el.closest('details:not([open])'); if (cd && !el.closest('summary')) continue;
    const cs = getComputedStyle(el);
    if (+cs.opacity === 0) continue;
    const fs = parseFloat(cs.fontSize);
    if (fs < opts.minFont) add('tiny-text', el, { fs: +fs.toFixed(1), t: n.nodeValue.trim().slice(0, 24) });
    const ca = clipAnc(el); const cr = ca && !/auto|scroll/.test(getComputedStyle(ca).overflowX) ? ca.getBoundingClientRect() : null;
    const rg = document.createRange(); rg.selectNodeContents(n);
    for (const r of rg.getClientRects()) {
      if (r.width < 2 || r.height < 2) continue;
      if (cr && (r.left < cr.left - 2 || r.right > cr.right + 2 || r.top < cr.top - 2 || r.bottom > cr.bottom + 2))
        add('text-cut', el, { t: n.nodeValue.trim().slice(0, 24), by: sel(ca) });
      const k = r.height * 0.22;
      boxes.push({ el, l: r.left, rt: r.right, t: r.top + scrollY + k, b: r.bottom + scrollY - k });
    }
  }
  boxes.sort((a, b) => a.t - b.t);
  for (let i = 0; i < boxes.length; i++) {
    const a = boxes[i];
    for (let j = i + 1; j < boxes.length && boxes[j].t < a.b; j++) {
      const b = boxes[j];
      if (a.el === b.el || a.el.contains(b.el) || b.el.contains(a.el)) continue;
      const ix = Math.min(a.rt, b.rt) - Math.max(a.l, b.l), iy = Math.min(a.b, b.b) - Math.max(a.t, b.t);
      if (ix > 2 && iy > 2) add('text-overlap', a.el, { with: sel(b.el), a: txt(a.el), b: txt(b.el) });
    }
  }

  /* 4. tap targets (inline links inside running text are exempt) */
  for (const el of root.querySelectorAll('a[href], button, summary, select, input:not([type=hidden]), textarea')) {
    if (!shown(el)) continue;
    if (el.closest('details:not([open])') && !el.closest('summary')) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'inline') {
      const block = el.closest('p, dd, td, .answer');
      if (block && block.textContent.trim().length > el.textContent.trim().length + 15) continue;
    }
    const r = el.getBoundingClientRect(); let w = Math.round(r.width), h = Math.round(r.height);
    if (el.matches('.dressing')) { const a = getComputedStyle(el, '::after'); w = Math.round(r.width - 2 * parseFloat(a.left)); }
    if (h < 24 || w < 24) add('tap-24', el, { w, h, t: txt(el) });
    else if (opts.touch && (h < 40 || w < 40)) add('tap-40', el, { w, h, t: txt(el) });
  }

  /* 5. images: not loaded, stretched, or upscaled past the screen's pixel density */
  for (const img of root.querySelectorAll('img')) {
    if (!shown(img)) continue;
    const src = (img.currentSrc || img.src).split('/').slice(-2).join('/');
    if (!img.complete || !img.naturalWidth) { add('img-not-loaded', img, { src }); continue; }
    const w = img.offsetWidth, h = img.offsetHeight, nw = img.naturalWidth, nh = img.naturalHeight;
    if (!w || !h) continue;
    const fit = getComputedStyle(img).objectFit;
    let scale;
    if (fit === 'cover') scale = Math.max(w / nw, h / nh);
    else if (fit === 'contain') scale = Math.min(w / nw, h / nh);
    else { scale = w / nw; const d = Math.abs((w / h) / (nw / nh) - 1); if (d > 0.03) add('img-distorted', img, { d: +d.toFixed(2), src }); }
    const need = scale * DPR;
    if (need > 1.3) add('img-soft', img, { need: +need.toFixed(2), src, css: w + 'x' + h, nat: nw + 'x' + nh });
  }

  /* 6. decorative cut-outs that sit on text, or lose much of themselves to a clipping box */
  for (const img of root.querySelectorAll('.pack-comp img, .tile-art img, .split-media .inset, .films img, .stage-circle img, .rp-carton img')) {
    if (!shown(img)) continue;
    const r = img.getBoundingClientRect(); const ca0 = clipAnc(img); const cr0 = ca0 ? ca0.getBoundingClientRect() : { left: -1e9, right: 1e9, top: -1e9, bottom: 1e9 };
    const R = { l: Math.max(r.left, cr0.left), rt: Math.min(r.right, cr0.right), t: Math.max(r.top, cr0.top) + scrollY, b: Math.min(r.bottom, cr0.bottom) + scrollY };
    for (const b of boxes) {
      if (img.parentElement.contains(b.el)) continue;
      const ix = Math.min(R.rt, b.rt) - Math.max(R.l, b.l), iy = Math.min(R.b, b.b) - Math.max(R.t, b.t);
      if (ix > 6 && iy > 6) { add('img-over-text', img, { t: txt(b.el), src: (img.currentSrc || '').split('/').pop() }); break; }
    }
    const ca = clipAnc(img);
    if (ca && img.closest('.pack-comp, .tile-art')) {
      const cr = ca.getBoundingClientRect();
      const vis = Math.max(0, Math.min(r.right, cr.right) - Math.max(r.left, cr.left)) * Math.max(0, Math.min(r.bottom, cr.bottom) - Math.max(r.top, cr.top));
      const cut = 1 - vis / (r.width * r.height);
      if (cut > 0.25) add('img-cut', img, { cut: +cut.toFixed(2), src: (img.currentSrc || '').split('/').pop() });
    }
  }

  if (!opts.root) {
    /* 7. header and nav */
    const hb = document.querySelector('.header-bar');
    if (hb) {
      const exp = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-h'));
      const h = hb.getBoundingClientRect().height;
      if (h > exp + 1) add('header-tall', hb, { h: Math.round(h), exp });
    }
    const nl = document.querySelector('.nav-list');
    if (nl && shown(nl) && getComputedStyle(nl).flexDirection === 'row') {
      const tops = new Set([...nl.children].filter(shown).map(li => Math.round(li.getBoundingClientRect().top)));
      if (tops.size > 1) add('nav-wrapped', nl);
      const brand = document.querySelector('.brand').getBoundingClientRect(), nr = nl.getBoundingClientRect();
      const gap = document.dir === 'rtl' ? brand.left - nr.right : nr.left - brand.right;
      if (gap < 16) add('nav-crowded', nl, { gap: Math.round(gap) });
    }
    /* 8. line lengths */
    for (const p of document.querySelectorAll('main p')) {
      if (!shown(p)) continue;
      const lh = parseFloat(getComputedStyle(p).lineHeight); if (!lh) continue;
      const lines = Math.round(p.getBoundingClientRect().height / lh); if (lines < 2) continue;
      const cpl = p.textContent.trim().length / lines;
      if (cpl > 95) add('long-lines', p, { cpl: Math.round(cpl), t: txt(p) });
      if (cpl < 16) add('narrow-lines', p, { cpl: Math.round(cpl), w: Math.round(p.getBoundingClientRect().width), t: txt(p) });
    }
    /* 9. first screen */
    const h1 = document.querySelector('h1');
    if (h1) { const r = h1.getBoundingClientRect(); if (r.bottom > H - 8) add('h1-below-fold', h1, { top: Math.round(r.top), bottom: Math.round(r.bottom), H }); }
    const lead = document.querySelector('.hero .actions, .phead-copy .actions');
    if (lead && shown(lead)) { const r = lead.getBoundingClientRect(); if (r.bottom > H * 1.6) add('cta-deep', lead, { bottom: Math.round(r.bottom), H }); }
    const sticky = [...document.querySelectorAll('.site-header, .subnav')].filter(e => shown(e) && /sticky|fixed/.test(getComputedStyle(e).position)).reduce((s, e) => s + e.getBoundingClientRect().height, 0);
    if (sticky > H * 0.3) add('sticky-heavy', document.querySelector('.site-header'), { px: Math.round(sticky), H });
    /* 10. the size chart */
    for (const c of document.querySelectorAll('.rp-chart')) if (shown(c) && c.scrollWidth > c.clientWidth + 1) add('chart-overflow', c, { sw: c.scrollWidth, cw: c.clientWidth });
    /* 11. section heights way past the screen (only for header blocks) */
    for (const s of document.querySelectorAll('.hero, .phead')) { const h = s.getBoundingClientRect().height; if (h > H * 1.25 && H < 700) add('header-block-tall', s, { h: Math.round(h), H }); }
  }
  return res;
}
"""

PREP_JS = r"""
async () => {
  document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 4000); })));
}
"""


async def audit_page(ctx, path, vp, sem, results):
    name, w, h, dpr, touch = vp
    async with sem:
        page = await ctx.new_page()
        try:
            await page.goto(BASE + path, wait_until="load")
            await page.evaluate(PREP_JS)
            r = await page.evaluate(AUDIT_JS, {"touch": touch, "minFont": 12})
            r["page"], r["vp"] = path, name
            results.append(r)
            # menus: open them and audit only the opened panel
            if path in ("index.html", "ar/index.html"):
                if await page.locator(".menu-btn").is_visible():
                    await page.locator(".menu-btn").click()
                    await page.wait_for_timeout(150)
                    m = await page.evaluate("""() => { const p = document.querySelector('.primary'), r = p.getBoundingClientRect();
                        return { open: getComputedStyle(p).display !== 'none', l: r.left, r: r.right, t: r.top, b: r.bottom,
                                 sh: p.scrollHeight, ch: p.clientHeight, oy: getComputedStyle(p).overflowY }; }""")
                    await page.locator(".nav-trigger").click()
                    await page.wait_for_timeout(150)
                    r2 = await page.evaluate(AUDIT_JS, {"touch": touch, "minFont": 12, "root": ".primary"})
                    m2 = await page.evaluate("""() => { const p = document.querySelector('.primary'); p.scrollTop = p.scrollHeight;
                        const c = document.querySelector('.mobile-cta').getBoundingClientRect(); return { ctaBottom: c.bottom, H: innerHeight, sh: p.scrollHeight, ch: p.clientHeight }; }""")
                    r2.update(page=path + "#menu", vp=name, menu=m, menu2=m2)
                    if m2["ctaBottom"] > m2["H"] + 1:
                        r2["issues"].append({"type": "menu-cta-unreachable", "sel": ".mobile-cta", **m2})
                    results.append(r2)
                else:
                    await page.locator(".nav-trigger").click()
                    await page.wait_for_timeout(150)
                    r2 = await page.evaluate(AUDIT_JS, {"touch": touch, "minFont": 12, "root": ".mega"})
                    mg = await page.evaluate("() => { const m = document.querySelector('.mega').getBoundingClientRect(); return { b: Math.round(m.bottom), H: innerHeight }; }")
                    if mg["b"] > mg["H"]:
                        r2["issues"].append({"type": "mega-taller-than-screen", "sel": ".mega", **mg})
                    r2.update(page=path + "#mega", vp=name)
                    results.append(r2)
        except Exception as e:  # keep going, report it
            results.append({"page": path, "vp": name, "issues": [{"type": "error", "sel": "", "msg": str(e)[:200]}]})
        finally:
            await page.close()


async def main():
    out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "responsive-audit.json"
    vps = VIEWPORTS
    if "--quick" in sys.argv:
        vps = [v for v in VIEWPORTS if v[0] in ("p320", "p390", "l844", "t768", "t1024l", "e1101", "d1440", "d1920")]
    results = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME") or None)
        sem = asyncio.Semaphore(8)
        tasks, ctxs = [], []
        for vp in vps:
            name, w, h, dpr, touch = vp
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr,
                                      is_mobile=touch, has_touch=touch, reduced_motion="reduce")
            ctxs.append(ctx)
            tasks += [audit_page(ctx, path, vp, sem, results) for path in PAGES]
        await asyncio.gather(*tasks)
        for c in ctxs:
            await c.close()
        await b.close()
    pathlib.Path(out).write_text(json.dumps(results, ensure_ascii=False, indent=0))

    # summary: issue type -> selector -> where
    order = [v[0] for v in VIEWPORTS]
    agg = collections.defaultdict(lambda: collections.defaultdict(lambda: {"vps": set(), "pages": set(), "ex": None}))
    for r in results:
        if r.get("docOverflow", 0) > 0:
            a = agg["doc-overflow"]["document"]; a["vps"].add(r["vp"]); a["pages"].add(r["page"]); a["ex"] = {"px": r["docOverflow"]}
        if r.get("iw") and r.get("W") and r["iw"] != r["W"]:
            a = agg["viewport-zoomed"]["window"]; a["vps"].add(r["vp"]); a["pages"].add(r["page"]); a["ex"] = {"iw": r["iw"], "W": r["W"]}
        for i in r["issues"]:
            a = agg[i["type"]][i["sel"]]
            a["vps"].add(r["vp"]); a["pages"].add(r["page"])
            if a["ex"] is None:
                a["ex"] = {k: v for k, v in i.items() if k not in ("type", "sel")} | {"at": r["vp"] + " " + r["page"]}
    print(f"{len(results)} page loads, {sum(len(r['issues']) for r in results)} issues\n")
    for t in sorted(agg):
        rows = agg[t]
        print(f"== {t}  ({len(rows)} selectors)")
        for s, a in sorted(rows.items(), key=lambda kv: -len(kv[1]["vps"]) * len(kv[1]["pages"]))[:14]:
            v = sorted(a["vps"], key=order.index)
            pg = sorted(a["pages"])
            print(f"   {s[:95]}\n      vps[{len(v)}]: {' '.join(v[:12])}{' …' if len(v) > 12 else ''} | pages[{len(pg)}]: {', '.join(pg[:4])}{' …' if len(pg) > 4 else ''}\n      e.g. {json.dumps(a['ex'], ensure_ascii=False)[:230]}")
        if len(rows) > 14:
            print(f"   … {len(rows) - 14} more")


asyncio.run(main())
