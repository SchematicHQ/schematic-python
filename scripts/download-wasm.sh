#!/bin/bash
set -e

# Downloads the rules engine WASM binary from the schematic-api GitHub Release.
# Reads the pinned version from WASM_VERSION at the repo root.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WASM_DIR="$REPO_ROOT/src/schematic/datastream/wasm"
VERSION_FILE="$REPO_ROOT/WASM_VERSION"
TARGET_FILE="$WASM_DIR/rulesengine.wasm"

GITHUB_REPO="SchematicHQ/schematic-api"

if [ ! -f "$VERSION_FILE" ]; then
    echo "ERROR: WASM_VERSION file not found at $VERSION_FILE"
    exit 1
fi

VERSION=$(tr -d '[:space:]' < "$VERSION_FILE")
TAG="rulesengine/v${VERSION}"

# Skip download if binary already exists and version matches
if [ -f "$TARGET_FILE" ] && [ -f "$WASM_DIR/.wasm_version" ]; then
    CURRENT=$(tr -d '[:space:]' < "$WASM_DIR/.wasm_version")
    if [ "$CURRENT" = "$VERSION" ]; then
        echo "WASM binary already at version $VERSION, skipping download."
        exit 0
    fi
fi

ASSET_NAME="rulesengine-wasm-python-v${VERSION}.tar.gz"

echo "Downloading rules engine WASM v${VERSION}..."
mkdir -p "$WASM_DIR"

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

if ! gh release download "$TAG" \
    -R "$GITHUB_REPO" \
    -p "$ASSET_NAME" \
    -D "$TMPDIR" 2>/dev/null; then
    echo "ERROR: Failed to download WASM binary"
    echo "Tag: $TAG"
    echo "Asset: $ASSET_NAME"
    echo ""
    echo "If this is a new version, ensure a release exists at:"
    echo "  https://github.com/${GITHUB_REPO}/releases/tag/${TAG}"
    echo ""
    echo "Ensure the GitHub CLI is authenticated: gh auth status"
    exit 1
fi

tar -xzf "$TMPDIR/$ASSET_NAME" -C "$TMPDIR"

if [ ! -f "$TMPDIR/rulesengine.wasm" ]; then
    echo "ERROR: rulesengine.wasm not found in release archive"
    ls -la "$TMPDIR"
    exit 1
fi

cp "$TMPDIR/rulesengine.wasm" "$TARGET_FILE"
echo "$VERSION" > "$WASM_DIR/.wasm_version"

echo "Downloaded rules engine WASM v${VERSION} to $TARGET_FILE"
