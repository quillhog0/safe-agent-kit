# Enforcement scripts

Copy the scripts you need into your repo and wire them into pre-commit or CI.

- `halt_check.sh` — fails if the HALT file exists.
- `forbidden_grep.sh` — fails on forbidden patterns (set `FORBIDDEN_PATTERNS_GREP`).
- `ast_gate.py` — Python AST comparison for comment-only changes (Librarian).
- `.pre-commit-config.yaml` — example.
- `github-workflow-example.yml` — example PR check that also guards rule files.

Fill placeholders and adjust paths before use.
