# Redesign Strategy — VENETA™ Window Fashions

## 1. The core strategic decision

Veneta does not sell online. Home Depot does. Every design decision must follow from that.

**Therefore the site's job is:** turn an unsure shopper into a confident buyer, then hand them off to Home Depot at the exact moment of confidence, and measure that handoff.

That reframes the site from "brand brochure" to **decision engine**. Everything on the new site either builds confidence or removes friction.

## 2. Positioning

> **Veneta™ makes custom window treatments you can actually choose with confidence: safe by design, engineered to fit, available at The Home Depot.**

Three pillars, in priority order:

1. **Engineered to fit** — real dimensions, real mount depths, real specs, published openly. Veneta already documents this better than the category leaders; make it the hero.
2. **Safe by design** — cordless-first, tested for homes with kids and pets. This is a genuine differentiator, currently buried as a generic icon.
3. **Effortless living** — cordless and motorized systems (TruQuiet™, ShadeAuto™, RevitaCharge™) that make daily life easier.

## 3. Audience segments and their jobs

| Segment | Their question | What the site must give them |
|---|---|---|
| First-time custom buyer (largest) | "Will I get this wrong?" | Product Finder, measuring guide, fit guarantee language, clear next step |
| Renovator / room-by-room shopper | "What works in my kitchen / nursery / patio door?" | Shop by Room, Shop by Need |
| Spec-driven shopper | "Does it fit my 108-inch slider / skylight / French door?" | Visible spec tables, dimension ranges, mount depth, spec book download |
| Parent / pet owner | "Is it safe?" | Dedicated Cordless & Safety page with certification detail |
| Trade (designer, builder, PM) | "Can I spec this at volume?" | Pro hub, spec sheets, warranty terms, contact route |
| Existing owner | "How do I clean / fix / claim warranty?" | Support hub, care guides, parts, warranty claim path |

## 4. Design direction

**Concept: "Editorial Daylight."**

The subject is light. The design should feel like a well-lit room in an architecture magazine: generous white space, large calm photography, thin precise rules, and confident editorial typography. Not a big-box retail site, not a purple-gradient tech site.

Principles:

- **Photography leads, UI recedes.** Full-bleed room imagery with real text on top, never text baked into JPEGs.
- **Light as the visual motif.** Soft directional gradients, warm neutral backgrounds, subtle slat/louver-inspired line patterns used sparingly as dividers and section markers.
- **Specs deserve beautiful typography too.** Spec tables should look intentional, not like leftover data.
- **One clear action per screen.** Every viewport has an obvious next step.
- **Yellow is the accent, not the theme.** The logo's yellow becomes a precise highlight (active states, key CTAs, small underlines), never a large fill.
- **Motion is restrained.** Fades and 200-300 ms transitions on reveal and hover. No carousel auto-rotation. No parallax.

Explicitly rejected: auto-rotating hero carousels, text-in-image banners, tabbed product content, stock-photo "happy family" imagery, generic icon rows with vague nouns.

## 5. Information architecture (new)

```
Home
│
├── Products
│   ├── Cellular Shades        (+ ClearFit™, Day & Night)
│   ├── Roller & Solar Shades  (+ Cordless Roller)
│   ├── Roman Shades           (+ Cordless Roman)
│   ├── Faux Wood Blinds       (+ SmartRail™, SmartPrivacy®)
│   ├── Shutters
│   ├── Sheer Shades
│   ├── DualDrape™
│   └── Vertical Blinds
│
├── Shop By
│   ├── Room            (Living, Bedroom, Nursery, Kitchen, Bath, Office, Patio Doors, Skylights, Arches)
│   ├── Need            (Blackout, Light Filtering, Insulation, Privacy, UV Protection, Child & Pet Safe, Oversized Windows)
│   └── Product Finder  (guided 3-step tool)
│
├── Innovation
│   ├── Cordless & Family Safety
│   ├── Motorization & Smart Home  (ShadeAuto™ Hub, TruQuiet™, RevitaCharge™)
│   ├── ClearFit™
│   ├── SmartRail™ & SmartPrivacy®
│   └── Energy Efficiency
│
├── Inspiration
│   ├── Room Galleries
│   ├── Color & Trend Guides
│   └── Journal (relaunched blog)
│
├── Support
│   ├── How to Measure
│   ├── How to Install
│   ├── How to Clean & Care
│   ├── Warranty
│   ├── FAQ (searchable, consolidated)
│   ├── Spec Book & Downloads
│   └── Contact Us  (1-855-558-1222 · help@venetawindowfashions.com)
│
├── Where to Buy   (Home Depot online + in-store, sample ordering)
├── For Professionals
└── About Veneta   (Richfield Window Coverings, manufacturing, awards, accessibility statement)
```

Header: `Logo | Products | Shop By | Innovation | Support | [Search] | Where to Buy | ▸ Shop at The Home Depot`
The Home Depot button is the only filled/high-contrast element in the header, and it sticks on scroll on all breakpoints.

## 6. Page templates required

1. **Home** — hero, product finder entry, category grid, safety story, motorization story, room inspiration, spec-confidence band, support strip, newsletter.
2. **Product Category (×8)** — single scrolling page with sticky sub-nav (Overview / Features / Colors & Fabrics / Options & Sizes / Measure / FAQ / Shop). No tabs.
3. **Innovation Feature (×5)** — story page with one hero claim, how it works, which products offer it, CTA.
4. **Shop By Room / Need index + detail** — curated recommendations with reasoning.
5. **Product Finder** — 3-step guided tool, results with "why this" explanations.
6. **Support Hub + Guide pages** — steps, video, printable PDF, related products.
7. **Inspiration Gallery + Journal index + article.**
8. **Where to Buy.**
9. **Contact / Pro / About / Legal.**
10. **404 and Search Results** (both designed, not default).

## 7. Content strategy

- **Rewrite every product page to a single template** with a benefit-led opening line, a "best for" summary box, and visible specs.
- **Add a "Best for / Not ideal for" box** on every product. Honesty converts.
- **Publish price ranges** ("Cellular shades from $XX at The Home Depot") pulled or manually maintained; update quarterly.
- **One source of truth for compatibility claims.** Build a single features matrix data file that both marketing pages and FAQs read from, so ShadeAuto™ and the cellular FAQ can never contradict each other again.
- **Consolidate FAQs** into a searchable library, tagged by product, surfaced in-context on product pages, marked up with FAQPage schema.
- **Relaunch the blog as "Journal"** with 2 posts a month across three pillars: Choose (decision guides), Live (care, energy, safety), Design (color and trend).
- **Retire or redirect:** `/products-2/`, all `?p=` permalinks, and any orphaned slide/category archives.

## 8. Technical plan

- **Stack:** Next.js (App Router) + TypeScript + Tailwind CSS, content in a headless CMS (Sanity or Payload) or MDX if the team prefers files. Deploy on Vercel.
- **If WordPress must stay:** use it headless via WPGraphQL, or build a lean custom block theme; either way remove WPBakery and Stockholm.
- **Images:** AVIF/WebP, responsive `srcset`, `next/image`, explicit width/height to eliminate layout shift, lazy-load everything below the fold, LCP hero preloaded.
- **Icons:** inline SVG sprite, no JPEG icons.
- **Performance budget:** < 900 KB homepage, < 35 requests, < 150 KB JS, LCP < 2.0 s mobile, CLS < 0.05, INP < 200 ms.
- **SEO:** one `h1` per page, hand-written titles and meta descriptions, canonical tags, single SEO tool, corrected `robots.txt`, XML sitemap with real lastmod dates, Product + FAQPage + BreadcrumbList + Organization schema, breadcrumbs on every page below Home.
- **Accessibility:** WCAG 2.2 AA as an acceptance criterion, skip link, visible focus rings, 4.5:1 minimum text contrast, keyboard-operable disclosures, `prefers-reduced-motion` respected, alt text on 100% of content images.
- **Security headers:** HSTS, X-Content-Type-Options, X-Frame-Options/frame-ancestors, Referrer-Policy, a starter CSP.
- **Analytics:** GA4 with outbound Home Depot clicks as the primary conversion, plus product-finder completions, swatch clicks, guide downloads, video plays, and newsletter signups. Consent Mode v2 with a real granular cookie banner.

## 9. Migration and redirects

| Old | New |
|---|---|
| `/products-2/` | `/products` (301) |
| `/help/` | `/support/contact` (301, keep `/help` as alias) |
| `venetawindowfashions.com/?p=5495` | `/support/warranty` (301) |
| `/clearfit/` | `/innovation/clearfit` (301) |
| `/smartrail/`, `/smartprivacy/` | `/innovation/smartrail-smartprivacy` (301) |
| `/truquietmotorization/` | `/innovation/motorization` (301) |
| `/cordless-roller-shades/`, `/roman-cordless/` | anchors on parent product pages (301) |
| `/design-blog/` and posts | `/inspiration/journal/...` (301) |
| Non-www → www, http → https | enforce site-wide |

Keep all existing product slugs (`/cellular/`, `/roman/`, etc.) as 301s into `/products/...` and preserve every FAQ answer during migration; that content is the most valuable thing on the site.

## 10. Phasing

| Phase | Duration | Output |
|---|---|---|
| 0. Discovery & measurement | 1-2 weeks | Analytics baseline, keyword map, content inventory, product data model |
| 1. Design | 3-4 weeks | Design system + mockups for Home, Product, Finder, Support, Inspiration (desktop + mobile) |
| 2. Content | 4-6 weeks (parallel) | Rewritten copy for all pages, new photography shot list, spec data migrated into structured fields |
| 3. Build | 5-7 weeks | Templates, CMS, finder tool, search, schema, redirects |
| 4. QA | 2 weeks | Accessibility audit, cross-browser, performance budget enforcement, redirect testing |
| 5. Launch & iterate | Ongoing | Ship, monitor Core Web Vitals + funnel, A/B test the Home Depot CTA placement |
