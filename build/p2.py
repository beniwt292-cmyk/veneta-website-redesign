#!/usr/bin/env python3
"""P2 — template rebuild (§7).

Replaces the P0/P1 homepage, category, product-family and gallery templates with
the section order specified in §7, built on the P1 image set.

The rhythm rule that drives every layout here: no two adjacent sections may share
a column count or a background. §1 root cause 4 was "every section is a grid of
equal cards", so the sequence alternates full-bleed image, prose split, index
grid, macro band, dark band, snap rail.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data as D
import p2data as P2D
import pic as PIC
import shell as SH
from shell import HD, crumbs, acc, shead, SLAT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SAMPLES = "free-samples.html"


def _hd(label, loc):
    return (f'<a class="btn btn--hd" href="{HD}" data-analytics="hd-outbound" '
            f'data-location="{loc}">{label}</a>')


def _ghost(label, href, light=False):
    cls = "btn btn--ghost-light" if light else "btn btn--ghost"
    return f'<a class="{cls}" href="{href}">{label}</a>'


def txt(s):
    """Strip tags for use in a meta description or an alt attribute."""
    return re.sub(r"<[^>]+>", "", s)


# =============================================================== components ===
def hero(shot, eyebrow, h1, lede, ctas, proof, tall=True):
    """Full-bleed image hero. 86vh on the homepage, 62vh on a category page."""
    media = PIC.pic(shot, cls="hero-img", lcp=True,
                    sizes="100vw") or ""
    chips = "".join(f"<span>{p}</span>" for p in proof)
    return f"""
  <div class="fhero{' fhero--tall' if tall else ''}">
    {media}
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <div class="cta-row">{ctas}</div>
      <div class="fhero-proof">{chips}</div>
    </div>
  </div>
"""


def duo(shot, eyebrow, h2, blocks, cta="", flip=False, sink=False, wide_text=False):
    """§7.1 SPLIT 5/7 and 7/5. The image bleeds to the page edge on the side it
    sits on, which is what stops this reading as two equal cards."""
    media = PIC.pic(shot, sizes="(min-width:1000px) 52vw, 100vw")
    if not media:
        return ""
    body = "".join(
        (f"<h3>{h}</h3><p>{p}</p>" if h else f"<p>{p}</p>") for h, p in blocks
    )
    cls = "duo" + (" duo--flip" if flip else "") + (" duo--wide" if wide_text else "")
    return f"""
  <section class="{cls}{' sink' if sink else ''}">
    <div class="duo-media">{media}</div>
    <div class="duo-text">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{h2}</h2>
      <div class="duo-body">{body}</div>
      {f'<div class="cta-row">{cta}</div>' if cta else ''}
    </div>
  </section>
"""


def macroband(shots, label):
    """§7.1 MACRO TEXTURE BAND — four full-bleed 3:4 material close-ups."""
    cells = ""
    for s in shots:
        m = PIC.pic(s, sizes="(min-width:900px) 25vw, 50vw")
        if m:
            cells += f'<div class="mb-cell">{m}</div>'
    if not cells:
        return ""
    return f"""
  <section class="macroband nobot">
    <p class="eyebrow macroband-lbl">{label}</p>
    <div class="mb-grid">{cells}</div>
  </section>
"""


def opacity3(items, eyebrow="Light control", h2="The same window, three ways."):
    """§7.2 OPACITY — one window at three openness levels, labelled."""
    cells = ""
    for shot, label, note in items:
        m = PIC.pic(shot, sizes="(min-width:900px) 33vw, 100vw")
        if not m:
            continue
        cells += (f'<figure class="op-cell">{m}'
                  f'<figcaption><b>{label}</b><span>{note}</span></figcaption></figure>')
    if not cells:
        return ""
    return f"""
  <section class="sink">
    <div class="wrap">
      {shead(eyebrow, h2, 'Shot on one window in one light, so the difference you see is the fabric and nothing else.')}
      <div class="op-grid">{cells}</div>
    </div>
  </section>
"""


def pindex(slugs=None, eyebrow="The collection", h2="Eight ways to control the light.",
           sub="", right=""):
    """§7.1 PRODUCT INDEX — 4:5 imagery, chips, text CTA. Not a card grid: the
    first item runs double width so the eye has somewhere to land."""
    items = [p for p in D.PRODUCTS if slugs is None or p["slug"] in slugs]
    out = ""
    for i, p in enumerate(items):
        m = PIC.pic("index-" + p["slug"], sizes="(min-width:1080px) 25vw, (min-width:640px) 50vw, 100vw")
        if not m:
            continue
        chips = "".join(f"<span>{b}</span>" for b in p["badges"][:2])
        out += f"""<a class="pi-item{' pi-item--lead' if i == 0 else ''}" href="{p['slug']}.html">
        <div class="pi-ph">{m}</div>
        <h3>{p['short']}</h3>
        <p>{p['tagline']}</p>
        <div class="pi-chips">{chips}</div>
        <span class="arrow">See the range</span>
      </a>"""
    if not out:
        return ""
    return f"""
  <section>
    <div class="wrap">
      {shead(eyebrow, h2, sub, right)}
      <div class="pi-grid">{out}</div>
    </div>
  </section>
"""


def darkband(shot, eyebrow, h2, lede, points, cta, note=""):
    """§7.1 DARK BAND — the only place --noir appears outside the footer."""
    m = PIC.pic(shot, sizes="(min-width:1000px) 58vw, 100vw")
    pts = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in points)
    return f"""
  <section class="noir">
    <div class="wrap">
      <div class="noir-top">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h2>{h2}</h2>
          <p class="lede">{lede}</p>
          <div class="cta-row">{cta}</div>
        </div>
        <div class="noir-media">{m}</div>
      </div>
      <div class="noir-pts">{pts}</div>
      {f'<p class="noir-note">{note}</p>' if note else ''}
    </div>
  </section>
"""


def roomrail(slugs, eyebrow="Rooms", h2="Start where you are standing."):
    """§7.1 ROOM RAIL — horizontal snap scroll, never a grid."""
    out = ""
    for s in slugs:
        name, sub = P2D.ROOM_SHOTS[s]
        m = PIC.pic("room-" + s, sizes="(min-width:900px) 30vw, 76vw")
        if not m:
            continue
        out += (f'<a href="shop-by-room.html#{s}"><div class="ph">{m}</div>'
                f'<span class="rr-n">{name}</span><span class="rr-s">{sub}</span></a>')
    if not out:
        return ""
    return f"""
  <section>
    <div class="wrap">{shead(eyebrow, h2)}</div>
    <div class="rail-wrap"><div class="wrap"><div class="rr">{out}</div></div></div>
  </section>
"""


def roomlinks(slugs, eyebrow="Rooms", h2="Where this one earns its keep."):
    out = ""
    for s in slugs:
        name, sub = P2D.ROOM_SHOTS[s]
        m = PIC.pic("room-" + s, sizes="(min-width:900px) 24vw, 50vw")
        if not m:
            continue
        out += (f'<a class="rl-item" href="shop-by-room.html#{s}"><div class="ph">{m}</div>'
                f'<h3>{name}</h3><p>{sub}</p></a>')
    if not out:
        return ""
    return f"""
  <section>
    <div class="wrap">
      {shead(eyebrow, h2)}
      <div class="rl-grid">{out}</div>
    </div>
  </section>
"""


def guidecards(items=None, eyebrow="Guides", h2="Read this before you measure."):
    items = items or P2D.GUIDES
    out = ""
    for href, kicker, title, desc in items:
        out += (f'<a class="gc" href="{href}"><p class="gc-k">{kicker}</p>'
                f'<h3>{title}</h3><p class="gc-d">{desc}</p>'
                f'<span class="arrow">Read the guide</span></a>')
    return f"""
  <section class="sink">
    <div class="wrap">
      {shead(eyebrow, h2)}
      <div class="gc-grid">{out}</div>
    </div>
  </section>
"""


def handoff(loc="handoff"):
    """§9 HANDOFF BAND — a premium retail partnership, stated plainly, with no
    apology and no invented pricing."""
    steps = "".join(
        f'<li><span class="n">{i+1}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (t, d) in enumerate(P2D.HANDOFF)
    )
    return f"""
  <section class="handoff">
    <div class="wrap">
      <div class="ho-head">
        <div>
          <p class="eyebrow">Where you buy it</p>
          <h2>Sold at The Home Depot, built by us.</h2>
          <p class="lede">Veneta is stocked and sold exclusively through The Home Depot. You order
          there; the shade is cut to your measurements here.</p>
        </div>
        <div class="cta-row">
          {_hd('Shop at The Home Depot', loc)}
          {_ghost('Measure &amp; install help', 'support.html')}
        </div>
      </div>
      <ol class="ho-steps">{steps}</ol>
    </div>
  </section>
"""


def audience_split():
    """§7.1 final split — For designers / For commercial."""
    a = PIC.pic("trade-office-meeting", sizes="(min-width:900px) 48vw, 100vw")
    b = PIC.pic("trade-hospitality-room", sizes="(min-width:900px) 48vw, 100vw")
    return f"""
  <section class="aud">
    <div class="wrap">
      <div class="aud-grid">
        <a class="aud-item" href="for-professionals.html">
          <div class="ph">{a}</div>
          <p class="eyebrow">For designers</p>
          <h3>Specification library, sample kits and lead times</h3>
          <p>Published size ranges for every line, a trade sample kit and a named contact for
          project quantities.</p>
          <span class="arrow">Go to trade</span>
        </a>
        <a class="aud-item" href="for-professionals.html#commercial">
          <div class="ph">{b}</div>
          <p class="eyebrow">For commercial</p>
          <h3>Multifamily, hospitality, office and healthcare</h3>
          <p>Capability statement, published spec ranges and a project inquiry route that does not
          go through a retail store.</p>
          <span class="arrow">Commercial enquiries</span>
        </a>
      </div>
    </div>
  </section>
"""


def chiprow(chips):
    out = "".join(f"<span>{c}</span>" for c in chips)
    return f'<div class="attrs"><div class="wrap"><div class="attrs-row">{out}</div></div></div>'


def compare(slug):
    """§7.2 COMPARE — this category plus its two closest rivals. Five columns max."""
    if slug not in P2D.CMP:
        return ""
    slugs = [slug] + P2D.CAT[slug]["rivals"]
    names = {p["slug"]: p["short"] for p in D.PRODUCTS}
    head = "".join(
        f'<th scope="col"{" class=self" if s == slug else ""}>'
        f'{"" if s == slug else f"<a href={chr(34)}{s}.html{chr(34)}>"}{names[s]}'
        f'{"" if s == slug else "</a>"}</th>'
        for s in slugs
    )
    rows = ""
    for i, label in enumerate(P2D.CMP_ROWS):
        cells = ""
        for s in slugs:
            v = P2D.CMP[s][i]
            cells += (f'<td class="{v}{" self" if s == slug else ""}">'
                      f'{P2D.CMP_LABEL[v]}</td>')
        rows += f'<tr><th scope="row">{label}</th>{cells}</tr>'
    return f"""
  <section>
    <div class="wrap">
      {shead('Compare', 'Against the two it is usually weighed against.')}
      <div class="scrollx"><table class="cmp2"><thead><tr><td></td>{head}</tr></thead>
      <tbody>{rows}</tbody></table></div>
      <p class="tnote">Partial means the effect is real but not complete: a closed slat or vane
      still passes some light at the edges. Blackout is only claimed where a fabric and a seal
      deliver it.</p>
    </div>
  </section>
"""


def swatches(p):
    sw = "".join(
        f'<div class="sw2"><span style="background:{h}"></span><b>{n}</b></div>'
        for n, h in p["colors"]
    )
    return f"""
  <section class="sink">
    <div class="wrap">
      {shead('Materials', 'Eight of the range, shown flat.',
             'A screen cannot show openness or hand. Order the swatch and tape it to the glass before you order the shade.')}
      <div class="sw2-grid">{sw}</div>
      <div class="cta-row" style="margin-top:32px">{_ghost('Order up to 8 free samples', SAMPLES)}</div>
    </div>
  </section>
"""


def spectable(p, note=""):
    rows = "".join(f"<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in p["spec"])
    return f"""
  <section id="specs">
    <div class="wrap">
      {shead('Specifications', 'The numbers, not the adjectives.',
             'Full published range, on the page, not behind a tab.')}
      <div class="scrollx"><table class="spec2"><tbody>{rows}</tbody></table></div>
      <p class="tnote">{note or 'Sizes shown are the full manufacturing range. Not every fabric is offered at every size, and pricing is set by The Home Depot.'}</p>
    </div>
  </section>
"""


def safetystrip(p):
    cordless = any("ordless" in b for b in p["badges"])
    line = ("Cordless lift is standard on this line, not a paid upgrade."
            if cordless else
            "This line is operated by a cordless wand, so there is no lift cord in the room.")
    m = PIC.pic("safety-nursery-cordless", sizes="(min-width:900px) 44vw, 100vw")
    return f"""
  <section class="sink safety2">
    <div class="wrap">
      <div class="s2-grid">
        <div>
          <p class="eyebrow">Child &amp; pet safety</p>
          <h2>No cord in reach.</h2>
          <p>{line} Corded window coverings remain a strangulation hazard for young children,
          which is why the cordless option is the default here and not an option you have to find.</p>
          <p class="tnote">Guidance published by the U.S. Consumer Product Safety Commission
          recommends cordless window coverings in any home with young children.</p>
          <div class="cta-row">{_ghost('Our safety position', 'child-safety.html')}</div>
        </div>
        <div class="s2-media">{m}</div>
      </div>
    </div>
  </section>
"""


def faqs(p):
    return f"""
  <section>
    <div class="wrap">
      <div class="faq-grid">
        <div>{shead('FAQ', 'Asked often, answered plainly.')}
        <p class="tnote">If the answer you need is not here, the full list covers every line.</p>
        <div class="cta-row">{_ghost('All questions', 'faq.html')}</div></div>
        <div>{acc(p["faqs"])}</div>
      </div>
    </div>
  </section>
"""


# ==================================================================== home ====
def build_home(write, page):
    finder = """
  <div class="finder" id="finder">
    <div class="wrap">
      <div class="finder-head">
        <p class="eyebrow">Product finder</p>
        <h2>Three questions, then three products.</h2>
      </div>
      <form class="finder-grid" action="product-finder.html" method="get">
        <div class="field"><label for="f-room">Room</label>
          <select id="f-room" name="room"><option>Living room</option><option>Bedroom</option><option>Nursery</option><option>Kitchen</option><option>Bathroom</option><option>Home office</option><option>Patio door</option></select></div>
        <div class="field"><label for="f-need">What matters most</label>
          <select id="f-need" name="need"><option>Block all light</option><option>Soften the light</option><option>Keep the view</option><option>Insulate the window</option><option>Privacy</option><option>Child &amp; pet safety</option><option>Humid room</option></select></div>
        <div class="field"><label for="f-look">Look</label>
          <select id="f-look" name="look"><option>Clean and modern</option><option>Soft folds</option><option>Natural wood</option><option>Sheer and airy</option><option>Architectural</option></select></div>
        <button class="btn" type="submit" data-analytics="finder-submit">See my matches</button>
      </form>
    </div>
  </div>
"""

    spec_preview = """
      <div class="scrollx"><table class="spec2 spec2--tight">
        <caption class="eyebrow">Cellular shades &mdash; published size range</caption>
        <thead><tr><th scope="col">Configuration</th><th scope="col">Width</th><th scope="col">Height</th></tr></thead>
        <tbody>
          <tr><th scope="row">Cordless, bottom-up</th><td>18&quot; &ndash; 96&quot;</td><td>24&quot; &ndash; 108&quot;</td></tr>
          <tr><th scope="row">Top-down / bottom-up</th><td>18&quot; &ndash; 96&quot;</td><td>24&quot; &ndash; 108&quot;</td></tr>
          <tr><th scope="row">ClearFit&trade; French door</th><td>8.5&quot; &ndash; 72&quot;</td><td>6&quot; &ndash; 86&quot;</td></tr>
          <tr><th scope="row">TruQuiet&trade; motorized</th><td>24&quot; &ndash; 120&quot;</td><td>10&quot; &ndash; 138&quot;</td></tr>
        </tbody>
      </table></div>
"""

    body = hero(
        "hero-home",
        "Custom blinds, shades &amp; shutters",
        "Light, exactly where you <em>want</em> it.",
        "Custom shades, blinds and shutters built to published specifications and sold "
        "through The Home Depot.",
        _hd("Shop at The Home Depot", "hero") + _ghost("Order free samples", SAMPLES, light=True),
        ["Cordless by default", "Published specs", "Made to size"],
    )
    body += finder

    body += f"""
  <section class="duo duo--wide">
    <div class="duo-media">{PIC.pic('macro-cellular-bone', sizes='(min-width:1000px) 46vw, 100vw')}</div>
    <div class="duo-text">
      <p class="eyebrow">Engineered to fit</p>
      <h2>We publish what others hide.</h2>
      <div class="duo-body">
        <p>Exact width and height ranges for every cell size and lift system, on the page,
        before you buy. If a window is outside the range we say so instead of letting the
        order fail at the plant.</p>
      </div>
      {spec_preview}
      <div class="cta-row">{_ghost('See all specifications', 'cellular-shades.html#specs')}</div>
    </div>
  </section>
"""

    body += pindex(
        sub="Every line is made to your measurements, ships cordless by default and carries a "
            "limited lifetime warranty.",
        right=_ghost("All products", "products.html"),
    )
    body += macroband(P2D.HOME_MACROS, "Materials &middot; weave, opacity, hand")

    body += duo(
        "safety-playroom",
        "Child &amp; pet safety",
        "Cordless where it matters.",
        [("", "Cordless lift is the standard across every line, not an upgrade you have to find "
              "in a dropdown. Roman shades are cord-free at the back as well as the front."),
         ("", "Where a window is genuinely out of reach, a motor removes the pull entirely.")],
        cta=_ghost("Our safety position", "child-safety.html"),
        flip=True,
    )

    body += darkband(
        "motor-dusk-bedroom",
        "Motorization",
        "Every shade in the house, at one time of day.",
        "Rechargeable TruQuiet&trade; motors, grouped by room, on a schedule or a single remote. "
        "No wiring and no batteries to buy.",
        [("Quiet enough for a nursery", "Tuned in-house to run under the noise floor of a sleeping room."),
         ("Grouped by room", "Set a whole facade in one command instead of shade by shade."),
         ("Charges in place", "Wired or wireless charging for the built-in lithium cell.")],
        _ghost("Explore motorization", "motorization.html", light=True),
        note="<strong>Smart-home compatibility, stated once:</strong> support depends on your motor "
             "and hub combination. The <a href=\"motorization.html\">motorization page</a> holds the "
             "current list and is the only place we maintain it.",
    )

    body += roomrail(P2D.HOME_ROOMS)
    body += guidecards()
    body += handoff("home-handoff")
    body += audience_split()

    write("index.html", page(
        "VENETA&trade; &mdash; Custom Blinds, Shades &amp; Shutters",
        "Custom blinds, shades and shutters built to published specifications, cordless by "
        "default, sold through The Home Depot.",
        body, active="home"))


# ================================================================ category ====
def build_category(p, write, page):
    slug = p["slug"]
    c = P2D.CAT[slug]
    short = p["short"]

    body = f'<div class="crumb-bar"><div class="wrap">{crumbs([("Home", "index.html"), ("Products", "products.html"), (short, None)])}</div></div>'
    body += hero(
        "category-" + slug,
        short,
        p["tagline"],
        p["lede"],
        _hd(f"Shop {short.lower()} at The Home Depot", f"cat-{slug}")
        + _ghost("Order free samples", SAMPLES, light=True),
        p["badges"][:3],
        tall=False,
    )
    body += chiprow(c["chips"])

    body += duo(
        c["split"],
        "Why " + short.lower(),
        c["why_h2"],
        c["why"],
        cta=_ghost("Jump to specifications", "#specs"),
    )

    body += opacity3(c["opacity"])
    body += spectable(p)
    body += swatches(p)
    body += macroband(c["macros"], "Materials &middot; " + txt(short).lower())
    body += roomlinks(c["rooms"])
    body += compare(slug)
    body += safetystrip(p)
    body += faqs(p)
    body += handoff(f"cat-{slug}-handoff")
    body += guidecards()

    write(slug + ".html", page(
        f"{short} &mdash; Custom, Cordless, Made to Fit | VENETA&trade;",
        f"{txt(short)} made to your measurements. {txt(p['tagline'])} Published size ranges, "
        f"materials, room guidance and FAQs.",
        body, active="products"))


# ========================================================== product family ====
def build_family(p, write, page):
    """§7.3 — gallery left, summary right, then feature story, specs, materials."""
    slug = p["slug"]
    c = P2D.CAT[slug]
    short = p["short"]

    shots = [("category-" + slug, f"{txt(short)} across a wide patio door")]
    shots += [(s, "Material close-up") for s in c["macros"][:3]]
    main = PIC.pic(shots[0][0], img_id="gal-main", lcp=True,
                   sizes="(min-width:1000px) 58vw, 100vw")
    thumbs = ""
    for i, (s, alt) in enumerate(shots):
        t = PIC.pic(s, sizes="120px")
        if t:
            files = re.search(r'src="([^"]+)"', t)
            thumbs += (f'<button type="button" data-src="{files.group(1)}" data-alt="{alt}" '
                       f'aria-label="View image {i+1}"{" aria-current=true" if i == 0 else ""}>{t}</button>')

    summary = [
        ("Best for", "Patio doors, sliders and window walls from 36&quot; to 192&quot; wide"),
        ("Light control", "Sheer to solid by rotating the vane; no second layer"),
        ("Operation", "Cordless wand, rotate then traverse"),
        ("Widths", "36&quot; to 192&quot;"),
        ("Heights", "36&quot; to 120&quot;"),
    ]
    rows = "".join(f"<div><b>{k}</b><span>{v}</span></div>" for k, v in summary)

    body = f'<div class="crumb-bar"><div class="wrap">{crumbs([("Home", "index.html"), ("Products", "products.html"), (short, None)])}</div></div>'
    body += f"""
  <section class="pf tight">
    <div class="wrap">
      <div class="pf-grid">
        <div class="pf-gal">
          <div class="pf-main">{main}</div>
          <div class="gal-thumbs pf-thumbs">{thumbs}</div>
        </div>
        <div class="pf-sum">
          <p class="eyebrow">Product family</p>
          <h1>{short}</h1>
          <p class="lede">{p["lede"]}</p>
          <div class="kv2">{rows}</div>
          <div class="cta-row">
            {_hd('Configure at The Home Depot', f'pf-{slug}')}
            {_ghost('Order free samples', SAMPLES)}
          </div>
          <p class="tnote">Pricing is set by The Home Depot and depends on width, height, fabric
          and stack. Nothing is sold on this site.</p>
        </div>
      </div>
    </div>
  </section>
"""
    body += duo(
        c["split"],
        "How it works",
        c["why_h2"],
        c["why"],
        cta=_ghost("Jump to specifications", "#specs"),
        flip=True,
    )
    body += spectable(p)
    body += swatches(p)
    body += macroband(c["macros"], "Materials &middot; " + txt(short).lower())
    body += compare(slug)
    body += safetystrip(p)
    body += faqs(p)
    body += handoff(f"pf-{slug}-handoff")
    body += guidecards()

    write(slug + ".html", page(
        f"{short} &mdash; Sheer to Solid on One Track | VENETA&trade;",
        f"{txt(short)}: {txt(p['tagline'])} Published widths to 192&quot;, cordless wand control, "
        f"washable vanes.",
        body, active="products"))


# ================================================================= gallery ====
def build_gallery(write, page):
    """§7.4 — mixed-aspect grid, never uniform, one feature every nine tiles."""
    sizes = {
        "portrait": "(min-width:1080px) 32vw, (min-width:640px) 50vw, 100vw",
        "landscape": "(min-width:1080px) 46vw, 100vw",
        "square": "(min-width:1080px) 22vw, 50vw",
    }
    tiles, n = "", 0
    for shot, aspect, room, product, href in P2D.GALLERY:
        m = PIC.pic(shot, sizes=sizes[aspect])
        if not m:
            continue
        n += 1
        tiles += f"""<a class="gt gt--{aspect}" href="{href}">
        <div class="ph">{m}</div>
        <div class="gt-cap"><b>{room}</b><span>{product}</span></div></a>"""
        if n in P2D.GAL_FEATURES:
            fshot, kicker, title, desc, credit, fhref = P2D.GAL_FEATURES[n]
            fm = PIC.pic(fshot, sizes="100vw")
            if fm:
                tiles += f"""<div class="gt-feature">
        <div class="ph">{fm}</div>
        <div class="gf-txt"><p class="eyebrow">{kicker}</p><h2>{title}</h2><p>{desc}</p>
        <p class="gf-credit">{credit}</p>
        <a class="arrow" href="{fhref}">See the products used</a></div></div>"""

    filters = ""
    for label, opts in P2D.GAL_FILTERS:
        o = "".join(f"<option>{x}</option>" for x in opts)
        fid = "gf-" + label.lower().replace(" ", "-")
        filters += (f'<div class="field"><label for="{fid}">{label}</label>'
                    f'<select id="{fid}"><option>All</option>{o}</select></div>')

    body = f"""
  <div class="crumb-bar"><div class="wrap">{crumbs([("Home", "index.html"), ("Inspiration", None)])}</div></div>
  <section class="gal-head tight">
    <div class="wrap">
      <p class="eyebrow">Inspiration</p>
      <h1>Rooms where the light was the point.</h1>
      <p class="lede">Real configurations, shot in one consistent daylight. Every frame links to
      the product actually used in it.</p>
    </div>
  </section>
  <div class="galbar"><div class="wrap"><div class="galbar-row">{filters}
    <p class="galbar-note">Filters are illustrative in this build. Every tile already links to its product.</p>
  </div></div></div>
  <section class="nobot"><div class="wrap"><div class="gt-grid">{tiles}</div></div></section>
  {handoff('gallery-handoff')}
  {guidecards()}
"""
    write("inspiration.html", page(
        "Inspiration &mdash; Rooms, Materials &amp; Light | VENETA&trade;",
        "A gallery of Veneta shades, blinds and shutters in real rooms, by product, room, style "
        "and light control.",
        body, active="inspiration"))
