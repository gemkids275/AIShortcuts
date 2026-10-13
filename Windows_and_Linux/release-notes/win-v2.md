**AI Shortcuts for Windows & Linux v2** — adds a way to discover ready-made commands. macOS has its own releases (`mac-v*` tags).

## What's new
- **Get More Commands...** — a new button in Settings and in the Command Manager opens the community command gallery on the website. Copy a prompt, or tick several commands and download them as one JSON file, then bring them in with the Command Manager's import. The gallery opens in Vietnamese when the app language is Vietnamese.

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
Build provenance can be checked with `gh attestation verify <file> --repo gemkids275/AIShortcuts`.

## Upgrading
- Your settings and commands are kept; install over the previous version.
- Re-enter your API keys only if a provider shows as not configured.

Full details: [CHANGELOG](https://github.com/gemkids275/AIShortcuts/blob/main/Windows_and_Linux/CHANGELOG.md). Found a problem? [Open an issue](https://github.com/gemkids275/AIShortcuts/issues/new).
