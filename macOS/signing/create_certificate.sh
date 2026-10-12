#!/bin/bash
set -euo pipefail

# Creates the self-signed certificate used to sign macOS releases, and the base64 p12
# that goes into the GitHub secrets. Run it ONCE; keep the generated files (they are
# git-ignored) because a new certificate means a new app identity, and macOS would ask
# every user for the Accessibility / Screen Recording permissions again.

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

if [ -e key.pem ]; then
    echo "key.pem already exists: not overwriting the signing identity."
    exit 1
fi

openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 3650 -config cert.cnf
openssl rand -base64 24 | tr -d '\n' > p12.password
# -legacy: macOS `security import` cannot read the default OpenSSL 3 p12 encryption.
openssl pkcs12 -export -legacy -inkey key.pem -in cert.pem -out signing.p12 \
    -passout "file:p12.password" -name "AI Shortcuts Release Signing"
base64 -i signing.p12 | tr -d '\n' > signing.p12.base64
chmod 600 key.pem p12.password signing.p12 signing.p12.base64

echo "Created. Next, upload the secrets (they are not stored anywhere else):"
echo "  gh secret set MAC_SIGNING_P12_BASE64 < macOS/signing/signing.p12.base64"
echo "  gh secret set MAC_SIGNING_P12_PASSWORD < macOS/signing/p12.password"
