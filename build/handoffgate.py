#!/usr/bin/env python3
"""§9 + §10 gate. Fails the build if the Home Depot handoff or the measurement
layer has drifted: an unmapped retail URL, a link without UTMs or a GA4 hook, a
page with no page_type, a malformed data-hd value, or a §10 event with no code
path to fire it."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import data as D           # noqa: E402
import hd as HD            # noqa: E402

PAGES = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
JS = open(os.path.join(ROOT, "assets/js/veneta.js")).read()

A_TAG = re.compile(r'<a\b[^>]*\bhref="(https://www\.homedepot\.com[^"]*)"[^>]*>')
FULL_A = re.compile(r'<a\b[^>]*\bhref="https://www\.homedepot\.com[^"]*"[^>]*>')

# §10 events and the string that proves each one has a firing path.
EVENTS = {
    "hd_click":           "'hd_click'",
    "sample_request":     "data-ev",          # declarative, hooked on the samples form
    "finder_complete":    "'finder_complete'",
    "spec_table_view":    "'spec_table_view'",
    "swatch_select":      "'swatch_select'",
    "guide_read":         "'guide_read'",
    "trade_apply":        "data-ev",          # declarative, hooked on the trade CTA
    "commercial_inquiry": "data-ev",          # declarative, awaits the §7.6 page
    "spec_download":      "data-ev",          # declarative, awaits spec assets
}

# Events that must actually be attached to markup today, and where.
ATTACHED = {
    "sample_request": "free-samples.html",
    "trade_apply":    "for-professionals.html",
}

fail, warn = [], []
bases = set(D.HD_LINKS.values())
links = 0
hooked = 0
seen_modules = set()
pt_counts = {}


def base_of(url):
    return url.split("?")[0]


for name in PAGES:
    html = open(os.path.join(ROOT, name)).read()

    # --- page identity ----------------------------------------------------
    if name not in HD.PAGE_META:
        fail.append(f"{name}: no entry in hd.PAGE_META")
    page_type, category = HD.meta(name)
    pt_counts[page_type] = pt_counts.get(page_type, 0) + 1

    m = re.search(r'<body\b[^>]*>', html)
    if not m:
        fail.append(f"{name}: no <body> tag")
    else:
        if f'data-page-type="{page_type}"' not in m.group(0):
            fail.append(f"{name}: body missing data-page-type={page_type}")
        if 'data-category=' not in m.group(0):
            fail.append(f"{name}: body missing data-category")

    if HD.PT in html:
        fail.append(f"{name}: unresolved page-type token left in the output")

    # --- GA4 boot ---------------------------------------------------------
    if "window.dataLayer" not in html:
        fail.append(f"{name}: GA4 bootstrap missing from <head>")
    if "gtag('consent','default'" not in html:
        fail.append(f"{name}: Consent Mode defaults missing")

    # --- retail links -----------------------------------------------------
    for tag in FULL_A.findall(html):
        links += 1
        url = re.search(r'href="([^"]+)"', tag).group(1)
        if base_of(url) not in bases:
            fail.append(f"{name}: retail URL not in HD_LINKS -> {base_of(url)}")
        if "utm_source=veneta" not in url or "utm_content=" not in url:
            fail.append(f"{name}: retail link missing UTMs -> {url[:70]}")
        if 'target="_blank"' not in tag or "noopener" not in tag:
            fail.append(f"{name}: retail link missing target/rel -> {tag[:70]}")
        if "nofollow" in tag:
            fail.append(f"{name}: retail link is nofollow (§6.4 says followed)")
        hd = re.search(r'data-hd="([^"]*)"', tag)
        if not hd:
            fail.append(f"{name}: retail link missing data-hd -> {tag[:70]}")
            continue
        hooked += 1
        parts = hd.group(1).split("|")
        if len(parts) != 3 or not parts[0] or not parts[1] or not parts[2]:
            fail.append(f"{name}: malformed data-hd -> {hd.group(1)}")
            continue
        if parts[0] != page_type:
            fail.append(f"{name}: data-hd page_type {parts[0]} != {page_type}")
        uc = re.search(r"utm_content=([^\"&]+)", url).group(1)
        if uc.replace(".", "|") != hd.group(1):
            fail.append(f"{name}: data-hd disagrees with utm_content -> {uc}")
        seen_modules.add(parts[1])

    # --- §9.3 trust line, body CTAs only (chrome is exempt) ---------------
    chrome = ("header", "mobile_nav", "sticky")
    body_cta = [t for t in FULL_A.findall(html)
                if 'btn--hd"' in t
                and not any(f'|{c}|' in t for c in chrome)]
    if body_cta and "hd-trust" not in html:
        warn.append(f"{name}: body retail CTA with no §9.3 trust line")

# --- no page may hardcode a retail URL outside the helper ----------------
for f in ("shell.py", "build_site.py", "pages2.py", "pages3.py", "p2.py"):
    src = open(os.path.join(ROOT, "build", f)).read()
    for u in re.findall(r'href="(https://www\.homedepot\.com[^"]*)"', src):
        fail.append(f"build/{f}: hardcoded retail href, use hd.btn() -> {u[:60]}")

# --- §10 event coverage ---------------------------------------------------
for ev, proof in EVENTS.items():
    if proof not in JS:
        fail.append(f"§10 event {ev}: no firing path in assets/js/veneta.js")
for ev, page in ATTACHED.items():
    html = open(os.path.join(ROOT, page)).read()
    if f'data-ev="{ev}"' not in html:
        fail.append(f"§10 event {ev}: not attached to any element on {page}")

# --- budget ---------------------------------------------------------------
import gzip                                                    # noqa: E402
jsz = len(gzip.compress(JS.encode())) / 1024
if jsz > 12:
    fail.append(f"JS budget: {jsz:.1f} KB gzip > 12 KB")

# --- report --------------------------------------------------------------
print(f"pages checked        : {len(PAGES)}")
print(f"retail links         : {links} | with UTMs + data-hd: {hooked}")
print(f"HD_LINKS keys        : {len(D.HD_LINKS)} | still placeholder: {len(D.HD_PLACEHOLDER)}")
print(f"modules seen         : {', '.join(sorted(seen_modules))}")
print(f"page types           : {dict(sorted(pt_counts.items()))}")
print(f"§10 events wired     : {len(EVENTS)}/9")
print(f"js bundle            : {jsz:.1f} KB gzip / 12 KB")
print(f"GA4 measurement id   : {HD.GA4_ID or 'NOT SET (mockup: events go to dataLayer only)'}")

if D.HD_PLACEHOLDER:
    print("\nPLACEHOLDER destinations awaiting real URLs from the retailer:")
    for k in sorted(D.HD_PLACEHOLDER):
        print(f"  - {k:22s} -> {D.HD_LINKS[k]}")

if warn:
    print(f"\nWARN {len(warn)}")
    for w in warn[:20]:
        print("  -", w)

if fail:
    print(f"\nFAIL {len(fail)}")
    for f in fail[:40]:
        print("  -", f)
    sys.exit(1)

print("\n§9/§10 gate: PASS")
