"""§9 Home Depot handoff + §10 measurement plumbing.

Two jobs:

1.  Render every outbound retail link through one helper so the destination, the
    UTM string and the GA4 hook can never drift apart. `href()` builds the URL,
    `btn()` builds the anchor.

2.  Stamp each finished page with its own identity: `stamp()` substitutes the
    page-type token, adds `data-hd` to every retail anchor (derived from that
    anchor's own `utm_content`, so the two can never disagree) and puts
    `data-page-type` / `data-category` on `<body>` for the event layer to read.

Set GA4_ID to a real "G-XXXXXXXXXX" measurement ID to switch analytics on. While
it is empty, events still fire into `window.dataLayer` so they can be inspected in
the console, but nothing leaves the browser.
"""
import re

import data as D

GA4_ID = ""          # launch step: paste the GA4 measurement ID here

# Substituted per page by stamp(). Kept out of the visible character range so a
# stray token in the output is obvious and the gate can fail on it.
PT = "__PAGETYPE__"

UTM = ("utm_source=veneta&amp;utm_medium=referral&amp;utm_campaign=brand_handoff"
       "&amp;utm_content=")


# --------------------------------------------------------------------------- §9.3
# One line of expectation-setting sits under every primary retail CTA.
TRUST = ("Configure size, opacity and lift on Home Depot. "
         "Veneta helps you decide before you buy.")

TRUST_P = f'<p class="hd-trust">{TRUST}</p>'


def _slug(s):
    """Normalise to a safe analytics value. Hyphens and underscores survive, so a
    category value is the product slug itself and joins straight to page data."""
    return re.sub(r"[^a-z0-9_-]+", "-", (s or "").lower()).strip("-_") or ""


def href(key="brand", module="body", category=""):
    """Retail URL with UTMs. `module` names the block the link sits in."""
    if key not in D.HD_LINKS:
        raise KeyError(f"HD_LINKS has no key {key!r}")
    base = D.HD_LINKS[key]
    cat = _slug(category or key)
    joiner = "&amp;" if "?" in base else "?"
    # dot-separated so the three fields survive a round trip: page_type, module and
    # category are all slugified to [a-z0-9_], so a dot never appears inside one.
    return f"{base}{joiner}{UTM}{PT}.{_slug(module)}.{cat}"


def btn(label="Shop at The Home Depot", key="brand", module="body",
        category="", cls="btn btn--hd", style="", extra=""):
    """A retail CTA. data-hd is added by stamp() from the utm_content value."""
    st = f' style="{style}"' if style else ""
    ex = f" {extra}" if extra else ""
    return (f'<a class="{cls}" href="{href(key, module, category)}"'
            f'{st}{ex}>{label}</a>')


def trust(align=""):
    """§9.3 trust line, for placing directly under a primary CTA."""
    st = ' style="text-align:center"' if align == "center" else ""
    return f'<p class="hd-trust"{st}>{TRUST}</p>'


# --------------------------------------------------------------------------- §10
# page_type and category for every page. page_type feeds the GA4 custom dimension
# of the same name and the utm_content string; category scopes spec_table_view,
# swatch_select and guide_read. handoffgate.py fails if a written page is missing.

PAGE_META = {
    "index.html":                            ("home", ""),
    "products.html":                         ("catalog", ""),

    "cellular-shades.html":                  ("category", "cellular-shades"),
    "roller-solar-shades.html":              ("category", "roller-solar-shades"),
    "roman-shades.html":                     ("category", "roman-shades"),
    "faux-wood-blinds.html":                 ("category", "faux-wood-blinds"),
    "shutters.html":                         ("category", "shutters"),
    "sheer-shades.html":                     ("category", "sheer-shades"),
    "vertical-blinds.html":                  ("category", "vertical-blinds"),
    "dualdrape.html":                        ("product_family", "dualdrape"),

    "shop-by-room.html":                     ("room_hub", ""),
    "shop-by-need.html":                     ("need_hub", ""),
    "product-finder.html":                   ("tool", ""),
    "inspiration.html":                      ("gallery", ""),
    "free-samples.html":                     ("samples", ""),
    "where-to-buy.html":                     ("retail", ""),

    "buying-guides.html":                    ("guide_hub", ""),
    "faux-wood-guide.html":                  ("guide", "faux-wood-blinds"),
    "roman-cordless-guide.html":             ("guide", "roman-shades"),
    "cordless-roller-shades-guide.html":     ("guide", "roller-solar-shades"),
    "how-to-measure.html":                   ("guide", "measure"),
    "how-to-install.html":                   ("guide", "install"),
    "how-to-clean.html":                     ("guide", "clean"),

    "support.html":                          ("support", ""),
    "faq.html":                              ("support", ""),
    "warranty.html":                         ("support", ""),
    "contact.html":                          ("support", ""),
    "installation-videos.html":              ("support", "install"),
    "installation-videos-l-frame.html":      ("support", "install"),
    "installation-videos-deco-frame.html":   ("support", "install"),

    "motorization.html":                     ("topic", "motorization"),
    "child-safety.html":                     ("topic", "child-safety"),
    "clearfit.html":                         ("technology", "clearfit"),
    "smartrail.html":                        ("technology", "smartrail"),
    "smartprivacy.html":                     ("technology", "smartprivacy"),
    "truquiet-motorization.html":            ("technology", "truquiet"),
    "innovation.html":                       ("technology", ""),

    "for-professionals.html":                ("trade", ""),
    "about.html":                            ("company", ""),
    "journal.html":                          ("journal_hub", ""),
    "journal-beat-summer-heat.html":         ("journal", ""),
    "journal-bellevue-coastal-colors.html":  ("journal", ""),
    "journal-faux-wood-decor.html":          ("journal", ""),
    "journal-gray-is-the-new-white.html":    ("journal", ""),
    "journal-spring-cleaning.html":          ("journal", ""),

    "terms-and-conditions.html":             ("legal", ""),
    "privacy-policy.html":                   ("legal", ""),
    "accessibility.html":                    ("legal", ""),
    "sitemap.html":                          ("utility", ""),
    "404.html":                              ("utility", ""),
}


def meta(name):
    return PAGE_META.get(name, ("other", ""))


# --------------------------------------------------------------------------- GA4
def ga4_head():
    """Consent Mode v2 defaults deny storage until a banner grants it, so the tag
    is compliant before the banner exists. gtag is always defined, so the event
    layer needs no null checks."""
    boot = ("window.dataLayer=window.dataLayer||[];"
            "function gtag(){dataLayer.push(arguments);}"
            "gtag('consent','default',{'ad_storage':'denied','ad_user_data':'denied',"
            "'ad_personalization':'denied','analytics_storage':'denied',"
            "'wait_for_update':500});"
            "gtag('js',new Date());")
    if not GA4_ID:
        return (f"<script>{boot}</script>\n"
                "<!-- GA4 tag not loaded: build/hd.py GA4_ID is empty (mockup). "
                "Events still fire into window.dataLayer for inspection. -->\n")
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>\n'
            f"<script>{boot}"
            f"gtag('config','{GA4_ID}',{{'page_type':'{PT}'}});</script>\n")


# ------------------------------------------------------------------------- stamp
_A = re.compile(r'<a\b[^>]*\bhref="https://www\.homedepot\.com[^"]*"[^>]*>')
_UC = re.compile(r"utm_content=([^\"&]+)")


def _add_hd(tag):
    if "data-hd=" in tag:
        return tag
    m = _UC.search(tag)
    if not m:
        return tag
    parts = m.group(1).split(".")
    while len(parts) < 3:
        parts.append("")
    return tag[:-1] + f' data-hd="{parts[0]}|{parts[1]}|{parts[2]}">'


def stamp(name, html):
    """Resolve the page-type token, hook every retail anchor, label the body."""
    page_type, category = meta(name)
    html = html.replace(PT, page_type)
    html = _A.sub(lambda m: _add_hd(m.group(0)), html)
    html = html.replace(
        "<body>",
        f'<body data-page-type="{page_type}" data-category="{category}">', 1)
    return html
