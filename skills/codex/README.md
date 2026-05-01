# Repo Architecture Walkthrough Skill for Codex

This Codex skill creates two repository architecture docs:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

It is designed for:

- new developer onboarding
- manager/business understanding
- safer AI-agent navigation
- human review of AI-assisted codebases

## Files

- `SKILL.md` — main Codex skill instructions
- `references/ARCHITECTURE_TEMPLATE.md` — required structure for the walkthrough
- `references/ARCHITECTURE_DIAGRAMS_TEMPLATE.md` — Mermaid diagram guidance and examples
- `references/LANGUAGE.md` — wording, confidence labels, and recommendation style
- `scripts/verify_architecture_docs.py` — Python 3.10.2 standard-library verifier
- `agents/openai.yaml` — optional Codex UI metadata and invocation policy
- `AGENTS_SNIPPET.md` — optional repo-level guidance you can paste into `AGENTS.md`

## Install globally on macOS

```bash
mkdir -p ~/.agents/skills
cd ~/Downloads
unzip codex-repo-architecture-walkthrough-skill.zip
cp -R codex-repo-architecture-walkthrough ~/.agents/skills/
```

Verify:

```bash
ls ~/.agents/skills/codex-repo-architecture-walkthrough
```

## Install into a specific repository

From the target repository:

```bash
mkdir -p .agents/skills
cp -R ~/Downloads/codex-repo-architecture-walkthrough .agents/skills/
```

## Use

Inside a repository, ask Codex:

```text
Use $repo-architecture-walkthrough to analyze this repository and create ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md.
```

Or describe the task naturally:

```text
Create an architecture walkthrough for this repository, including ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md.
```

## Verification

After Codex writes the docs, run from the repository root:

```bash
python ~/.agents/skills/codex-repo-architecture-walkthrough/scripts/verify_architecture_docs.py
```

If the skill is installed inside the repo, run:

```bash
python .agents/skills/codex-repo-architecture-walkthrough/scripts/verify_architecture_docs.py
```
