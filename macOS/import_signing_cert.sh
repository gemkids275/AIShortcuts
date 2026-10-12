#!/bin/bash
set -euo pipefail

# Imports the release signing certificate into a temporary keychain (CI only).
# Env: MAC_SIGNING_P12_BASE64, MAC_SIGNING_P12_PASSWORD, RUNNER_TEMP, GITHUB_ENV.
# Exports SIGN_IDENTITY (certificate SHA-1) and SIGN_KEYCHAIN for export_app.sh.
# Without the secrets (pull requests from forks, no certificate configured) it does
# nothing and the app is signed ad-hoc instead.

if [ -z "${MAC_SIGNING_P12_BASE64:-}" ]; then
    echo "No signing certificate configured: the app will be signed ad-hoc."
    exit 0
fi

keychain="$RUNNER_TEMP/signing.keychain-db"
keychain_password="$(uuidgen)"
p12="$RUNNER_TEMP/signing.p12"

security create-keychain -p "$keychain_password" "$keychain"
security set-keychain-settings -lut 3600 "$keychain"
security unlock-keychain -p "$keychain_password" "$keychain"
echo "$MAC_SIGNING_P12_BASE64" | base64 --decode > "$p12"
security import "$p12" -k "$keychain" -P "$MAC_SIGNING_P12_PASSWORD" -T /usr/bin/codesign
rm "$p12"
security set-key-partition-list -S apple-tool:,apple: -s -k "$keychain_password" "$keychain" > /dev/null

# codesign only accepts identities the system trusts for code signing. This runs on a
# throwaway CI runner (passwordless sudo), so trusting our own certificate there is safe.
cert="$RUNNER_TEMP/signing-cert.pem"
security find-certificate -c "AI Shortcuts Release Signing" -p "$keychain" > "$cert"
sudo security add-trusted-cert -d -r trustRoot -p codeSign -k /Library/Keychains/System.keychain "$cert"
rm "$cert"

identity="$(security find-identity -v -p codesigning "$keychain" | awk '/^ *1\)/ {print $2}')"
[ -n "$identity" ] || { echo "::error::No code signing identity found in the imported certificate"; exit 1; }

echo "SIGN_IDENTITY=$identity" >> "$GITHUB_ENV"
echo "SIGN_KEYCHAIN=$keychain" >> "$GITHUB_ENV"
echo "Signing identity imported: $identity"
