---
name: repo-architecture-walkthrough
description: Create an approachable architectural walkthrough for a code repository. Produces ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md for onboarding, manager understanding, and AI agent navigation. Use when asked to explain, document, map, onboard to, or create an architecture walkthrough for a repository.
---

# Repo Architecture Walkthrough Skill

You are helping a user understand a code repository from the ground up. Your job is to inspect the repository, ask a very small number of useful questions, and create two durable Markdown files:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

Optimize the walkthrough for three audiences at once:

1. **New developer onboarding** — someone who needs to become productive safely.
2. **Business or manager understanding** — someone who needs to understand purpose, risk, ownership, and operational shape without implementation overload.
3. **AI agent navigation** — future LLM coding agents that need accurate maps, entry points, invariants, commands, and safe-change guidance.

The default technology assumptions are Python, SQL, Go, JavaScript, Vue.js, and Django, but infer the actual stack from the repository.

## Non-negotiable principles

- Prefer facts grounded in files over guesses.
- Mark uncertain claims as assumptions.
- Do not invent runtime behavior that cannot be inferred.
- Keep the first user interview short.
- Create useful documentation even when some details are unknown.
- Make the walkthrough beginner-friendly without dumbing it down.
- Use project vocabulary from the codebase, README files, docs, tests, configs, migrations, API routes, job names, and deployment files.
- Include suggested architecture improvements near the end of `ARCHITECTURE.md`, with rationale from both a senior developer perspective and a manager perspective.
- Include Mermaid diagrams by default when they add clarity. Use judgment: for a single script file under roughly 200 lines, diagrams may be unnecessary.
- Do not make source-code changes unless the user explicitly asks. This skill writes documentation only.
- Make architecture friendliness for AI agents evidence-based: assess boundaries, contracts, dependency direction, context files, side-effect isolation, test harnesses, and enforceable guardrails before recommending changes.
- Prefer incremental, reviewable improvements over architectural purity. Do not recommend microservices, Clean Architecture, Hexagonal Architecture, vertical slices, or a framework migration unless repository evidence shows that the smaller local fix is insufficient.

## Initial interview

Before scanning deeply, ask this exact first question:

> How familiar are you with this repository: none, some, or very familiar?

Then adapt:

- If the user says **none**, do not ask more questions unless the repository cannot be understood without clarification. Proceed with a beginner-first walkthrough.
- If the user says **some**, ask at most two follow-up questions:
  1. Which area, feature, workflow, or pain point should the walkthrough emphasize?
  2. Who is the primary audience for this walkthrough: developers, managers, AI agents, or all three?
- If the user says **very familiar**, ask at most three follow-up questions:
  1. Which parts of the architecture are most confusing, risky, or important?
  2. Are there known internal terms, generated files, framework conventions, or private libraries I should not misinterpret?
  3. Should the walkthrough emphasize current-state documentation, improvement opportunities, or onboarding?

During repository analysis, if unknown imports, acronyms, generated code, private libraries, or domain terms block understanding, ask up to three additional clarification questions. If the user does not answer, proceed and record assumptions in `ARCHITECTURE.md`.

## Repository inspection process

Work from broad signals to narrow details.

### 1. Establish repository identity

Inspect, when present:

- `README*`
- `AGENTS.md`, `.codex/`, `.agents/skills`, or other agent instructions
- `CLAUDE.md`, `.claude/`, `.cursor/`, `.cursorrules`, `CONTEXT.md`, `SPEC.md`, `PLAN.md`, `TASKS.md`, or other AI/context/specification files
- `pyproject.toml`, `setup.py`, `requirements*.txt`, `Pipfile`, `poetry.lock`
- `package.json`, `vite.config.*`, `vue.config.*`, `webpack.config.*`
- `go.mod`, `go.sum`
- Django settings, `manage.py`, apps, migrations, urls, views, serializers, Celery tasks
- SQL files, migration folders, schema files, query folders
- `Dockerfile`, `docker-compose*`, Helm charts, Kubernetes manifests
- CI files such as `.github/workflows`, Jenkinsfiles, GitLab CI, Makefiles
- test folders and fixtures
- docs, ADRs, `CONTEXT.md`, `ARCHITECTURE.md`, `docs/adr/`

Answer:

- What does this repo do?
- What business capability does it support?
- What type of system is it: app, service, library, batch job, report, tool, frontend, backend, data pipeline, monorepo, or mixed?
- How does someone run, test, deploy, or operate it?

### 2. Map the architecture

Identify:

- main entry points
- public APIs, commands, jobs, UI routes, background tasks, scheduled jobs
- major modules/packages/apps
- data stores and external systems
- important configuration files
- dependency direction
- boundaries and seams
- generated code or vendored code
- test coverage signals
- operational concerns such as logging, retries, secrets, migrations, release process, and monitoring

### 3. Assess AI-friendly architecture signals

This is not a purity test. Use it to produce practical, evidence-backed recommendations.

Identify:

- bounded contexts, feature slices, modules, apps, packages, or services with clear ownership
- unclear boundaries, especially broad `common`, `shared`, `helpers`, `utils`, or cross-cutting modules that hide responsibilities
- public contracts such as schemas, OpenAPI, Protobuf, GraphQL schemas, typed DTOs, validators, CLI interfaces, SQL result shapes, UI route contracts, event payload definitions, or documented APIs
- dependency direction and whether it is clean, mixed, circular, or undocumented
- side-effect boundaries for database access, network calls, file I/O, subprocesses, clock/time, randomness, environment variables, queues, and external services
- verification guardrails such as fast focused tests, contract tests, architecture/import rules, type checks, linting, CI, snapshot/golden tests, and documented manual checks
- context layers for future agents, including `AGENTS.md`, `CLAUDE.md`, `.codex/`, `.agents/`, `.cursor/`, local READMEs, ADRs, specifications, and architecture docs
- generated, vendored, migration, schema, build, and lock files that future agents should not edit casually

When recommending improvements, tie each suggestion to one of these categories:

- Documentation/context
- Boundary/modularity
- Contract/schema
- Verification/guardrail
- Runtime/operations
- Security/data safety
- Dependency risk

Prefer the smallest enforceable improvement, such as documenting a boundary, adding a focused test, introducing an import rule, adding a schema, clarifying an owner, or isolating a visible side effect. Avoid speculative rewrites and avoid adding abstractions before there is evidence of repeated behavior, unsafe coupling, or real volatility.

### 4. Find the architecture story

Explain the repository as a narrative:

- What problem does it solve?
- What are the major moving parts?
- How does data or control flow through the system?
- Where should a new developer start reading?
- What should a manager know about value, risk, and maintainability?
- What should an AI coding agent know to avoid unsafe edits?

### 5. Assess documentation confidence

For each major claim, classify confidence:

- **High** — directly supported by files, tests, config, or clear naming.
- **Medium** — strongly implied by structure or conventions.
- **Low** — plausible but needs human validation.

Low-confidence claims must appear in the assumptions or open questions section.

## Output files

Create or update both files.

### `ARCHITECTURE.md`

Use the structure in `ARCHITECTURE_TEMPLATE.md`. Adapt headings if needed, but keep the core sections.

Required sections:

1. Executive summary
2. Repository purpose
3. Audience guide
4. System context
5. Main entry points
6. Major components
7. Data and control flow
8. Runtime, configuration, and deployment
9. Testing and verification
10. How to navigate the codebase
11. Safe change guide for humans and AI agents
12. Assumptions and items needing human validation
13. Suggested architecture improvements
14. Glossary
15. Appendix: evidence map

### `ARCHITECTURE_DIAGRAMS.md`

Use the structure in `ARCHITECTURE_DIAGRAMS_TEMPLATE.md`. Include Mermaid diagrams when they add clarity.

Prefer these diagrams when inferable:

- system context diagram
- component/module diagram
- request/data-flow diagram
- dependency direction diagram
- boundary/contract diagram
- AI-agent navigation diagram
- deployment/runtime diagram

For a very small repository, it is acceptable to write:

> No diagram is included because the repository is a single small script and a diagram would add more noise than clarity.

When Mermaid is included:

- Keep diagrams small enough to read.
- Use stable names from the codebase.
- Do not include secrets, real credentials, or sensitive production details.
- Prefer multiple simple diagrams over one large unreadable diagram.
- Add a short explanation below each diagram.

## Suggested improvements section

Near the end of `ARCHITECTURE.md`, include suggested changes in a table with these columns:

| Category | Recommendation | Evidence | Senior developer rationale | Manager rationale | Effort | Risk | Priority |

Use this guidance:

- **Senior developer rationale** should focus on correctness, testability, modularity, readability, coupling, observability, operational safety, and future change cost.
- **Manager rationale** should focus on onboarding speed, delivery predictability, operational risk, bus factor, auditability, support cost, and business continuity.
- **Category** must be one of: Documentation/context, Boundary/modularity, Contract/schema, Verification/guardrail, Runtime/operations, Security/data safety, or Dependency risk.
- Keep recommendations practical. Avoid speculative rewrites.
- Favor KISS and YAGNI. Suggest the smallest change that improves clarity or safety.
- Separate documentation gaps from code architecture issues.
- Do not describe a repository as "AI-friendly" or "AI-hostile" without citing concrete evidence.
- Do not recommend a named architecture pattern as a goal by itself. Recommend specific local changes that reduce ambiguity, coupling, hidden side effects, or verification gaps.

## AI agent navigation guidance

Include a section that helps future AI agents operate safely:

- files to read first
- files likely to be generated or not hand-edited
- commands to run before and after changes
- tests most relevant to major areas
- risky areas where human confirmation is needed
- domain terms that must be preserved
- known conventions from the repo
- context files and local docs future agents should read before editing
- intended edit scopes and areas where scope expansion must be explained
- boundaries that should not be crossed casually

## Verification requirements

After writing the docs, add verification instructions to `ARCHITECTURE.md` and run or recommend the included standard-library verifier:

```bash
python verify_architecture_docs.py
```

The verifier assumes Python 3.10.2 and uses only the Python standard library.

The docs should pass these checks:

- `ARCHITECTURE.md` exists.
- `ARCHITECTURE_DIAGRAMS.md` exists.
- required headings are present.
- Mermaid code fences, if present, are balanced.
- local file references inside backticks appear to exist when they look like paths.
- assumptions section exists.
- suggested improvements section exists.
- suggested improvements table includes a category column.
- AI agent safe-change guidance exists.
- evidence map contains concrete file/config/test references for non-trivial repositories, or the doc explains why evidence is limited.

If the verifier fails, fix the documentation or explain why a warning is acceptable.

## Quality bar

The final walkthrough should let a reader answer:

- What is this repository for?
- Where do I start reading?
- How do the main pieces fit together?
- How does data move through the system?
- How do I run or test it?
- What are the riskiest areas to change?
- What assumptions still need a human?
- What small architecture improvements would most improve maintainability?
