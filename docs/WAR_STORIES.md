# War stories

These are anonymized real incidents from multi-agent projects that the kit's rules came from. Project names, numbers and account data are removed.

## 1. The copy that started the original
**What happened.** A project was copied into a new folder so agents could rebuild it safely. The copied dashboard looked independent, but its START button still called the launch script of the **live original**. A mirrored `restart_watcher` script in the copy also pointed back at the original's processes. Pressing START in the "safe" copy would have started the live system.

**Why it hurts.** Everyone thinks they're in a sandbox, so nobody double-checks. Hardcoded paths, service names and copied scripts carry references nobody remembers, and the first sign of trouble is a live process you didn't mean to start.

**Rules that prevent it.**
- The charter's "work only inside `{{REPO_ROOT}}`", with off-limits paths listed explicitly (`01_IDE_CODER.md`).
- A **guard test** in CI that fails if code, scripts or configs reference the original project's paths, service names or identifiers (`{{FORBIDDEN_PATTERNS_GREP}}`).
- Don't run entrypoints that connect to external or live systems without a human instruction.
- The Cartographer role's inventory step, which lists hardcoded absolute paths and cross-project references before anyone works on the copy.

## 2. Docs that drifted from code
**What happened.** On an agent-written codebase, the docs slowly stopped matching reality. The README listed exported files that the code no longer produced. Comments described behaviour that had been changed. The support channel in the docs was out of date, and a payment address was hardcoded in the source while the docs claimed it came from config.

**Why it hurts.** Agents read docs and comments as context. Lying docs make every later agent session start from false premises, so the drift compounds. A hardcoded payment detail is also a money risk and an operational one.

**Rules that prevent it.**
- **Code is truth** about behaviour, and instructions are truth about intent. Every claim needs `file:line` evidence (`00_TEAM_CHARTER.md`).
- The **Librarian** role (`02_LIBRARIAN.md`) may change only docs and comments. It runs `DIFF_WATCH` on new commits and flags lying comments and hardcoded identifiers.
- **Comment-only edits must leave the syntax tree unchanged:** the source must compile before and after, with an identical syntax tree once comments are stripped. Otherwise the change is discarded.
- Docs are updated in the same commit as code, and no real identifiers (including payment details) live in code.

## 3. Lessons from trading infrastructure
**What happened.** Several separate defects turned up while building trading tooling:
- The dashboard showed a locally computed balance that differed from the broker's.
- Position IDs were reused, so new positions were matched to old records.
- Cancels of limit orders were assumed to have worked without the broker confirming them.
- Real trading costs (spread, fees) came out at roughly half of what the design had assumed, so the model of the system was wrong even where it looked "conservative".

**Why it hurts.** Every one of these makes the system believe something false about money. Decisions and risk limits based on wrong state are worse than having no automation.

**Rules that prevent it** (`05_MONEY_GUARD.md`):
- **The external provider (broker, payment provider) is the source of truth** for balances and PnL. Reconcile after every reconnect or restart.
- An operation isn't done until the external system confirms it. Unconfirmed cancels stay "pending".
- IDs come from the external system or are guaranteed unique, and the reconciliation check catches reuse.
- Cost and limit assumptions are re-validated on history and in sandbox before anyone proposes live, and results are always labelled as estimates.
