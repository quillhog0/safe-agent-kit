# Enforcement scripts

Copy the scripts you need into your repo and wire them into pre-commit or CI.

- `halt_check.sh` — fails if the HALT file exists.
- `forbidden_grep.sh` — fails on forbidden patterns (set `FORBIDDEN_PATTERNS_GREP` or pass the pattern as the first argument). The pattern is an extended regular expression. If no pattern is configured, the script exits 2 (fail closed) instead of passing.
- `ast_gate.py` — **Python only.** Compares two `.py` files' syntax trees after stripping docstrings. Comments are already ignored by the Python parser. Exit 0 if the trees match. This is not a multi-language checker; TypeScript and other languages are not supported.
- `validate_report.py` — checks a task report has the required fields from the charter (STATUS, CHANGED, VERIFIED, NOT DONE / SKIPPED, RISKS, HALT_CHECKED, RULE_FILES_TOUCHED, QUESTIONS FOR) and that enum fields use an allowed value. It does not check whether the claims in the report are true.
- `.pre-commit-config.yaml` — example. The forbidden-grep hook will fail until you set `FORBIDDEN_PATTERNS_GREP`.
- `github-workflow-example.yml` — example PR check that also guards rule files.

Fill placeholders and adjust paths before use.

Tests for these scripts live in `tests/`. From the repo root:

```bash
python3 -m pytest -q
```
