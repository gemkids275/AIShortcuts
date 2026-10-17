# Deviations: download counts on the website

Kept apart from `tasks.md` so the approved artifacts stay untouched. Each entry: what the plan said / what the code showed / choice made / needs user judgment.

## D1. Test command
- Plan (design.md section 8): run the tests with `node --test tests/`.
- Code showed: on Node 22 `node --test tests/` treats `tests/` as a module path and fails with "Cannot find module".
- Choice: use plain `node --test`, which discovers `*.test.js` files. README of the website repo documents this form.
- Needs user judgment: no.

## D2. Size of PR B
- Plan (tasks.md): PR B (T1+T2) about 380 lines over 4 files.
- Code showed: commit `f01d69a` has 625 added lines over 3 files: `downloads.js` 232, `tests/downloads.test.js` 312, `tests/fixtures/releases.json` 81. The module is larger than estimated because of validation of cached data, and the test file covers the full failure matrix.
- Choice: keep T1 and T2 together in one PR as planned; the module is not loaded by any page until PR C, so merging it changes nothing for visitors. Test and fixture lines are 63% of the total.
- Needs user judgment: no.

## D3. Body hash command
- Plan (command text): `sed '/^\*\*\(Status\|Approved by\|Date\|Body-sha256\):\*\*/d'`.
- Code showed: macOS BSD `sed` does not support `\|`, so no header line was removed and the hash included its own line. Two hashes reported earlier in the session (`7eeb3cec…`, `8da960ad…`) were therefore invalid. Fixed before any approval was recorded.
- Choice: use `sed -E '/^\*\*(Status|Approved by|Date|Body-sha256):\*\*/d'`. Hashes of spec, design and tasks were recomputed with it and re-checked before each `Approved`.
- Needs user judgment: no.
