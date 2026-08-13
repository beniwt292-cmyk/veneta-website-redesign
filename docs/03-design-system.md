# Design System — "Editorial Daylight"

## Colour palette

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#141414` | Primary text, logo, footer base |
| `--ink-70` | `#4A4A48` | Secondary text |
| `--ink-45` | `#83837E` | Meta text, captions, labels |
| `--line` | `#E3DFD8` | Hairline rules, table borders, dividers |
| `--paper` | `#FFFFFF` | Primary surface |
| `--linen` | `#F7F4EF` | Alternating section background (warm neutral) |
| `--sand` | `#EDE6DA` | Cards, spec table header fill |
| `--daylight` | `#F2C230` | Brand accent (from logo). Small fills, underlines, active states |
| `--daylight-deep` | `#C99A15` | Accent hover / accessible accent text on light |
| `--slate` | `#2E3A3F` | Dark sections (motorization, pro hub) |
| `--sky` | `#8FA9B4` | Cool secondary, sparingly (from cellular product photography) |
| `--success` | `#2E6B4F` | "Cordless" / safety badges |

**Rules:** yellow never carries body text on white (fails contrast). Use `--ink` on `--daylight` for buttons. Maximum two accent uses per viewport.

## Typography

| Role | Font | Size (desktop / mobile) | Weight | Tracking |
|---|---|---|---|---|
| Display H1 | Canela, Freight Display, or Playfair Display | 64 / 38 px | 400 | −0.02em |
| H2 | same serif | 44 / 30 px | 400 | −0.01em |
| H3 | Neue Haas Grotesk / Inter | 24 / 20 px | 600 | 0 |
| Body | Inter | 18 / 17 px, 1.65 line-height | 400 | 0 |
| Small / spec | Inter | 15 px, 1.5 | 400-500 | 0 |
| Eyebrow / label | Inter | 12 px | 600 | 0.16em, uppercase |
| Button | Inter | 15 px | 600 | 0.04em, uppercase |

A serif display face paired with a neutral grotesque is what separates "editorial" from "template". Free substitutes: Playfair Display + Inter, or Fraunces + Inter.

## Spacing and layout

- 8 px base scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160.
- Max content width 1280 px; text measure capped at 68 characters (~640 px).
- 12-column grid, 32 px gutters desktop; 4-column, 20 px gutters mobile.
- Section vertical padding: 128 px desktop, 72 px mobile.
- Page gutters: 24 px mobile, 40 px tablet, 64 px desktop.

## Components

**Buttons**
- Primary: `--ink` fill, white text, 2 px radius, 14×28 px padding. Hover: `--slate`.
- Home Depot CTA: `--daylight` fill, `--ink` text, small store icon, always the highest-contrast element in view.
- Secondary: 1 px `--ink` border, transparent fill.
- Text link: `--ink` with a 1 px `--daylight` underline that thickens to 2 px on hover.
- Focus: 2 px `--slate` outline with 2 px offset, always visible.

**Product card**
Full-bleed 4:5 image, category name (H3), one-line benefit, "From $XX" meta, thin `--line` bottom rule. Image scales 1.03 over 400 ms on hover. Entire card is one link.

**Spec table**
`--sand` header row, hairline `--line` rows, monospaced-tabular numbers, sticky first column on mobile with horizontal scroll and a visible scroll hint.

**Best-for box**
`--linen` background, two columns: "Best for" (check icons, `--success`) and "Consider something else if" (dash icons, `--ink-45`). This is the trust component; use it on every product page.

**Disclosure (replaces tabs)**
Sections stay open by default on desktop with a sticky in-page anchor nav. On mobile they become accordions with real `<button aria-expanded>` semantics.

**Slat divider**
A section break made of 5 thin horizontal `--line` rules with decreasing opacity, echoing louvers. The site's one signature graphic device. Use it 2-3 times per page maximum.

**Badges**
Pill, 1 px `--line` border, 12 px uppercase label: `Cordless`, `Blackout`, `Motorized`, `Child & Pet Safe`, `Energy Efficient`, `Moisture Resistant`.

**Sticky mobile action bar**
Appears after 40% scroll: `Shop at The Home Depot` (primary) + `Order Free Samples` (secondary).

## Imagery direction

- Real rooms, natural daylight, one window treatment as the clear subject.
- Warm neutral interiors; avoid saturated colour blocking.
- Include at least one hand/scale shot per product (someone operating a cordless lift) to communicate ease.
- Detail macros for fabric and hardware, shot on `--linen`.
- Every image needs descriptive alt text naming the product, colour, and room.
- Aspect ratios: hero 21:9 desktop / 4:5 mobile; product card 4:5; gallery 3:2; detail 1:1.

## Motion

- Entrance: 16 px rise + fade, 320 ms, `cubic-bezier(0.2, 0.6, 0.2, 1)`, staggered 60 ms.
- Hover: 200 ms.
- No auto-advancing content anywhere.
- All motion disabled under `prefers-reduced-motion: reduce`.

## Accessibility requirements (acceptance criteria)

- 4.5:1 minimum contrast for text, 3:1 for large text and UI borders.
- Visible focus on every interactive element.
- One `h1` per page, no skipped heading levels, no body copy in heading tags.
- Skip-to-content link as the first focusable element.
- Touch targets 44×44 px minimum.
- Forms: persistent visible labels, inline errors tied with `aria-describedby`.
- Text over imagery always sits on a scrim or solid panel, never raw photography.
