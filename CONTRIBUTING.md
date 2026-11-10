# Contributing

Thanks for helping make AI agents safer to work with.

## What's welcome
- New roles (open a **Role request** issue first)
- Setup notes for more tools (Windsurf, Copilot, Aider…)
- Anonymized war stories that show why a rule exists
- Clarity fixes, typos, translations

## Rules for contributions
1. **No private data:** no real account IDs, tokens, keys, absolute personal paths, IPs or company/project names. Use `{{PLACEHOLDERS}}`.
2. **No outcome promises:** no profit, return or "guaranteed safe" claims.
3. **Rules must stay tool-agnostic.** Put tool-specific notes in the README quick start.
4. **A new rule needs a reason.** Link a war story or describe the failure it prevents.
5. **Tighten, don't weaken.** Don't loosen a charter hard rule without an issue discussion first.
6. Keep each PR to one topic and add a line to `CHANGELOG.md` under "Unreleased".

## Checks
The hard rules live in `roles/00_TEAM_CHARTER.md` and `roles/06_ESCALATION_ADR.md`. IDE templates and the filled examples are generated from those files. After you edit the charter, the ADR, a coder role placeholder, or `examples/*/placeholders.json`, run:

```bash
python3 scripts/generate_templates.py
```

Before you open a PR:

```bash
pip install -r tests/requirements.txt
python3 scripts/generate_templates.py --check
python3 -m pytest -q
```

By contributing, you agree that your contribution is licensed under the MIT License.
