# VENETA™ — Master Redesign Plan

**Single source of truth for this repository.** Version 1.0 · Supersedes `docs/01`–`docs/07`.
Anything in `docs/` is historical context. If this file and a `docs/` file disagree, this file wins.

---

## 0. How to use this document

| If you are… | Read |
|---|---|
| A build agent picking up work | §1 diagnosis, §4 design system, §7 page specs, §11 image pipeline, §14 build brief |
| Reviewing whether the redesign is working | §2 the premium bar, §15 acceptance gates |
| Writing content or SEO | §5 IA, §6 SEO clusters, §8 copy system |
| Handling the Home Depot relationship | §9 handoff model, §10 measurement |
| Planning the work | §13 roadmap |

**Non-negotiable rules for every commit**

1. Commit author must be `beniwt292-cmyk <280820324+beniwt292-cmyk@users.noreply.github.com>` or Vercel will not deploy.
2. No build step. The repo deploys as static HTML from root. `python3 build/make.py` regenerates CSS/pages locally; the committed output is what ships.
3. Never introduce a framework, bundler, or npm dependency without updating §3 of this file first.
4. Every page must pass §15 gates before it is committed.

---

## 1. Why the current redesign still reads as dated

The strategy in this repo is right. The execution fails on five measurable things, not on taste. These were measured against the committed repo state at v1.0 of this plan.

| # | Root cause | Evidence in repo | Consequence |
|---|---|---|---|
| 1 | **There is almost no photography.** 12 WebP files (28–68 KB each) serve 50 pages. The homepage hero is a 60 KB image stretched to full-bleed. | `assets/img/` contains 12 files; `hero.webp` is 60 KB | This is the single largest reason the site does not feel premium. Premium in this category *is* imagery. No type system can compensate for a soft, low-resolution hero. |
| 2 | **Four CSS layers fight each other.** `veneta.css` is a concatenation of `base.css` + `extra.css` + `luxe.css` + `gallery.css`, where layer 4 re-tunes tokens layer 1 already set (Fraunces + brass in the head of the file, Instrument Serif + clay overriding it later). | `assets/css/veneta.css` line 1–6 declares `--daylight:#F2C230` and Fraunces; `build/gallery.css` overrides both | Spacing, type, and colour drift page to page. Drift is what "template-y" actually looks like. |
| 3 | **Decoration substitutes for craft.** Marquee ticker, 30s Ken Burns pan, CSS-counter product numbers, a 240px outlined footer wordmark, hover "View" plates. | `docs/07-design-direction-v2.md` | These are 2021 portfolio-site tropes. They read as effort, not as confidence. Premium brands in this category are quieter and let material do the talking. |
| 4 | **Every section is a grid of equal cards.** Products, rooms, needs, guides, reviews, support all resolve to `repeat(auto-fill, minmax(240px,1fr))`. | `.cards`, `.three`, `.rgrid`, `.sgrid` in `assets/css/veneta.css` | Uniform rhythm flattens hierarchy. The eye finds nothing to land on. |
| 5 | **The technical premium signals are entirely absent.** Across 50 pages: 0 canonical tags, 0 JSON-LD blocks, 0 `og:image`, no `sitemap.xml`, no `robots.txt`, no analytics, and all 207 Home Depot links resolve to one brand shelf URL with no UTMs. | `grep` across `*.html` | The site cannot be found, cannot be shared attractively, and cannot prove it drives revenue. |

### The reframe that stays

Veneta does not sell online; Home Depot does. The site's job is to be the most trustworthy **decision engine** in the category and hand a confident, correctly-specified shopper to Home Depot. That is correct and unchanged. What changes is that the site must *look* like the premium end of the category while doing it.

### Before / after principles

| Retire | Adopt |
|---|---|
| One 60 KB hero reused sitewide | 3–5 art-directed hero variants per page family, 2400px wide, AVIF + WebP |
| Marquee ticker, Ken Burns, counters, outlined wordmark | Zero ambient motion. Motion only on reveal, swatch, and sticky CTA |
| Equal-card grids in every section | Alternating rhythm: full-bleed → asymmetric 5/7 split → macro texture band → compact index |
| 4 stacked CSS layers | One token file, one component file, one page file. Tokens declared exactly once |
| Hairline-everything as the whole idea | Hairlines as *support*; imagery and type contrast carry the design |
| Generic "premium materials" claims | Published specs, opacity percentages, weave close-ups, CPSC-aligned safety facts |
| One Home Depot shelf link | Category-mapped deep links with UTMs and GA4 events |

---

## 2. The premium bar

A reviewer should be able to answer yes to all ten in the first 15 seconds of the homepage on a phone.

1. Does the first screen show real, believable daylight falling through a window covering?
2. Is there exactly one dominant headline, under 12 words?
3. Are there exactly two CTAs above the fold, one of them Home Depot?
4. Can I tell within one glance that this brand is more expensive than Levolor?
5. Is there at least one macro texture image in the first three scrolls?
6. Does any section look like it came from a theme? (must be no)
7. Is anything moving that I did not trigger? (must be no)
8. Do the type sizes differ by at least 3× between headline and body?
9. Is the widest text block under 70 characters?
10. Does the Home Depot relationship read as a premium retail partnership rather than an apology?

**Positioning line to design against:** *Veneta is an interiors brand that happens to sell through Home Depot — not a manufacturer microsite that happens to list products.*

---

## 3. Stack decision

**Stay static. Do not rewrite in Next.js.**

Rationale: the deliverable is 50 mostly-static marketing pages with zero transactions, zero auth, and zero personalisation. A Next.js + headless CMS rewrite would add build complexity, hosting cost, and dependency risk while improving nothing the business actually needs. Static HTML on Vercel already gives near-perfect Core Web Vitals headroom, and the failure modes in §1 are content and design failures that a framework does not fix.

| Layer | Decision |
|---|---|
| Output | Hand-authored + Python-generated static HTML at repo root, `cleanUrls: true` |
| Generator | Keep `build/` Python scripts. Refactor to a single `build/site.py` with one `TOKENS` dict and one `render(page)` function |
| CSS | Collapse to three files: `tokens.css`, `components.css`, `pages.css`, concatenated to `assets/css/veneta.css`. **Tokens declared exactly once.** |
| JS | Vanilla, one file, under 12 KB. Nav, filters, accordions, sticky CTA, GA4 events. No libraries |
| Fonts | Self-hosted WOFF2 subset (latin), `font-display: swap`, preload the two files used above the fold |
| Images | AVIF primary + WebP fallback via `<picture>`, explicit `width`/`height`, `loading="lazy"` except LCP, `fetchpriority="high"` on LCP |
| Hosting | Vercel, static, no build command |
| Analytics | GA4 via `gtag.js`, loaded `async`, consent-safe |
| CMS | None. Content lives in `build/data.py`. Revisit only if a non-technical editor is hired |

**Migration trigger:** move to Astro (not Next.js) only if page count exceeds ~120 or if a CMS becomes a real requirement.

---

## 4. Design system — "Daylight Editorial"

The motif is **light, shadow, and weave**. Not beige. Warm neutral canvas, deep espresso ink, one clay accent, and dark surfaces reserved for motorization.

### 4.1 Tokens

Replace all four existing CSS layers' token blocks with this, declared once in `build/tokens.css`.

```css
:root{
  /* ---- Surface ---- */
  --canvas:        #F6F2EC;  /* page background, warm bone */
  --surface:       #FCFAF6;  /* raised panels, tables, cards */
  --surface-sink:  #EDE7DD;  /* quiet fills, image placeholders */
  --line:          #DCD5C9;  /* hairline */
  --line-soft:     #E8E2D8;
  --noir:          #16150F;  /* dark band: motorization only */
  --noir-soft:     #23221A;

  /* ---- Ink ---- */
  --ink:           #211C16;  /* body + headlines */
  --ink-70:        #55503F;  /* secondary copy */
  --ink-45:        #8A8371;  /* meta, captions, eyebrows */
  --ink-25:        #B7B0A0;  /* disabled */

  /* ---- Accent (use sparingly: <5% of any screen) ---- */
  --clay:          #8C5A38;
  --clay-deep:     #6B4228;
  --clay-soft:     #E0CDBC;
  --hd-orange:     #F96302;  /* Home Depot CTA only, never decorative */
  --success:       #2E6B4F;

  /* ---- Type ---- */
  --serif: "Instrument Serif", "Iowan Old Style", Georgia, serif;
  --sans:  "Inter Tight", "Inter", system-ui, -apple-system, sans-serif;

  --fs-display: clamp(44px, 7.4vw, 96px);
  --fs-h1:      clamp(36px, 5.6vw, 68px);
  --fs-h2:      clamp(28px, 3.6vw, 46px);
  --fs-h3:      clamp(20px, 1.7vw, 26px);
  --fs-h4:      18px;
  --fs-lede:    clamp(17px, 1.35vw, 21px);
  --fs-body:    17px;
  --fs-body-s:  15px;
  --fs-caption: 13px;
  --fs-micro:   11px;

  --lh-display: 0.96;
  --lh-head:    1.08;
  --lh-body:    1.62;
  --tr-display: -0.022em;
  --tr-micro:   0.18em;

  /* ---- Space (8px base, editorial jumps) ---- */
  --s1: 8px;   --s2: 16px;  --s3: 24px;  --s4: 32px;
  --s5: 40px;  --s6: 48px;  --s8: 64px;  --s10: 80px;
  --s12: 96px; --s15: 120px; --s20: 160px;
  --section-y: clamp(80px, 9vw, 148px);
  --pad: clamp(20px, 5vw, 64px);
  --wrap: 1360px;
  --reading: 68ch;

  /* ---- Radius / elevation ---- */
  --r-0: 0;     /* default: everything */
  --r-1: 2px;   /* buttons, inputs only */
  --shadow-none: none;   /* no decorative shadows anywhere */
  --shadow-lift: 0 12px 32px rgba(33,28,22,.07); /* sticky bars + open menus only */

  /* ---- Motion ---- */
  --ease: cubic-bezier(.22,1,.36,1);
  --d-fast: 160ms; --d-med: 280ms; --d-slow: 520ms;
}
@media (prefers-reduced-motion: reduce){
  *{animation:none !important; transition-duration:1ms !important}
}
```

### 4.2 Type rules

| Role | Face | Size token | Weight | Notes |
|---|---|---|---|---|
| Hero display | Instrument Serif | `--fs-display` | 400 | Max 12 words. Never uppercase. One `<em>` in clay permitted per page |
| H1 (interior) | Instrument Serif | `--fs-h1` | 400 | Exactly one per page |
| H2 | Instrument Serif | `--fs-h2` | 400 | |
| H3 | Inter Tight | `--fs-h3` | 500 | Switch to sans at H3 — this contrast is the system |
| Lede | Inter Tight | `--fs-lede` | 400 | Max 46ch |
| Body | Inter Tight | `--fs-body` | 400 | `max-width: var(--reading)` |
| Eyebrow / micro-label | Inter Tight | `--fs-micro` | 500 | uppercase, `letter-spacing: var(--tr-micro)` |
| Spec tables | Inter Tight | `--fs-body-s` | 400/500 | `font-variant-numeric: tabular-nums` |

**Hard limits:** no more than 9 distinct font sizes render on any page. Headline-to-body ratio must be ≥ 3× on desktop hero.

### 4.3 Component inventory

| Component | Premium execution spec |
|---|---|
| Header | 76px, `--canvas` at 94% opacity + 10px blur, 1px bottom hairline. Transparent over hero, solidifies past 80px scroll. Logo wordmark in Inter Tight, `letter-spacing:.30em` |
| Mega menu | Max 4 columns of links + **one editorial image panel** on the right with a category photo and a one-line caption. Never a bare link dump. Opens on click, closes on Esc, focus-trapped |
| Hero | Full-bleed `<picture>`, min-height `min(86vh, 780px)`. Gradient scrim only where text sits (bottom-left), never a flat overlay across the whole image. Headline + lede + 2 CTAs + 3-item trust row on a hairline |
| Editorial split | `grid-template-columns: 5fr 7fr`, gap `--s8`. Image bleeds to one page edge. Alternate direction every other instance |
| Product index card | 4:5 image, no border, no shadow. Name in H3 sans, one-line descriptor in `--ink-70`, 2–3 attribute chips, single text CTA. Hover: image scales 1.03 over `--d-slow` |
| Macro texture band | Full-bleed row of 3–4 100mm macro shots at 3:4, no gaps, no captions except one micro-label. This band is what sells "premium material" |
| Swatch picker | 56px tactile tiles, 1px `--line`, shows weave. Each swatch carries name + openness/opacity % as micro-label. Selected state: 2px `--ink` inset ring |
| Spec table | `--surface` background, hairline rows, `--surface-sink` head row, sticky first column on mobile via `overflow-x`. This is Veneta's differentiator — never hide it in tabs |
| Comparison table | Max 5 columns, row groups labelled, checkmarks in `--success`, "best for" row first |
| Sticky Home Depot bar | Appears past 60% viewport scroll. Desktop: right rail, 300px. Mobile: bottom bar, 64px, product name + `--hd-orange` CTA. Dismissible, remembers dismissal for the session only (in-memory, no storage APIs) |
| FAQ accordion | Hairline dividers, 24px vertical padding, `<details>`/`<summary>` native, chevron rotates over `--d-fast` |
| Footer | `--noir`, 4 link columns + newsletter + Home Depot statement + CPSC safety line. No oversized outlined wordmark |

### 4.4 Motion policy

Permitted, and nothing else:

- Reveal on scroll: `opacity 0→1`, `translateY 12px→0`, `--d-slow`, `--ease`, staggered 60ms, once only.
- Image hover scale to 1.03.
- Swatch hover lift, 2px.
- Sticky CTA slide-in.
- Accordion/menu open-close.

Banned: marquees, Ken Burns, auto-rotating carousels, parallax, counters that tick, text scramble, cursor followers.

### 4.5 Accessibility (WCAG 2.2 AA, mandatory)

- Contrast: `--ink` on `--canvas` = pass; `--ink-45` only at ≥15px and never for essential copy; `--hd-orange` button always uses `--ink` text, never white.
- Focus visible: 2px `--clay` outline, 2px offset, on all interactive elements.
- Target size: 44×44 minimum for all primary controls.
- One `<h1>` per page, no skipped levels.
- All non-decorative images carry descriptive alt text naming product type and room.
- `prefers-reduced-motion` honoured globally (already in tokens).
- No hover-only content. No auto-playing motion.
- Forms: visible labels, inline errors, `aria-describedby`.

---

## 5. Information architecture

### 5.1 Primary navigation

`Products · Shop by Need · Rooms · Inspiration · Guides · Support` + persistent utility: `Free Samples` · `Shop at Home Depot`
Audience entries (`For Designers`, `Commercial`) live in the top utility bar and the footer, not the main nav.

### 5.2 Sitemap

Existing URLs are kept wherever possible; `vercel.json` redirects already cover the legacy WordPress paths. New pages are marked **NEW**.

| URL | Template | Audience | Primary CTA |
|---|---|---|---|
| `/` | Home | All | Shop at Home Depot |
| `/products` | Category hub | Homeowner | Explore categories |
| `/cellular-shades` | Category | Homeowner | Shop cellular at Home Depot |
| `/roller-solar-shades` | Category | Homeowner | Shop roller & solar at Home Depot |
| `/roman-shades` | Category | Homeowner | Shop roman at Home Depot |
| `/sheer-shades` | Category | Homeowner | Shop sheer at Home Depot |
| `/faux-wood-blinds` | Category | Homeowner | Shop faux wood at Home Depot |
| `/vertical-blinds` | Category | Homeowner | Shop vertical at Home Depot |
| `/shutters` | Category | Homeowner | Shop shutters at Home Depot |
| `/woven-wood-shades` **NEW** | Category | Homeowner | Shop woven wood at Home Depot |
| `/dualdrape` | Product family | Homeowner | Configure at Home Depot |
| `/clearfit`, `/smartrail`, `/smartprivacy`, `/truquiet-motorization` | Feature | Homeowner + Trade | See compatible products |
| `/motorization` | Feature hub | Homeowner + Trade | Explore motorized |
| `/product-finder` | Tool | Homeowner | See my matches |
| `/shop-by-need` | Need hub | Homeowner | Start with a priority |
| `/shop-by-need/blackout` **NEW** | Need | Homeowner | Compare blackout options |
| `/shop-by-need/light-filtering` **NEW** | Need | Homeowner | Compare light filtering |
| `/shop-by-need/privacy` **NEW** | Need | Homeowner | Explore privacy options |
| `/shop-by-need/energy-efficiency` **NEW** | Need | Homeowner | See insulating shades |
| `/shop-by-need/patio-doors` **NEW** | Need | Homeowner | See wide-opening options |
| `/shop-by-room` | Room hub | Homeowner | Browse by room |
| `/shop-by-room/{bedroom,living-room,kitchen,bathroom,home-office,nursery}` **NEW** | Room | Homeowner | Shop room picks |
| `/inspiration` | Gallery | All | View gallery |
| `/styles/{modern-minimal,warm-organic,coastal,classic-tailored}` **NEW** | Style | Homeowner + Designer | See recommended products |
| `/buying-guides` | Guide hub | Homeowner | Compare options |
| `/how-to-measure`, `/how-to-install`, `/how-to-clean` | HowTo | Homeowner | Continue to Home Depot |
| `/guides/blinds-vs-shades-vs-shutters` **NEW** | Comparison | Homeowner | Find your match |
| `/child-safety` | Trust | Homeowner | Explore cordless |
| `/innovation` | Brand | All | Explore features |
| `/about` | Brand | All | Where to buy |
| `/journal` + 5 posts | Editorial | All | Related products |
| `/for-professionals` | Trade | Designer | Request sample kit |
| `/for-professionals/resources` **NEW** | Trade | Designer | Download specs |
| `/commercial` **NEW** | Commercial | Commercial | Start a project |
| `/commercial/spec-library` **NEW** | Commercial | Commercial | Download CAD/CSI |
| `/free-samples` | Conversion | Homeowner + Designer | Order samples |
| `/where-to-buy` | Handoff | All | Shop at Home Depot |
| `/support`, `/faq`, `/warranty`, `/contact`, `/installation-videos*` | Support | All | Get help |
| `/accessibility`, `/privacy-policy`, `/terms-and-conditions`, `/sitemap` | Legal | All | — |

**Page-count discipline:** do not add a page unless it owns a distinct search intent *and* a distinct CTA. Thin duplicates are the fastest way back to a dated site.

---

## 6. SEO strategy

### 6.1 Division of labour with Home Depot

Veneta owns **education, material guidance, specification depth, and brand**. Home Depot owns **SKU detail, price, configuration, cart**. Never republish Home Depot PDP copy. Never create a page whose only content is one SKU's attributes.

### 6.2 Clusters

| Cluster | Hub | Spokes | Intent |
|---|---|---|---|
| Cellular | `/cellular-shades` | blackout cellular, energy efficiency, bedroom, cordless, cell-size spec guide | Commercial |
| Roller & solar | `/roller-solar-shades` | solar openness factor, large windows, light filtering, cordless roller guide | Commercial |
| Roman | `/roman-shades` | flat vs soft fold, cordless roman, living room | Commercial |
| Faux wood & vertical | `/faux-wood-blinds`, `/vertical-blinds` | bathroom/kitchen moisture, patio doors, wood vs faux wood | Commercial |
| Shutters | `/shutters` | interior shutters, L-frame vs deco frame, install videos | Commercial |
| Need | `/shop-by-need` | blackout, privacy, light filtering, energy, patio doors | Commercial + informational |
| Room | `/shop-by-room` | bedroom, living room, kitchen, bathroom, office, nursery | Commercial |
| Decision | `/buying-guides` | blinds vs shades vs shutters, inside vs outside mount, opacity explained | Mid-funnel |
| Measure & install | `/how-to-measure` | inside/outside mount, tools, common mistakes | Informational, high assist |
| Safety | `/child-safety` | cordless options, CPSC guidance, nursery | Trust |
| Motorization | `/motorization` | TruQuiet, compatibility truth, high windows, scheduling | Commercial |
| Trade / commercial | `/for-professionals`, `/commercial` | spec library, lead times, sector pages | B2B lead |

### 6.3 On-page template requirements

Every category page must contain, in order: hero image + H1 + 2-sentence summary; 2 CTAs; attribute chips; "best for" rooms; opacity/light-control explainer with visual; **published spec table** (Veneta's real differentiator); material swatches; safety status; comparison block; FAQ; Home Depot handoff band; 3+ internal links to need/room/guide pages.

### 6.4 Technical SEO checklist (currently 0% complete)

- [ ] Self-referencing `<link rel="canonical">` on all 50+ pages
- [ ] Unique `<title>` ≤ 60 chars and `<meta name="description">` ≤ 155 chars per page
- [ ] `og:title`, `og:description`, `og:image` (1200×630, per-page), `twitter:card=summary_large_image`
- [ ] `sitemap.xml` generated by `build/site.py`, referenced in `robots.txt`
- [ ] `robots.txt` allowing all, pointing to sitemap
- [ ] `BreadcrumbList` JSON-LD on every non-home page
- [ ] `Organization` JSON-LD on `/` with logo, contactPoint, sameAs
- [ ] `Product` JSON-LD on every category and product-family page
- [ ] `FAQPage` JSON-LD wherever FAQs render
- [ ] `HowTo` JSON-LD on measure / install / clean
- [ ] Home Depot outbound links: **followed**, `target="_blank"`, `rel="noopener"` — this is the intended retail path, not sponsored placement
- [ ] Descriptive alt text on 100% of images

### 6.5 JSON-LD reference blocks

```html
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"Product",
  "name":"Veneta Custom Cellular Shades",
  "brand":{"@type":"Brand","name":"VENETA"},
  "category":"Cellular Shades",
  "description":"Custom cellular shades with published width and height ranges for every cell size and lift system, in light filtering and blackout opacities.",
  "image":["https://www.venetawindowfashions.com/assets/img/cellular-hero-2400.webp"],
  "material":["Spunlace non-woven","Honeycomb fabric"],
  "additionalProperty":[
    {"@type":"PropertyValue","name":"Light control","value":"Light filtering, Room darkening, Blackout"},
    {"@type":"PropertyValue","name":"Operation","value":"Cordless, Continuous loop, Motorized"},
    {"@type":"PropertyValue","name":"Best for","value":"Bedrooms, Nurseries, Energy efficiency"}
  ],
  "url":"https://www.venetawindowfashions.com/cellular-shades",
  "offers":{
    "@type":"Offer",
    "availability":"https://schema.org/InStock",
    "seller":{"@type":"Organization","name":"The Home Depot"},
    "url":"https://www.homedepot.com/b/VENETA/N-5yc1vZryk"
  }
}
</script>
```

```html
<script type="application/ld+json">
{
  "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://www.venetawindowfashions.com/"},
    {"@type":"ListItem","position":2,"name":"Products","item":"https://www.venetawindowfashions.com/products"},
    {"@type":"ListItem","position":3,"name":"Cellular Shades","item":"https://www.venetawindowfashions.com/cellular-shades"}
  ]
}
</script>
```

```html
<script type="application/ld+json">
{
  "@context":"https://schema.org","@type":"HowTo",
  "name":"How to measure for inside-mount shades",
  "totalTime":"PT10M",
  "tool":[{"@type":"HowToTool","name":"Steel tape measure"},{"@type":"HowToTool","name":"Pencil"}],
  "step":[
    {"@type":"HowToStep","name":"Measure width in three places","text":"Measure the inside width at the top, middle and bottom of the window opening."},
    {"@type":"HowToStep","name":"Use the narrowest width","text":"Record the narrowest of the three widths to the nearest 1/8 inch. Do not deduct anything."},
    {"@type":"HowToStep","name":"Measure height in three places","text":"Measure height at the left, centre and right of the opening."},
    {"@type":"HowToStep","name":"Use the longest height","text":"Record the longest of the three heights to the nearest 1/8 inch."}
  ]
}
</script>
```

### 6.6 Core Web Vitals targets and budgets

| Metric | Target (75th pct, mobile) |
|---|---|
| LCP | ≤ 2.0s (headroom under the 2.5s threshold) |
| INP | ≤ 150ms |
| CLS | ≤ 0.05 |

| Budget | Limit |
|---|---|
| Homepage first load, mobile | ≤ 1.1 MB |
| Category page | ≤ 1.0 MB |
| Guide/article page | ≤ 700 KB |
| LCP image | ≤ 180 KB AVIF |
| CSS total | ≤ 45 KB gzip |
| JS total | ≤ 12 KB gzip |
| Third-party | GA4 only |
| Requests, homepage | ≤ 35 |

---

## 7. Page specifications

### 7.1 Homepage

```
┌──────────────────────────────────────────────────────────────┐
│ UTILITY   Free Samples · For Designers · Commercial · Support │
│ HEADER    VENETA   Products Need Rooms Inspiration Guides     │
│                              [Shop at Home Depot]             │
├──────────────────────────────────────────────────────────────┤
│ HERO — full bleed, 86vh, morning light through roller shades   │
│                                                               │
│  Light, exactly where you want it.                            │
│  Custom shades, blinds and shutters built to published        │
│  specifications and sold through The Home Depot.              │
│  [Shop at Home Depot]  [Order free samples]                   │
│  ─────────────────────────────────────────────────            │
│  CORDLESS BY DEFAULT · PUBLISHED SPECS · MADE TO SIZE         │
├──────────────────────────────────────────────────────────────┤
│ FINDER — 3 selects on --surface-sink: Room / Priority / Look  │
│          [See my matches]   (posts to /product-finder)        │
├──────────────────────────────────────────────────────────────┤
│ SPLIT 5/7 — image bleeds left                                 │
│   "We publish what others hide."                              │
│   Exact width and height ranges for every cell size and       │
│   lift system. Compact spec preview table. [See all specs]    │
├──────────────────────────────────────────────────────────────┤
│ PRODUCT INDEX — 8 items, 4:5 imagery, chips, text CTA         │
├──────────────────────────────────────────────────────────────┤
│ MACRO TEXTURE BAND — 4 full-bleed 3:4 material close-ups      │
│   micro-label: "MATERIALS · WEAVE, OPACITY, HAND"             │
├──────────────────────────────────────────────────────────────┤
│ SPLIT 7/5 — image bleeds right                                │
│   Cordless where it matters. CPSC-aligned safety story.       │
│   [Explore cordless] → /child-safety                          │
├──────────────────────────────────────────────────────────────┤
│ DARK BAND (--noir) — motorization, one image, 3 short points,  │
│   single source of truth on smart-home compatibility          │
├──────────────────────────────────────────────────────────────┤
│ ROOM RAIL — 6 room scenes, horizontal snap scroll             │
├──────────────────────────────────────────────────────────────┤
│ GUIDES — 3 editorial cards: measure, opacity, blinds vs shades│
├──────────────────────────────────────────────────────────────┤
│ HANDOFF BAND — co-branded. What happens at Home Depot, in 3   │
│   steps. [Shop at Home Depot] [Measure & install help]        │
├──────────────────────────────────────────────────────────────┤
│ SPLIT — For designers / For commercial, two entries           │
├──────────────────────────────────────────────────────────────┤
│ FOOTER (--noir) — 4 columns, newsletter, HD statement, CPSC   │
└──────────────────────────────────────────────────────────────┘
```

Removed from the current homepage: marquee ticker, review cards with placeholder copy, numbered product counters, oversized outlined footer wordmark. Placeholder reviews must not ship — replace with published-spec proof, which is true and stronger.

### 7.2 Category page

```
BREADCRUMB  Home / Products / Cellular Shades
HERO 62vh   room scene, H1 + 2 sentences + [Shop at HD] [Free samples]
CHIPS       Light filtering · Blackout · Cordless · Motorized · Insulating
SPLIT 5/7   Why cellular — image + 3 short benefit paragraphs
OPACITY     3-up visual: same window at 5% / 25% / blackout, with % labels
SPECS       Full published spec table, --surface, tabular numerals, no tabs
SWATCHES    Material picker, 56px tiles, name + opacity micro-label
ROOMS       4 room links with photos
COMPARE     Cellular vs Roman vs Roller, max 5 columns
SAFETY      Cordless status + CPSC line
FAQ         6 questions, native <details>
HANDOFF     Sticky right rail (desktop) / bottom bar (mobile) throughout
RELATED     3 guides
```

### 7.3 Product family page (e.g. `/dualdrape`)

Gallery left / summary right. Summary contains: name, one paragraph, `Best for`, `Light control`, `Operation`, `Widths`, `Heights`, then `[Configure at Home Depot]` and `[Order free samples]`. Then: feature story with one large image, full spec table, materials, install/care/safety strip, related guides.

### 7.4 Inspiration gallery

Hero one-liner. Filter bar: Product / Room / Style / Light control. Mixed-aspect grid (portrait 3:4, landscape 3:2, macro 1:1) — never uniform. One editorial project feature every 9 tiles. Each tile: room + product caption, links to the category page.

### 7.5 Trade page

Hero + `[Request a sample kit]` `[Download spec library]`. Benefits band (4 items). Resource grid (spec PDFs, CAD, care guides, lead times). Project gallery. Short inquiry form: name, firm, project type, timeline, resources needed.

### 7.6 Commercial page **NEW**

Sector row (multifamily, hospitality, office, healthcare, education). Capability statement with published spec ranges. Spec library downloads. 2–3 case studies (may be composite/illustrative — label clearly). Project inquiry form.

---

## 8. Copy system

**Voice:** plainspoken, specific, quietly confident. Borrow Lutron's restraint, not Graza's irreverence.

| Do | Don't |
|---|---|
| "Exact width and height ranges for every lift system." | "Premium materials and innovative features." |
| "Cordless by default on every cellular shade." | "Family safety is our top priority." |
| "5% openness keeps the view, cuts the glare." | "Perfect light control for any room." |
| "Configure and buy at The Home Depot." | "Visit our retail partner to learn more." |

Rules: hero headlines ≤ 12 words. Ledes ≤ 2 sentences. No exclamation marks. No "elevate", "seamless", "curated", "game-changing". Every claim either has a number or is cut. Placeholder prices, star ratings, and invented reviews must be removed before launch.

---

## 9. Home Depot handoff model

### 9.1 CTA hierarchy (sitewide, unchanging)

1. **Primary — `Shop at Home Depot`** (`--hd-orange` fill, `--ink` text)
2. **Secondary — `Order free samples`** (ghost, `--ink` border)
3. **Tertiary — `Measure & install help`** (text link with hairline)

### 9.2 Link map

Replace all 207 generic shelf links with category-mapped deep links held in one place (`build/data.py → HD_LINKS`), so they can be corrected in a single commit.

```python
HD_LINKS = {
  "brand":     "https://www.homedepot.com/b/VENETA/N-5yc1vZryk",
  "cellular":  "https://www.homedepot.com/b/VENETA/N-5yc1vZryk",  # TODO: filtered shelf
  "roller":    "...",
  "roman":     "...",
  "sheer":     "...",
  "fauxwood":  "...",
  "vertical":  "...",
  "shutters":  "...",
  "install":   "https://www.homedepot.com/services/c/blinds-installation/...",
  "stores":    "https://www.homedepot.com/l/storeDirectory",
}
```

Every link is rendered through one helper that appends UTMs and the GA4 event hook:

```python
def hd(key, page_type, module, category=""):
    url = HD_LINKS[key]
    utm = (f"?utm_source=veneta&utm_medium=referral&utm_campaign=brand_handoff"
           f"&utm_content={page_type}_{module}_{category or key}")
    return (f'<a class="btn btn--hd" href="{url}{utm}" target="_blank" rel="noopener" '
            f'data-hd="{page_type}|{module}|{category or key}">Shop at Home Depot</a>')
```

### 9.3 Trust continuity

Directly under every primary CTA, one line of expectation-setting: *"Configure size, opacity and lift on Home Depot. Veneta helps you decide before you buy."* Handoff bands state, in three steps: choose your spec here → configure and order at Home Depot → optional measure and install through Home Depot's licensed providers. Order status, returns, and delivery questions route to Home Depot, and the site says so plainly instead of hiding it.

---

## 10. Measurement

GA4 with enhanced measurement on (captures outbound clicks natively), plus these explicit events fired by `assets/js/veneta.js`:

| Event | Trigger | Params |
|---|---|---|
| `hd_click` | Any element with `data-hd` | `page_type`, `module`, `category` |
| `sample_request` | `/free-samples` submit | `products[]`, `audience` |
| `finder_complete` | Product finder submit | `room`, `priority`, `look` |
| `spec_table_view` | Spec table 50% visible 2s | `category` |
| `swatch_select` | Swatch click | `category`, `material` |
| `guide_read` | 75% scroll on guide | `slug` |
| `trade_apply` | Trade form submit | `firm_type` |
| `commercial_inquiry` | Commercial form submit | `sector` |
| `spec_download` | PDF/CAD download | `file` |

Custom dimensions: `page_type`, `module`, `category`, `audience`.
Key report: organic landing page → `hd_click` rate, segmented by template.

---

## 11. Image pipeline (the highest-priority workstream)

The site needs roughly **70 images**, not 12. All AI-generated at launch, treated as temporary stand-ins for real photography.

### 11.1 Shot list

| Set | Count | Ratio | Long edge | Purpose |
|---|---:|---|---:|---|
| Homepage hero | 1 | 16:9 | 2400 | LCP |
| Category heroes | 9 | 3:2 | 2000 | One per category |
| Product index | 8 | 4:5 | 1200 | Homepage + `/products` |
| Macro materials | 12 | 3:4 | 1400 | Texture bands, swatch enlargements |
| Opacity triptychs | 9 | 1:1 | 1000 | Same window at 3 openness levels ×3 categories |
| Room scenes | 6 | 3:4 | 1400 | Room rail + room pages |
| Style scenes | 4 | 3:2 | 1600 | Style pages |
| Motorization | 3 | 16:9 | 2000 | Dark band + feature pages |
| Safety / nursery | 2 | 4:3 | 1600 | Child safety |
| Trade + commercial | 6 | 3:2 | 1800 | Hospitality, office, multifamily, lounge |
| Guides / diagrams | 6 | 4:3 | 1400 | Measure, mount types |
| `og:image` set | 8 | 1200×630 | — | Social cards |

Naming: `assets/img/{set}-{slug}-{longedge}.{avif|webp}`, e.g. `hero-home-2400.avif`, `macro-woven-flax-1400.webp`.

### 11.2 Constant art direction (apply to every prompt)

- **Light:** natural daylight only, single source, directional from camera-left or camera-right. Morning or late afternoon warmth. Soft, physically consistent shadows. No mixed colour temperature. No orange filter.
- **Lens:** rooms 32mm; product-in-room 50mm; macro 100mm. Camera height 4'8". Verticals corrected. No fisheye.
- **Palette:** warm bone, limestone, flax, mushroom, muted white oak, espresso accents. One clay object maximum per scene.
- **Styling:** under-styled. Maximum three props. No people. No pets. No text, signage, or artwork with legible lettering. No plants in every frame.
- **Finish:** matte, film-like. Slight grain. Compressed highlights. Warm-neutral whites, never blue.

### 11.3 Prompt template

```
[SUBJECT / ROOM], [STYLE] interior, featuring [PRODUCT] in [MATERIAL + COLOUR],
[POSITION: half lowered / fully lowered / tilted slats].
Natural daylight from camera-[LEFT/RIGHT] showing realistic filtered light and
soft directional shadows on [FLOOR/WALL MATERIAL].
Shot on [32mm|50mm|100mm macro], eye-level architectural interior photography,
corrected verticals, editorial composition, generous negative space.
Palette: warm bone, limestone, flax, mushroom, white oak.
Mood: calm, precise, quietly expensive, believable, tactile.
Emphasise: [FEATURE], even pleat/slat spacing, crisp fabric edges, accurate
window proportions, visible weave texture.
Avoid: warped mullions, uneven slat spacing, duplicated furniture, impossible
shadow directions, legible text or signage, glossy CGI surfaces, HDR halos,
people, oversaturated colour.
Aspect ratio [RATIO]. Photorealistic. Matte film finish, fine grain.
```

### 11.4 Worked prompts

**Homepage hero (16:9, 2400px)**
> Open-plan living room in a warm modern interior, featuring light-filtering roller shades in flax linen, three-quarters lowered across a tall window wall. Natural morning daylight from camera-left showing realistic filtered light and soft directional shadows across white oak flooring and lime-plaster walls. Shot on 32mm, eye-level architectural interior photography, corrected verticals, editorial composition, generous negative space at lower left for headline. Palette: warm bone, limestone, flax, mushroom, white oak. Mood: calm, precise, quietly expensive, believable, tactile. Emphasise the soft glow of light through the shade fabric, crisp shade edges, accurate window proportions, visible weave. Avoid warped mullions, duplicated furniture, impossible shadows, legible text, glossy CGI surfaces, people. Aspect ratio 16:9. Photorealistic, matte film finish, fine grain.

**Macro material (3:4, 1400px)**
> Macro photograph of woven wood shade material in flax and mushroom tones, natural bamboo and reed fibres with visible slubs and colour variation. Soft directional daylight raking across the surface from camera-right. Shot on 100mm macro, editorial materials photography, shallow but realistic depth of field. Emphasise fibre detail, weave rhythm, tactile hand, subtle irregularity. Avoid repeating pattern glitches, plastic sheen, synthetic uniformity, HDR halos. Aspect ratio 3:4. Photorealistic, matte film finish, fine grain.

**Opacity triptych frame (1:1, 1000px)**
> Straight-on view of a single window fitted with a solar roller shade at 5 percent openness, fully lowered, bright exterior visible as a soft silhouette through the weave. Neutral interior wall, no furniture. Natural midday daylight. Shot on 50mm, perfectly level, corrected verticals, clinical editorial product photography. Emphasise the openness of the weave, even tension across the fabric, straight bottom bar. Avoid warped mullions, uneven fabric tension, legible exterior detail, people. Aspect ratio 1:1. Photorealistic, matte finish.

**Motorization dark band (16:9, 2000px)**
> Minimal bedroom at dusk in a modern interior, motorized cellular shades half lowered, low warm interior light and a deep blue-grey exterior sky. No visible remote or device screens. Shot on 32mm, eye-level architectural interior photography, corrected verticals, moody but clean. Palette: espresso, charcoal, bone, white oak. Emphasise even pleat spacing, precise shade alignment, quiet luxury. Avoid floating objects, glowing UI overlays, legible text, glossy CGI surfaces, people. Aspect ratio 16:9. Photorealistic, matte film finish, fine grain.

### 11.5 Rejection checklist (reject, do not retouch)

Mullions that don't align · slats that taper or bend · uneven pleat spacing · roman folds that defy gravity · sheer layers with inconsistent transparency · hems melting into walls · duplicated furniture or decor · conflicting shadow directions · gibberish text · asymmetric chair or trim geometry · plastic/CGI sheen · HDR halos around window frames · bottom bars that aren't level.

Category-specific: **cellular** = count the pleats, spacing must be uniform; **blinds** = ladder/tilt geometry must be coherent; **shutters** = stile and rail proportions realistic; **woven wood** = weave must not visibly tile.

### 11.6 Processing and delivery

1. Generate at 2× target long edge, then downscale (removes AI micro-artefacts).
2. Apply one shared grade across the whole set: highlights −8, warmth +3, clarity −5, grain 8%.
3. Export AVIF q55 + WebP q78. Ship both via `<picture>`.
4. Enforce budgets: hero ≤ 180 KB AVIF, category hero ≤ 140 KB, cards ≤ 70 KB, macros ≤ 90 KB.
5. Every image gets alt text naming product type, material, and room.
6. Log every accepted image's prompt in `docs/image-log.md` so the set can be extended consistently.

**Replacement path:** when real photography is commissioned, shoot the same shot list, same lenses, same light direction, so files swap 1:1. Priority order: homepage hero → top 5 category heroes → macros → gallery.

---

## 12. Content honesty rules

The current build ships placeholder prices, star ratings, and review copy. Remove all of it. A premium brand does not fake social proof, and Home Depot already hosts real ratings. Replace with: published spec ranges, cordless-by-default status, warranty terms, and Home Depot ratings referenced by link only. Fix the contradiction between homepage smart-home claims and the cellular FAQ by declaring one compatibility truth in `build/data.py` and rendering it everywhere from that one source.

---

## 13. Roadmap

| Phase | Scope | Exit condition |
|---|---|---|
| **P0 — Foundations** | Collapse CSS to `tokens/components/pages`, tokens declared once, delete marquee / Ken Burns / counters / outlined wordmark, remove placeholder reviews and prices | One coherent visual system; zero token overrides |
| **P1 — Imagery** | Generate, grade, and ship the 70-image set per §11; `<picture>` AVIF+WebP everywhere | Homepage and all 9 category heroes are art-directed originals |
| **P2 — Templates** | Rebuild home, category, product-family, guide, gallery per §7 with alternating rhythm and macro bands | Premium bar §2 passes on mobile |
| **P3 — Technical SEO** | Canonicals, meta, OG images, JSON-LD, `sitemap.xml`, `robots.txt` | §6.4 checklist 100% complete |
| **P4 — Handoff + analytics** | `HD_LINKS` map, UTM helper, GA4 + all §10 events, sticky CTA | `hd_click` reporting live and segmented by template |
| **P5 — Depth** | New need, room, style, comparison pages; commercial + trade resources | Every §5.2 **NEW** page live with unique intent and CTA |
| **P6 — Ongoing** | Replace AI imagery with real photography; expand guides; CRO on handoff | Real photography on hero + top 5 categories |

Sequencing rule: **P1 before P2.** Rebuilding layouts before the imagery exists is exactly how this repo got here.

---

## 14. Build-agent brief

Paste this when handing work to a coding agent.

> You are working in `beniwt292-cmyk/veneta-website-redesign`, a dependency-free static site deployed on Vercel from the repo root. `MASTER_PLAN.md` is the single source of truth; read it before changing anything. Commit as `beniwt292-cmyk <280820324+beniwt292-cmyk@users.noreply.github.com>`.
>
> Rules: no npm, no framework, no bundler. CSS is generated by `python3 build/make.py` into `assets/css/veneta.css` from `tokens.css`, `components.css`, `pages.css` only — tokens declared exactly once, no overrides. JS stays under 12 KB in `assets/js/veneta.js`, vanilla only, no storage APIs. Every image ships as `<picture>` with AVIF + WebP, explicit dimensions, descriptive alt text, `loading="lazy"` except the LCP image which gets `fetchpriority="high"`. Motion is limited to the five permitted cases in §4.4; anything else is a bug. Every page needs one `<h1>`, a canonical, unique title/description, an OG image, and the JSON-LD blocks specified for its template. All Home Depot links render through the `hd()` helper so UTMs and the `data-hd` analytics hook are never missed. Do not ship placeholder prices, ratings, or reviews. Before committing, run the §15 gates and state the result in the commit body.

---

## 15. Acceptance gates

A page cannot be committed until all of these pass.

**Design**
- [ ] Premium bar §2: all ten yes
- [ ] ≤ 9 distinct font sizes rendered
- [ ] No two adjacent sections use the same layout pattern
- [ ] At least one full-bleed image and one macro texture on every category page
- [ ] Zero decorative shadows; radius 0 except buttons/inputs
- [ ] Accent colour under 5% of screen area

**Accessibility**
- [ ] One `<h1>`, no skipped heading levels
- [ ] All images have descriptive alt text
- [ ] Contrast AA on all text and controls
- [ ] Full keyboard path, visible focus, Esc closes menus
- [ ] Targets ≥ 44×44
- [ ] Reduced-motion honoured
- [ ] No hover-only content, no auto-motion

**SEO**
- [ ] Canonical, unique title ≤ 60, description ≤ 155, OG image present
- [ ] Correct JSON-LD for template, validates clean
- [ ] Breadcrumbs present and marked up
- [ ] ≥ 3 internal links to related hub/spoke pages
- [ ] Listed in `sitemap.xml`

**Performance**
- [ ] Within §6.6 page-weight budget
- [ ] LCP image preloaded, correctly sized, ≤ 180 KB
- [ ] No layout shift on font or image load
- [ ] Lighthouse mobile ≥ 95 performance, 100 accessibility, 100 best practices, 100 SEO

**Handoff**
- [ ] Primary CTA is Home Depot, rendered via `hd()`
- [ ] UTMs and `data-hd` present; GA4 event fires
- [ ] Expectation-setting line under the CTA
- [ ] Deep link resolves to the right category, not a 404

---

## 16. Success metrics

| Metric | 90 days | 12 months |
|---|---|---|
| `hd_click` rate from category pages | Baseline established, +20% relative | +50% relative |
| Organic sessions to guide + need + room pages | +40% | +150% |
| Sample requests | 2–4% of category sessions | 4–6% |
| Trade applications | Baseline established | +100% |
| Commercial inquiries | Baseline established | +75% |
| Pages with valid JSON-LD | 100% | 100% |
| Mobile LCP / INP / CLS (75th pct) | ≤2.0s / ≤150ms / ≤0.05 | sustained |
| Lighthouse mobile perf, top 10 pages | ≥ 95 | ≥ 95 |
| AI images replaced with photography | Hero + 5 categories planned | Hero + top 5 shipped |

---

## 17. Decision log

| Decision | Choice | Why |
|---|---|---|
| Framework | Static HTML, keep Python build | 50 static marketing pages; a framework fixes none of the real failures |
| Design direction | Daylight Editorial | Light and weave are native to the category; supersedes "Atelier Grid" |
| Display face | Instrument Serif | Editorial presence without craft-fair softness (Fraunces retired) |
| UI face | Inter Tight | Neutral, crisp at micro-label sizes |
| Accent | Clay `#8C5A38` | Reads as material, not gold hardware |
| CTA colour | Home Depot orange, primary CTA only | Retail continuity; never decorative |
| Dark surfaces | Motorization + footer only | Daylight brand should not go dark globally |
| Motion | Five permitted cases | Ambient motion was reading as portfolio-site, not premium |
| Outbound rel | Followed, `noopener` | Intended retail path, not sponsored placement |
| Imagery | AI now, photography later, same shot list | Fastest route to the one thing that actually signals premium |
| Reviews | Removed until real | Faking social proof is disqualifying for a premium brand |
| Priority order | Imagery before layout | Layout was rebuilt twice without imagery; that is why it still reads dated |
