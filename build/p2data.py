"""Content for the P2 template rebuild (§7).

Everything a §7.2 category page needs beyond build/data.py lives here: the chip
row, the three benefit paragraphs for the 5/7 split, the opacity triptych, the
macro band, the room links and the compare matrix.

One rule: nothing in this file may contradict build/data.py. Sizes, opacity names
and lift options are quoted from the spec tables there, not re-invented.
"""

# --- compare matrix ---------------------------------------------------------
# Single source of truth for every comparison table on the site. §7.2 allows a
# maximum of five columns, so each category page renders itself plus two rivals.
CMP_ROWS = [
    "Blackout available",
    "Keeps the view",
    "Insulates",
    "Humid rooms",
    "Spans over 96\"",
    "Motorized",
]

# y = yes, p = partial, n = no
CMP = {
    "cellular-shades":     ["y", "n", "y", "n", "y", "y"],
    "roller-solar-shades": ["y", "y", "p", "n", "y", "y"],
    "roman-shades":        ["y", "n", "p", "n", "n", "y"],
    "faux-wood-blinds":    ["p", "y", "p", "y", "n", "y"],
    "shutters":            ["p", "y", "y", "y", "y", "n"],
    "sheer-shades":        ["p", "y", "p", "n", "n", "y"],
    "dualdrape":           ["p", "y", "n", "n", "y", "n"],
    "vertical-blinds":     ["p", "y", "n", "y", "y", "n"],
}

CMP_LABEL = {"y": "Yes", "p": "Partial", "n": "No"}

# --- room links -------------------------------------------------------------
ROOM_SHOTS = {
    "living-room": ("Living room", "Glare control without losing the view"),
    "bedroom":     ("Bedroom", "Blackout, and quiet enough to sleep through"),
    "nursery":     ("Nursery", "Cordless first, dark second"),
    "kitchen":     ("Kitchen", "Wipes clean, handles steam"),
    "home-office": ("Home office", "Zero glare on the screen"),
    "bathroom":    ("Bathroom", "Privacy in a humid room"),
}

# --- per-category ------------------------------------------------------------
# chips   : the filter language a shopper already has in their head
# why     : (heading, paragraph) x3 for the 5/7 split
# split   : macro shot that carries the split
# opacity : (shot, label, note) x3, or [] when no triptych was shot
# macros  : four macro shots for the texture band
# rooms   : four room-scene slugs
# rivals  : the two other categories in the compare table
CAT = {
  "cellular-shades": {
    "why_h2": "Three jobs a honeycomb does that a flat shade cannot.",
    "chips": ["Light filtering", "Room darkening", "Blackout", "Cordless", "Motorized", "Insulating"],
    "why": [
      ("It works on the temperature, not just the light",
       "The honeycomb traps a pocket of still air against the glass, which is where a house loses "
       "most of its heat. Double cell holds a second pocket and insulates best."),
      ("Blackout without a blackout look",
       "A light filtering fabric reads as an even glow at midday. The same shade in blackout "
       "closes a bedroom down completely, with the same slim stack."),
      ("Top-down, bottom-up on the windows that need both",
       "Drop the top rail for daylight with the street covered, or raise the bottom rail the "
       "usual way. One shade, both jobs."),
    ],
    "split": "macro-cellular-bone",
    "opacity": [
      ("triptych-cellular-light", "Light filtering", "Even daylight, no view through"),
      ("triptych-cellular-room", "Room darkening", "Shapes stay visible, glare gone"),
      ("triptych-cellular-black", "Blackout", "Sealed for sleep"),
    ],
    "macros": ["macro-cellular-bone", "macro-cotton-mushroom", "macro-blackout-espresso", "macro-linen-flax"],
    "rooms": ["bedroom", "nursery", "living-room", "home-office"],
    "rivals": ["roman-shades", "roller-solar-shades"],
  },
  "roller-solar-shades": {
    "why_h2": "One flat fabric, and the whole decision is openness.",
    "chips": ["Solar screen", "Light filtering", "Blackout", "Cordless", "Motorized", "Keeps the view"],
    "why": [
      ("Openness is a number, so choose it deliberately",
       "1% blocks the most heat and glare and gives the least view. 14% keeps the view and lets "
       "more sun through. 5% is the default for a west-facing room."),
      ("One clean sweep of fabric",
       "No folds, no slats, no stack lines. Lowered it is a flat plane, raised it disappears "
       "into a 2\" roll at the top of the opening."),
      ("Blackout on the same hardware",
       "A blackout roller uses the same bracket and bottom bar as the screen, so a bedroom and "
       "an office can read as one system across a facade."),
    ],
    "split": "macro-solar-5",
    "opacity": [
      ("triptych-solar-open", "Shade raised", "The window as it is"),
      ("triptych-solar-10", "10% openness", "View kept, glare cut"),
      ("triptych-solar-5", "5% openness", "Heat and glare blocked"),
    ],
    "macros": ["macro-solar-5", "macro-solar-10", "macro-blackout-espresso", "macro-bottom-bar"],
    "rooms": ["home-office", "living-room", "kitchen", "bedroom"],
    "rivals": ["cellular-shades", "sheer-shades"],
  },
  "roman-shades": {
    "why_h2": "Drapery fabric, held in a fold that repeats.",
    "chips": ["Flat fold", "Hobbled fold", "Blackout lining", "Cordless", "Motorized", "Designer fabric"],
    "why": [
      ("Fabric, with the structure kept",
       "A flat fold hangs almost sheer against the frame. A hobbled fold holds a soft stack of "
       "curves even when it is fully lowered."),
      ("The lining decides the room",
       "Unlined for light, privacy lining for a street-facing window, blackout lining for a "
       "bedroom. The face fabric does not change."),
      ("Cord-free front and back",
       "Most fabric shades hide a cord ladder behind the panel. Ours does not, which is the "
       "reason a Roman shade can go in a nursery at all."),
    ],
    "split": "macro-linen-flax",
    "opacity": [],
    "macros": ["macro-linen-flax", "macro-cotton-mushroom", "macro-blackout-espresso", "macro-woven-flax"],
    "rooms": ["living-room", "bedroom", "nursery", "kitchen"],
    "rivals": ["cellular-shades", "sheer-shades"],
  },
  "faux-wood-blinds": {
    "why_h2": "Built for the rooms that ruin real wood.",
    "chips": ["2\" slats", "2 1/2\" slats", "Cordless", "Motorized", "Humid rooms", "Routeless"],
    "why": [
      ("Wood grain that will not move",
       "A polymer composite takes a real grain finish and then ignores the steam from a shower "
       "or a kettle. No warping, no bowing, no yellowing at the bottom slat."),
      ("Tilt is the real control",
       "Slats aimed up bounce daylight onto the ceiling. Aimed down they hold privacy and keep "
       "the view of the ground. That is a different tool from raising a shade."),
      ("Routeless slats close the pinholes",
       "The standard slat carries a route hole at every ladder. The routeless option moves the "
       "ladder to the edge, so a closed blind reads as a solid surface."),
    ],
    "split": "macro-faux-wood-white",
    "opacity": [],
    "macros": ["macro-faux-wood-white", "macro-wood-oak", "macro-bottom-bar", "macro-shutter-paint"],
    "rooms": ["kitchen", "bathroom", "living-room", "home-office"],
    "rivals": ["shutters", "cellular-shades"],
  },
  "shutters": {
    "why_h2": "The only covering that reads as part of the house.",
    "chips": ["2 1/2\" louvre", "3 1/2\" louvre", "4 1/2\" louvre", "L-frame", "Deco frame", "Hidden tilt"],
    "why": [
      ("It reads as part of the house",
       "A shutter is framed into the opening and painted like joinery. It is the one window "
       "treatment a buyer counts as a fixture rather than a furnishing."),
      ("Louvre size sets the character",
       "2 1/2\" is traditional and closes tightest. 4 1/2\" gives the widest view and the "
       "cleanest line on a large opening."),
      ("Insulation from the panel itself",
       "A closed hardwood composite panel plus the air gap behind it slows heat at the glass "
       "without any fabric in the room."),
    ],
    "split": "macro-shutter-paint",
    "opacity": [],
    "macros": ["macro-shutter-paint", "macro-wood-oak", "macro-faux-wood-white", "macro-linen-flax"],
    "rooms": ["living-room", "bathroom", "bedroom", "kitchen"],
    "rivals": ["faux-wood-blinds", "cellular-shades"],
  },
  "sheer-shades": {
    "why_h2": "A vane that tilts inside two layers of sheer.",
    "chips": ["2\" vane", "3\" vane", "Light filtering", "Room darkening vane", "Cordless", "Motorized"],
    "why": [
      ("A vane between two sheers",
       "Tilt the vane and the light changes without the shade moving. Open, the window is a "
       "soft screen. Closed, it is a quiet wall of fabric."),
      ("Glare, handled properly",
       "Two knit facings scatter direct sun instead of stopping it, so a south window loses the "
       "hot spot and keeps the brightness."),
      ("Vanes come out",
       "Individual vanes are removable, which means one damaged vane is a replacement part "
       "rather than a new shade."),
    ],
    "split": "macro-sheer-vane",
    "opacity": [
      ("triptych-sheer-open", "Vanes open", "View and full daylight"),
      ("triptych-sheer-half", "Vanes at 45\u00b0", "Light in, sightline gone"),
      ("triptych-sheer-closed", "Vanes closed", "Soft privacy, still not dark"),
    ],
    "macros": ["macro-sheer-vane", "macro-linen-flax", "macro-cotton-mushroom", "macro-woven-flax"],
    "rooms": ["living-room", "bedroom", "home-office", "nursery"],
    "rivals": ["cellular-shades", "roller-solar-shades"],
  },
  "vertical-blinds": {
    "why_h2": "The widest opening in the house, on one track.",
    "chips": ["Vinyl louvre", "Fabric louvre", "S-curve", "Cordless wand", "Split stack", "Humid rooms"],
    "why": [
      ("Built for the width, not scaled up to it",
       "A 144\" opening is the normal case here, not the limit. The weight hangs from a headrail "
       "track instead of a lift cord, so the span does not fight the mechanism."),
      ("Walk through without raising anything",
       "Rotate the louvres for light, draw them to one side to use the door. The stack sits "
       "clear of the handle."),
      ("Louvres are replaceable",
       "A cracked or discoloured louvre is a single part. Vinyl wipes clean; fabric louvres come "
       "out for washing."),
    ],
    "split": "macro-bottom-bar",
    "opacity": [],
    "macros": ["macro-bottom-bar", "macro-linen-flax", "macro-faux-wood-white", "macro-cotton-mushroom"],
    "rooms": ["living-room", "kitchen", "bathroom", "home-office"],
    "rivals": ["dualdrape", "faux-wood-blinds"],
  },
  "dualdrape": {
    "why_h2": "A patio door treated like a window, not a wall.",
    "chips": ["3 1/2\" vane", "Rotate and traverse", "Split stack", "Cordless wand", "Washable vanes", "Up to 192\""],
    "why": [
      ("A sheer and a drape on one track",
       "Rotate the vanes and the opening goes from a sheer screen to a run of soft fabric "
       "panels. There is no second layer to install."),
      ("Patio door scale as standard",
       "Up to 192\" wide and 120\" tall, stacking left, right or split at the centre so the "
       "handle stays reachable."),
      ("Vanes wash",
       "Each vane unclips from the carrier, so the fabric that faces a sliding door and a dog "
       "can be cleaned rather than replaced."),
    ],
    "split": "macro-sheer-vane",
    "opacity": [],
    "macros": ["macro-sheer-vane", "macro-woven-flax", "macro-linen-flax", "macro-bottom-bar"],
    "rooms": ["living-room", "kitchen", "bedroom", "home-office"],
    "rivals": ["vertical-blinds", "sheer-shades"],
  },
}

# --- guides shown at the foot of a category page ----------------------------
GUIDES = [
    ("how-to-measure.html", "Measuring", "How to measure a window",
     "Inside or outside mount, three-point measuring, and the deduction you must not make."),
    ("buying-guides.html", "Choosing", "Light filtering, room darkening or blackout",
     "The three opacity names mean three specific things. This is which one your room needs."),
    ("how-to-install.html", "Installing", "How to install brackets and a headrail",
     "Bracket spacing, depth and the order of operations, in six steps."),
]

# --- homepage ---------------------------------------------------------------
HOME_MACROS = ["macro-cellular-bone", "macro-woven-flax", "macro-solar-10", "macro-wood-oak"]
HOME_ROOMS = ["living-room", "bedroom", "nursery", "kitchen", "home-office", "bathroom"]

HANDOFF = [
    ("Configure the window",
     "Enter your measurements, fabric and lift option on the Home Depot product page. "
     "Every size in our published range is orderable there."),
    ("Home Depot takes the order",
     "Payment, delivery and returns are handled by The Home Depot under their policies. "
     "Nothing is sold on this site."),
    ("We build it to your numbers",
     "The order comes to our plant, is cut to your measurements and ships to your address, "
     "typically inside two weeks."),
]

# --- inspiration gallery (§7.4) ---------------------------------------------
# (shot, aspect, room, product, href) — aspect drives the mixed grid
GALLERY = [
    ("room-living-room", "portrait", "Living room", "Vertical blinds", "vertical-blinds.html"),
    ("style-warm-minimal", "landscape", "Open plan", "Roller shades", "roller-solar-shades.html"),
    ("macro-woven-flax", "square", "Material", "Woven flax", "roman-shades.html"),
    ("room-bedroom", "portrait", "Bedroom", "Blackout cellular", "cellular-shades.html"),
    ("category-shutters", "landscape", "Bay window", "Shutters", "shutters.html"),
    ("macro-sheer-vane", "square", "Material", "Sheer vane", "sheer-shades.html"),
    ("room-kitchen", "portrait", "Kitchen", "Faux wood blinds", "faux-wood-blinds.html"),
    ("style-modern-coastal", "landscape", "Coastal living", "Solar shades", "roller-solar-shades.html"),
    ("macro-wood-oak", "square", "Material", "White oak", "shutters.html"),
    ("room-nursery", "portrait", "Nursery", "Cordless cellular", "cellular-shades.html"),
    ("category-roman-shades", "landscape", "Dining room", "Roman shades", "roman-shades.html"),
    ("macro-cellular-bone", "square", "Material", "Cellular bone", "cellular-shades.html"),
    ("room-home-office", "portrait", "Home office", "Solar screen", "roller-solar-shades.html"),
    ("style-quiet-traditional", "landscape", "Sitting room", "Roman shades", "roman-shades.html"),
    ("macro-shutter-paint", "square", "Material", "Shutter paint", "shutters.html"),
    ("room-bathroom", "portrait", "Bathroom", "Faux wood blinds", "faux-wood-blinds.html"),
    ("category-dualdrape", "landscape", "Patio doors", "DualDrape\u2122", "dualdrape.html"),
    ("macro-linen-flax", "square", "Material", "Linen flax", "roman-shades.html"),
    ("category-sheer-shades", "landscape", "Living room", "Sheer shades", "sheer-shades.html"),
    ("macro-solar-5", "square", "Material", "5% solar screen", "roller-solar-shades.html"),
    ("category-vertical-blinds", "landscape", "Sliding door", "Vertical blinds", "vertical-blinds.html"),
    ("macro-faux-wood-white", "square", "Material", "Faux wood white", "faux-wood-blinds.html"),
]

# one editorial feature every nine tiles (§7.4)
GAL_FEATURES = {
    9: ("style-organic-modern", "Project", "Organic modern, north light",
        "A whole-floor scheme in three materials: woven flax at the tall windows, bone cellular "
        "in the bedrooms, and white oak shutters in the room that needed a fixture.",
        "Roller shades, cellular shades, shutters", "inspiration.html"),
    18: ("trade-hospitality-lounge", "Project", "Hospitality lounge, west facade",
         "A 5% solar screen on every west window, motorized in one group, so the room can be set "
         "for afternoon service without touching a single shade.",
         "Solar shades, TruQuiet\u2122 motorization", "for-professionals.html"),
}

GAL_FILTERS = [
    ("Product", ["Cellular", "Roller & solar", "Roman", "Faux wood", "Shutters", "Sheer", "Vertical"]),
    ("Room", ["Living room", "Bedroom", "Nursery", "Kitchen", "Bathroom", "Home office", "Patio doors"]),
    ("Style", ["Warm minimal", "Modern coastal", "Quiet traditional", "Organic modern"]),
    ("Light control", ["Keeps the view", "Light filtering", "Room darkening", "Blackout"]),
]
