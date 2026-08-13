"""Attribute tags and recommendation maps used by the interactive layer."""

# filterable attributes per product line
TAGS = {
    "cellular-shades":     ["cordless", "blackout", "motorized", "energy", "under50"],
    "roller-solar-shades": ["cordless", "blackout", "solar", "motorized", "energy", "under50"],
    "roman-shades":        ["cordless", "blackout", "motorized"],
    "faux-wood-blinds":    ["cordless", "moisture", "motorized", "under50"],
    "shutters":            ["cordless", "moisture", "patio", "energy"],
    "sheer-shades":        ["cordless", "solar", "motorized"],
    "dualdrape":           ["cordless", "patio"],
    "vertical-blinds":     ["cordless", "patio", "moisture"],
}

# chip label -> tag
CHIPS = [
    ("Cordless", "cordless"),
    ("Blackout", "blackout"),
    ("Solar screen", "solar"),
    ("Motorized", "motorized"),
    ("Patio door", "patio"),
    ("Moisture resistant", "moisture"),
    ("Energy efficient", "energy"),
    ("Under $50", "under50"),
]

# lines that hold up on openings 96" and wider
WIDE = {"vertical-blinds", "dualdrape", "shutters", "roller-solar-shades"}

ROOM = {
    "Living room": ["roller-solar-shades", "sheer-shades", "roman-shades"],
    "Bedroom": ["cellular-shades", "roman-shades", "roller-solar-shades"],
    "Nursery": ["cellular-shades", "sheer-shades", "roller-solar-shades"],
    "Kitchen": ["faux-wood-blinds", "roller-solar-shades", "vertical-blinds"],
    "Bathroom": ["faux-wood-blinds", "shutters", "vertical-blinds"],
    "Home office": ["roller-solar-shades", "sheer-shades", "cellular-shades"],
    "Dining room": ["roman-shades", "sheer-shades", "shutters"],
    "Patio door": ["vertical-blinds", "dualdrape", "shutters"],
    "Patio door or wide opening": ["vertical-blinds", "dualdrape", "shutters"],
    "Skylight": ["cellular-shades", "roller-solar-shades", "sheer-shades"],
    "Arched window": ["cellular-shades", "shutters", "sheer-shades"],
}

NEED = {
    "Block all light": ["cellular-shades", "roller-solar-shades", "roman-shades"],
    "Block all the light": ["cellular-shades", "roller-solar-shades", "roman-shades"],
    "Soften the light": ["sheer-shades", "cellular-shades", "roman-shades"],
    "Keep the view": ["roller-solar-shades", "shutters", "sheer-shades"],
    "Cut glare and heat": ["roller-solar-shades", "sheer-shades", "cellular-shades"],
    "Save energy": ["cellular-shades", "shutters", "faux-wood-blinds"],
    "Lower the energy bill": ["cellular-shades", "shutters", "faux-wood-blinds"],
    "Privacy": ["shutters", "cellular-shades", "faux-wood-blinds"],
    "Privacy without darkness": ["sheer-shades", "shutters", "cellular-shades"],
    "Child & pet safety": ["cellular-shades", "sheer-shades", "roller-solar-shades"],
    "Child and pet safety": ["cellular-shades", "sheer-shades", "roller-solar-shades"],
    "Moisture resistance": ["faux-wood-blinds", "vertical-blinds", "shutters"],
    "Handle humidity": ["faux-wood-blinds", "vertical-blinds", "shutters"],
    "Lowest price": ["roller-solar-shades", "faux-wood-blinds", "cellular-shades"],
}

LOOK = {
    "Clean and modern": ["roller-solar-shades", "cellular-shades"],
    "Soft folds": ["roman-shades", "sheer-shades"],
    "Natural wood": ["faux-wood-blinds", "shutters"],
    "Sheer and airy": ["sheer-shades", "dualdrape"],
    "Classic shutters": ["shutters", "faux-wood-blinds"],
}

LIFT = {
    "Cordless": ["cellular-shades", "roller-solar-shades", "roman-shades"],
    "Motorized": ["cellular-shades", "roller-solar-shades", "sheer-shades"],
    "No preference": [],
}
