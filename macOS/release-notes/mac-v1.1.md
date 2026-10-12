**AI Shortcuts for macOS 1.1** — select text in any app, press a hotkey, and let an AI proofread, rewrite or summarize it in place.

## What's new
- **Updates keep your permissions.** The app is signed with a fixed certificate instead of a new one-off signature for every build, so macOS keeps the Accessibility and Screen Recording permissions you granted when you update to a later release.
- **Fix: API keys lost after restart.** Keys are now stored reliably in the local Keychain.
- **Fix: false "update available" alert.** A failed update check (for example an HTTP 404) is no longer read as a version number.
- **Fix: custom provider API keys** are no longer replaced by a placeholder after the app reloads its commands. Keys that were already overwritten must be entered again.
- **Localization:** settings screens and components now use localized strings (English, German, French, Spanish).

## Download
`AI_Shortcuts_v1.1.dmg` — macOS 14 or later.

1. Open the DMG and drag **AI Shortcuts** to **Applications**.
2. The app is not notarized. If macOS says it is "damaged" or cannot be opened, run:
   ```bash
   xattr -cr "/Applications/AI Shortcuts.app"
   ```

3. If the Accessibility or Screen Recording permission looks enabled but does not work (for example after replacing an older copy of the app), run these commands in Terminal and grant the permissions again when asked:
   ```bash
   tccutil reset Accessibility com.gemkids.writing-tools
   tccutil reset ScreenCapture com.gemkids.writing-tools
   ```
   Your commands, settings and API keys are not affected.

### Verify your download
```bash
shasum -a 256 -c SHA256SUMS.txt --ignore-missing
```
