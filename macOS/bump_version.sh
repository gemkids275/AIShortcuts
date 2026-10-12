#!/bin/bash
set -e

# Sets the macOS app version in the Xcode project and in the update-check file.
# Usage: ./macOS/bump_version.sh 1.2

VERSION="$1"
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Usage: $0 <X.Y[.Z]>"
    exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"

perl -pi -e "s/MARKETING_VERSION = [^;]*;/MARKETING_VERSION = $VERSION;/" "$DIR/AI Shortcuts.xcodeproj/project.pbxproj"
echo "$VERSION" > "$DIR/Latest_Version_for_Update_Check.txt"

echo "Version set to $VERSION."
echo "Next: write macOS/release-notes/mac-v$VERSION.md, merge to main, then tag mac-v$VERSION."
