# Safe AI Agent Team Kit

**Drop-in `AGENTS.md` role templates that keep AI coding agents away from live systems, secrets and made-up claims.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) · Works with Cursor · Claude Code · Codex · Gemini CLI · anything that reads `AGENTS.md`

## Why
AI agents are fast. Near production, payments or trading infrastructure, fast is also how things break. An agent restarts the live service instead of the copy, trusts a stale comment over the code, "fixes" a red test by skipping it, or ends up reading a `.env`. Most of these failures come from the process, and a model upgrade won't fix them.

This kit is a set of plain-Markdown rules, derived from real multi-agent incidents:
- **DRY_RUN by default.** No agent switches anything to live.
- **Nothing irreversible without a human yes:** push, publish, merge, money and deletion.
- **Secrets are untouchable.** If an agent finds one, it reports the path and type only.
- **Code is the source of truth.** Claims need `file:line` evidence.
- **Agents archive files and never delete them.** Failing tests are never bypassed.
- **Every task ends in the same report format**, so you can review it in a minute.
- **Clear escalation.** Technical questions get an ADR, and only business, money and irreversible items reach you.

See [`docs/WAR_STORIES.md`](docs/WAR_STORIES.md) for the incidents these rules came from.

## Enforcement
These rules tell agents what to do. Optional stronger enforcement: [QA-Ecosystem](https://github.com/quillhog0/QA-Ecosystem) runs the tests in an isolated sandbox, maps claims to tests and can return a veto if docs, code and tests disagree. The kit itself works without it.

## What's inside
| File | Role | Use when |
| :--- | :--- | :--- |
| [`roles/00_TEAM_CHARTER.md`](roles/00_TEAM_CHARTER.md) | Shared hard rules, rule hierarchy, kill switch, report format | Always |
| [`roles/01_IDE_CODER.md`](roles/01_IDE_CODER.md) | Coding agent with quality gates / Definition of Done | Always |
| [`roles/02_LIBRARIAN.md`](roles/02_LIBRARIAN.md) | Keeps docs true to code: may only edit docs/comments, checks comment edits leave the syntax tree unchanged, keeps the incident log | Docs keep drifting |
| [`roles/03_ORCHESTRATOR_PM.md`](roles/03_ORCHESTRATOR_PM.md) | Plans phases, briefs agents, decides technical questions | 2+ agents |
| [`roles/04_REVIEWER.md`](roles/04_REVIEWER.md) | Review order + SHIP / SHIP WITH FIXES / REJECT | Before every merge |
| [`roles/05_MONEY_GUARD.md`](roles/05_MONEY_GUARD.md) | Rules for payments, billing, wallets, trading, spend | Anything with money |
| [`roles/06_ESCALATION_ADR.md`](roles/06_ESCALATION_ADR.md) | When an agent decides itself and when it asks the human, plus the ADR template | Always |
| [`roles/07_CLEANUP_CARTOGRAPHER.md`](roles/07_CLEANUP_CARTOGRAPHER.md) | Inventory/tidy a legacy repo, zero behaviour change | Inherited mess |
| [`roles/08_DEPLOY_HARDENING.md`](roles/08_DEPLOY_HARDENING.md) | Optional deploy / persistence / config checklist (from war stories) | Before production deploys |
| [`templates/`](templates/) | `INCIDENTS.md`, `OPEN_QUESTIONS.md`, folder `AGENTS.md` | Drop into `docs/` |
| [`enforcement/`](enforcement/) | Small scripts: halt check, forbidden grep, AST gate, example CI | Optional mechanical enforcement |
| [`examples/minimal/`](examples/minimal/) | Fully filled example files | Copy-paste starting point |
| [`examples/realistic/`](examples/realistic/) | Realistic example with sample report, ADR, incident | See full flow |
| [`templates/cursor/`](templates/cursor/) | Ready `.mdc` for Cursor | Drop into `.cursor/rules/` |
| [`templates/claude/`](templates/claude/) | Ready agent files for Claude Code | Drop into `.claude/agents/` |
| [`templates/antigravity/`](templates/antigravity/) | Rules + agents for Antigravity | Drop `.agents/` contents |
| [`templates/vscode/`](templates/vscode/) | Copilot instructions | Drop as `.github/copilot-instructions.md` |
| [`templates/codex/`](templates/codex/) | AGENTS.md for Codex | Drop as root `AGENTS.md` |

Project specifics are `{{PLACEHOLDERS}}`. Syntax: `{{KEY|default}}` uses the default if you leave it empty. List them with:
```bash
grep -rnoE "\{\{[^}]+\}\}" roles templates | sort -u
```

## Quick start

### Turn it on in 2 minutes
1. Copy into the root of your project:
   ```bash
   cp roles/00_TEAM_CHARTER.md ./TEAM_CHARTER.md
   cp roles/01_IDE_CODER.md ./AGENTS.md
   ```
2. Open `TEAM_CHARTER.md` and fill the 6 required values: `PROJECT_NAME`, `OWNER_NAME`, `REPO_ROOT`, `MAIN_BRANCH`, `TEST_COMMAND`, `LINT_COMMAND`.
3. Copy the ready template for your IDE (see below). Done.

That's all you need. The kit starts working.

### Per IDE
- **Antigravity**:  
  `mkdir -p .agents/rules .agents/agents`  
  `cp templates/antigravity/rules/* .agents/rules/`  
  `cp templates/antigravity/agents/* .agents/agents/`  
  Set the rules to Always On.
- **Cursor**: `cp templates/cursor/coder.mdc .cursor/rules/`
- **Claude Code**: `cp templates/claude/* .claude/agents/` + add `@TEAM_CHARTER.md` and `@AGENTS.md` in `CLAUDE.md`
- **VS Code Copilot**: `cp templates/vscode/copilot-instructions.md .github/copilot-instructions.md`
- **Codex**: `cp templates/codex/AGENTS.md ./AGENTS.md`

### Úplný postup (když chceš všechno)
Minimum required placeholders: `PROJECT_NAME`, `OWNER_NAME`, `REPO_ROOT`, `MAIN_BRANCH`, `TEST_COMMAND`, `LINT_COMMAND`. The rest are optional.

1. Copy:
   - `roles/00_TEAM_CHARTER.md` → root `TEAM_CHARTER.md`
   - `roles/06_ESCALATION_ADR.md` → root `ESCALATION_ADR.md`
   - `roles/01_IDE_CODER.md` → root `AGENTS.md` (or your tool's rules file)
   - `roles/02_LIBRARIAN.md` → root or `docs/` (if you use the Librarian)
   - `templates/*` → `docs/`
   - Optionally `roles/08_DEPLOY_HARDENING.md` and `enforcement/` scripts.
2. Fill the minimum placeholders (or copy from `examples/minimal/` or `examples/realistic/`).
3. Wire the files into your tool (or use the templates above).

4. Enforce what you can outside the prompt: copy scripts from `enforcement/`, a pre-commit secret scan, a CI grep for forbidden IDs, coverage gates, and branch protection. See `enforcement/README.md`.

## Role isolation
Roles are text. To stop one agent from playing multiple roles:
- Use separate chats / agent instances / workspaces.
- Cursor: different `.mdc` files, open Reviewer in a new chat.
- Claude Code: separate files under `.claude/agents/`.
- Never let the same session both write code and approve it.


## How the roles work together
```mermaid
flowchart LR
    H([Human owner]) -->|goals, yes/no on irreversible items| O[Orchestrator / PM]
    O -->|task brief| C[IDE Coder]
    C -->|diff + standard report| R[Reviewer]
    R -->|SHIP / FIXES / REJECT| O
    R -->|doc drift| L[Librarian]
    C -->|fix commits| L
    L -->|docs-only branch| H
    M[Money Guard] -. limits & sandbox .-> C
    O -->|technical decisions| A[(ADRs)]
    O -->|business / money / live / publish| H
    H -->|merge| G[(main branch)]
```

## Honest limits
- These are instructions. Models can still ignore them, so the kit lowers risk but can't remove it.
- Keep real credentials out of agent reach and keep the human approval step real.
- The kit deliberately leaves out stack-specific style rules. Use it alongside your own.
- Nothing here is financial, legal or tax advice.

## Contributing
New roles, tool-specific setups and war stories are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
