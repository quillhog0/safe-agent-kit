# War stories

These are anonymized real incidents from multi-agent projects that the kit's rules came from. Project names, numbers and account data are removed. Most of the code involved was written by AI agents, and most of the bugs were found by other agents doing review or audit.

## 1. The copy that started the original
**What happened.** A project was copied into a new folder so agents could rebuild it safely. The copied dashboard looked independent, but its START button opened a terminal session, `cd`'d into the **live original's** hardcoded directory and started its engine. A copied `restart_watcher` script did the same thing from the shell: it switched into the original folder, used the original's virtualenv, killed the running engine by process name with `kill -9`, and restarted it. Pressing START in the "safe" copy would have started the original system.

**Why it hurts.** Everyone thinks they're in a sandbox, so nobody double-checks. Hardcoded paths, service names and copied scripts carry references nobody remembers, and the first sign of trouble is a live process you didn't mean to start.

**Rules that prevent it.**
- The charter's "work only inside `{{REPO_ROOT}}`", with off-limits paths listed explicitly (`00_TEAM_CHARTER.md`, `01_IDE_CODER.md`).
- A **guard test** in CI that fails if code, scripts or configs reference the original project's paths, service names or identifiers (`{{FORBIDDEN_PATTERNS_GREP}}`, `00_TEAM_CHARTER.md` hard rule 4).
- The web/API layer never spawns processes or shells out. Start/stop goes through the application's own API, and a test fails if any process-spawning call appears there.
- Don't run entrypoints that connect to external or live systems without a human instruction.
- The Cartographer role's inventory step (`07_CLEANUP_CARTOGRAPHER.md`), which lists hardcoded absolute paths and cross-project references before anyone works on the copy.

## 2. The copy also kept the real accounts and the live host
**What happened.** The same copy carried more than scripts. Real broker account IDs and trader logins were hardcoded in config, in fallback defaults in the engine, in a tooling script and in unit tests. The broker config defaulted to the provider's **live** API host, and the dashboard bound to all network interfaces and logged the machine's private LAN address on startup.

**Why it hurts.** A copy made "for development" was one config read away from talking to a real account, reachable from the local network, and committing real identifiers into git history.

**Rules that prevent it.**
- **DRY_RUN by default**, and all network defaults are local and demo/sandbox. No live host or LAN-facing bind may be a default (`00_TEAM_CHARTER.md`, `05_MONEY_GUARD.md`).
- Real account IDs never live in code, config or tests. Tests use synthetic IDs, and the CI forbidden-pattern grep includes the real ones.
- Secrets and identifiers found by an agent are reported by path and type only.

## 3. Docs that drifted from code
**What happened.** On an agent-written codebase, the docs slowly stopped matching reality. The README listed exported files that the code no longer produced. Comments described behaviour that had been changed. The support channel in the docs was out of date, and a payment address was hardcoded in the source while the docs claimed it came from config.

**Why it hurts.** Agents read docs and comments as context. Lying docs make every later agent session start from false premises, so the drift compounds. A hardcoded payment detail is also a money risk and an operational one.

**Rules that prevent it.**
- **Code is truth** about behaviour, and instructions are truth about intent. Every claim needs `file:line` evidence (`00_TEAM_CHARTER.md`).
- The **Librarian** role (`02_LIBRARIAN.md`) may change only docs and comments. It runs `DIFF_WATCH` on new commits and flags lying comments and hardcoded identifiers.
- **Comment-only edits must leave the syntax tree unchanged:** the source must compile before and after, with an identical syntax tree once comments are stripped. Otherwise the change is discarded (`02_LIBRARIAN.md` §6, AST gate).
- Docs are updated in the same commit as code, and no real identifiers (including payment details) live in code.

## 4. "It's in production" (it wasn't)
**What happened.** The project's fact sheet said a redesigned interface was running on the production server. The public site was still serving the old form. A separate problem made it worse: edits and docs were split between an agent's scratch working folder and the main repository, so there were two versions of the truth.

**Why it hurts.** Every agent and every human downstream plans against the doc. "Merged locally" and "deployed" got treated as the same state.

**Rules that prevent it.**
- One authoritative repository. Agents work there, not in side copies.
- Docs may say "live" only after an actual release a human ordered. Local code is local truth; production is not updated until someone says so.
- The Librarian checks status claims against evidence, the same way it checks behaviour claims.

## 5. The public promise the code didn't keep
**What happened.** Public messaging said the protocol fee was capped at zero. The code had a fee ceiling of 10% and a dead helper that could compute a platform fee. The fee actually charged was zero, but the code contradicted the public claim, and an audit rated it high severity.

**Why it hurts.** Users and auditors read the code. A gap between what you say and what the code allows is a trust problem even when nobody was charged.

**Rules that prevent it.**
- Every public claim is backed by code and by a test that fails if the claim stops being true (here: the ceiling hardcoded to zero, any other value raises, and a test proves no transaction builder emits a fee transfer).
- Dead code that touches money is deleted, not left "just in case".
- The Reviewer checks marketing/docs claims against code before SHIP (`04_REVIEWER.md`).

## 6. Green CI by widening the scope
**What happened.** CI broke: a test dependency was missing, and tests failed because a price table only covered one time window. An agent "fixed" it by restoring the price table for every window, which made the tests green. The project's single source of truth said that product was not live yet and had exactly one allowed window. The fix left an unfinished product publicly reachable and accepting orders it was never supposed to take.

**Why it hurts.** The goal became "make the tests pass", and the agent changed product scope to get there. The next audit caught it, not the review.

**Rules that prevent it.**
- Failing tests are never bypassed, and a fix can't change business scope. If the spec and the test disagree, that's an escalation, not a code change (`06_ESCALATION_ADR.md`).
- Unreleased features sit behind a flag that defaults to off, and a deploy smoke test checks the feature is still unreachable.
- The Reviewer reads the diff against the spec, not just the CI status (`04_REVIEWER.md`).

## 7. Showing success before the system confirmed it
**What happened.** A web client showed "done" right after the user's wallet signed a transaction, before the network confirmed it. The confirm call to the server ran immediately and its errors were silently swallowed. The server answered "too early" with an error instead of a "pending" status, accepted an unstable "processed" state as final, didn't check who paid the fee or which instructions the transaction contained, and took financial numbers from the client request.

**Why it hurts.** If the transaction failed or was dropped, the user saw a fake success. Stats and the ledger could be poisoned with transactions or numbers that weren't real.

**Rules that prevent it.**
- An operation isn't done until the external system confirms it. The UI shows "submitted, waiting for confirmation" and polls with backoff; the server returns "pending" instead of an error.
- Only final confirmation states count.
- The server derives amounts from the external system, never from the client. Every instruction must be on an allowlist, and inputs are range-checked.
- Money values are integers. An unknown price is stored as unknown, not as zero.

## 8. The half-applied fix
**What happened.** An invoice had a 15-minute lifetime plus a 5-minute grace period. A fix added the grace period to payment confirmation and invoice creation but missed the lookup and status methods. Those marked invoices as expired at 15 minutes, so a payment arriving inside the grace window was rejected and ended up as an orphaned deposit. Expired invoices also never released their slots, so the allocator eventually reported it was full.

**Why it hurts.** The previous fix was declared done. The same rule lived in several places and only some of them changed.

**Rules that prevent it.**
- One function owns each rule (here: "is this invoice still in grace?"), and every caller uses it.
- A fix comes with a test that reproduces the original failure end to end, not just the line that changed (`01_IDE_CODER.md`, "Before you change code": test-first).
- The Reviewer greps for every other place the old logic lives.
- Tests run on their own temporary databases, never on the local working one (`01_IDE_CODER.md`: tests never touch live state).

## 9. State that lived only in memory
**What happened.** Active invoices were held only in the process's memory. A restart or deploy wiped them, so a user's payment couldn't be matched to its order, and the frontend's status polling failed silently, leaving the user stuck on the payment screen.

**Why it hurts.** Deploys and restarts are routine. Anything involving money that doesn't survive a restart will eventually lose someone's payment.

**Rules that prevent it.**
- Money-related state is persisted before anyone is asked to pay.
- There is a recovery path that verifies a payment directly against the external system, independent of session or memory (`05_MONEY_GUARD.md` hard rule 3: reconcile after every reconnect or restart).
- The UI never fails silently; it tells the user what's happening and how to recover.

## 10. The paid export that could be truncated
**What happened.** Found in code review before launch, with the feature still disabled. The pre-payment check counted transactions from a single page of 100 results, for one address only, so it could never detect that a request exceeded the export cap. Above that count it warned that the export "will be capped" and let checkout proceed. A customer could pay and receive incomplete data. The engine also still accepted time windows the product no longer offered, and the example env file documented the old limits.

**Why it hurts.** Selling an incomplete result as complete is a refund dispute and a trust problem, and the check that should have stopped it was structurally unable to.

**Rules that prevent it.**
- The decision went to the human and was written into the spec: over the cap, checkout is blocked before payment, output is never truncated, and an upstream error never counts as "zero".
- Limits are enforced in the engine and config too, not only in the API.
- A go-live gate in the spec keeps the feature off until destructive tests for those cases pass.

## 11. Two configs, one of them stale
**What happened.** The repository held two copies of the web server config. The newer one at the root had a rule marking a warning image as private and uncacheable. An old copy in a product subfolder still had a generic 30-day cache rule, and the deploy script copied the subfolder version first. Production was running the old file, so the CDN cached the image publicly for 30 days.

**Why it hurts.** Everyone edited the config they could see. The deploy used the one nobody looked at.

**Rules that prevent it.**
- One source of truth per config. Duplicates are archived, not kept "in sync" by hand.
- The Cartographer inventory flags duplicated config and deploy fallbacks (`07_CLEANUP_CARTOGRAPHER.md`).
- After a deploy, verify the actual response from the server, not the file in the repo.

## 12. The deploy that forgot a folder
**What happened.** A new shared module was added during hardening, but the deploy pipeline didn't package or copy it to the server. The service crashed on startup with a missing-module error. The pipeline's automatic rollback caught it and restored the previous release, so production stayed up on the old version.

**Why it hurts.** Tests passed locally because the module was on disk. Only the deployed artifact was incomplete. It was the rollback, not luck, that made this a non-event.

**Rules that prevent it.**
- Deploys are reversible: keep the previous release and roll back automatically when a health check fails.
- When you add a top-level module, check the packaging/deploy step in the same change.
- Runtime data and logs live outside the code directory, so the running service can't block the next deploy. (A related incident: the service wrote temp files into the working tree and broke a `git pull` deploy.)

## 13. "Hashed" isn't anonymous
**What happened.** Two privacy promises didn't hold. A rate limiter stored visitor IPs as plain unsalted SHA-256, which can be reversed by brute force because the IPv4 space is small. Rows from one-time visitors were never cleaned up, and raw IPs were also kept as in-memory keys. Separately, a ledger stored wallet addresses as unsalted hashes, and server alerts went through a third-party push service while the public messaging said "zero trackers".

**Why it hurts.** The public notice promised masked metadata and data minimisation. An unsalted hash of a small or public identifier is a lookup table away from the original.

**Rules that prevent it.**
- Identifiers are hashed with a keyed HMAC, with a defined retention period and cleanup.
- Alerts to external services carry only aggregates, and a test rejects messages containing identifiers.
- Privacy claims in docs and marketing get the same evidence check as behaviour claims (`02_LIBRARIAN.md`, `04_REVIEWER.md`).

## 14. The agent that freelanced
**What happened.** Raw ideas from a chat with an outside assistant were pasted straight into the code, with no review and no sign-off. In one pass this shipped an unstyled white input box on a dark UI, a download flow where the browser's prefetch used up the one-time download token so a paying customer got nothing, an unhandled error path that returned a 500, a price on the website that didn't match the price in the product, untranslated text on an English-only site, a marketing term the project had explicitly banned, and an unapproved change to the logo.

**Why it hurts.** None of these was hard to catch. They got through because nothing stood between "an idea" and "the main branch".

**Rules that prevent it.**
- Every agent works in a defined role with a defined scope, and changes go through review before merge (`03_ORCHESTRATOR_PM.md`, `04_REVIEWER.md`).
- Root `AGENTS.md` rules, so every tool that opens the repo reads them first.
- Nothing irreversible without a human yes. Brand, pricing and public wording are business decisions that get escalated (`06_ESCALATION_ADR.md`).

## 15. Lessons from trading infrastructure
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
