#!/usr/bin/env python3
"""§6.4 technical SEO layer.

Everything here is applied as a post-process inside build_site.write(), so a page
gains canonical + Open Graph + JSON-LD purely by existing. There is nothing to
remember to add at the 50 call sites, and nothing to keep in sync by hand.

Machine-derived from the rendered HTML:
  - BreadcrumbList  from the <p class="crumb"> trail every non-home page renders
  - FAQPage         from every <div class="acc"> details/summary pair
Hand-authored here (small, high-value, must match page copy exactly):
  - Organization + WebSite on /
  - Product on the eight category pages and the DualDrape family page
  - HowTo on measure / install / clean

PRODUCTION is the single switch between "mockup deploy" and "live site". While it
is False every page keeps its noindex and robots.txt disallows everything, but the
canonical, Open Graph and structured data are already complete and correct.
"""
import html as _html
import json
import os
import re

SITE = "https://www.venetawindowfashions.com"
HD = "https://www.homedepot.com/b/VENETA/N-5yc1vZryk"
PRODUCTION = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ URLs

def url_for(name):
    """vercel.json sets cleanUrls + trailingSlash:false, so canonicals are extensionless."""
    slug = name[:-5] if name.endswith(".html") else name
    return SITE + "/" if slug == "index" else SITE + "/" + slug


# ------------------------------------------------------------------ social cards
# Card ids resolve to assets/img/<id>-1200.webp, cropped from accepted P1 heroes
# by `python3 build/images.py og`. Keep OG_CARDS in step with p1_manifest.og.
OG_CARDS = {
    "og-home": "hero-home",
    "og-products": "category-cellular-shades",
    "og-cellular-shades": "category-cellular-shades",
    "og-roller-solar-shades": "category-roller-solar-shades",
    "og-roman-shades": "category-roman-shades",
    "og-faux-wood-blinds": "category-faux-wood-blinds",
    "og-shutters": "category-shutters",
    "og-sheer-shades": "category-sheer-shades",
    "og-dualdrape": "category-dualdrape",
    "og-vertical-blinds": "category-vertical-blinds",
    "og-motorization": "motor-dusk-bedroom",
    "og-child-safety": "safety-nursery-cordless",
    "og-rooms": "room-living-room",
    "og-need": "room-bedroom",
    "og-inspiration": "style-warm-minimal",
    "og-guides": "style-quiet-traditional",
    "og-support": "room-home-office",
    "og-innovation": "motor-living-wall",
    "og-trade": "trade-office-open",
    "og-commercial": "trade-commercial-lobby",
    "og-journal": "style-modern-coastal",
    "og-samples": "macro-linen-flax",
    "og-company": "style-organic-modern",
}

OG_PAGE = {
    "index.html": "og-home",
    "products.html": "og-products",
    "cellular-shades.html": "og-cellular-shades",
    "roller-solar-shades.html": "og-roller-solar-shades",
    "roman-shades.html": "og-roman-shades",
    "faux-wood-blinds.html": "og-faux-wood-blinds",
    "shutters.html": "og-shutters",
    "sheer-shades.html": "og-sheer-shades",
    "dualdrape.html": "og-dualdrape",
    "vertical-blinds.html": "og-vertical-blinds",
    "shop-by-room.html": "og-rooms",
    "shop-by-need.html": "og-need",
    "need-blackout.html": "og-need",
    "need-light-filtering.html": "og-need",
    "need-privacy.html": "og-need",
    "need-energy-efficiency.html": "og-need",
    "need-patio-doors.html": "og-need",
    "room-bedroom.html": "og-rooms",
    "room-living-room.html": "og-rooms",
    "room-kitchen.html": "og-rooms",
    "room-bathroom.html": "og-rooms",
    "room-home-office.html": "og-rooms",
    "room-nursery.html": "og-rooms",
    "style-modern-minimal.html": "og-inspiration",
    "style-warm-organic.html": "og-company",
    "style-coastal.html": "og-journal",
    "style-classic-tailored.html": "og-shutters",

    "product-finder.html": "og-need",
    "inspiration.html": "og-inspiration",
    "journal.html": "og-journal",
    "journal-beat-summer-heat.html": "og-cellular-shades",
    "journal-bellevue-coastal-colors.html": "og-inspiration",
    "journal-faux-wood-decor.html": "og-faux-wood-blinds",
    "journal-gray-is-the-new-white.html": "og-journal",
    "journal-spring-cleaning.html": "og-company",
    "buying-guides.html": "og-guides",
    "cordless-roller-shades-guide.html": "og-roller-solar-shades",
    "faux-wood-guide.html": "og-faux-wood-blinds",
    "roman-cordless-guide.html": "og-roman-shades",
    "support.html": "og-support",
    "how-to-measure.html": "og-support",
    "how-to-install.html": "og-support",
    "how-to-clean.html": "og-support",
    "installation-videos.html": "og-support",
    "installation-videos-l-frame.html": "og-shutters",
    "installation-videos-deco-frame.html": "og-shutters",
    "faq.html": "og-support",
    "contact.html": "og-support",
    "warranty.html": "og-support",
    "innovation.html": "og-innovation",
    "motorization.html": "og-motorization",
    "truquiet-motorization.html": "og-motorization",
    "smartrail.html": "og-innovation",
    "smartprivacy.html": "og-innovation",
    "clearfit.html": "og-innovation",
    "child-safety.html": "og-child-safety",
    "for-professionals.html": "og-trade",
    "for-professionals-resources.html": "og-trade",
    "commercial.html": "og-commercial",
    "commercial-spec-library.html": "og-commercial",
    "blinds-vs-shades-vs-shutters.html": "og-guides",
    "free-samples.html": "og-samples",
    "where-to-buy.html": "og-products",
    "about.html": "og-company",
    "sitemap.html": "og-company",
    "accessibility.html": "og-company",
    "privacy-policy.html": "og-company",
    "terms-and-conditions.html": "og-company",
    "404.html": "og-company",
}

OG_ALT = {
    "og-home": "A sunlit living room with Veneta cellular shades lowered to the sill.",
    "og-products": "Eight Veneta product lines shown across a range of rooms.",
    "og-cellular-shades": "Veneta cellular shades in a bedroom, honeycomb cells lit from behind.",
    "og-roller-solar-shades": "A Veneta solar shade filtering afternoon glare in a home office.",
    "og-roman-shades": "A Veneta Roman shade in flax linen, folds stacked evenly.",
    "og-faux-wood-blinds": "Veneta faux wood blinds in a bathroom, slats tilted half open.",
    "og-shutters": "Veneta plantation shutters framing a traditional window.",
    "og-sheer-shades": "Veneta sheer shades with vanes tilted between two layers of sheer.",
    "og-dualdrape": "Veneta DualDrape on a patio door, stacked to one side.",
    "og-vertical-blinds": "Veneta vertical blinds on a wide slider, louvres angled to the room.",
    "og-motorization": "A bedroom at dusk with Veneta TruQuiet motorised shades closing.",
    "og-child-safety": "A nursery with cordless Veneta shades and no operating cords.",
    "og-rooms": "A living room styled with Veneta window treatments.",
    "og-need": "A darkened bedroom showing blackout performance at the window.",
    "og-inspiration": "A warm minimal interior with Veneta shades in a neutral fabric.",
    "og-guides": "A quiet traditional room used to illustrate the Veneta buying guides.",
    "og-support": "A home office window, used to illustrate measuring and installation.",
    "og-innovation": "A living room wall of Veneta motorised shades moving in unison.",
    "og-trade": "An open-plan office fitted with Veneta commercial solar shades.",
    "og-commercial": "A commercial lobby with Veneta solar shades on a tall glazed elevation.",
    "og-journal": "A modern coastal interior from the Veneta journal.",
    "og-samples": "A macro photograph of flax linen shade fabric.",
    "og-company": "An organic modern interior representing Veneta Window Fashions.",
}


def og_image(name):
    card = OG_PAGE.get(name, "og-home")
    path = "assets/img/%s-1200.jpg" % card
    if not os.path.exists(os.path.join(ROOT, path)):
        card, path = "og-home", "assets/img/og-home-1200.jpg"
    return SITE + "/" + path, OG_ALT.get(card, "Veneta Window Fashions")


# ------------------------------------------------------------------ text helpers

def txt(s):
    """Rendered HTML fragment -> plain text safe to drop into JSON-LD."""
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"</(p|li|h[1-6]|div)>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = _html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def ld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
            + "</script>")


# ------------------------------------------------------------------ derived blocks

def breadcrumbs(name, page_html):
    """BreadcrumbList from the crumb trail the page already renders."""
    m = re.search(r'<p class="crumb">(.*?)</p>', page_html, re.S)
    if not m:
        return None
    items, pos = [], 0
    for part in re.split(r"<span>/</span>", m.group(1)):
        part = part.strip()
        if not part:
            continue
        pos += 1
        a = re.match(r'<a href="([^"]+)"[^>]*>(.*?)</a>\s*$', part, re.S)
        if a:
            items.append({"@type": "ListItem", "position": pos,
                          "name": txt(a.group(2)), "item": url_for(a.group(1))})
        else:
            items.append({"@type": "ListItem", "position": pos, "name": txt(part)})
    if len(items) < 2:
        return None
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}


def faqpage(page_html):
    """FAQPage from every details/summary pair inside an .acc block."""
    qa = []
    for m in re.finditer(r"<details[^>]*>\s*<summary>(.*?)</summary>"
                         r'\s*<div class="a">(.*?)</div>\s*</details>', page_html, re.S):
        q, a = txt(m.group(1)), txt(m.group(2))
        if q and a:
            qa.append({"@type": "Question", "name": q,
                       "acceptedAnswer": {"@type": "Answer", "text": a}})
    if len(qa) < 2:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa}


# ------------------------------------------------------------------ authored blocks

ORGANIZATION = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": "VENETA Window Fashions",
    "legalName": "Richfield Window Coverings",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/veneta-logo.png",
             "width": 512, "height": 512},
    "description": ("Custom blinds, shades and shutters engineered to fit, cordless by "
                    "design, sold through The Home Depot."),
    "contactPoint": [{
        "@type": "ContactPoint",
        "telephone": "+1-855-558-1222",
        "contactType": "customer support",
        "areaServed": ["US", "CA"],
        "availableLanguage": ["en"],
        "hoursAvailable": {"@type": "OpeningHoursSpecification",
                           "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                           "opens": "08:00", "closes": "18:00"},
    }],
    "sameAs": [
        "https://www.homedepot.com/b/VENETA/N-5yc1vZryk",
        "https://www.facebook.com/venetawindowfashions",
        "https://www.instagram.com/venetawindowfashions",
        "https://www.pinterest.com/venetawindowfashions",
        "https://www.youtube.com/@venetawindowfashions",
    ],
}

WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "url": SITE + "/",
    "name": "VENETA Window Fashions",
    "publisher": {"@id": SITE + "/#organization"},
    "inLanguage": "en-US",
}

# Spec labels worth promoting into Product.additionalProperty, in this order.
SPEC_KEYS = ["Opacity", "Operation", "Lift options", "Width range", "Height range",
             "Minimum mount depth", "Cell type", "Slat size", "Louvre size",
             "Fold style", "Vane size", "Louvre width", "Best for", "Warranty"]

def _shot_webp(shot_id):
    """Path to an accepted P1 shot's webp, or None if it has not shipped."""
    try:
        with open(os.path.join(ROOT, "docs", "p1-manifest.json")) as f:
            doc = json.load(f)
    except FileNotFoundError:
        return None
    for s in doc.get("shots", []):
        if s["id"] == shot_id:
            path = s["files"]["webp"]
            return path if os.path.exists(os.path.join(ROOT, path)) else None
    return None


MATERIALS = {
    "cellular-shades": ["Spunlace non-woven", "Honeycomb fabric"],
    "roller-solar-shades": ["Vinyl-coated polyester mesh", "Woven solar screen"],
    "roman-shades": ["Linen", "Cotton blend", "Drapery fabric"],
    "faux-wood-blinds": ["PVC composite", "Moisture-resistant polymer"],
    "shutters": ["Engineered hardwood", "Polymer-coated MDF"],
    "sheer-shades": ["Sheer knit facing", "Fabric vane"],
    "dualdrape": ["Sheer knit facing", "Room-darkening vane"],
    "vertical-blinds": ["Vinyl louvre", "Fabric-insert louvre"],
}


def product_ld(p):
    props = []
    spec = {k: v for k, v in p.get("spec", [])}
    for k in SPEC_KEYS:
        if k in spec:
            props.append({"@type": "PropertyValue", "name": k, "value": txt(spec[k])})
    img = _shot_webp("category-" + p["slug"]) or ("assets/img/" + p["hero"])
    obj = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Veneta Custom " + txt(p["name"]),
        "brand": {"@type": "Brand", "name": "VENETA"},
        "category": txt(p["name"]),
        "description": txt(p["lede"]),
        "image": [SITE + "/" + img],
        "url": url_for(p["slug"]),
        "isRelatedTo": {"@id": SITE + "/#organization"},
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "priceCurrency": "USD",
            "url": HD,
            "seller": {"@type": "Organization", "name": "The Home Depot"},
        },
    }
    if p["slug"] in MATERIALS:
        obj["material"] = MATERIALS[p["slug"]]
    if props:
        obj["additionalProperty"] = props
    return obj


HOWTO = {
    "how-to-measure.html": {
        "@context": "https://schema.org", "@type": "HowTo",
        "name": "How to measure a window for blinds and shades",
        "description": ("Measure the exact opening size for an inside or outside mount and "
                        "let the factory make the deductions."),
        "totalTime": "PT10M",
        "url": SITE + "/how-to-measure",
        "tool": [{"@type": "HowToTool", "name": "Steel tape measure"},
                 {"@type": "HowToTool", "name": "Pencil and paper"}],
        "step": [
            {"@type": "HowToStep", "name": "Decide inside or outside mount",
             "url": SITE + "/how-to-measure#mount",
             "text": ("Inside mount sits within the window frame and needs enough depth: 3/4 inch "
                      "for a cellular shade, 2 inches for faux wood, 2 1/2 inches for a Roman or "
                      "sheer shade. Choose outside mount when the frame is too shallow, out of "
                      "square, or when you want maximum darkness.")},
            {"@type": "HowToStep", "name": "Measure the width in three places",
             "url": SITE + "/how-to-measure#width",
             "text": ("Measure the top, middle and bottom of the opening. For an inside mount use "
                      "the narrowest of the three. For an outside mount use the widest and add "
                      "2 inches on each side for overlap.")},
            {"@type": "HowToStep", "name": "Measure the height in three places",
             "url": SITE + "/how-to-measure#height",
             "text": ("Measure the left, centre and right. For an inside mount use the longest of "
                      "the three so the shade reaches the sill everywhere. For an outside mount "
                      "measure from the headrail position down, plus 2 inches below the opening.")},
            {"@type": "HowToStep", "name": "Write it down width first",
             "url": SITE + "/how-to-measure#order",
             "text": ("Record width by height to the nearest 1/8 inch, never height first. Submit "
                      "the exact opening size and do not deduct anything; clearance is applied at "
                      "the factory.")},
        ],
    },
    "how-to-install.html": {
        "@context": "https://schema.org", "@type": "HowTo",
        "name": "How to install blinds and shades",
        "description": ("Six steps that apply to every product in the Veneta range, from "
                        "unpacking to the final test."),
        "totalTime": "PT20M",
        "url": SITE + "/how-to-install",
        "tool": [{"@type": "HowToTool", "name": "Cordless drill"},
                 {"@type": "HowToTool", "name": "Spirit level"},
                 {"@type": "HowToTool", "name": "Pencil"}],
        "step": [
            {"@type": "HowToStep", "name": "Unpack and check",
             "text": ("Confirm the width and height against your order before you make a hole. "
                      "Check the box for brackets, valance clips and the wand or remote.")},
            {"@type": "HowToStep", "name": "Mark the bracket positions",
             "text": ("Hold the headrail in the opening and mark through the bracket slots. On an "
                      "inside mount the brackets go at the top of the opening, flush with the "
                      "front edge unless the instructions say otherwise.")},
            {"@type": "HowToStep", "name": "Check level, then drill",
             "text": ("A shade 1/8 inch out of level will show a wedge of light at the sill. Use a "
                      "spirit level as your reference, not the window frame.")},
            {"@type": "HowToStep", "name": "Fit the brackets",
             "text": ("Pilot-drill into timber and use the supplied anchors in drywall. Snug, not "
                      "overtightened; composite brackets crack under a driver.")},
            {"@type": "HowToStep", "name": "Clip in the headrail",
             "text": ("Push the headrail up and back until both brackets click, then tug gently "
                      "down to confirm it is seated.")},
            {"@type": "HowToStep", "name": "Fit the valance and test",
             "text": ("Clip the valance, then raise and lower the shade fully twice. Anything that "
                      "binds is a bracket alignment problem, not a fabric problem.")},
        ],
    },
}

# how-to-clean is authored separately because its steps are material-specific.
HOWTO["how-to-clean.html"] = {
    "@context": "https://schema.org", "@type": "HowTo",
    "name": "How to clean and care for blinds and shades",
    "description": ("Routine cleaning by material, from cellular fabric to shutters, plus a "
                    "seasonal maintenance pass."),
    "totalTime": "PT15M",
    "url": SITE + "/how-to-clean",
    "tool": [{"@type": "HowToTool", "name": "Vacuum with brush attachment"},
             {"@type": "HowToTool", "name": "Microfibre cloth"},
             {"@type": "HowToTool", "name": "Lambswool duster"}],
    "step": [
        {"@type": "HowToStep", "name": "Dust before you ever wash",
         "text": ("Dust regularly with a lambswool duster or a vacuum brush attachment on the "
                  "lowest suction. Most coverings never need more than this.")},
        {"@type": "HowToStep", "name": "Spot clean fabric shades",
         "text": ("On cellular, Roman and sheer shades, blot a mark with a barely damp cloth and "
                  "plain water. Never rub, never soak, and never submerge a fabric shade.")},
        {"@type": "HowToStep", "name": "Wipe hard materials down",
         "text": ("Faux wood, vinyl verticals and shutters take a damp microfibre cloth with mild "
                  "soap. Dry immediately so water does not sit in the slat joints.")},
        {"@type": "HowToStep", "name": "Run a seasonal check",
         "text": ("Twice a year, dust the headrail, check bracket screws are tight, and cycle "
                  "every shade fully to keep the lift system running smoothly.")},
    ],
}


# ------------------------------------------------------------------ injection

ROBOTS_LIVE = "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
ROBOTS_MOCK = "noindex,nofollow"

_PRODUCTS = None


def _products():
    global _PRODUCTS
    if _PRODUCTS is None:
        import data as D
        _PRODUCTS = {p["slug"]: p for p in D.PRODUCTS}
    return _PRODUCTS


def inject(name, page_html):
    url = url_for(name)
    slug = name[:-5] if name.endswith(".html") else name
    title = re.search(r"<title>(.*?)</title>", page_html, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', page_html, re.S)
    og_t = _html.escape(txt(title.group(1)) if title else "VENETA Window Fashions", quote=True)
    og_d = _html.escape(txt(desc.group(1)) if desc else "", quote=True)
    img, alt = og_image(name)

    page_html = page_html.replace(
        '<meta name="robots" content="noindex,nofollow">',
        '<meta name="robots" content="%s">' % (ROBOTS_LIVE if PRODUCTION else ROBOTS_MOCK))

    meta = [
        '<link rel="canonical" href="%s">' % url,
        '<meta property="og:type" content="%s">' % ("website" if slug == "index" else "article"),
        '<meta property="og:site_name" content="VENETA Window Fashions">',
        '<meta property="og:locale" content="en_US">',
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % og_t,
        '<meta property="og:description" content="%s">' % og_d,
        '<meta property="og:image" content="%s">' % img,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:type" content="image/jpeg">',
        '<meta property="og:image:alt" content="%s">' % _html.escape(alt, quote=True),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % og_t,
        '<meta name="twitter:description" content="%s">' % og_d,
        '<meta name="twitter:image" content="%s">' % img,
        '<meta name="twitter:image:alt" content="%s">' % _html.escape(alt, quote=True),
    ]

    blocks = []
    if slug == "index":
        blocks += [ORGANIZATION, WEBSITE]
    b = breadcrumbs(name, page_html)
    if b:
        blocks.append(b)
    if slug in _products():
        blocks.append(product_ld(_products()[slug]))
    f = faqpage(page_html)
    if f:
        blocks.append(f)
    if name in HOWTO:
        blocks.append(HOWTO[name])

    head_add = "\n".join(meta) + "\n" + "\n".join(ld(x) for x in blocks) + "\n"
    page_html = page_html.replace("</head>", head_add + "</head>", 1)

    # §6.4: the Home Depot handoff is the intended retail path, so these links are
    # followed. New tab + noopener, never nofollow or sponsored.
    page_html = re.sub(r'(<a\b(?![^>]*\btarget=)[^>]*\bhref="https://www\.homedepot\.com[^"]*")',
                       r'\1 target="_blank" rel="noopener"', page_html)
    return page_html


# ------------------------------------------------------------------ sitemap + robots

# Priority / change frequency by role, highest first.
PRI = [
    (["index.html"], "1.0", "weekly"),
    (["products.html", "shop-by-room.html", "shop-by-need.html", "product-finder.html"],
     "0.9", "weekly"),
    ([p + ".html" for p in ("cellular-shades", "roller-solar-shades", "roman-shades",
                            "faux-wood-blinds", "shutters", "sheer-shades", "dualdrape",
                            "vertical-blinds")], "0.9", "weekly"),
    (["inspiration.html", "buying-guides.html", "support.html", "how-to-measure.html",
      "how-to-install.html", "how-to-clean.html", "free-samples.html",
      "where-to-buy.html", "innovation.html", "motorization.html", "child-safety.html",
      "blinds-vs-shades-vs-shutters.html", "commercial.html"],
     "0.8", "monthly"),
    ([f"need-{n}.html" for n in ("blackout", "light-filtering", "privacy",
                                 "energy-efficiency", "patio-doors")]
     + [f"room-{r}.html" for r in ("bedroom", "living-room", "kitchen", "bathroom",
                                   "home-office", "nursery")],
     "0.8", "monthly"),
    ([f"style-{t}.html" for t in ("modern-minimal", "warm-organic", "coastal",
                                  "classic-tailored")], "0.7", "monthly"),
]
NOINDEX_PAGES = {"404.html"}


def _rank(name):
    for group, pri, freq in PRI:
        if name in group:
            return pri, freq
    if name.startswith("journal"):
        return "0.6", "monthly"
    if name in ("privacy-policy.html", "terms-and-conditions.html", "accessibility.html",
                "warranty.html", "sitemap.html"):
        return "0.3", "yearly"
    return "0.7", "monthly"


def write_sitemap(names, lastmod=None):
    import datetime
    lastmod = lastmod or datetime.date.today().isoformat()
    rows = []
    for n in sorted(names):
        if n in NOINDEX_PAGES:
            continue
        pri, freq = _rank(n)
        rows.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
                    "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
                    % (url_for(n), lastmod, freq, pri))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)

    if PRODUCTION:
        txt_ = ("User-agent: *\nAllow: /\n\n"
                "Sitemap: %s/sitemap.xml\n" % SITE)
    else:
        txt_ = ("# Redesign mockup. Nothing here should be indexed until it replaces the\n"
                "# live site. Flip PRODUCTION in build/seo.py to open it up.\n"
                "User-agent: *\nDisallow: /\n\n"
                "Sitemap: %s/sitemap.xml\n" % SITE)
    open(os.path.join(ROOT, "robots.txt"), "w").write(txt_)
    return len(rows)
