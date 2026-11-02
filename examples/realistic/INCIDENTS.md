# INCIDENTS.md

## [2026-10-01] INC-001 Half-applied grace period
- Where: src/invoice.py:42
- What happened: lookup ignored 5-min grace
- Cause: logic duplicated
- Fix: extracted is_in_grace()
- Rule for next time: one function owns each rule
