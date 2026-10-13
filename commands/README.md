# Shared commands

Ready-made commands anyone can import into AI Shortcuts. Each `<slug>.json` here is the same file the app exports for one command, plus a `gallery` block with listing details. After a pull request is merged, the file appears on the [website gallery](https://aishortcuts.github.io/commands/) and can be downloaded from there.

## Add yours

1. In the app, create the command, test it on a few real texts, then export it (Settings → Commands → the export button on the command). On Windows and Linux use the command's export in the Command Manager.
2. Save the file as `commands/<slug>.json` in a fork of this repository. The slug is 3–48 lowercase letters, digits or `-` (for example `polite-decline`).
3. Add the `gallery` block (see the example) and remove anything the checks reject (below).
4. Run the checks, then open a pull request using the **command** template: `https://github.com/gemkids275/AIShortcuts/compare/main...YOUR-BRANCH?template=command.md`.

```bash
python .github/scripts/validate_commands.py commands
```

Not comfortable with Git? Open a [Suggest a command](https://github.com/gemkids275/AIShortcuts/issues/new?template=command_suggestion.yml) issue and describe it; a maintainer can turn it into a file.

## File format

```json
{
  "appIdentifier": "AIShortcuts",
  "version": 1,
  "exportDate": 813000000,
  "commands": [
    {
      "id": "7B1E0C0E-52C4-4C55-9D55-3B9C2E7B8F10",
      "name": "Polite decline",
      "prompt": "Rewrite the selected text as a polite, warm refusal. Keep the same decision and facts. Return only the rewritten text.",
      "icon": "hand.raised",
      "useResponseWindow": false,
      "isBuiltIn": false,
      "hasShortcut": false,
      "preserveFormatting": false
    }
  ],
  "gallery": {
    "category": "email",
    "description": {
      "en": "Turns a blunt refusal into a courteous one.",
      "vi": "Biến lời từ chối thẳng thành lời từ chối lịch sự."
    },
    "tags": ["email", "tone"],
    "author": "your-github-username"
  }
}
```

| Field | Rule |
|---|---|
| file name | `<slug>.json`, 3–48 lowercase letters, digits or `-`; `index` is reserved |
| `commands` | exactly one command; `id` is a unique UUID |
| `name` | 2–40 characters, one line, unique in the gallery |
| `prompt` | 10–2000 characters |
| `icon` | an SF Symbol name such as `hand.raised` (shown by the macOS app; Windows and Linux fall back to a default icon) |
| `gallery.category` | `writing`, `email`, `translation`, `summarizing`, `coding`, `learning` or `productivity` |
| `gallery.description` | `en` is required, `vi` is optional; 10–160 characters each, one line |
| `gallery.tags` | up to 5 lowercase words (a–z, 0–9, `-`) |
| `gallery.author` | your GitHub username |

## What the checks reject

Shared files come from the community, so they stay safe to import:

- any provider, model or custom-provider field (a command must never send text to another server), and API keys
- links (`http://`, `https://`, `www.`) and key- or token-like strings, in the prompt and in the descriptions
- built-in commands, keyboard shortcuts, a `customInstruction`, and any unknown field
- files over 16 KB, duplicate ids and duplicate names

Contributions are reviewed before they are merged. By contributing you agree your command is shared under the GPL-3.0 license of this project.
