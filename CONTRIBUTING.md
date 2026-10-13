# Contributing

Thanks for helping improve AI Shortcuts. Bug reports, fixes and translations are welcome.

## Before you start

- Search [existing issues](https://github.com/gemkids275/AIShortcuts/issues) first.
- For larger changes, open an issue to discuss the idea before writing code.

## Windows & Linux (Python)

```bash
cd Windows_and_Linux
python -m venv .venv
.venv/Scripts/activate        # Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
python -m unittest discover -s tests   # run the tests
```

- Wrap every UI string in `_()` and add it to all five `.po` files in
  `locales/` (en, vi, it, ja, zh). `tests/test_translations.py` fails on any
  missing msgid. `.mo` files are compiled at build time and are not committed.
- Keep changes focused; avoid unrelated refactors.

## macOS (Swift)

Open `macOS/WritingTools.xcodeproj` in Xcode (macOS 14+) and run the
`WritingTools` scheme. Run the tests with
`xcodebuild test -scheme WritingTools -project macOS/WritingTools.xcodeproj`.

## Share a command

Useful ready-made commands live in [commands/](commands/) and are listed on the [website](https://aishortcuts.github.io/commands/). Export your command from the app, add the `gallery` block and open a pull request with the **command** template; the format, the rules and the local check are described in [commands/README.md](commands/README.md). If you would rather not touch Git, open a [Suggest a command](https://github.com/gemkids275/AIShortcuts/issues/new?template=command_suggestion.yml) issue.

## Pull requests

- Branch from `main` and open the PR against `main`.
- CI must pass: the Windows and Linux checks and builds are required.
- Describe what changed and why, and how you tested it.

By contributing you agree your work is licensed under the GPL-3.0 license of this project.
