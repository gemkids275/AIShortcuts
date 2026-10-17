**Status:** Approved
**Approved by:** Nam Tran (owner) - "Duyệt hết" (G1, G2, G3), 2026-10-17
**Date:** 2026-10-17
**Body-sha256:** b2bf898c5ec4a1d38d997158a32661d227c826cb860e8e08a006cf4aa17267cf

# Design: download counts on the website

Implements `spec.md` (Approved, body hash `e0399d82…046b`). Risk tier R1. Everything below happens in the website repo `aishortcuts/aishortcuts.github.io`; this repository only holds the planning documents.

## 1. Architecture

```
visitor browser
  index.html / vi/index.html ──loads──> /downloads.js (defer)
        downloads.js
          1. read localStorage cache  ── fresh (< 1 h)? ──yes──> render
          2. else fetch https://api.github.com/repos/gemkids275/AIShortcuts/releases?per_page=100
          3. summarize(releases) -> per-platform {version, current, total} + grand total
          4. write cache, render into [data-dl] placeholders (textContent only)
          any failure at any step -> render nothing
```

Verified facts: the Releases API answers CORS with `access-control-allow-origin: *`, unauthenticated limit is 60 requests per hour per IP, and the response is cached by GitHub for 60 seconds.

No new service, secret, workflow or build step. The site stays plain HTML and CSS plus one small script, like `commands/gallery.js`.

## 2. Files (website repo)

| File | Change |
|---|---|
| `downloads.js` | New. IIFE with pure functions (`summarize`, `format*`, `readCache`, `writeCache`, `render`) and a guarded `module.exports` so Node can test them. No other global. |
| `index.html`, `vi/index.html` | Inside each of the 3 platform cards add one empty `<p class="dl-count" data-dl="windows|macos|linux" hidden></p>` above the button. Under the `<h2>` add `<p class="dl-total" data-dl="total" hidden></p>`. In `.dl-note` add `<span data-dl="note" hidden>` with the fixed sentence of AC-12 (translated in the file, not by the script). Add `<script src="/downloads.js" defer></script>` before `</body>`. |
| `style.css` | New `.dl-count`, `.dl-total` (muted text, small size, existing tokens `--muted`, `--fg`, so light and dark need no extra rules). |
| `tests/downloads.test.js`, `tests/fixtures/releases.json` | New. Node built-in `node:test`, no dependency, no `package.json` needed (`node --test tests/`). The fixture is a trimmed copy of the live API response of 2026-10-17 (5 releases). |
| `README.md` | One bullet: where the counts come from and how to run the tests. |

No change in `gemkids275/AIShortcuts` code, workflows or `update_site_downloads.py` (AC-10).

## 3. Data flow and rules

Constants: `REPO = 'gemkids275/AIShortcuts'`, `TTL_MS = 3600000`, `CACHE_KEY = 'aishortcuts.downloads.v1'`, `FETCH_TIMEOUT_MS = 8000`.

Platform table (identical to `update_site_downloads.py`):

| Platform | Tag regex | Asset suffix |
|---|---|---|
| windows | `^win-v(\d+)$` | `.exe` |
| linux | `^win-v(\d+)$` | `.tar.gz` |
| macos | `^(?:mac-)?v(\d+(?:\.\d+)*)$` | `.dmg` |

`summarize(releases)` returns `{ windows, macos, linux, grand }` where each platform is `null` or `{ version: 'v2', current: 22, total: 41 }`:
1. Skip a release if it is a draft, a prerelease, or its tag matches no regex above.
2. For a matching release take the first asset whose name ends with the platform suffix (same as the Python script). No such asset: the release adds nothing for that platform. `SHA256SUMS.txt` never matches a suffix, so it is ignored (AC-4).
3. `count = asset.download_count`; accepted only if `Number.isInteger(count) && count >= 0`, otherwise the asset is skipped.
4. `total` is the sum of counts. `current` is the count of the release with the highest version tuple (numeric compare, like the Python script), `version` is `'v' + captured group`.
5. `grand` is the sum of the three totals, or `null` when all platforms are `null`.

`getSummary()`:
1. `readCache()`: parse JSON from `localStorage[CACHE_KEY]`; accept only `{ t, data }` with `t` a number in `(now - TTL_MS, now]` and `data` passing `isValidSummary` (shape and numeric checks, `version` must match `^v\d+(\.\d+)*$`). Any exception or invalid value: treat as a miss.
2. Miss: `fetch(url, { headers: { Accept: 'application/vnd.github+json' }, signal })` with an `AbortController` timeout. `!res.ok`, non-array JSON, or a thrown error: resolve `null`, nothing cached.
3. On a non-null summary call `writeCache` inside try/catch (storage may throw or be disabled), then return it.

Pagination: only the first 100 releases are read, as stated in AC-2. The project has 5; if it ever has more, totals would miss the oldest releases and the design must add paging first.

## 4. Rendering and i18n

- `lang = document.documentElement.lang === 'vi' ? 'vi' : 'en'` (same rule as `gallery.js`).
- Numbers: `new Intl.NumberFormat(lang === 'vi' ? 'vi-VN' : 'en-US').format(n)`.
- Strings (English / Vietnamese):
  - Card: `v2: 22 downloads · 41 total` / `v2: 22 lượt tải · tổng 41`. English uses `download` when the number is exactly 1.
  - Grand total: `68 downloads so far` / `68 lượt tải tính đến nay`.
- `render(summary, doc)`: for each platform with a non-null entry set `el.textContent` and `el.hidden = false`; platforms with `null` stay hidden (AC-7, partial). Grand total and the note span are shown only when `grand !== null`. A `null` summary touches nothing.
- Only `textContent` and the `hidden` property are used. No `innerHTML`, no attribute built from API data, no anchors created (AC-9, AC-10).
- The badge sits inside the existing flex column card above the button, so when it appears the button moves down by one text line at most (accepted by AC-11). The elements are normal paragraphs, so screen readers read them as plain text without extra ARIA.

## 5. Edge cases

| Case | Behaviour |
|---|---|
| Offline, DNS failure, timeout (8 s), HTTP 403/429/5xx | No counts, no message, buttons unaffected (AC-7). Nothing cached, next page load retries. |
| Response is not an array, release lacks `assets`, `download_count` missing or not an integer | That asset or release is skipped; if nothing is left the platform is `null`. |
| Release exists but asset not uploaded yet | Skipped for that platform; the previous release stays "current". |
| Draft or prerelease | Ignored. |
| Asset re-uploaded and its counter resets | Totals can drop. Data source limitation, in the spec's Out of Scope. |
| `localStorage` disabled, full, or throwing | Cache read treated as a miss, write ignored; page still renders from the live call. |
| Corrupt or tampered cache entry | Fails `isValidSummary`, treated as a miss. |
| JavaScript disabled | Placeholders stay `hidden`; page identical to today. |
| Two tabs load at once | Both fetch; harmless (2 requests of the 60 per hour). |

## 6. Security

- Data from the API and from `localStorage` is untrusted: validated by type, rendered only with `textContent`. The version label comes from a regex capture and is re-validated on cache read.
- No token, secret or cookie. No third party other than `api.github.com`, which the site already links to.
- The site sets no Content-Security-Policy; no change needed. If one is added later, `connect-src https://api.github.com` and `script-src 'self'` are required.
- Privacy: the visitor's browser contacts GitHub on page load (IP visible to GitHub). The site already sends visitors to GitHub for downloads and states "no telemetry" for the app; this is a page-load request to a third party, so the README note and the AC-12 sentence state that counts come from GitHub. No analytics is added.

## 7. Compatibility with the CI link rewriter (AC-10)

`update_site_downloads.py` rewrites `href="https://github.com/gemkids275/AIShortcuts/releases/download/…<suffix>"` and exits with an error if a page has none. The new markup contains no such href, and `downloads.js` creates no links, so the rewriter still finds exactly three matches per page. The release-notes link in `.dl-note` (`…/releases`) does not match because the pattern requires `/releases/download/`.

## 8. Test strategy (every AC mapped)

Automated unit tests run with `node --test tests/` (Node ≥ 20, built-in runner). They use the fixture and small stubs: fake `fetch`, fake `localStorage` (including one whose methods throw) and element stubs with `textContent`, `hidden` and an `innerHTML` setter that fails the test.

| AC | Planned test |
|---|---|
| AC-1 | `summarize` on the fixture: windows `v2/22`, linux `v2/5`, macos `v1.2/3`. A variant with a newer release puts it first regardless of array order. |
| AC-2 | `summarize` on the fixture: totals windows 41, linux 7, macos 20. |
| AC-3 | `grand` is 68 on the fixture; `null` when no platform matches; the rendered total element shows it. |
| AC-4 | Fixture variant with `SHA256SUMS.txt`, a draft and a prerelease carrying large counts: counts unchanged. |
| AC-5 | Tags `win-v2`, `mac-v1.2`, legacy `v1.0` classified as in the table; `foo-1`, `win-v2-beta`, `v1.0.0-rc` ignored. |
| AC-6 | `format` outputs for `en` and `vi`, singular/plural, digit grouping of 1234; both HTML files contain the placeholders, the note span and the script tag (static check over the HTML). |
| AC-7 | Fake fetch rejecting, returning 403, returning non-JSON, returning `[]`, returning an object: `getSummary()` resolves `null`, `render` leaves all placeholders hidden. One platform missing: only its element stays hidden. |
| AC-8 | Fresh cache: no fetch call. Entry older than 1 h or from the future: fetch called. Throwing storage on read and on write: still renders. Invalid cached shape: fetch called. |
| AC-9 | Render with element stubs whose `innerHTML` setter throws and with a hostile `version` string in a cached entry: entry rejected, stubs only ever receive `textContent`. |
| AC-10 | Static test: each HTML file has exactly three `releases/download/` hrefs matching the rewriter's pattern and `downloads.js` contains no `href`/`createElement('a')`. Manual: run `update_site_downloads.py` against the working copy and check `git diff` shows no change beyond link targets. |
| AC-11 | Manual browser check with `/verify`: screenshots at 375 px and 1280 px, light and dark; the badge text is selectable and read in the accessibility tree. |
| AC-12 | Static test: both HTML files contain the note sentence in `data-dl="note"`; browser check that it appears together with the counts and not when the API is blocked. |

Integration: serve the site locally (`python3 -m http.server`), open `/` and `/vi/` in the browser with the live API, then with the request blocked, then with `localStorage` cleared, and confirm the three outcomes.

## 9. Delivery and agy lane

- Claude writes the tests first and all of `downloads.js` (logic, validation, cache).
- agy writes the UI and prose parts: the HTML placeholders and CSS, the English and Vietnamese note sentence, and the README bullet, within an allowlist of `index.html`, `vi/index.html`, `style.css`, `README.md`.
- Output is a branch/patch in a worktree of the website repo. The owner pushes and opens the PR there; this repository's branch carries only these documents.
- Cross-review (R1): one Codex pass over design plus tasks.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Rate limit reached by visitors sharing one IP (offices, mobile carriers) | The 1 hour cache only lowers repeat requests from the same browser; it cannot prevent the limit on a shared IP. Accepted: the badges are hidden silently on failure (AC-7). |
| The API shape changes | Defensive validation; failure hides the badges only. |
| The tag naming scheme changes (new tag family) | Same regexes as the CI script; both must change together. Noted in `downloads.js` header comment. |
| Third-party request on page load | Stated in the page note; no personal data sent beyond the HTTP request itself. |

## Review log

- Round 1, body sha `af48bf3c…a0ca` (design) + `4a31160d…77d4` (tasks): Codex `gpt-6-luna`, effort high, read-only, offline pool. Outcome: 2 minor findings, 0 blocker. F1 (first 100 releases vs "every release") fixed by narrowing AC-2; F2 (cache does not protect shared IPs) fixed by rewording AC-8 and the risk table. Verified OK by Codex: hand-run of `summarize` gives 41/7/20/68 and versions v2/v2/v1.2; CI rewriter regex unaffected; AC-to-task consistency. Not verified by Codex (no network, no browser): CORS and rate-limit headers (checked by Claude with curl on 2026-10-17), layout and accessibility (T4). Round 2 not run: the delta is wording only.
