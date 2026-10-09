#!/usr/bin/env python3
"""Verbatim mirror of the ZTO cave-site into dist/.

Steps, in order:
  1. download  index.html, seats.json, MANIFEST.json, img/index.json, fonts/index.json,
               every file named in img/index.json  -> dist/img/
               every file named in fonts/index.json -> dist/fonts/
  2. verify    every downloaded file against the sha256 in MANIFEST.json;
               any mismatch aborts before anything is written to dist/
  3. patch     exactly three substrings inside the single `const CONFIG =` line of index.html
  4. publish   write dist/ and dist/MANIFEST-PUBLISHED.txt (sha256 of what was placed in dist/)

Usage:
  python3 scripts/mirror.py            # download, verify, patch, write dist/
  python3 scripts/mirror.py --verify   # only re-verify the existing dist/ (no network)
"""
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile
import urllib.request

SOURCE = "https://7130de0a-c74f-4dc3-9a8a-79db37963f97-00-1lk87v2ravyz1.reed.replit.dev/zto/cave-site/"
TOP_LEVEL = ["index.html", "seats.json", "MANIFEST.json", "img/index.json", "fonts/index.json"]
CONFIG_PREFIX = b"const CONFIG ="
EDITS = [
    (b"preview: true", b"preview: false"),
    (b'contract: ""', b'contract: "0x765956a7307222346b08fff681820a5d77e92028"'),
    (b"start: 0", b"start: 1791810000"),
]

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(rel: str) -> bytes:
    with urllib.request.urlopen(SOURCE + rel, timeout=60) as r:
        return r.read()


def patch_index(src: bytes) -> bytes:
    lines = src.split(b"\n")
    hits = [i for i, l in enumerate(lines) if l.lstrip().startswith(CONFIG_PREFIX)]
    if len(hits) != 1:
        sys.exit(f"expected exactly one `const CONFIG =` line, found {len(hits)}")
    i = hits[0]
    line = lines[i]
    for old, new in EDITS:
        if line.count(old) != 1:
            sys.exit(f"expected exactly one {old!r} in the CONFIG line, found {line.count(old)}")
        line = line.replace(old, new)
    lines[i] = line
    out = b"\n".join(lines)
    changed = [k for k, (a, b) in enumerate(zip(src.split(b"\n"), out.split(b"\n"))) if a != b]
    if changed != [i]:
        sys.exit(f"patch touched lines {changed}, expected only {i}")
    return out


def unpatch_check(published: bytes, manifest_sha: str) -> None:
    """Reverse the three edits and confirm the result is the upstream file."""
    lines = published.split(b"\n")
    i = next(k for k, l in enumerate(lines) if l.lstrip().startswith(CONFIG_PREFIX))
    line = lines[i]
    for old, new in EDITS:
        line = line.replace(new, old)
    lines[i] = line
    if sha256(b"\n".join(lines)) != manifest_sha:
        sys.exit("dist/index.html differs from MANIFEST.json by more than the three CONFIG edits")


def verify_dist() -> int:
    manifest = json.loads((DIST / "MANIFEST.json").read_bytes())
    published = {}
    for line in (DIST / "MANIFEST-PUBLISHED.txt").read_text().splitlines():
        h, p = line.split("  ", 1)
        published[p] = h
    bad = []
    for rel, want in manifest.items():
        data = (DIST / rel).read_bytes()
        got = sha256(data)
        if rel == "index.html":
            unpatch_check(data, want)
        elif got != want:
            bad.append(f"{rel}: MANIFEST {want} != dist {got}")
        if published.get(rel) != got:
            bad.append(f"{rel}: MANIFEST-PUBLISHED {published.get(rel)} != dist {got}")
    extra = set(published) - set(manifest) - {"MANIFEST.json"}
    if extra:
        bad.append(f"MANIFEST-PUBLISHED lists files not in MANIFEST.json: {sorted(extra)}")
    for rel in TOP_LEVEL:
        if not (DIST / rel).exists():
            bad.append(f"missing {rel}")
    if bad:
        print("\n".join(bad))
        return 1
    print(f"dist/ verified: {len(manifest)} manifest entries, index.html differs only by the three CONFIG edits")
    return 0


def mirror() -> int:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="cave-mirror-"))
    files = {}
    for rel in TOP_LEVEL:
        files[rel] = fetch(rel)
    for sub in ("img", "fonts"):
        for name in json.loads(files[f"{sub}/index.json"]):
            files[f"{sub}/{name}"] = fetch(f"{sub}/{name}")
    print(f"downloaded {len(files)} files")

    manifest = json.loads(files["MANIFEST.json"])
    mismatches = [rel for rel, want in manifest.items() if rel not in files or sha256(files[rel]) != want]
    missing = sorted(set(manifest) - set(files))
    unlisted = sorted(set(files) - set(manifest) - {"MANIFEST.json"})
    if mismatches or unlisted:
        print("MANIFEST.json verification FAILED; nothing written to dist/")
        for rel in mismatches:
            print(f"  mismatch/missing: {rel}")
        for rel in unlisted:
            print(f"  downloaded but not in manifest: {rel}")
        return 1
    print(f"verified {len(manifest)} files against MANIFEST.json (missing: {missing})")

    files["index.html"] = patch_index(files["index.html"])

    for rel, data in files.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    lines = [f"{sha256(files[rel])}  {rel}" for rel in manifest] + [f"{sha256(files['MANIFEST.json'])}  MANIFEST.json"]
    (tmp / "MANIFEST-PUBLISHED.txt").write_text("\n".join(lines) + "\n")

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.move(str(tmp), str(DIST))
    print(f"wrote dist/ ({len(files)} files + MANIFEST-PUBLISHED.txt)")
    return verify_dist()


if __name__ == "__main__":
    sys.exit(verify_dist() if "--verify" in sys.argv else mirror())
