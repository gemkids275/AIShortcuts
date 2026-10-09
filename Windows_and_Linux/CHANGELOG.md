# Changelog — Windows & Linux

All notable changes to the Windows & Linux app are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases are tagged `win-v<N>`
(`N` is the integer in `update_checker.py` / `Latest_Version_for_Update_Check.txt`).
macOS releases use separate `v*` tags and version files.

## [1] - 2026-10-09

First release of the AI Shortcuts fork for Windows and Linux. Published as pre-built binaries.

### Added
- Command Manager: built-in and custom commands, drag-and-drop ordering, per-command export/import and full backup/restore (compatible with the macOS bundle format).
- Per-command keyboard shortcuts with conflict detection (single global listener).
- Per-command AI override: provider, model, or a custom OpenAI-compatible endpoint, with an optional per-command API key stored in the OS keyring.
- Image and text attachments in prompts and follow-up questions.
- Providers: Anthropic, Mistral and OpenRouter (in addition to Gemini, OpenAI-compatible and Ollama).
- Redesigned settings, popup and response windows; About page links to this fork.
- Pre-built binaries for Windows (x64) and Linux (x64, X11) published through GitHub Actions, with SHA-256 checksums and build provenance attestations.
- Pull request CI: lint, unit tests, dependency import check, and a build + startup smoke test on both platforms.

### Changed
- Gemini now uses the `google-genai` SDK; `mistralai>=2` is required.
- The update checker points to this fork and uses its own version file, separate from macOS.
- Commands are stored in `commands.json` in the user config directory instead of `options.json`.

### Fixed
- Custom commands from the legacy `options.json` are migrated to `commands.json` on first run.
- "Restore Built-ins" no longer deletes custom commands.
- A per-command base URL override no longer receives the global API key.
- Importing shortcuts checks conflicts case-insensitively and against the app hotkey.
- Ollama image attachments are sent as plain base64.
- A corrupt `commands.json` is backed up as `commands.json.corrupt` instead of being overwritten.
- The Linux build bundles pynput's X11 backend (the binary crashed on startup without it).
- Gemini: the retired Gemma 3 models (404) are replaced by Gemma 4 and `flash-latest` options; saved configs are migrated automatically.
- Translations are compiled at build time and bundled, so the selected language (en, vi, it, ja, zh) is actually applied. Remaining hardcoded UI strings are now translatable.

### Known limitations
- Linux: global hotkeys and simulated copy/paste need X11; they do not work under Wayland. `xclip` or `xsel` must be installed.
- Windows binaries are not code-signed; SmartScreen may warn on first run.
- Per-command API keys fall back to a lightly obfuscated file (not encrypted) when no OS keyring is available.

[1]: https://github.com/gemkids275/WritingToolsV2/releases/tag/win-v1
