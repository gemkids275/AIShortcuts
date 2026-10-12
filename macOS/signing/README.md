# macOS release signing material

The macOS releases are signed with one fixed self-signed certificate so the app keeps the
same identity across updates (macOS then keeps its Accessibility / Screen Recording grants).

| File | Tracked | What it is |
|---|---|---|
| `cert.cnf`, `create_certificate.sh` | yes | how the certificate is generated |
| `key.pem`, `cert.pem`, `signing.p12`, `signing.p12.base64`, `p12.password` | **no (git-ignored)** | the certificate and its private key |

- CI reads the certificate from the GitHub secrets `MAC_SIGNING_P12_BASE64` and
  `MAC_SIGNING_P12_PASSWORD` (see `../import_signing_cert.sh`); it never reads this folder.
- Back these files up somewhere safe (password manager). If they are lost, create a new
  certificate and users have to grant the permissions once more.
- Never commit them. CI fails if a key or certificate file is tracked.
