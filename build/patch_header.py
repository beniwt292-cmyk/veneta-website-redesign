s = open('shell.py').read()

old = r'''def header(active=""):
    links = "".join(
        f'<a href="{u}"{" class=\"on\"" if k == active else ""}>{n}</a>' for n, u, k in NAV
    )'''

new = r'''PRODUCT_MENU = [
    ("Cellular Shades", "cellular-shades", "cellular-card.webp", "Insulating honeycomb"),
    ("Roller &amp; Solar", "roller-solar-shades", "roller-card.webp", "Clean, single sweep"),
    ("Roman Shades", "roman-shades", "roman-card.webp", "Soft fabric folds"),
    ("Faux Wood Blinds", "faux-wood-blinds", "fauxwood-card.webp", "Real wood look"),
    ("Shutters", "shutters", "shutters-card.webp", "Built in and permanent"),
    ("Sheer Shades", "sheer-shades", "sheer-card.webp", "Light through fabric"),
    ("DualDrape&trade;", "dualdrape", "dualdrape-card.webp", "Sheer to solid"),
    ("Vertical Blinds", "vertical-blinds", "vertical-card.webp", "Wide spans and sliders"),
]


def mega():
    tiles = "".join(
        '<a href="%s.html"><span class="mm-ph"><img src="assets/img/%s" alt="" loading="lazy"></span>'
        '<span class="mm-t">%s</span><span class="mm-d">%s</span></a>' % (sl, im, n, d)
        for n, sl, im, d in PRODUCT_MENU
    )
    return (
        '<div class="mm" role="group" aria-label="Products"><div class="mm-in">'
        '<div class="mm-grid">' + tiles + '</div>'
        '<div class="mm-side"><h4>Not sure where to start?</h4><ul>'
        '<li><a href="product-finder.html">Product finder, three questions</a></li>'
        '<li><a href="shop-by-room.html">Shop by room</a></li>'
        '<li><a href="shop-by-need.html">Shop by need</a></li>'
        '<li><a href="buying-guides.html">Buying guides</a></li>'
        '<li><a href="free-samples.html">Order free samples</a></li>'
        '</ul><a class="btn btn--ghost btn--sm" href="products.html">See all products</a>'
        '</div></div></div>'
    )


MAG = ('<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" fill="none" '
       'stroke="currentColor" stroke-width="1.6"><circle cx="10.5" cy="10.5" r="6.5"/>'
       '<path d="M15.5 15.5 21 21"/></svg>')

SEARCH_BTN = ('<button class="iconbtn" data-search-open aria-label="Search this site">'
              + MAG + '</button>')

SEARCH_PANEL = (
    '<div class="searchp" id="search" role="dialog" aria-modal="true" aria-label="Search this site">'
    '<div class="searchp-in"><div class="searchp-bar">' + MAG +
    '<input id="search-q" type="search" placeholder="Search products, guides and support" '
    'autocomplete="off" aria-label="Search">'
    '<button class="searchp-x" data-search-close aria-label="Close search">&times;</button></div>'
    '<div class="searchp-res" id="search-res"></div>'
    '<p class="searchp-hint">Press <kbd>Esc</kbd> to close</p>'
    '</div></div>'
)


def header(active=""):
    parts = []
    for n, u, k in NAV:
        cls = ' class="on"' if k == active else ""
        if k == "products":
            parts.append('<div class="hasmenu"><a href="%s"%s aria-expanded="false">%s</a>%s</div>'
                         % (u, cls, n, mega()))
        else:
            parts.append('<a href="%s"%s>%s</a>' % (u, cls, n))
    links = "".join(parts)'''

assert old in s, "header def not found"
s = s.replace(old, new)

old2 = r'''    <div class="hd-wrap"><a class="btn btn--hd btn--sm" href="{HD}" data-analytics="hd-outbound" data-location="header">Shop at The Home Depot</a></div>
    <button class="burger"'''
new2 = r'''    <div class="hd-wrap">{SEARCH_BTN}<a class="btn btn--hd btn--sm" href="{HD}" data-analytics="hd-outbound" data-location="header">Shop at The Home Depot</a></div>
    <button class="iconbtn m-only" data-search-open aria-label="Search this site">{MAG}</button>
    <button class="burger"'''
assert old2 in s, "hd-wrap not found"
s = s.replace(old2, new2)

old3 = '<main id="main">\n"""'
new3 = '{SEARCH_PANEL}\n<main id="main">\n"""'
assert old3 in s, "main not found"
s = s.replace(old3, new3)

open('shell.py', 'w').write(s)
print("header patched")
