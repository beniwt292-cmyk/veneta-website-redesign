# Design direction v2 — "Atelier Grid"

Reference point: the curated modern ecommerce work collected in the Land-book
Ecommerce gallery. The shared traits of that work, and how each one is applied
here.

| Gallery trait | Applied to Veneta |
| --- | --- |
| Bone or off-white canvas, never pure white | `--paper:#F2F0EA` across every page; `--card:#FBFAF6` for raised panels |
| Oversized editorial display type | Instrument Serif, `h1` up to 104px, line-height 0.92, tracking -0.028em |
| Micro-label secondary voice | Inter Tight, 10-11px, 0.16-0.22em tracking, uppercase, used for nav, eyebrows, prices, meta |
| Hairline grid instead of shadows | `section + section` gets a 1px rule; cards, tables, panels and media all carry a 1px `--line` border; radius is 0 everywhere |
| One restrained accent | Burnt clay `#8E5A3C`, used only for eyebrow marks, the italic word in a headline, micro-labels and the primary button |
| Full-bleed hero, type on the baseline | 100svh image, slow 30s Ken Burns, headline parked bottom-left, trust row on a hairline above the fold edge |
| Marquee ticker | Olive-black band under the hero, six trust statements, 42s loop, pauses for reduced-motion users |
| Numbered product index | CSS counter prints `01`-`08` on each product photo |
| Reveal-on-hover product action | A `View` plate slides up inside the photo |
| Oversized wordmark in the footer | `VENETA` at up to 240px, outlined in 1px, clipped by the page edge |

## Tokens

```
--ink        #0E0E0B      --paper   #F2F0EA
--ink-70     #4C4C43      --card    #FBFAF6
--ink-45     #8B8A7E      --linen   #E8E5DC
--ink-25     #B6B4A8      --sand    #DEDACF
--line       #D6D2C6      --noir    #15160F
--line-soft  #E3DFD4      --clay    #8E5A3C
                          --clay-deep #6E432B
                          --clay-soft #D6BEAB
```

Type: `Instrument Serif` (display, roman + italic), `Inter Tight 300-600`
(everything else).

## What changed from v1

* Fraunces and antique brass are gone. Fraunces read soft and craft-fair at
  large sizes; the brass read closer to gold hardware than to daylight.
* Every corner radius, drop shadow and pill badge was removed. Surfaces are now
  defined by hairlines, which is what makes the gallery references feel precise.
* The headline scale roughly doubled, and body copy shrank slightly. The
  contrast between the two is the design.
* Sections no longer alternate loudly between white and cream. The canvas is one
  bone tone, and separation comes from rules plus two olive-black bands.
* Vertical rhythm is looser: `clamp(72px, 8vw, 140px)` per section.

## Layering

`assets/css/veneta.css` is built by concatenating, in order:

1. `build/base.css` — structure and layout
2. `build/extra.css` — interior page components
3. `build/luxe.css` — v1 refinements still in use (mega menu, search, filters)
4. `build/gallery.css` — this direction, which retunes the tokens and restyles
   every signature component

Rebuild with `python3 build/make.py`.
