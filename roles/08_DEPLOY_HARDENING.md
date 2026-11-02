# AGENTS.md — Deploy Hardening (optional) for {{PROJECT_NAME}}

> Optional checklist derived from war stories 9, 11, 12 and 13. Use before any production deploy or when money/state is involved.
> Mark as optional in your setup if the project has no deploys or external state.

## Checklist (before proposing live or merge that touches deploy)

- [ ] Money-related or order state is persisted before any payment is requested from the user (no in-memory only).
- [ ] Single source of truth for every config file. No duplicate copies that deploy might pick up first.
- [ ] Packaging / deploy step includes every new top-level module or shared dependency.
- [ ] Identifiers (IPs, addresses, account IDs) are stored as keyed HMAC with a defined retention period and cleanup job. No unsalted hashes of small spaces.
- [ ] Deploy is reversible: previous release is kept and automatic rollback runs on failed health check.
- [ ] After deploy, verify the live response (not just the file in the repo).

## Report
Use the standard report format. List any item that is not yet true as NOT DONE / SKIPPED with reason.
