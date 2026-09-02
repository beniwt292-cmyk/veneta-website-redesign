#!/usr/bin/env python3
"""Warranty, contact, FAQ, buying guides, inspiration, journal, company, legal, utility pages."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hd as HD
from shell import (page, crumbs, phero, phero_media, anchors, SLAT, shead, acc,
                   steps, kv, vids, tiles, cards, rowfeat, stats, cta_band, support_strip)
import data as D
from build_site import write, slugify


def prose_blocks(items):
    out = ""
    for kind, val in items:
        if kind == "h2":
            out += f"<h2>{val}</h2>"
        elif kind == "h3":
            out += f"<h3>{val}</h3>"
        elif kind == "p":
            out += f"<p>{val}</p>"
        elif kind == "ul":
            out += "<ul>" + "".join(f"<li>{x}</li>" for x in val) + "</ul>"
        elif kind == "ol":
            out += "<ol>" + "".join(f"<li>{x}</li>" for x in val) + "</ol>"
        elif kind == "callout":
            out += f'<div class="callout"><p>{val}</p></div>'
        elif kind == "pullquote":
            out += f'<p class="pullquote">{val}</p>'
    return out


# ---------------------------------------------------------------- warranty / contact / faq
def build_policies():
    W = D.WARRANTY
    body = phero("Warranty", "Limited lifetime warranty, in plain English.",
                 W["lede"],
                 trail=[("Home", "index.html"), ("Support", "support.html"), ("Warranty", None)],
                 ctas='<a class="btn" href="contact.html">Start a claim</a>')
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="withside">
        <div class="prose">
          {prose_blocks([
            ("h2", "What is covered"),
            ("p", W["scope"]),
            ("ul", W["covered"]),
            ("h2", "What is not covered"),
            ("ul", W["excluded"]),
            ("h2", "How to make a claim"),
            ("ol", W["claim"]),
            ("callout", W["direct"]),
            ("h2", "Motorization specifics"),
            ("p", W["motor"]),
            ("h2", "Consumer rights"),
            ("p", W["rights"]),
            ("h2", "Registering a product"),
            ("p", W["register"]),
          ])}
        </div>
        <aside class="side">
          <div class="box sticky-box"><h4>Claim checklist</h4><ul>{''.join(f'<li>{i}</li>' for i in W["checklist"])}</ul>
            <a class="btn btn--sm" style="width:100%;justify-content:center;margin-top:16px" href="contact.html">Start a claim</a></div>
          <div class="box tint"><h4>Phone</h4><p style="margin:0"><strong>{D.SUPPORT_PHONE}</strong><br>{D.SUPPORT_HOURS}</p></div>
        </aside>
      </div>
    </div>
  </section>
"""
    write("warranty.html", page("Limited Lifetime Warranty | VENETA&trade;",
                                "What the Veneta limited lifetime warranty covers, what it excludes, motorization coverage, and the five-step claim process.",
                                body, active="support"))


    # contact
    body = phero("Contact", "Talk to someone who knows the product.",
                 "Support is handled by Veneta directly, not by the retailer. Have your Home Depot order number ready and most questions are resolved on the first call.",
                 trail=[("Home", "index.html"), ("Support", "support.html"), ("Contact", None)])
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="methods">
        <div class="method"><h3>Call</h3><b>1-855-558-1222</b><p>Monday to Friday, 8am to 6pm CT. Average wait under three minutes.</p></div>
        <div class="method"><h3>Email</h3><b style="font-size:var(--fs-body)">help@venetawindowfashions.com</b><p>We reply within one business day. Attach photos and we will usually resolve it in one exchange.</p></div>
        <div class="method"><h3>Order status</h3><b style="font-size:var(--fs-body)">The Home Depot</b><p>Delivery tracking sits with the retailer. Order status, changes and cancellations go through them.</p></div>
      </div>
      <div class="withside" style="margin-top:64px">
        <div>
          {shead('Send a message', "Tell us what we need to know.")}
          <form class="form" data-mock>
            <div><label for="c-name">Name</label><input id="c-name" required></div>
            <div><label for="c-email">Email</label><input id="c-email" type="email" required></div>
            <div><label for="c-phone">Phone (optional)</label><input id="c-phone" type="tel"></div>
            <div><label for="c-order">Home Depot order number</label><input id="c-order" placeholder="WM123456789"></div>
            <div class="full"><label for="c-topic">What is this about?</label>
              <select id="c-topic"><option>Product question before buying</option><option>Measuring help</option><option>Installation help</option><option>Warranty claim</option><option>Replacement part</option><option>Motorization or smart home</option><option>Trade and professional enquiry</option><option>Something else</option></select></div>
            <div class="full"><label for="c-prod">Which product?</label>
              <select id="c-prod">{''.join(f'<option>{re.sub("&trade;|&reg;", "", p["short"])}</option>' for p in D.PRODUCTS)}<option>Not sure yet</option></select></div>
            <div class="full"><label for="c-msg">Details</label><textarea id="c-msg" placeholder="Window size, what is happening, and what you have already tried."></textarea>
              <p class="hint">Photos help more than description. You can attach up to three in the built form.</p></div>
            <div class="full"><button class="btn" type="submit">Send message</button>
              <p class="mockmsg hint" hidden style="margin-top:12px;color:var(--success)">Mockup only: no message has been sent. In build, this posts to the support desk and returns a ticket number on screen.</p></div>
          </form>
        </div>
        <aside class="side">
          <div class="box tint sticky-box"><h4>Answer it yourself, faster</h4><ul>
            <li><a href="faq.html">Frequently asked questions</a></li>
            <li><a href="how-to-measure.html">How to measure</a></li>
            <li><a href="how-to-install.html">How to install</a></li>
            <li><a href="how-to-clean.html">How to clean</a></li>
            <li><a href="warranty.html">Warranty terms</a></li>
            <li><a href="motorization.html">Smart home compatibility</a></li></ul></div>
          <div class="box"><h4>Trade enquiries</h4><p style="margin:0;color:var(--ink-70)">Builders, designers and property managers: see <a href="for-professionals.html" style="border-bottom:1px solid var(--clay)">For Professionals</a>.</p></div>
        </aside>
      </div>
    </div>
  </section>
"""
    write("contact.html", page("Contact Support | VENETA&trade;",
                               "Reach Veneta support by phone on 1-855-558-1222, by email, or through the contact form. Warranty claims, measuring help and product questions.",
                               body, active="support"))

    # faq
    groups = [
        ("Buying", [
            ("Where can I buy Veneta products?", "<p>Exclusively at The Home Depot, online at homedepot.com and in store. We do not sell direct.</p>"),
            ("Why can't I order on this site?", "<p>Because configuring a made-to-measure product needs live pricing and inventory, and that lives with the retailer. This site exists to help you decide correctly before you get there.</p>"),
            ("How long does an order take?", "<p>Typically 10 to 15 business days. Made-to-measure products are built after you order, not picked from a shelf.</p>"),
            ("Can I get free samples?", '<p>Yes, up to eight swatches. <a class="link" href="free-samples.html">Order samples</a>.</p>'),
            ("Do you price match?", "<p>Pricing and promotions are set by The Home Depot, so their price match policy applies, not ours.</p>"),
        ]),
        ("Measuring &amp; fitting", [
            ("Should I deduct anything from my measurements?", "<p>No. Submit the exact opening size to the nearest 1/8&quot;. The factory applies clearances.</p>"),
            ("Width or height first?", "<p>Always width first. Reversing them is the most common ordering error in this category.</p>"),
            ("What if my window is not square?", '<p>If the three width measurements differ by more than 1/2&quot;, use an outside mount, or a shutter with a deco frame. See <a class="link" href="how-to-measure.html">how to measure</a>.</p>'),
            ("How much depth do I need for an inside mount?", '<p>3/4&quot; for cellular, 2&quot; for faux wood and roller, 2 1/2&quot; for Roman and sheer. Each product page lists its minimum.</p>'),
            ("Can I install these myself?", '<p>Yes, in about twenty minutes for a typical shade. Shutters are a bigger job. Follow the <a class="link" href="how-to-install.html">installation guide</a>.</p>'),
        ]),
        ("Safety", [
            ("Are your products cordless?", "<p>Yes, all of them. There is no looped cord on any product we make.</p>"),
            ("Do they meet child safety standards?", '<p>They are designed to meet the current ANSI/WCMA A100.1 requirements. See <a class="link" href="child-safety.html">child and pet safety</a>.</p>'),
            ("What about older blinds in my house?", "<p>Secure any cords out of reach today, and consider the free retrofit programme run by the Window Covering Safety Council.</p>"),
        ]),
        ("Motorization &amp; smart home", [
            ("Does motorization work with Alexa or Google Home?", '<p>With a ShadeAuto&trade; Hub, yes, on supported motor generations. Without the hub, no. The <a class="link" href="motorization.html">compatibility list</a> is the source of truth.</p>'),
            ("Is Apple Home supported?", "<p>Not at this time.</p>"),
            ("How long do the batteries last?", "<p>Several months per charge in typical use. RevitaCharge&trade; packs recharge in place over USB-C.</p>"),
            ("Can I motorize a shade I already own?", "<p>No. The motor is fitted inside the headrail during manufacture.</p>"),
            ("How many shades can one hub control?", "<p>Up to 30 motors across 10 rooms.</p>"),
        ]),
        ("Care &amp; warranty", [
            ("How do I clean a blackout shade?", '<p>Dust and spot clean only. Never soak it: the foil liner can separate. Full guidance in <a class="link" href="how-to-clean.html">how to clean</a>.</p>'),
            ("Can I machine wash fabric vanes?", "<p>Hand wash cool and hang flat to dry. Never machine dry.</p>"),
            ("What does the warranty cover?", '<p>Materials and workmanship for life, motorization for five years. Full terms on the <a class="link" href="warranty.html">warranty page</a>.</p>'),
            ("My shade arrived damaged. What do I do?", "<p>Photograph it, then call 1-855-558-1222 with the order number. Do not install it.</p>"),
            ("Can I buy replacement parts?", "<p>Yes. Vanes, louvres, wands, brackets and remotes are all available individually.</p>"),
        ]),
    ]
    blocks = ""
    for label, items in groups:
        blocks += f'<div id="{slugify(label)}" style="margin-bottom:60px">{shead(label, "")}{acc(items)}</div>'
    body = phero("FAQ", "The questions support actually gets.",
                 "Grouped by where you are in the process, and answered without marketing language. If your question is not here, tell us and it probably should be.",
                 trail=[("Home", "index.html"), ("Support", "support.html"), ("FAQ", None)])
    body += f"""{anchors([(l, slugify(l)) for l, _ in groups])}
  <section class="tight"><div class="wrap">{blocks}</div></section>
  {cta_band("Question not answered?", "Call 1-855-558-1222 or send a message. We add the good ones to this page.", ("Contact support", "contact.html"), ("Read the warranty", "warranty.html"))}"""
    write("faq.html", page("Frequently Asked Questions | VENETA&trade;",
                           "Answers on buying, measuring, fitting, child safety, motorization compatibility, cleaning and warranty for Veneta blinds, shades and shutters.",
                           body, active="support"))


# ---------------------------------------------------------------- buying guides
GUIDES = [
    dict(file="faux-wood-guide.html", label="Faux wood buying guide", img="fauxwood-card.webp",
         h1="Faux wood blinds: the complete buying guide.",
         lede="Slat width, routeless slats, valances, weight limits and the two rooms where faux wood beats real wood outright. Everything you need before you configure a size.",
         blocks=[
             ("h2", "Faux wood versus real wood"),
             ("p", "Real wood is lighter and has genuine grain variation. Faux wood is a polymer composite that will not warp in humidity and costs meaningfully less at the same slat size. In a kitchen, bathroom or laundry, composite is not a compromise; it is the correct specification."),
             ("h2", "Choosing a slat width"),
             ("ul", ['2" slats: standard windows, a smaller stack when raised, slightly more privacy when closed.',
                     '2 1/2" slats: large windows, fewer lines across the glass, a clearer view when tilted open, a more architectural look.']),
             ("p", "On any window wider than about 48&quot;, the wider slat almost always looks more expensive for very little extra money."),
             ("h2", "Routeless slats"),
             ("p", "Standard slats have holes routed through them for the lift cords, which produce a row of pinholes of light. Routeless slats move the route to the back edge, so you lose the pinholes. On a bedroom or a street-facing window it is the single best upgrade on this product."),
             ("pullquote", "If the room needs to be dark, order routeless. If it is a hallway, do not bother."),
             ("h2", "Weight and width limits"),
             ("ul", ['Up to 48": standard two-bracket installation.',
                     '48" to 72": a centre support bracket is included and required.',
                     'Above 72": consider motorization, or split the opening into two blinds on one headrail.']),
             ("h2", "Colour and finish"),
             ("p", "Match the trim, not the wall. Bright white beside antique white trim reads as a mistake from across the room. Order both swatches and hold them against the casing in daylight."),
             ("h2", "The valance"),
             ("p", "A matched 3&quot; crown valance is included. Fit it. It hides the headrail and it is the difference between a finished window and a visible mechanism."),
             ("h2", "What to avoid"),
             ("ul", ["Cutting slats down after delivery. It voids the warranty and never looks right.",
                     "Furniture polish, which leaves a film that attracts dust.",
                     "Skipping the centre bracket on a wide blind, which bows the headrail within a season."]),
         ],
         rel=["faux-wood-blinds", "shutters", "vertical-blinds"]),
    dict(file="roman-cordless-guide.html", label="Cordless Roman shade guide", img="roman-card.webp",
         h1="Cordless Roman shades: how to choose the fold, the lining and the mount.",
         lede="Roman shades are the softest thing we make, and the one where small decisions change the look most. Three choices matter: fold style, lining, and how you mount it.",
         blocks=[
             ("h2", "Flat fold or hobbled fold"),
             ("p", "A flat fold reads tailored and contemporary. The panel hangs as one clean plane when lowered and stacks into crisp horizontal folds as it rises. A hobbled fold keeps a soft cascade even when fully lowered, which suits traditional trim and deeper window frames."),
             ("p", "If the room has strong architectural detail, hobbled will sit comfortably with it. In a plain modern room, flat is usually the better call."),
             ("h2", "Lining changes everything"),
             ("ul", ["Unlined: maximum light, visible weave, almost no privacy.",
                     "Privacy lining: the everyday choice. Softens light, blocks silhouettes.",
                     "Blackout lining: for bedrooms. Note that an inside-mounted Roman shade still leaks light at the edges."]),
             ("callout", "If you need a genuinely dark bedroom, a blackout Roman shade alone will not get you there. Pair it with an outside mount, or use a blackout roller with SmartPrivacy&reg; channels behind a decorative Roman."),
             ("h2", "Why cordless matters here"),
             ("p", "Traditional Roman shades were the worst offender for cord loops, because the lift cords run through rings on the back of the panel. Our cordless system moves the mechanism into the headrail, so there is nothing hanging down the wall and nothing near a crib."),
             ("h2", "Mounting depth"),
             ("p", "Roman shades need 2 1/2&quot; of depth for a flush inside mount, because the fabric stack sits behind the headrail. Shallow frames should use an outside mount, which also improves light control at the edges."),
             ("h2", "Fabric choice"),
             ("ul", ["Linen blends: the most attractive drape, the most relaxation over time.",
                     "Textured cotton: holds a crisper fold, better on a flat fold shade.",
                     "Performance weaves: for a bright window where fading is a real risk."]),
             ("h2", "Living with them"),
             ("p", "Dust regularly, spot clean gently, and use a professional cleaner for anything bigger. Washing removes the sizing that holds the folds and the shade will never hang the same again."),
         ],
         rel=["roman-shades", "sheer-shades", "cellular-shades"]),
    dict(file="cordless-roller-shades-guide.html", label="Cordless roller shade guide", img="roller-card.webp",
         h1="Cordless roller and solar shades: openness, roll direction and cassettes.",
         lede="Roller shades look simple because they are, but three specification details decide whether the shade solves your problem: openness factor, roll direction and how the tube is finished.",
         blocks=[
             ("h2", "Openness factor, explained properly"),
             ("p", "Openness is the percentage of the weave that is open space. A 3% screen is 3% holes and 97% yarn, so it blocks more glare, more heat and more of the view. A 14% screen keeps the view sharpest and controls the least."),
             ("ul", ["1% and 3%: home offices, west-facing rooms, anywhere with a screen you work at.",
                     "5%: the balanced default for a living room.",
                     "10% and 14%: a view you specifically want to preserve."]),
             ("callout", "Openness has nothing to do with night privacy. With the lights on inside, a lit room is visible through any screen fabric. If you need night privacy, you need a blackout fabric or a second layer."),
             ("h2", "Blackout rollers"),
             ("p", "A coated blackout fabric blocks light through the material completely. What it does not block is the gap at each side, which is why we recommend pairing it with SmartPrivacy&reg; channels in bedrooms and media rooms."),
             ("h2", "Standard roll or reverse roll"),
             ("p", "Standard roll brings the fabric off the back of the tube, closest to the glass. Reverse roll brings it off the front, which you need when a deep sill, a crank handle or a window latch would otherwise foul the fabric. Check for obstructions before you order."),
             ("h2", "Open roll, fascia or cassette"),
             ("ul", ["Open roll: the tube is visible. Cheapest, most industrial.",
                     "Fascia: a flat aluminium face conceals the tube. The usual choice.",
                     "Cassette: wraps the tube on three sides, keeps dust off and finishes best against a ceiling recess."]),
             ("h2", "SmartRail&trade; bottom bar"),
             ("p", "A weighted, fabric-wrapped bar keeps the hem flat and the shade tracking straight. Under-weighted bars are the reason cheap roller shades start to wander on the tube after a season."),
             ("h2", "When to motorize"),
             ("p", "Tall windows, banks of shades you want to move together, and rooms you want closed before you get home on a hot afternoon. Motorization is also the honest answer for any shade above a stairwell."),
         ],
         rel=["roller-solar-shades", "cellular-shades", "sheer-shades"]),
]


def build_guides():
    grid = ""
    for g in GUIDES:
        grid += f'<a class="card rev" href="{g["file"]}"><div class="ph"><img src="assets/img/{g["img"]}" alt="{g["label"]}" loading="lazy"></div><h3>{g["label"]}</h3><p class="desc">{re.sub("<[^>]+>", "", g["lede"])[:120]}&hellip;</p><p class="price">Read the guide</p></a>'
    body = phero("Buying guides", "Long-form answers, before you spend money.",
                 "Each guide covers one product line in the detail a specification sheet cannot: what the options actually do, which ones matter in your room, and where the money is well spent.",
                 trail=[("Home", "index.html"), ("Buying guides", None)])
    body += f"""<section class="tight"><div class="wrap">
      <a class="rowfeat rev" href="blinds-vs-shades-vs-shutters.html" style="text-decoration:none;color:inherit">
        <div class="txt"><p class="eyebrow">Start here</p><h2>Blinds, shades or shutters?</h2>
          <p style="color:var(--ink-70)">Three different objects, not three styles of the same thing. Nine differences that decide it, and a straight recommendation for each room.</p>
          <span class="arrow" style="margin-top:22px">Read the comparison</span></div>
        <div><img src="assets/img/style-quiet-traditional-1536.webp" alt="A traditional room with shutters, blinds and shades at three different windows" loading="lazy"></div>
      </a>
      <div style="margin-top:clamp(48px,6vw,80px)">{shead('By product line', 'Long-form, one line at a time.')}<div class="cards">{grid}</div></div>
    </div></section>
  {SLAT}
  {support_strip()}"""
    write("buying-guides.html", page("Buying Guides | VENETA&trade;",
                                     "In-depth buying guides for faux wood blinds, cordless Roman shades and cordless roller and solar shades.",
                                     body, active="products"))

    for g in GUIDES:
        others = "".join(f'<li><a href="{x["file"]}">{x["label"]}</a></li>' for x in GUIDES if x["file"] != g["file"])
        body = phero_media("Buying guide", g["h1"], g["lede"], g["img"], g["label"],
                           trail=[("Home", "index.html"), ("Buying guides", "buying-guides.html"), (g["label"], None)],
                           ctas=HD.btn("Shop at The Home Depot", module="hero") + '<a class="btn btn--ghost" href="free-samples.html">Order free samples</a>' + HD.TRUST_P)
        body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="withside">
        <div class="prose">{prose_blocks(g["blocks"])}</div>
        <aside class="side">
          <div class="box sticky-box"><h4>Other guides</h4><ul>{others}</ul></div>
          <div class="box tint"><h4>Get the swatches</h4><p style="margin:0 0 12px;color:var(--ink-70)">Colour decisions made on a screen are decisions made badly.</p><a class="btn btn--ghost btn--sm" style="width:100%;justify-content:center" href="free-samples.html">Free samples</a></div>
        </aside>
      </div>
      <div style="margin-top:64px">{shead('Products in this guide', 'Specifications and options.')}{cards(D.card_tuples(g["rel"]))}</div>
    </div>
  </section>
"""
        write(g["file"], page(f'{g["label"]} | VENETA&trade;', re.sub("<[^>]+>", "", g["lede"])[:155], body, active="products"))


# ---------------------------------------------------------------- inspiration + journal
def build_inspiration():
    body = phero("Inspiration", "Rooms first. Products second.",
                 "Real rooms, the palette behind them, and the exact product and fabric used. No mood boards without a product name attached.",
                 trail=[("Home", "index.html"), ("Inspiration", None)],
                 ctas='<a class="btn" href="shop-by-room.html">Shop by room</a><a class="btn btn--ghost" href="journal.html">Read the journal</a>')
    trends = [
        ("Warm neutrals over cool grey", "Greige and sand have replaced stark white and cold grey as the default. They work with both warm oak and cool tile, which is what an open plan room needs.", "cellular-card.webp"),
        ("Texture instead of pattern", "A visible weave catches light and reads relaxed. Printed pattern on a window dates faster than anything else in a room.", "sheer-card.webp"),
        ("Layering a screen and a blackout", "Two shades on one window: a 3% solar screen for the day, blackout for the evening. Increasingly standard in bedrooms.", "roller-card.webp"),
        ("Wider slats and louvres", 'The 2 1/2" slat and the 4 1/2" louvre. Fewer lines across the glass, more view when open.', "shutters-card.webp"),
        ("Full-height glazing treated as one plane", "Wide-span tracks so a wall of glass reads as one continuous treatment rather than four separate shades.", "dualdrape-card.webp"),
        ("Quiet motorization", "Schedules matter more than voice control. Shades that close before the room heats up, without anyone thinking about it.", "solar-card.webp"),
    ]
    rows = ""
    for i, (t, d, img) in enumerate(trends):
        rows += rowfeat(f"Trend {str(i+1).zfill(2)}", t, f'<p style="color:var(--ink-70)">{d}</p>', img, t, flip=(i % 2 == 1))
    posts = ""
    for p in D.POSTS[:3]:
        posts += f'<a class="post rev" href="{p["slug"]}.html"><div class="ph"><img src="assets/img/{p["img"]}" alt="{p["title"]}" loading="lazy"></div><p class="meta">{p["cat"]} &middot; {p["read"]}</p><h3>{p["title"]}</h3><p>{p["excerpt"]}</p></a>'
    body += f"""
  <section class="nobot"><div class="wrap">{shead('By room', 'Eight rooms, eight starting points.')}{tiles([(n, s, i, "shop-by-room.html#" + slugify(n)) for n, s, i in D.ROOMS])}</div></section>
  <section><div class="wrap">{shead('Trends 2026', 'What is actually changing.', 'Six shifts we are seeing in orders, not six things we would like to sell you.')}{rows}</div></section>
  {SLAT}
  <section><div class="wrap">{shead('Journal', 'Longer reads.', '', '<a class="btn btn--ghost btn--sm" href="journal.html">All articles</a>')}<div class="posts">{posts}</div></div></section>
  {cta_band("Take the palette to the window.", "Order eight free swatches and look at them at the time of day you use the room.", ("Order free samples", "free-samples.html"), ("Shop by room", "shop-by-room.html"))}
"""
    write("inspiration.html", page("Inspiration &mdash; Rooms, Palettes &amp; 2026 Trends | VENETA&trade;",
                                   "Window treatment inspiration by room, the 2026 trends we are actually seeing, and long-form articles on colour, texture and light.",
                                   body, active="inspiration"))

    feat = D.POSTS[0]
    rest = ""
    for p in D.POSTS[1:]:
        rest += f'<a class="post rev" href="{p["slug"]}.html"><div class="ph"><img src="assets/img/{p["img"]}" alt="{p["title"]}" loading="lazy"></div><p class="meta">{p["cat"]} &middot; {p["date"]} &middot; {p["read"]}</p><h3>{p["title"]}</h3><p>{p["excerpt"]}</p></a>'
    body = phero("Journal", "Notes on light, colour and keeping things clean.",
                 "Published when we have something useful to say, which is roughly monthly. Care guides, colour thinking and honest answers about energy performance.",
                 trail=[("Home", "index.html"), ("Inspiration", "inspiration.html"), ("Journal", None)])
    body += f"""
  <section class="tight">
    <div class="wrap">
      <a class="feature-post rev" href="{feat["slug"]}.html">
        <div><img src="assets/img/{feat["img"]}" alt="{feat["title"]}"></div>
        <div><p class="meta" style="font-size:var(--fs-micro);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-45);margin:0 0 12px">Latest &middot; {feat["cat"]} &middot; {feat["date"]}</p>
          <h2>{feat["title"]}</h2><p style="color:var(--ink-70);margin-top:16px">{feat["excerpt"]}</p>
          <span class="arrow" style="font-weight:600;border-bottom:1px solid var(--clay)">Read the article</span></div>
      </a>
      <div class="posts">{rest}</div>
    </div>
  </section>
  {cta_band("Get one email a month, at most.", "New guides, seasonal care reminders and colour releases. Unsubscribe in one click.", ("Order free samples", "free-samples.html"), ("Browse products", "products.html"))}
"""
    write("journal.html", page("Journal &mdash; Window Treatment Guides &amp; Ideas | VENETA&trade;",
                               "The Veneta journal: care routines, colour guidance, energy performance and design thinking for blinds, shades and shutters.",
                               body, active="inspiration"))

    for i, p in enumerate(D.POSTS):
        nxt = D.POSTS[(i + 1) % len(D.POSTS)]
        body = f"""
  <div class="phero">
    <div class="wrap" style="max-width:820px;margin:0 auto">
      {crumbs([("Home", "index.html"), ("Journal", "journal.html"), (p["cat"], None)])}
      <p class="eyebrow">{p["cat"]}</p>
      <h1 style="max-width:24ch">{p["title"]}</h1>
      <p class="lede">{p["excerpt"]}</p>
      <div class="artmeta"><span>{p["date"]}</span><span>{p["read"]}</span><span>Veneta editorial team</span></div>
    </div>
  </div>
  <section class="tight">
    <div class="wrap">
      <figure style="max-width:1080px;margin:0 auto clamp(40px,5vw,64px)"><img src="assets/img/{p["img"]}" alt="{p["title"]}" style="width:100%;aspect-ratio:16/9;object-fit:cover"><figcaption style="font-size:var(--fs-fine);color:var(--ink-45);margin-top:10px">Placeholder photography for the redesign mockup.</figcaption></figure>
      <div style="max-width:820px;margin:0 auto">
        <div class="prose" style="max-width:none">{prose_blocks(p["body"])}</div>
        <div class="slat" style="padding:0;margin:56px 0" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
        <p class="eyebrow">Read next</p>
        <a class="post" href="{nxt["slug"]}.html" style="display:grid;gap:22px;grid-template-columns:120px 1fr;align-items:center">
          <div class="ph" style="aspect-ratio:1/1"><img src="assets/img/{nxt["img"]}" alt="{nxt["title"]}" loading="lazy"></div>
          <div><p class="meta">{nxt["cat"]} &middot; {nxt["read"]}</p><h3>{nxt["title"]}</h3></div>
        </a>
      </div>
    </div>
  </section>
  {cta_band("Ready to fix the window?", "Every product is made to measure, cordless as standard, and sold at The Home Depot.", ("Shop at The Home Depot", HD.href(module="cta_band")), ("Use the product finder", "product-finder.html"))}
"""
        write(p["slug"] + ".html", page(f'{p.get("seo_title", p["title"])} | VENETA&trade; Journal',
                                        p["excerpt"][:155], body, active="inspiration"))


# ---------------------------------------------------------------- company + utility
def build_company():
    body = phero("Where to buy", "Sold exclusively at The Home Depot.",
                 "Two ways to buy: configure and order online, or take your measurements to a store and have someone walk you through the options. Support afterwards comes from us either way.",
                 trail=[("Home", "index.html"), ("Where to buy", None)],
                 ctas=HD.btn("Shop at The Home Depot", module="wtb_hero") + '<a class="btn btn--ghost" href="how-to-measure.html">Measure first</a>')
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="two">
        <div><p class="eyebrow">Online</p><h2>Order at homedepot.com</h2>
          <ul class="ticks" style="margin-top:18px">
            <li>Full range, every fabric and every option</li>
            <li>Live pricing for your exact size</li>
            <li>Free samples posted to you</li>
            <li>Delivery direct to the door, typically 10 to 15 business days</li>
          </ul>
          {HD.btn("Shop the range", module="wtb_online")}{HD.TRUST_P}</div>
        <div><p class="eyebrow">In store</p><h2>Visit the blinds desk</h2>
          <ul class="ticks" style="margin-top:18px">
            <li>See and handle the actual materials</li>
            <li>Talk through mount type and lift options</li>
            <li>Bring your measurements: width first, to the nearest 1/8&quot;</li>
            <li>Ask about installation services available in your area</li>
          </ul>
          {HD.btn("Find a store", key="stores", module="wtb_stores", cls="btn btn--ghost")}</div>
      </div>
    </div>
  </section>
  {SLAT}
  <section>
    <div class="wrap">
      {shead('Before you go', 'Three things worth doing first.')}
      {steps([("Measure the opening", "Ten minutes with a steel tape saves a remake. Width first, three measurements each way."),
              ("Order swatches", "Colour on a screen is not colour on your window. Eight free samples, no charge."),
              ("Decide the mount", "Inside for a built-in look, outside for maximum light control. Check the depth on the product page.")])}
      <div class="callout" style="max-width:860px"><p><strong>A note on support:</strong> product questions, warranty claims and replacement parts are handled by Veneta on 1-855-558-1222. Order status, delivery and returns are handled by The Home Depot.</p></div>
    </div>
  </section>
  {support_strip()}
"""
    write("where-to-buy.html", page("Where to Buy &mdash; The Home Depot | VENETA&trade;",
                                    "Veneta blinds, shades and shutters are sold exclusively at The Home Depot, online and in store. What to do before you order.",
                                    body, active="buy"))

    body = phero_media("About", "We make window coverings that fit properly.",
                       "Veneta is the window fashions brand of Richfield Window Coverings. We build made-to-measure blinds, shades and shutters in 1/8&quot; increments, ship them cordless, and stand behind them for the life of the product.",
                       "hero.webp", "A Veneta shade fitted precisely into a window opening",
                       trail=[("Home", "index.html"), ("About", None)],
                       ctas='<a class="btn" href="products.html">See the range</a><a class="btn btn--ghost" href="innovation.html">How we build them</a>')
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="withside">
        <div class="prose">
          {prose_blocks([
            ("h2", "What we do"),
            ("p", "Eight product lines, all made to order, all sold through The Home Depot. Nothing in our range is a stock size, because almost no window is a stock size."),
            ("h2", "Three things we decided early"),
            ("h3", "Cordless on everything"),
            ("p", "Not as a premium option or a separate safety line. There is no looped cord on any product we make, which is the simplest way to meet a safety standard: remove the hazard."),
            ("h3", "Cut to 1/8 inch"),
            ("p", "Rounding to the nearest half inch is cheaper to manufacture and it is why so many shades have an inconsistent light gap. We cut ClearFit&trade; headrails to the opening you give us."),
            ("h3", "Say what the product does not do"),
            ("p", "A solar screen does not give you night privacy. A blackout Roman shade still leaks light at the edges. A motorized shade needs a hub for voice control. Telling you that before you buy costs us a sale occasionally and saves a return every time."),
            ("h2", "Where we sit in the market"),
            ("p", "Between the stock sizes on a shelf and a full custom workroom. You get made-to-measure manufacturing and a limited lifetime warranty, at retail prices, with the retailer handling the transaction and us handling the product."),
            ("h2", "Richfield Window Coverings"),
            ("p", "Veneta is one of several brands operated by Richfield Window Coverings, a manufacturer of residential window treatments for the North American market. Trade and volume enquiries are handled through our professionals team."),
          ])}
        </div>
        <aside class="side">
          <div class="box sticky-box"><h4>Quick facts</h4>{kv([("Product lines", "8"), ("Cut increment", '1/8"'), ("Cordless products", "All"), ("Warranty", "Lifetime"), ("Sold at", "The Home Depot"), ("Support", "Direct from Veneta")])}</div>
          <div class="box tint"><h4>Trade</h4><p style="margin:0;color:var(--ink-70)">Builders, designers and property managers: see <a href="for-professionals.html" style="border-bottom:1px solid var(--clay)">For Professionals</a>.</p></div>
        </aside>
      </div>
    </div>
  </section>
  <section class="dark">
    <div class="wrap">
      <p class="eyebrow">Trademarks</p>
      <h2 style="max-width:24ch">The names, and what they mean.</h2>
      <div class="three">
        <div><h3>ClearFit&trade;</h3><p>Headrails cut to your exact opening.</p></div>
        <div><h3>SmartRail&trade;</h3><p>Weighted bottom bar that keeps fabric flat.</p></div>
        <div><h3>SmartPrivacy&reg;</h3><p>Side channels that close the edge light gap.</p></div>
      </div>
      <div class="three" style="margin-top:34px">
        <div><h3>TruQuiet&trade;</h3><p>Damped motorization with soft start and stop.</p></div>
        <div><h3>RevitaCharge&trade;</h3><p>Rechargeable battery packs, topped up in place.</p></div>
        <div><h3>DualDrape&trade;</h3><p>Sheer and vane treatment for wide openings.</p></div>
      </div>
    </div>
  </section>
"""
    write("about.html", page("About Veneta &mdash; Made to Measure, Cordless | VENETA&trade;",
                             "Veneta is the window fashions brand of Richfield Window Coverings: made-to-measure blinds, shades and shutters, cordless as standard.",
                             body, active=""))

    body = phero("For professionals", "Specification, volume and a contact who answers.",
                 "Builders, interior designers, property managers and installers: the details you need are on the page, and the trade team is a phone call rather than a form-to-nowhere.",
                 trail=[("Home", "index.html"), ("For professionals", None)],
                 ctas='<a class="btn" href="contact.html" data-ev="trade_apply" data-ev-firm_type="unspecified">Contact the trade team</a><a class="btn btn--ghost" href="for-professionals-resources.html">Download resources</a><a class="btn btn--ghost" href="commercial.html">Commercial projects</a>')
    body += f"""
  <section class="tight">
    <div class="wrap">
      {shead('Resources', 'Everything downloadable, in one place.')}
      <div class="sgrid">
        <a href="for-professionals-resources.html"><p class="meta">Specification</p><h3>Spec book</h3><p class="desc" style="color:var(--ink-70);margin:8px 0 0">Full size ranges, mount depths, weights and tolerances for all eight lines.</p><span class="arrow">Download</span></a>
        <a href="for-professionals-resources.html"><p class="meta">CAD &amp; BIM</p><h3>Drawing files</h3><p class="desc" style="color:var(--ink-70);margin:8px 0 0">DWG sections for headrails, brackets and shutter frames, with the full resource set.</p><span class="arrow">Open resources</span></a>
        <a href="warranty.html"><p class="meta">Policy</p><h3>Warranty terms</h3><p class="desc" style="color:var(--ink-70);margin:8px 0 0">Coverage, exclusions and the claim process in full.</p><span class="arrow">Read</span></a>
      </div>
      <div style="margin-top:64px">
        {shead('Volume', 'Multi-unit and development pricing.')}
        <div class="two">
          <div class="prose" style="max-width:none">
            {prose_blocks([
              ("h3", "What we need to quote"),
              ("ul", ["Unit count and window schedule, or a drawing set.",
                      "Product line and fabric, or the performance requirement if you want us to specify it.",
                      "Delivery phasing and site address.",
                      "Whether installation is in scope for you or for us."]),
              ("h3", "Lead times on volume"),
              ("p", "Standard retail lead time is 10 to 15 business days. Volume orders are scheduled to your programme, and we will commit to dates in writing rather than estimating them."),
            ])}
          </div>
          <div class="prose" style="max-width:none">
            {prose_blocks([
              ("h3", "Specifying for a rental or HMO"),
              ("ul", ["Cordless is standard, which removes the main compliance issue.",
                      "Vinyl verticals and faux wood are the cheapest to maintain and replace per unit.",
                      "Replaceable louvres and vanes mean a damaged unit is a part, not a whole treatment.",
                      "Match one colour across a scheme so stock holds interchangeable spares."]),
              ("h3", "Specifying for performance"),
              ("p", "Double cell blackout cellular shades with SmartPrivacy&reg; channels are the most insulating combination we build. Framed shutters seal the opening best. Both are worth specifying on west elevations."),
            ])}
          </div>
        </div>
      </div>
      <div class="callout" style="max-width:860px;margin-top:56px"><p><strong>Trade contact:</strong> 1-855-558-1222, option 3, or use the contact form and select "Trade and professional enquiry". We reply within one business day.</p></div>
    </div>
  </section>
"""
    write("for-professionals.html", page("For Professionals &mdash; Specification &amp; Volume | VENETA&trade;",
                                         "Trade resources for builders, designers, property managers and installers: spec book, CAD files, volume pricing and specification advice.",
                                         body, active=""))

    body = phero("Free samples", "Eight swatches, no charge, no sales call.",
                 "Colour and openness cannot be judged on a screen. Order swatches, tape them to the window, and look at them at the time of day you actually use the room.",
                 trail=[("Home", "index.html"), ("Free samples", None)])
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="withside">
        <div>
          <form class="form" data-mock data-ev="sample_request" data-ev-audience="consumer">
            <div class="full"><label for="s-lines">Which product lines?</label>
              <select id="s-lines" data-ev-param="products" multiple size="6" style="min-height:auto">{''.join(f'<option>{re.sub("&trade;|&reg;", "", p["short"])}</option>' for p in D.PRODUCTS)}</select>
              <p class="hint">Hold Ctrl or Cmd to select more than one. Up to eight swatches in total.</p></div>
            <div><label for="s-name">Name</label><input id="s-name" required></div>
            <div><label for="s-email">Email</label><input id="s-email" type="email" required></div>
            <div class="full"><label for="s-addr">Shipping address</label><input id="s-addr" placeholder="Street address"></div>
            <div><label for="s-city">City</label><input id="s-city"></div>
            <div><label for="s-zip">ZIP code</label><input id="s-zip"></div>
            <div class="full"><label for="s-note">Anything we should know?</label><textarea id="s-note" style="min-height:100px" placeholder="Room, window size, and the problem you are solving."></textarea></div>
            <div class="full"><button class="btn" type="submit">Send my samples</button>
              <p class="mockmsg hint" hidden style="margin-top:12px;color:var(--success)">Mockup only: nothing has been ordered. In build, samples ship within two business days.</p>
              <p class="hint">We use your address to post the samples. We will not call you and we will not add you to a mailing list unless you ask.</p></div>
          </form>
        </div>
        <aside class="side">
          <div class="box tint sticky-box"><h4>How to judge a swatch</h4><ul>
            <li>Tape it to the glass, not to a table.</li>
            <li>Look at it in morning and late afternoon light.</li>
            <li>Hold it against the trim, not the wall.</li>
            <li>For screens, look through it at the actual view.</li>
            <li>For blackout, hold it up to a bright window.</li></ul></div>
          <div class="box"><h4>Then what?</h4><p style="margin:0;color:var(--ink-70)">Measure the opening, then configure the size at The Home Depot.</p>
            {HD.btn("Shop now", module="samples_rail", cls="btn btn--hd btn--sm", style="width:100%;justify-content:center;margin-top:14px")}</div>
        </aside>
      </div>
    </div>
  </section>
"""
    write("free-samples.html", page("Order Free Samples | VENETA&trade;",
                                    "Order up to eight free fabric swatches from any Veneta product line, with no sales call. How to judge colour and openness at your own window.",
                                    body, active="shopby"))


LEGAL = [
    ("terms-and-conditions.html", "Terms &amp; Conditions", "Terms of use for this website, covering products sold at Home Depot, content accuracy, trademarks, warranty, liability and third-party links.",
     [("p", "<em>Mockup notice: this is placeholder legal copy for a design prototype. The live site must use terms reviewed by counsel.</em>"),
      ("h2", "1. About these terms"),
      ("p", "These terms govern your use of this website, operated by Richfield Window Coverings on behalf of the Veneta brand. By using the site you accept them."),
      ("h2", "2. Products and availability"),
      ("p", "Products shown on this site are sold by The Home Depot. Pricing, availability, delivery terms and returns are set by the retailer. Specifications on this site describe the full manufacturing range and not every configuration is available at every size."),
      ("h2", "3. Accuracy of content"),
      ("p", "We work to keep specifications, compatibility information and care instructions current. Colours reproduced on a screen are approximate; order physical samples before purchase. Where a compatibility page conflicts with other material, the compatibility page governs."),
      ("h2", "4. Intellectual property"),
      ("p", "The Veneta name and logo, ClearFit, SmartRail, SmartPrivacy, TruQuiet, RevitaCharge, ShadeAuto, DualDrape and BelleVue are trademarks of Richfield Window Coverings. Site content, photography and copy may not be reproduced without permission."),
      ("h2", "5. Warranty and liability"),
      ("p", "Product warranty terms are set out on the warranty page and are the complete statement of our product coverage. To the extent permitted by law, we are not liable for indirect or consequential loss arising from use of this site."),
      ("h2", "6. Third-party links"),
      ("p", "This site links to homedepot.com and other third-party sites. We are not responsible for their content, terms or privacy practices."),
      ("h2", "7. Changes"),
      ("p", "We may update these terms. The version in force is the one published on this page, with the date of last revision shown below."),
      ("h2", "8. Contact"),
      ("p", "Questions about these terms: help@venetawindowfashions.com or 1-855-558-1222.")]),
    ("privacy-policy.html", "Privacy Policy", "How Veneta handles personal information: what we collect, why we use it, cookies, sharing, retention and how to exercise your privacy rights.",
     [("p", "<em>Mockup notice: this is placeholder legal copy for a design prototype. The live policy must be reviewed by counsel and reflect actual data practices.</em>"),
      ("h2", "1. What we collect"),
      ("ul", ["Contact details you give us: name, email, postal address and phone number when you request samples, submit a support request or make a warranty claim.",
              "Order references you supply, so we can verify coverage.",
              "Technical data: IP address, device and browser type, and pages viewed, collected through analytics.",
              "Cookie preferences you set through the consent banner."]),
      ("h2", "2. Why we use it"),
      ("ul", ["To post the samples you asked for.",
              "To answer support enquiries and process warranty claims.",
              "To improve the site, based on aggregate usage rather than individual behaviour.",
              "To send email only where you have asked us to."]),
      ("h2", "3. Cookies and tracking"),
      ("p", "Essential cookies keep the site working. Analytics and marketing cookies are set only after you accept them in the consent banner, and you can change your choice at any time from the banner link in the footer."),
      ("h2", "4. Sharing"),
      ("p", "We share personal information with service providers who post samples, host the site and run our support desk, under contract and only for those purposes. We do not sell personal information."),
      ("h2", "5. Your rights"),
      ("p", "Depending on where you live, you may have the right to access, correct, delete or port your personal information, and to opt out of certain sharing. Residents of California, Colorado, Connecticut, Utah and Virginia have specific rights under state law. To exercise any of them, email help@venetawindowfashions.com."),
      ("h2", "6. Retention"),
      ("p", "We keep support and warranty records for as long as the product is covered, and marketing contact details until you unsubscribe."),
      ("h2", "7. Children"),
      ("p", "This site is not directed to children and we do not knowingly collect information from anyone under 16."),
      ("h2", "8. Contact"),
      ("p", "Privacy questions and requests: help@venetawindowfashions.com, or write to Richfield Window Coverings, attention Privacy.")]),
    ("accessibility.html", "Accessibility Statement", "Our accessibility commitment: we build to WCAG 2.2 Level AA, what we test, the gaps we know about, and how to tell us when something blocks you.",
     [("p", "<em>Mockup notice: placeholder wording for a design prototype. A live statement must reflect a real audit.</em>"),
      ("h2", "Our target"),
      ("p", "We build to WCAG 2.2 Level AA. That is a target we test against, not a badge we award ourselves."),
      ("h2", "What we do"),
      ("ul", ["A single H1 on every page, and heading levels that describe structure rather than font size.",
              "Text contrast of at least 4.5:1 for body copy and 3:1 for large text and interface elements.",
              "Full keyboard operability, with a visible focus indicator on every interactive element.",
              "Alternative text on every meaningful image, and empty alt on decorative ones.",
              "Captions and written transcripts on installation videos.",
              "Motion that respects the reduced-motion setting in your operating system.",
              "Forms with real labels, described errors and no reliance on colour alone."]),
      ("h2", "Known gaps"),
      ("ul", ["Third-party content embedded from the retailer is outside our control and may not meet the same standard.",
              "Older PDF specification sheets are not fully tagged. We are reworking them.",
              "Video transcripts trail new video releases by a few days."]),
      ("h2", "Testing"),
      ("p", "We test with keyboard only, with a screen reader, at 200% zoom, and with automated tooling on every release. Automated tools catch perhaps a third of real issues, so manual testing is the part that matters."),
      ("h2", "Tell us"),
      ("p", "If something on this site blocks you, email help@venetawindowfashions.com or call 1-855-558-1222 and we will fix it and tell you when it is done. Please include the page and what you were trying to do.")]),
]


def build_legal():
    for f, title, lede, blocks in LEGAL:
        body = phero("Legal" if "Accessibility" not in title else "Accessibility", title.replace("&amp;", "&"), lede,
                     trail=[("Home", "index.html"), (title, None)])
        body += f"""<section class="tight"><div class="wrap"><div class="prose">{prose_blocks(blocks)}
        <p style="margin-top:44px;font-size:var(--fs-fine);color:var(--ink-45)">Last revised: this is a mockup page and carries no effective date.</p></div></div></section>"""
        write(f, page(f"{title} | VENETA&trade;", lede, body, active=""))


def build_utility():
    import pages6 as P6          # late: pages6 imports prose_blocks from here
    groups = [
        ("Products", [("All products", "products.html")] + [(p["short"], p["slug"] + ".html") for p in D.PRODUCTS]),
        ("Shop by", [("Shop by room", "shop-by-room.html"), ("Shop by need", "shop-by-need.html"), ("Product finder", "product-finder.html"), ("Free samples", "free-samples.html"), ("Where to buy", "where-to-buy.html")]),
        ("Rooms", [(P6.ROOM_BY_SLUG[r]["name"], f"room-{r}.html") for r in
                   ("bedroom", "living-room", "kitchen", "bathroom", "home-office", "nursery")]),
        ("Needs", [(n["nav"], f'need-{n["slug"]}.html') for n in P6.NEEDS]),
        ("Styles", [(t["name"], f'style-{t["slug"]}.html') for t in P6.STYLES]),
        ("Innovation", [("Innovation hub", "innovation.html")] + [(n, h) for n, h, _ in D.INNOVATIONS] + [("Child &amp; pet safety", "child-safety.html")]),
        ("Support", [("Support hub", "support.html"), ("How to measure", "how-to-measure.html"), ("How to install", "how-to-install.html"), ("How to clean", "how-to-clean.html"), ("Installation videos", "installation-videos.html"), ("L-frame videos", "installation-videos-l-frame.html"), ("Deco frame videos", "installation-videos-deco-frame.html"), ("Warranty", "warranty.html"), ("FAQ", "faq.html"), ("Contact", "contact.html")]),
        ("Guides", [("Buying guides", "buying-guides.html"), ("Blinds vs shades vs shutters", "blinds-vs-shades-vs-shutters.html")] + [(g["label"], g["file"]) for g in GUIDES]),
        ("Inspiration", [("Inspiration", "inspiration.html"), ("Journal", "journal.html")] + [(p["title"], p["slug"] + ".html") for p in D.POSTS]),
        ("Trade &amp; commercial", [("For professionals", "for-professionals.html"), ("Trade resources", "for-professionals-resources.html"), ("Commercial", "commercial.html"), ("Commercial spec library", "commercial-spec-library.html")]),
        ("Company", [("About Veneta", "about.html"), ("Terms &amp; conditions", "terms-and-conditions.html"), ("Privacy policy", "privacy-policy.html"), ("Accessibility", "accessibility.html"), ("404 page", "404.html")]),
    ]
    cols = ""
    total = 0
    for label, items in groups:
        total += len(items)
        cols += f'<div><h3>{label}</h3><ul>' + "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in items) + "</ul></div>"
    body = phero("Sitemap", "Every page in the mockup.",
                 f"{total + 1} pages, including the homepage. The live site has 30 pages plus a blog, so this covers the existing content and adds the pages the audit found missing.",
                 trail=[("Home", "index.html"), ("Sitemap", None)])
    body += f'<section class="tight"><div class="wrap"><div class="smap"><div><h3>Home</h3><ul><li><a href="index.html">Homepage</a></li><li><a href="sitemap.html">Sitemap</a></li></ul></div>{cols}</div></div></section>'
    write("sitemap.html", page("Sitemap | VENETA&trade; Redesign Mockup", "Every page in the Veneta redesign mockup, grouped by section.", body, active=""))

    body = f"""
  <section class="err">
    <div class="wrap">
      <p class="eyebrow">404</p>
      <h1 style="max-width:20ch">That page has moved, or never existed.</h1>
      <p style="color:var(--ink-70);max-width:52ch;margin:20px auto 0">The old site had three navigation links that led nowhere. This one has a redirect map, and this page, in case we still missed something.</p>
      <div class="cta-row" style="justify-content:center;margin-top:32px">
        <a class="btn" href="products.html">Browse products</a>
        <a class="btn btn--ghost" href="support.html">Get support</a>
      </div>
      <div style="margin-top:64px;text-align:left">{cards(D.card_tuples(["cellular-shades", "roller-solar-shades", "faux-wood-blinds", "shutters"]))}</div>
    </div>
  </section>
"""
    write("404.html", page("Page Not Found | VENETA&trade;", "That page has moved or no longer exists. Browse products or get support.", body, active=""))
