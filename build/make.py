#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_site as S
import pages2 as P2
import pages3 as P3
import data as D

S.build_assets()
S.build_home()
S.build_products()
for p in D.PRODUCTS:
    S.build_pdp(p)
S.build_shop_by()
P2.build_innovation()
P2.build_support()
P2.build_videos()
P3.build_policies()
P3.build_guides()
P3.build_inspiration()
P3.build_company()
P3.build_legal()
P3.build_utility()

S.build_search_index()

print("pages written:", len(S.written))
for n in sorted(S.written):
    print("  ", n)
