# AI Repository Architecture Walkthrough Skills

Create clear, human-reviewable architecture documentation for code repositories edited by AI coding agents.

This repository contains architecture walkthrough skills for:

- Claude Code
- OpenAI Codex

The skills help AI coding tools inspect a repository, ask light clarification questions, and generate:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

These files are designed to help developers, managers, reviewers, and future AI agents understand how a codebase works before changing it.

---

## Who Is This For?

### Developers

This is for developers who are using Claude Code, Codex, or other AI coding agents to write or modify software.

AI agents can generate code quickly, but fast code is not always correct code. The risk is that the code starts to work like a black box: it passes a few tests, looks polished, but nobody fully understands the design assumptions, hidden dependencies, data flow, or failure modes.

This skill helps developers:

- Understand the design before making changes
- Find the main entry points and core workflows
- Identify safe areas to edit
- Avoid touching protected or risky areas without approval
- See how modules, packages, services, and data flows fit together
- Give AI agents better context before asking them to code
- Reduce review friction by documenting the architecture clearly

A good architecture file is not bureaucracy. It is a map that helps humans and AI agents make smaller, safer, better changes.

---

### Engineering Managers

This is for managers who want the productivity benefits of AI coding without losing control of software quality.

AI-assisted development increases output, but it can also increase review burden. Human reviewers still need to understand whether the generated code matches the business need, fits the architecture, has the right tests, and avoids risky assumptions.

This skill helps managers:

- Reduce bottlenecks in code review
- Make architecture knowledge visible instead of tribal
- Improve onboarding for new developers
- Preserve human accountability for design decisions
- Create a standard artifact reviewers can rely on
- Make AI-assisted code easier to audit, maintain, and support
- Ensure code is tied back to business requirements, tests, and operational risk

The goal is not to let AI replace review. The goal is to give human reviewers a better starting point.

---

### AI Coding Agents

This is also for AI agents.

AI agents work better when they have durable, high-signal context. Without an architecture walkthrough, an agent may infer the wrong pattern from nearby files, copy outdated designs, edit too broadly, or miss important business rules.

A detailed `ARCHITECTURE.md` helps agents:

- Locate the right files faster
- Respect module boundaries
- Avoid protected areas
- Understand dependency direction
- Use the correct configuration and integration patterns
- Add tests in the right places
- Preserve known design constraints
- Avoid speculative abstractions and broad rewrites

The architecture document becomes part of the repository’s context engineering layer.

---

## Why This Matters

AI coding agents are powerful, but they are not automatically aware of the real design intent behind a codebase.

They may miss:

- Why a particular data model exists
- Which key or identifier is semantically correct
- Which layer owns a business rule
- Which dependency direction is intentional
- Which legacy behavior must not change
- Which files are generated
- Which configurations are production-sensitive
- Which tests are required before a change is safe

When those details are not documented, AI-generated code can look correct while being fundamentally wrong.

These skills are meant to prevent that by making architecture explicit, reviewable, and reusable.

---

## What These Skills Create

The skills generate two primary files.

### `ARCHITECTURE.md`

A written architecture walkthrough of the repository.

Typical sections include:

- Executive summary
- Purpose and scope
- Audience guide
- System context
- Main entry points
- Major components
- Core workflows
- Data flow and persistence
- Runtime, configuration, and deployment model
- Testing and verification strategy
- Safe-to-edit and do-not-edit-without-approval areas
- Known risks and sharp edges
- Assumptions and items needing human validation
- Suggested architecture improvements
- Glossary
- Evidence map

### `ARCHITECTURE_DIAGRAMS.md`

A diagram-focused companion file.

It may include Mermaid diagrams such as:

- System context diagram
- Component/module diagram
- Request or job workflow diagram
- Data flow diagram
- Deployment/runtime diagram

The skill uses judgment. For a tiny single-file script, diagrams may be unnecessary. For a larger repository, diagrams can make the architecture much easier to understand.

---

## Why Architecture Files Help AI Coding

A detailed architecture file gives AI agents durable context before they modify code.

Without one, the agent has to rediscover the system every time. That increases the chance of:

- Wrong assumptions
- Overbroad edits
- Duplicated patterns
- New dependencies that do not fit
- Changes in the wrong layer
- Tests that verify implementation details instead of behavior
- Refactors that look clean but break design intent

With one, the agent can start from a shared map of the system.

That means better prompts, better plans, better diffs, and easier human review.

---

## Use Cases

### 1. Onboarding a New Developer

Use the skill to create an architecture walkthrough before a new developer starts working in the repo.

The generated files help them answer:

- What does this repo do?
- Where should I start reading?
- What are the main entry points?
- What workflows matter most?
- What areas are risky to change?

---

### 2. Preparing a Repository for AI Coding

Before asking Claude Code or Codex to make changes, run the architecture walkthrough skill.

This gives the agent a stable context file it can use during future tasks.

---

### 3. Reducing Code Review Friction

Attach or reference `ARCHITECTURE.md` during code review so reviewers can understand the intended design before inspecting the diff.

This is especially useful when a change touches multiple packages, services, jobs, or integration points.

---

### 4. Reviewing AI-Generated Code

Use the architecture files to check whether AI-generated code respects:

- Existing boundaries
- Dependency direction
- Data flow
- Configuration patterns
- Test strategy
- Safe edit areas
- Protected areas

---

### 5. Modernizing a Legacy Repository

For legacy systems, the skill can create a first-pass architecture map without requiring a large refactor.

This helps teams improve understanding before changing structure.

---

### 6. Creating a Design Baseline Before a Major Feature

Before adding a major feature, generate or update the architecture walkthrough.

This helps identify where the feature should live and which tests should be added.

---

### 7. Capturing Tribal Knowledge

The skill asks a light set of human clarification questions.

This helps capture knowledge that may not exist in code, such as:

- Why a module exists
- Which integrations are fragile
- Which areas require approval
- Which workflows are business-critical
- Which assumptions are uncertain

---

### 8. Architecture Review Readiness

Use the generated files as inputs to a formal architecture review checklist.

They provide evidence for sections like:

- Purpose and scope
- Entry points
- Module boundaries
- External integrations
- Data flow
- Configuration and secrets
- Testing strategy
- Deployment/runtime model
- Known risks
- Safe edit boundaries

---

## Repository Contents

Example structure:

```text
.
├── claude-code-repo-architecture-walkthrough/
│   ├── SKILL.md
│   ├── ARCHITECTURE_TEMPLATE.md
│   ├── ARCHITECTURE_DIAGRAMS_TEMPLATE.md
│   ├── LANGUAGE.md
│   ├── verify_architecture_docs.py
│   └── README.md
│
├── codex-repo-architecture-walkthrough/
│   ├── SKILL.md
│   ├── ARCHITECTURE_TEMPLATE.md
│   ├── ARCHITECTURE_DIAGRAMS_TEMPLATE.md
│   ├── LANGUAGE.md
│   ├── verify_architecture_docs.py
│   ├── AGENTS_SNIPPET.md
│   └── README.md
│
└── README.md
```

Folder names may differ depending on how you organize the repo.

---

## Quick Start: Claude Code

### Install Globally on macOS

```bash
mkdir -p ~/.claude/skills

cd ~/Downloads
unzip repo-architecture-walkthrough-skill.zip

cp -R repo-architecture-walkthrough-skill ~/.claude/skills/
```

Verify:

```bash
ls ~/.claude/skills/repo-architecture-walkthrough-skill
```

You should see:

```text
SKILL.md
ARCHITECTURE_TEMPLATE.md
ARCHITECTURE_DIAGRAMS_TEMPLATE.md
LANGUAGE.md
verify_architecture_docs.py
README.md
```

Restart Claude Code if it is already running.

Then, inside a repository, ask Claude Code:

```text
Use the repo architecture walkthrough skill to analyze this repository and create ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md.
```

---

## Quick Start: Codex

### Install Globally on macOS

```bash
mkdir -p ~/.agents/skills

cd ~/Downloads
unzip codex-repo-architecture-walkthrough-skill.zip

cp -R codex-repo-architecture-walkthrough ~/.agents/skills/
```

### Install Into a Specific Repository

From the target repository:

```bash
mkdir -p .agents/skills

cp -R ~/Downloads/codex-repo-architecture-walkthrough .agents/skills/
```

Then ask Codex:

```text
Use the repo architecture walkthrough skill to analyze this repository and create ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md.
```

Optionally copy the included `AGENTS_SNIPPET.md` content into your repo’s `AGENTS.md` so Codex knows to use the skill for architecture documentation tasks.

---

## Recommended Workflow

### 1. Start with a clean working tree

```bash
git status
```

This makes it easier to review only the generated documentation changes.

### 2. Run the skill

Ask Claude Code or Codex to create the architecture walkthrough.

### 3. Answer clarification questions

The skill should first ask whether you already know the codebase.

If you do not know the codebase, it should proceed with a beginner-friendly walkthrough.

If you do know the codebase, it may ask a few targeted questions about:

- Important workflows
- Risky areas
- Business rules
- Protected files
- Deployment details
- Known architectural concerns

### 4. Review the generated files

Review:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

Pay special attention to:

- Assumptions
- Protected areas
- Suggested improvements
- Evidence map
- Mermaid diagrams
- Testing gaps
- Known risks and sharp edges

### 5. Run the verifier

The skills include a Python standard-library verification script.

```bash
python3 verify_architecture_docs.py
```

The verifier checks for expected architecture sections and basic documentation quality signals.

### 6. Commit the docs

```bash
git add ARCHITECTURE.md ARCHITECTURE_DIAGRAMS.md
git commit -m "Add repository architecture walkthrough"
```

---

## How This Fits with Human Code Review

These skills do not replace human code review.

They help humans review better.

A human reviewer should still verify:

- The architecture description matches the code
- The diagrams are accurate
- Assumptions are clearly marked
- Suggested improvements are reasonable
- Protected areas are correct
- Tests match the intended behavior
- Security, data, and operational risks are addressed
- AI-generated changes respect the documented architecture

The skill creates a map. The human reviewer still owns the judgment.

---

## Suggested Prompt

Use this when running the skill:

```text
Use the repository architecture walkthrough skill.

Analyze this repository and create:
1. ARCHITECTURE.md
2. ARCHITECTURE_DIAGRAMS.md

First ask whether I already know this codebase.

If I do not know it, create a beginner-friendly walkthrough.

If I do know it, ask only a few targeted clarification questions about the areas I care about, risky areas, protected areas, business rules, or unclear design assumptions.

Use Mermaid diagrams when they add clarity, but skip diagrams for very small repositories where they would add noise.

Clearly mark assumptions and items needing human validation.

Include suggested architecture improvements near the end of ARCHITECTURE.md, with rationale from both:
1. a senior developer perspective
2. an engineering manager perspective
```

---

## Good Architecture Documentation Principles

The generated architecture docs should be:

- Clear enough for a new developer
- Useful to a senior reviewer
- Helpful to an AI coding agent
- Grounded in actual files
- Explicit about uncertainty
- Focused on design, not a file-by-file inventory
- Updated when important architecture changes
- Honest about risks, gaps, and sharp edges

---

## What This Is Not

This is not:

- A replacement for human review
- A full security audit
- A full production readiness review
- A guarantee that the code is correct
- A substitute for tests
- A reason to trust AI-generated code blindly

It is a practical tool for making architecture easier to understand before humans and AI agents change the system.

---

## License
- Apache-2.0 for explicit patent language
---

## Contributing

Contributions are welcome.

Useful improvements include:

- Better architecture templates
- Better verification checks
- More language-specific guidance
- Better examples for Python, Go, JavaScript, Vue, Django, and SQL repositories
- Better Mermaid diagram patterns
- More guidance for legacy systems
- More guidance for regulated environments

