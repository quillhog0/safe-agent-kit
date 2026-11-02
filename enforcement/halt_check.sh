#!/usr/bin/env bash
# halt_check.sh — exit 1 if HALT file exists
# Usage: HALT_FILE=state/HALT ./halt_check.sh
# or: ./halt_check.sh path/to/HALT

set -euo pipefail
HALT="${1:-${HALT_FILE:-state/HALT}}"
if [[ -f "$HALT" ]]; then
  echo "HALT file exists at $HALT — external state actions blocked"
  exit 1
fi
echo "HALT_CHECKED: yes (file $HALT absent)"
exit 0
