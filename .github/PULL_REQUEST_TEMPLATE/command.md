## Command

<!-- Name of the command and what it does, in one or two sentences. -->

## Checklist

- [ ] One file: `commands/<slug>.json` (lowercase letters, digits and `-`, e.g. `polite-decline.json`)
- [ ] Exported from the app (Settings → Commands → export) and the `gallery` block added, as described in [commands/README.md](../../commands/README.md); on Windows/Linux the fields `prefix`, `deletable`, `keyboard_shortcut` and `customProviderBaseUrl` removed
- [ ] `gallery.author` is my GitHub username and `gallery.category` is one of the allowed categories
- [ ] Short English description (and a Vietnamese one if I can write it)
- [ ] The prompt works on any selected text and does not depend on my own data
- [ ] No API keys or tokens, no links, no provider or model overrides (the checks reject them)
- [ ] I tested the command in the app on a few real texts
- [ ] I agree my command is shared under the GPL-3.0 license of this project

<!-- Reviewers check the file with `python .github/scripts/validate_commands.py commands`; you can run the same command. New commands appear on the website after the pull request is merged. -->
