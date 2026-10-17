**Status:** Approved
**Approved by:** Nam Tran (owner) - "Duyệt hết" (G1, G2, G3), 2026-10-17
**Date:** 2026-10-17
**Body-sha256:** fb2728c3948db3c0b1781866e1b76078c573747c4e54e84ddb083d0afe19285d

# Tasks: download counts on the website

Implements `design.md` (Approved, `b2bf898c…67cf`) for `spec.md` (Approved, `e0399d82…046b`). Risk tier R1 overall. Code lives in the website repo `aishortcuts/aishortcuts.github.io`, worked in its own git worktree; only T0 touches this repository.

## Task list

| ID | Title | Depends on | Tier | Size | Lane | PR |
|---|---|---|---|---|---|---|
| T0 | Commit the planning documents (spec, design, tasks) on `feat/downloads-per-version` | none | R0 | S: 3 docs | Claude | A (this repo) |
| T1 | Fixture + failing tests + `summarize()` and validation in `downloads.js` | none | R1 | M: ~180 lines, 3 files | Claude | B (site) |
| T2 | Tests + `format`, cache, `getSummary()`, `render()` in `downloads.js` | T1 | R1 | M: ~200 lines, 2 files | Claude | B (site) |
| T3 | Placeholders, note sentence, `<script>` tag in both pages; CSS; static tests | T2 | R1 | S: ~70 lines, 4 files | agy (UI + prose), tests by Claude | C (site) |
| T4 | README bullet; run the real CI link rewriter; browser verification (AC-11, AC-12) | T3 | R0 | S: ~10 lines, 1 file | Claude (README text by agy) | C (site) |

Split rationale (rule: about 200 lines and 8 files per PR). PR B holds T1+T2, about 380 lines over 4 files (`downloads.js`, the test file, the fixture, nothing else). That is above the hint on purpose: roughly 60% is test code and a JSON fixture, the module is not loaded by any page until PR C, so merging B changes nothing for visitors, and splitting T1 from T2 would put half of a cache/render module in a PR with no way to run it end to end. PR C wires the UI (T3+T4, about 80 lines). PR A is documents only.

Execution order: T0 first (documents become durable), then T1 → T2 → T3 → T4. Fix budget: at most 2 fix rounds per task on gate failures.

## Task details

### T0 Planning documents
Commit `context/specs/downloads-per-version/{spec,design,tasks}.md` on `feat/downloads-per-version`. Show the push and `gh pr create` commands; the owner runs them (or invokes `/commit-pr`). Gate: none beyond a clean `git status`.

### T1 Core summary logic
Create a worktree of the website repo (`gh repo clone aishortcuts/aishortcuts.github.io`, branch `feat/download-counts`). Add `tests/fixtures/releases.json` (trimmed live response of 2026-10-17, plus synthetic variants built inside the tests). Write `tests/downloads.test.js` cases for `summarize` first and watch them fail, then add `downloads.js` with the platform table, `summarize`, `isValidSummary` and the guarded `module.exports`. Header comment records that the tag regexes mirror `update_site_downloads.py`.
Done when: AC-1..AC-5 tests pass with `node --test tests/`.

### T2 Format, cache, fetch, render
Tests first for `format` (en/vi, singular/plural, grouping), `readCache`/`writeCache` (fresh, stale, future, corrupt, throwing storage), `getSummary` (fake fetch: reject, 403, bad JSON, `[]`, object, timeout via aborted signal) and `render` (element stubs, `innerHTML` setter that fails, hostile version string). Then implement the functions and the auto-start at the end of the file (runs only when `document` exists).
Done when: AC-6 (formatting part), AC-7, AC-8, AC-9 tests pass.

### T3 Page wiring and styling (agy lane)
Brief for agy with allowlist `index.html`, `vi/index.html`, `style.css`: add the placeholders, the translated note sentence (AC-12) and the script tag exactly as in design §2; style `.dl-count` and `.dl-total` with existing tokens only. agy may not touch `downloads.js`, `tests/`, Status blocks or run git. Claude adds static tests (placeholders, note, script tag, exactly three rewriter-pattern hrefs per page, no anchors created by the script) before the brief is sent, then verifies `git status` shows only allowlisted files.
Done when: static tests for AC-6, AC-10, AC-12 pass.

### T4 Docs and end-to-end verification
`README.md` bullet (where counts come from, how to run `node --test tests/`). Run `python3 .github/scripts/update_site_downloads.py <site checkout>` from a checkout of `gemkids275/AIShortcuts` and confirm the diff contains no change outside link targets (AC-10). Serve the site locally and check with the browser: live API, request blocked, cleared storage, 375 px and 1280 px, light and dark, `/` and `/vi/` (AC-11, AC-12, AC-6).
Done when: evidence listed in the PR description.

## Consistency table

| AC | Task(s) | Planned test | Result |
|---|---|---|---|
| AC-1 | T1 | `summarize` current version, array order independent | covered |
| AC-2 | T1 | `summarize` platform totals 41 / 7 / 20 | covered |
| AC-3 | T1, T2, T3 | `grand` 68 / null; `render` shows total; markup has the placeholder | covered |
| AC-4 | T1 | SHA256SUMS, draft, prerelease ignored | covered |
| AC-5 | T1 | tag classification table | covered |
| AC-6 | T2, T3, T4 | `format` en/vi; static HTML check; browser check of `/vi/` | covered |
| AC-7 | T2, T4 | failure matrix on `getSummary` and `render`; browser with request blocked | covered |
| AC-8 | T2, T4 | cache matrix; browser with cleared storage | covered |
| AC-9 | T2 | `innerHTML` setter fails test; hostile cache entry | covered |
| AC-10 | T3, T4 | static href count and no-anchor test; real rewriter run | covered |
| AC-11 | T3, T4 | CSS written in T3; screenshots and accessibility tree in T4 | covered |
| AC-12 | T3, T4 | static note test; browser shows note only with counts | covered |

Other checks:
- Open questions in `spec.md`: none (defaults recorded).
- Dependencies: T0 none; T1 none; T2→T1; T3→T2; T4→T3. Acyclic.
- Every task has tier and size: yes.
- Not covered / limitations: counter reset after asset re-upload (spec Out of Scope); more than 100 releases (design §3).

## Deviations

(none)

## Review log

- Round 1, body sha `4a31160d…77d4`: reviewed together with the design by Codex `gpt-6-luna` (see design.md Review log). No finding against the tasks; consistency table, dependencies and PR split confirmed. This file changed only by the new document hashes in its header line and this log.
