**AI Shortcuts for macOS 1.2** — select text in any app, press a hotkey, and let an AI proofread, rewrite or summarize it in place.

## What's new
- **Import several commands at once.** **Settings → Commands → Import** now adds every command in a file instead of only the first one. A command you already have is never overwritten: a copy is added with "(Imported)" in its name. This is what the shared command packs on the [website gallery](https://aishortcuts.github.io/commands/) use.
- **Get More Commands.** A new button in **Settings → Commands** opens the website gallery of ready-made commands.
- **Safer restore.** **Import Full Configuration** now asks for confirmation before it replaces all your commands (and deletes their custom API keys).

## Download
`AI_Shortcuts_v1.2.dmg` — macOS 14 or later.

1. Open the DMG and drag **AI Shortcuts** to **Applications**.
2. The app is not notarized. If macOS says it is "damaged" or cannot be opened, run:
   ```bash
   xattr -cr "/Applications/AI Shortcuts.app"
   ```

3. Your Accessibility and Screen Recording permissions are kept when you update from 1.1. If they ever look enabled but do not work, run these commands in Terminal and grant them again when asked:
   ```bash
   tccutil reset Accessibility com.gemkids.writing-tools
   tccutil reset ScreenCapture com.gemkids.writing-tools
   ```
   Your commands, settings and API keys are not affected.

### Verify your download
```bash
shasum -a 256 -c SHA256SUMS.txt --ignore-missing
```
