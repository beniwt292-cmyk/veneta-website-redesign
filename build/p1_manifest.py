#!/usr/bin/env python3
"""Generates docs/p1-manifest.json — the single source of truth for the P1 image set.

Every shot carries its own full prompt, generation size, crop ratio, final
dimensions, byte budget, alt text and batch number, so a build agent can run one
batch without reading MASTER_PLAN.md. Regenerate with:

    python3 build/p1_manifest.py

Amendments to MASTER_PLAN.md §11 encoded here (image generation maxes out at
1536px long edge and offers only 1:1, 3:2 and 2:3):
  - long edges are native, never upscaled: heroes 1536, cards/macros 1024,
    triptychs 1000
  - non-native ratios (16:9, 4:5, 3:4, 4:3) are centre-cropped from the three
    generatable sizes, so gen_size and ratio are stored separately
  - og:image set is script-cropped from accepted heroes (see build/images.py og)
  - guides/diagrams are hand-built SVG, not generated
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "p1-manifest.json")
BATCH_SIZE = 5

# ---------------------------------------------------------------- art direction
PALETTE = "warm bone, limestone, flax, mushroom, white oak"
MOOD = "calm, precise, quietly expensive, believable, tactile"
AVOID = ("warped mullions, uneven slat or pleat spacing, duplicated furniture or decor, "
         "impossible shadow directions, legible text or signage, glossy CGI surfaces, "
         "HDR halos, people, pets, oversaturated colour")

RATIOS = {"16:9": (16, 9), "3:2": (3, 2), "4:5": (4, 5), "3:4": (3, 4),
          "1:1": (1, 1), "4:3": (4, 3), "2:3": (2, 3)}
GEN = {"land": "1536x1024", "port": "1024x1536", "sq": "1024x1024"}

BUDGETS = {  # KB, AVIF
    "hero": 180, "category": 140, "index": 70, "macro": 90, "triptych": 60,
    "room": 90, "style": 120, "motor": 140, "safety": 120, "trade": 140,
}


def final_dims(gen_size, ratio, long_edge):
    gw, gh = (int(v) for v in gen_size.split("x"))
    rw, rh = RATIOS[ratio]
    # centre-crop the generated frame to the target ratio, then scale to long_edge
    if rw / rh >= gw / gh:
        cw, ch = gw, round(gw * rh / rw)
    else:
        ch, cw = gh, round(gh * rw / rh)
    scale = long_edge / max(cw, ch)
    return max(1, round(cw * scale)), max(1, round(ch * scale))


def room_prompt(s):
    return (
        f"{s['subject']}, featuring {s['product']} in {s['material']}, {s['position']}. "
        f"Natural {s.get('light', 'morning')} daylight from camera-{s.get('dir', 'left')} showing realistic "
        f"filtered light and soft directional shadows on {s.get('surface', 'white oak flooring and lime-plaster walls')}. "
        f"Shot on {s.get('lens', '32mm')}, eye-level architectural interior photography, camera height 4'8\", "
        f"corrected verticals, editorial composition, generous negative space{s.get('space', '')}. "
        f"Palette: {s.get('palette', PALETTE)}. Mood: {MOOD}. "
        f"Under-styled, maximum three props, no legible lettering. "
        f"Emphasise: {s['feature']}, even pleat and slat spacing, crisp fabric edges, accurate window "
        f"proportions, visible weave texture. Avoid: {AVOID}. "
        f"Framed so a centre crop to {s['ratio']} keeps the composition intact. "
        f"Photorealistic. Matte film finish, fine grain."
    )


def macro_prompt(s):
    return (
        f"Macro photograph of {s['subject']} in {s['material']}, with visible fibre, texture and natural "
        f"colour variation. Soft directional daylight raking across the surface from camera-{s.get('dir', 'right')}. "
        f"Shot on 100mm macro, editorial materials photography, shallow but realistic depth of field. "
        f"Emphasise: {s['feature']}, weave or grain rhythm, tactile hand, subtle irregularity. "
        f"Avoid: repeating pattern glitches, plastic sheen, synthetic uniformity, HDR halos, legible text. "
        f"Framed so a centre crop to {s['ratio']} keeps the composition intact. "
        f"Photorealistic. Matte film finish, fine grain."
    )


def triptych_prompt(s):
    return (
        f"Straight-on view of a single window fitted with {s['product']} in {s['material']}, {s['position']}, "
        f"{s['subject']}. Neutral warm-bone interior wall, no furniture. Natural midday daylight. "
        f"Shot on 50mm, perfectly level, corrected verticals, clinical editorial product photography. "
        f"Emphasise: {s['feature']}, even tension across the fabric, straight level bottom bar. "
        f"Avoid: warped mullions, uneven fabric tension, legible exterior detail, {AVOID}. "
        f"Aspect ratio 1:1. Photorealistic, matte finish, fine grain."
    )


BUILDERS = {"macro": macro_prompt, "triptych": triptych_prompt}

# ---------------------------------------------------------------- shot specs
CATEGORIES = [
    ("cellular-shades", "Sunlit open-plan dining room in a warm modern interior",
     "cordless cellular shades", "bone honeycomb fabric", "half lowered across two tall windows",
     "the soft glow of light through the honeycomb cells, uniform pleat depth", "left",
     "cellular shades in bone honeycomb fabric, half lowered in a sunlit modern dining room"),
    ("roller-solar-shades", "Calm living room with a tall window wall",
     "light-filtering roller shades", "flax linen weave", "three-quarters lowered",
     "the even weave openness and crisp shade edge", "right",
     "flax linen roller shades three-quarters lowered across a tall living room window wall"),
    ("roman-shades", "Quiet reading corner in a warm modern interior",
     "cordless Roman shades", "mushroom textured cotton", "raised to two-thirds with soft flat folds",
     "the weight and evenness of the flat folds", "left",
     "mushroom cotton Roman shades with flat folds in a sunlit reading corner"),
    ("faux-wood-blinds", "Bright kitchen with a deep window sill",
     "faux wood blinds", "warm white 2.5-inch slats", "slats tilted half open",
     "coherent ladder and tilt geometry, consistent slat spacing", "right",
     "warm white faux wood blinds with slats tilted half open in a bright kitchen"),
    ("shutters", "Bay window in a limestone-toned living room",
     "interior plantation shutters", "warm white painted hardwood", "louvres tilted upward, panels closed",
     "realistic stile and rail proportions, clean hinge lines", "left",
     "warm white plantation shutters on a bay window in a limestone-toned living room"),
    ("sheer-shades", "Serene bedroom with a wide window",
     "sheer horizontal shades", "bone fabric vanes between sheer facings", "vanes fully open, shade lowered",
     "consistent transparency across every vane", "right",
     "bone sheer shades with open fabric vanes diffusing daylight in a serene bedroom"),
    ("dualdrape", "Wide patio door in a warm minimal living space",
     "DualDrape vertical sheer panels", "flax fabric vanes on a sheer backing", "vanes half rotated",
     "even vane spacing and the layered sheer effect", "left",
     "flax DualDrape vertical sheer panels half rotated across a wide patio door"),
    ("vertical-blinds", "Sliding glass door in a bright family room",
     "cordless vertical blinds", "mushroom textured vinyl vanes", "vanes rotated to half open",
     "straight plumb vanes and even spacing", "right",
     "mushroom vertical blinds rotated half open across a sliding glass door"),
    ("woven-wood-shades", "Sunlit stairwell landing with a tall window",
     "woven wood shades", "flax and mushroom bamboo reed", "half lowered",
     "weave rhythm that does not visibly tile, warm light through the reeds", "left",
     "flax bamboo woven wood shades half lowered on a tall stairwell window"),
]

MACROS = [
    ("woven-flax", "woven wood shade material", "flax and mushroom bamboo and reed fibres with visible slubs", "fibre detail and weave rhythm"),
    ("cellular-bone", "cellular shade honeycomb material seen edge-on", "bone spun polyester with crisp cell walls", "the geometry of the honeycomb cells"),
    ("linen-flax", "roller shade fabric", "flax linen with an open plain weave", "thread count and weave openness"),
    ("solar-5", "solar shade mesh at 5 percent openness", "espresso and charcoal fibreglass yarn", "the precise grid of the mesh"),
    ("solar-10", "solar shade mesh at 10 percent openness", "bone and limestone yarn", "the open grid and yarn twist"),
    ("cotton-mushroom", "Roman shade fabric", "mushroom textured cotton with a soft slub", "the hand of the cloth and fold memory"),
    ("faux-wood-white", "faux wood blind slat", "warm white composite with a subtle grain emboss", "the slat edge profile and matte finish"),
    ("wood-oak", "real wood blind slat", "muted white oak with visible grain", "grain direction and satin sheen"),
    ("shutter-paint", "shutter louvre and stile joint", "warm white painted hardwood", "the paint texture and joinery line"),
    ("sheer-vane", "sheer shade fabric vane against its sheer facing", "bone polyester", "the layered translucency"),
    ("blackout-espresso", "blackout roller shade fabric", "espresso coated fabric", "the dense opaque surface and matte coating"),
    ("bottom-bar", "the bottom bar and hem of a cordless shade", "brushed aluminium and flax fabric", "the level hem line and hardware finish"),
]

TRIPTYCHS = [
    ("solar", "solar roller shades", [("5", "at 5 percent openness, fully lowered", "bright exterior visible as a soft silhouette through the weave"),
                                      ("10", "at 10 percent openness, fully lowered", "exterior shapes softly readable through the weave"),
                                      ("open", "fully raised", "the bare window and clean rolled shade at the head")]),
    ("cellular", "cellular shades", [("light", "in light-filtering bone fabric, fully lowered", "an even glow across the whole blind"),
                                     ("room", "in room-darkening bone fabric, fully lowered", "a soft halo only at the edges"),
                                     ("black", "in blackout fabric, fully lowered", "a near-dark window with a thin light line at the sill")]),
    ("sheer", "sheer horizontal shades", [("open", "with vanes fully open, lowered", "clear diffused daylight between the vanes"),
                                          ("half", "with vanes half rotated, lowered", "banded light across the fabric"),
                                          ("closed", "with vanes fully closed, lowered", "a flat privacy surface with no gaps")]),
]

ROOMS = [
    ("living-room", "Living room with a low sofa and a tall window", "light-filtering roller shades", "flax linen", "half lowered", "glare control with the view kept"),
    ("bedroom", "Bedroom with a linen-dressed bed", "blackout cellular shades", "bone honeycomb", "three-quarters lowered", "the darkening effect and even pleats"),
    ("nursery", "Nursery with a simple crib away from the window", "cordless cellular shades", "bone honeycomb", "fully lowered", "the absence of any cord or chain"),
    ("kitchen", "Kitchen with a window above the sink", "faux wood blinds", "warm white slats", "slats tilted open", "the wipeable matte slat surface"),
    ("home-office", "Home office with a desk side-on to the window", "solar roller shades", "charcoal 5 percent mesh", "fully lowered", "screen-safe glare control"),
    ("bathroom", "Bathroom with a small high window", "interior shutters", "warm white hardwood", "louvres closed", "privacy with light still entering"),
]

STYLES = [
    ("warm-minimal", "Warm minimal living room", "roller shades", "flax linen", "half lowered", "restraint and material honesty"),
    ("modern-coastal", "Modern coastal dining room", "woven wood shades", "bone bamboo reed", "two-thirds lowered", "airy light and natural fibre"),
    ("quiet-traditional", "Quiet traditional sitting room", "Roman shades", "mushroom cotton", "raised to half", "soft folds against panelled trim"),
    ("organic-modern", "Organic modern bedroom", "cellular shades", "limestone honeycomb", "three-quarters lowered", "calm tonal layering"),
]

MOTOR = [
    ("dusk-bedroom", "Minimal bedroom at dusk in a modern interior", "motorized cellular shades", "bone honeycomb", "half lowered",
     "even pleat spacing and precise alignment", "espresso, charcoal, bone, white oak", " with a deep blue-grey exterior sky and low warm interior light"),
    ("living-wall", "Living room with a three-window wall in the morning", "motorized roller shades", "flax linen", "lowered to three matching heights",
     "identical alignment across all three shades", PALETTE, ""),
    ("patio-run", "Open living space with a wide patio door", "motorized vertical sheer panels", "flax fabric", "half rotated",
     "the clean headrail with no visible cords or devices", PALETTE, ""),
]

SAFETY = [
    ("nursery-cordless", "Nursery corner with a low bookshelf under the window", "cordless cellular shades", "bone honeycomb", "fully lowered",
     "a completely clean window with no cord, chain or wand"),
    ("playroom", "Bright playroom with a wide low window", "cordless roller shades", "limestone linen", "half lowered",
     "the plain hem and absence of any hanging control"),
]

TRADE = [
    ("hospitality-room", "Boutique hotel guest room", "blackout roller shades", "espresso coated fabric", "three-quarters lowered", "repeatable specification and clean sightlines"),
    ("hospitality-lounge", "Hotel lounge with a tall glazed wall", "solar roller shades", "charcoal 10 percent mesh", "fully lowered", "uniform shade lines across a long run"),
    ("office-open", "Open-plan office with a long window run", "solar roller shades", "charcoal 5 percent mesh", "lowered to a matching height", "consistent alignment down the whole run"),
    ("office-meeting", "Small glass-walled meeting room", "sheer shades", "bone fabric vanes", "vanes half rotated", "privacy control without losing daylight"),
    ("multifamily-living", "Apartment living room in a new multifamily building", "cordless roller shades", "bone linen", "half lowered", "durable, uniform, cordless specification"),
    ("commercial-lobby", "Quiet commercial lobby with a limestone floor", "woven wood shades", "mushroom bamboo reed", "two-thirds lowered", "scale, repetition and warmth"),
]


def build():
    shots = []

    shots.append(dict(
        id="hero-home", set="hero", gen_size=GEN["land"], ratio="16:9", long_edge=1536,
        alt="Flax linen roller shades three-quarters lowered across a tall window wall in a sunlit open-plan living room",
        legacy=["hero.webp", "hero-card.webp"], lcp=True,
        prompt=room_prompt(dict(
            subject="Open-plan living room in a warm modern interior", ratio="16:9",
            product="light-filtering roller shades", material="flax linen",
            position="three-quarters lowered across a tall window wall",
            feature="the soft glow of light through the shade fabric, crisp shade edges",
            space=" at lower left for a headline", dir="left")),
    ))

    for slug, subject, product, material, position, feature, dirn, alt in CATEGORIES:
        shots.append(dict(
            id=f"category-{slug}", set="category", gen_size=GEN["land"], ratio="3:2", long_edge=1536,
            alt=alt, legacy=[], prompt=room_prompt(dict(
                subject=subject, product=product, material=material, position=position,
                feature=feature, dir=dirn, ratio="3:2")),
        ))

    for slug, subject, product, material, position, feature, dirn, alt in CATEGORIES[:8]:
        legacy = {"cellular-shades": "cellular-card.webp", "roller-solar-shades": "roller-card.webp",
                  "roman-shades": "roman-card.webp", "faux-wood-blinds": "fauxwood-card.webp",
                  "shutters": "shutters-card.webp", "sheer-shades": "sheer-card.webp",
                  "dualdrape": "dualdrape-card.webp", "vertical-blinds": "vertical-card.webp"}[slug]
        shots.append(dict(
            id=f"index-{slug}", set="index", gen_size=GEN["port"], ratio="4:5", long_edge=1024,
            alt=alt, legacy=[legacy], prompt=room_prompt(dict(
                subject=f"{subject}, tightly framed on the window", product=product, material=material,
                position=position, feature=feature, dir=dirn, lens="50mm", ratio="4:5")),
        ))

    for slug, subject, material, feature in MACROS:
        shots.append(dict(
            id=f"macro-{slug}", set="macro", gen_size=GEN["port"], ratio="3:4", long_edge=1024,
            alt=f"Macro detail of {subject} in {material}", legacy=[],
            prompt=macro_prompt(dict(subject=subject, material=material, feature=feature, ratio="3:4")),
        ))

    for group, product, frames in TRIPTYCHS:
        for key, position, subject in frames:
            shots.append(dict(
                id=f"triptych-{group}-{key}", set="triptych", gen_size=GEN["sq"], ratio="1:1", long_edge=1000,
                alt=f"{product.capitalize()} {position}, {subject}", legacy=[],
                prompt=triptych_prompt(dict(product=product, material="bone or charcoal fabric as specified",
                                            position=position, subject=subject,
                                            feature="the openness of the weave or fabric")),
            ))

    room_legacy = {"living-room": "room-vertical-card.webp", "home-office": "solar-card.webp"}
    for slug, subject, product, material, position, feature in ROOMS:
        shots.append(dict(
            id=f"room-{slug}", set="room", gen_size=GEN["port"], ratio="3:4", long_edge=1024,
            alt=f"{subject.split(' with ')[0]} fitted with {product} in {material}",
            legacy=[room_legacy[slug]] if slug in room_legacy else [],
            prompt=room_prompt(dict(subject=subject, product=product, material=material,
                                    position=position, feature=feature, lens="50mm", ratio="3:4")),
        ))

    for slug, subject, product, material, position, feature in STYLES:
        shots.append(dict(
            id=f"style-{slug}", set="style", gen_size=GEN["land"], ratio="3:2", long_edge=1536,
            alt=f"{subject} with {product} in {material}", legacy=[],
            prompt=room_prompt(dict(subject=subject, product=product, material=material,
                                    position=position, feature=feature, ratio="3:2")),
        ))

    for slug, subject, product, material, position, feature, palette, extra in MOTOR:
        shots.append(dict(
            id=f"motor-{slug}", set="motor", gen_size=GEN["land"], ratio="16:9", long_edge=1536,
            alt=f"{subject} with {product} in {material}, {position}", legacy=[],
            prompt=room_prompt(dict(subject=subject + extra, product=product, material=material,
                                    position=position, feature=feature, palette=palette, ratio="16:9"))
            + " No visible remote, device screens or glowing interface overlays.",
        ))

    for slug, subject, product, material, position, feature in SAFETY:
        shots.append(dict(
            id=f"safety-{slug}", set="safety", gen_size=GEN["land"], ratio="4:3", long_edge=1365,
            alt=f"{subject} fitted with {product} in {material}", legacy=[],
            prompt=room_prompt(dict(subject=subject, product=product, material=material,
                                    position=position, feature=feature, ratio="4:3")),
        ))

    for slug, subject, product, material, position, feature in TRADE:
        shots.append(dict(
            id=f"trade-{slug}", set="trade", gen_size=GEN["land"], ratio="3:2", long_edge=1536,
            alt=f"{subject} specified with {product} in {material}", legacy=[],
            prompt=room_prompt(dict(subject=subject, product=product, material=material,
                                    position=position, feature=feature, ratio="3:2")),
        ))

    for i, s in enumerate(shots):
        s["batch"] = i // BATCH_SIZE + 1
        s["budget_kb"] = BUDGETS[s["set"]]
        w, h = final_dims(s["gen_size"], s["ratio"], s["long_edge"])
        s["width"], s["height"] = w, h
        s["files"] = {"avif": f"assets/img/{s['id']}-{s['long_edge']}.avif",
                      "webp": f"assets/img/{s['id']}-{s['long_edge']}.webp"}
        s.setdefault("lcp", False)
        s.setdefault("legacy", [])

    # §6.4 needs a per-page og:image, so the card set covers every product line plus
    # one card per site area. build/seo.py maps all 50 pages onto these ids.
    og = [{"id": f"og-{n}", "source": src} for n, src in [
        ("home", "hero-home"), ("products", "category-cellular-shades"),
        ("cellular-shades", "category-cellular-shades"), ("roller-solar-shades", "category-roller-solar-shades"),
        ("roman-shades", "category-roman-shades"), ("shutters", "category-shutters"),
        ("faux-wood-blinds", "category-faux-wood-blinds"), ("sheer-shades", "category-sheer-shades"),
        ("dualdrape", "category-dualdrape"), ("vertical-blinds", "category-vertical-blinds"),
        ("motorization", "motor-dusk-bedroom"), ("child-safety", "safety-nursery-cordless"),
        ("rooms", "room-living-room"), ("need", "room-bedroom"),
        ("inspiration", "style-warm-minimal"), ("guides", "style-quiet-traditional"),
        ("support", "room-home-office"), ("innovation", "motor-living-wall"),
        ("trade", "trade-office-open"), ("commercial", "trade-commercial-lobby"),
        ("journal", "style-modern-coastal"),
        ("samples", "macro-linen-flax"), ("company", "style-organic-modern")]]

    doc = {
        "version": 1,
        "batch_size": BATCH_SIZE,
        "generated_count": len(shots),
        "grade": {"highlights": -8, "warmth": 3, "clarity": -5, "grain_pct": 8},
        "encode": {"avif_q": 55, "webp_q": 78},
        "og": og,
        "diagrams_are_svg": ["measure-inside-mount", "measure-outside-mount", "mount-types",
                             "shade-anatomy", "opacity-scale", "install-brackets"],
        "shots": shots,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
    return doc


if __name__ == "__main__":
    d = build()
    print("shots:", d["generated_count"], "batches:", d["shots"][-1]["batch"])
    for s in d["shots"][:3]:
        print(" ", s["batch"], s["id"], s["width"], "x", s["height"])
