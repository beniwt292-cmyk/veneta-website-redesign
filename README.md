# VENETA™ Window Fashions — Website Redesign

Audit, redesign strategy, design system, content guide and a deployable homepage mockup for
[venetawindowfashions.com](https://www.venetawindowfashions.com/).

## What's here

| File | What it is |
|---|---|
| [`docs/01-website-audit.md`](docs/01-website-audit.md) | Full audit: severity-ranked findings across UX, content, technical, SEO and accessibility, with measured numbers |
| [`docs/02-redesign-strategy.md`](docs/02-redesign-strategy.md) | Positioning, audience jobs, new information architecture, design direction, tech plan, redirect map, phasing |
| [`docs/03-design-system.md`](docs/03-design-system.md) | "Editorial Daylight" design system: colour, type, spacing, components, imagery, motion, accessibility criteria |
| [`docs/04-mockup-prompt.md`](docs/04-mockup-prompt.md) | The copy-paste build prompt for an AI coding tool, plus an image-generation prompt for static comps |
| [`docs/05-content-guide.md`](docs/05-content-guide.md) | Page-by-page copy, replacement value props, product page template, copy fixes, SEO patterns |
| [`docs/06-implementation-roadmap.md`](docs/06-implementation-roadmap.md) | Phases, owners, pre-launch QA checklist, first-90-days plan |
| `index.html` | Static homepage mockup demonstrating the design system. Deploys to Vercel with zero config |
| `assets/img/` | Optimised WebP imagery for the mockup |

## The short version

The current site is a 2019 WordPress brochure (Stockholm theme + WPBakery) that has been
patched rather than redesigned. Measured on the homepage:

- **~4.7 MB** transferred across **~118 requests**
- **73 JavaScript files** (2,390 KB) and **25 stylesheets** (1,425 KB)
- **0 `<h1>` elements** on any page tested; body copy marked up as `<h6>`
- **22 of 38 images** missing alt text
- Three primary nav labels resolve to **404** pages
- The homepage promotes Alexa/Google support for ShadeAuto™ Hub while the Cellular FAQ says
  motorization "is not compatible with Alexa or any smart device"
- Footer still reads **© 2022**; the blog stopped in 2020

Meanwhile the site's real asset — the most detailed product specifications in the category
(exact width and height ranges for every cell size and lift system) — is buried behind tab
widgets.

**The strategic reframe:** Veneta doesn't sell online, Home Depot does. So the site's job is
not to be a store, it's to be the most trustworthy *decision engine* in the category — then
hand the confident shopper to Home Depot and measure that handoff.

## The mockup

`index.html` is a single-file, dependency-free homepage mockup: sticky Home Depot CTA,
guided product finder, eight-product grid, a published-specs band, cordless safety story,
dark motorization section with a single source of truth on compatibility, room rail,
reviews, support strip, and a designed newsletter. One `h1`, alt text on every image, no
auto-rotating content, `prefers-reduced-motion` respected, ~600 KB total.

Deploy: point Vercel at this repo as a static site (no build step required).

## Licence / notes

Photography in `assets/img/` is Veneta's own product imagery, optimised to WebP, used for
internal mockup purposes only. Prices, review copy and ratings are placeholders.
