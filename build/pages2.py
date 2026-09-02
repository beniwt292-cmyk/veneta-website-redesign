#!/usr/bin/env python3
"""Innovation, support, guides, journal, company and legal pages."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hd as HD
from shell import (page, crumbs, phero, phero_media, anchors, SLAT, shead, acc,
                   steps, kv, vids, tiles, cards, rowfeat, stats, cta_band, support_strip)
import data as D
from build_site import write, slugify, ROOT
import pic as PIC


# ---------------------------------------------------------------- innovation hub + detail
def build_innovation():
    grid = ""
    for name, href, desc in D.INNOVATIONS:
        grid += f'<a class="card rev" href="{href}"><div class="ph"><img src="assets/img/{"cellular-card.webp" if "ClearFit" in name else "roller-card.webp" if "SmartRail" in name else "sheer-card.webp" if "SmartPrivacy" in name else "roman-card.webp" if "TruQuiet" in name else "solar-card.webp"}" alt="{re.sub("&[a-z]+;", "", name)} detail" loading="lazy"></div><h3>{name}</h3><p class="desc">{desc}</p><p class="price">Learn more</p></a>'
    body = phero("Innovation", "Five details you only notice when they're missing.",
                 "Veneta engineering is not about features on a box. It is about the edge gap you stop seeing, the shade that still tracks straight after five years, and a motor quiet enough to run during a film.",
                 trail=[("Home", "index.html"), ("Innovation", None)],
                 ctas='<a class="btn" href="products.html">See the products</a><a class="btn btn--ghost" href="child-safety.html">Child safety standards</a>')
    body += f"""
  <section><div class="wrap"><div class="cards">{grid}</div></div></section>
  {SLAT}
  <section class="dark">
    <div class="wrap">
      <p class="eyebrow">By the numbers</p>
      <h2 style="max-width:22ch">Engineering you can measure.</h2>
      {stats([('1/4"', "Typical edge light gap with ClearFit&trade; headrails"), ("0", "Looped cords on any product we make"),
              ("Lifetime", "Limited warranty on every line"), ('1/8"', "Manufacturing increment on width")])}
      <div class="note"><p style="margin:0">Figures describe our manufacturing tolerances and product policy. Performance in your home depends on the window, the mount and the fabric you choose.</p></div>
    </div>
  </section>
  {support_strip()}
"""
    write("innovation.html", page("Innovation &mdash; ClearFit&trade;, SmartRail&trade;, SmartPrivacy&reg; | VENETA&trade;",
                                  "The engineering behind Veneta: ClearFit headrails, SmartRail bottom bars, SmartPrivacy side channels, TruQuiet motorization and RevitaCharge batteries.",
                                  body, active="innovation"))

    tech = [
        dict(file="clearfit.html", name="ClearFit&trade;", h1="A headrail cut to your window, not to a size chart.",
             lede="Most shades are built to the nearest half inch and the gap at the edge is left to the installer. ClearFit&trade; headrails are cut to your exact opening in 1/8&quot; increments, which is why the light gap is consistent instead of lucky.",
             img="cellular-card.webp",
             sections=[
                 ("h2", "What the problem actually is"),
                 ("p", "Every inside-mounted shade needs clearance to move. Too little and the shade drags on the frame; too much and you get a bright stripe of daylight down each side. The difference between a shade that looks made for the window and one that looks bought for it is usually a quarter of an inch."),
                 ("h2", "How ClearFit&trade; works"),
                 ("ul", ["Your measurements are cut in 1/8&quot; increments rather than rounded to the nearest half inch.",
                         "Deductions are applied by the factory, so you submit the exact opening size and nothing else.",
                         "Bracket positions are set from the same cut list, so the shade sits square in the opening.",
                         "The result is a typical edge gap of about 1/4&quot; per side on an inside mount."]),
                 ("h2", "Where it matters most"),
                 ("p", "Bedrooms, nurseries and media rooms, where the edge gap is the last light you notice before you fall asleep. Pair ClearFit&trade; with SmartPrivacy&reg; channels and a blackout fabric for the darkest result we can build."),
                 ("callout", "ClearFit&trade; is standard on cellular, sheer and Roman shades. It is not a paid upgrade."),
             ],
             faqs=[("Do I need to deduct anything from my measurements?", "<p>No. Give us the exact opening in 1/8&quot; increments. If you deduct as well, the shade will be too small.</p>"),
                   ("Does ClearFit&trade; eliminate the light gap completely?", "<p>No, and no inside-mounted shade can. It makes the gap small and consistent. To close it, add SmartPrivacy&reg; channels or use an outside mount.</p>")]),
        dict(file="smartrail.html", name="SmartRail&trade;", h1="The bottom bar is where cheap shades fail.",
             lede="A light bottom bar lets fabric curl, twist and track off-centre within a couple of seasons. SmartRail&trade; is weighted and fabric-wrapped, so the hem stays flat and the shade keeps running straight.",
             img="roller-card.webp",
             sections=[
                 ("h2", "Why weight matters"),
                 ("p", "A roller shade is a flat plane held in tension by gravity. Remove enough weight from the hem and the fabric relaxes, curls at the corners and starts to wander on the tube. Once it wanders, it wears on one edge and the problem accelerates."),
                 ("h2", "What SmartRail&trade; adds"),
                 ("ul", ["A weighted core sized to the fabric, not a single generic bar for every shade.",
                         "A wrapped face in the shade fabric, so the bar disappears into the design.",
                         "Sealed end caps that stop the bar rattling in a draught.",
                         "A consistent hem line that stays parallel to the sill."]),
                 ("h2", "Available on"),
                 ("p", "Roller and solar shades as standard, with an exposed aluminium option if you want the industrial look. Cellular and sheer shades use a matched weighted rail on the same principle."),
             ],
             faqs=[("Can I choose an exposed aluminium bar instead?", "<p>Yes, on roller and solar shades. It is a look preference; the weighting is the same.</p>"),
                   ("Does the wrapped bar add to the stack height?", "<p>Marginally, about 1/2&quot; on a fully raised shade. Most people never notice it behind a fascia or cassette.</p>")]),
        dict(file="smartprivacy.html", name="SmartPrivacy&reg;", h1="Blackout fabric is only half of a dark room.",
             lede="A blackout shade still leaks light around its edges. SmartPrivacy&reg; side channels enclose the shade against the jamb, which is the difference between a dark room and an actually dark room.",
             img="sheer-card.webp",
             sections=[
                 ("h2", "Where the light really comes from"),
                 ("p", "Ask someone to stand outside a bedroom with a blackout shade at night and you will see the outline of the window, not the fabric. Light travels around the shade through the side gaps and over the top of the headrail. Better fabric does nothing about either."),
                 ("h2", "How the channels work"),
                 ("ul", ["Aluminium channels mount to the jamb on both sides and capture the shade edge.",
                         "A brush seal keeps contact without dragging on the fabric.",
                         "A matched top treatment closes the gap above the headrail.",
                         "The result is a room that stays dark at 7am in June."]),
                 ("h2", "A secondary benefit"),
                 ("p", "Closing the edge gap also closes the air gap, which improves the insulating performance of a cellular shade. On a cold north-facing bedroom the difference is noticeable on a still night."),
                 ("callout", "SmartPrivacy&reg; is available on blackout cellular shades and blackout roller shades. It cannot be retrofitted to a Roman shade."),
             ],
             faqs=[("Will the channels be visible?", "<p>Yes, as a narrow painted channel on each side of the opening, colour-matched to the shade. They are less visible than the light gap they replace.</p>"),
                   ("Can I add channels to a shade I already own?", "<p>Only if the shade was ordered with the channel-compatible bottom bar and headrail. Contact support with your order number and we will check.</p>")]),
        dict(file="truquiet-motorization.html", name="TruQuiet&trade; Motorization", h1="Quiet enough to run during a film.",
             lede="Most window motors announce themselves. TruQuiet&trade; uses a damped drive and a soft start and stop, so the shade moves without becoming the loudest thing in the room.",
             img="roman-card.webp",
             sections=[
                 ("h2", "What quiet actually means"),
                 ("p", "Two things make a motorized shade annoying: the whine of the motor itself and the clunk at each end of travel. TruQuiet&trade; addresses both, with a damped gear train and a controlled ramp into and out of every movement."),
                 ("h2", "Power options"),
                 ("ul", ["RevitaCharge&trade; rechargeable battery pack, topped up in place with a USB-C lead.",
                         "Hardwired low-voltage supply for new build and renovation.",
                         "Solar top-up panel for bright windows you would rather not revisit."]),
                 ("h2", "Control options"),
                 ("ul", ["Handheld remote, one channel per shade or grouped by room.",
                         "Wall-mounted keypad for a fixed switch position.",
                         "ShadeAuto&trade; Hub for schedules, app control and voice assistants."]),
                 ("callout", "Smart-home support depends on your motor and hub combination. Check the <a class=\"link\" href=\"motorization.html\">compatibility list</a> before you buy. It is the single source of truth and we keep it current."),
                 ("h2", "Where motorization earns its price"),
                 ("p", "Tall windows above a stairwell. A bank of four shades you want to move together. A hot west-facing room where the shades need to close before you get home. Anywhere a manual shade means a ladder."),
             ],
             faqs=[("How long does the battery last?", "<p>Typically several months on a full charge, depending on shade size and how often it moves. The remote shows a low-battery warning well before it stops.</p>"),
                   ("Can I add motorization to an existing shade?", "<p>No. The motor sits inside the headrail and is fitted during manufacture.</p>"),
                   ("Does it work with Alexa or Google Home?", "<p>With the ShadeAuto&trade; Hub, yes, for supported motor generations. Without the hub, no. The compatibility list states exactly which combinations are supported.</p>")]),
        dict(file="motorization.html", name="Motorization &amp; Compatibility", h1="Motorization, and exactly what works with what.",
             lede="One page, kept current, that tells you which motors, hubs, remotes and voice assistants work together. If a combination is not listed here, we do not support it, whatever a product box says.",
             img="solar-card.webp",
             sections=[
                 ("h2", "Start here"),
                 ("p", "Smart-home compatibility is the single most common source of confusion in this category, and the most common source of returns. So this page is deliberately blunt: supported, or not supported."),
                 ("table", None),
                 ("h2", "What you need for voice control"),
                 ("ul", ["A TruQuiet&trade; motorized shade.",
                         "A ShadeAuto&trade; Hub on the same 2.4GHz network.",
                         "The Veneta app, to commission the shades and create rooms and scenes.",
                         "An Amazon Alexa or Google Home account linked in the app."]),
                 ("h2", "What will not work"),
                 ("ul", ["A motorized shade with no hub, controlled by voice. The remote is radio-only.",
                         "Apple Home, which is not supported at this time.",
                         "Third-party hubs and universal blind controllers.",
                         "Cordless manual shades, which have no motor to talk to."]),
                 ("callout", "If you have seen a claim elsewhere on the site or on packaging that conflicts with this page, this page is correct. Tell us where you saw it and we will fix it."),
             ],
             faqs=[("How many shades can one hub handle?", "<p>Up to 30 motors across up to 10 rooms in the app.</p>"),
                   ("Do schedules keep working if the internet drops?", "<p>Yes. Schedules run on the hub, so they continue without a cloud connection. Voice and remote app control need internet.</p>"),
                   ("Can I control shades when I am away from home?", "<p>Yes, through the app, with the hub online.</p>")]),
    ]
    cmp_table = """<div class="scrollx" style="margin:26px 0 8px"><table class="cmp">
        <thead><tr><th>Combination</th><th>Remote</th><th>App &amp; schedules</th><th>Alexa</th><th>Google Home</th><th>Apple Home</th></tr></thead>
        <tbody>
          <tr><th>TruQuiet&trade; motor only</th><td class="y">Yes</td><td class="n">No</td><td class="n">No</td><td class="n">No</td><td class="n">No</td></tr>
          <tr><th>TruQuiet&trade; + ShadeAuto&trade; Hub</th><td class="y">Yes</td><td class="y">Yes</td><td class="y">Yes</td><td class="y">Yes</td><td class="n">No</td></tr>
          <tr><th>TruQuiet&trade; + wall keypad</th><td class="y">Yes</td><td class="n">No</td><td class="n">No</td><td class="n">No</td><td class="n">No</td></tr>
          <tr><th>Cordless manual shade</th><td class="n">N/A</td><td class="n">N/A</td><td class="n">N/A</td><td class="n">N/A</td><td class="n">N/A</td></tr>
          <tr><th>Third-party hub</th><td class="n">No</td><td class="n">No</td><td class="n">No</td><td class="n">No</td><td class="n">No</td></tr>
        </tbody></table></div>
        <p class="tnote">Placeholder matrix for the mockup. In build, this table is the single source of truth and is versioned with a visible "last updated" date.</p>"""

    for t in tech:
        prose = ""
        for kind, val in t["sections"]:
            if kind == "h2":
                prose += f"<h2>{val}</h2>"
            elif kind == "p":
                prose += f"<p>{val}</p>"
            elif kind == "ul":
                prose += "<ul>" + "".join(f"<li>{x}</li>" for x in val) + "</ul>"
            elif kind == "callout":
                prose += f'<div class="callout"><p>{val}</p></div>'
            elif kind == "table":
                prose += cmp_table
        others = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h, _ in D.INNOVATIONS if h != t["file"])
        body = phero_media("Innovation", t["h1"], t["lede"], t["img"], f'{re.sub("&[a-z]+;|<[^>]+>", "", t["name"])} shown in detail',
                           trail=[("Home", "index.html"), ("Innovation", "innovation.html"), (t["name"], None)],
                           ctas=HD.btn("Shop at The Home Depot", module="hero") + '<a class="btn btn--ghost" href="products.html">See compatible products</a>')
        body += f"""
  <section>
    <div class="wrap">
      <div class="withside">
        <div class="prose">{prose}
          <h2>Questions</h2>
        </div>
        <aside class="side">
          <div class="box sticky-box"><h4>More innovation</h4><ul>{others}</ul></div>
          <div class="box tint"><h4>Talk to support</h4><p style="margin:0"><strong>1-855-558-1222</strong><br><a href="contact.html" style="border-bottom:1px solid var(--daylight)">Send a message</a></p></div>
        </aside>
      </div>
      <div style="margin-top:10px">{acc(t["faqs"])}</div>
    </div>
  </section>
  {cta_band("See it on a real window.", "Every Veneta product is sold through The Home Depot, online and in store, with the full option list.", ("Shop at The Home Depot", HD.href(module="cta_band")), ("Order free samples", "free-samples.html"))}
"""
        write(t["file"], page(f'{t["name"]} | VENETA&trade;',
                              re.sub("<[^>]+>", "", t["lede"])[:155],
                              body, active="innovation"))

    # child safety
    body = phero("Child &amp; pet safety", "Cordless is the default, not an upgrade.",
                 "There is no looped cord on any window treatment Veneta makes. Not as an option you select, not as a premium line: on everything.",
                 trail=[("Home", "index.html"), ("Innovation", "innovation.html"), ("Child &amp; pet safety", None)])
    body += f"""
  <section>
    <div class="wrap">
      <div class="withside">
        <div class="prose">
          <h2>The standard we build to</h2>
          <p>Every Veneta product is designed to meet the current ANSI/WCMA A100.1 requirements for corded window covering products sold for residential use. We meet them the simple way: we do not put an operating cord on the product.</p>
          <h2>What that means at the window</h2>
          <ul>
            <li>No looped lift cord, and no continuous chain on cordless products.</li>
            <li>No tension device to screw into the wall, and nothing for a child to pull loose.</li>
            <li>No cleat to wrap a cord around, which is the step most households skip.</li>
            <li>Shades hold position anywhere you leave them, so nobody needs to tie anything off.</li>
          </ul>
          <h2>Where cords still exist in the category</h2>
          <p>Corded blinds are still legal to sell in some configurations, particularly custom commercial products. If you are buying window coverings anywhere and a cord is present, it needs to be out of reach and secured. We would rather you did not have to think about it.</p>
          <h2>Pets, too</h2>
          <p>Cats climb blinds and dogs push through them at door height. Two practical answers: removable vanes on DualDrape&trade; and vertical blinds, so a damaged section is a two-minute fix, and wipe-clean vinyl and composite materials where a nose print is inevitable.</p>
          <h2>Rooms to prioritise</h2>
          <ul>
            <li><strong>Nursery and children's bedrooms.</strong> Cordless plus blackout for daytime naps.</li>
            <li><strong>Low windows and window seats.</strong> Anywhere a child can reach the bottom rail.</li>
            <li><strong>Stair landings.</strong> Motorization removes the ladder as well as the cord.</li>
          </ul>
          <div class="callout"><p><strong>Older window coverings in the house?</strong> The Window Covering Safety Council runs a free retrofit programme for corded products. Replacing them is better, but securing them today costs nothing.</p></div>
        </div>
        <aside class="side">
          <div class="box tint sticky-box">
            <h4>Cordless on every line</h4>
            <ul>{''.join(f'<li><a href="{p["slug"]}.html">{p["short"]}</a></li>' for p in D.PRODUCTS)}</ul>
          </div>
        </aside>
      </div>
    </div>
  </section>
  {cta_band("Safe by default.", "Choose any product in the range and cordless operation comes with it.", ("Shop at The Home Depot", HD.href(module="cta_band")), ("Shop for a nursery", "shop-by-room.html#nursery"))}
"""
    write("child-safety.html", page("Child &amp; Pet Safety Standards | VENETA&trade;",
                                    "Every Veneta window treatment is cordless as standard and designed to meet ANSI/WCMA A100.1. What that means room by room.",
                                    body, active="innovation"))


# ---------------------------------------------------------------- support hub + guides
def build_support():
    body = phero("Support", "Measure it, install it, keep it looking new.",
                 "Everything you need after the order, in one place: measuring and installation guides, cleaning by material, videos for each frame type, the warranty in plain English, and a way to reach a person.",
                 trail=[("Home", "index.html"), ("Support", None)],
                 ctas='<a class="btn" href="how-to-measure.html">Start with measuring</a><a class="btn btn--ghost" href="contact.html">Contact support</a>')
    cardsets = [
        ("Guides", [("How to Measure", "how-to-measure.html", "Inside mount, outside mount, and the rule that saves most orders."),
                    ("How to Install", "how-to-install.html", "Brackets, levels and the six steps that apply to every product."),
                    ("How to Clean &amp; Care", "how-to-clean.html", "What to use on fabric, faux wood, vinyl and painted shutters.")]),
        ("Videos", [("Installation Videos", "installation-videos.html", "Short, product-specific videos with the tools listed up front."),
                    ("L-Frame Shutters", "installation-videos-l-frame.html", "Flush, trim-free shutter installation, step by step."),
                    ("Deco Frame Shutters", "installation-videos-deco-frame.html", "Full-surround shutter installation for out-of-square openings.")]),
        ("Policies &amp; contact", [("Warranty", "warranty.html", "Limited lifetime coverage, what it includes and what it does not."),
                                    ("FAQ", "faq.html", "The forty questions support answers most often."),
                                    ("Contact Us", "contact.html", "Phone, email and a form that tells you what we need.")]),
    ]
    blocks = ""
    for label, items in cardsets:
        rows = "".join(f'<a href="{h}"><p class="meta">{label}</p><h3>{n}</h3><p class="desc" style="color:var(--ink-70);margin:8px 0 0">{d}</p><span class="arrow">Open</span></a>' for n, h, d in items)
        blocks += f'<div style="margin-bottom:56px">{shead(label, "")}<div class="sgrid">{rows}</div></div>'
    blocks = blocks.replace('<div class="shead">\n        <div><p class="eyebrow">', '<div class="shead" style="margin-bottom:20px">\n        <div><p class="eyebrow">')
    body += f"""<section class="tight"><div class="wrap">{blocks}</div></section>
  {SLAT}
  <section>
    <div class="wrap">
      {shead('Common questions', 'Answered without a phone call.')}
      {acc([
        ("Where do I buy Veneta products?", '<p>Exclusively at The Home Depot, online and in store. <a class="link" href="where-to-buy.html">Where to buy</a> explains both routes.</p>'),
        ("My shade arrived the wrong size. What now?", "<p>Call 1-855-558-1222 with your Home Depot order number. Manufacturing errors are covered and replaced. Measuring errors are not covered by the warranty, but call anyway and we will tell you the cheapest way forward.</p>"),
        ("How long does a made-to-measure order take?", "<p>Typically 10 to 15 business days from order to delivery. The Home Depot order confirmation carries the current estimate for your configuration.</p>"),
        ("Can I get replacement parts?", "<p>Yes. Individual vanes, louvres, wands, brackets and remotes are all available. Have your order number ready.</p>"),
        ("Is there a spec book for trade customers?", '<p>Yes, on the <a class="link" href="for-professionals.html">professionals page</a>, with full size ranges and CAD details.</p>'),
      ])}
    </div>
  </section>
  {cta_band("Still stuck?", "Call 1-855-558-1222, Monday to Friday, 8am to 6pm CT. Or send a message and we will come back within one business day.", ("Contact support", "contact.html"), ("Read the warranty", "warranty.html"))}
"""
    write("support.html", page("Support &mdash; Measuring, Installation, Care &amp; Warranty | VENETA&trade;",
                               "Veneta support hub: measuring and installation guides, cleaning instructions by material, installation videos, warranty details and contact options.",
                               body, active="support"))

    # measure
    body = phero("Guide", "How to measure a window.",
                 "Ten minutes with a steel tape and you will not have to think about this again. Give us the exact opening size and let the factory make the deductions.",
                 trail=[("Home", "index.html"), ("Support", "support.html"), ("How to measure", None)])
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="withside">
        <div class="prose">
          <h2>What you need</h2>
          <ul><li>A steel tape measure. Not a fabric one; fabric stretches.</li><li>A pencil and paper, or the notes app.</li><li>Two minutes per window.</li></ul>
          <h2 id="mount">Step 1: decide inside or outside mount</h2>
          <p><strong>Inside mount</strong> sits within the window frame for a built-in look. It needs enough depth: 3/4&quot; for a cellular shade, 2&quot; for faux wood, 2 1/2&quot; for a Roman or sheer shade.</p>
          <p><strong>Outside mount</strong> fits to the wall or trim above the opening and overlaps it. Choose it when the frame is too shallow, out of square, or when you want maximum darkness.</p>
          {PIC.diagram_pair("diagram-inside-mount", "diagram-outside-mount",
                            "Inside mount: order the exact opening size.",
                            "Outside mount: add 4&quot; to width, 3&quot; to height.")}
          <h2 id="width">Step 2: measure the width in three places</h2>
          <p>Measure top, middle and bottom of the opening. Openings are rarely square. For an inside mount, use the <strong>narrowest</strong> of the three. For an outside mount, use the widest and add 2&quot; on each side for overlap.</p>
          {PIC.diagram("diagram-measure-width", "Three widths. The narrowest is the one you record.")}
          <h2 id="height">Step 3: measure the height in three places</h2>
          <p>Measure left, centre and right. For an inside mount, use the <strong>longest</strong> of the three so the shade reaches the sill everywhere. For an outside mount, measure from where the headrail will sit down to where you want the shade to end, plus 2&quot; below the opening.</p>
          {PIC.diagram("diagram-measure-height", "Three heights. The longest is the one you record.")}
          <h2 id="order">Step 4: write it down width first</h2>
          <p>Always width by height, to the nearest 1/8&quot;. A 36&quot; wide, 60&quot; tall window is 36 x 60, never 60 x 36. Reversing the two is the single most common ordering error in this category.</p>
          <div class="callout"><p><strong>Do not deduct anything.</strong> Submit the exact opening size. Every Veneta product is built with the correct clearance applied at the factory. If you deduct as well, the shade will be too small and it will not be covered by the warranty.</p></div>
          <h2 id="special">Special cases</h2>
          <h3>Patio and sliding doors</h3>
          <p>Measure the full opening including the frame, then decide which side the stack should sit on. Allow 6&quot; to 14&quot; of wall beside the opening for the stack on a DualDrape&trade; or vertical blind.</p>
          <h3>Bay windows</h3>
          <p>Measure each face as a separate window. Nothing tracks cleanly around the angle, so you are ordering three shades, not one.</p>
          <h3>Out-of-square openings</h3>
          <p>If the difference between your three width measurements is more than 1/2&quot;, use an outside mount, or a shutter with a deco frame that hides the discrepancy.</p>
          <h2>Before you order</h2>
          {PIC.diagram("diagram-depth-clearance", "Depth is measured in front of the glass, not across the opening.")}
          <ul><li>Check depth against the product's minimum mount depth on its page.</li><li>Confirm nothing intrudes into the opening: handles, cranks, alarm sensors, tile edges.</li><li>Write down which window each measurement belongs to. Label them.</li></ul>
        </div>
        <aside class="side">
          <div class="box sticky-box"><h4>On this page</h4><ul>
            <li><a href="#mount">Inside or outside mount</a></li><li><a href="#width">Width in three places</a></li><li><a href="#height">Height in three places</a></li><li><a href="#order">Width first, always</a></li><li><a href="#special">Special cases</a></li></ul></div>
          <div class="box tint"><h4>Minimum mount depth</h4>{kv([(lbl, d) for d, lbl, _ in D.MOUNT_DEPTH])}</div>
          <div class="box"><h4>Next</h4><ul><li><a href="how-to-install.html">How to install</a></li><li><a href="installation-videos.html">Installation videos</a></li><li><a href="contact.html">Ask a question</a></li></ul></div>
        </aside>
      </div>
    </div>
  </section>
  {cta_band("Measured up?", "Take your numbers to The Home Depot and configure the size, fabric and lift.", ("Shop at The Home Depot", HD.href(module="cta_band")), ("Order free samples", "free-samples.html"))}
"""
    write("how-to-measure.html", page("How to Measure for Blinds &amp; Shades | VENETA&trade;",
                                      "Step-by-step measuring guide for inside and outside mount, patio doors, bay windows and out-of-square openings. Submit the exact opening size.",
                                      body, active="support"))

    # install
    body = phero("Guide", "How to install.",
                 "Six steps that apply to every product in the range, plus the parts that differ. Twenty minutes for a typical shade, longer for a framed shutter.",
                 trail=[("Home", "index.html"), ("Support", "support.html"), ("How to install", None)])
    body += f"""
  <section class="tight">
    <div class="wrap">
      {shead('The sequence', 'Every product, same six steps.')}
      {steps([
        ("Unpack and check", "Confirm the width and height against your order before you make a hole. Check the box for brackets, valance clips and the wand or remote."),
        ("Mark the bracket positions", "Hold the headrail in the opening and mark through the bracket slots. Inside mount: brackets go at the top of the opening, flush with the front edge unless the instructions say otherwise."),
        ("Check level, then drill", "A shade that is 1/8\" out of level will show a wedge of light at the sill. Use a spirit level, not the window frame, as your reference."),
        ("Fit the brackets", "Pilot-drill into timber; use the supplied anchors in drywall. Snug, not overtightened. Composite brackets crack if you lean on the driver."),
        ("Clip in the headrail", "Push the headrail up and back until both brackets click. Give it a gentle tug down to confirm it is seated."),
        ("Fit the valance and test", "Clip the valance, then raise and lower the shade fully twice. Anything that binds is a bracket alignment problem, not a fabric problem."),
      ])}
    </div>
  </section>
  {SLAT}
  <section>
    <div class="wrap">
      <div class="withside">
        <div class="prose">
          {PIC.diagram("diagram-bracket-placement", "End brackets 2&quot; in, one support per 36&quot; of span.")}
          <h2>Tools you will actually need</h2>
          <ul><li>Cordless drill with a No. 2 Phillips bit</li><li>3/32&quot; pilot bit for timber, 1/4&quot; for drywall anchors</li><li>Spirit level, 12&quot; is enough</li><li>Pencil, steel tape, step ladder</li></ul>
          <h2>What differs by product</h2>
          <h3>Faux wood blinds</h3>
          <p>Heavier than fabric. On widths above 48&quot;, fit a centre support bracket. It ships in the box and it is not optional.</p>
          <h3>Vertical blinds and DualDrape&trade;</h3>
          <p>Ceiling mount is usual on a patio door. Space the brackets evenly, no more than 32&quot; apart, and fit the louvres after the track is up.</p>
          <h3>Shutters</h3>
          <p>The frame goes in first and gets shimmed square, then the panels hang on it. This is the one product where a second pair of hands genuinely helps. Watch the frame-specific video first: <a class="link" href="installation-videos-l-frame.html">L-frame</a> or <a class="link" href="installation-videos-deco-frame.html">deco frame</a>.</p>
          <h3>Motorized shades</h3>
          <p>Charge the battery pack fully before installation, then pair the remote with the shade on the bench where you can reach both buttons.</p>
          <h2>If something is wrong</h2>
          <p>Stop before you drill a second set of holes. Call 1-855-558-1222 with the order number. A manufacturing error is our problem and we will replace it.</p>
        </div>
        <aside class="side">
          <div class="box tint sticky-box"><h4>Watch instead</h4><p style="margin:0 0 12px;color:var(--ink-70)">Every product line has a short installation video with the tool list on screen.</p><a class="btn btn--ghost btn--sm" style="width:100%;justify-content:center" href="installation-videos.html">All videos</a></div>
          <div class="box"><h4>Also useful</h4><ul><li><a href="how-to-measure.html">How to measure</a></li><li><a href="how-to-clean.html">How to clean</a></li><li><a href="warranty.html">Warranty</a></li></ul></div>
        </aside>
      </div>
    </div>
  </section>
"""
    write("how-to-install.html", page("How to Install Blinds, Shades &amp; Shutters | VENETA&trade;",
                                      "Six-step installation sequence for every Veneta product, the tools you need, and what differs for faux wood, verticals, shutters and motorized shades.",
                                      body, active="support"))

    # clean
    C = D.CARE
    body = phero("Guide", "How to clean and care.",
                 "Dust first, water second, solvents never. What to use on each material and the mistakes that cause permanent marks.",
                 trail=[("Home", "index.html"), ("Support", "support.html"), ("How to clean", None)])
    body += f"""
  <section class="tight">
    <div class="wrap">
      <div class="withside">
        <div class="prose">
          <h2>The rule that covers everything</h2>
          <p>{C["rule"]}</p>
          <h2>By material</h2>
          {''.join(f'<h3>{n}</h3><p>{t}</p>' for n, t in C["by_material"])}
          <div class="callout"><p><strong>Never use:</strong> {C["never"]}</p></div>
          <h2>Seasonal maintenance, 15 minutes</h2>
          <ul>{''.join(f'<li>{i}</li>' for i in C['seasonal'])}</ul>
        </div>
        <aside class="side">
          <div class="box tint sticky-box"><h4>Quick reference</h4>{kv(C["quick"])}</div>
          <div class="box"><h4>Related</h4><ul><li><a href="warranty.html">What the warranty covers</a></li><li><a href="journal-spring-cleaning.html">Spring cleaning routine</a></li><li><a href="contact.html">Ask about a stain</a></li></ul></div>
        </aside>
      </div>
    </div>
  </section>
"""
    write("how-to-clean.html", page("How to Clean Blinds, Shades &amp; Shutters | VENETA&trade;",
                                    "Cleaning and care instructions by material for cellular, roller, Roman, sheer, faux wood, vinyl and shutter products, plus what never to use.",
                                    body, active="support"))


def build_videos():
    common = [
        ("Cellular shades: inside mount", "Bracket placement, clip-in headrail, valance.", "3:12", "cellular-card.webp"),
        ("Roller shades: fascia and cassette", "Fitting the fascia before the tube goes in.", "4:05", "roller-card.webp"),
        ("Roman shades: bracket alignment", "Getting the fold stack to hang square.", "3:48", "roman-card.webp"),
        ("Faux wood: centre support bracket", "Why wide blinds need the third bracket.", "2:31", "fauxwood-card.webp"),
        ("Vertical blinds: ceiling mount", "Bracket spacing and hanging the louvres.", "5:20", "vertical-card.webp"),
        ("DualDrape&trade;: track and vanes", "Split stack setup on a patio door.", "6:02", "dualdrape-card.webp"),
        ("Sheer shades: vane handling", "Unpacking without creasing the vanes.", "2:58", "sheer-card.webp"),
        ("TruQuiet&trade;: pairing a remote", "Commissioning a motor and setting limits.", "4:41", "solar-card.webp"),
        ("ShadeAuto&trade; Hub: first setup", "Network, rooms, schedules, voice linking.", "7:15", "hero-card.webp"),
    ]
    body = phero("Videos", "Installation videos.",
                 "Short, product-specific and honest about how long each job takes. Tools are listed on screen in the first ten seconds so you can gather everything before you start.",
                 trail=[("Home", "index.html"), ("Support", "support.html"), ("Installation videos", None)],
                 ctas='<a class="btn btn--ghost" href="how-to-install.html">Read the written guide</a>')
    body += f"""
  <section class="tight"><div class="wrap">{shead('All products', 'Nine videos, none longer than eight minutes.')}{vids(common)}
      <p class="tnote" style="margin-top:24px">Video thumbnails are placeholders in this mockup. In build, each embeds a captioned video with a transcript below it for accessibility and search.</p></div></section>
  {SLAT}
  <section><div class="wrap">{shead('Shutters', 'Two frame types, two playlists.')}
    <div class="two">
      <div><h3>L-frame</h3><p style="color:var(--ink-70)">Flush inside the opening, no added trim. The cleanest look, and the one that needs the squarest opening.</p><a class="btn btn--ghost btn--sm" href="installation-videos-l-frame.html">L-frame videos</a></div>
      <div><h3>Deco frame</h3><p style="color:var(--ink-70)">A visible surround that finishes the opening and forgives an out-of-square wall.</p><a class="btn btn--ghost btn--sm" href="installation-videos-deco-frame.html">Deco frame videos</a></div>
    </div></div></section>
"""
    write("installation-videos.html", page("Installation Videos | VENETA&trade;",
                                           "Product-specific installation videos for cellular, roller, Roman, faux wood, vertical, DualDrape and sheer shades plus motorization setup.",
                                           body, active="support"))

    for f, label, blurb, vlist in [
        ("installation-videos-l-frame.html", "L-frame shutters",
         "L-frame shutters sit flush inside the opening with no added trim, so the panel face lines up with the wall. It is the cleanest result and the least forgiving of an out-of-square opening, which is why the frame goes in first and gets shimmed before any panel is hung.",
         [("L-frame: check the opening", "Measuring diagonals and finding the worst corner.", "3:22", "shutters-card.webp"),
          ("L-frame: assemble the frame", "Corner joints, glue and squaring on the floor.", "5:10", "shutters-card.webp"),
          ("L-frame: shim and fix", "Where to shim and how much is too much.", "4:47", "hero-card.webp"),
          ("L-frame: hang the panels", "Hinge pins, panel gaps and the reveal line.", "4:02", "shutters-card.webp"),
          ("L-frame: set the louvre tension", "Adjusting tension so louvres hold position.", "2:44", "shutters-card.webp"),
          ("L-frame: final trim and caulk", "Finishing the joint between frame and wall.", "3:31", "hero-card.webp")]),
        ("installation-videos-deco-frame.html", "Deco frame shutters",
         "A deco frame adds a visible surround to the opening. It reads more traditional, it finishes a rough or previously trimmed opening properly, and it hides a good deal of discrepancy in a wall that is not square. If you are unsure which frame you have, check the order confirmation.",
         [("Deco frame: unpack and identify parts", "Frame profiles, panels and the hardware pack.", "2:50", "shutters-card.webp"),
          ("Deco frame: dry fit the surround", "Checking coverage before you fix anything.", "4:18", "hero-card.webp"),
          ("Deco frame: fixing to masonry", "Anchors, pilot depth and avoiding blow-out.", "5:36", "shutters-card.webp"),
          ("Deco frame: fixing to timber", "Pilot sizes and screw placement in trim.", "3:59", "shutters-card.webp"),
          ("Deco frame: hang and align panels", "Setting the gap so panels close cleanly.", "4:25", "shutters-card.webp"),
          ("Deco frame: bi-fold configurations", "Hinging three and four panel runs.", "6:08", "hero-card.webp")]),
    ]:
        body = phero("Videos", label + ".", blurb,
                     trail=[("Home", "index.html"), ("Support", "support.html"), ("Installation videos", "installation-videos.html"), (label, None)],
                     ctas='<a class="btn btn--ghost" href="shutters.html">See shutter specifications</a>')
        body += f"""<section class="tight"><div class="wrap">{vids(vlist)}
        <p class="tnote" style="margin-top:24px">Placeholder thumbnails. Each video ships with captions and a written transcript.</p>
        <div class="callout" style="max-width:860px"><p><strong>Not sure which frame you ordered?</strong> The order confirmation lists the frame type, or call 1-855-558-1222 with the order number and we will check.</p></div></div></section>
        {cta_band("Shutters, properly fitted.", "Configure louvre size, frame type and finish at The Home Depot.", ("Shop at The Home Depot", HD.href(key="shutters", module="cta_band")), ("Shutter specifications", "shutters.html"))}"""
        write(f, page(f"{label} Installation Videos | VENETA&trade;",
                      f"Step-by-step {label.lower()} installation videos covering frame assembly, shimming, fixing, panel hanging and finishing.",
                      body, active="support"))
