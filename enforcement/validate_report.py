#!/usr/bin/env python3
"""validate_report.py — check a task report has the required fields and values.

Usage: python3 validate_report.py report.md
Exit 0 if valid, 1 otherwise, 2 on usage errors.

This checks the standard report format from TEAM_CHARTER.md §5:
field presence, allowed values for STATUS / HALT_CHECKED /
RULE_FILES_TOUCHED, and that value fields are not empty.
It does not check whether the claims in the report are true.
"""
import re
import sys

# Field name as it appears before the colon, then:
# - enum: required first token (or whole value)
# - required: must be present
# - prefix: name is a prefix (QUESTIONS FOR <owner>)
FIELDS = [
    {"key": "STATUS", "enum": ("DONE", "PARTIAL", "BLOCKED", "HANDED_TO_REVIEW")},
    {"key": "CHANGED", "non_empty": True},
    {"key": "VERIFIED", "non_empty": True},
    {"key": "NOT DONE / SKIPPED", "non_empty": True},
    {"key": "RISKS", "non_empty": True},
    {"key": "HALT_CHECKED", "enum": ("yes", "no", "n/a")},
    {"key": "RULE_FILES_TOUCHED", "enum": ("yes", "no")},
    {"key": "QUESTIONS FOR", "prefix": True, "non_empty": True},
]

# A line starts a new field if it matches one of the known names.
FIELD_START = re.compile(
    r"^(STATUS|CHANGED|VERIFIED|NOT DONE / SKIPPED|RISKS|"
    r"HALT_CHECKED|RULE_FILES_TOUCHED|QUESTIONS FOR)(?:\s+[^:]*)?\s*:",
    re.M,
)


def parse_fields(text: str) -> dict[str, str]:
    """Return {canonical_key: value} for known fields, last occurrence wins."""
    matches = list(FIELD_START.finditer(text))
    found: dict[str, str] = {}
    for i, m in enumerate(matches):
        raw_key = m.group(1)
        key = "QUESTIONS FOR" if raw_key.startswith("QUESTIONS FOR") else raw_key
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        value = text[start:end].strip()
        found[key] = value
    return found


def validate(text: str) -> list[str]:
    errors = []
    found = parse_fields(text)
    for spec in FIELDS:
        key = spec["key"]
        if key not in found:
            errors.append(f"missing field: {key}")
            continue
        value = found[key]
        if spec.get("non_empty") and not value:
            errors.append(f"empty value: {key}")
            continue
        if "enum" in spec:
            first = value.split()[0] if value else ""
            # Allow a trailing parenthetical or comment after the enum token.
            first = first.rstrip(",.;")
            if first not in spec["enum"]:
                allowed = " | ".join(spec["enum"])
                errors.append(f"invalid {key} value {value!r} (expected {allowed})")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_report.py <report.md>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"Cannot read file: {e}", file=sys.stderr)
        sys.exit(1)
    errors = validate(text)
    if errors:
        print("Invalid report:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        sys.exit(1)
    print("report: valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
