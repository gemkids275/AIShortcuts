#!/bin/bash
set -e

# Sets the macOS app version in the Xcode project.
# Usage: ./macOS/bump_version.sh 1.2
# The update notice for existing users is NOT changed here: run announce_update.sh
# only after the GitHub release exists.

VERSION="$1"
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Usage: $0 <X.Y[.Z]>"
    exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"

perl -pi -e "s/MARKETING_VERSION = [^;]*;/MARKETING_VERSION = $VERSION;/" "$DIR/AI Shortcuts.xcodeproj/project.pbxproj"

echo "Version set to $VERSION."
echo "Next: write macOS/release-notes/mac-v$VERSION.md, merge to main, tag mac-v$VERSION,"
echo "then, once the release is published, run macOS/announce_update.sh $VERSION."
