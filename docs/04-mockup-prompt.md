# Mockup Build Prompt

Two prompts are provided.

- **Prompt A** is for an AI coding tool (Cursor, Claude Code, v0, Lovable, Bolt) to build an interactive, deployable mockup.
- **Prompt B** is for an image generation tool (Midjourney, Figma AI, GPT image tools) if you want static visual comps instead.

Copy the prompt block verbatim. Both assume `docs/03-design-system.md` as the source of truth for tokens.

---

## Prompt A — Interactive mockup (recommended)

````
ROLE
You are a senior product designer and front-end engineer. Build a high-fidelity, deployable
mockup of a redesigned website for VENETA™ Window Fashions (venetawindowfashions.com), a
custom window treatment brand (blinds, shades, shutters) owned by Richfield Window Coverings.

CRITICAL BUSINESS CONTEXT
Veneta does NOT sell online. All purchases happen at The Home Depot (homedepot.com and in
store). The site's only job is to make an unsure shopper confident, then hand them off to
Home Depot at the moment of confidence. Every screen must have one obvious next step, and
the Home Depot call to action must be the highest-contrast element in the viewport at all times.

WHAT IS WRONG WITH THE CURRENT SITE (do not repeat these mistakes)
- Auto-rotating hero carousel with marketing headlines baked into JPEG images.
- No H1 on any page; body copy marked up as <h6>.
- Nav labels that lead to 404s; "Design Center" and "Information" as menu labels.
- 4.7 MB homepage, 73 JS files, 25 stylesheets, 118 requests.
- 58% of images missing alt text.
- Product specs hidden behind tab widgets with machine-generated anchor IDs.
- No price signal, no reviews, no product finder, no store locator, no search.
- Generic value props: "Technical Innovation", "High Quality", "Premium Materials".
- Footer still says © 2022; blog abandoned since 2020.

TECH REQUIREMENTS
- Next.js 15 App Router, TypeScript, Tailwind CSS v4, deployable to Vercel with zero config.
- No UI kit dependency beyond Tailwind; hand-build components. Lucide for icons.
- Fully responsive: design mobile-first, verify at 390, 768, 1024, 1440, 1920 px.
- next/image with explicit width/height, AVIF/WebP, lazy-loading below the fold.
- Semantic HTML: exactly one <h1> per page, correct heading order, <p> for body copy,
  real <button aria-expanded> for disclosures, skip-to-content link, visible focus rings,
  descriptive alt text on every image, WCAG 2.2 AA contrast.
- Respect prefers-reduced-motion. No auto-advancing content anywhere.
- Use placeholder imagery from a photo service or solid <div>s with a descriptive
  data-shot-note attribute describing the intended photograph.

DESIGN LANGUAGE — "EDITORIAL DAYLIGHT"
Feel: a well-lit room in an architecture magazine. Generous white space, large calm
photography, hairline rules, confident editorial typography. NOT big-box retail, NOT a
purple-gradient SaaS page, NOT a template.

Colour tokens:
  --ink #141414        --ink-70 #4A4A48     --ink-45 #83837E
  --line #E3DFD8       --paper #FFFFFF      --linen #F7F4EF
  --sand #EDE6DA       --daylight #F2C230   --daylight-deep #C99A15
  --slate #2E3A3F      --sky #8FA9B4        --success #2E6B4F
Rules: yellow is an accent only (buttons, underlines, active states), never a large fill and
never behind body text. Maximum two accent uses per viewport.

Type: Playfair Display (or Fraunces) for display/H1/H2 at 400 weight with tight tracking;
Inter for everything else. H1 64/38 px, H2 44/30 px, H3 24/20 px, body 18/17 px at 1.65,
eyebrow labels 12 px uppercase 0.16em tracking.

Layout: 8 px spacing scale, 1280 px max width, text measure capped at 68 characters,
section padding 128 px desktop / 72 px mobile.

Signature graphic device: the "slat divider" — five thin horizontal rules with decreasing
opacity, echoing window louvers. Use it 2-3 times per page maximum as a section break.

Motion: 16 px rise + fade on scroll entrance, 320 ms, staggered 60 ms; 200 ms hovers. Nothing more.

PAGES TO BUILD (5 routes)

1) HOME — "/"
   a. Header: logo left; nav Products / Shop By / Innovation / Support / Where to Buy;
      search icon; then a filled --daylight "Shop at The Home Depot" button. Sticky on
      scroll with a subtle bottom hairline. Mobile: hamburger opening a full-screen panel.
   b. Hero (full-bleed, 21:9 desktop / 4:5 mobile): real text over a scrim, not baked in.
      H1 "Light, exactly how you want it." Sub: "Custom blinds, shades and shutters
      engineered to fit your windows — cordless by design, available at The Home Depot."
      Primary CTA "Find your window treatment" → Product Finder. Secondary "Shop at The
      Home Depot". Below the fold edge, three small trust items: "Cordless-first safety",
      "Fits skylights, arches & patio doors", "Free fabric samples".
   c. Product Finder entry band: three visible selects (Which room? / What matters most?
      / What look?) plus a "See my matches" button. It must feel like the site's front door.
   d. Category grid: 8 cards — Cellular Shades, Roller & Solar, Roman Shades, Faux Wood
      Blinds, Shutters, Sheer Shades, DualDrape™, Vertical Blinds. Each card: 4:5 image,
      name, one-line benefit, "From $XX", 2-3 badges. Image scales 1.03 on hover.
   e. "Engineered to fit" band on --linen: the differentiator. Show a real spec excerpt
      (e.g. "Cellular, cordless: width 8.5"-96", height 10"-86"" and "ClearFit™ skylight:
      width 8.5"-59", height 6"-120"") styled as a beautiful table, with the line
      "We publish every dimension, so you order once and it fits." CTA to the measuring guide.
   f. Safety story (split layout, real photograph of a nursery): "Cordless by design,
      because kids and pets don't read labels." Bullet the tested/certified detail. CTA
      "See our safety standards."
   g. Motorization band on --slate (dark section): ShadeAuto™ Hub, TruQuiet™ motors,
      RevitaCharge™ charging. Three concrete benefits: control multiple windows, works with
      compatible smart home devices, automated scheduling. IMPORTANT: state compatibility
      once, precisely, and link to a single compatibility page — the current site
      contradicts itself on Alexa support and this must not be repeated.
   h. Shop by Room: horizontal scroll rail (manual, no autoplay) — Living Room, Bedroom,
      Nursery, Kitchen, Bath, Home Office, Patio Doors, Skylights, Arched Windows.
   i. Social proof: 3 review cards with star ratings and "Verified at The Home Depot",
      plus an aggregate rating line. Use realistic placeholder review copy.
   j. Support strip: three links — How to Measure, How to Install, How to Clean & Care —
      each with a step count and estimated time.
   k. Newsletter: designed, not default. Value proposition ("Colour trends, care tips and
      new collections — once a month"), single email field, privacy line, real button.
   l. Footer: four columns (Products / Shop By / Support / Company), phone
      1-855-558-1222, help@venetawindowfashions.com, social icons, legal row with a
      current copyright year rendered dynamically, and an Accessibility Statement link.
   m. Sticky mobile action bar appearing after 40% scroll: "Shop at The Home Depot" +
      "Order free samples".

2) PRODUCT CATEGORY — "/products/cellular-shades"
   One continuous scrolling page. NO TABS. Sticky in-page anchor nav (Overview, Features,
   Colours & Fabrics, Options & Sizes, Measure, FAQ) that highlights the active section.
   - Breadcrumb: Home / Products / Cellular Shades.
   - Hero: H1 "Cellular Shades", one benefit-led sentence, "From $XX at The Home Depot",
     star rating, badges, primary Shop CTA, secondary "Order free samples".
   - "Best for / Consider something else if" box on --linen. Two honest columns.
   - Signature features: ClearFit™, Day & Night, cordless lift, motorized option — each
     with an image and a single clear claim.
   - Colours & fabrics: swatch grid grouped by opacity (Sheer / Light Filtering / Blackout)
     with a note that free samples are the accurate way to judge colour.
   - Options & Sizes: a proper spec table — cell size (3/8", 9/16", 3/4", 1 1/4", double
     cell 1/2" and 3/4"), lift type, and min/max width and height for each configuration.
     Sticky first column with horizontal scroll on mobile.
   - Measure: inside vs outside mount, three-point measuring, the shortest-width /
     longest-height rule, with a "Download the printable guide" link.
   - FAQ: 8-10 accordion items with real question text, marked up for FAQPage schema.
   - Related products: Roller & Solar, Sheer Shades, Roman.
   - Closing CTA band.

3) PRODUCT FINDER — "/finder"
   Three steps with a visible progress indicator. Step 1 Room (9 image tiles). Step 2 Need
   (multi-select: block light, save energy, keep privacy, protect from UV, child & pet safe,
   oversized window, moisture resistant). Step 3 Look (soft folds, clean modern, natural
   wood, sheer). Results page: 2-3 recommended products, each with a "Why this matches"
   explanation referencing the user's answers, plus Shop and Sample CTAs. Fully keyboard
   navigable; state in URL query params so results are shareable.

4) SUPPORT — HOW TO MEASURE — "/support/how-to-measure"
   Breadcrumb, H1, estimated time, tools needed ("Use a metal tape measure — cloth tapes
   stretch"), a mount-type chooser (Inside / Outside), numbered steps with a large diagram
   per step, a common-mistakes callout, a printable PDF link, a video placeholder, and a
   "Ready to order?" CTA band.

5) WHERE TO BUY — "/where-to-buy"
   Two clear paths: "Shop online at The Home Depot" (deep links per product category) and
   "See it in store" (store locator input, in-store availability note). Plus a free-samples
   panel explaining the 10-swatch process, and a note for trade customers.

DELIVERY
- Shared components: Header, MobileNav, Footer, Button, ProductCard, SpecTable, BestForBox,
  Disclosure, SlatDivider, Badge, ReviewCard, StickyActionBar, NewsletterForm, Breadcrumb.
- Tailwind theme configured with the tokens above; no hard-coded hex values in components.
- Add data-analytics attributes on every Home Depot outbound link so the handoff is
  measurable, plus a comment noting each should fire a GA4 conversion event.
- Include a short README explaining the routes, the design rationale, and how to swap in
  real photography.
- Performance budget: under 900 KB per page, under 35 requests, under 150 KB JS.

ACCEPTANCE CHECKLIST (verify before you finish)
[ ] Exactly one H1 per page; no body text inside heading tags
[ ] No text rendered inside images
[ ] Home Depot CTA visible in every viewport on every page
[ ] Every image has descriptive alt text
[ ] Keyboard-only pass completes the Product Finder and all accordions
[ ] Contrast checked: 4.5:1 text, 3:1 UI
[ ] No horizontal overflow at 390 px
[ ] No auto-rotating content
[ ] Footer copyright year is dynamic
[ ] Smart-home compatibility is stated once, in one place, consistently
````

---

## Prompt B — Static visual comps (image generation)

````
A high-fidelity website homepage design mockup for VENETA, a premium custom window
treatment brand. Editorial magazine aesthetic: generous white space, warm neutral palette
of white, linen beige (#F7F4EF) and soft sand (#EDE6DA), with charcoal (#141414) text and
a single precise golden-yellow accent (#F2C230) used only on the primary button.
Typography pairs a refined serif display headline with a clean neutral sans-serif for body
copy. Full-bleed hero photograph of a sunlit modern living room with pale cellular shades
half-lowered, soft directional daylight, minimal Scandinavian furniture. Overlaid on a
subtle dark scrim: a large serif headline, one short line of supporting copy, and two
buttons. Below the hero, a three-field guided product finder bar, then a clean four-across
grid of product cards with 4:5 photography, thin hairline dividers, and small uppercase
labels. Flat vector UI presentation, straight-on view, no browser chrome, no device frame,
crisp and realistic, high detail, 16:9.
````

Variants to request: (1) desktop homepage above the fold, (2) full-length desktop homepage,
(3) mobile homepage, (4) product detail page with a visible spec table, (5) dark motorization
section. Keep the prompt identical and change only the final scene description so the set
looks like one system.
