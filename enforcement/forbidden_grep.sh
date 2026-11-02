#!/usr/bin/env bash
# forbidden_grep.sh — fail if forbidden patterns appear
# Usage: ./forbidden_grep.sh "pattern1|pattern2" [paths...]
# or set FORBIDDEN_PATTERNS_GREP

set -euo pipefail
PATTERN="${1:-${FORBIDDEN_PATTERNS_GREP:-}}"
shift || true
PATHS=("$@")
if [[ -z "$PATTERN" ]]; then
  echo "No pattern given. Set FORBIDDEN_PATTERNS_GREP or pass as first arg."
  exit 0
fi
if [[ ${#PATHS[@]} -eq 0 ]]; then
  PATHS=(.)
fi
if grep -rEn "$PATTERN" "${PATHS[@]}" --exclude-dir=.git --exclude-dir=_archive 2>/dev/null; then
  echo "Forbidden pattern found"
  exit 1
fi
echo "forbidden_grep: clean"
exit 0
