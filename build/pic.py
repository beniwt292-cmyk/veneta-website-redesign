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
import hashlib, json, os, re

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


# --- background video --------------------------------------------------------
# No codecs= parameter in the type: the container may hold AV1, VP9 or H.264 and
# a mismatched codec string makes the browser skip a file it could have played.
VIDEO_TYPES = [("webm", "video/webm"), ("mp4", "video/mp4")]


def video_files(name):
    """Which assets/video/NAME.* encodes exist, smallest transfer first.

    Sorting by size rather than hard-coding webm-before-mp4 means whichever
    encode actually came out lighter is the one most browsers take.

    The path carries a short content hash (?v=...) so replacing an encode under
    the same filename is a new URL to the browser and the CDN, not a cache hit
    on the old bytes. Without this, swapping hero-home.mp4 for a corrected cut
    can silently keep serving the previous clip for a long time.
    """
    out = []
    for ext, mime in VIDEO_TYPES:
        path = os.path.join("assets", "video", f"{name}.{ext}")
        full = os.path.join(ROOT, path)
        if os.path.exists(full):
            with open(full, "rb") as f:
                digest = hashlib.sha1(f.read()).hexdigest()[:10]
            out.append((os.path.getsize(full), f"{path}?v={digest}", mime))
    return [(p, m) for _, p, m in sorted(out)]


def bg_video(name, poster_shot):
    """Decorative looping hero video, or "" when no encode has shipped yet.

    The sources are held in data-src and attached by build/interactive.js, so a
    visitor on prefers-reduced-motion, Save-Data or a 2G connection never pays
    for the download. The poster is the same file the <picture> already loads,
    so it is a cache hit rather than a second request.
    """
    files = video_files(name)
    if not files:
        return ""
    by_id, _ = _shots()
    s = by_id.get(poster_shot)
    poster = s["files"]["webp"] if s and shipped(s) else ""
    srcs = "".join(f'<source data-src="{p}" type="{m}">' for p, m in files)
    return (f'<video class="hero-vid" data-bg-video muted playsinline '
            f'disablepictureinpicture preload="none" tabindex="-1" aria-hidden="true"'
            f'{f" poster={chr(34)}{poster}{chr(34)}" if poster else ""}>{srcs}</video>')


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


# --- guide diagrams ----------------------------------------------------------
# Hand-built SVG rather than generated raster, because these need legible
# lettering and §11.2 forbids that in generated imagery. Alt text lives in
# build/diagrams.py so the drawing and its description are edited together.
def diagram(name, caption=""):
    """<figure> wrapping one of the assets/img/diagram-*.svg guide drawings."""
    import diagrams as DG
    path = os.path.join("assets", "img", name + ".svg")
    if not os.path.exists(os.path.join(ROOT, path)):
        return ""
    alt = DG.ALT.get(name, "")
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="diagram">'
            f'<img src="{path}" alt="{alt}" width="1400" height="1050" '
            f'loading="lazy" decoding="async">{cap}</figure>')


def diagram_pair(a, b, cap_a="", cap_b=""):
    """Two diagrams, stacked. Never side by side: a 1400px-wide drawing shown at
    half the prose column drops its lettering below a readable size."""
    return diagram(a, cap_a) + diagram(b, cap_b)
