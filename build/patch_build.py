import json
import re

s = open('build_site.py').read()

# ---------------------------------------------------------------- assets
old = '''    css = "".join(open(os.path.join(B, f)).read() for f in ("base.css", "extra.css", "luxe.css"))
    open(os.path.join(ROOT, "assets/css/veneta.css"), "w").write(css)'''
new = '''    css = "".join(open(os.path.join(B, f)).read() for f in ("base.css", "extra.css", "luxe.css"))
    open(os.path.join(ROOT, "assets/css/veneta.css"), "w").write(css)'''
assert old in s

# append interactive.js (with injected data) to the js bundle
tgt = '    open(os.path.join(ROOT, "assets/js/veneta.js"), "w").write(js.strip() + "\\n")'
assert tgt in s, "js write not found"
s = s.replace(tgt, '    js = js.strip() + "\\n" + interactive_js()\n' + tgt.replace('js.strip() + "\\n"', "js"))

# ---------------------------------------------------------------- helpers
helpers = '''

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
        title = re.sub(r"\\s*\\|.*$", "", t.group(1))
        title = re.sub(r"\\s*&mdash;.*$", "", title).strip()
        desc = (d.group(1) if d else "").strip()
        out.append({"t": unes(title), "d": unes(desc), "u": name})
    out.sort(key=lambda r: (priority.index(r["u"]) if r["u"] in priority else 99, r["t"]))
    js = "window.VENETA_INDEX=" + json.dumps(out, separators=(",", ":")) + ";"
    open(os.path.join(ROOT, "assets/js/search-index.js"), "w").write(js)


def unes(x):
    for a, b in (("&amp;", "&"), ("&mdash;", "\\u2014"), ("&trade;", "\\u2122"),
                 ("&reg;", "\\u00ae"), ("&middot;", "\\u00b7"), ("&quot;", '"'),
                 ("&ndash;", "\\u2013"), ("&#39;", "'")):
        x = x.replace(a, b)
    return x
'''
s = s.replace("\n# ---------------------------------------------------------------- products index",
              helpers + "\n# ---------------------------------------------------------------- products index", 1)

if "import json" not in s:
    s = s.replace("import os, re", "import json, os, re", 1)
if "import json" not in s:
    s = "import json\n" + s

# ---------------------------------------------------------------- products page filters
old_chips = '''    chips = "".join(f'<button class="chip" aria-pressed="false">{c}</button>' for c in
                    ["Cordless", "Blackout", "Solar screen", "Motorized", "Patio door", "Moisture resistant", "Energy efficient", "Under $50"])'''
new_chips = '''    import interactive_data as I
    chips = "".join(f'<button class="chip" type="button" aria-pressed="false" data-tag="{t}">{c}</button>'
                    for c, t in I.CHIPS)'''
assert old_chips in s
s = s.replace(old_chips, new_chips)

old_grid = '''      {shead('Filter', 'Narrow it down.', 'Mockup filters are illustrative. In build, these map to real product attributes and update the grid without a page reload.')}
      <div class="chips">{chips}</div>
      <div style="margin-top:52px">{cards(D.card_tuples())}</div>'''
new_grid = '''      {shead('Filter', 'Narrow it down.', 'Pick the attributes that matter. The grid updates instantly, no page reload.')}
      <div class="chips" data-filter>{chips}</div>
      <div class="filter-bar">
        <p id="filter-count" aria-live="polite">All 8 products</p>
        <button class="arrow" type="button" id="filter-reset" hidden>Clear filters</button>
      </div>
      <div id="filter-grid" data-empty="No single product does all of that. Try clearing one filter, or use the product finder.">{cards(D.card_tuples())}</div>'''
assert old_grid in s
s = s.replace(old_grid, new_grid)

# ---------------------------------------------------------------- finder page
old_form = '''          <form class="form" data-mock style="max-width:none">'''
new_form = '''          <form class="form" id="pf-form" style="max-width:none">'''
assert old_form in s
s = s.replace(old_form, new_form)

old_sub = '''            <div class="full"><button class="btn" type="submit">Show my recommendations</button>
              <p class="mockmsg hint" hidden style="margin-top:12px;color:var(--success)">Mockup only: in the built site this returns a ranked shortlist with reasons, plus a note on what will not work at this size.</p></div>'''
new_sub = '''            <div class="full"><button class="btn" type="submit">Show my recommendations</button></div>'''
assert old_sub in s
s = s.replace(old_sub, new_sub)

old_ex = '''          <div style="margin-top:56px">
            {shead('Example result', 'What a recommendation looks like.', 'Bedroom &middot; block all the light &middot; 36&quot; &times; 60&quot; &middot; cordless')}
            {cards(D.card_tuples(["cellular-shades", "roller-solar-shades", "roman-shades"]))}
            <div class="callout"><p><strong>What we would not fit here:</strong> a solar screen. At night a lit room is visible through any screen fabric, so it is the wrong product for a bedroom even at 1% openness.</p></div>
          </div>'''
new_ex = '''          <div class="fout" id="pf-out" style="margin-top:56px">
            {shead('Your shortlist', 'Living room &middot; block all the light')}
            {cards(D.card_tuples(["cellular-shades", "roller-solar-shades", "roman-shades"]))}
          </div>
          <div class="callout" style="margin-top:28px"><p><strong>What we will tell you not to buy:</strong> a solar screen for a bedroom. At night a lit room is visible through any screen fabric, so it is the wrong product even at 1% openness.</p></div>'''
assert old_ex in s
s = s.replace(old_ex, new_ex)

open('build_site.py', 'w').write(s)
print("build_site patched")
