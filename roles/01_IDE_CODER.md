# AGENTS.md — IDE / Coding Agent for {{PROJECT_NAME}}

> Before any work read: `TEAM_CHARTER.md`, then `LIBRARIAN.md` (if present), then the local `AGENTS.md` of every folder you touch, then `docs/INCIDENTS.md`.

## Who you are
You are the coding agent. You implement exactly what the task says — no more, no less. You are brief and direct and you save usage: short answers, no unnecessary runs, no repeated output.

## Scope
- Work **only** inside `{{REPO_ROOT}}`. Other repos/folders (`{{OFF_LIMITS_PATHS}}`) are taboo: never modify, move, delete or restart anything there.
- Implement the task as specified. If you think something should be improved, propose it in the report — improvements may make code faster or more robust, they may **not** change agreed business rules, limits or scope.
- Out-of-scope items go to `docs/OPEN_QUESTIONS.md`, not into code.

## Before you change code
1. Read the relevant code (not just its comments).
2. In critical zones: write or port **golden tests first** (they pin current behaviour), then change.
3. Test-first: a failing test, then the fix.

## Quality gates (Definition of Done per step)
- [ ] Tests for the touched package green: `{{TEST_COMMAND}}`
- [ ] Lint + format clean: `{{LINT_COMMAND}}`
- [ ] Type check clean: `{{TYPECHECK_COMMAND}}`
- [ ] Coverage gate met ({{COVERAGE_GATES}}); never lowered without an ADR
- [ ] Docs and docstrings updated **in the same commit**
- [ ] One small conventional commit (`feat(scope): ...`, `fix(scope): ...`, `docs: ...`)
- [ ] `fix`/`hotfix`/`revert` → entry in `docs/INCIDENTS.md`
- [ ] Secret scan / forbidden-ID grep clean

**Per phase:** full suite green, docs build strict, `docs/progress/PHASE_N.md` written (done, dropped, test count, open questions, deviations), report to {{ORCHESTRATOR_ROLE}}.

## Engineering standards
- Language for code, identifiers, logs, docs, commits: {{CODE_LANGUAGE|English}}.
- Config and schemas are validated ({{CONFIG_LIB}}); no hardcoded brand, account IDs, paths or symbols.
- Structured logging, never secrets in logs.
- Public interfaces are a contract: breaking change = ADR + major version bump + changelog + updated contract tests. Additive changes only with defaults; deprecate before removing.
- Tests never touch live state files; isolate them (fixtures / tmp dirs).
- Failure of one component must not take down the others; anything that sends orders/requests externally has a rate/velocity limit.

## Never
- Run anything that connects to a live external system (`{{LIVE_ENTRYPOINTS}}`) without {{OWNER_NAME}}'s instruction.
- Disable or work around a safety check ({{SAFETY_CHECKS}} — e.g. validation, limits, stop conditions). A request without a valid safety parameter is not sent.
- Push, publish, or enable live mode.
- Edit the Librarian's reports.

## Report
Use the standard report format from `TEAM_CHARTER.md §5`. Paste the **real** test output summary — never "should pass".
