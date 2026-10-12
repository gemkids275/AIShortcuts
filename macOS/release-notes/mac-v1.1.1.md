**AI Shortcuts for macOS 1.1.1** — select text in any app, press a hotkey, and let an AI proofread, rewrite or summarize it in place.

## What's new
- **Updates keep your permissions.** The app is now signed with a fixed certificate instead of a new one-off signature for every build, so macOS keeps the Accessibility and Screen Recording permissions you granted when you update to the next release.
- **One-time step for this update:** because the signature changes once now, macOS will ask for the **Accessibility** (and **Screen Recording**) permission again after installing 1.1.1. If the permission looks enabled but does not work, run these two commands in Terminal and grant the permissions again when asked:
  ```bash
  tccutil reset Accessibility com.gemkids.writing-tools
  tccutil reset ScreenCapture com.gemkids.writing-tools
  ```
  Your commands, settings and API keys are not affected.

## Download
`AI_Shortcuts_v1.1.1.dmg` — macOS 14 or later.

1. Quit AI Shortcuts, open the DMG and drag **AI Shortcuts** to **Applications**, replacing the old copy.
2. The app is not notarized. If macOS says it is "damaged" or cannot be opened, run:
   ```bash
   xattr -cr "/Applications/AI Shortcuts.app"
   ```

### Verify your download
```bash
shasum -a 256 -c SHA256SUMS.txt --ignore-missing
```
