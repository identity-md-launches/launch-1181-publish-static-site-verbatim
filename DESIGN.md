# DESIGN.md — Pepeolithic by ZTO (cave-site mirror)

This documents the design **as implemented in the published source**, `dist/index.html`. The site is a
verbatim mirror of an upstream single-page site; every value below was extracted from that file
(all CSS lives in the single `<style>` block, `dist/index.html:13-393`). Nothing here was designed in this
repository, and the mirror task forbids changing any of it. Treat this as a map for a future page that must
belong to the same product, not as a proposal.

Line numbers refer to `dist/index.html`.

## Overview

Audience: ZTO / IMD community members deciding whether to buy or claim a "Pepeolithic" cave painting during a
seven-day on-chain sale. Visual character: a dark, torch-lit cave. Backgrounds are near-black browns, text is
chalk-coloured, accents are ochre and ember red, display type is a distressed "Rubik Dirt" face, and every card
corner is an irregular hand-cut blob rather than a clean radius. Motion is used as "juice" (embers, flicker,
scroll reveal, a pointer-following glow) and is fully switched off under `prefers-reduced-motion`.

System-wide rules (reusable on any page):

- One container width (`.wrap`), one body size (17px), one label style (`.label`), one card surface (`.slab`).
- Hierarchy is carried by **font family and colour**, not weight: display type is Rubik Dirt at a single 400 weight,
  UI labels are Space Mono uppercase with wide tracking, body is Space Grotesk.
- Page-specific arrangements that are *not* rules: the hero's torch/print stamping, the 7-column "teeth" price chart,
  the 21-cell cave map, the easter-egg layer (`.dark`, `.rain`, `.peek`, `#eggs`).

## Colors

Tokens are CSS custom properties on `:root` (`dist/index.html:19-24`). Hex is the canonical notation; translucent
variants are written inline as `rgba()` of the same hues.

| Token | Value | Job |
| --- | --- | --- |
| `--rock-0` | `#0d0805` | Page background (`body`), nav backdrop base, overlay tints |
| `--rock-1` | `#17100a` | Darker tonal layer (unused directly by selectors; kept for the ramp) |
| `--rock-2` | `#241810` | Mid rock tone (used via `rgba(36,24,16,.9)` in `.deal`) |
| `--rock-3` | `#3a2717` | Lightest rock tone; top of the `.slab` gradient |
| `--chalk` | `#efe6d6` | Primary text, `h3`, button text |
| `--chalk-dim` | `#b9aa90` | Secondary text, nav links, captions, `.dim` |
| `--ochre` | `#d9a441` | Label colour (`.label`), arrows, outlines, key accents |
| `--ochre-hi` | `#f2c462` | Headings (`h2`), links (`a`), numbers, "lit" states, nav logo |
| `--red` | `#b5482a` | Selected state fill (`.states button.on`), tag chips, toast links |
| `--red-hi` | `#d4633d` | Primary action (`.btn.red`), live dot, "gathering" highlight, errors in map/teeth |
| `--amber` | `#f5a623` | Logo arrow only |
| `--char` | `#15100c` | Text on light fills (`.navbuy em`, `.btn` default, `.split`, `.end .n`) |
| `--moss` | `#a5d78a` | Success text (`.seatout b`) |

Status colours that exist: success = `--moss`, error = `#ff8a65` (`.err`, line 138) and `--red-hi` for the
"not on the list" seat result. Focus colour: none is defined; the site relies on the browser default focus ring
(see `VALIDATION.md`, finding A-5).

Borders are always translucent ochre or chalk: `rgba(217,164,65,.14–.45)` for separators and card edges,
`rgba(239,230,214,.2–.3)` for ghost buttons and chips. No light theme exists; do not add one.

Contrast ratios computed from these source values are tabulated in `VALIDATION.md`; every text-on-rock pair
exceeds 5:1, and the one failing pair is `#fff3e6` on `--red-hi` in `.btn.red` (3.4:1). Text on the hero image
sits on a dark radial overlay (`.hero .torch`, line 76-78) plus text-shadow, so hero contrast depends on the
photo and was not measured.

## Typography

Local fonts, loaded with `font-display: swap` (`dist/index.html:14-17`, files in `dist/fonts/`):

| Family | File | Weights supplied | Role |
| --- | --- | --- | --- |
| Rubik Dirt | `fonts/rubik-dirt.woff2` | 400 only | Display: `h1`, `h2`, big numbers, prices, blockquotes, arrows |
| Space Grotesk | `fonts/space-grotesk.woff2` | variable 300–700 | Body, `h3`, captions, `.rday b` |
| Space Mono | `fonts/space-mono.woff2` | 400 | Labels, buttons, data, inputs, footer |
| Space Mono | `fonts/space-mono-bold.woff2` | 700 | Bold buttons/chips, `.auction .price small` |

Fallback stacks: `"Space Grotesk", system-ui, sans-serif` (body); `"Rubik Dirt", "Space Grotesk", sans-serif`
(headings); `"Space Mono", ui-monospace, monospace` (mono).

Roles and sizes (all from the stylesheet):

- **Body**: `17px/1.55` Space Grotesk (`body`, line 29). `.lede` is `1.16rem`, max measure `56ch`.
- **H1** (hero only): `clamp(2.6rem, 10.4vw, 8.6rem)`, line-height `.92`, `--ochre-hi`, SVG `#rough` filter (line 88).
- **H2** (section titles): `clamp(2rem, 5.2vw, 3.5rem)`, line-height `1.02`, `--ochre-hi`, letter-spacing `.01em` (line 41).
- **H3**: `700 1.1rem/1.25` Space Grotesk, `--chalk` (line 42).
- **Label** (`.label`, line 38): `400 11px/1.4` Space Mono, `letter-spacing .18em`, uppercase, `--ochre`. Used as
  section kickers and card eyebrows.
- **Nav links**: `11px` Space Mono, `.14em` tracking, uppercase (line 63).
- **Buttons**: `700 14px` Space Mono, `.04em` tracking (line 67).
- **Data / numbers**: Rubik Dirt 400 at `30px` (`.stats b`), `2.7rem` (`.auction .price b`), `1.7rem` (`.kv b`),
  `clamp(2.6rem,5.4vw,3.9rem)` (`.tile b`). Small numeric helpers use Space Mono `10–13px`.
- **FAQ**: `summary` `700 1.05rem` Space Grotesk; answers `--chalk-dim`, max `70ch` (lines 351-355).

Wrapping rules: `.auction .what, .auction .when { overflow-wrap: anywhere }` (line 121) protects the narrow
auction card; `footer .mono { word-break: break-all }` (line 358) for addresses; `.split div { white-space: nowrap }` (line 328).
Headings use the `#rough` SVG displacement filter (inline `<svg>` at lines 398-402) for a chalk edge.

## Layout

- **Container**: `.wrap { width: min(1120px, calc(100% - 32px)); margin: 0 auto }` (line 36). Every section and
  the nav use it; 16px side gutters below 1152px.
- **Section rhythm**: `section { padding: 84px 0 12px }`, `.head { gap 12px; margin-bottom 28px }` (lines 46-47).
  Mobile: `section { padding-top: 60px }`.
- **Spacing scale in use**: 4, 6, 8, 10, 12, 14, 16, 18, 22, 28, 34, 40, 60, 84, 90px. Cards use `18px` or `22px`
  padding; grids use `gap: 18px` (`.grid`) or `14px` (`.picks`, `.caves`, `.clockrow`).
- **Grids**: `.grid.g2/.g3/.g4` equal columns (line 154); feature grids `.live 1.15fr 1fr`, `.levels 1fr 1.25fr`,
  `.piece 1fr 1.1fr`, `.anatomy 1fr 48px 1.35fr`, `.comic 1fr 34px 1fr 34px 1fr`.
- **Sticky nav**: `nav { position: sticky; top: 0; z-index: 50 }`, 56px tall, blurred `rgba(13,8,5,.86)` (lines 57-58).
- **Hero**: `height: min(calc(100vh - 56px), 880px); min-height: 640px`, two-column `minmax(0,1fr) 452px` with the
  auction card on the right (lines 75-99). Stats row is absolutely positioned at the bottom.

Breakpoints (lines 151, 371-391):

| Width | Changes |
| --- | --- |
| `≤ 900px` | All multi-column grids collapse to one column (`.g4` to two); nav text links hidden, `.navbuy` stays; hero becomes auto-height with `.hero .left { display: contents }` and explicit `order` so the sub-copy, auction card, CTAs and hint stack; stats row becomes static; `.glow` hidden; `.ramp` 4 columns, `.strip` 5, `.steps` 2, `.clockrow` 2 |
| `≤ 720px` | `.kilnslab` single column |
| `≤ 520px` | `.wide` text hidden in `.navbuy`; auction body `88px 1fr`; auction price `2.1rem`; state-button caption hidden; `.cave` single column |

Overflow: `body { overflow-x: hidden }` (line 28) and the marquee band `.band { overflow: hidden }` with a
`width: max-content` `.track`. The `.auction` card sets `min-width: 0; max-width: 100%` on itself and its grid
children (line 106) so long values cannot widen the hero column.

Observed in the browser (headless Chromium, see `VALIDATION.md`): widths 1366, 900, 390 and 320 CSS px were
rendered with no horizontal scroll; the collapse described above was confirmed at 900, 390 and 320. Known
exception: at 320px the auction card's price caption overflows the card (finding L-1).

## Elevation & Depth

Depth is tonal, with a few real shadows:

- **Surface card** `.slab` (line 102): gradient `160deg rgba(58,39,23,.72) → rgba(30,20,12,.82)`, 1px border
  `rgba(217,164,65,.17)`, inset highlight `0 1px 0 rgba(255,220,160,.06)`.
- **Emphasised card** `.auction` (line 105): darker gradient, brighter border `rgba(242,196,98,.45)`, stacked
  outer shadows.
- **Images** `.paint` (line 141): `0 0 0 1px rgba(217,164,65,.2), 0 18px 40px rgba(0,0,0,.55)`; hover adds an
  ochre glow. Selected/"gathering" images use a 2px `--red-hi` ring.
- **Primary button** `.btn.red` (line 70): hard offset shadow `0 3px 0 #6d2412` plus soft `0 10px 24px rgba(0,0,0,.45)`;
  `:active` translates 2px down to "press".
- **Stacking** (lines 52-54, 57, 144, 363-368): `.glow` z 0 → content z 1 → nav z 50 → `.dark` 55 → `.rain` 58 → `.toast` 60 → `.sparks` 95.

## Shapes

Two shared radius tokens produce the hand-cut look (line 23):

- `--slab: 20px 28px 22px 30px / 28px 20px 30px 22px` for cards (`.slab`, `.piece .shot`, line 311).
- `--blob: 26px 34px 28px 38px / 34px 26px 38px 28px` for artwork (`.paint`).

Smaller controls use fixed irregular radii: buttons `14px 18px 14px 20px / 18px 14px 20px 14px`, slots/thumbs
`12px 16px 12px 18px / 16px 12px 18px 12px`, tiles `4px 6px 4px 7px`. Plain pills/chips use symmetrical `10–12px`,
small badges `5–8px`, dots are circles. The `.deal` quote block (line 171) has its own large blob
(`40px 60px 46px 64px / 60px 40px 64px 46px`). Keep new cards on `--slab` and new imagery on `--blob`.

## Components

All components are CSS classes plus inline-script rendering in `dist/index.html`; there is no component library.

- **Nav** (`nav`, lines 57-66, markup lines 414-423): sticky bar with `.logo` button, `.links` anchor list
  (hidden ≤900px), and `.navbuy` live-price pill whose content is rewritten every second by `render()`
  (line ~1278). Text links use `.14em` tracked Space Mono.
- **Buttons** `.btn` (line 67-71): default = ochre fill, `--char` text; `.ghost` = translucent dark with 1px chalk
  ring; `.red` = primary action; `[disabled]` = 55% opacity + `not-allowed`. Hover brightens 8%, active scales
  `.96`. `.chip` (line 72) is the small secondary (used for "Check" in the seat lookup).
- **Labels** `.label` (line 38): eyebrow/kicker for sections and cards.
- **Card** `.slab` (line 102) with variants `.auction` (live sale card, rendered by `card()`), `.panel` (sale
  panel with `.tag` corner badge, lines 321-322), `.exp` (174), `.teeth` (243), `.tile` (212), `.cave` (289), `.pick` (258).
- **Auction state dot** `.dot` (line 109): pulsing `--red-hi` when live, `.off` grey when not.
- **Progress bar** `.fall` (line 126): 6px track with red→ochre gradient fill; width animated over 1s.
- **Seat check** (markup line 665, styles 332-335): `input#seatin` (placeholder is the only label; see
  validation finding A-1) + `.chip#seatgo`; result in `.seatout` with `b` (moss) or `b.no` (red).
- **Map cells** `.cells i` (lines 295-299): 21-per-row dot grid; `.sale` red tint, `.g` rotated square,
  `.sel` white outline; clicking writes to `.mapinfo`.
- **FAQ** `details/summary` (lines 351-355): native disclosure, `+`/`–` glyph via `::after`.
- **Toast** `.toast[role=status]` (lines 363-365, markup line 728): fixed bottom centre, slides in on `.show`.
- **Image tile** `.paint` (line 141-148): blob-clipped square image with 3D tilt on pointer move.

Keyboard/focus: all interactive elements are native `a`, `button`, `input`, `summary`. No custom focus ring is
defined, so the browser's default `:focus-visible` ring applies. Map cells (`.cells i`, line 295) and `.end` rows (line 301) are
`<i>`/`<div>` elements with click handlers only; they are not keyboard reachable (validation finding A-2).

Loading/empty/error states that exist: the auction card renders "before", "waiting", "mystery", "revealed",
"floor", "soldout", "over" and "leftover" phases from `CONFIG` and chain reads; `.err` shows wallet/RPC errors;
the seat check shows an explicit "not on the list" state.

## Do's and Don'ts

- **Do** start a new page from `nav` + `.wrap` + `section > .head(.label + h2 + .lede)` + `.slab` cards.
- **Do** keep display type Rubik Dirt 400 in `--ochre-hi`; use Space Mono uppercase `.label` for kickers;
  never bold Rubik Dirt (the file ships only 400).
- **Do** choose actions by weight: `.btn.red` for the one consequential action, `.btn` for secondary, `.btn.ghost`
  for navigation-like actions, `.chip` for inline tools.
- **Do** put all animation behind the existing `prefers-reduced-motion` block (line 392) and the `still` flag in script.
- **Don't** introduce a symmetrical radius for cards or art, a second accent hue, a light theme, or a
  non-mono numeral style.
- **Don't** add dividers to group content; the system groups with space and translucent surfaces.
- **Don't** change `dist/` by hand: it is a verified mirror. New pages belong upstream, then re-mirror.

Recipe for one more page: copy the `<head>` (fonts, `:root`, global rules through line 50), the `nav` and
`footer`, then compose `section#id > .wrap > .head + .grid.g3 > .slab`. Keep images square in `.paint`.
