# Changelog
All notable changes to this project are documented here. Format: [Keep a Changelog](https://keepachangelog.com/), versioning: [SemVer](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-11-10

First recorded release. `plugin.json` already named this version 1.0.0; this entry is the first complete changelog for what is in the kit.

### Added
- Team charter with shared hard rules, rule hierarchy, kill switch and standard report format.
- Roles: IDE Coder, Librarian, Orchestrator/PM, Reviewer, Money Guard, Escalation & ADR, Cleanup Cartographer, and optional Deploy Hardening (08).
- Hard rule 11: rule files immutable for agents.
- Task lifecycle section and report fields (`HALT_CHECKED`, `RULE_FILES_TOUCHED`, `HANDED_TO_REVIEW`).
- External-truth exception in charter §6.
- Templates: incident log, open questions, folder-level `AGENTS.md`.
- Ready templates for Cursor, Claude Code, Antigravity, VS Code Copilot, and Codex, plus Cursor Directory / plugin files (`plugin.json`, `rules/safe-agent.mdc`, `skills/safe-agent-kit/SKILL.md`).
- IDE templates include the full hard rules and escalation text, generated from the charter and ADR (`scripts/generate_templates.py`) so they stay in sync.
- War stories (with a reverse map), contributing guide, and a role-request issue template.
- `enforcement/` scripts: `halt_check`, `forbidden_grep`, `ast_gate` (Python only), `validate_report`, plus an example CI workflow and pre-commit config.
- Tests for the enforcement scripts and the template generator.
- `examples/minimal/`: a fully filled charter, escalation rules, and coder role.
- `examples/realistic/`: the same filled starting files, plus a sample ADR, incident log, folder `AGENTS.md`, and an illustrative task report.
- Released under the MIT License.

### Changed
- Archive location unified to `_archive/`.
- Librarian critical alerts go through the standard report and `INCIDENTS.md` only.
- Money Guard rule 5 marked optional (trading-specific).
- README: placeholder syntax, minimum set, quick-start file list, and claims aligned with what the kit actually does.
- `forbidden_grep.sh` fails closed when no pattern is configured.
- `validate_report.py` checks allowed values and rejects empty fields, not only field presence.
- `ast_gate.py` states and enforces that it accepts Python files only.
- Kit CI runs the tests and the generator sync check.
- The realistic sample report is marked as an illustrative format example, not a real test run.
