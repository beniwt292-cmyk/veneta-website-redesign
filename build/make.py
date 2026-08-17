#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_site as S
import pages2 as P2
import pages3 as P3
import pages5 as P5
import pages6 as P6
import p2 as P2T
import data as D
import seo as SEO

# P2 (§7) owns home, the eight category pages, the DualDrape product family and
# the inspiration gallery. Everything still on the P0 templates is listed below it.
S.build_assets()
P2T.build_home(S.write, S.page)
S.build_products()
for p in D.PRODUCTS:
    if p["slug"] == "dualdrape":
        P2T.build_family(p, S.write, S.page)
    else:
        P2T.build_category(p, S.write, S.page)
S.build_shop_by()
P2.build_innovation()
P2.build_support()
P2.build_videos()
P3.build_policies()
P3.build_guides()
P3.build_inspiration()
P2T.build_gallery(S.write, S.page)   # §7.4 replaces the P0 inspiration template
P3.build_company()
P3.build_legal()
P5.build_all()   # §7.6 commercial, spec library, trade resources, comparison
P6.build_all()   # §5.2 need, room and style decision pages
P3.build_utility()

S.build_search_index()
urls = SEO.write_sitemap(S.written)

print("pages written:", len(S.written))
print("sitemap urls:", urls, "| robots.txt:", "index" if SEO.PRODUCTION else "noindex (mockup)")
for n in sorted(S.written):
    print("  ", n)
