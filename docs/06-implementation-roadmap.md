# Implementation Roadmap & QA Checklist

## Phases

| Phase | Weeks | Key deliverables | Owner |
|---|---|---|---|
| 0 · Discovery & measurement | 1-2 | GA4 + Search Console baseline, outbound-click tracking on the *current* site (so you have a before number), keyword map, full content inventory, product spec data extracted to structured fields | Analytics + strategy |
| 1 · Design | 3-4 | Design system in Figma, mockups for Home / Product / Finder / Support / Where to Buy at mobile + desktop, component library | Design |
| 2 · Content (parallel) | 4-6 | Rewritten copy for all pages, photography shot list and shoot, spec data QA against the spec book, alt text for every asset | Content |
| 3 · Build | 5-7 | Next.js templates, CMS models, Product Finder, site search, schema markup, redirect map implemented | Engineering |
| 4 · QA & hardening | 2 | Accessibility audit, cross-browser, performance budget enforcement, redirect testing, form and analytics validation | QA |
| 5 · Launch | 1 | DNS/Cloudflare cutover, sitemap resubmission, monitoring dashboards | Engineering |
| 6 · Iterate | Ongoing | CTA placement A/B tests, Journal publishing cadence, room/need page expansion | All |

Realistic total: **14-18 weeks** to launch with content produced properly. A design-and-build-only track with existing copy could ship in 8-10 weeks, but the content is where most of the value is.

## Pre-launch QA checklist

**Semantics & SEO**
- [ ] Exactly one `<h1>` per page, correct heading order, no body copy in heading tags
- [ ] Hand-written title and meta description on every page
- [ ] Single SEO tool installed (remove the Yoast/AIOSEO conflict)
- [ ] `robots.txt` uses relative paths (the current full-URL Disallow is invalid)
- [ ] XML sitemap with accurate `lastmod`, submitted to Search Console
- [ ] Canonical tags on every page; www + https enforced
- [ ] Product, FAQPage, BreadcrumbList and Organization schema validated
- [ ] Full redirect map tested, including `/products-2/` and the `?p=5495` warranty link
- [ ] Zero 404s from navigation or footer

**Accessibility (WCAG 2.2 AA)**
- [ ] axe DevTools and Lighthouse: zero violations
- [ ] Keyboard-only pass on every template, including the Product Finder and all accordions
- [ ] Screen reader pass (VoiceOver + NVDA) on Home and one product page
- [ ] Contrast verified: 4.5:1 text, 3:1 UI and large text
- [ ] 100% of content images have descriptive alt text
- [ ] Skip-to-content link present and visible on focus
- [ ] `prefers-reduced-motion` honoured
- [ ] No text baked into images anywhere
- [ ] Accessibility statement published

**Performance**
- [ ] Homepage under 900 KB, under 35 requests (baseline: 4.7 MB, 118 requests)
- [ ] JS under 150 KB; CSS under 60 KB critical
- [ ] Mobile LCP under 2.0 s, CLS under 0.05, INP under 200 ms
- [ ] All images AVIF/WebP with `srcset` and explicit dimensions
- [ ] Hero LCP image preloaded; everything below the fold lazy-loaded
- [ ] Icons as inline SVG (no JPEG icons)
- [ ] Sensible browser `Cache-Control` (current `max-age=0` gives repeat visitors nothing)

**Content**
- [ ] Vertical Blinds description no longer duplicates Sheer Shades copy
- [ ] Smart-home compatibility stated once, consistently, on one page
- [ ] Copyright year renders dynamically
- [ ] Every spec dimension cross-checked against the spec book
- [ ] "Award-winning" claim either substantiated or removed
- [ ] Price ranges present on all eight product pages
- [ ] Phone number and email visible in header or footer on every page

**Analytics & tracking**
- [ ] GA4 installed with Consent Mode v2
- [ ] Outbound Home Depot clicks tracked as the primary conversion, labelled by source page
- [ ] Product Finder starts and completions tracked
- [ ] Sample-request, guide-download, video-play and newsletter events tracked
- [ ] Site search queries logged (they are free product-roadmap research)
- [ ] Dashboard built before launch, not after

**Security & compliance**
- [ ] HSTS, X-Content-Type-Options, Referrer-Policy, frame-ancestors, starter CSP
- [ ] Granular cookie consent (not "OK to continue")
- [ ] Privacy policy and terms reviewed and dated
- [ ] Form spam protection without a CAPTCHA that blocks assistive tech

## Post-launch: first 90 days

1. Watch Core Web Vitals weekly in Search Console; fix regressions within a sprint.
2. A/B test the Home Depot CTA: header-only vs. header + sticky mobile bar.
3. Measure Product Finder completion rate; if under 40%, cut a step.
4. Publish the first six Journal posts to establish cadence.
5. Expand Shop by Room and Shop by Need pages based on actual search queries.
6. Review the FAQ search log monthly and promote the top questions onto product pages.

## Definition of done for the redesign

The redesign is done when a first-time visitor on a phone can, in under two minutes:
choose the right product for their room, confirm it fits their window, know roughly what it
costs, and land on the correct Home Depot page — and you can see all four of those steps in
your analytics.
