---
name: repo-architecture-walkthrough
description: Generate relationship-validated repository architecture documentation for AI-assisted development. Use when asked to analyze, explain, document, map, onboard to, recover, or create ARCHITECTURE.md / ARCHITECTURE_DIAGRAMS.md for a codebase. Produces a human-reviewable architecture walkthrough for developers, managers, and future AI coding agents.
---

# Repo Architecture Walkthrough Skill for Claude Code

You are helping the user understand a code repository from the ground up. Inspect the repository, ask a very small number of useful questions, recover the architecture from repository evidence, validate relationships before diagramming, and create two durable Markdown files:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

Optimize the walkthrough for three audiences at once:

1. **New developer onboarding** — someone who needs to become productive safely.
2. **Business or manager understanding** — someone who needs purpose, risk, ownership, and operational shape without implementation overload.
3. **AI coding agent navigation** — future Claude Code/LLM coding agents that need accurate maps, entry points, invariants, commands, assumptions, dependency edges, and safe-change guidance.

The default technology assumptions are Python, SQL, Go, JavaScript, Vue.js, and Django, but infer the actual stack from repository evidence.

## What is improved in this version

This version adds a more rigorous architecture-recovery workflow:

- explicit evidence gathering before synthesis;
- adaptive grouping for large, legacy, generated-heavy, or monorepo codebases;
- dependency-aware relationship extraction before diagrams;
- a claim-and-edge validation pass before writing final docs;
- C4-style diagram layering where useful;
- mismatch detection between code, docs, diagrams, configuration, tests, and deployment files;
- stronger guidance for documenting relationships, not just components.

Use these additions to reduce unsupported edges, orphan components, fragmented diagrams, and plausible-but-ungrounded architecture narratives.

## Claude Code-specific behavior

- This skill writes documentation only unless the user explicitly asks for source-code changes.
- Treat the repository as the source of truth. Prefer file evidence over guesses.
- Use Claude Code tools to inspect files, search text, read configuration, examine tests, and trace dependencies before writing conclusions.
- Use read-only discovery commands where useful. Do not run destructive commands.
- Do not claim that commands passed unless you actually ran them and observed the result.
- If the working tree already has user changes, avoid overwriting unrelated files. Preserve user edits.
- Keep generated documentation easy to diff and review in Git.
- When useful, mention this skill explicitly in your plan as `$repo-architecture-walkthrough` so the user knows which workflow is being applied.
- Use a phase-grounded recovery workflow: discover evidence, map candidate nodes and edges, validate relationships, write the docs, then verify the docs.
- Keep any intermediate architecture graph, checklist, relationship ledger, or recovery notes in your working context unless the user asks for additional files. The durable repository output remains `ARCHITECTURE.md` and `ARCHITECTURE_DIAGRAMS.md`.

## Non-negotiable principles

- Prefer facts grounded in files over guesses.
- Mark uncertain claims as assumptions.
- Do not invent runtime behavior that cannot be inferred.
- Treat relationships between components as higher-risk claims than component names. Every meaningful edge in a diagram should have evidence or be explicitly marked as inferred.
- Do not connect components only because they are near each other in the tree or sound related.
- Keep the first user interview short.
- Create useful documentation even when some details are unknown.
- Make the walkthrough beginner-friendly without dumbing it down.
- Use project vocabulary from the codebase, README files, docs, tests, configs, migrations, API routes, job names, deployment files, schemas, and generated artifacts.
- Include suggested architecture improvements near the end of `ARCHITECTURE.md`, with rationale from both a senior developer perspective and a manager perspective.
- Include Mermaid diagrams by default when they add clarity. Use judgment: for a single script file under roughly 200 lines, diagrams may be unnecessary.
- Prefer multiple small, relationship-validated diagrams over one large, impressive, weakly grounded diagram.
- Do not replace human architectural judgment. Use the architecture docs to make human review easier.
- Make architecture friendliness for AI agents evidence-based: assess boundaries, contracts, dependency direction, context files, side-effect isolation, test harnesses, and enforceable guardrails before recommending changes.
- Prefer incremental, reviewable improvements over architectural purity. Do not recommend microservices, Clean Architecture, Hexagonal Architecture, vertical slices, or a framework migration unless repository evidence shows that the smaller local fix is insufficient.
- If collaboration-style review is useful, simulate role-specific review passes rather than creating artificial complexity: developer, domain/business, operations/security, and AI-agent safety.

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

During repository analysis, if unknown imports, acronyms, generated code, private libraries, domain terms, or cross-repository dependencies block understanding, ask up to three additional clarification questions. If the user does not answer, proceed and record assumptions in `ARCHITECTURE.md`.

## Architecture recovery workflow

Use this workflow before writing the final files. It is designed to reduce context blindness, missing business semantics, and weak relationship diagrams.

### Phase 0. Scope and safety check

Before deep inspection:

- Check the working tree status if the repository is under Git.
- Identify whether existing architecture docs already exist.
- Identify repository size and likely complexity.
- Decide whether to inspect all files or use adaptive grouping.
- Note generated, vendored, archived, build, migration, lock, cache, or dependency folders that should not be overinterpreted.
- Identify the intended output location. Default to the repository root unless the user specifies another location.

Useful read-only commands, when available:

```bash
git status --short
git ls-files | sed -n '1,200p'
find . -maxdepth 3 -type f | sed -n '1,200p'
rg -n "TODO|FIXME|deprecated|generated|do not edit|architecture|ADR|contract|schema|OpenAPI|protobuf|GraphQL" .
```

Do not run destructive commands. Avoid expensive full-repository commands on very large repositories unless scoped.

### Phase 1. Establish repository identity

Inspect broad signals first. Record the strongest evidence sources for later use in the evidence map.

Inspect, when present:

- `README*`
- `AGENTS.md`, `.codex/`, `.agents/skills`, or other agent instructions
- `CLAUDE.md`, `.claude/`, `.cursor/`, `.cursorrules`, `CONTEXT.md`, `SPEC.md`, `PLAN.md`, `TASKS.md`, or other AI/context/specification files
- `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, `Pipfile`, `poetry.lock`, `uv.lock`, `tox.ini`, `noxfile.py`
- `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `vite.config.*`, `vue.config.*`, `webpack.config.*`, `tsconfig*.json`
- `go.mod`, `go.sum`
- language-specific manifests, build files, dependency locks, and workspace files
- Django settings, `manage.py`, apps, migrations, urls, views, serializers, Celery tasks
- SQL files, migration folders, schema files, query folders, ORM models, seed data, fixtures
- OpenAPI, AsyncAPI, Protobuf, GraphQL, JSON Schema, Avro, Thrift, or other contract files
- `Dockerfile`, `docker-compose*`, Helm charts, Kubernetes manifests, Terraform, Pulumi, CloudFormation, deployment scripts
- CI files such as `.github/workflows`, Jenkinsfiles, GitLab CI, Buildkite, Makefiles
- test folders, fixtures, factories, mocks, golden files, snapshots, contract tests
- docs, ADRs, runbooks, architecture diagrams, `CONTEXT.md`, existing `ARCHITECTURE.md`, `docs/adr/`
- generated, vendored, migration, schema, build, and lock files that future agents should not edit casually

Answer:

- What does this repo do?
- What business capability does it support?
- What type of system is it: app, service, library, batch job, report, tool, frontend, backend, data pipeline, monorepo, or mixed?
- How does someone run, test, deploy, or operate it?
- What vocabulary does the repository use for its domain, modules, jobs, APIs, and data?
- Which files are the strongest source of truth?
- Which parts are likely generated, vendored, or externally owned?

### Phase 2. Build an evidence inventory

Before writing final prose, build an internal inventory with these columns:

| Evidence type | Files or commands | What it supports | Confidence |
| --- | --- | --- | --- |
| Entry point | path / command | API, UI, CLI, job, worker, test, deployment | High/Medium/Low |
| Component | path / package / app | responsibility and ownership | High/Medium/Low |
| Contract | schema / route / DTO / serializer / query | public boundary | High/Medium/Low |
| Data | table / model / migration / queue / topic / file | persistence or data flow | High/Medium/Low |
| Runtime | config / container / CI / deploy file | execution and operations | High/Medium/Low |
| Verification | tests / lint / type checks / CI | guardrails | High/Medium/Low |

Use this inventory to populate the evidence map in `ARCHITECTURE.md`. If evidence is missing, say so.

### Phase 3. Use adaptive grouping for large repositories

If the repository is small, inspect source files directly. If it is large, do not flatten everything into one context window. Group first, then inspect representative and high-signal files.

Suggested grouping rules:

- **Small repo:** roughly 30 source files or fewer. Inspect all meaningful source/config/test files.
- **Medium repo:** roughly 31-300 source files. Group by package, service, app, feature, framework convention, or bounded context.
- **Large repo or monorepo:** more than roughly 300 source files. Group by deployable unit, package manager workspace, service boundary, app, top-level domain folder, or build target.
- **Legacy repo with weak boundaries:** group by entry points, database access, external integrations, data models, job queues, and high fan-in/fan-out modules.
- **Generated-heavy repo:** separate generated code, schemas, migrations, lockfiles, and build output from hand-authored architecture.

For each group, record internally:

| Group | Likely responsibility | Key files | Inbound dependencies | Outbound dependencies | Public contracts | Side effects | Tests | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use grouping to avoid context blindness. Do not let one familiar framework convention override contrary repository evidence.

### Phase 4. Extract relationships before drawing diagrams

Architecture is mostly relationships. Before final diagrams, build an internal relationship ledger. Every important diagram edge should be backed by this ledger.

Relationship ledger columns:

| Source | Target | Relationship type | Evidence | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |

Relationship types to look for:

- import/package dependency;
- API route to handler/controller/view;
- handler/controller to service/domain module;
- service/module to repository/database/query layer;
- producer to queue/topic/event;
- consumer/worker/job to queue/topic/event;
- UI route/component to API/client/store;
- CLI command to implementation module;
- scheduled job to task/function;
- schema/model/migration to data store;
- deployment/runtime config to service/process;
- test/fixture/snapshot to behavior or contract;
- generated source to generator/schema;
- internal system to external service;
- repository/package/workspace dependency to another repository, package, service, or build target.

Evidence can include imports, routing tables, dependency manifests, framework conventions, schema references, tests, config values, explicit docs, build files, or observed command output.

Use **no edge without evidence**:

- If an edge is directly supported, include it with High confidence.
- If an edge is strongly implied by framework convention or repeated naming, include it with Medium confidence and explain the convention.
- If an edge is plausible but unsupported, do not draw it as fact. Put it in assumptions or open questions.

### Phase 5. Map the architecture

Identify:

- main entry points;
- public APIs, commands, jobs, UI routes, background tasks, scheduled jobs;
- major modules/packages/apps;
- data stores and external systems;
- important configuration files;
- dependency direction;
- boundaries and seams;
- generated code or vendored code;
- test coverage signals;
- operational concerns such as logging, retries, secrets, migrations, release process, and monitoring;
- cross-repository, cross-package, or workspace dependencies, if visible.

Do not stop at component names. Explain how control and data move between components.

### Phase 6. Assess AI-friendly architecture signals

This is not a purity test. Use it to produce practical, evidence-backed recommendations.

Identify:

- bounded contexts, feature slices, modules, apps, packages, or services with clear ownership;
- unclear boundaries, especially broad `common`, `shared`, `helpers`, `utils`, or cross-cutting modules that hide responsibilities;
- public contracts such as schemas, OpenAPI, Protobuf, GraphQL schemas, typed DTOs, validators, CLI interfaces, SQL result shapes, UI route contracts, event payload definitions, or documented APIs;
- dependency direction and whether it is clean, mixed, circular, or undocumented;
- side-effect boundaries for database access, network calls, file I/O, subprocesses, clock/time, randomness, environment variables, queues, and external services;
- verification guardrails such as fast focused tests, contract tests, architecture/import rules, type checks, linting, CI, snapshot/golden tests, and documented manual checks;
- context layers for future agents, including `AGENTS.md`, `CLAUDE.md`, `.codex/`, `.agents/`, `.cursor/`, local READMEs, ADRs, specifications, and architecture docs;
- generated, vendored, migration, schema, build, and lock files that future agents should not edit casually.

When recommending improvements, tie each suggestion to one of these categories:

- Documentation/context
- Boundary/modularity
- Contract/schema
- Verification/guardrail
- Runtime/operations
- Security/data safety
- Dependency risk

Prefer the smallest enforceable improvement, such as documenting a boundary, adding a focused test, introducing an import rule, adding a schema, clarifying an owner, isolating a visible side effect, or adding a contract check. Avoid speculative rewrites and avoid adding abstractions before there is evidence of repeated behavior, unsafe coupling, or real volatility.

### Phase 7. Build the architecture story

Explain the repository as a narrative:

- What problem does it solve?
- What are the major moving parts?
- How does data or control flow through the system?
- Where should a new developer start reading?
- What should a manager know about value, risk, and maintainability?
- What should an AI coding agent know to avoid unsafe edits?

Keep the story grounded in evidence. Preserve project terminology.

### Phase 8. Validate claims and diagrams before finalizing

Before writing or updating the final docs, run a validation pass. Treat this as an evaluator review, not another generation pass.

Check for:

- diagram nodes with no evidence;
- diagram edges with no relationship-ledger support;
- major entry points missing from diagrams or prose;
- components in prose but absent from diagrams;
- external systems mentioned without config, code, docs, or tests supporting them;
- contradictory claims between README, docs, code, config, tests, and deployment files;
- claims about runtime behavior that only come from naming or convention;
- generated or vendored code described as hand-authored architecture;
- missing tests or commands in the safe-change guide;
- mismatches between dependency direction in prose and imports/config;
- hidden side effects not surfaced in safe-change guidance;
- broad utility/common modules that need boundary notes;
- orphan components in diagrams that indicate either missing evidence or fragmented modeling.

Record validation results in the docs:

- Resolve supported issues before final output.
- Put unresolved contradictions in **Assumptions and items needing human validation**.
- Put high-value fixes in **Suggested architecture improvements**.
- Do not hide low-confidence areas.

### Phase 9. Assess documentation confidence

For each major claim, classify confidence:

- **High** — directly supported by files, tests, config, command output, or clear explicit docs.
- **Medium** — strongly implied by structure, framework conventions, or repeated naming patterns.
- **Low** — plausible but needs human validation.

Low-confidence claims must appear in the assumptions or open questions section.

## Diagram strategy

Use Mermaid diagrams when they add clarity. Prefer stable names from the codebase.

For most non-trivial repositories, prefer a C4-inspired stack of diagrams:

1. **System context** — users, the repository/system, external systems, external data stores, and external actors.
2. **Container/runtime view** — deployable or runnable units such as API service, frontend app, worker, CLI, database, queue, scheduler, or data pipeline.
3. **Component/module view** — major packages, apps, modules, services, controllers, workers, stores, or libraries inside a container.
4. **Dynamic/request/data-flow view** — the highest-value runtime flow, such as request handling, job processing, data import/export, or UI-to-API flow.
5. **Dependency direction view** — dependency arrows between major modules or layers when inferable.
6. **Boundary/contract view** — APIs, schemas, DTOs, events, SQL result shapes, or validation boundaries.
7. **AI-agent navigation view** — files to read first and safe edit boundaries.
8. **Deployment/runtime view** — processes, containers, infrastructure, CI/CD, or operational dependencies when inferable.

Do not force all diagrams. Use the smallest set that helps readers answer the quality-bar questions.

When Mermaid is included:

- Keep diagrams small enough to read.
- Prefer multiple simple diagrams over one large unreadable diagram.
- Use stable names from code, config, docs, and tests.
- Do not include secrets, real credentials, tokens, or sensitive production details.
- Put a short explanation below each diagram.
- State the evidence basis for important edges.
- Avoid diagram edges that only exist because they “look architecturally right.”

## Output files

Create or update both files in the repository root unless the user specifies a different location.

If `ARCHITECTURE_TEMPLATE.md` or `ARCHITECTURE_DIAGRAMS_TEMPLATE.md` exists, use it as the preferred structure. If those templates are absent, use the required sections below.

### `ARCHITECTURE.md`

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
16. Appendix: relationship ledger summary
17. Appendix: validation notes

### `ARCHITECTURE_DIAGRAMS.md`

Include Mermaid diagrams when they add clarity.

Prefer these diagrams when inferable:

- system context diagram;
- container/runtime diagram;
- component/module diagram;
- request/data-flow diagram;
- dependency direction diagram;
- boundary/contract diagram;
- AI-agent navigation diagram;
- deployment/runtime diagram.

For a very small repository, it is acceptable to write:

> No diagram is included because the repository is a single small script and a diagram would add more noise than clarity.

For each diagram, include:

- a short purpose statement;
- the Mermaid diagram;
- key evidence for important nodes and edges;
- confidence notes for inferred relationships;
- open questions if the relationship evidence is incomplete.

## Suggested improvements section

Near the end of `ARCHITECTURE.md`, include suggested changes in a table with these columns:

| Category | Recommendation | Evidence | Senior developer rationale | Manager rationale | Effort | Risk | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |

Use this guidance:

- **Senior developer rationale** should focus on correctness, testability, modularity, readability, coupling, observability, operational safety, and future change cost.
- **Manager rationale** should focus on onboarding speed, delivery predictability, operational risk, bus factor, auditability, support cost, and business continuity.
- **Category** must be one of: Documentation/context, Boundary/modularity, Contract/schema, Verification/guardrail, Runtime/operations, Security/data safety, or Dependency risk.
- Keep recommendations practical. Avoid speculative rewrites.
- Favor KISS and YAGNI. Suggest the smallest change that improves clarity or safety.
- Separate documentation gaps from code architecture issues.
- Do not describe a repository as "AI-friendly" or "AI-hostile" without citing concrete evidence.
- Do not recommend a named architecture pattern as a goal by itself. Recommend specific local changes that reduce ambiguity, coupling, hidden side effects, or verification gaps.
- Prefer enforceable recommendations: a test, contract, import rule, schema, boundary note, runbook, CI check, or ownership clarification.

## AI agent navigation guidance

Include guidance that helps future AI agents operate safely:

- files to read first;
- files likely to be generated or not hand-edited;
- commands to run before and after changes;
- tests most relevant to major areas;
- risky areas where human confirmation is needed;
- domain terms that must be preserved;
- known conventions from the repo;
- context files and local docs future agents should read before editing;
- intended edit scopes and areas where scope expansion must be explained;
- boundaries that should not be crossed casually;
- relationship edges that are evidence-backed versus inferred;
- side effects that require extra caution;
- contracts or schemas that must be updated together.

## Verification requirements

After writing the docs, add verification instructions to `ARCHITECTURE.md` and run or recommend the included standard-library verifier if it exists:

```bash
python verify_architecture_docs.py
```

If the verifier is stored in a skill or scripts folder, use the actual path, for example:

```bash
python .claude/skills/repo-architecture-walkthrough/scripts/verify_architecture_docs.py
```

If no verifier exists, manually check the docs against the quality bar and mention that no verifier script was found.

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
- important diagram edges are represented in the relationship ledger summary.
- validation notes identify unresolved contradictions, inferred relationships, or missing evidence.

If the verifier fails, fix the documentation or explain why a warning is acceptable.

## Quality bar

The final walkthrough should let a reader answer:

- What is this repository for?
- Where do I start reading?
- How do the main pieces fit together?
- What evidence supports the main components and relationships?
- How does data or control move through the system?
- How do I run or test it?
- What contracts, schemas, or interfaces define important boundaries?
- What are the riskiest areas to change?
- What assumptions still need a human?
- What small architecture improvements would most improve maintainability?

## Completion response

When finished, summarize only:

- files created or updated;
- highest-value findings;
- assumptions needing human validation;
- verification result or command to run.

Do not paste the full generated architecture documents into chat unless the user asks.
