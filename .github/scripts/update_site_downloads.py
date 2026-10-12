#!/usr/bin/env python3
"""Point the website download buttons at the newest release of each platform.

Usage: update_site_downloads.py <site_dir>

Reads the public GitHub Releases API (GITHUB_TOKEN is used if set) and rewrites
the release-download links in <site_dir>/index.html and <site_dir>/vi/index.html:

  Windows .exe and Linux .tar.gz  <- newest release tagged  win-v<N>
  macOS .dmg                      <- newest release tagged  mac-v<X.Y> (or legacy v<X.Y>)

Drafts and prereleases are ignored. A platform whose newest release has no
matching asset yet keeps its current link, so re-run once the asset is uploaded.
"""
import json
import os
import re
import sys
import urllib.request

REPO = "gemkids275/AIShortcuts"
PAGES = ("index.html", "vi/index.html")
WIN_TAG = re.compile(r"^win-v(\d+)$")
MAC_TAG = re.compile(r"^(?:mac-)?v(\d+(?:\.\d+)*)$")
# kind -> (tag pattern, asset suffix, href pattern to replace)
KINDS = {
    "windows": (WIN_TAG, ".exe"),
    "linux": (WIN_TAG, ".tar.gz"),
    "macos": (MAC_TAG, ".dmg"),
}
HREF = r"https://github\.com/" + re.escape(REPO) + r"/releases/download/[^\"]+?"


def fetch_releases():
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases?per_page=100",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "site-updater"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def newest_asset(releases, tag_re, suffix):
    best = None
    for rel in releases:
        if rel.get("draft") or rel.get("prerelease"):
            continue
        m = tag_re.match(rel["tag_name"])
        if not m:
            continue
        version = tuple(int(p) for p in m.group(1).split("."))
        for asset in rel.get("assets", []):
            if asset["name"].endswith(suffix):
                if best is None or version > best[0]:
                    best = (version, rel["tag_name"], asset["browser_download_url"])
                break
    return best


def main(site_dir):
    releases = fetch_releases()
    changed = False
    for kind, (tag_re, suffix) in KINDS.items():
        found = newest_asset(releases, tag_re, suffix)
        if not found:
            print(f"{kind}: no release with a {suffix} asset yet, keeping current link")
            continue
        _, tag, url = found
        pattern = re.compile(r'(href=")' + HREF + re.escape(suffix) + r'(")')
        for page in PAGES:
            path = os.path.join(site_dir, page)
            with open(path, encoding="utf-8", newline="") as f:
                text = f.read()
            new_text, n = pattern.subn(lambda m: m.group(1) + url + m.group(2), text)
            if n == 0:
                sys.exit(f"{kind}: no download link found in {page}")
            if new_text != text:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(new_text)
                changed = True
                print(f"{kind}: {page} -> {tag}")
    print("changed" if changed else "up to date")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
