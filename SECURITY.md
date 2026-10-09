# Security Policy

## Supported versions

Only the latest release of each platform receives security fixes:

- macOS: the latest `v*` release
- Windows & Linux: the latest `win-v*` release

## Reporting a vulnerability

Please do **not** open a public issue for security problems.

Use GitHub's private reporting: **Security → Report a vulnerability** on
[gemkids275/AIShortcuts](https://github.com/gemkids275/AIShortcuts/security/advisories/new),
or email **gemkids275@gmail.com**.

Include the affected version, steps to reproduce and the impact. You can expect
a first reply within a few days.

## Scope notes

- API keys are stored in the macOS Keychain or the OS keyring. Without a keyring,
  per-command keys fall back to a lightly obfuscated local file, which is not
  encrypted storage.
- Release binaries ship with SHA-256 checksums and build provenance. Verify with
  `gh attestation verify <file> --repo gemkids275/AIShortcuts`.
