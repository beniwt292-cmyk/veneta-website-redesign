#!/usr/bin/env python3
"""Builds the full multi-page VENETA redesign mockup into the repo root."""
import json, os, re, shutil, sys
import shell as SH
import pic as PIC
import seo as SEO
import hd as HD
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (page, crumbs, phero, phero_media, anchors, SLAT, shead, acc,
                   steps, kv, vids, tiles, cards, rowfeat, stats, cta_band, support_strip)
import data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
written = []


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"&[a-z]+;|&#\d+;", "", s.lower())).strip("-")


def write(name, html):
    html = PIC.upgrade(html)
    html = SEO.inject(name, html)   # §6.4: canonical, Open Graph, JSON-LD, outbound rels
    html = HD.stamp(name, html)     # §9/§10: page type, retail hooks, body dimensions
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(html)
    if name not in written:      # inspiration.html is built by P0 then replaced by §7.4
        written.append(name)


# ---------------------------------------------------------------- stylesheet + js
def build_assets():
    os.makedirs(os.path.join(ROOT, "assets/css"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "assets/js"), exist_ok=True)
    css = "".join(open(os.path.join(B, f)).read() for f in ("tokens.css", "components.css", "pages.css"))
    open(os.path.join(ROOT, "assets/css/veneta.css"), "w").write(css)
    js = """
document.querySelectorAll('#yr').forEach(function(e){e.textContent=new Date().getFullYear();});
function openNav(){document.getElementById('mnav').classList.add('on');document.body.style.overflow='hidden';}
function closeNav(){document.getElementById('mnav').classList.remove('on');document.body.style.overflow='';}
document.querySelectorAll('.mnav a').forEach(function(a){a.addEventListener('click',closeNav);});
addEventListener('keydown',function(e){if(e.key==='Escape')closeNav();});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});
document.querySelectorAll('.rev').forEach(function(el,i){el.style.transitionDelay=(i%4*60)+'ms';io.observe(el);});
var hdr=document.querySelector('header');
if(hdr){var setStuck=function(){hdr.classList.toggle('stuck',scrollY>8);};setStuck();addEventListener('scroll',setStuck,{passive:true});}
var bar=document.getElementById('sticky');
if(bar){addEventListener('scroll',function(){var p=scrollY/(document.body.scrollHeight-innerHeight);bar.classList.toggle('on',p>0.12&&p<0.94);},{passive:true});}
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')==='true'?'false':'true');});});
document.querySelectorAll('form[data-mock]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var n=f.querySelector('.mockmsg');if(n){n.hidden=false;}});});
document.querySelectorAll('.gal-thumbs button').forEach(function(b){b.addEventListener('click',function(){var m=document.getElementById('gal-main');if(!m)return;var pp=m.parentNode;if(pp&&pp.tagName==='PICTURE'){pp.querySelectorAll('source').forEach(function(s){s.remove();});}m.src=b.dataset.src;m.alt=b.dataset.alt||m.alt;});});
"""
    js = js.strip() + "\n" + interactive_js()
    js += "\n" + open(os.path.join(B, "analytics.js")).read()   # §10 measurement layer
    open(os.path.join(ROOT, "assets/js/veneta.js"), "w").write(js)


# ---------------------------------------------------------------- home
HOME_LINKS = [
    "products.html", "cellular-shades.html", "roller-solar-shades.html", "roman-shades.html",
    "faux-wood-blinds.html", "shutters.html", "sheer-shades.html", "dualdrape.html",
    "vertical-blinds.html", "child-safety.html", "motorization.html",
    "shop-by-room.html#living-room", "shop-by-room.html#bedroom", "shop-by-room.html#nursery",
    "shop-by-room.html#kitchen", "shop-by-room.html#patio-doors", "shop-by-room.html#home-office",
    "shop-by-room.html#bathroom",
    "how-to-measure.html", "how-to-install.html", "how-to-clean.html", "free-samples.html",
]


def build_home():
    body = open(os.path.join(B, "home.html")).read()
    it = iter(HOME_LINKS)
    body = re.sub(r'href="#"', lambda m: 'href="%s"' % next(it), body)
    body = body.replace('href="#finder"', 'href="product-finder.html"')
    write("index.html", page(
        "VENETA&trade; Window Fashions &mdash; Custom Blinds, Shades &amp; Shutters",
        "Custom blinds, shades and shutters engineered to fit, cordless by design, available at The Home Depot.",
        body, active="home"))



def interactive_js():
    """interactive.js with the recommendation + filter data injected."""
    import interactive_data as I
    prods = {}
    for p in D.PRODUCTS:
        prods[p["slug"]] = {
            "name": p["short"],
            "desc": p["tagline"],
            "price": p["price"],
            "img": p["card"],
            "badges": p["badges"][:2],
            "wide": p["slug"] in I.WIDE,
        }
    payload = {
        "products": prods,
        "room": I.ROOM,
        "need": I.NEED,
        "look": I.LOOK,
        "lift": I.LIFT,
    }
    src = open(os.path.join(B, "interactive.js")).read()
    return src.replace("/*__DATA__*/{}", json.dumps(payload, separators=(",", ":")))


def build_search_index():
    """Scan the written pages for title + description and emit a search index."""
    out = []
    priority = ["products.html", "product-finder.html", "cellular-shades.html",
                "roller-solar-shades.html", "how-to-measure.html", "support.html",
                "where-to-buy.html", "free-samples.html"]
    for name in written:
        if name in ("404.html", "sitemap.html"):
            continue
        html = open(os.path.join(ROOT, name)).read()
        t = re.search(r"<title>(.*?)</title>", html, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        if not t:
            continue
        title = re.sub(r"\s*\|.*$", "", t.group(1))
        title = re.sub(r"\s*&mdash;.*$", "", title).strip()
        desc = (d.group(1) if d else "").strip()
        out.append({"t": unes(title), "d": unes(desc), "u": name})
    out.sort(key=lambda r: (priority.index(r["u"]) if r["u"] in priority else 99, r["t"]))
    js = "window.VENETA_INDEX=" + json.dumps(out, separators=(",", ":")) + ";"
    open(os.path.join(ROOT, "assets/js/search-index.js"), "w").write(js)


def unes(x):
    for a, b in (("&amp;", "&"), ("&mdash;", "\u2014"), ("&trade;", "\u2122"),
                 ("&reg;", "\u00ae"), ("&middot;", "\u00b7"), ("&quot;", '"'),
                 ("&ndash;", "\u2013"), ("&#39;", "'")):
        x = x.replace(a, b)
    return x

# ---------------------------------------------------------------- products index
def build_products():
    body = phero(
        "All products",
        "Eight ways to control the light in a room.",
        "Every product is made to your measurements, ships cordless by default and carries a limited lifetime warranty. Start from the category, or answer three questions and let the finder narrow it down.",
        trail=[("Home", "index.html"), ("Products", None)],
        ctas=f'<a class="btn" href="product-finder.html">Use the product finder</a><a class="btn btn--ghost" href="free-samples.html">Order free samples</a>',
    )
    import interactive_data as I
    chips = "".join(f'<button class="chip" type="button" aria-pressed="false" data-tag="{t}">{c}</button>'
                    for c, t in I.CHIPS)
    body += f"""
  <section>
    <div class="wrap">
      {shead('Filter', 'Narrow it down.', 'Pick the attributes that matter. The grid updates instantly, no page reload.')}
      <div class="chips" data-filter>{chips}</div>
      <div class="filter-bar">
        <p id="filter-count" aria-live="polite">All 8 products</p>
        <button class="arrow" type="button" id="filter-reset" hidden>Clear filters</button>
      </div>
      <div id="filter-grid" data-empty="No single product does all of that. Try clearing one filter, or use the product finder.">{cards(D.card_tuples())}</div>
    </div>
  </section>
  {SLAT}
  <section>
    <div class="wrap">
      {shead('Compare', 'Which one fits the problem?')}
      <div class="scrollx"><table class="cmp">
        <thead><tr><th>Product</th><th>Blackout</th><th>Keeps the view</th><th>Wet rooms</th><th>Patio doors</th><th>Motorized</th></tr></thead>
        <tbody>
          <tr><th><a href="cellular-shades.html">Cellular Shades</a></th><td class="y">Yes</td><td class="n">No</td><td class="n">No</td><td class="n">No</td><td class="y">Yes</td></tr>
          <tr><th><a href="roller-solar-shades.html">Roller &amp; Solar</a></th><td class="y">Yes</td><td class="y">Yes</td><td class="n">No</td><td class="n">No</td><td class="y">Yes</td></tr>
          <tr><th><a href="roman-shades.html">Roman Shades</a></th><td class="y">Yes</td><td class="n">No</td><td class="n">No</td><td class="n">No</td><td class="y">Yes</td></tr>
          <tr><th><a href="faux-wood-blinds.html">Faux Wood Blinds</a></th><td class="n">Partial</td><td class="y">Yes</td><td class="y">Yes</td><td class="n">No</td><td class="y">Yes</td></tr>
          <tr><th><a href="shutters.html">Shutters</a></th><td class="n">Partial</td><td class="y">Yes</td><td class="y">Yes</td><td class="y">Yes</td><td class="n">No</td></tr>
          <tr><th><a href="sheer-shades.html">Sheer Shades</a></th><td class="n">Partial</td><td class="y">Yes</td><td class="n">No</td><td class="n">No</td><td class="y">Yes</td></tr>
          <tr><th><a href="dualdrape.html">DualDrape&trade;</a></th><td class="n">Partial</td><td class="y">Yes</td><td class="n">No</td><td class="y">Yes</td><td class="n">No</td></tr>
          <tr><th><a href="vertical-blinds.html">Vertical Blinds</a></th><td class="n">Partial</td><td class="y">Yes</td><td class="y">Yes</td><td class="y">Yes</td><td class="n">No</td></tr>
        </tbody>
      </table></div>
      <p class="tnote">Pricing is set by The Home Depot and varies by size, fabric and lift option. Configure your window there for an exact price.</p>
    </div>
  </section>
  {cta_band("Not sure yet? Get the fabric in your hand.",
            "Order up to eight free swatches and tape them to the window. It is the only reliable way to judge colour and openness.",
            ("Order free samples", "free-samples.html"), ("Use the finder", "product-finder.html"))}
"""
    write("products.html", page("All Products &mdash; Blinds, Shades &amp; Shutters | VENETA&trade;",
                                "Compare all eight Veneta product lines: cellular, roller and solar, Roman, faux wood, shutters, sheer, DualDrape and vertical blinds.",
                                body, active="products"))


# ---------------------------------------------------------------- PDPs
def build_pdp(p):
    others = [x["slug"] for x in D.PRODUCTS if x["slug"] != p["slug"]][:4]
    sw = "".join(f'<span class="sw" data-name="{n}" style="background:{h}" title="{n}"></span>' for n, h in p["colors"])
    feats = "".join(f'<div class="rev"><h3>{t}</h3><p style="color:var(--ink-70);margin:8px 0 0">{d}</p></div>' for t, d in p["features"])
    thumbs = "".join(
        f'<button type="button" data-src="assets/img/{img}" data-alt="{p["short"]} detail view" aria-label="View image {i+1}"><img src="assets/img/{img}" alt="" loading="lazy"></button>'
        for i, img in enumerate([p["hero"], "hero.webp", "room-vertical-card.webp", p["card"]]))
    body = f"""
  <div class="phero">
    <div class="wrap">
      {crumbs([("Home", "index.html"), ("Products", "products.html"), (p["short"], None)])}
      <div class="phero-media">
        <div>
          <p class="eyebrow">{p["short"]}</p>
          <h1>{p["tagline"]}</h1>
          <p class="lede">{p["lede"]}</p>
          <p class="pill" style="margin-top:22px">{p["price"]}</p>
          <div class="cta-row" style="margin-top:26px">
            {HD.btn("Shop at The Home Depot", key=p["slug"], module="pdp_hero")}
            <a class="btn btn--ghost" href="free-samples.html">Order free samples</a>
          </div>
          <div class="badges" style="margin-top:24px">{''.join(f'<span class="badge">{b}</span>' for b in p["badges"])}</div>
        </div>
        <div>
          {PIC.pic("category-" + p["slug"], img_id="gal-main", alt=f'{p["short"]} installed in a styled room', lcp=True) or f'<img id="gal-main" src="assets/img/{p["hero"]}" alt="{p["short"]} installed in a styled room">'}
          <div class="gal-thumbs" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px">{thumbs}</div>
        </div>
      </div>
    </div>
  </div>
  {anchors([("Overview", "overview"), ("Options", "options"), ("Colours", "colours"), ("Specifications", "specs"), ("Measuring", "measuring"), ("FAQ", "faq")])}

  <section id="overview">
    <div class="wrap">
      <div class="withside">
        <div>
        <div class="prose">
          <h2>Overview</h2>
          <p>{p["intro"]}</p>
        </div>
      <div class="shead rev" id="options" style="margin-top:clamp(48px,5vw,72px)">
        <div><p class="eyebrow">Options</p><h2>What you choose</h2></div>
      </div>
      <div class="three" style="margin-top:0">{feats}</div>
        </div>
        <aside class="side">
          <div class="box sticky-box">
            <h4>At a glance</h4>
            <ul>
              <li><strong>{p["price"]}</strong> at The Home Depot</li>
              <li>Made to your measurements</li>
              <li>Limited lifetime warranty</li>
              <li>Cordless options available</li>
            </ul>
            {HD.btn("Shop now", key=p["slug"], module="pdp_rail", cls="btn btn--hd btn--sm", style="width:100%;justify-content:center;margin-top:16px")}
            <a class="btn btn--ghost btn--sm" style="width:100%;justify-content:center;margin-top:8px" href="free-samples.html">Free samples</a>
          </div>
          <div class="box tint">
            <h4>Need a hand?</h4>
            <p style="margin:0 0 10px;color:var(--ink-70)">Talk to someone who knows the product line.</p>
            <p style="margin:0"><strong>1-855-558-1222</strong><br><a href="contact.html" style="border-bottom:1px solid var(--clay)">Contact support</a></p>
          </div>
        </aside>
      </div>
    </div>
  </section>
  {SLAT}
  <section id="colours">
    <div class="wrap">
      {shead('Colours', 'Eight of the range, shown flat.', 'Screens lie. Order the swatch and tape it to the window before you order the shade.')}
      <div class="swatches">{sw}</div>
      <p class="tnote">Swatch colours are approximate in this mockup. In build, each swatch links to a real SKU and a full-window preview image.</p>
      <div class="cta-row" style="margin-top:26px"><a class="btn btn--ghost" href="free-samples.html">Order up to 8 free samples</a></div>
    </div>
  </section>
  <section id="specs" class="spec-sec">
    <div class="wrap">
      <div class="split">
        <div>
          <p class="eyebrow">Specifications</p>
          <h2>The numbers, not the adjectives.</h2>
          <p style="color:var(--ink-70);margin-top:16px">Full specifications are on the page, not behind a tab. Everything below is also in the downloadable spec sheet for trade customers.</p>
          <div class="cta-row" style="margin-top:24px"><a class="btn btn--ghost" href="for-professionals.html">Trade spec book</a></div>
        </div>
        <div class="scrollx">
          <table class="spec">
            <thead><tr><th>Attribute</th><th>Detail</th></tr></thead>
            <tbody>{''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in p["spec"])}</tbody>
          </table>
          <p class="tnote">Sizes shown are the full manufacturing range. Not every fabric is available at every size.</p>
        </div>
      </div>
    </div>
  </section>
  <section id="measuring">
    <div class="wrap">
      {shead('Before you order', 'Measure once, properly.')}
      {steps([
        ("Choose the mount", "Inside mount sits within the frame for a built-in look. Outside mount covers the whole opening and blocks more light."),
        ("Measure width in three places", "Top, middle and bottom. Use the narrowest number for an inside mount."),
        ("Measure height in three places", "Left, centre and right. Use the longest number for an inside mount."),
        ("Do not deduct anything", "Give us the exact opening. We make the deductions for you."),
      ], four=True)}
      <div class="callout" style="max-width:860px"><p><strong>The rule that saves most orders:</strong> record measurements to the nearest 1/8&quot; and never round down on height. The full walkthrough, with diagrams, is in the <a class="link" href="how-to-measure.html">measuring guide</a>.</p></div>
    </div>
  </section>
  <section id="faq" class="tight">
    <div class="wrap">
      {shead('FAQ', '{} questions, answered honestly.'.format(len(p["faqs"])))}
      {acc(p["faqs"])}
      <p style="margin-top:26px"><a class="btn btn--ghost btn--sm" href="faq.html">All frequently asked questions</a></p>
    </div>
  </section>
  {SLAT}
  <section>
    <div class="wrap">
      {shead('Also consider', 'Related products.', '', '<a class="btn btn--ghost btn--sm" href="products.html">View all products</a>')}
      {cards(D.card_tuples(others))}
    </div>
  </section>
  {cta_band("Ready when you are.",
            "Veneta is sold exclusively through The Home Depot, online and in store. Configure your size and options there.",
            ("Shop at The Home Depot", HD.href(module="cta_band")), ("Find a store", "where-to-buy.html"))}
"""
    write(p["slug"] + ".html", page(
        f'{p["short"]} &mdash; Custom, Cordless, Made to Fit | VENETA&trade;',
        f'{p["short"]} made to your measurements. {re.sub("<[^>]+>", "", p["tagline"])} Full specifications, colours and FAQs.',
        body, active="products"))


# ---------------------------------------------------------------- shop by room / need / finder
def build_shop_by():
    room_tiles = []
    for name, sub, img in D.ROOMS:
        room_tiles.append((name, sub, img, f"#{slugify(name)}"))
    blocks = ""
    rec = {
        "Living Room": ["roller-solar-shades", "sheer-shades", "roman-shades"],
        "Bedroom": ["cellular-shades", "roller-solar-shades", "roman-shades"],
        "Nursery": ["cellular-shades", "sheer-shades", "faux-wood-blinds"],
        "Kitchen": ["faux-wood-blinds", "roller-solar-shades", "vertical-blinds"],
        "Bathroom": ["faux-wood-blinds", "shutters", "vertical-blinds"],
        "Home Office": ["roller-solar-shades", "cellular-shades", "sheer-shades"],
        "Patio Doors": ["dualdrape", "vertical-blinds", "shutters"],
        "Dining Room": ["roman-shades", "shutters", "sheer-shades"],
    }
    notes = {
        "Living Room": "The living room usually has two competing problems: glare on the television in the afternoon and a view you do not want to give up. A 5% or 10% solar screen solves both. Add a soft layer if the room feels bare at night.",
        "Bedroom": "Bedrooms are a light-blocking problem, not a decorating problem. Double cell blackout cellular shades with SmartPrivacy&reg; channels are the darkest combination we build, and they cut outside noise noticeably too.",
        "Nursery": "Cordless is not optional here. Every Veneta product is cordless as standard, which means there is no looped cord anywhere near a crib. Add blackout for daytime naps.",
        "Kitchen": "Steam, grease and splashes rule out most fabrics. Faux wood wipes clean and will not warp above a sink. Keep the treatment clear of the hob.",
        "Bathroom": "Privacy plus humidity. Composite shutters and faux wood handle the moisture; vinyl verticals are the budget answer on a wide bathroom window.",
        "Home Office": "Glare is the whole job. A 1% or 3% solar screen kills reflections on a monitor while keeping the room bright enough to work in without lights on.",
        "Patio Doors": "The treatment has to move out of the way. DualDrape&trade; gives you a soft, drapery-like face that rotates and traverses; vertical blinds do the same job for less.",
        "Dining Room": "This is the window that gets to be decorative. Roman shades in a textured linen, or shutters if the room has strong architecture already.",
    }
    for name, sub, img in D.ROOMS:
        sid = slugify(name)
        blocks += f"""
      <div id="{sid}" style="padding-top:clamp(56px,7vw,92px)">
        {shead(name, sub + ".")}
        <div class="rowfeat rev">
          <div class="txt"><p style="color:var(--ink-70)">{notes[name]}</p>
            <ul class="ticks" style="margin-top:18px">
              <li>Recommended: {', '.join(D.BY_SLUG[s]["short"] for s in rec[name])}</li>
              <li>Cordless lift available on every option</li>
              <li>Free samples before you commit</li>
            </ul>
            <a class="btn btn--ghost btn--sm" href="{rec[name][0]}.html">Start with {D.BY_SLUG[rec[name][0]]["short"]}</a>
          </div>
          <div><img src="assets/img/{img}" alt="{name} fitted with Veneta window treatments" loading="lazy"></div>
        </div>
        <div style="margin-top:44px">{cards(D.card_tuples(rec[name]))}</div>
      </div>"""
    body = phero("Shop by room", "Start where you're standing.",
                 "The right product is usually decided by the room, not the catalogue. Pick the room you are trying to fix and we will narrow eight product lines down to three.",
                 trail=[("Home", "index.html"), ("Shop by room", None)],
                 ctas='<a class="btn" href="product-finder.html">Answer three questions instead</a><a class="btn btn--ghost" href="shop-by-need.html">Shop by need</a>')
    body += f"""
  <section class="nobot">
    <div class="wrap">{tiles(room_tiles)}</div>
  </section>
  <section class="tight">
    <div class="wrap">{blocks}</div>
  </section>
  {cta_band("Still deciding?", "Order free swatches, or tell us the window and we will tell you what we would fit.",
            ("Order free samples", "free-samples.html"), ("Contact support", "contact.html"))}
"""
    write("shop-by-room.html", page("Shop by Room &mdash; Blinds &amp; Shades for Every Room | VENETA&trade;",
                                    "Window treatment recommendations by room: living room, bedroom, nursery, kitchen, bathroom, home office, patio doors and dining room.",
                                    body, active="shopby"))

    # by need
    nblocks = ""
    for i, (need, sub, img, slugs) in enumerate(D.NEEDS):
        nid = slugify(need)
        nblocks += f"""<div id="{nid}" style="padding-top:clamp(48px,6vw,80px)">
          {rowfeat(f'Need {str(i+1).zfill(2)}', need + ".", f'<p style="color:var(--ink-70)">{sub}</p><p style="color:var(--ink-70)">Recommended lines: ' + ", ".join(f'<a class="link" href="{s}.html" style="border-bottom:1px solid var(--clay)">{D.BY_SLUG[s]["short"]}</a>' for s in slugs) + '.</p>', img, need + " solution shown at a window", flip=(i % 2 == 1))}
        </div>"""
    body = phero("Shop by need", "Name the problem. We'll name the product.",
                 "Most people arrive with a problem, not a product in mind: the sun hits the screen, the bedroom is too bright, the patio door looks bare. Start there.",
                 trail=[("Home", "index.html"), ("Shop by need", None)],
                 ctas='<a class="btn" href="product-finder.html">Use the product finder</a><a class="btn btn--ghost" href="shop-by-room.html">Shop by room</a>')
    body += f"""<section class="tight"><div class="wrap">{nblocks}</div></section>
  {SLAT}
  <section><div class="wrap">{shead('All products', 'Or just browse everything.')}{cards(D.card_tuples())}</div></section>"""
    write("shop-by-need.html", page("Shop by Need &mdash; Blackout, Glare, Safety, Energy | VENETA&trade;",
                                    "Find window treatments by the problem you are solving: blocking light, cutting glare, keeping the view, child safety, energy use, patio doors and humidity.",
                                    body, active="shopby"))

    # finder
    body = phero("Product finder", "Three questions. One honest recommendation.",
                 "No lead form, no email gate. Answer three questions and we will show you the two or three products that actually suit the window, and tell you what we would not fit.",
                 trail=[("Home", "index.html"), ("Product finder", None)])
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="withside">
        <div>
          <form class="form" id="pf-form" style="max-width:none">
            <div class="full"><label for="f-room">1. Which room?</label>
              <select id="f-room"><option>Living room</option><option>Bedroom</option><option>Nursery</option><option>Kitchen</option><option>Bathroom</option><option>Home office</option><option>Dining room</option><option>Patio door or wide opening</option></select></div>
            <div class="full"><label for="f-need">2. What matters most?</label>
              <select id="f-need"><option>Block all the light</option><option>Cut glare and heat</option><option>Keep the view</option><option>Privacy without darkness</option><option>Child and pet safety</option><option>Lower the energy bill</option><option>Handle humidity</option><option>Lowest price</option></select></div>
            <div class="half"><label for="f-w">3. Opening width (inches)</label><input id="f-w" type="number" min="18" max="192" placeholder="36"></div>
            <div class="half"><label for="f-h">Opening height (inches)</label><input id="f-h" type="number" min="24" max="120" placeholder="60"></div>
            <div class="full"><label for="f-lift">Lift preference</label>
              <select id="f-lift"><option>Cordless</option><option>Motorized</option><option>No preference</option></select></div>
            <div class="full"><button class="btn" type="submit">Show my recommendations</button></div>
          </form>
          <div class="fout" id="pf-out" style="margin-top:56px">
            {shead('Your shortlist', 'Living room &middot; block all the light')}
            {cards(D.card_tuples(["cellular-shades", "roller-solar-shades", "roman-shades"]))}
          </div>
          <div class="callout" style="margin-top:28px"><p><strong>What we will tell you not to buy:</strong> a solar screen for a bedroom. At night a lit room is visible through any screen fabric, so it is the wrong product even at 1% openness.</p></div>
        </div>
        <aside class="side">
          <div class="box tint sticky-box">
            <h4>Why we ask for size</h4>
            <p style="margin:0 0 12px;color:var(--ink-70)">Some products are not available at every size, and weight becomes a real problem on wide blinds. Knowing the opening lets us rule things out instead of listing everything.</p>
            <h4 style="margin-top:22px">Prefer to talk?</h4>
            <p style="margin:0"><strong>1-855-558-1222</strong><br>Mon&ndash;Fri, 8am&ndash;6pm CT</p>
          </div>
        </aside>
      </div>
    </div>
  </section>
"""
    write("product-finder.html", page("Product Finder &mdash; Find the Right Blind or Shade | VENETA&trade;",
                                      "Answer three questions about your room, your priority and your window size, and get a short, honest list of the Veneta products that fit.",
                                      body, active="shopby"))
