# ZTO cave-site — verbatim static mirror

`dist/` is a byte-for-byte mirror of the Pepeolithic cave-site published at
`https://7130de0a-c74f-4dc3-9a8a-79db37963f97-00-1lk87v2ravyz1.reed.replit.dev/zto/cave-site/`,
with exactly three configuration edits applied to one line of `index.html`. There is no build step, no
framework, no bundler and no dependency: the published export **is** the source.

## What is in the repository

| Path | Purpose |
| --- | --- |
| `dist/` | The static site to publish. `index.html`, `seats.json`, `MANIFEST.json`, `img/` (82 files + `index.json`), `fonts/` (4 files + `index.json`). All relative URLs; works at any subpath. |
| `dist/MANIFEST-PUBLISHED.txt` | `sha256  path` for every file placed in `dist/`, in `sha256sum -c` format. |
| `scripts/mirror.py` | Reproduces `dist/` from the source: download, verify against `MANIFEST.json`, apply the three edits, write the published manifest. `--verify` re-checks an existing `dist/` offline. |
| `scripts/check-scripts.mjs` | Parses every inline `<script>` in `dist/index.html` (the "typecheck" for a no-TypeScript site). |
| `package.json`, `package-lock.json` | npm script aliases only. No dependencies, so the lockfile is empty of packages and no `node_modules` is ever created. |
| `DESIGN.md` | The implemented design system, extracted from `dist/index.html`. |
| `VALIDATION.md` | Better Interface review: coverage, findings, verification commands and limitations. An identical copy is delivered as `artifacts/validation.md` (the `artifacts/` directory is excluded from Git by the workspace and uploaded separately). |
| `artifacts/screenshots/` | Headless-Chromium screenshots of the export at 1366, 900, 390 and 320 CSS px (delivered with the artifacts, not committed). |

## The three edits

All inside the single line of `dist/index.html` that starts with `const CONFIG =` (line 740). Nothing else differs
from upstream.

| Upstream | Published |
| --- | --- |
| `preview: true` | `preview: false` |
| `contract: ""` | `contract: "0x765956a7307222346b08fff681820a5d77e92028"` |
| `start: 0` | `start: 1791810000` |

`scripts/mirror.py --verify` proves this: it reverses the three edits in memory and checks that the result hashes
to the upstream `index.html` value recorded in `MANIFEST.json`. Every other file must hash exactly to its
`MANIFEST.json` entry.

## Install

Requirements: Python 3.8+ (standard library only) and Node 18+ (for the script parse check). Nothing to install:

```bash
npm install   # optional; installs nothing, only confirms the empty lockfile
```

## Preview

```bash
npm run preview
# → http://127.0.0.1:4173/
```

This serves `dist/` with Python's built-in HTTP server. Open the URL in a browser. The page fetches `seats.json`
relatively (so it must be served over HTTP, not opened as a `file://` URL) and reads the Ethereum mainnet contract
through the public RPC endpoints listed in the page; those external calls are part of the upstream site and are
intentional.

## Rebuild (re-mirror)

```bash
npm run build      # = python3 scripts/mirror.py
npm run verify     # = python3 scripts/mirror.py --verify   (offline)
npm run typecheck  # = node scripts/check-scripts.mjs
```

`build` downloads everything again into a temporary directory, verifies every file against the downloaded
`MANIFEST.json`, and only then replaces `dist/`. Any hash mismatch aborts with the offending paths listed and
leaves the existing `dist/` untouched. Do not edit files under `dist/` by hand; change them upstream and re-mirror.

## Publish

Upload the contents of `dist/` as-is to any static host (IPFS/ENS gateway, S3, GitHub Pages, nginx). No rewrite
rules are needed: the site is one page with hash navigation and every asset URL is relative. Keep
`dist/MANIFEST-PUBLISHED.txt` alongside it so the published bytes can be re-verified:

```bash
cd dist && sha256sum -c MANIFEST-PUBLISHED.txt
```

## Validation results (this delivery)

Commands run from the repository root on 2026-10-09, all exit 0:

| Command | Result |
| --- | --- |
| `python3 scripts/mirror.py --verify` | `dist/ verified: 88 manifest entries, index.html differs only by the three CONFIG edits` |
| `cd dist && sha256sum -c --quiet MANIFEST-PUBLISHED.txt` | OK (89 lines) |
| `npm run typecheck` | `inline scripts parsed OK: 2 block(s), 120845 bytes of HTML` |
| `node test/scratch/check.mjs` and `check2.mjs` (headless Chromium 1243 via `playwright-core`, serving `dist/` under `/preview/`) | 0 console errors, 0 failed requests, 0 broken images at all four widths; fonts loaded; nav, FAQ, seat check (positive, negative, invalid), map cell selection and keyboard walk exercised. Details in `VALIDATION.md`. |

Production build: there is none to run; the export is verified bytes, not compiled output.

Limitations: the assignment's MCP browser could not open the export (no preview launcher was provided and
`file:` URLs are blocked), so rendered checks were made with a scripted headless Chromium instead; no
screen-reader, native-zoom or physical-device checks were performed. The mirror brief forbids changing anything
in `dist/`, so the eight Better Interface findings in `VALIDATION.md` (320px caption overflow, 3.4:1 primary
button contrast, unlabeled seat input, mouse-only map cells, duplicate "Opens in" labels, 16px nav hit areas,
missing `main` landmark, default-only focus ring) are recorded with `file:line` for upstream, not fixed here.
