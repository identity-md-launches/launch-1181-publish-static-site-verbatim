# Validation record — ZTO cave-site verbatim mirror

Date: 2026-10-09. Worker-side report; not an independent certification.

## 1. Scope and assumptions

- **Deliverable:** `dist/` is a byte-for-byte mirror of the upstream single-page site, with three edits on the
  `const CONFIG =` line of `dist/index.html:740`. The brief forbids any other change, so this review **records**
  findings and does not fix them. "Fixes applicable" therefore means: none are applicable; all are reported
  upstream-ready with `file:line`.
- **Pages/flows reviewed:** the one page (`dist/index.html`). Primary interactions: nav anchors, sale card
  countdown, seat-list check (`#seatin`/`#seatgo`), cave map cell selection (`.cells i` → `#mapinfo`), FAQ
  disclosures, keyboard walk. Wallet connect / buy flows were **not** exercised (they require an injected
  Ethereum wallet; the page shows a "No wallet in this browser" toast otherwise).
- **State observed:** with `start: 1791810000` the page is in the pre-sale "before" phase: countdown
  "Opens in 68:46:xx", "cave 1 opens Mon, Oct 12, 9:00 AM EDT", contract address shown in the footer and in
  the card header ("Ethereum · 0x7659…2028"), `preview: false` so the fake-sale state buttons are absent.
  Live-sale phases (line/floor/soldout/over/leftover) were not observable and were not reviewed in the browser.
- **Variants:** no theme or locale variants exist. Reduced-motion is supported and was checked.
- **Exclusions:** no screen-reader session, no native browser zoom, no physical device, no cross-browser run
  (Chromium only).

## 2. Coverage (six domains)

| Domain | Status | Inspected / evidence |
| --- | --- | --- |
| Accessibility | Checked | Native elements audit from source; keyboard walk (12 Tabs) with `:focus-visible` true on each stop; Enter on a nav link navigates (`#proof`, scrollY 2177); Space opens a FAQ `details`; Enter in `#seatin` runs the check; landmarks (`nav`, `header`, `footer`, 1×h1, 13×h2, 15×h3, no `main`); reduced-motion context: `.hero .torch` and `.track` animation `none`, `.reveal` opacity 1, scroll-behavior auto. **Unperformed:** screen reader, native 200% zoom, automated axe-style scan. |
| Layout | Checked | Rendered at 1366×900, 900×900, 390×844, 320×568. `scrollWidth == innerWidth` at all four (no horizontal scroll). Nav links hide ≤900; hero collapses to one column (`heroRowCols` "868px" at 900, "628px 452px" at 1366). Screenshots in `artifacts/screenshots/`. |
| Writing | Checked | Source read of all visible copy, button labels and seat-check messages; rendered messages captured for the three seat-check outcomes. |
| Typography | Checked | `document.fonts` reports all four faces `loaded`; computed body font "Space Grotesk", h1 "Rubik Dirt"; h1 137.6px at 1366 / 93.6px at 900, h2 56px / 46.8px. Weights requested in CSS exist in the shipped files (Mono 400 + 700 files, Grotesk variable 300–700, Dirt 400 only). |
| Colors | Checked | Contrast computed from source hex values for 18 identified pairs (table below). Pairs over photos (hero), gradients with noise texture, and translucent overlays were composited over `--rock-0` only; real rendered pixels were not sampled. |
| UI | Checked | Button variants and disabled state (opacity .55 + `not-allowed` + text "Opens in …"), `.dot.off` state, FAQ `+`/`–` affordance, toast `role=status`. Hover tilt/sparks observed only via source. |

## 3. Findings (not fixed — verbatim mirror)

| ID | Sev | Domain | Location | Evidence | Impact / correction (for upstream) |
| --- | --- | --- | --- | --- | --- |
| L-1 | MEDIUM | Layout | `dist/index.html:123` (`.auction .price` flex row) and `:391` (520px rule) | `artifacts/screenshots/top-320.jpg`: at 320px the caption "until cave 1 opens" renders outside the card's right edge, partly clipped by `body { overflow-x: hidden }`. | Secondary caption unreadable on the narrowest phones. Allow `.price` to wrap (`flex-wrap: wrap`) or drop the 88px thumbnail column below ~360px. |
| C-1 | MEDIUM | Colors | `dist/index.html:70` (`.btn.red`) | `#fff3e6` on `#d4633d` = **3.4:1** at 14px bold (not large text). | Primary action label below 4.5:1. Darken the fill toward `--red` (`#b5482a`, 4.9:1) or use `--char` text. |
| A-1 | MEDIUM | Accessibility | `dist/index.html:665` (`<input id="seatin" placeholder="0x… is my wallet on the list?">`) | No `label`, `aria-label` or `aria-labelledby`; placeholder is the only name and disappears on input. | Add a visually-hidden label or `aria-label="Wallet address"`. |
| A-2 | MEDIUM | Accessibility | `dist/index.html:295-299` (`.cells i`), `:301` (`.end`), markup `:612` (`#mapinfo`), cells rendered by script | Map cells and the "Zero/One" rows are `<i>`/`<div>` with click handlers only; not in the Tab order; `#mapinfo` is not a live region. | Keyboard users cannot explore the 737 map. Render cells as `<button>` and add `aria-live="polite"` to `#mapinfo`. The primary task (check seat, read sale) remains keyboard-reachable, hence MEDIUM. |
| W-1 | LOW | Writing | `dist/index.html:1216` (`Opens in …` buy button) and the `seatBtn` ghost button rendered beside it | `top-1366.jpg`: two adjacent disabled buttons both read "Opens in 68:46:29". | Buy and seat-claim actions are indistinguishable before the sale. Prefix with the verb ("Buy opens in…", "Claim opens in…"). |
| A-3 | LOW | Accessibility | `dist/index.html:63` (`nav .links a`) | Rendered hit boxes 25–83 × **16px**; 18px gaps. | Below the 24px minimum target; add vertical padding to the links. |
| A-4 | LOW | Accessibility | `dist/index.html:414-729` (body: `nav`, `header.hero`, sections, `footer`) | No `<main>` landmark; sections sit directly in `body`. | Wrap sections in `<main>` so assistive tech can skip the nav/hero. |
| A-5 | LOW | Accessibility | global (no `:focus-visible` rule) | Browser-default ring used. `focus-nav-1366.jpg` shows it visible on the dark nav in Chromium. | Verified in Chromium only; define an explicit high-contrast ring for consistency across browsers. |

Not findings: `button#rug` was flagged by the audit script as "unlabeled" only because it is `display:none` in
this phase (its text is "Check for rugs"); the marquee `.track` extends past the viewport by design inside
`.band { overflow: hidden }` and causes no page scroll.

### Contrast table (computed from source values, WCAG 2.x formula)

| Pair | Ratio |
| --- | --- |
| `--chalk` #efe6d6 on `--rock-0` #0d0805 (body text) | 16.09 |
| `--chalk-dim` #b9aa90 on `--rock-0` (secondary) | 8.74 |
| `--ochre` #d9a441 on `--rock-0` (`.label`) | 8.86 |
| `--ochre-hi` #f2c462 on `--rock-0` (h2, links) | 12.19 |
| `--red-hi` #d4633d on `--rock-0` (accent text) | 5.36 |
| `--moss` #a5d78a on `--rock-0` (success) | 12.04 |
| `#ff8a65` on `--rock-0` (`.err`) | 8.61 |
| `--chalk` on `.slab` top (#2d1e12 composite) | 12.99 |
| `--chalk-dim` on `.slab` top / bottom | 7.06 / 8.10 |
| `--ochre` on `.slab` top | 7.15 |
| `--chalk-dim` on `.auction` top (#2a1b0f composite) | 7.30 |
| `--char` #15100c on `--ochre-hi` (default `.btn`, `.navbuy em`, `.split`) | 11.56 |
| `#fff3e6` on `--red-hi` (`.btn.red`) | **3.40** |
| `#fff3e6` on `--red` (`.states .on`, `.tag`) | 4.90 |

## 4. Verification

Commands (repository root, exit 0 unless noted):

```
python3 scripts/mirror.py --verify
  → dist/ verified: 88 manifest entries, index.html differs only by the three CONFIG edits
cd dist && sha256sum -c --quiet MANIFEST-PUBLISHED.txt   → OK
npm run typecheck
  → inline scripts parsed OK: 2 block(s), 120845 bytes of HTML
node test/scratch/check.mjs     (headless Chromium 1243 via the globally installed playwright-core,
node test/scratch/check2.mjs     python3 http.server serving dist/ under /preview/ for the run's lifetime)
```

Browser results (both scripts exit 0):

- Viewports 1366×900, 900×900, 390×844, 320×568: console errors 0, console warnings 0, failed requests 0,
  HTTP ≥400 responses 0, broken images 0 of 103, horizontal overflow none.
- External hosts contacted: `ethereum-rpc.publicnode.com` only (the page's intentional mainnet RPC read).
  `seats.json` loaded (314 seat wallets; positive, negative and invalid-address checks returned the expected
  messages).
- Interactions: nav "FAQ" click → `#faq`, scrollY 12151; first FAQ opens on click and on Space; map cell click →
  "#47 · Base cave · line 2 · Pepe 10 of 21 · free: claimed by a seat wallet, in id order"; seat check via
  button and via Enter.
- Keyboard: Tab order logo → 8 nav links → `#navbuy` → hero CTAs; every stop `:focus-visible`.
- Reduced motion: hero torch and marquee animations `none`, reveals opaque, smooth scroll off.
- Screenshots (`artifacts/screenshots/`): `top-1366.jpg`, `top-900.jpg`, `top-390.jpg`, `top-320.jpg`,
  `full-1366.jpg`, `full-390.jpg` (full page, half scale), `focus-nav-1366.jpg` (focus ring on "Tools").

Production build: none exists for this deliverable (no compiler); the export is the verified mirror.
There is no TypeScript; the parse check above stands in for a typecheck.

## 5. Completion

**Complete for the stated scope.** Limitations: the assignment's MCP browser tool could not reach the export
(no preview launcher was supplied and `file:` navigation is blocked), so rendered evidence comes from a scripted
headless Chromium run instead of the MCP session. Unperformed: screen reader, native zoom, physical devices,
non-Chromium browsers, live-sale phases, wallet/transaction flows. All eight findings remain open by
design of the verbatim brief.
