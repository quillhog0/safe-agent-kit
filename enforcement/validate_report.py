#!/usr/bin/env python3
"""validate_report.py — check a task report has required fields.
Usage: python3 validate_report.py report.md
Exit 0 if valid, 1 otherwise.
"""
import sys
import re

REQUIRED = [
    r"^STATUS:\s*(DONE|PARTIAL|BLOCKED|HANDED_TO_REVIEW)",
    r"^CHANGED:",
    r"^VERIFIED:",
    r"^HALT_CHECKED:\s*(yes|no|n/a)",
    r"^RULE_FILES_TOUCHED:\s*(yes|no)",
]

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_report.py <report.md>", file=sys.stderr)
        sys.exit(2)
    text = open(sys.argv[1]).read()
    missing = []
    for pat in REQUIRED:
        if not re.search(pat, text, re.M):
            missing.append(pat)
    if missing:
        print("Missing or invalid fields:", file=sys.stderr)
        for m in missing:
            print(" ", m, file=sys.stderr)
        sys.exit(1)
    print("report: valid")
    sys.exit(0)

if __name__ == "__main__":
    main()
