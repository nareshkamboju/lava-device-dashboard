#!/usr/bin/env bash
# Regenerate the LAVA HYD device dashboard and publish it to GitHub Pages.
#
# Layout assumption:
#   <lava-dispatcher-config>/                          <- worker-configs/ + gen_dashboard.py
#   <lava-dispatcher-config>/lava-device-dashboard/    <- this Pages repo (run from here)
#
# Usage:  ./deploy.sh ["optional commit message"]
set -euo pipefail

# Directory of this script = the Pages repo root.
PAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Source checkout with worker-configs + gen_dashboard.py (the parent dir).
SRC_DIR="$(dirname "$PAGES_DIR")"
OUT_DIR="$(mktemp -d)"
MSG="${1:-Regenerate dashboard data}"

trap 'rm -rf "$OUT_DIR"' EXIT

if [[ ! -f "$SRC_DIR/gen_dashboard.py" || ! -d "$SRC_DIR/worker-configs" ]]; then
  echo "ERROR: expected gen_dashboard.py and worker-configs/ in: $SRC_DIR" >&2
  exit 1
fi

echo ">> Regenerating dashboard from: $SRC_DIR"
( cd "$SRC_DIR" && python3 gen_dashboard.py "$OUT_DIR" )

echo ">> Copying generated files into: $PAGES_DIR"
cp -f "$OUT_DIR/data.json"  "$PAGES_DIR/data.json"
cp -f "$OUT_DIR/index.html" "$PAGES_DIR/index.html"

cd "$PAGES_DIR"
if git diff --quiet -- data.json index.html; then
  echo ">> No changes to publish."
  exit 0
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"

echo ">> Committing..."
git add data.json index.html
git commit -m "$MSG"

echo ">> Syncing with remote (rebase) and pushing..."
git pull --rebase origin "$BRANCH"
git push origin "$BRANCH"

echo ">> Done. GitHub Pages will redeploy shortly."
echo "   URL: https://nareshkamboju.github.io/lava-device-dashboard/"