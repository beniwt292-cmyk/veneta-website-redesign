#!/usr/bin/env python3
"""§6.4 gate. Fails loudly on anything the checklist requires and the build missed."""
import glob
import html as H
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
import seo as SEO  # noqa: E402

fail, warn = [], []


def check(cond, msg):
    if not cond:
        fail.append(msg)


pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
titles, descs, canons = {}, {}, {}
ld_by_type = {}
imgs_total = imgs_alt = imgs_decorative = 0
hd_links = hd_ok = 0

for name in pages:
    h = open(os.path.join(ROOT, name)).read()

    t = re.search(r"<title>(.*?)</title>", h, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', h, re.S)
    c = re.search(r'<link rel="canonical" href="([^"]+)">', h)
    check(t, f"{name}: no <title>")
    check(d, f"{name}: no meta description")
    check(c, f"{name}: no canonical")
    if t:
        v = H.unescape(t.group(1))
        check(len(v) <= 60, f"{name}: title {len(v)} chars > 60 -> {v}")
        titles.setdefault(v, []).append(name)
    if d:
        v = H.unescape(d.group(1))
        check(len(v) <= 155, f"{name}: description {len(v)} chars > 155")
        check(len(v) >= 50, f"{name}: description only {len(v)} chars")
        descs.setdefault(v, []).append(name)
    if c:
        check(c.group(1) == SEO.url_for(name),
              f"{name}: canonical {c.group(1)} != {SEO.url_for(name)}")
        canons.setdefault(c.group(1), []).append(name)

    for prop in ("og:type", "og:site_name", "og:url", "og:title", "og:description",
                 "og:image", "og:image:width", "og:image:height", "og:image:alt"):
        check(f'property="{prop}"' in h, f"{name}: missing {prop}")
    for nm in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
        check(f'name="{nm}"' in h, f"{name}: missing {nm}")
    tw = re.search(r'<meta name="twitter:card" content="([^"]+)"', h)
    check(tw and tw.group(1) == "summary_large_image", f"{name}: twitter:card not summary_large_image")

    ogi = re.search(r'<meta property="og:image" content="([^"]+)"', h)
    if ogi:
        rel = ogi.group(1).replace(SEO.SITE + "/", "")
        p = os.path.join(ROOT, rel)
        check(os.path.exists(p), f"{name}: og:image missing on disk -> {rel}")
        if os.path.exists(p):
            from PIL import Image
            w, hh = Image.open(p).size
            check((w, hh) == (1200, 630), f"{name}: og:image is {w}x{hh}, not 1200x630")

    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            fail.append(f"{name}: invalid JSON-LD ({e})")
            continue
        check(obj.get("@context") == "https://schema.org", f"{name}: JSON-LD @context wrong")
        ld_by_type.setdefault(obj.get("@type"), set()).add(name)

    for m in re.finditer(r"<img\b[^>]*>", h):
        tag = m.group(0)
        imgs_total += 1
        a = re.search(r'\salt="(.*?)"', tag)
        check(a is not None, f"{name}: <img> with no alt attribute")
        if a and a.group(1).strip():
            imgs_alt += 1
        elif 'class="mm-ph"' in h[max(0, m.start() - 80):m.start()]:
            imgs_decorative += 1   # labelled mega-menu link: alt="" is the correct choice
        else:
            fail.append(f"{name}: empty alt on a content image -> {tag[:90]}")

    for m in re.finditer(r"<a\b[^>]*homedepot\.com[^>]*>", h):
        tag = m.group(0)
        hd_links += 1
        ok = 'target="_blank"' in tag and "noopener" in tag
        check("nofollow" not in tag and "sponsored" not in tag,
              f"{name}: Home Depot link must stay followed -> {tag[:80]}")
        if ok:
            hd_ok += 1
        else:
            fail.append(f"{name}: HD link missing target/rel -> {tag[:80]}")

for v, ns in titles.items():
    check(len(ns) == 1, f"duplicate title across {ns}: {v}")
for v, ns in descs.items():
    check(len(ns) == 1, f"duplicate description across {ns}")
for v, ns in canons.items():
    check(len(ns) == 1, f"duplicate canonical {v} across {ns}")

# --- required structured data coverage
CATS = ["cellular-shades", "roller-solar-shades", "roman-shades", "faux-wood-blinds",
        "shutters", "sheer-shades", "dualdrape", "vertical-blinds"]
got = ld_by_type
check("Organization" in got and got["Organization"] == {"index.html"},
      "Organization JSON-LD must be on index.html only")
check("WebSite" in got and "index.html" in got["WebSite"], "WebSite JSON-LD missing on index.html")
crumbed = got.get("BreadcrumbList", set())
for name in pages:
    if name in ("index.html", "404.html"):
        check(name not in crumbed, f"{name}: should not carry a BreadcrumbList")
    else:
        check(name in crumbed, f"{name}: missing BreadcrumbList JSON-LD")
prods = got.get("Product", set())
check(prods == {c + ".html" for c in CATS},
      "Product JSON-LD coverage wrong: " + str(sorted(prods)))
for n in ("how-to-measure.html", "how-to-install.html", "how-to-clean.html"):
    check(n in got.get("HowTo", set()), f"{n}: missing HowTo JSON-LD")
faqs = got.get("FAQPage", set())
for name in pages:
    has_acc = "<details" in open(os.path.join(ROOT, name)).read()
    if has_acc:
        check(name in faqs, f"{name}: renders FAQs but has no FAQPage JSON-LD")

# --- sitemap.xml + robots.txt
sm = os.path.join(ROOT, "sitemap.xml")
check(os.path.exists(sm), "sitemap.xml missing")
if os.path.exists(sm):
    root = ET.parse(sm).getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locs = [e.findtext(ns + "loc") for e in root.findall(ns + "url")]
    check(len(locs) == len(set(locs)), "sitemap.xml has duplicate <loc> entries")
    expect = {SEO.url_for(n) for n in pages if n not in SEO.NOINDEX_PAGES}
    check(set(locs) == expect,
          "sitemap.xml urls != indexable pages; missing=%s extra=%s"
          % (sorted(expect - set(locs)), sorted(set(locs) - expect)))
    for e in root.findall(ns + "url"):
        check(e.findtext(ns + "lastmod") and e.findtext(ns + "priority")
              and e.findtext(ns + "changefreq"), "sitemap.xml url missing lastmod/priority/changefreq")

rb = os.path.join(ROOT, "robots.txt")
check(os.path.exists(rb), "robots.txt missing")
if os.path.exists(rb):
    body = open(rb).read()
    check("Sitemap: %s/sitemap.xml" % SEO.SITE in body, "robots.txt does not point to the sitemap")
    if SEO.PRODUCTION:
        check("Allow: /" in body and "Disallow: /" not in body, "robots.txt should allow all in production")
    else:
        check("Disallow: /" in body, "robots.txt should disallow all while this is a mockup")

print("pages checked        :", len(pages))
print("images              :", imgs_total, "| descriptive alt:", imgs_alt,
      "| decorative alt='':", imgs_decorative)
print("home depot links    :", hd_links, "| target+noopener:", hd_ok)
print("json-ld types       :", {k: len(v) for k, v in sorted(ld_by_type.items())})
print("robots mode         :", "PRODUCTION index,follow" if SEO.PRODUCTION else "mockup noindex")
print()
if warn:
    for w in warn:
        print("WARN ", w)
if fail:
    print("FAIL", len(fail))
    for f in fail[:60]:
        print("  -", f)
    sys.exit(1)
print("§6.4 gate: PASS")
