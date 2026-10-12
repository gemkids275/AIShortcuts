**AI Shortcuts for macOS 1.1** — select text in any app, press a hotkey, and let an AI proofread, rewrite or summarize it in place.

## What's new
- **Fix: API keys lost after restart.** Keys are now stored reliably in the local Keychain.
- **Fix: false "update available" alert.** A failed update check (for example an HTTP 404) is no longer read as a version number.
- **Fix: custom provider API keys** are no longer replaced by a placeholder after the app reloads its commands. Keys that were already overwritten must be entered again.
- **Localization:** settings screens and components now use localized strings (English, German, French, Spanish).

## Download
`AI_Shortcuts_v1.1.dmg` — macOS 14 or later.

1. Open the DMG and drag **AI Shortcuts** to **Applications**.
2. The app is ad-hoc signed, not notarized. If macOS says it is "damaged" or cannot be opened, run:
   ```bash
   xattr -cr "/Applications/AI Shortcuts.app"
   ```

3. The app is re-signed for every release, so macOS may ask for the **Accessibility** and **Screen Recording** permissions again after updating. If a permission looks enabled but does not work, remove AI Shortcuts from the list in **System Settings → Privacy & Security** and add it back.

### Verify your download
```bash
shasum -a 256 -c SHA256SUMS.txt --ignore-missing
```
