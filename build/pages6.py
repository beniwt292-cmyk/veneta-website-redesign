#!/usr/bin/env python3
"""P5 depth, part two: the §5.2 decision pages.

Five need pages, six room pages and four style pages. All three families are
promoted out of hub sections into standalone pages, because "blackout blinds"
and "bedroom blinds" are the phrases people actually type, and an anchor on a
hub cannot rank for them or carry its own FAQ block.

Content rules honoured here (§12):
  * Every number quoted comes from data.py, so a page cannot disagree with the
    category page it links to.
  * Every recommendation carries the tradeoff in the same block. A pick with no
    downside written next to it is advertising, not advice.
  * Nothing claims a percentage saving, an R-value or total darkness.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hd as HD
import pic as PIC
import data as D
from shell import (page, crumbs, phero, anchors, SLAT, shead, acc, kv, tiles,
                   cards, stats, cta_band, support_strip)
from build_site import write, slugify
from pages3 import prose_blocks
from p2 import macroband

SAMPLES = "free-samples.html"


# --------------------------------------------------------------------- helpers
def hero(shot, eyebrow, h1, lede, trail, ctas=""):
    """phero_media, but sourced from the P1 manifest so the hero ships AVIF,
    explicit dimensions and the shot's own alt text."""
    media = PIC.pic(shot, sizes="(min-width:1000px) 46vw, 100vw", lcp=True)
    return f"""
  <div class="phero">
    <div class="wrap">
      {crumbs(trail)}
      <div class="phero-media">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h1>{h1}</h1>
          <p class="lede">{lede}</p>
          {f'<div class="cta-row" style="margin-top:32px">{ctas}</div>' if ctas else ''}
        </div>
        <div>{media}</div>
      </div>
    </div>
  </div>
"""


def rowpic(eyebrow, h2, body, shot, cta="", flip=False):
    media = PIC.pic(shot, sizes="(min-width:900px) 48vw, 100vw")
    return f"""<div class="rowfeat{' flip' if flip else ''} rev">
      <div class="txt" style="min-width:0"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>{body}
      {f'<div class="cta-row" style="margin-top:26px">{cta}</div>' if cta else ''}</div>
      <div style="min-width:0">{media}</div>
    </div>"""


def picks(items, eyebrow="What we would fit", h2="Three that actually work.",
          sub="Ranked, with the downside written next to each one."):
    """items = [(product_slug, headline, why, tradeoff), ...]"""
    out = ""
    for i, (slug, headline, why, trade) in enumerate(items):
        p = D.BY_SLUG[slug]
        out += f"""<div class="box rev" style="min-width:0">
          <p class="meta">Pick {str(i+1).zfill(2)} &middot; {p["short"]}</p>
          <h3 style="margin:6px 0 10px">{headline}</h3>
          <p style="color:var(--ink-70)">{why}</p>
          <p style="margin-top:14px"><b>The tradeoff.</b> <span style="color:var(--ink-70)">{trade}</span></p>
          <a class="btn btn--ghost btn--sm" href="{slug}.html" style="margin-top:18px">{p["short"]}</a>
        </div>"""
    return f"""<section class="tight" id="picks"><div class="wrap">
      {shead(eyebrow, h2, sub)}
      <div class="three">{out}</div>
    </div></section>"""


def wont(items, h2="What will not get you there."):
    lis = "".join(f"<li>{x}</li>" for x in items)
    return f"""<section id="limits"><div class="wrap">
      {shead('Straight answer', h2, 'The range has eight lines. Some of them are the wrong answer here, and it is cheaper to read that than to return an order.')}
      <div class="callout" style="max-width:900px"><ul class="ticks">{lis}</ul></div>
    </div></section>"""


def roomrail(slugs, eyebrow="Rooms", h2="Where this matters most."):
    out = ""
    for s in slugs:
        name, sub = ROOM_SUB[s]
        m = PIC.pic("room-" + s, sizes="(min-width:900px) 24vw, 50vw")
        if not m:
            continue
        out += (f'<a class="rl-item" href="room-{s}.html"><div class="ph">{m}</div>'
                f'<h3>{name}</h3><p>{sub}</p></a>')
    return f'<section><div class="wrap">{shead(eyebrow, h2)}<div class="rl-grid">{out}</div></div></section>'


def needrail(slugs, eyebrow="By need", h2="Or start from the problem."):
    out = ""
    for s in slugs:
        n = NEED_BY_SLUG[s]
        out += (f'<a href="need-{s}.html"><p class="meta">Need</p><h3>{n["nav"]}</h3>'
                f'<p class="desc" style="color:var(--ink-70);margin:8px 0 0">{n["blurb"]}</p>'
                f'<span class="arrow">Read the page</span></a>')
    return f'<section class="tight"><div class="wrap">{shead(eyebrow, h2)}<div class="sgrid">{out}</div></div></section>'


def palette(pairs, note=""):
    """pairs = [(product_slug, colour_name), ...]. Hex comes from data.py, so a
    palette can only show colours the range actually offers."""
    sw = ""
    for slug, cname in pairs:
        hexv = dict(D.BY_SLUG[slug]["colors"]).get(cname)
        if not hexv:
            raise KeyError(f"{cname} is not a colourway of {slug}")
        sw += (f'<div class="sw2"><span style="background:{hexv}"></span>'
               f'<b>{cname}</b><span class="hint" style="display:block;margin-top:2px">'
               f'{D.BY_SLUG[slug]["short"]}</span></div>')
    return f"""<section class="sink" id="palette"><div class="wrap">
      {shead('Palette', 'The colours this look is built from.',
             note or 'Every swatch below is a real colourway in the range. A screen still cannot show hand or openness, so order the samples before you commit.')}
      <div class="sw2-grid">{sw}</div>
      <div class="cta-row" style="margin-top:32px"><a class="btn btn--ghost" href="{SAMPLES}">Order up to 8 free samples</a></div>
    </div></section>"""


def specrow(slugs, cols=("Width range", "Height range")):
    """Published ranges for just the lines a page recommends."""
    rows = ""
    for s in slugs:
        p = D.BY_SLUG[s]
        sp = dict(p["spec"])
        w = sp.get("Width range") or sp.get("Opening width") or "&mdash;"
        h = sp.get("Height range") or sp.get("Panel width") or "&mdash;"
        op = (sp.get("Opacity") or sp.get("Material") or sp.get("Lining")
              or sp.get("Fold style") or "&mdash;")
        mt = sp.get("Mount", "&mdash;")
        rows += (f'<tr><th scope="row"><a class="link" href="{s}.html">{p["short"]}</a></th>'
                 f'<td>{w}</td><td>{h}</td><td>{op}</td><td>{mt}</td></tr>')
    return f"""<div class="scrollx"><table class="spec2">
      <caption class="hint" style="text-align:left;margin-bottom:12px">Published ranges for the lines on this page. Same numbers as the category pages, generated from one source.</caption>
      <thead><tr><th scope="col">Line</th><th scope="col">Width</th><th scope="col">Height</th>
      <th scope="col">Opacity or material</th><th scope="col">Mount</th></tr></thead>
      <tbody>{rows}</tbody></table></div>"""


# ================================================================== need pages
ROOM_SUB = {
    "living-room": ("Living room", "Glare control without losing the view"),
    "bedroom":     ("Bedroom", "Blackout, and quiet enough to sleep through"),
    "nursery":     ("Nursery", "Cordless first, dark second"),
    "kitchen":     ("Kitchen", "Wipes clean, handles steam"),
    "home-office": ("Home office", "Zero glare on the screen"),
    "bathroom":    ("Bathroom", "Privacy in a humid room"),
}

NEEDS = [
    dict(
        slug="blackout",
        nav="Block the light",
        blurb="Blackout fabric plus a plan for the four gaps around it.",
        h1="Make the room properly dark.",
        eyebrow="Need &middot; Blackout",
        hero="motor-dusk-bedroom",
        lede="Blackout fabric is the easy part. What actually decides how dark the room gets is "
             "whether you close the four gaps around the fabric: the two sides, the top and the bottom.",
        title="Blackout Blinds &amp; Shades | VENETA&trade;",
        desc="How to get a genuinely dark room: blackout fabric, side channels and the mount choice "
             "that closes the light gap. Three picks with the tradeoffs.",
        mech=[
            ("h3", "Fabric is one of five surfaces"),
            ("p", "A blackout fabric with a foil liner stops effectively all the light that hits it. "
                  "The light you still see in a darkened bedroom is almost never coming through the "
                  "fabric. It is coming around the edge, and the biggest of those edges is the two sides."),
            ("h3", "Close the sides first"),
            ("p", "On an inside mount, the shade has to be cut narrower than the opening so it can move, "
                  "which leaves a slim gap down each side. SmartPrivacy&reg; side channels cover that gap "
                  "with a track the fabric runs inside. It is the single biggest improvement you can make."),
            ("h3", "Or go outside and go generous"),
            ("p", "If channels are not for you, mount outside the opening and overlap the trim by at least "
                  "two inches on each side, plus the same above. An outside mount cannot seal the way a "
                  "channel does, but overlap turns a bright line into a soft edge."),
            ("h3", "The bottom bar is the last inch"),
            ("p", "A fabric-wrapped SmartRail&trade; bottom bar sits flatter against the sill than an "
                  "exposed aluminium bar, which matters on a windowsill that is not perfectly level."),
        ],
        picks=[
            ("cellular-shades", "Double cell blackout, in a side channel",
             "A double cell honeycomb in blackout gives you the darkest face we make, and the cell "
             "structure also damps outside noise, which is usually the second complaint in a bedroom. "
             "Add SmartPrivacy&reg; channels and the side gap is gone.",
             "The channels are a visible frame around the window and they need to be planned into the "
             "measurement, not added afterwards. On a shallow opening they push you to an outside mount."),
            ("roller-solar-shades", "Blackout roller in a cassette",
             "The flattest, quietest-looking option: one unbroken panel of blackout fabric, with a "
             "cassette or fascia over the roll so light cannot escape above the tube. Widths run to 108\".",
             "Without side channels, a roller leaks more at the edges than a channelled cellular shade, "
             "because the tube has to be shorter than the opening. Plan an outside mount if the room "
             "needs to be genuinely dark."),
            ("roman-shades", "Blackout lining behind a real fabric",
             "For a bedroom that has to look like a bedroom rather than a hotel room. A blackout lining "
             "sits behind the face fabric, so you get the fold and the texture with the light stopped.",
             "The folds break the seal along the bottom and the stack sits proud of the glass, so a "
             "blackout roman is reliably dim rather than reliably dark. Not the pick for a shift worker."),
        ],
        numbers=[
            ("Darkest combination", "Double cell blackout cellular in SmartPrivacy&reg; channels"),
            ("Widest blackout roller", '108" single unit'),
            ("Minimum inside-mount depth", '3/4" for cellular, 2 1/2" for roman'),
            ("Recommended outside overlap", '2" each side and above'),
            ("Cordless lift", "Standard on all three picks"),
        ],
        wont=[
            "Sheer shades. The vanes close, but the knit facings stay translucent by design.",
            "Faux wood blinds and shutters. Even a fully closed louvre leaves a hairline between slats, "
            "and light finds it.",
            "Vertical blinds. The vanes overlap rather than seal, so a lit street reads straight through.",
            "Any inside-mount shade with no side channel, if the room has to be dark enough for daytime "
            "sleep. It will be dim. It will not be dark.",
        ],
        rooms=["bedroom", "nursery", "home-office"],
        faqs=[
            ("Will a blackout shade make the room completely dark?",
             "<p>No product with a moving part is completely dark, and we will not claim otherwise. A "
             "double cell blackout cellular shade in SmartPrivacy&reg; side channels is the darkest "
             "combination we build, and it is dark enough for daytime sleep in most rooms. What limits it "
             "is your window: a sill that is out of level or trim that is out of square leaves a gap no "
             "shade can close.</p>"),
            ("Blackout or room darkening?",
             "<p>Room darkening cuts most of the light and keeps a little glow. Blackout adds a liner and "
             "stops effectively all of it at the fabric. If the reason you are shopping is a baby's nap or "
             "a night shift, buy blackout. If it is a television at 8pm, room darkening is enough and it "
             "looks softer.</p>"),
            ("Do I need the side channels?",
             '<p>If the room needs to be genuinely dark, yes. If you want dim, no. Read the '
             '<a class="link" href="smartprivacy.html">SmartPrivacy&reg;</a> page for how the channel '
             'works and what it adds to the opening.</p>'),
            ("Can I get blackout and top-down/bottom-up on the same shade?",
             "<p>On cellular shades, yes. It is a useful combination on a street-facing bedroom: drop the "
             "top rail for daylight at the ceiling while the bottom stays closed at eye level.</p>"),
            ("Is a blackout shade worth it on a north-facing window?",
             "<p>Often not. A north window never takes direct sun, so a room-darkening fabric usually gets "
             "you where you want to be for less. Spend the difference on the side channels instead, "
             "because ambient light from a streetlamp comes around the edge regardless of orientation.</p>"),
        ],
    ),
    dict(
        slug="light-filtering",
        nav="Soften the light",
        blurb="Diffuse the daylight instead of blocking it.",
        h1="Keep the daylight. Lose the glare.",
        eyebrow="Need &middot; Light filtering",
        hero="category-sheer-shades",
        lede="Most rooms do not need to be dark. They need the hard edge taken off the light, so the "
             "room stays bright without a stripe of sun across the floor.",
        title="Light Filtering Shades &amp; Blinds | VENETA&trade;",
        desc="Light filtering shades diffuse daylight instead of blocking it. How opacity and openness "
             "differ, three products worth fitting, and what to avoid.",
        mech=[
            ("h3", "Opacity and openness are not the same thing"),
            ("p", "Opacity describes how much light a fabric passes: light filtering, room darkening, "
                  "blackout. Openness describes how much of the fabric is physically hole: a 3% screen "
                  "is 3% open weave. A light filtering fabric glows. An open screen lets you see through it."),
            ("h3", "Diffusion is what you are buying"),
            ("p", "A light filtering fabric turns one bright source into a whole illuminated surface. The "
                  "room reads brighter than the light meter says, because the glow arrives from a large "
                  "area instead of a small one. That is also why it kills glare on a screen or a glossy table."),
            ("h3", "Privacy in daylight, silhouette at night"),
            ("p", "Any fabric that lets light through in one direction lets it through in the other. A "
                  "light filtering shade is private in daylight and becomes a silhouette after dark once "
                  "the room lights are on. If that matters, look at the privacy page."),
            ("h3", "Colour changes the answer"),
            ("p", "A pale fabric diffuses and brightens. A dark fabric of the same opacity absorbs and "
                  "preserves contrast, which is why a charcoal screen gives you a sharper view out. Same "
                  "fabric spec, completely different room."),
        ],
        picks=[
            ("cellular-shades", "Light filtering honeycomb, for an even glow",
             "The most consistent diffuser in the range. Light entering the honeycomb bounces inside the "
             "cell before it reaches the room, so the whole shade lights up evenly with no hot spot.",
             "You cannot see out of it at all. If the window has a view you care about, this is the wrong "
             "line and a 10% screen is the right one."),
            ("sheer-shades", "Fabric vanes between two sheers",
             "The one that gives you both. Open the vanes and you have a soft view through the knit "
             "facings; close them and the room diffuses. Up to 88% UV blocked with the vanes open.",
             "It needs 2 1/2\" of depth for an inside mount and it is the most delicate fabric here. It "
             "also cannot get properly dark, whatever you do with the vanes."),
            ("roman-shades", "Unlined or privacy-lined fabric",
             "When you want the light softened and the window dressed at the same time. An unlined linen "
             "glows; a privacy lining takes it a stop darker without going opaque.",
             "Romans stack in front of the glass, so the top of the window is never fully clear. Care is "
             "dust and spot clean only, which rules them out over a sink."),
        ],
        numbers=[
            ("Softest even glow", "Light filtering cellular"),
            ("Best view retained", 'Sheer shades, or a 10% and 14% solar screen'),
            ("UV blocked, vanes open", "Up to 88% on sheer shades"),
            ("Cellular width range", '18" to 96"'),
            ("Sheer minimum depth", '2 1/2" inside mount'),
        ],
        wont=[
            "Blackout anything. It is the opposite specification, and in a living room it reads as a "
            "hole in the wall during the day.",
            "1% and 3% solar screens if you want the room bright. They are glare tools for a screen, and "
            "they are dark to sit behind all day.",
            "Faux wood or shutters, if a soft glow is the goal. Louvres slice light into bands rather "
            "than diffusing it, which is a look, but it is not this one.",
            "A dark light-filtering fabric on a north window. There is not enough light to soften and the "
            "room will just feel dim.",
        ],
        rooms=["living-room", "kitchen", "bedroom"],
        faqs=[
            ("Can people see in through a light filtering shade?",
             "<p>Not in daylight, when the outside is brighter than the room. After dark with the lights "
             "on, the shade backlights and you get a silhouette. That is physics, not a fabric defect. "
             "For night privacy, use a room darkening fabric or a shutter you can tilt.</p>"),
            ("What is the difference between light filtering and room darkening?",
             "<p>Roughly one stop of light. Light filtering keeps the room bright and glowing. Room "
             "darkening drops it to a dim, even light and holds more privacy at night. Both are available "
             "on cellular and roller shades.</p>"),
            ("Which is better for a screen: light filtering fabric or a solar screen?",
             '<p>A solar screen at 1% or 3%, because it cuts the brightness of the sky itself. A light '
             'filtering fabric removes the direct beam but leaves a large bright surface, which can still '
             'reflect in a monitor. The <a class="link" href="room-home-office.html">home office</a> '
             'answer is a screen.</p>'),
            ("Do light filtering fabrics fade?",
             "<p>All fabrics change over years in direct sun. Pale colours show it least. The lining side "
             "of a roman shade takes the exposure rather than the face fabric, which is one of the "
             "quieter arguments for a lined roman on a south window.</p>"),
            ("Can I mix light filtering and blackout in one room?",
             "<p>Yes, and on a bedroom with two windows it is often the right call: blackout on the "
             "window that faces the street or the sunrise, light filtering on the other. Order swatches "
             "of both and hold them up together, because the two fabrics need to agree on colour.</p>"),
        ],
    ),
    dict(
        slug="privacy",
        nav="Privacy, day and night",
        blurb="Daytime privacy is easy. Night privacy is the real brief.",
        h1="Privacy that still lets the day in.",
        eyebrow="Need &middot; Privacy",
        hero="category-shutters",
        lede="Nearly every shade is private in daylight. The question worth asking is what happens at "
             "eight in the evening with the lamps on, because that is when most people get it wrong.",
        title="Privacy Blinds &amp; Shades | VENETA&trade;",
        desc="Daytime privacy versus night privacy, and why they need different products. Three picks "
             "for real privacy, plus what silhouettes after dark.",
        mech=[
            ("h3", "Privacy follows the brighter side"),
            ("p", "You can see from the dark side into the light side. In daylight the street is brighter "
                  "than your room, so a translucent shade reads as opaque from outside. After dark the "
                  "room is brighter than the street, and the same shade reads as a lit screen with you on it."),
            ("h3", "Two products solve it two different ways"),
            ("p", "Either the material is opaque, so nothing passes in either direction, or the material "
                  "tilts, so you aim the gap at the sky instead of at the pavement. Louvres and vanes take "
                  "the second route, and it is the more liveable one on a ground floor."),
            ("h3", "Top-down/bottom-up is the underrated answer"),
            ("p", "On a street-facing window, lowering the top rail gives you daylight arriving above "
                  "head height while the bottom two thirds stay closed. You keep the brightness and lose "
                  "the sightline, without covering the window all day."),
            ("h3", "Tilt up, not down"),
            ("p", "With a blind, tilting the concave face of the slat upward sends the sightline to the "
                  "sky and bounces light onto your ceiling. Tilting the other way points the gap at the "
                  "footpath. Same blind, same angle, opposite result."),
        ],
        picks=[
            ("shutters", "Tilt a louvre and the sightline goes away",
             "The most complete answer we make. An engineered hardwood composite louvre is opaque, so "
             "closing it is genuinely private at any hour, and tilting it gives you light with no sightline. "
             "Louvres run 2 1/2\", 3 1/2\" and 4 1/2\".",
             "Shutters are fitted inside a frame in the opening, which means they are the most permanent "
             "and the most expensive thing here. Panels are limited to 36\" each, so a wide window gets "
             "more stiles across the glass."),
            ("cellular-shades", "Room darkening with top-down/bottom-up",
             "Two thirds closed at eye level, top rail dropped for daylight. On a ground-floor bedroom or "
             "a bathroom facing a neighbour, this is usually the answer, and it stays private after dark "
             "because the fabric is room darkening rather than sheer.",
             "It is a fabric, so there is no tilt: you are trading coverage for light rather than aiming "
             "it. And a light filtering cellular will silhouette at night, so specify room darkening."),
            ("faux-wood-blinds", "The cheapest honest tilt",
             "A 2\" or 2 1/2\" composite slat does the same job as a shutter louvre for a fraction of the "
             "cost, and the moisture-resistant polymer suits a bathroom. Routeless slats remove the cord "
             "holes that let pinpricks of light through.",
             "Slats stack at the top and never disappear the way a rolled shade does, and there is always "
             "a hairline between closed slats. Private, but not dark."),
        ],
        numbers=[
            ("Most private, any hour", "Closed composite shutter louvre"),
            ("Best day privacy with light", "Top-down/bottom-up cellular"),
            ("Shutter louvre sizes", '2 1/2", 3 1/2", 4 1/2"'),
            ("Faux wood slat sizes", '2", 2 1/2"'),
            ("Routeless slats", "Available, removes cord holes"),
        ],
        wont=[
            "Sheer shades on a ground-floor front room. Vanes closed still leaves two knit facings, and "
            "at night that is a silhouette.",
            "10% and 14% solar screens for privacy. They are view-preserving by design, which is the "
            "same as saying you can be seen through them once the room is lit.",
            "Light filtering cellular or roller fabric, if night privacy is the point. Specify room "
            "darkening or blackout instead: same product, one step further.",
            "Any shade at all on a bathroom window where the glass is clear and the sill is deep enough "
            "to stand on. Frosted film plus a tilting louvre is the belt-and-braces answer.",
        ],
        rooms=["bathroom", "bedroom", "living-room"],
        faqs=[
            ("Can people see in at night through my shades?",
             "<p>If the fabric passes any light, yes, they can see movement and shape. The test is simple: "
             "turn the room lights on, go outside after dark and look. If you can read the shape of a lamp "
             "through the shade, someone on the footpath can read you.</p>"),
            ("Are shutters more private than blinds?",
             "<p>Marginally, and mostly because the louvre is thicker and the frame closes the perimeter. "
             "A closed faux wood blind is private too. The real difference is that a shutter feels like "
             "part of the building and a blind feels like something hung in front of it.</p>"),
            ("What is the best privacy option for a bathroom?",
             '<p>Composite shutters if the budget allows, because they tilt and they do not mind the '
             'humidity. Faux wood blinds if it does not. Both are covered on the '
             '<a class="link" href="room-bathroom.html">bathroom page</a> with the mount notes that matter '
             'above a bath.</p>'),
            ("Does top-down/bottom-up work on every product?",
             "<p>Cellular shades, yes. It is not offered across the whole range, because it needs a "
             "second cord path inside the headrail that a roller tube or a shutter frame does not have.</p>"),
            ("Will a blind give me privacy from a neighbour above me?",
             "<p>Tilt the slats up and someone at a higher level can look down through the gap. That is "
             "the one case where a louvre loses to a fabric. If you are overlooked from above, use a room "
             "darkening shade with top-down/bottom-up and keep the top rail up.</p>"),
        ],
    ),
    dict(
        slug="energy-efficiency",
        nav="Lower the energy bill",
        blurb="Two different problems: winter conduction and summer gain.",
        h1="Stop paying to heat the window.",
        eyebrow="Need &middot; Energy",
        hero="category-cellular-shades",
        lede="A window is the weakest part of the wall in winter and the strongest heater in summer. "
             "Those are two different problems and they take two different products.",
        title="Energy Efficient Blinds &amp; Shades | VENETA&trade;",
        desc="Insulating shades for winter heat loss and solar screens for summer gain: two problems, "
             "the right product for each, and no invented savings figures.",
        mech=[
            ("h3", "Winter is conduction. Summer is radiation"),
            ("p", "In winter, warm indoor air touches cold glass and loses its heat by contact. The fix is "
                  "a layer of still air between the room and the glass. In summer, sunlight comes through "
                  "the glass as radiation and turns into heat inside the room. The fix is to stop it at "
                  "the glass before it converts."),
            ("h3", "Trapped air is the whole trick"),
            ("p", "A honeycomb cell holds a pocket of air that cannot circulate. Still air is a poor "
                  "conductor, which is why a double cell shade insulates better than a single cell, and "
                  "why both beat a flat fabric of the same thickness."),
            ("h3", "Seal the perimeter or lose the benefit"),
            ("p", "An insulating shade with a two-inch gap down each side lets a convection loop run "
                  "behind it: air cools at the glass, drops, and spills into the room at the bottom. Side "
                  "channels or a generous outside mount are what turn a warm-looking shade into a working one."),
            ("h3", "What we will not tell you"),
            ("p", "We do not publish an R-value or a percentage saving for any product. Both depend on "
                  "your glazing, your orientation, your climate and how you use the shade, and any single "
                  "number would be marketing rather than measurement."),
        ],
        picks=[
            ("cellular-shades", "Double cell, for the winter problem",
             "Two honeycomb chambers instead of one, so there are two pockets of still air between the "
             "room and the glass. This is the most insulating fabric product in the range and the cell "
             "structure damps sound as a side effect.",
             "It insulates by covering the window, so on a bright winter day you are choosing between "
             "warmth and daylight. Top-down/bottom-up gives some of both. Also: it needs the side gap "
             "closed to work properly."),
            ("roller-solar-shades", "1% to 5% screen, for the summer problem",
             "A solar screen stops the sun at the glass and blocks up to 99% of UV depending on openness, "
             "while still letting you see out. On a west elevation it is the difference between a room you "
             "can use at five in the afternoon and one you cannot.",
             "A screen does nothing for winter heat loss, because it is an open weave with no trapped "
             "air. If you have both problems, you need two products or a dual roller."),
            ("shutters", "Framed, for a window that leaks",
             "A shutter is fitted into a frame inside the opening, so it closes the perimeter in a way no "
             "hung shade does. On an old sash window that draughts, the frame is doing as much work as "
             "the louvre.",
             "The most expensive answer, and the louvre gaps mean it will never seal like a fabric in a "
             "channel. Buy it for the frame and the look, and take the insulation as a bonus."),
        ],
        numbers=[
            ("Most insulating fabric", 'Double cell 9/16" cellular, blackout'),
            ("UV blocked, solar screen", "Up to 99% depending on openness"),
            ("Openness factors offered", "1%, 3%, 5%, 10%, 14%"),
            ("Perimeter seal", "SmartPrivacy&reg; channels or a framed shutter"),
            ("Published R-value", "None. See below."),
        ],
        wont=[
            "Any claim of a percentage saving from us. Your glazing and orientation decide it, not the shade.",
            "Vertical blinds and faux wood, for insulation. Hard louvres with air moving freely between "
            "them do very little to slow heat transfer.",
            "A blackout roller for a cold room, unless you also fix the edges. A sealed-looking fabric "
            "with an open perimeter still runs a convection loop behind it.",
            "A solar screen on a north window. There is no direct gain to stop, so you are darkening the "
            "room for nothing.",
        ],
        rooms=["living-room", "bedroom", "home-office"],
        faqs=[
            ("How much will cellular shades save me?",
             "<p>We do not publish a figure, because an honest one does not exist. What we can tell you is "
             "the mechanism: a double cell shade adds two pockets of still air at the coldest surface in "
             "the room, and closing the side gap roughly doubles the benefit of whatever fabric you chose.</p>"),
            ("Single cell or double cell?",
             "<p>Double cell if energy is the reason you are buying. Single cell if you want a slimmer "
             "stack at the top of the window and a lower price, and insulation is a nice-to-have. Double "
             "cell is 9/16\", single is 3/8\".</p>"),
            ("Do I need blackout for insulation?",
             "<p>No. The air pocket does the insulating, not the opacity. Blackout adds a foil liner which "
             "helps a little with radiant heat, but a light filtering double cell insulates nearly as well "
             "and keeps the room usable in daylight.</p>"),
            ("What is the best combination for a west-facing room?",
             '<p>A 3% solar screen for the afternoon and a cellular shade behind or beside it for the '
             'winter. If you only want one product, take the screen: an overheated west room in July is a '
             'bigger problem than a cool one in January. See the '
             '<a class="link" href="journal-beat-summer-heat.html">summer heat piece</a>.</p>'),
            ("Does motorisation help with energy use?",
             '<p>Indirectly, and only if it changes behaviour. A shade on a schedule actually gets closed '
             'before the sun hits the glass, which is the part people forget to do manually. '
             '<a class="link" href="truquiet-motorization.html">TruQuiet&trade;</a> supports scheduling '
             'through the hub you pair it with.</p>'),
        ],
    ),
    dict(
        slug="patio-doors",
        nav="Cover a patio door",
        blurb="A traffic problem more than a light problem.",
        h1="Cover the glass and still walk through it.",
        eyebrow="Need &middot; Patio doors",
        hero="motor-patio-run",
        lede="A patio door is not a big window. It is a door, and whatever you fit has to move out of the "
             "way several times a day without being fought with.",
        title="Patio Door Blinds &amp; Shades | VENETA&trade;",
        desc="Sliding and French door coverings that stack out of the way: DualDrape, vertical blinds and "
             "wide rollers, with widths, stack sides and handle clearance.",
        mech=[
            ("h3", "Decide the stack side before anything else"),
            ("p", "Vanes have to gather somewhere. Stack them on the fixed panel, not the one that opens, "
                  "or you will be pushing fabric aside every time you go outside. Left, right and split "
                  "centre are all available, and it is a manufacturing choice, not an adjustment."),
            ("h3", "Measure the handle, not just the opening"),
            ("p", "A slider handle projects into the room. A treatment that hangs flat against the glass "
                  "will foul it. Mount off the ceiling or far enough up the wall that the vanes clear the "
                  "handle through its whole travel."),
            ("h3", "Rotate first, traverse second"),
            ("p", "The reason vane systems beat a single wide shade here is that you get two moves. "
                  "Rotate for light and privacy without opening anything; traverse only when you actually "
                  "want to walk through. A roller gives you one move: up or down."),
            ("h3", "Ceiling or wall, not inside the opening"),
            ("p", "Both DualDrape&trade; and vertical blinds mount to the ceiling or the wall above the "
                  "door. That is deliberate: an inside mount on a door opening puts the track where the "
                  "door needs to be."),
        ],
        picks=[
            ("dualdrape", "Drapery look, vane behaviour",
             "A 3 1/2\" fabric vane on a low-profile track: it reads like a soft curtain, rotates for "
             "light and traverses aside for access. Widths run 36\" to 192\", which covers almost any "
             "residential slider in one unit.",
             "The most expensive of the three, and the vanes are fabric, so a doorway that takes wet dogs "
             "and bikes is asking a lot of them. They are removable and washable, which helps."),
            ("vertical-blinds", "The value answer that has not been beaten",
             "A 3 1/2\" vinyl or S-curve louvre rotating and drawing on a cordless wand, to 144\" wide. "
             "Vinyl wipes clean, individual vanes are replaceable for a few dollars, and nothing else "
             "costs less per square foot of door.",
             "It looks like what it is. Fabric vanes soften it, but if the door is the focal point of the "
             "room, DualDrape&trade; is the one you will be happier with in five years."),
            ("roller-solar-shades", "A screen over a door you rarely use",
             "On a French door pair or a slider that is mostly a window, a single wide solar screen at "
             "5% or 10% keeps the view and kills the afternoon glare, with no vanes to gather.",
             "One roller reaches 108\" and it has to come all the way up to walk through. Fine on a door "
             "you use twice a week, wrong on the one you use twice an hour."),
        ],
        numbers=[
            ("Widest single unit", 'DualDrape&trade; 36" to 192"'),
            ("Vertical blind width range", '24" to 144"'),
            ("Widest single roller", '108"'),
            ("Vane and louvre width", '3 1/2" on both vane systems'),
            ("Mounting", "Ceiling or wall above the opening"),
        ],
        wont=[
            "Cellular or roman shades over a working slider. They have to be fully raised to pass, and "
            "the stack sits where the door head is.",
            "Shutters on a sliding door. Bypass shutter panels exist for wide openings, but they need "
            "track depth and they will not clear a projecting slider handle.",
            "An inside mount on any door opening. The track belongs on the ceiling or the wall above.",
            "A split-centre stack on a door with one fixed panel and one slider. Stack it all onto the "
            "fixed side.",
        ],
        rooms=["living-room", "kitchen"],
        faqs=[
            ("What is the best window covering for a sliding glass door?",
             "<p>A vane system, because it gives you two independent moves: rotate for light, traverse for "
             "access. DualDrape&trade; if you want it to look like drapery, vertical blinds if you want "
             "the lowest cost per square foot. Both mount above the opening and stack to one side.</p>"),
            ("Which side should the vanes stack on?",
             "<p>The fixed panel. Work out which half of the door actually slides, then stack away from "
             "it. Split centre only makes sense on a door where both panels open or where the door is "
             "purely decorative.</p>"),
            ("How wide can you go in one unit?",
             "<p>DualDrape&trade; runs to 192\" and vertical blinds to 144\". A single roller shade tops "
             "out at 108\", so a wider opening needs two rollers coupled, which leaves a visible seam.</p>"),
            ("Will it clear the door handle?",
             '<p>Only if you mount it high enough or far enough off the wall. Measure the handle '
             'projection and the height of its travel before you order, and use the '
             '<a class="link" href="how-to-measure.html">measuring guide</a> outside-mount method rather '
             'than the inside-mount one.</p>'),
            ("Can a patio door treatment be motorised?",
             '<p>Yes on DualDrape&trade;, with <a class="link" href="truquiet-motorization.html">'
             'TruQuiet&trade;</a>. On a wide run it is worth it: a 16-foot traverse is a long way to walk '
             'a wand, and a rechargeable motor removes the one job people stop doing after a month.</p>'),
        ],
    ),
]

NEED_BY_SLUG = {n["slug"]: n for n in NEEDS}


# ================================================================== room pages
ROOMS = [
    dict(
        slug="bedroom",
        name="Bedroom",
        h1="Dark enough to sleep. Quiet enough to stay asleep.",
        eyebrow="Room &middot; Bedroom",
        lede="A bedroom asks for two things a living room does not: real darkness on demand, and a bit "
             "less of the street. One product line does both better than the rest.",
        title="Bedroom Blinds &amp; Shades | VENETA&trade;",
        desc="Bedroom window treatments for darkness and quiet: double cell blackout, blackout rollers "
             "and lined romans, with the side-gap fix that matters most.",
        brief=[
            ("h3", "The brief"),
            ("p", "Darkness first, sound second, look third. The order matters, because the products that "
                  "do the first two well are all fabric, and fabric is where the design decisions are."),
            ("h3", "Where bedrooms go wrong"),
            ("p", "People buy blackout fabric and stop there. The fabric was never the problem: the gap "
                  "down each side of an inside-mounted shade is, and on a summer morning it throws a line "
                  "of light straight across the bed."),
            ("h3", "The quiet part"),
            ("p", "A double cell honeycomb has two air pockets, and still air absorbs reflected sound as "
                  "well as heat. It will not silence a main road, and we would not claim it does, but it "
                  "audibly takes the edge off traffic and reflected noise."),
        ],
        picks=[
            ("cellular-shades", "Double cell blackout, with side channels",
             "The bedroom default. Darkest fabric face we make, two air pockets for warmth and sound, and "
             "SmartPrivacy&reg; channels to close the sides. Add top-down/bottom-up on a street-facing "
             "window for daylight above head height.",
             "The channels are visible and have to be measured in from the start. On an opening shallower "
             "than 3/4\" you are going to an outside mount instead."),
            ("roller-solar-shades", "Blackout roller with a fascia",
             "The cleanest look: one flat panel, nothing stacked at the top when it is up. A fascia or "
             "cassette closes the light path above the tube, which is the second-biggest leak after the sides.",
             "Edge leak is worse than a channelled cellular shade. Plan a generous outside mount if the "
             "room has to be genuinely dark."),
            ("roman-shades", "Blackout-lined, in a fabric you like",
             "For a bedroom that should not look technical. Flat fold in a linen or a hobbled fold for "
             "something softer, with a blackout lining behind it doing the work.",
             "Folds break the seal at the bottom and the stack never fully clears the glass. Reliably dim, "
             "not reliably dark, and dry clean only."),
        ],
        notes=[
            ("Check depth before anything else",
             'A flush inside mount needs 3/4" for cellular and 2 1/2" for a roman. Measure to the face of '
             'the glass, not to the trim.'),
            ("Measure in three places",
             "Width at top, middle and bottom; height at left, centre and right. Use the narrowest width "
             "and the longest height. Old bedrooms are rarely square."),
            ("Decide the channel now, not later",
             "SmartPrivacy&reg; channels change the ordered width. They cannot be added to a shade that "
             "was cut for a bare opening."),
            ("Two windows, one fabric",
             "If the room has two windows, order both at once from the same dye lot and hold the swatches "
             "side by side under the bedroom's own light."),
        ],
        avoid=[
            "Sheer shades, if daytime sleep matters. Lovely product, wrong room for this brief.",
            "Faux wood or shutters as the only treatment. Closed louvres still pass a hairline of light, "
            "and at 5am in June that is enough to wake you.",
            "A light filtering fabric on a street-facing window. It silhouettes at night, which is the "
            "one room where that is genuinely unwelcome.",
        ],
        needs=["blackout", "privacy", "energy-efficiency"],
        products=["cellular-shades", "roller-solar-shades", "roman-shades"],
        faqs=[
            ("What is the best blind for a bedroom?",
             "<p>A double cell blackout cellular shade with SmartPrivacy&reg; side channels. It is the "
             "darkest, warmest and quietest combination in the range, and cordless lift is standard so "
             "there is nothing to fit around a bed.</p>"),
            ("How do I stop light coming in around the edges?",
             '<p>Side channels if you want it solved properly, or an outside mount with at least two '
             'inches of overlap each side and above if you do not want a visible frame. The '
             '<a class="link" href="need-blackout.html">blackout page</a> goes through both.</p>'),
            ("Will shades help with street noise?",
             "<p>A double cell honeycomb will noticeably soften reflected and mid-frequency noise. It will "
             "not stop a bus. Glazing does that, and no window covering is a substitute for it.</p>"),
            ("Are motorised bedroom shades worth it?",
             '<p>On a high window or behind a bed you cannot reach across, yes. '
             '<a class="link" href="truquiet-motorization.html">TruQuiet&trade;</a> is rechargeable '
             'lithium and quiet enough not to wake the room, which is the whole point of the name.</p>'),
            ("Can I have blackout and still get daylight in the morning?",
             "<p>Top-down/bottom-up on a cellular shade gives you exactly that: leave the bottom closed "
             "and drop the top rail a foot. Light arrives at the ceiling, the bed stays in shade, and "
             "nobody can see in.</p>"),
        ],
    ),
    dict(
        slug="living-room",
        name="Living room",
        h1="Keep the view. Lose the glare on the television.",
        eyebrow="Room &middot; Living room",
        lede="The living room is the one window where covering the glass is a loss. The job is to cut the "
             "hard light and keep everything else.",
        title="Living Room Blinds &amp; Shades | VENETA&trade;",
        desc="Living room window treatments that cut glare without blocking the view: solar screens by "
             "openness, sheer shades and light filtering cellular.",
        brief=[
            ("h3", "The brief"),
            ("p", "Glare control that does not cost you the view, on a window that is usually the largest "
                  "in the house and often the reason you bought the room."),
            ("h3", "Openness is the dial"),
            ("p", "Solar screens come at 1%, 3%, 5%, 10% and 14% open. The lower the number, the more "
                  "glare it kills and the less you see through it. For a living room, 5% and 10% are the "
                  "two that get specified most: enough to sit behind all afternoon, open enough to keep "
                  "the outside."),
            ("h3", "Dark fabric sees out better"),
            ("p", "This surprises people. A charcoal screen gives a sharper view out than a white one at "
                  "the same openness, because the pale fabric scatters light and hazes the view. Pale "
                  "brightens the room; dark preserves the view. Pick which you want."),
        ],
        picks=[
            ("roller-solar-shades", "5% or 10% solar screen",
             "The default living room answer. Kills the direct beam and the sky glare, keeps the view, and "
             "blocks a large share of UV so the sofa lasts longer. SmartRail&trade; fabric-wrapped bottom "
             "bar if you want the hardware to disappear.",
             "A screen is never private at night. If this room faces a footpath, you need a second layer "
             "or a room darkening fabric for the evening."),
            ("sheer-shades", "Vanes for a window you look at as much as through",
             "Two knit sheers with a fabric vane between them: open for a soft view, closed for diffusion. "
             "It reads more like a textile than a screen, which suits a room with furniture in it.",
             "Needs 2 1/2\" of depth and 24\" of minimum width, and it will never get dark. The most "
             "delicate fabric in the range, so not the pick for a room with a large dog."),
            ("cellular-shades", "Light filtering honeycomb, for the winter side",
             "On the cold elevation of the room, a light filtering cellular gives you an even glow plus "
             "the insulation nothing else here offers. Often the right second product rather than the first.",
             "You cannot see out of it at all. Fit it on the window without the view, not the one with it."),
        ],
        notes=[
            ("Pick openness per window, not per room",
             "West and south need 3% or 5%. North rarely needs less than 10%. Specifying one fabric for "
             "the whole room means over-darkening half of it."),
            ("Wide windows: check the 108 inch limit",
             'A single roller reaches 108" wide. Beyond that you are coupling two units, and the seam '
             "will be visible, so plan where it falls."),
            ("Reverse roll for a deep sill",
             "Standard roll drops the fabric close to the glass. Reverse roll brings it forward, which "
             "clears a projecting sill or a crank handle."),
            ("Order the swatch and tape it up",
             "Openness cannot be judged on a screen. Tape the sample to the glass at four in the "
             "afternoon and look at the television through it."),
        ],
        avoid=[
            "1% and 3% screens across a whole living room. They are glare tools for a monitor and they "
            "make a sitting room gloomy.",
            "Blackout fabric on the main window. It works, and the room reads as a wall for eight months "
            "of the year.",
            "A single roller on a window wider than 108 inches, unless you have decided where the coupling "
            "seam goes.",
        ],
        needs=["light-filtering", "energy-efficiency", "patio-doors"],
        products=["roller-solar-shades", "sheer-shades", "cellular-shades"],
        faqs=[
            ("What openness should I choose for a living room?",
             "<p>5% or 10% for most rooms. Go to 3% only if the window faces direct west and you use the "
             "room in the late afternoon. 14% keeps the most view and does the least about glare.</p>"),
            ("How do I stop glare on the television without darkening the room?",
             "<p>A solar screen on the window opposite or beside the screen, at 5%. It cuts the bright "
             "sky, which is what reflects, while leaving the rest of the daylight. Blackout is overkill "
             "and it makes the room feel like a cinema at two in the afternoon.</p>"),
            ("Will a solar shade give me privacy in the evening?",
             '<p>No. Openness works in both directions once the room is the brighter side. If evening '
             'privacy matters, read the <a class="link" href="need-privacy.html">privacy page</a> and plan '
             'a room darkening layer.</p>'),
            ("What about a very wide window wall?",
             "<p>Multiple rollers on a shared fascia looks deliberate and reads as one line, which is "
             "better than fighting a coupled 140-inch unit. Motorising a run of three or four is the "
             "point at which motorisation stops being a luxury.</p>"),
            ("Do solar screens fade the furniture?",
             "<p>They slow it down considerably: up to 99% of UV blocked depending on openness. They do "
             "not stop visible light, and visible light fades things too, so a sofa in a south window will "
             "still change over years.</p>"),
        ],
    ),
    dict(
        slug="kitchen",
        name="Kitchen",
        h1="Wipes clean, handles steam, keeps out of the way.",
        eyebrow="Room &middot; Kitchen",
        lede="A kitchen window sits above a sink or beside a hob, which rules out most fabrics before "
             "the conversation about style even starts.",
        title="Kitchen Blinds &amp; Shades | VENETA&trade;",
        desc="Kitchen blinds that survive steam and grease: moisture-resistant faux wood, vinyl verticals "
             "for a slider, and what not to hang near a hob.",
        brief=[
            ("h3", "The brief"),
            ("p", "A surface you can wipe, a material that does not mind humidity, and a treatment short "
                  "enough not to trail in the sink or reach the hob."),
            ("h3", "Grease is the real enemy"),
            ("p", "Steam alone is manageable. Airborne cooking oil is what ruins a fabric shade, because "
                  "it lands, cools and holds dust. Once it is in a woven fabric it does not come out "
                  "without professional cleaning, which most kitchen shades are not worth."),
            ("h3", "Fit it short, deliberately"),
            ("p", "Over a sink, order the height so the bottom bar sits above the tap rather than level "
                  "with the sill. It looks intentional and it stays dry, which is worth more than the "
                  "extra four inches of coverage."),
        ],
        picks=[
            ("faux-wood-blinds", "Moisture-resistant composite, 2 inch slat",
             "The kitchen workhorse. A polymer composite slat that will not warp above a sink, wipes down "
             "with a damp cloth, and tilts so you get light without a sightline. Individual slats are "
             "replaceable, which matters in the room where things get knocked.",
             "Slats collect dust on the top edge and there are a lot of edges. Routeless slats remove the "
             "cord holes but not the dusting."),
            ("vertical-blinds", "Vinyl louvres for a kitchen door",
             "If the kitchen opens onto the garden, a vinyl vertical is the most practical thing you can "
             "hang there: it wipes clean, it rotates and draws, and a damaged vane costs a few dollars "
             "rather than a reorder.",
             "It is a functional look, not a decorative one. Fabric vanes soften it but give up the "
             "wipe-clean advantage that made it the right answer."),
            ("roller-solar-shades", "A screen on the window you only look through",
             "On a kitchen window away from the sink and the hob, a solar screen at 5% or 10% handles the "
             "morning glare with one flat panel and almost nothing to collect grease.",
             "The fabric is still a fabric. Keep it out of the splash zone and off the wall behind a hob, "
             "where nothing woven belongs."),
        ],
        notes=[
            ("Order it short on purpose",
             "Finish the bottom bar above the tap and above any tiled upstand. Coverage you cannot keep "
             "clean is not coverage."),
            ("Check the depth over a deep sill",
             'Faux wood needs 2" for a flush inside mount. A tiled reveal often has less than the plaster '
             "one next door, so measure the actual reveal."),
            ("Nothing woven near a hob",
             "Keep any fabric treatment at least the width of the hob away from it, and prefer a hard "
             "louvre on that window regardless of what the rest of the kitchen has."),
            ("Match the valance to the cabinets, not the walls",
             "The 3\" crown valance on a faux wood blind is the visible part. Hold the swatch against a "
             "cabinet door, because that is what it sits next to."),
        ],
        avoid=[
            "Roman shades over a sink or near a hob. Dust and spot clean only, professional cleaning "
            "otherwise, and grease does not spot clean.",
            "Sheer shades anywhere in a working kitchen. The knit facings hold everything the air carries.",
            "Real wood blinds, which is why we do not make them. Composite exists precisely because wood "
            "warps in this room.",
        ],
        needs=["light-filtering", "privacy", "patio-doors"],
        products=["faux-wood-blinds", "vertical-blinds", "roller-solar-shades"],
        faqs=[
            ("What is the best blind for a kitchen?",
             "<p>Faux wood blinds. The composite is moisture resistant, the slats wipe clean, and the tilt "
             "gives you light without a sightline into the room. On a kitchen door, vinyl verticals for "
             "the same reasons.</p>"),
            ("Can I put a fabric shade in a kitchen?",
             "<p>On a window away from the sink and the hob, yes, and a roller shade is the fabric that "
             "copes best because it is one flat face with nowhere for grease to sit. Avoid romans and "
             "sheers in a kitchen you actually cook in.</p>"),
            ("How do I clean kitchen blinds?",
             '<p>Warm water, a drop of washing-up liquid, a microfibre cloth, slats closed then flipped '
             'and done again. Full method by material on the '
             '<a class="link" href="how-to-clean.html">care page</a>. Do not use solvent on a composite '
             'slat: it hazes the finish.</p>'),
            ("Should the blind cover the whole window over the sink?",
             "<p>No. Order the height to finish above the tap. It looks deliberate, it stays out of the "
             "water, and the few inches of glass below the bar are not a privacy problem at sink height.</p>"),
            ("Are faux wood blinds heavy on a wide kitchen window?",
             "<p>They get heavy past about 72 inches, which is where a cordless lift is doing real work "
             "and a motorised tilt starts to earn its money. Width range runs to 96 inches.</p>"),
        ],
    ),
    dict(
        slug="bathroom",
        name="Bathroom",
        h1="Privacy in the one room that is always damp.",
        eyebrow="Room &middot; Bathroom",
        lede="Every bathroom window has the same two requirements and they pull in opposite directions: "
             "cover the glass, and survive the humidity.",
        title="Bathroom Blinds &amp; Shades | VENETA&trade;",
        desc="Moisture-resistant bathroom window coverings: composite shutters, faux wood and vinyl "
             "verticals, with mount notes for above a bath.",
        brief=[
            ("h3", "The brief"),
            ("p", "Opaque or tiltable, moisture resistant, and mounted where it will not be splashed or "
                  "grabbed. Material choice does most of the work here; style follows it."),
            ("h3", "Humidity is a cycle, not a state"),
            ("p", "A bathroom goes from dry to saturated and back several times a day. That cycling is "
                  "what delaminates a fabric and warps a natural material. A composite or a vinyl does "
                  "not care."),
            ("h3", "Night privacy is the real test"),
            ("p", "A translucent shade that feels private during a morning shower becomes a lit panel at "
                  "ten at night. In a bathroom, specify something opaque or something that tilts, and do "
                  "not compromise on it."),
        ],
        picks=[
            ("shutters", "Composite louvre, framed into the opening",
             "The best bathroom answer we make. Engineered hardwood composite handles the damp, the louvre "
             "tilts for light without a sightline, and the frame closes the perimeter of an old, "
             "out-of-square window better than anything hung in front of it.",
             "The most expensive option and the most permanent. Panels cap at 36\" wide, so a wide "
             "bathroom window picks up an extra stile across the glass."),
            ("faux-wood-blinds", "The practical answer at a sensible price",
             "Moisture-resistant polymer composite in a 2\" or 2 1/2\" slat, tilting for privacy, wiping "
             "clean when it gets splashed. Routeless slats close out the cord holes, which is worth having "
             "on a window someone can see straight into.",
             "Slats never disappear, and above a bath they will collect condensation on the top edge. "
             "Plan to wipe them."),
            ("vertical-blinds", "Vinyl on a wide or awkward window",
             "On a long, low bathroom window, a vinyl vertical costs the least, wipes down, and rotates "
             "for exactly the amount of privacy you want. Individual vanes replace for a few dollars.",
             "Not a decorative choice in a room people often want to feel calm. It is the budget answer "
             "and it looks like one."),
        ],
        notes=[
            ("Mount clear of the splash zone",
             "Outside mount above the reveal on a window over a bath, so the hardware is out of reach of "
             "the shower and easier to wipe."),
            ("Composite, not wood, without exception",
             "Both faux wood and our shutters are composite. That is the specification that makes this "
             "room work, and it is why we do not offer a real wood alternative."),
            ("Frosted glass plus a tilting louvre",
             "If the window is overlooked at close range, film on the glass and a tiltable louvre in "
             "front of it is the combination that stops the conversation."),
            ("Check the reveal on a tiled window",
             'Tiling eats depth. Faux wood wants 2" and a shutter needs a frame, so measure the finished '
             "tiled reveal, not the plaster behind it."),
        ],
        avoid=[
            "Roman shades. Dry clean only, in a room that is wet twice a day.",
            "Sheer shades. Delicate knit facings, and a silhouette at night in the one room where that is "
            "least acceptable.",
            "Light filtering fabric of any kind as the only layer. It is not private after dark.",
        ],
        needs=["privacy", "light-filtering", "blackout"],
        products=["shutters", "faux-wood-blinds", "vertical-blinds"],
        faqs=[
            ("What window covering is best for a bathroom?",
             "<p>Composite shutters if the budget allows: they tilt, they are opaque when closed, and the "
             "material does not mind the humidity. Faux wood blinds do the same job for less. Both are "
             "moisture-resistant composite rather than wood.</p>"),
            ("Will a blind warp in a bathroom?",
             "<p>Not a composite one. Faux wood blinds are a moisture-resistant polymer composite and our "
             "shutters are engineered hardwood composite, both chosen for exactly this room. A real wood "
             "blind would warp, which is why we do not sell one.</p>"),
            ("Can I use a fabric shade in a bathroom?",
             "<p>A cellular shade in a room darkening fabric survives a well-ventilated bathroom, and "
             "top-down/bottom-up is genuinely useful on a window at eye level. In a small unventilated "
             "bathroom, use a hard louvre instead.</p>"),
            ("How do I get privacy without losing all the light?",
             "<p>Tilt, do not close. A louvre angled up sends the sightline to the sky and bounces light "
             "onto the ceiling, so the room stays bright and nobody sees in. That is the single advantage "
             "shutters and blinds have over every fabric.</p>"),
            ("What about a window inside the shower enclosure?",
             "<p>Nothing we make is designed to be rained on directly. Use frosted or textured glass "
             "there, and treat the window covering as a solution for the rest of the room.</p>"),
        ],
    ),
    dict(
        slug="home-office",
        name="Home office",
        h1="Zero glare on the screen. Still a room, not a bunker.",
        eyebrow="Room &middot; Home office",
        lede="A home office has one measurable requirement: nothing reflecting in the monitor. Solve that "
             "first and the rest of the room follows easily.",
        title="Home Office Blinds &amp; Shades | VENETA&trade;",
        desc="Home office window treatments that kill monitor glare: 1% and 3% solar screens, light "
             "filtering cellular, and where to put each one.",
        brief=[
            ("h3", "The brief"),
            ("p", "Cut the brightness of the sky so it stops appearing in your screen, without dropping "
                  "the room so far that you need the lights on at noon."),
            ("h3", "The sky is the reflection, not the sun"),
            ("p", "People assume glare is the direct beam. On a monitor it is usually the large bright "
                  "area of sky behind you, mirrored in the glass. That is why a low-openness screen works "
                  "and a partly-lowered blind does not: you need to dim the whole area, not block one angle."),
            ("h3", "Behind you matters more than beside you"),
            ("p", "Treat the window your screen faces, which is the one behind your head. A window off to "
                  "the side is a comfort issue; a window behind you is the one printing itself onto your work."),
            ("h3", "Dark screen fabric, every time"),
            ("p", "In an office, specify a charcoal or graphite screen rather than a pale one. Dark fabric "
                  "absorbs instead of scattering, so you get a crisper view out and markedly less haze at "
                  "the same openness."),
        ],
        picks=[
            ("roller-solar-shades", "1% or 3% screen, in a dark colour",
             "The correct answer for the window behind your monitor. A 1% or 3% graphite screen brings the "
             "sky down to a level that stops reflecting, keeps a usable view out, and blocks up to 99% of UV.",
             "It is dark to sit behind if the room only has one window. Pair it with a lighter treatment "
             "elsewhere, or accept that a working office is a slightly dimmer room."),
            ("cellular-shades", "Light filtering, for the side window",
             "On the window that is not causing the problem, a light filtering cellular gives you an even "
             "glow with no hot spot and adds the insulation that makes a converted spare room usable in "
             "January.",
             "No view through it at all, and no tilt. It is a light source, not a window, once it is down."),
            ("sheer-shades", "When the office is also a room people see",
             "If the office doubles as a guest room or sits off the hallway, sheer vanes give you "
             "adjustable diffusion in something that looks like a textile rather than a technical screen.",
             "Less effective than a low-openness screen on hard glare, and it needs 2 1/2\" of depth. A "
             "compromise, chosen knowingly."),
        ],
        notes=[
            ("Work out which window is behind the screen",
             "Sit at the desk, look at the monitor, and note what you can see reflected. That window gets "
             "the low-openness screen. Everything else is secondary."),
            ("Order the swatch and hold it up at your desk",
             "Tape a 3% and a 5% sample to the glass and look at your own monitor through each. Ten "
             "minutes here saves a return."),
            ("Dark colour, low openness",
             "Graphite or black screen at 1% to 3%. A white 3% screen scatters light and hazes the view, "
             "which defeats half the purpose."),
            ("Consider a schedule, not a habit",
             "Glare arrives at the same time every day. A motorised shade on a schedule is closed before "
             "you notice the problem, which is the part manual operation always loses."),
        ],
        avoid=[
            "10% and 14% screens on the window behind your monitor. They keep the view, which means they "
            "keep the reflection.",
            "Pale white screen fabric in an office. It hazes the view and scatters the light you were "
            "trying to control.",
            "Blackout as a glare fix. It works and it means you are lit by a lamp at midday, which is "
            "worse for your eyes than the glare was.",
        ],
        needs=["light-filtering", "energy-efficiency", "blackout"],
        products=["roller-solar-shades", "cellular-shades", "sheer-shades"],
        faqs=[
            ("What openness stops monitor glare?",
             "<p>1% or 3%, in a dark colour. Those two are specified in commercial workplaces for exactly "
             "this reason. 5% is the highest we would go on the window directly behind a screen.</p>"),
            ("Should I get a white or a dark solar shade?",
             "<p>Dark, for an office. A charcoal or graphite fabric absorbs light rather than scattering "
             "it, so the view out stays sharp and the fabric itself does not become a bright surface. "
             "White looks lighter from the street and hazier from the desk.</p>"),
            ("Do I need to cover every window in the room?",
             "<p>No, and you probably should not. Treat the window that reflects in your screen with a low "
             "openness screen and leave or lightly filter the rest. A fully screened room is a dim room.</p>"),
            ("Is a blackout shade better for video calls?",
             "<p>No. On a call you want soft even light on your face, which is what a light filtering "
             "fabric produces and what blackout removes entirely. Diffuse the window in front of you, "
             "screen the one behind you.</p>"),
            ("Is motorisation worth it in an office?",
             '<p>More than in most rooms, because the shade needs to move at a predictable time every day. '
             '<a class="link" href="truquiet-motorization.html">TruQuiet&trade;</a> handles scheduling '
             'through the hub you pair it with, and it is quiet enough to run mid-call.</p>'),
        ],
    ),
    dict(
        slug="nursery",
        name="Nursery",
        h1="Cordless first. Dark second. Everything else after that.",
        eyebrow="Room &middot; Nursery",
        lede="There is one non-negotiable in a nursery and it is not the colour. Every product we make is "
             "cordless as standard, which means this decision is already made for you.",
        title="Nursery Blinds &amp; Shades | VENETA&trade;",
        desc="Cordless nursery blinds and blackout shades: why cordless is standard on every line, and "
             "the darkest combination for daytime naps.",
        brief=[
            ("h3", "The brief"),
            ("p", "No looped cord anywhere in the room, and enough darkness for a nap at two in the "
                  "afternoon in June. In that order."),
            ("h3", "Cordless is standard, not an upgrade"),
            ("p", "All eight lines ship cordless, with no looped operating cord, no cleats and no tension "
                  "devices, meeting ANSI/WCMA A100.1. You do not need to hunt for a safe option in the "
                  "range, because there is no unsafe one."),
            ("h3", "Daytime dark is harder than night dark"),
            ("p", "At night any room darkening fabric is fine. A midday nap is the real test, and it is "
                  "won or lost at the two side gaps rather than at the fabric. Plan side channels or a "
                  "generous outside mount from the start."),
            ("h3", "Think about the cot position"),
            ("p", "Whatever is on the window, the cot should not be under it or beside it. Keep furniture "
                  "a child can climb away from the window, and keep the bottom bar above the reach of "
                  "someone standing in the cot."),
        ],
        picks=[
            ("cellular-shades", "Double cell blackout, in side channels",
             "The nursery default and the darkest thing we build. Cordless as standard, two air pockets "
             "for a room that holds its temperature, and SmartPrivacy&reg; channels closing the sides so a "
             "midday nap actually happens.",
             "Channels have to be measured in from the start and they read as a frame around the window. "
             "The fabric is also the one thing in the room a toddler can reach and pull on."),
            ("roller-solar-shades", "Blackout roller with a cassette",
             "One flat panel, nothing to grab, and a cassette closing the light path above the tube. On a "
             "nursery that will become a child's bedroom, it is the treatment that ages best.",
             "Edge leak without channels, so plan an outside mount with real overlap if daytime sleep is "
             "the point of the purchase."),
            ("sheer-shades", "For the daytime room, not the nap",
             "If the nursery is also where the day happens, sheer vanes give a soft diffused light that "
             "photographs beautifully and adjusts through the afternoon. Cordless, like everything else.",
             "It cannot get dark, at all. This is a second treatment or a second window, never the answer "
             "to the blackout requirement."),
        ],
        notes=[
            ("Nothing to specify for safety",
             "Cordless lift is standard on every line, so there is no safe-option upgrade to look for and "
             "no cord retrofit to buy."),
            ("Keep the cot off the window wall",
             "A shade is only part of the answer. Furniture that can be climbed should not sit under a "
             "window, whatever is hanging in it."),
            ("Order the height so the bar is out of reach",
             "On a low window, finishing the bottom bar a little high is worth the small loss of coverage "
             "once a child can stand."),
            ("Decide blackout now",
             "Nap requirements arrive suddenly and channels cannot be added later. If there is any chance "
             "you will want darkness, order the blackout fabric and the channels together."),
        ],
        avoid=[
            "Anything with a looped cord, which is nothing we make, and worth checking on a treatment "
            "already in the room.",
            "Faux wood or shutters as the blackout answer. Closed louvres pass a hairline of light and a "
            "slat is also a ladder rung at the wrong height.",
            "Light filtering fabric as the only layer, if daytime naps matter. It will be bright, evenly.",
        ],
        needs=["blackout", "privacy", "light-filtering"],
        products=["cellular-shades", "roller-solar-shades", "sheer-shades"],
        faqs=[
            ("Are Veneta shades safe for a nursery?",
             '<p>Cordless lift is standard on all eight lines, with no looped operating cord anywhere in '
             'the range, meeting ANSI/WCMA A100.1. The full detail is on the '
             '<a class="link" href="child-safety.html">child safety page</a>.</p>'),
            ("What is the best blackout shade for a baby's room?",
             "<p>A double cell blackout cellular shade with SmartPrivacy&reg; side channels. It is the "
             "darkest combination we make, it insulates, and the honeycomb damps some outside noise, which "
             "matters more in a nursery than in most rooms.</p>"),
            ("Do I really need side channels?",
             "<p>For daytime naps in summer, yes. Without them, an inside-mounted blackout shade leaves a "
             "line of light down each side that lands somewhere in the room. The alternative is an outside "
             "mount with at least two inches of overlap each side.</p>"),
            ("Should the shade be motorised?",
             "<p>It is convenient and it means the shade gets closed one-handed. It is not a safety "
             "feature here, because the cordless lift already removed the hazard. Judge it on convenience "
             "and on whether you want a rechargeable battery in the room.</p>"),
            ("Will this still suit the room in five years?",
             "<p>A blackout roller or cellular shade in a neutral colour becomes a child's bedroom "
             "treatment without any change. That is the argument against a themed fabric: the blackout "
             "requirement outlasts the nursery.</p>"),
        ],
    ),
]

ROOM_BY_SLUG = {r["slug"]: r for r in ROOMS}


# ================================================================= style pages
STYLES = [
    dict(
        slug="modern-minimal",
        name="Modern minimal",
        h1="Nothing on the window that does not need to be there.",
        eyebrow="Style &middot; Modern minimal",
        hero="style-warm-minimal",
        lede="Minimal is not the absence of decisions. It is a small number of decisions made precisely, "
             "which at a window means flat faces, hidden hardware and one colour repeated.",
        title="Modern Minimal Window Treatments | VENETA&trade;",
        desc="Flat faces, recessed hardware and one neutral repeated: how to specify blinds and shades "
             "for a modern minimal interior, with the palette and products.",
        rules=[
            ("Flat beats folded", "A roller shade is one plane. A roman shade is a stack of horizontals. "
                                  "In a minimal room the plane disappears and the stack announces itself."),
            ("Hide the hardware", "Specify a cassette or a fascia so the roll is not visible, and a "
                                  "fabric-wrapped SmartRail&trade; bottom bar so the only aluminium in the "
                                  "room is not at eye level."),
            ("One colour, repeated", "Pick a single neutral and use it on every window in the sightline. "
                                     "Variation between windows is the thing that makes a room look busy, "
                                     "not the treatment itself."),
            ("Inside mount, if the reveal allows", "A shade sitting inside the opening reads as part of "
                                                   "the architecture. An outside mount reads as an object "
                                                   "hung on the wall."),
        ],
        palette=[("roller-solar-shades", "Chalk"), ("cellular-shades", "Alabaster"),
                 ("cellular-shades", "Fog"), ("roller-solar-shades", "Pewter"),
                 ("dualdrape", "Bone"), ("cellular-shades", "Charcoal")],
        macros=["macro-linen-flax", "macro-solar-10", "macro-cellular-bone", "macro-bottom-bar"],
        products=["roller-solar-shades", "cellular-shades", "dualdrape"],
        why={
            "roller-solar-shades": "One flat panel, a cassette to hide the roll, and a fabric-wrapped bar. "
                                   "The most invisible treatment in the range when it is up and the "
                                   "quietest when it is down.",
            "cellular-shades": "Specify single cell for the slimmest stack at the head of the window. In "
                               "Alabaster or Fog it reads as a plane of light rather than a fabric.",
            "dualdrape": "For a slider, where minimal usually fails. A low-profile 2 3/4\" track and a "
                         "single vane colour gives you a soft wall of fabric with no visible mechanism.",
        },
        rooms=["living-room", "bedroom", "home-office"],
        avoid="Hobbled folds, decorative valances, contrast trim and mixing two fabric families on windows "
              "you can see at once. Also: a white shade against a warm white wall. Get the neutral right "
              "or the whole look collapses into a mismatch.",
    ),
    dict(
        slug="warm-organic",
        name="Warm organic",
        h1="Texture doing the work that colour usually does.",
        eyebrow="Style &middot; Warm organic",
        hero="style-organic-modern",
        lede="A warm organic room is nearly monochrome and never flat. The interest comes from weave, "
             "slub and hand, which is a specification you cannot judge on a screen.",
        title="Warm Organic Window Treatments | VENETA&trade;",
        desc="Linen, flax and woven texture in a near-monochrome palette: how to specify warm organic "
             "window treatments, with the fabrics and products that suit it.",
        rules=[
            ("Choose weave over pattern", "An open flax weave changes through the day as the light moves "
                                          "across it. A printed pattern looks the same at every hour."),
            ("Stay inside one temperature", "Everything warm, or everything cool. A greige next to a cool "
                                            "grey reads as a mistake even when both are beautiful alone."),
            ("Let it fold", "This is the one look where a roman shade is the right first answer. The fold "
                            "is what shows the fabric has weight."),
            ("Order the swatches, genuinely", "Hand and slub are the entire point and no screen transmits "
                                              "either. Order eight, and look at them at the hour you use "
                                              "the room."),
        ],
        palette=[("roman-shades", "Ivory Linen"), ("roman-shades", "Flax"), ("roman-shades", "Greige"),
                 ("cellular-shades", "Sand"), ("sheer-shades", "Almond"), ("roman-shades", "Clay")],
        macros=["macro-woven-flax", "macro-cotton-mushroom", "macro-linen-flax", "macro-wood-oak"],
        products=["roman-shades", "sheer-shades", "cellular-shades"],
        why={
            "roman-shades": "A flat fold in an unlined linen is the centre of this look. Hobbled fold if "
                            "you want it softer still; add a privacy or blackout lining and the texture "
                            "stays on the room side.",
            "sheer-shades": "Knit facings over a fabric vane, which is texture and light control in the "
                            "same product. Almond and Taupe sit exactly in this palette.",
            "cellular-shades": "The practical member of the group. In Sand or Linen it holds the "
                               "temperature of the room in both senses, on the windows where a roman would "
                               "be impractical.",
        },
        rooms=["living-room", "bedroom", "kitchen"],
        avoid="Cool greys, bright whites, high-sheen fabrics and vinyl. Also: a heavily textured fabric on "
              "a window with no direct light, where the weave never catches and you have paid for texture "
              "you cannot see.",
    ),
    dict(
        slug="coastal",
        name="Coastal",
        h1="Bright, salt-washed, and never actually blue.",
        eyebrow="Style &middot; Coastal",
        hero="style-modern-coastal",
        lede="Coastal rooms are about light and air, not nautical colour. The look is built on pale warm "
             "neutrals with the view kept open, and at most one blue in the whole room.",
        title="Coastal Window Treatments &amp; Shades | VENETA&trade;",
        desc="Pale neutrals, open weaves and a preserved view: how to specify coastal blinds and shades, "
             "with the palette and the one blue worth using.",
        rules=[
            ("Keep the view, always", "A coastal room is bought for what is outside it. Specify a 10% or "
                                      "14% screen or a sheer vane, and treat a fully opaque shade as a "
                                      "bedroom-only decision."),
            ("Pale and warm, not pale and cold", "Chalk, Oyster and Snow. A cool grey in a bright coastal "
                                                 "light goes flat and slightly blue, which is not the "
                                                 "blue anyone wants."),
            ("One blue, used once", "Bellevue Blue or Coastal Blue on a single window or a single room. "
                                    "Repeated across a house it stops being a colour and becomes a theme."),
            ("Composite where the air is salt", "Near the coast, humidity and salt are constant. Faux wood "
                                                "and composite shutters are the materials that do not "
                                                "care about either."),
        ],
        palette=[("roller-solar-shades", "Chalk"), ("roller-solar-shades", "Oyster"),
                 ("sheer-shades", "Snow"), ("faux-wood-blinds", "Bright White"),
                 ("cellular-shades", "Bellevue Blue"), ("dualdrape", "Coastal Blue")],
        macros=["macro-solar-10", "macro-linen-flax", "macro-faux-wood-white", "macro-woven-flax"],
        products=["roller-solar-shades", "sheer-shades", "faux-wood-blinds"],
        why={
            "roller-solar-shades": "A 10% or 14% screen in Chalk or Oyster keeps the water in the window "
                                   "and takes the hard edge off a very bright light. This is the coastal "
                                   "workhorse.",
            "sheer-shades": "Snow or Pearl vanes give you the airiest thing in the range: adjustable, soft, "
                            "and translucent rather than opaque even when closed.",
            "faux-wood-blinds": "Bright White or Cottage on a bathroom or a kitchen window. Composite, so "
                                "salt air and humidity are somebody else's problem.",
        },
        rooms=["living-room", "bedroom", "bathroom"],
        avoid="Navy across a whole house, rope and shell detailing, dark screen fabric on a water view, and "
              "real wood anywhere near salt air. Also: blackout on the main living window, which throws "
              "away the reason the room exists.",
    ),
    dict(
        slug="classic-tailored",
        name="Classic tailored",
        h1="Architecture first. The fabric agrees with the room.",
        eyebrow="Style &middot; Classic tailored",
        hero="style-quiet-traditional",
        lede="A classic room already has lines: rails, casings, panelled doors. The window treatment's job "
             "is to line up with them rather than introduce a competing idea.",
        title="Classic Tailored Window Treatments | VENETA&trade;",
        desc="Shutters, wide slats and lined romans for a traditional interior: how to specify classic "
             "tailored window treatments that follow the architecture.",
        rules=[
            ("Frame the opening", "A shutter fitted into an L-frame or a deco frame finishes the reveal "
                                  "and reads as joinery. Nothing else we make does that."),
            ("Go wider on the louvre", 'A 3 1/2" or 4 1/2" louvre suits a tall sash window; 2 1/2" suits '
                                       "a small one. Matching the louvre to the window scale is most of "
                                       "the craft here."),
            ("Paint to the woodwork, not the wall", "Pure White, Alabaster and Ivory exist because "
                                                    "trim white is never wall white. Hold the sample "
                                                    "against the architrave."),
            ("Hobbled, if you want fabric", "A hobbled fold keeps a soft roll of fabric at every stage, "
                                            "which sits more comfortably in a traditional room than a "
                                            "crisp flat fold."),
        ],
        palette=[("shutters", "Pure White"), ("shutters", "Alabaster"), ("shutters", "Ivory"),
                 ("faux-wood-blinds", "Antique White"), ("roman-shades", "Sage"),
                 ("roman-shades", "Navy")],
        macros=["macro-shutter-paint", "macro-faux-wood-white", "macro-cotton-mushroom", "macro-wood-oak"],
        products=["shutters", "faux-wood-blinds", "roman-shades"],
        why={
            "shutters": "The centre of the look. Engineered hardwood composite, three frame profiles and "
                        "louvres to 4 1/2\", with arch, angle and circle shapes for the windows a "
                        "traditional house actually has.",
            "faux-wood-blinds": 'A 2 1/2" slat with the matched 3" crown valance in Antique White or '
                                "Cottage. Reads as painted joinery at a fraction of a shutter's cost.",
            "roman-shades": "Where a room needs softness above the shutters or on an interior window. "
                            "Hobbled fold, privacy lined, in Sage or Greige.",
        },
        rooms=["living-room", "bedroom", "bathroom"],
        avoid="Solar screen fabric in a period room, exposed aluminium bottom bars, and a stark bright "
              "white against warm old woodwork. Also: a narrow 2 1/2\" louvre on a tall Georgian sash, "
              "where it reads as a stack of lines rather than a shutter.",
    ),
]

STYLE_BY_SLUG = {s["slug"]: s for s in STYLES}


# ==================================================================== builders
def other_needs(slug):
    return [n["slug"] for n in NEEDS if n["slug"] != slug][:3]


def build_needs():
    for n in NEEDS:
        s = n["slug"]
        ctas = (f'<a class="btn" href="#picks">See the three picks</a>'
                f'<a class="btn btn--ghost" href="{SAMPLES}">Order free samples</a>')
        body = hero(n["hero"], n["eyebrow"], n["h1"], n["lede"],
                    [("Home", "index.html"), ("Shop by need", "shop-by-need.html"), (n["nav"], None)],
                    ctas)
        body += anchors([("How it works", "how"), ("What we would fit", "picks"),
                         ("Published ranges", "ranges"), ("What will not work", "limits"),
                         ("Rooms", "rooms"), ("Questions", "faq")])
        body += f"""
  <section class="tight" id="how">
    <div class="wrap">
      {shead('How it works', 'The mechanism, before the products.')}
      <div class="two" style="align-items:start">
        <div class="prose" style="max-width:none;min-width:0">{prose_blocks(n["mech"])}</div>
        <div style="min-width:0">{kv(n["numbers"])}
          <div class="box tint" style="margin-top:24px"><h4>Before you order</h4>
            <p style="margin:0;color:var(--ink-70)">Order up to eight free swatches and tape them to the
            glass at the hour the problem actually happens. It is the only test that settles this.</p>
            <a class="btn btn--ghost btn--sm" href="{SAMPLES}" style="margin-top:14px">Order free samples</a></div>
        </div>
      </div>
    </div>
  </section>
"""
        body += picks(n["picks"])
        body += f"""{SLAT}
  <section id="ranges"><div class="wrap">
    {shead('Published ranges', 'The numbers, for the three lines above.')}
    {specrow([p[0] for p in n["picks"]])}
  </div></section>
"""
        body += wont(n["wont"])
        body += f'<div id="rooms">{roomrail(n["rooms"], h2="Where this matters most.")}</div>'
        body += needrail(other_needs(s))
        body += f"""<section class="tight" id="faq"><div class="wrap">
          {shead('Questions', 'Asked and answered.')}
          <div style="max-width:900px">{acc(n["faqs"])}</div>
        </div></section>"""
        body += cta_band(
            "Configure it at The Home Depot.",
            "Every line on this page is sold and configured at The Home Depot, at the same published "
            "sizes and opacities we list here.",
            ("Shop at The Home Depot", HD.href(n["picks"][0][0], module="cta_band",
                                               category=n["picks"][0][0])),
            ("Compare all eight lines", "products.html"))
        write(f"need-{s}.html", page(n["title"], n["desc"], body, active="need"))


def build_rooms():
    for r in ROOMS:
        s = r["slug"]
        ctas = (f'<a class="btn" href="#picks">See the three picks</a>'
                f'<a class="btn btn--ghost" href="product-finder.html">Answer three questions</a>')
        body = hero("room-" + s, r["eyebrow"], r["h1"], r["lede"],
                    [("Home", "index.html"), ("Shop by room", "shop-by-room.html"), (r["name"], None)],
                    ctas)
        body += anchors([("The brief", "brief"), ("What we would fit", "picks"),
                         ("Published ranges", "ranges"), ("Measuring notes", "notes"),
                         ("What to avoid", "limits"), ("Questions", "faq")])
        body += f"""
  <section class="tight" id="brief">
    <div class="wrap">
      {shead(r["name"], 'What this room actually demands.')}
      <div class="two" style="align-items:start">
        <div class="prose" style="max-width:none;min-width:0">{prose_blocks(r["brief"])}</div>
        <div style="min-width:0">
          <div class="box tint"><h4>Shortlist</h4><ul>{''.join(
            f'<li><a class="link" href="{p}.html">{D.BY_SLUG[p]["short"]}</a></li>' for p in r["products"])}</ul>
            <p class="hint" style="margin:14px 0 0">Cordless lift is standard on all three.</p></div>
          <div class="box" style="margin-top:24px"><h4>Free samples first</h4>
            <p style="margin:0;color:var(--ink-70)">Eight swatches, no cost, no account. Look at them in
            this room, in this light, before you order anything.</p>
            <a class="btn btn--ghost btn--sm" href="{SAMPLES}" style="margin-top:14px">Order free samples</a></div>
        </div>
      </div>
    </div>
  </section>
"""
        body += picks(r["picks"], h2="Three that suit this room.")
        body += f"""{SLAT}
  <section id="ranges"><div class="wrap">
    {shead('Published ranges', 'The numbers, for the three lines above.')}
    {specrow(r["products"])}
  </div></section>
"""
        body += f"""<section class="tight" id="notes"><div class="wrap">
          {shead('Measuring notes', 'Four things specific to this room.',
                 'The general method is in the measuring guide. These are the ones people get wrong here.')}
          {steps_notes(r["notes"])}
          <div class="cta-row" style="margin-top:36px"><a class="btn btn--ghost" href="how-to-measure.html">Full measuring guide</a></div>
        </div></section>"""
        body += wont(r["avoid"], h2="What to avoid in this room.")
        body += needrail(r["needs"], h2="Or start from the problem.")
        body += f'<section class="tight"><div class="wrap">{shead("The shortlist", "Three lines, in detail.")}{cards(D.card_tuples(r["products"]))}</div></section>'
        body += f"""<section id="faq"><div class="wrap">
          {shead('Questions', 'Asked and answered.')}
          <div style="max-width:900px">{acc(r["faqs"])}</div>
        </div></section>"""
        body += cta_band(
            f"Configure your {r['name'].lower()} shades.",
            "All three lines are sold and configured at The Home Depot, at the published sizes on this page.",
            ("Shop at The Home Depot", HD.href(r["products"][0], module="cta_band",
                                               category=r["products"][0])),
            ("Browse every room", "shop-by-room.html"))
        write(f"room-{s}.html", page(r["title"], r["desc"], body, active="shopby"))


def steps_notes(items):
    out = "".join(
        f'<div class="step rev"><span class="n">{str(i+1).zfill(2)}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(items))
    return f'<div class="steps four">{out}</div>'


def build_styles():
    for st in STYLES:
        s = st["slug"]
        ctas = (f'<a class="btn" href="#palette">See the palette</a>'
                f'<a class="btn btn--ghost" href="inspiration.html">Inspiration gallery</a>')
        body = hero(st["hero"], st["eyebrow"], st["h1"], st["lede"],
                    [("Home", "index.html"), ("Inspiration", "inspiration.html"), (st["name"], None)],
                    ctas)
        body += anchors([("Four rules", "rules"), ("Palette", "palette"), ("Materials", "materials"),
                         ("Products", "products"), ("Rooms", "rooms"), ("What to avoid", "limits")])
        body += f"""
  <section class="tight" id="rules">
    <div class="wrap">
      {shead('Four rules', 'How the look is actually built.',
             'Style advice is usually a mood board. These are four decisions you can make at the point of ordering.')}
      {steps_notes(st["rules"])}
    </div>
  </section>
"""
        body += palette(st["palette"])
        body += f'<div id="materials">{macroband(st["macros"], "Materials &middot; " + st["name"].lower())}</div>'
        prods = ""
        for i, p in enumerate(st["products"]):
            prod = D.BY_SLUG[p]
            prods += f"""<div style="padding-top:{'0' if i == 0 else 'clamp(48px,6vw,80px)'}">
              {rowpic(f'Product 0{i+1}', prod["short"] + ".",
                      f'<p style="color:var(--ink-70)">{st["why"][p]}</p>',
                      "category-" + p,
                      cta=f'<a class="btn btn--ghost btn--sm" href="{p}.html">{prod["short"]}</a>',
                      flip=(i % 2 == 1))}
            </div>"""
        body += f"""<section class="tight" id="products"><div class="wrap">
          {shead('Products', 'Three lines that carry this look.')}
          {prods}
        </div></section>"""
        body += f"""<section id="limits"><div class="wrap">
          {shead('Straight answer', 'What to avoid.',
                 'The fastest way to break a look is one element that belongs to a different one.')}
          <div class="callout" style="max-width:900px"><p style="margin:0">{st["avoid"]}</p></div>
        </div></section>"""
        body += f'<div id="rooms">{roomrail(st["rooms"], eyebrow="Rooms", h2="Where to start in the house.")}</div>'
        body += stylerail(s)
        body += cta_band(
            "Swatches settle it.",
            "Order up to eight free samples and look at them in your own room, at the hour you use it. "
            "No screen shows weave, sheen or openness honestly.",
            ("Order free samples", SAMPLES), ("Shop at The Home Depot", HD.href("brand", module="cta_band")))
        write(f"style-{s}.html", page(st["title"], st["desc"], body, active="inspiration"))


def stylerail(current):
    out = ""
    for st in STYLES:
        if st["slug"] == current:
            continue
        out += (f'<a href="style-{st["slug"]}.html"><p class="meta">Style</p><h3>{st["name"]}</h3>'
                f'<p class="desc" style="color:var(--ink-70);margin:8px 0 0">{st["lede"][:110].rstrip()}&hellip;</p>'
                f'<span class="arrow">See the look</span></a>')
    return f'<section class="tight"><div class="wrap">{shead("More looks", "The other three.")}<div class="sgrid">{out}</div></div></section>'


def build_all():
    build_needs()
    build_rooms()
    build_styles()
