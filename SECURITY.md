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

- On macOS, API keys are stored in the Keychain. On Windows and Linux, provider keys are saved
  in the app's settings file with light obfuscation, which is not encryption. Keys set per
  command use the OS keyring when available.
- Release binaries ship with SHA-256 checksums and build provenance. Verify with
  `gh attestation verify <file> --repo gemkids275/AIShortcuts`.
