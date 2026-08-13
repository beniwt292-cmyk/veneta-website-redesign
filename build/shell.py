"""Shared page shell + component helpers for the VENETA redesign mockup."""

HD = "https://www.homedepot.com/b/VENETA/N-5yc1vZryk"

NAV = [
    ("Products", "products.html", "products"),
    ("Shop By", "shop-by-room.html", "shopby"),
    ("Innovation", "innovation.html", "innovation"),
    ("Inspiration", "inspiration.html", "inspiration"),
    ("Support", "support.html", "support"),
    ("Where to Buy", "where-to-buy.html", "buy"),
]

MNAV = [
    ("Products", "products.html"),
    ("Shop by Room", "shop-by-room.html"),
    ("Shop by Need", "shop-by-need.html"),
    ("Product Finder", "product-finder.html"),
    ("Innovation", "innovation.html"),
    ("Inspiration", "inspiration.html"),
    ("Support", "support.html"),
    ("Where to Buy", "where-to-buy.html"),
]


def head(title, desc, css="assets/css/veneta.css"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<p class="mocknote">Redesign mockup &middot; not the live VENETA&trade; site &middot; photography, prices and reviews are placeholders</p>
"""


def header(active=""):
    links = "".join(
        f'<a href="{u}"{" class=\"on\"" if k == active else ""}>{n}</a>' for n, u, k in NAV
    )
    mlinks = "".join(
        f'<li><a href="{u}">{n}</a></li>' for n, u in MNAV
    )
    return f"""
<header>
  <div class="bar">
    <a href="index.html" class="logo" aria-label="Veneta home">VENET<span>A</span></a>
    <nav class="main" aria-label="Primary">{links}</nav>
    <div class="hd-wrap"><a class="btn btn--hd btn--sm" href="{HD}" data-analytics="hd-outbound" data-location="header">Shop at The Home Depot</a></div>
    <button class="burger" aria-label="Open menu" aria-expanded="false" onclick="openNav()"><i></i></button>
  </div>
</header>

<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="top"><span class="logo">VENET<span>A</span></span><button class="close" aria-label="Close menu" onclick="closeNav()">&times;</button></div>
  <ul>{mlinks}</ul>
  <a class="btn btn--hd" style="width:100%;justify-content:center" href="{HD}" data-analytics="hd-outbound" data-location="mobile-nav">Shop at The Home Depot</a>
  <p style="margin-top:26px;font-size:15px;color:var(--ink-70)">Questions? Call <strong>1-855-558-1222</strong></p>
</div>

<main id="main">
"""


FOOTER = f"""
</main>

<footer>
  <div class="wrap">
    <div class="fgrid">
      <div class="fbrand">
        <span class="logo">VENET<span style="color:var(--daylight)">A</span></span>
        <p>Custom blinds, shades and shutters by Richfield Window Coverings. Sold at The Home Depot.</p>
        <p class="fcontact"><strong>1-855-558-1222</strong><br>help@venetawindowfashions.com</p>
      </div>
      <div><h4>Products</h4><ul>
        <li><a href="cellular-shades.html">Cellular Shades</a></li>
        <li><a href="roller-solar-shades.html">Roller &amp; Solar Shades</a></li>
        <li><a href="roman-shades.html">Roman Shades</a></li>
        <li><a href="faux-wood-blinds.html">Faux Wood Blinds</a></li>
        <li><a href="shutters.html">Shutters</a></li>
        <li><a href="sheer-shades.html">Sheer Shades</a></li>
        <li><a href="dualdrape.html">DualDrape&trade;</a></li>
        <li><a href="vertical-blinds.html">Vertical Blinds</a></li>
      </ul></div>
      <div><h4>Shop by</h4><ul>
        <li><a href="shop-by-room.html">Room</a></li>
        <li><a href="shop-by-need.html">Need</a></li>
        <li><a href="product-finder.html">Product Finder</a></li>
        <li><a href="free-samples.html">Free Samples</a></li>
        <li><a href="where-to-buy.html">Where to Buy</a></li>
        <li><a href="buying-guides.html">Buying Guides</a></li>
      </ul></div>
      <div><h4>Support</h4><ul>
        <li><a href="how-to-measure.html">How to Measure</a></li>
        <li><a href="how-to-install.html">How to Install</a></li>
        <li><a href="how-to-clean.html">How to Clean</a></li>
        <li><a href="installation-videos.html">Installation Videos</a></li>
        <li><a href="warranty.html">Warranty</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="contact.html">Contact Us</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="about.html">About Veneta</a></li>
        <li><a href="innovation.html">Innovation</a></li>
        <li><a href="journal.html">Journal</a></li>
        <li><a href="for-professionals.html">For Professionals</a></li>
        <li><a href="accessibility.html">Accessibility</a></li>
        <li><a href="sitemap.html">Sitemap</a></li>
      </ul></div>
    </div>
    <div class="legal">
      <span>&copy; <span id="yr"></span> Richfield Window Coverings. All rights reserved.</span>
      <a href="terms-and-conditions.html">Terms &amp; Conditions</a><a href="privacy-policy.html">Privacy Policy</a><a href="warranty.html">Warranty</a><a href="accessibility.html">Accessibility Statement</a>
    </div>
  </div>
</footer>

<div class="sticky" id="sticky">
  <a class="btn btn--hd" href="{HD}" data-analytics="hd-outbound" data-location="sticky-bar">Shop at The Home Depot</a>
  <a class="btn btn--ghost" href="free-samples.html" data-analytics="sample-request">Free samples</a>
</div>

<script src="assets/js/veneta.js" defer></script>
</body>
</html>
"""


def page(title, desc, body, active=""):
    return head(title, desc) + header(active) + body + FOOTER


# ---------------- components ----------------

def crumbs(trail):
    """trail = [(label, href_or_None), ...]"""
    out = []
    for label, href in trail:
        out.append(f'<a href="{href}">{label}</a>' if href else f"{label}")
    return '<p class="crumb">' + "<span>/</span>".join(out) + "</p>"


def phero(eyebrow, h1, lede, trail=None, ctas="", dark=False, extra=""):
    return f"""
  <div class="phero{' dark' if dark else ''}">
    <div class="wrap">
      {crumbs(trail) if trail else ''}
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      {f'<div class="cta-row">{ctas}</div>' if ctas else ''}
      {extra}
    </div>
  </div>
"""


def phero_media(eyebrow, h1, lede, img, alt, trail=None, ctas=""):
    return f"""
  <div class="phero">
    <div class="wrap">
      {crumbs(trail) if trail else ''}
      <div class="phero-media">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h1>{h1}</h1>
          <p class="lede">{lede}</p>
          {f'<div class="cta-row" style="margin-top:32px">{ctas}</div>' if ctas else ''}
        </div>
        <div><img src="assets/img/{img}" alt="{alt}"></div>
      </div>
    </div>
  </div>
"""


def anchors(items):
    row = "".join(f'<a href="#{i}">{n}</a>' for n, i in items)
    return f'<div class="anchors"><div class="row">{row}</div></div>'


SLAT = '<div class="slat" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>'


def shead(eyebrow, h2, sub="", right=""):
    return f"""<div class="shead">
        <div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>{f'<p>{sub}</p>' if sub else ''}</div>
        {right}
      </div>"""


def acc(items):
    rows = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><div class="a">{a}</div></details>'
        for i, (q, a) in enumerate(items)
    )
    return f'<div class="acc">{rows}</div>'


def steps(items, four=False):
    out = "".join(
        f'<div class="step rev"><span class="n">{str(i+1).zfill(2)}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(items)
    )
    return f'<div class="steps{" four" if four else ""}">{out}</div>'


def kv(rows):
    out = "".join(f"<div><b>{k}</b><span>{v}</span></div>" for k, v in rows)
    return f'<div class="kv">{out}</div>'


def vids(items):
    out = ""
    for title, desc, length, img in items:
        out += f"""<a class="vid rev" href="#"><div class="frame"><img src="assets/img/{img}" alt="" loading="lazy"><b></b><span class="len">{length}</span></div><h3>{title}</h3><p>{desc}</p></a>"""
    return f'<div class="vids">{out}</div>'


def tiles(items):
    out = ""
    for name, sub, img, href in items:
        out += f"""<a class="tile rev" href="{href}"><div class="ph"><img src="assets/img/{img}" alt="{name} with Veneta window treatments" loading="lazy"></div><div class="cap"><h3>{name}</h3><p>{sub}</p></div></a>"""
    return f'<div class="tiles">{out}</div>'


def cards(items):
    out = ""
    for name, desc, price, img, href, badges in items:
        b = "".join(f'<span class="badge">{x}</span>' for x in badges)
        out += f"""<a class="card rev" href="{href}">
          <div class="ph"><img src="assets/img/{img}" alt="{name} shown in a styled room" loading="lazy"></div>
          <h3>{name}</h3><p class="desc">{desc}</p><p class="price">{price}</p>
          <div class="badges">{b}</div>
        </a>"""
    return f'<div class="cards">{out}</div>'


def rowfeat(eyebrow, h2, body, img, alt, cta="", flip=False):
    return f"""<div class="rowfeat{' flip' if flip else ''} rev">
      <div class="txt"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>{body}{f'<div class="cta-row" style="margin-top:26px">{cta}</div>' if cta else ''}</div>
      <div><img src="assets/img/{img}" alt="{alt}" loading="lazy"></div>
    </div>"""


def stats(items):
    out = "".join(f'<div class="stat"><b>{v}</b><span>{l}</span></div>' for v, l in items)
    return f'<div class="stats">{out}</div>'


def cta_band(h2, body, primary=None, secondary=None, dark=True):
    p = f'<a class="btn btn--hd" href="{primary[1]}" data-analytics="hd-outbound">{primary[0]}</a>' if primary else ""
    s = f'<a class="btn btn--ghost-light" href="{secondary[1]}">{secondary[0]}</a>' if secondary else ""
    return f"""
  <section class="{'dark' if dark else ''}">
    <div class="wrap center" style="max-width:760px">
      <h2>{h2}</h2><p style="margin-top:18px">{body}</p>
      <div class="cta-row" style="justify-content:center;margin-top:30px">{p}{s}</div>
    </div>
  </section>
"""


def support_strip():
    items = [
        ("4 steps &middot; 10 minutes", "How to Measure", "Inside mount, outside mount and the one rule that saves most orders.", "how-to-measure.html"),
        ("6 steps &middot; 20 minutes", "How to Install", "Bracket diagrams and a short video for every product line.", "how-to-install.html"),
        ("By material", "How to Clean &amp; Care", "What to use on fabric, faux wood and vinyl, and what to avoid.", "how-to-clean.html"),
    ]
    out = ""
    for meta, h3, d, href in items:
        out += f'<a href="{href}"><p class="meta">{meta}</p><h3>{h3}</h3><p class="desc" style="color:var(--ink-70);margin:8px 0 0">{d}</p><span class="arrow">Read the guide</span></a>'
    return f"""
  <section id="support">
    <div class="wrap">
      {shead('Support', "Measure it, install it, keep it looking new.")}
      <div class="sgrid">{out}</div>
    </div>
  </section>
"""
