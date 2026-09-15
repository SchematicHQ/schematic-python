#!/usr/bin/env bash
set -euo pipefail

# Builds the release artifact from the working tree and installs it the way an
# end user would, for the `pack` install mode of the SDK E2E harness
# (SchematicHQ/actions .github/workflows/sdk-e2e.yml).
#
# `pip install .` would also build a wheel, but it is not the artifact we ship.
# This builds what `poetry build` produces, checks the rules engine WASM really
# made it into the wheel, and installs that wheel with the datastream extra, so
# a broken package fails pre-merge instead of after publishing.
#
# Usage (from the repo root):
#     ./scripts/e2e-pack.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="${PYTHON:-python}"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=python3

# ---------------------------------------------------------------------------
# 1. Rules engine WASM
# ---------------------------------------------------------------------------
# Always run it: the script is a no-op when the pinned WASM_VERSION is already
# on disk, and re-running is what picks up a version bump.
echo "==> Fetching rules engine WASM"
./scripts/download-wasm.sh

# ---------------------------------------------------------------------------
# 2. Build the release artifact (sdist + wheel)
# ---------------------------------------------------------------------------
# Build through PEP 517 (`python -m build`) rather than whatever `poetry` happens
# to be on the E2E runner. `build` resolves the backend from the pyproject
# build-system requires, so the artifact matches what CI publishes with poetry
# 2.1.4. It matters: poetry-core 1.x (poetry 1.8) silently drops the WASM from
# the wheel, which would fail the check below for a reason the release does not
# actually have.
echo "==> Building release artifact"
rm -rf dist
"$PYTHON" -m pip install --quiet --upgrade build
"$PYTHON" -m build

shopt -s nullglob
wheels=(dist/*.whl)
shopt -u nullglob
if [ "${#wheels[@]}" -ne 1 ]; then
    echo "ERROR: expected exactly one wheel in dist/, found ${#wheels[@]}:" >&2
    ls -la dist >&2 || true
    exit 1
fi
WHEEL="${wheels[0]}"
echo "Built $WHEEL"

# ---------------------------------------------------------------------------
# 3. The WASM must be inside the wheel
# ---------------------------------------------------------------------------
# List once into a variable: `unzip -l | grep -q` dies of SIGPIPE under pipefail.
wheel_files="$(unzip -Z1 "$WHEEL")"
if ! wasm_in_wheel="$(printf '%s\n' "$wheel_files" | grep -E '^schematic/datastream/wasm/[^/]+\.wasm$')"; then
    echo "ERROR: no schematic/datastream/wasm/*.wasm in $WHEEL" >&2
    echo "The datastream rules engine will not work for anyone installing this package." >&2
    echo "Check the pyproject [tool.poetry] include entry and scripts/download-wasm.sh." >&2
    printf '%s\n' "$wheel_files" >&2
    exit 1
fi
echo "==> WASM found in wheel: $wasm_in_wheel"

# ---------------------------------------------------------------------------
# 4. Install the wheel, then the testapp deps
# ---------------------------------------------------------------------------
# testapp/requirements.txt lists `schematichq`, so order matters: install the
# wheel first (pip then treats the requirement as already satisfied and does not
# reach PyPI for it), and reinstall it afterwards anyway so the local build is
# unambiguously what ends up in site-packages.
echo "==> Installing $WHEEL[datastream]"
"$PYTHON" -m pip install "${WHEEL}[datastream]"

echo "==> Installing testapp requirements"
"$PYTHON" -m pip install -r testapp/requirements.txt

"$PYTHON" -m pip install --force-reinstall --no-deps "$WHEEL"

# ---------------------------------------------------------------------------
# 5. Verify what actually got installed
# ---------------------------------------------------------------------------
echo "==> Verifying installed package"
WHEEL="$WHEEL" "$PYTHON" - <<'PY'
import glob
import os
import sys
import sysconfig

wheel = os.path.basename(os.environ["WHEEL"])
expected_version = wheel.split("-")[1]

import schematic  # noqa: E402

pkg_dir = os.path.dirname(os.path.abspath(schematic.__file__))
site_packages = os.path.abspath(sysconfig.get_paths()["purelib"])

errors = []
if os.path.commonpath([pkg_dir, site_packages]) != site_packages:
    errors.append(f"schematic imported from {pkg_dir}, not from site-packages ({site_packages})")

try:
    from importlib.metadata import version as dist_version
    installed_version = dist_version("schematichq")
except Exception as e:  # pragma: no cover
    installed_version = None
    errors.append(f"could not read installed schematichq version: {e}")

if installed_version is not None and installed_version != expected_version:
    errors.append(f"installed schematichq {installed_version}, expected {expected_version} from {wheel}")

wasm = glob.glob(os.path.join(pkg_dir, "datastream", "wasm", "*.wasm"))
if not wasm:
    errors.append(f"no *.wasm in {os.path.join(pkg_dir, 'datastream', 'wasm')}")

if errors:
    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    sys.exit(1)

print(f"schematichq {installed_version} installed at {pkg_dir}")
for path in wasm:
    print(f"  wasm: {os.path.relpath(path, pkg_dir)} ({os.path.getsize(path)} bytes)")
PY

"$PYTHON" -m pip show schematichq | grep -E '^(Name|Version|Location):'
echo "==> pack install ready"
