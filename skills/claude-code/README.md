# Repo Architecture Walkthrough Claude Skill

This Claude Code skill creates two repository architecture docs:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

It is designed for:

- new developer onboarding
- manager/business understanding
- safe AI-agent navigation

## Files

- `SKILL.md` — main Claude skill instructions
- `ARCHITECTURE_TEMPLATE.md` — required structure for the walkthrough
- `ARCHITECTURE_DIAGRAMS_TEMPLATE.md` — Mermaid diagram guidance and examples
- `LANGUAGE.md` — wording, confidence labels, and recommendation style
- `verify_architecture_docs.py` — Python 3.10.2 standard-library verifier

## Suggested install

Copy the `repo-architecture-walkthrough` folder into your Claude Code skills directory, commonly:

```bash
.claude/skills/repo-architecture-walkthrough/
```

Then ask Claude Code something like:

```text
Use the repo-architecture-walkthrough skill to create ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md for this repository.
```

## Verification

After Claude writes the docs, run from the repository root:

```bash
python verify_architecture_docs.py
```

The verifier uses only the Python standard library.
