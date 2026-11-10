#!/usr/bin/env bash
# forbidden_grep.sh — fail if forbidden patterns appear
# Usage: ./forbidden_grep.sh "pattern1|pattern2" [paths...]
# or set FORBIDDEN_PATTERNS_GREP
#
# The pattern is an extended regular expression (grep -E).
# Directories .git and _archive are skipped.
# If no pattern is configured, this script exits 2 (fail closed).
# It never treats an empty pattern as "all clear".

set -euo pipefail
PATTERN="${1:-${FORBIDDEN_PATTERNS_GREP:-}}"
if [[ -n "${1:-}" ]]; then
  shift
fi
PATHS=("$@")
if [[ -z "$PATTERN" ]]; then
  echo "forbidden_grep: ERROR: no pattern configured." >&2
  echo "Set FORBIDDEN_PATTERNS_GREP or pass a pattern as the first argument." >&2
  echo "Refusing to pass with an empty pattern (fail closed)." >&2
  exit 2
fi
if [[ ${#PATHS[@]} -eq 0 ]]; then
  PATHS=(.)
fi
# The `if` keeps a no-match exit from triggering `set -e`.
if grep -rEn "$PATTERN" "${PATHS[@]}" --exclude-dir=.git --exclude-dir=_archive 2>/dev/null; then
  echo "Forbidden pattern found" >&2
  exit 1
fi
echo "forbidden_grep: clean"
exit 0
