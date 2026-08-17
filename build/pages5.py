#!/usr/bin/env python3
"""P5 depth, part one: §7.6 commercial, the commercial spec library, the §7.5
trade resources page and the §6.2 decision-cluster comparison guide.

Everything downloadable renders through `dl()` so the `spec_download` event and
the "not yet attached" honesty label can never drift apart. Case studies are
composite and are labelled as such on the page, per §12.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hd as HD
from shell import (page, crumbs, phero, phero_media, anchors, SLAT, shead, acc,
                   steps, kv, tiles, cards, rowfeat, stats, cta_band)
import data as D
from build_site import write, slugify
from pages3 import prose_blocks

# Spec assets are not authored yet. One switch: when the PDFs and DWGs land in
# assets/spec/, flip this and every download link goes live at once.
SPEC_ASSETS_LIVE = False
SPEC_DIR = "assets/spec/"

PENDING = ('<p class="hint" style="margin:8px 0 0">Not attached in this mockup. '
           'The link goes live when the file ships.</p>')


def dl(label, desc, filename, kind="Specification", audience="commercial"):
    """One download card. Fires spec_download with the file name and audience."""
    href = SPEC_DIR + filename if SPEC_ASSETS_LIVE else "#"
    note = "" if SPEC_ASSETS_LIVE else PENDING
    return (f'<a href="{href}" data-ev="spec_download" data-ev-file="{filename}" '
            f'data-ev-audience="{audience}">'
            f'<p class="meta">{kind}</p><h3>{label}</h3>'
            f'<p class="desc" style="color:var(--ink-70);margin:8px 0 0">{desc}</p>'
            f'{note}<span class="arrow">Download</span></a>')


def sgrid(cards_html):
    return f'<div class="sgrid">{"".join(cards_html)}</div>'


# --------------------------------------------------------------- published ranges
def range_table(category=""):
    """§7.6 capability statement. Built from the same spec data the category pages
    publish, so the two can never disagree."""
    rows = ""
    for p in D.PRODUCTS:
        s = dict(p["spec"])
        w = s.get("Width range") or s.get("Opening width") or "&mdash;"
        h = s.get("Height range") or s.get("Panel width") or "&mdash;"
        op = (s.get("Opacity") or s.get("Material") or s.get("Lining")
              or s.get("Fold style") or "&mdash;")
        rows += (f'<tr><th scope="row"><a class="link" href="{p["slug"]}.html">'
                 f'{p["short"]}</a></th><td>{w}</td><td>{h}</td><td>{op}</td></tr>')
    return f"""<div class="scrollx"><table class="spec2" data-category="{category}">
      <caption class="hint" style="text-align:left;margin-bottom:12px">Published ranges for every line. Shutters are quoted by opening width and panel width because they are framed.</caption>
      <thead><tr><th scope="col">Line</th><th scope="col">Width</th><th scope="col">Height</th><th scope="col">Opacity or material</th></tr></thead>
      <tbody>{rows}</tbody></table></div>"""


# ============================================================ §7.6 commercial
SECTORS = [
    ("Multifamily", "Repeatable, replaceable, cordless",
     "trade-multifamily-living-1536.webp", [
         "Cordless is standard on every line, which removes the main compliance question on a rental schedule.",
         "Vinyl verticals and faux wood cost the least to replace per unit and survive turnover.",
         "Louvres and vanes are replaceable parts, so a damaged treatment is a $6 component, not a reorder.",
         "Hold one colour across the scheme and a single spare box covers every stack.",
     ], "vertical-blinds"),
    ("Hospitality", "Blackout at the guest room, sheer at the lounge",
     "trade-hospitality-room-1536.webp", [
         "Double cell blackout cellular with SmartPrivacy&reg; channels is the darkest guest-room combination we build.",
         "Sheer shades handle the public rooms where the view is the amenity.",
         "TruQuiet&trade; motorisation is specified where housekeeping cannot reach a high window.",
         "Fabric direction stays consistent between floors because openness is published, not sampled by eye.",
     ], "cellular-shades"),
    ("Workplace", "Glare on the screen is the whole brief",
     "trade-office-open-1536.webp", [
         "1% and 3% solar screens kill monitor reflections and keep the daylight that people actually want.",
         "5% and 10% suit meeting rooms where the view matters more than the screen.",
         "Runs up to 108\" wide on a single roller; wider openings are coupled.",
         "Specify openness by elevation, not by floor. West is not the same problem as north.",
     ], "roller-solar-shades"),
    ("Healthcare", "Wipeable surfaces, no looped cords",
     "trade-commercial-lobby-1536.webp", [
         "Composite faux wood and vinyl wipe down and do not warp in a humid or frequently cleaned room.",
         "No looped cords anywhere in the line, which matters in behavioural health and paediatrics.",
         "Framed shutters seal an opening better than anything else we make.",
         "Replaceable slats keep a damaged unit out of the capital budget.",
     ], "faux-wood-blinds"),
    ("Education", "Darken a room without darkening the building",
     "trade-office-meeting-1536.webp", [
         "Room-darkening roller shades handle projection without going fully blackout.",
         "Cordless lift removes the ligature and entanglement question in a classroom.",
         "Faux wood survives being knocked, and the slats are individually replaceable.",
         "One fabric across a wing keeps the elevation reading consistently from outside.",
     ], "roller-solar-shades"),
]

CASES = [
    ("Multifamily", "184 units, three buildings",
     "Vinyl verticals on every patio door and faux wood on every bedroom window, one colour throughout. "
     "The spare-parts box holds louvres and vanes rather than complete treatments, so unit turnover is a "
     "part swap by the on-site team instead of a reorder.",
     [("184", "units"), ("2", "lines specified"), ("1", "colour across the scheme")]),
    ("Hospitality", "96-key select service hotel",
     "Double cell blackout cellular in the guest rooms with SmartPrivacy&reg; side channels, sheer shades in "
     "the lobby and the breakfast room. Guest rooms hit the dark the brief asked for; the public rooms kept "
     "the view that sells them.",
     [("96", "guest rooms"), ("2", "opacities"), ("0", "looped cords")]),
    ("Workplace", "Two floors, 11,000 sq ft",
     "3% solar screens on the west and south elevations, 10% on the north where glare was never the issue. "
     "Openness was specified per elevation from the published numbers rather than matched by eye on site.",
     [("3%", "west and south"), ("10%", "north"), ("108\"", "widest single roller")]),
]


def build_commercial():
    ctas = ('<a class="btn" href="#inquiry">Start a project</a>'
            '<a class="btn btn--ghost" href="commercial-spec-library.html">Spec library</a>')
    body = phero_media(
        "Commercial", "Specified for buildings, not just windows.",
        "Veneta is the window fashions brand of Richfield Window Coverings. Published size ranges, cordless "
        "lift as standard and replaceable parts are what make the line specifiable at volume.",
        "trade-commercial-lobby-1536.webp",
        "A commercial lobby fitted with Veneta solar shades on a tall glazed elevation.",
        trail=[("Home", "index.html"), ("Commercial", None)], ctas=ctas)

    body += f"""
  {anchors([(s[0], slugify(s[0])) for s in SECTORS] + [("Capability", "capability"), ("Downloads", "downloads"), ("Inquiry", "inquiry")])}
  <section class="tight">
    <div class="wrap">
      {shead('Sectors', 'Five briefs, not one product list.')}
      <div class="tiles">{''.join(
        f'<a class="tile rev" href="#{slugify(n)}"><div class="ph"><img src="assets/img/{img}" alt="{n} interior fitted with Veneta window treatments" loading="lazy"></div><div class="cap"><h3>{n}</h3><p>{sub}</p></div></a>'
        for n, sub, img, pts, key in SECTORS)}</div>
    </div>
  </section>
"""

    blocks = ""
    for i, (name, sub, img, pts, key) in enumerate(SECTORS):
        blocks += f"""<div id="{slugify(name)}" style="padding-top:clamp(48px,6vw,80px)">
          {rowfeat(name, sub + ".",
                   '<ul class="ticks">' + "".join(f"<li>{x}</li>" for x in pts) + "</ul>",
                   img, f"{name} project fitted with Veneta window treatments",
                   cta=f'<a class="btn btn--ghost btn--sm" href="{key}.html">Start with {D.BY_SLUG[key]["short"]}</a>',
                   flip=(i % 2 == 1))}
        </div>"""
    body += f'<section class="tight"><div class="wrap">{blocks}</div></section>{SLAT}'

    body += f"""
  <section id="capability">
    <div class="wrap">
      {shead('Capability', 'What we will put in writing.')}
      <div class="two" style="align-items:start">
        <div class="prose" style="max-width:none;min-width:0">
          {prose_blocks([
            ("h3", "Manufacturing"),
            ("p", "Every treatment is made to the measurement supplied. There is no stock-size substitution and no rounding to the nearest inch."),
            ("h3", "Lead time"),
            ("p", "Standard retail lead time is 10 to 15 business days. Volume orders are scheduled against your programme and we commit to dates in writing rather than estimating them."),
            ("h3", "Safety"),
            ("p", "Cordless lift is standard across all eight lines, so there is no looped operating cord to specify around or to certify."),
            ("h3", "Warranty"),
            ("p", 'Limited lifetime on mechanism and workmanship. <a class="link" href="warranty.html">Full terms</a>, including what volume and commercial installations change.'),
          ])}
        </div>
        <div style="min-width:0">
          {range_table()}
          {kv([("Cordless lift", "Standard, all lines"),
               ("Widest single unit", 'DualDrape&trade; to 192"'),
               ("Replaceable parts", "Slats, louvres, vanes, valances"),
               ("Motorisation", "TruQuiet&trade;, rechargeable lithium"),
               ("Lead time", "10 to 15 business days standard")])}
        </div>
      </div>
    </div>
  </section>

  <section class="tight">
    <div class="wrap">
      {shead('Projects', 'Three composite examples.',
             'Illustrative: these are representative of the specifications we quote, assembled from typical projects. They are not named references and no client is identified.')}
      <div class="three">{''.join(
        f'<div class="box rev"><p class="meta">{sec}</p><h3 style="margin:6px 0 10px">{scale}</h3>'
        f'<p style="color:var(--ink-70)">{txt}</p>{stats(st)}</div>'
        for sec, scale, txt, st in CASES)}</div>
      <div class="callout" style="max-width:860px;margin-top:40px"><p><strong>Labelled honestly:</strong> Veneta does not publish named case studies or client logos without written consent. When consented references exist they will replace these three panels.</p></div>
    </div>
  </section>

  <section id="downloads">
    <div class="wrap">
      {shead('Downloads', 'Specification, drawings and policy.',
             right=f'<a class="btn btn--ghost btn--sm" href="commercial-spec-library.html">Full spec library</a>')}
      {sgrid([
        dl("Commercial spec book", "Published size ranges, mount depths, weights and tolerances for all eight lines.", "veneta-commercial-spec-book.pdf"),
        dl("CSI three-part spec", "Editable Section 12 24 00 text for window shades and blinds.", "veneta-csi-122400.docx", kind="CSI"),
        dl("DWG detail pack", "Headrail, bracket and shutter frame sections in DWG and PDF.", "veneta-details.zip", kind="CAD"),
      ])}
    </div>
  </section>

  <section class="tight" id="inquiry">
    <div class="wrap">
      {shead('Inquiry', 'Start a project.', 'Tell us the building and the problem. If you already have a window schedule or a drawing set, that is all we need.')}
      <div class="withside">
        <div>
          <form class="form" data-mock data-ev="commercial_inquiry" data-ev-audience="commercial">
            <div><label for="c-name">Name</label><input id="c-name" required></div>
            <div><label for="c-firm">Company</label><input id="c-firm" required></div>
            <div><label for="c-email">Email</label><input id="c-email" type="email" required></div>
            <div><label for="c-phone">Phone</label><input id="c-phone" type="tel"></div>
            <div><label for="c-sector">Sector</label>
              <select id="c-sector" data-ev-param="sector">{''.join(f'<option>{s[0]}</option>' for s in SECTORS)}<option>Other</option></select></div>
            <div><label for="c-role">Your role</label>
              <select id="c-role" data-ev-param="firm_type"><option>Architect or designer</option><option>General contractor</option><option>Owner or developer</option><option>Property or facilities manager</option><option>Purchasing</option></select></div>
            <div><label for="c-units">Openings or units</label><input id="c-units" placeholder="Approximate is fine"></div>
            <div><label for="c-when">Programme date</label><input id="c-when" placeholder="Month and year"></div>
            <div class="full"><label for="c-scope">Scope</label><textarea id="c-scope" style="min-height:110px" placeholder="Building type, elevations, the performance you need, and whether installation is in your scope or ours."></textarea></div>
            <div class="full"><button class="btn" type="submit">Send project inquiry</button>
              <p class="mockmsg hint" hidden style="margin-top:12px;color:var(--success)">Mockup only: nothing has been submitted. In build, commercial inquiries route to the trade desk and are answered within one business day.</p>
              <p class="hint">We use these details to quote the project. We do not add commercial contacts to a marketing list.</p></div>
          </form>
        </div>
        <aside class="side">
          <div class="box tint sticky-box"><h4>What lets us quote fast</h4><ul>
            <li>Unit count and a window schedule, or a drawing set.</li>
            <li>Product and fabric, or the performance requirement if you want us to specify it.</li>
            <li>Delivery phasing and the site address.</li>
            <li>Whether installation is in your scope or ours.</li></ul></div>
          <div class="box"><h4>Trade, not commercial?</h4><p style="margin:0;color:var(--ink-70)">Single homes, design projects and volume residential are handled by the trade desk.</p>
            <a class="btn btn--ghost btn--sm" href="for-professionals.html" style="margin-top:14px">For professionals</a></div>
          <div class="box"><h4>Direct</h4><p style="margin:0;color:var(--ink-70)">1-855-558-1222, option 3. Monday to Friday, 8am to 6pm ET.</p></div>
        </aside>
      </div>
    </div>
  </section>
  {cta_band("Small project, or one window?",
            "Everything in the line is configured and sold at The Home Depot, at the same published sizes we quote commercially.",
            ("Shop at The Home Depot", HD.href("brand", module="cta_band", category="commercial")),
            ("Order free samples", "free-samples.html"))}
"""
    write("commercial.html", page(
        "Commercial Window Coverings &amp; Spec | VENETA&trade;",
        "Commercial window coverings for multifamily, hospitality, workplace, healthcare and education: published spec ranges, cordless lift, CSI and CAD files.",
        body, active=""))


# ============================================ commercial spec library
LIB = [
    ("Specification", [
        dl("Commercial spec book", "Every published range, mount depth, weight and tolerance in one PDF.", "veneta-commercial-spec-book.pdf"),
        dl("CSI three-part spec", "Editable Section 12 24 00 text for window shades and blinds.", "veneta-csi-122400.docx", kind="CSI"),
        dl("Fabric and openness schedule", "Openness factors, opacities and colourways by line, with fabric weights.", "veneta-fabric-schedule.pdf"),
    ]),
    ("Drawings", [
        dl("DWG detail pack", "Headrail, bracket, pocket and shutter frame sections.", "veneta-details.zip", kind="CAD"),
        dl("Mount depth diagrams", "Minimum and recommended depth for inside mount, by line.", "veneta-mount-depths.pdf", kind="CAD"),
        dl("Shutter frame profiles", "L-frame, deco frame and Z-frame sections at full scale.", "veneta-shutter-frames.pdf", kind="CAD"),
    ]),
    ("Compliance and policy", [
        dl("Cordless statement", "Written confirmation that cordless lift is standard on every line.", "veneta-cordless-statement.pdf", kind="Compliance"),
        dl("Warranty terms", "Limited lifetime coverage, exclusions and the claim process.", "veneta-warranty.pdf", kind="Policy"),
        dl("Care and maintenance", "Cleaning method by material, for facilities teams.", "veneta-care-maintenance.pdf", kind="Policy"),
    ]),
]


def build_spec_library():
    body = phero(
        "Spec library", "Every document, one page.",
        "Specification text, drawing files and written policy for the eight Veneta lines. Nothing here needs a form filled in first.",
        trail=[("Home", "index.html"), ("Commercial", "commercial.html"), ("Spec library", None)],
        ctas='<a class="btn" href="commercial.html#inquiry">Start a project</a><a class="btn btn--ghost" href="for-professionals-resources.html">Trade resources</a>')

    groups = ""
    for i, (name, items) in enumerate(LIB):
        groups += f"""<div style="padding-top:{'0' if i == 0 else 'clamp(48px,6vw,72px)'}">
          {shead(f'{str(i+1).zfill(2)}', name + ".")}
          {sgrid(items)}
        </div>"""

    body += f"""
  <section class="tight"><div class="wrap">{groups}</div></section>
  {SLAT}
  <section>
    <div class="wrap">
      {shead('Published ranges', 'The numbers the documents are built from.',
             'If a download and this table ever disagree, the table is correct: both are generated from the same product data.')}
      {range_table()}
      <p class="hint" style="margin-top:18px">Per-line detail sits on the category pages:
        {' &middot; '.join(f'<a class="link" href="{p["slug"]}.html">{p["short"]}</a>' for p in D.PRODUCTS)}.</p>
    </div>
  </section>
  {cta_band("Need something that is not here?",
            "Tell us the document you need for the submittal and we will send it or write it.",
            ("Contact the trade desk", "commercial.html#inquiry"), ("Call 1-855-558-1222", "contact.html"))}
"""
    write("commercial-spec-library.html", page(
        "Commercial Spec Library &mdash; CSI, CAD, Warranty | VENETA&trade;",
        "Download Veneta commercial spec documents: spec book, CSI Section 12 24 00 text, DWG details, mount depths, cordless statement and warranty terms.",
        body, active=""))


# ============================================ §7.5 trade resources
TRADE_RES = [
    ("Specification", [
        dl("Trade spec book", "Published ranges, mount depths and tolerances for all eight lines.", "veneta-trade-spec-book.pdf", audience="trade"),
        dl("Fabric and openness schedule", "Openness factors and opacities, with fabric weights and colourways.", "veneta-fabric-schedule.pdf", audience="trade"),
        dl("Mount depth diagrams", "Minimum and recommended depth for inside mount, by line.", "veneta-mount-depths.pdf", kind="CAD", audience="trade"),
    ]),
    ("Client-facing", [
        dl("Measuring worksheet", "One page per window: opening, mount, product, fabric, lift.", "veneta-measuring-worksheet.pdf", kind="Worksheet", audience="trade"),
        dl("Fabric care card", "Cleaning method by material, sized to leave with the client.", "veneta-care-card.pdf", kind="Client leave-behind", audience="trade"),
        dl("Cordless safety card", "The cordless statement in plain language, for handover packs.", "veneta-cordless-card.pdf", kind="Client leave-behind", audience="trade"),
    ]),
]

TRADE_FAQ = [
    ("How do trade orders get placed?",
     "<p>Through The Home Depot like any other order, or through the trade desk when the order is multi-unit, phased, or needs dates committed in writing. The product and the published sizes are identical either way.</p>"),
    ("Is there trade pricing?",
     "<p>Volume and development pricing is quoted per project. Single orders are priced at The Home Depot, and we do not undercut the retail price through a side channel.</p>"),
    ("What lead time should I put in a schedule?",
     "<p>10 to 15 business days for standard orders. Volume orders are scheduled to your programme and confirmed in writing, so put the confirmed date in the schedule rather than the standard one.</p>"),
    ("Can you specify on my behalf?",
     "<p>Yes. Send the elevations and the performance requirement (glare, blackout, humidity, span) and we will come back with a line, a fabric and an openness factor, with the reasoning.</p>"),
    ("Do you supply samples for client presentations?",
     '<p>Up to eight swatches free, with no sales call. <a class="link" href="free-samples.html">Order swatches</a>, or ask the trade desk for a larger presentation set.</p>'),
]


def build_trade_resources():
    body = phero(
        "Trade resources", "Documents, worksheets and the numbers behind them.",
        "Everything a designer, builder or installer needs to specify Veneta without emailing to ask. Published ranges, drawing files and client leave-behinds.",
        trail=[("Home", "index.html"), ("For professionals", "for-professionals.html"), ("Resources", None)],
        ctas='<a class="btn" href="free-samples.html">Request a sample kit</a><a class="btn btn--ghost" href="commercial-spec-library.html">Commercial spec library</a>')

    groups = ""
    for i, (name, items) in enumerate(TRADE_RES):
        groups += f"""<div style="padding-top:{'0' if i == 0 else 'clamp(48px,6vw,72px)'}">
          {shead(f'{str(i+1).zfill(2)}', name + ".")}
          {sgrid(items)}
        </div>"""

    body += f"""
  <section class="tight"><div class="wrap">{groups}</div></section>
  <section>
    <div class="wrap">
      {shead('Specify by problem', 'The four requirements that come up most.')}
      {steps([
        ("Glare on screens", "1% or 3% solar screen on west and south elevations. 10% where the view matters more than the monitor."),
        ("Blackout for sleep", "Double cell blackout cellular with SmartPrivacy&reg; side channels. Framed shutters where the opening must seal."),
        ("Humidity", "Composite faux wood or vinyl vertical. Nothing woven, nothing that can wick."),
        ("Wide spans", 'DualDrape&trade; to 192" or verticals to 144". Above that, couple the runs and say so in the schedule.'),
      ], four=True)}
    </div>
  </section>
  {SLAT}
  <section class="tight">
    <div class="wrap">
      {shead('Published ranges', 'Copy these into your schedule.')}
      {range_table()}
    </div>
  </section>
  <section>
    <div class="wrap">
      {shead('Trade questions', 'The five we are actually asked.')}
      {acc(TRADE_FAQ)}
      <div class="callout" style="max-width:860px;margin-top:40px"><p><strong>Trade desk:</strong> 1-855-558-1222, option 3, or use the <a class="link" href="contact.html">contact form</a> and select "Trade and professional enquiry". We reply within one business day.</p></div>
    </div>
  </section>
  {cta_band("Working on a building rather than a room?",
            "Multifamily, hospitality, workplace, healthcare and education have their own brief and their own documents.",
            ("Commercial", "commercial.html"), ("Spec library", "commercial-spec-library.html"))}
"""
    write("for-professionals-resources.html", page(
        "Trade Resources &mdash; Spec Book, CAD, Worksheets | VENETA&trade;",
        "Downloadable Veneta trade resources: spec book, fabric and openness schedule, mount depth diagrams, measuring worksheet and client care cards.",
        body, active=""))


# ============================================ §6.2 decision comparison
CMP_ROWS = [
    ("What it actually is",
     "A fabric panel: rolled, stacked, folded or cellular.",
     "Horizontal or vertical slats that tilt.",
     "A framed panel of louvres, fixed to the opening."),
    ("Light control",
     "On or off, plus whatever the fabric passes. Openness is published as a number.",
     "Infinitely adjustable by tilt without moving the treatment.",
     "Adjustable by tilt, and the whole panel opens away from the glass."),
    ("Blackout available",
     "Yes. Double cell blackout with side channels is the darkest we build.",
     "No. Light passes at every slat edge, always.",
     "Close to it with a framed fit, but never absolute."),
    ("Best rooms",
     "Bedrooms, nurseries, media rooms, home offices.",
     "Kitchens, bathrooms, utility rooms, rentals.",
     "Living rooms, dining rooms, bay windows, period houses."),
    ("Humidity and grease",
     "Avoid above a sink or a hob unless it is vinyl.",
     "Faux wood and vinyl wipe clean and will not warp.",
     "Composite handles a bathroom; real wood does not."),
    ("Wide openings",
     'To 192" on DualDrape&trade;; most fabric lines stop near 96".',
     'Verticals run to 144" and slide clear of a patio door.',
     'To 144" with multiple panels, but the panels need somewhere to swing.'),
    ("Cleaning",
     "Vacuum with a brush head. Spot clean only.",
     "Wipe with a damp cloth. The fastest to clean.",
     "Dust the louvres. Slowest, because there are more surfaces."),
    ("Cost order",
     "Middle. Cellular and roller are the value end of fabric.",
     "Lowest. Faux wood and vinyl are the cheapest per window.",
     "Highest. It is joinery fitted to the opening."),
    ("Resale and permanence",
     "Replaceable soft furnishing. Comes with you if you want.",
     "Replaceable, and cheap enough to renew per tenancy.",
     "Reads as part of the house. Stays with it."),
]

CMP_FAQ = [
    ("Blinds or shades for a bedroom?",
     "<p>Shades. Blinds leak light at every slat edge, which is a physical property of slats and not a quality issue. Double cell blackout cellular shades with SmartPrivacy&reg; side channels are the darkest combination we build.</p>"),
    ("Which is cheapest?",
     "<p>Blinds, specifically faux wood and vinyl vertical. Shades sit in the middle. Shutters cost the most because they are a framed panel fitted to the opening rather than a treatment hung in front of it.</p>"),
    ("What works over a bath or above a hob?",
     "<p>Composite faux wood blinds or vinyl verticals. Both wipe clean and neither warps. Avoid fabric shades in either position unless the fabric is vinyl.</p>"),
    ("What covers a patio door?",
     '<p>Something that moves aside. <a class="link" href="dualdrape.html">DualDrape&trade;</a> gives a soft drapery face that rotates and traverses; <a class="link" href="vertical-blinds.html">vertical blinds</a> do the same job for less. Shutters can work as bypass panels if there is room to stack them.</p>'),
    ("Do any of them cut a heating bill?",
     '<p>Cellular shades and framed shutters, because both trap air at the glass. Double cell insulates best of anything we make. See <a class="link" href="cellular-shades.html">cellular shades</a> for the cell sizes.</p>'),
    ("Are all three cordless?",
     '<p>Yes. Cordless lift is standard on every Veneta line, so the choice between blinds, shades and shutters is never a safety trade-off. See <a class="link" href="child-safety.html">child safety</a>.</p>'),
]

CMP_PICKS = [
    ("Choose shades if", ["The room needs to get dark.", "You want a soft, uninterrupted face at the window.",
                          "You care about the heating and cooling bill.", "You want a published openness number to specify against."],
     "cellular-shades"),
    ("Choose blinds if", ["The window is above a sink, a hob or a bath.", "You want to tilt for light without raising anything.",
                          "It is a rental and replacement cost matters.", "The opening is a wide slider."],
     "faux-wood-blinds"),
    ("Choose shutters if", ["You want the window to read as architecture.", "The house has strong existing joinery.",
                           "You are staying, and want it to add to the house.", "The opening is a bay or an odd shape."],
     "shutters"),
]


def build_comparison():
    body = phero_media(
        "Comparison", "Blinds, shades or shutters?",
        "Three different objects, not three styles of the same thing. The difference that decides it is usually light leak, humidity or how wide the opening is.",
        "style-quiet-traditional-1536.webp",
        "A traditional room showing shutters, blinds and shades side by side at three windows.",
        trail=[("Home", "index.html"), ("Buying guides", "buying-guides.html"), ("Blinds vs shades vs shutters", None)],
        ctas='<a class="btn" href="product-finder.html">Find your match</a><a class="btn btn--ghost" href="free-samples.html">Order free samples</a>')

    rows = "".join(
        f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
        for a, b, c, d in CMP_ROWS)

    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="prose">
        {prose_blocks([
          ("h2", "The one-line answer"),
          ("p", "Shades block light and insulate. Blinds adjust light and survive water. Shutters are joinery, and they change how the window reads."),
          ("p", "Everything below is the same three-way comparison at more detail. If you would rather answer three questions and be told, use the <a class=\"link\" href=\"product-finder.html\">product finder</a>."),
        ])}
      </div>
    </div>
  </section>
  <section>
    <div class="wrap">
      {shead('Side by side', 'Nine differences that matter.')}
      <div class="scrollx"><table class="spec2" data-category="comparison">
        <thead><tr><th scope="col">&nbsp;</th><th scope="col">Shades</th><th scope="col">Blinds</th><th scope="col">Shutters</th></tr></thead>
        <tbody>{rows}</tbody></table></div>
      <p class="hint" style="margin-top:16px">Veneta shades: cellular, roller and solar, roman, sheer, DualDrape&trade;. Veneta blinds: faux wood, vertical. Veneta shutters: engineered hardwood composite.</p>
    </div>
  </section>
  {SLAT}
  <section class="tight">
    <div class="wrap">
      {shead('Decide', 'Four statements each. Whichever list you nod at most is your answer.')}
      <div class="three">{''.join(
        f'<div class="box rev"><h3>{h}</h3><ul class="ticks" style="margin-top:14px">'
        + "".join(f"<li>{x}</li>" for x in pts)
        + f'</ul><a class="btn btn--ghost btn--sm" href="{key}.html" style="margin-top:18px">See {D.BY_SLUG[key]["short"]}</a></div>'
        for h, pts, key in CMP_PICKS)}</div>
    </div>
  </section>
  <section>
    <div class="wrap">
      {shead('By room', 'The same decision, made six times.')}
      <div class="sgrid">{''.join(
        f'<a href="shop-by-room.html#{slugify(n)}"><p class="meta">{n}</p><h3>{sub}</h3><span class="arrow">Room guide</span></a>'
        for n, sub, img in D.ROOMS[:6])}</div>
    </div>
  </section>
  <section class="tight">
    <div class="wrap">
      {shead('Questions', 'The six that decide it.')}
      {acc(CMP_FAQ)}
    </div>
  </section>
  {cta_band("Narrowed it down to two?",
            "Order swatches of both. Colour and openness cannot be judged on a screen, and a swatch settles it in a day.",
            ("Order free samples", "free-samples.html"), ("Answer three questions", "product-finder.html"))}
"""
    write("blinds-vs-shades-vs-shutters.html", page(
        "Blinds vs Shades vs Shutters &mdash; How to Choose | VENETA&trade;",
        "Blinds, shades and shutters compared on light control, blackout, humidity, wide openings, cleaning and cost, with a straight recommendation for each room.",
        body, active="products"))


def build_all():
    build_commercial()
    build_spec_library()
    build_trade_resources()
    build_comparison()
