#!/usr/bin/env bash
# Cron entrypoint: refresh the LAVA dashboard and push to GitHub.
#
# Designed to run non-interactively from crontab. It sets a sane PATH,
# points git at the SSH key, and logs each run to cron_deploy.log.
#
# Install (every 6 hours, at 00:00, 06:00, 12:00, 18:00):
#   crontab -e
#   0 */6 * * * /usr2/nkamboju/src/lava-device-dashboard/cron_deploy.sh
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$REPO/cron_deploy.log"

# Cron runs with a minimal environment; make common tools reachable.
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="${HOME:-/usr2/nkamboju}"
# Use the user's SSH key for the git push (adjust if your key differs).
export GIT_SSH_COMMAND="ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new"

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') : cron deploy start ====="
  cd "$REPO"
  ./deploy.sh "Scheduled refresh: live LAVA device data"
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') : cron deploy done ====="
} >>"$LOG" 2>&1