#!/usr/bin/env bash
# Regenerate the LAVA HYD device dashboard and publish it to GitHub Pages.
#
# This repo is self-contained: it ships lava_scrape.py + dashboard_template.html.
# It only needs a worker-configs/ directory, found via (in order):
#   1. $WORKER_CONFIGS_DIR
#   2. ./worker-configs inside this repo
#   3. ../lava-dispatcher-config/worker-configs (sibling checkout)
#
# Usage:  ./deploy.sh ["optional commit message"]
set -euo pipefail

# Directory of this script = the Pages repo root.
PAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$(mktemp -d)"
MSG="${1:-Regenerate dashboard data}"

trap 'rm -rf "$OUT_DIR"' EXIT

if [[ ! -f "$PAGES_DIR/lava_scrape.py" ]]; then
  echo "ERROR: lava_scrape.py not found in: $PAGES_DIR" >&2
  exit 1
fi

echo ">> Scraping live device data from LAVA"
python3 "$PAGES_DIR/lava_scrape.py" "$OUT_DIR"

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