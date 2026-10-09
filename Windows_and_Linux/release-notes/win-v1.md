**AI Shortcuts for Windows & Linux — first release of this fork.** Select text in any app, press a hotkey, and let an AI proofread, rewrite or summarize it in place. macOS has its own releases (`v*` tags).

## Highlights
- **Command Manager** — create, reorder, export/import and back up your commands (compatible with the macOS format).
- **Per-command shortcuts** and **per-command AI override** (provider, model, or a custom OpenAI-compatible endpoint with its own key).
- **Attachments** — paste or attach images and text files in prompts and follow-up questions.
- **More providers** — Gemini, OpenAI-compatible, Ollama, Anthropic, Mistral, OpenRouter.

## Download
| Platform | File |
|---|---|
| Windows 10/11 (x64) | `AI-Shortcuts-windows-x64.exe` |
| Linux (x64, X11) | `AI-Shortcuts-linux-x64.tar.gz` |

### Windows
1. Download and run `AI-Shortcuts-windows-x64.exe`.
2. The file is not code-signed, so SmartScreen may show "Windows protected your PC". Choose **More info → Run anyway**, or verify the checksum below first.

### Linux
```bash
tar -xzf AI-Shortcuts-linux-x64.tar.gz
./"AI Shortcuts"
```
Requirements: an **X11** session, `xclip` or `xsel`, and (recommended) a Secret Service keyring such as GNOME Keyring or KWallet. Global hotkeys do not work on Wayland.

### Verify your download
```bash
sha256sum -c SHA256SUMS.txt --ignore-missing      # Linux / macOS / Git Bash
```
```powershell
Get-FileHash .\AI-Shortcuts-windows-x64.exe -Algorithm SHA256   # compare with SHA256SUMS.txt
```
Build provenance can be checked with `gh attestation verify <file> --repo gemkids275/WritingToolsV2`.

## Upgrading
- Settings and commands live in `%APPDATA%\AIShortcuts` (Windows) or `~/.config/aishortcuts` (Linux).
- If you used the original Windows/Linux version, custom commands from `options.json` (next to the executable) are migrated automatically on first run.
- Re-enter your API keys if a provider shows as not configured.

## Known limitations
- No Wayland support for global hotkeys on Linux.
- Windows binary is unsigned.
- Without an OS keyring, per-command API keys are stored in a lightly obfuscated (not encrypted) file.

Full details: [CHANGELOG](https://github.com/gemkids275/WritingToolsV2/blob/main/Windows_and_Linux/CHANGELOG.md). Found a problem? [Open an issue](https://github.com/gemkids275/WritingToolsV2/issues/new).
