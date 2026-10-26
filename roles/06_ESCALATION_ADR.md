# ESCALATION_ADR.md — How agents decide and escalate in {{PROJECT_NAME}}

## The rule in one line
Technical ambiguity → **decide with {{ORCHESTRATOR_ROLE}} and write an ADR**. Business, money, legal, irreversible → **ask {{OWNER_NAME}}**, one sentence, recommendation, yes/no.

## What always goes to the human
- Enabling live mode / production / mainnet
- `git push`, merge to `{{MAIN_BRANCH}}`, publishing, releases
- Spending or moving money; pricing; licence; legal text
- Deleting anything outside `_archive/`
- Loosening any limit, coverage gate or hard rule

## How to ask the human
```
[DECISION NEEDED] <one sentence: what and why now>
Recommendation: <option> because <reason>.
Yes/No?
```
Max 3 per report. Until answered: the item stays BLOCKED; work continues on everything else.

## ADR template (`docs/adr/NNNN-<slug>.md`, MADR-style)
```
# NNNN. <Title>
- Status: proposed | accepted | superseded by NNNN
- Date: YYYY-MM-DD
- Deciders: <roles / owner>
## Context
<problem, evidence file:line>
## Options
1. <option> — pros / cons
2. <option> — pros / cons
## Decision
<chosen option and why>
## Consequences
<what changes, what tests/docs updated, migration>
```
An ADR is required for: breaking interface changes, lowering a coverage gate, adding a dependency/integration outside agreed scope, docs-vs-code conflicts in critical zones, any deviation from the plan.

## Open questions file
`docs/OPEN_QUESTIONS.md` — when unsure, don't do it; write the question there with date, asker, context, options.
