# Changelog
All notable changes to this project are documented here. Format: [Keep a Changelog](https://keepachangelog.com/), versioning: [SemVer](https://semver.org/).

## [Unreleased]
### Added
- Hard rule 11: rule files immutable for agents.
- Task lifecycle section and new report fields (HALT_CHECKED, RULE_FILES_TOUCHED, HANDED_TO_REVIEW).
- External-truth exception in charter §6.
- Optional Deploy Hardening role (08).
- enforcement/ scripts (halt_check, forbidden_grep, ast_gate, example CI).
- examples/minimal/ filled starter.
- Reverse map in WAR_STORIES.

### Changed
- Archive location unified to `_archive/`.
- Librarian critical alerts go through report + INCIDENTS.md only.
- Money Guard rule 5 marked optional (trading-specific).
- README: placeholder syntax, minimum set, quick-start file list, softened "battle-tested".

### Added
- Team charter with shared hard rules, rule hierarchy, kill switch and standard report format.
- Roles: IDE Coder, Librarian, Orchestrator/PM, Reviewer, Money Guard, Escalation & ADR, Cleanup Cartographer.
- Templates: incident log, open questions, folder-level `AGENTS.md`.
- War stories, contributing guide, role-request issue template.
- Released under the MIT License.
