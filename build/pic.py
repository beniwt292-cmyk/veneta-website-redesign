#!/usr/bin/env python3
"""Manifest-driven <picture> output for the P1 image set.

Two entry points:

  pic(shot_id, ...)  -> full <picture> markup for a shot, used by new templates.
  upgrade(html)      -> rewrites any legacy <img src="assets/img/NAME.webp"> into
                        <picture> once the matching P1 shot has shipped.

`upgrade` is applied inside build_site.write(), so accepted images appear on every
page as each batch lands, with no per-page edits and no broken build while the set
is incomplete.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "docs", "p1-manifest.json")

_cache = {}


def _shots():
    if "shots" not in _cache:
        try:
            with open(MANIFEST) as f:
                doc = json.load(f)
        except FileNotFoundError:
            doc = {"shots": []}
        by_id, by_legacy = {}, {}
        for s in doc["shots"]:
            by_id[s["id"]] = s
            for name in s.get("legacy", []):
                by_legacy.setdefault(name, s)
        _cache["shots"], _cache["legacy"] = by_id, by_legacy
    return _cache["shots"], _cache["legacy"]


def shipped(s):
    return all(os.path.exists(os.path.join(ROOT, s["files"][k])) for k in ("avif", "webp"))


def pic(shot_id, cls="", sizes="", style="", alt=None, lcp=None, img_id=""):
    """<picture> with AVIF + WebP, explicit dimensions and descriptive alt text."""
    by_id, _ = _shots()
    s = by_id.get(shot_id)
    if not s or not shipped(s):
        return ""
    return _markup(s, cls=cls, sizes=sizes, style=style, img_id=img_id,
                   alt=alt or s["alt"], lcp=s["lcp"] if lcp is None else lcp)


def _markup(s, cls="", sizes="", style="", alt="", lcp=False, img_id=""):
    load = 'fetchpriority="high" decoding="async"' if lcp else 'loading="lazy" decoding="async"'
    sz = f' sizes="{sizes}"' if sizes else ""
    return (
        f'<picture{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'
        f'<source type="image/avif" srcset="{s["files"]["avif"]}"{sz}>'
        f'<source type="image/webp" srcset="{s["files"]["webp"]}"{sz}>'
        f'<img {f"id={chr(34)}{img_id}{chr(34)} " if img_id else ""}src="{s["files"]["webp"]}" alt="{alt}" width="{s["width"]}" height="{s["height"]}" '
        f'{load}{f" style={chr(34)}{style}{chr(34)}" if style else ""}></picture>'
    )


_IMG = re.compile(r'<img\b[^>]*?src="assets/img/([^"]+)"[^>]*>')


def _attr(tag, name):
    m = re.search(r'\b%s="([^"]*)"' % name, tag)
    return m.group(1) if m else ""


def upgrade(html):
    """Swap legacy <img> tags for <picture> wherever a P1 shot has shipped.

    Decorative images (empty alt: gallery thumbnails, video posters) are left on
    their small legacy files. Substituting a full-size hero into a 90px thumbnail
    wastes bytes, and those modules are rebuilt in P2 anyway.
    """
    _, by_legacy = _shots()

    def sub(m):
        tag, name = m.group(0), m.group(1)
        s = by_legacy.get(os.path.basename(name))
        if not s or not shipped(s):
            return tag
        if not _attr(tag, "alt"):
            return tag                       # decorative: leave the legacy thumbnail
        return _markup(
            s,
            cls=_attr(tag, "class"),
            style=_attr(tag, "style"),
            alt=s["alt"],
            lcp="fetchpriority" in tag,      # never promote a second LCP candidate
        )

    return _IMG.sub(sub, html)
