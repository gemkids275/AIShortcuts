**Status:** Approved
**Approved by:** Nam Tran (owner) - "Duyệt hết" (G1, G2, G3), 2026-10-17
**Date:** 2026-10-17
**Body-sha256:** e0399d821c1043a22cc6b50b33cef0f77b068950d8918d7fa2647b373605046b

# Spec: download counts on the website

Feature slug: `downloads-per-version`. Mode: NEW. Proposed risk tier: R1 (user-facing change, two repos, a third-party API read at page load; no data model, auth or secret involved).

## Problem

The website (`aishortcuts/aishortcuts.github.io`, static HTML/CSS, no build step) lets people download AI Shortcuts but shows nothing about how many times each version was downloaded. The owner wants those numbers visible on the page. GitHub already records them: every release asset has a `download_count` in the Releases API.

## Proposal

The Download section (`#download` in `index.html` and `vi/index.html`) reads the public Releases API of `gemkids275/AIShortcuts` in the visitor's browser and shows:

1. On each platform card (Windows, macOS, Linux): the download count of the platform's current version, and the all-time total for that platform across every version.
2. Under the section heading: one grand total across all platforms.

Decisions already made by the owner in this session:
- Source: the browser calls `api.github.com` directly. No CI job, no cron, no generated JSON. Counts may be up to 1 hour stale.
- Shape: badges on the three cards plus one grand total. No per-release table.
- Badge content: current version plus platform total (for example `v2: 22 downloads · 41 total`).

Numbers are produced by one small script added to the site, `downloads.js`, loaded by both pages. All changes live in the website repo; this repository only holds these planning documents.

## User Stories

- As a visitor, I see how many times each platform's current build was downloaded, so I can judge adoption.
- As the owner, I see the total number of downloads across all versions and platforms on the site without opening GitHub.
- As a Vietnamese-speaking visitor, I see the same numbers in Vietnamese on `/vi/`.

## Acceptance Criteria

- **AC-1** Each platform card shows the download count of that platform's current version, labelled with the version (for example `v2`, `v1.2`). The current version is the newest non-draft, non-prerelease release for that platform, using the same tag rules as `.github/scripts/update_site_downloads.py`.
- **AC-2** Each platform card also shows the platform's all-time total: the sum over every release the Releases API returns on its first page (the 100 most recent; the project has 5) of that platform's asset (`.exe`, `.tar.gz`, `.dmg`).
- **AC-3** A grand total (sum of the three platform totals) appears under the Download heading.
- **AC-4** Only the installer assets are counted. `SHA256SUMS.txt` and any other asset are ignored. Draft and prerelease releases are ignored.
- **AC-5** Tag classification: `win-v<N>` counts toward Windows (`.exe`) and Linux (`.tar.gz`); `mac-v<X.Y>` and the legacy `v<X.Y>` count toward macOS (`.dmg`). A release whose tag matches neither is ignored.
- **AC-6** Both `index.html` (English) and `vi/index.html` (Vietnamese) show the counts, with translated labels and locale-appropriate digit grouping.
- **AC-7** If the API call fails (network error, HTTP 403 rate limit, malformed JSON, or no matching release), the page shows no counts and no error message, and the download buttons keep working exactly as before. A single platform with no matching release hides only its own badge.
- **AC-8** A successful response is cached in `localStorage` for 1 hour, so repeat visits and page navigation in the same browser within that hour make no API call. The unauthenticated rate limit (60 requests per hour per IP) is shared by every visitor behind one IP, so it can still be reached; AC-7 then applies and the badges stay hidden. Counts may therefore be up to 1 hour old; that is acceptable because download volume is low. Unavailable or throwing storage must not break rendering (fall back to a live call).
- **AC-9** API data reaches the DOM only as text (`textContent`), never as HTML.
- **AC-10** The existing CI link rewriter keeps working unchanged: after the change, `update_site_downloads.py` still finds and rewrites exactly the same three download links per page, and the new markup adds no extra `href="https://github.com/gemkids275/AIShortcuts/releases/download/..."` matches.
- **AC-11** The badges are readable on mobile widths and in the site's existing light and dark styles, and are exposed to assistive technology as plain text. The page has no layout jump larger than the badge height when counts arrive.
- **AC-12** The counts carry a short plain note that they only include downloads of release files from GitHub, so the numbers are not read as unique users.

## Out of Scope

- A per-release history table or chart (the owner chose badges plus a grand total).
- Any CI, cron, or generated data file; any change to `.github/workflows/*` or `update_site_downloads.py`.
- Server-side or privacy-affecting analytics; counting unique users; filtering bots or CI downloads.
- Compensating for counter resets when a release asset is re-uploaded (`ci/rebuild-existing-release`): GitHub creates a new asset with a zero counter. Known limitation of the data source.
- Other pages (`/guides/`, `/commands/`, `/about/`) and structured data (JSON-LD).
- Authenticated API calls (no token may ship in client code).
- Reading more than the 100 most recent releases (pagination).

## Open Questions

None blocking. Defaults chosen, change them at the gate if you disagree:
- Cache lifetime: 1 hour (owner: counts need not be live).
- Display string shape: `v2: 22 downloads · 41 total`; Vietnamese `v2: 22 lượt tải · tổng 41`.
- Grand total wording: `68 downloads so far` / `68 lượt tải tính đến nay`.

## Evidence (as-is)

- `index.html:165-194`: three `.card` blocks inside `.dl`, each with one `a.btn` whose href is rewritten by CI. Same structure expected in `vi/index.html`.
- `.github/scripts/update_site_downloads.py`: tag regexes `WIN_TAG`, `MAC_TAG`, asset suffixes, ignores drafts and prereleases; its `HREF` regex rewrites every matching `href` on both pages.
- `commands/gallery.js` is the site's only existing client script and the precedent for `fetch` plus `I18N` per `document.documentElement.lang`.
- Live data on 2026-10-17: Windows 41 (win-v2 22, win-v1 19), Linux 7 (5 + 2), macOS 20 (mac-v1.2 3, mac-v1.1 1, v1.0 16), total 68.

## Review log

- 2026-10-17 amended after Codex round 1 on design+tasks (findings F1, F2): AC-2 limited to the first API page, AC-8 no longer claims the rate limit is not a concern, pagination added to Out of Scope. Previous Approved body hash `eb42df43…fc98` is superseded; this document is Draft again and needs a new approval.
