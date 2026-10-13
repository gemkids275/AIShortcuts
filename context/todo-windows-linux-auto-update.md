# TODO: in-app auto update for Windows & Linux

Status: deferred (2026-10-13). Not worth building until the app has real users.

## Today
- Windows ships `AI-Shortcuts-windows-x64.exe` and Linux `AI-Shortcuts-linux-x64.tar.gz`, both PyInstaller `--onefile`, no installer.
- `update_checker.py` only compares the version number and opens `https://github.com/gemkids275/AIShortcuts/releases`. The user replaces the file by hand. Settings and commands live outside the app (`%APPDATA%\AIShortcuts`, `~/.config/aishortcuts`), so replacing the file is safe.

## Idea
"Check for updates" -> if newer, offer to update -> download the asset and `SHA256SUMS.txt` from the release into a temp dir -> verify -> swap the file -> restart.
- Windows: a running `.exe` cannot be overwritten but can be renamed. Rename the current file to `.old`, move the new one in, relaunch, delete `.old` on the next start.
- Linux: replace the binary with an atomic rename, then `exec` again.
- Any failure keeps the old version and falls back to opening the releases page.

## Decisions to make first
- Integrity: a checksum in the same release only catches corruption. Because the app would run the downloaded file, prefer an ed25519 signature over `SHA256SUMS.txt` (private key in a GitHub secret, public key embedded in the app, refuse to install on a bad signature). Needs a new step in `release.yml` and a backed-up key, like the macOS signing key.
- Install location: a folder that needs admin rights (for example Program Files) cannot be swapped; show a message and open the releases page.
- Alternatives: a Windows installer (MSI or Inno Setup), or leave the manual flow.
- Testing: unit-test download, hash, signature and file swap; the real swap and restart on Windows needs one manual run.
