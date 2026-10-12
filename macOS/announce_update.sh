#!/bin/bash
set -e

# Tells existing users that version <X.Y> is available, by updating the file the
# in-app update checker reads from main. Refuses to run unless the GitHub release
# for mac-v<X.Y> exists and has its DMG, so nobody is told to update too early.
# Usage: ./macOS/announce_update.sh 1.2   (then commit and merge the change)

VERSION="$1"
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Usage: $0 <X.Y[.Z]>"
    exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"

assets="$(gh release view "mac-v$VERSION" --json assets --jq '.assets[].name')" || {
    echo "Release mac-v$VERSION not found. Publish it first."
    exit 1
}
echo "$assets" | grep -qx "AI_Shortcuts_v$VERSION.dmg" || {
    echo "Release mac-v$VERSION has no AI_Shortcuts_v$VERSION.dmg asset."
    exit 1
}

echo "$VERSION" > "$DIR/Latest_Version_for_Update_Check.txt"
echo "Update notice set to $VERSION. Commit and merge this change to announce it."
