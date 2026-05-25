---
name: repo-architecture-walkthrough
description: Generate repository architecture documentation for AI-assisted development. Use when asked to analyze, explain, document, map, onboard to, or create ARCHITECTURE.md / ARCHITECTURE_DIAGRAMS.md for a codebase. Produces a human-reviewable architecture walkthrough for developers, managers, and future AI coding agents.
---

# Repo Architecture Walkthrough Skill for Codex

You are helping the user understand a code repository from the ground up. Inspect the repository, ask a very small number of useful questions, recover the architecture from repository evidence, and create two durable Markdown files:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

Optimize the walkthrough for three audiences at once:

1. **New developer onboarding** — someone who needs to become productive safely.
2. **Manager or business understanding** — someone who needs purpose, risk, ownership, and operational shape without implementation overload.
3. **AI coding agent navigation** — future Codex/LLM coding agents that need accurate maps, entry points, invariants, commands, assumptions, and safe-change guidance.

The default technology assumptions are Python, SQL, Go, JavaScript, Vue.js, and Django, but infer the actual stack from repository evidence.

## What is improved in this version

This version adds a more rigorous architecture-recovery workflow:

- explicit evidence gathering before synthesis;
- adaptive grouping for large or legacy repositories;
- dependency-aware relationship extraction before diagrams;
- a claim-and-edge validation pass before writing final docs;
- C4-style diagram layering where useful;
- mismatch detection between code, docs, diagrams, configuration, and tests;
- stronger guidance for documenting relationships, not just components.

Use these additions to reduce unsupported edges, orphan components, fragmented diagrams, and plausible-but-ungrounded architecture narratives.

## Codex-specific behavior

- This skill writes documentation only unless the user explicitly asks for source-code changes.
- Treat the repository as the source of truth. Prefer file evidence over guesses.
- Use Codex tools to inspect files, search text, read configuration, examine tests, and run read-only discovery commands before writing conclusions.
- Do not claim that commands passed unless you actually ran them and observed the result.
- If the working tree already has user changes, avoid overwriting unrelated files. Preserve user edits.
- Keep generated documentation easy to diff and review in Git.
- When useful, mention this skill explicitly in your plan as `$repo-architecture-walkthrough` so the user knows which workflow is being applied.
- Keep any intermediate scratch work internal unless the user asks to see it. The durable deliverables remain `ARCHITECTURE.md` and `ARCHITECTURE_DIAGRAMS.md`.

## Non-negotiable principles

- Prefer facts grounded in files over guesses.
- Mark uncertain claims as assumptions.
- Do not invent runtime behavior that cannot be inferred.
- Do not draw a relationship edge unless there is evidence for it, or it is clearly labeled as an assumption.
- Keep the first user interview short.
- Create useful documentation even when some details are unknown.
- Make the walkthrough beginner-friendly without dumbing it down.
- Use project vocabulary from the codebase, README files, docs, tests, configs, migrations, API routes, job names, deployment files, and domain schemas.
- Include suggested architecture improvements near the end of `ARCHITECTURE.md`, with rationale from both a senior developer perspective and a manager perspective.
- Include Mermaid diagrams by default when they add clarity. Use judgment: for a single script file under roughly 200 lines, diagrams may be unnecessary.
- Prefer multiple small diagrams over one large diagram.
- Do not replace human architectural judgment. Use the architecture docs to make human review easier.
- Make architecture friendliness for AI agents evidence-based: assess boundaries, contracts, dependency direction, context files, side-effect isolation, test harnesses, and enforceable guardrails before recommending changes.
- Prefer incremental, reviewable improvements over architectural purity. Do not recommend microservices, Clean Architecture, Hexagonal Architecture, vertical slices, or a framework migration unless repository evidence shows that smaller local fixes are insufficient.

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

## Research-informed recovery workflow

Work in phases. Do not skip directly from file listing to final diagrams on non-trivial repositories.

### Phase 0. Scope and safety check

Before deep inspection:

- Check the working tree status if the repository is under Git.
- Identify whether existing architecture docs already exist.
- Identify repository size and likely complexity.
- Decide whether to inspect all files or use adaptive grouping.
- Note generated, vendored, archived, build, migration, lock, cache, or dependency folders that should not be overinterpreted.

Useful commands, when available:

```bash
git status --short
git ls-files | sed -n '1,200p'
find . -maxdepth 3 -type f | sed -n '1,200p'
rg -n "TODO|FIXME|deprecated|generated|do not edit|architecture|ADR|contract|schema|OpenAPI|protobuf|GraphQL" .
```

Do not run destructive commands. Avoid expensive full-repository commands on very large repositories unless scoped.

### Phase 1. Establish repository identity

Inspect, when present:

- `README*`
- `AGENTS.md`, `.codex/`, `.agents/skills`, or other agent instructions
- `CLAUDE.md`, `.claude/`, `.cursor/`, `.cursorrules`, `CONTEXT.md`, `SPEC.md`, `PLAN.md`, `TASKS.md`, or other AI/context/specification files
- `pyproject.toml`, `setup.py`, `requirements*.txt`, `Pipfile`, `poetry.lock`
- `package.json`, `vite.config.*`, `vue.config.*`, `webpack.config.*`, `tsconfig*.json`
- `go.mod`, `go.sum`
- Django settings, `manage.py`, apps, migrations, urls, views, serializers, Celery tasks
- SQL files, migration folders, schema files, query folders
- OpenAPI, Protobuf, GraphQL, Avro, JSON Schema, Prisma, dbt, ORM model, or API contract files
- `Dockerfile`, `docker-compose*`, Helm charts, Kubernetes manifests, Terraform, Pulumi, serverless configs
- CI files such as `.github/workflows`, Jenkinsfiles, GitLab CI, Makefiles
- test folders, fixtures, golden files, snapshots, contract tests
- docs, ADRs, existing `ARCHITECTURE.md`, `docs/adr/`

Answer:

- What does this repo do?
- What business capability does it support?
- What type of system is it: app, service, library, batch job, report, tool, frontend, backend, data pipeline, monorepo, or mixed?
- How does someone run, test, deploy, or operate it?
- What vocabulary does the repository use for its domain, modules, jobs, APIs, and data?

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
- internal system to external service.

Evidence can include imports, routing tables, dependency manifests, framework conventions, schema references, tests, config values, explicit docs, build files, or observed command output.

Use **no edge without evidence**:

- If an edge is directly supported, include it with High confidence.
- If an edge is strongly implied by framework convention or naming, include it with Medium confidence and explain the convention.
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

For a very small repository, it is acceptable to write:

> No diagram is included because the repository is a single small script and a diagram would add more noise than clarity.

## Technology-specific discovery hints

Use only as hints. The repository’s files are the source of truth.

### Python / Django

Inspect:

- `manage.py`, settings modules, `urls.py`, apps, views, serializers, forms, models, migrations, management commands, Celery tasks, pytest/unittest configuration.
- ORM models, migrations, serializers, API routes, templates, static/frontend integration.

Useful commands when safe:

```bash
python - <<'PY'
import ast, pathlib
for path in pathlib.Path('.').rglob('*.py'):
    if any(part in {'.venv', 'venv', '__pycache__', 'migrations'} for part in path.parts):
        continue
    try:
        tree = ast.parse(path.read_text(errors='ignore'))
    except Exception:
        continue
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [n.name for n in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    if imports:
        print(f"{path}: {', '.join(sorted(set(imports))[:20])}")
PY
```

### JavaScript / TypeScript / Vue

Inspect:

- `package.json`, workspace files, route definitions, `src/`, API clients, stores, components, composables, build configs, test configs.
- UI routes, API client calls, state stores, generated clients, schema/types.

Useful commands when safe:

```bash
rg -n "createRouter|routes:|defineStore|fetch\(|axios|graphql|useQuery|OpenAPI|generated|do not edit" .
```

### Go

Inspect:

- `go.mod`, `cmd/`, `internal/`, `pkg/`, route setup, handlers, services, repositories, generated files, tests.

Useful commands when safe:

```bash
go list ./...
rg -n "func main|http\.Handle|grpc|cobra|sql|gorm|Generated|DO NOT EDIT" .
```

### SQL / data systems

Inspect:

- migrations, schema files, stored procedures, query folders, dbt models, seed data, ORM models, fixtures, ETL jobs.

Useful commands when safe:

```bash
rg -n "CREATE TABLE|ALTER TABLE|INSERT INTO|SELECT .* FROM|dbt|migration|schema|index|foreign key" .
```

### Runtime / deployment

Inspect:

- Docker, Compose, Kubernetes, Helm, Terraform, serverless configs, Procfiles, Makefiles, CI, env examples.

Useful commands when safe:

```bash
rg -n "docker|image:|service:|deployment|cron|schedule|DATABASE_URL|REDIS|QUEUE|SECRET|TOKEN|PORT|health" .
```

## Reference files bundled with this skill

Use these bundled files when creating the output:

- `references/ARCHITECTURE_TEMPLATE.md` — preferred structure for `ARCHITECTURE.md`
- `references/ARCHITECTURE_DIAGRAMS_TEMPLATE.md` — Mermaid diagram guidance and examples
- `references/LANGUAGE.md` — wording, confidence labels, and recommendation style
- `scripts/verify_architecture_docs.py` — Python 3.10.2 standard-library verifier

If the reference files are not available, still create useful docs using the required sections below.

## Output files

Create or update both files in the repository root unless the user specifies a different location.

### `ARCHITECTURE.md`

Use the structure in `references/ARCHITECTURE_TEMPLATE.md`. Adapt headings only when the repository clearly needs it, but keep the core sections.

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

Add a short **Validation notes** subsection inside either section 12 or section 15 when the repository is non-trivial. Include mismatches found during the validation pass, such as unsupported edges, conflicting docs, generated-code ambiguity, or missing runtime evidence.

The evidence map should include enough concrete references for a reviewer to audit the architecture claims. Prefer compact entries over exhaustive file dumps.

### `ARCHITECTURE_DIAGRAMS.md`

Use the structure in `references/ARCHITECTURE_DIAGRAMS_TEMPLATE.md`. Include Mermaid diagrams when they add clarity.

Prefer these diagrams when inferable:

- system context diagram;
- container/runtime diagram;
- component/module diagram;
- request/data-flow diagram;
- dependency direction diagram;
- boundary/contract diagram;
- AI-agent navigation diagram;
- deployment/runtime diagram.

For each diagram, include:

- purpose;
- confidence level;
- Mermaid diagram or explanation for why no diagram is useful;
- short edge-evidence notes for important relationships;
- assumptions or omissions.

For a very small repository, it is acceptable to write:

> No diagram is included because the repository is a single small script and a diagram would add more noise than clarity.

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
- Do not recommend a named architecture pattern as a goal by itself. Recommend specific local changes that reduce ambiguity, coupling, hidden side effects, unsupported relationships, or verification gaps.
- Include at least one recommendation about missing relationship evidence when diagrams or prose required assumptions.
- Include at least one verification/guardrail recommendation when important architecture claims cannot be checked by tests, contracts, import rules, type checks, or CI.

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
- relationships or diagram edges that are low-confidence and need validation before changes;
- entry points whose behavior is not fully covered by tests.

## Verification requirements

After writing the docs, add verification instructions to `ARCHITECTURE.md` and copy or run the bundled standard-library verifier if useful:

```bash
python scripts/verify_architecture_docs.py
```

If the repository does not keep this skill folder inside the repo, use the actual path to the verifier, for example:

```bash
python ~/.agents/skills/repo-architecture-walkthrough/scripts/verify_architecture_docs.py
```

The verifier assumes Python 3.10.2 and uses only the Python standard library.

The docs should pass these checks:

- `ARCHITECTURE.md` exists.
- `ARCHITECTURE_DIAGRAMS.md` exists.
- Required headings are present.
- Mermaid code fences, if present, are balanced.
- Local file references inside backticks appear to exist when they look like paths.
- Assumptions section exists.
- Suggested improvements section exists.
- Suggested improvements table includes a category column.
- AI agent safe-change guidance exists.
- Evidence map contains concrete file/config/test references for non-trivial repositories, or the doc explains why evidence is limited.

Also manually check:

- every major diagram edge has evidence or an assumption label;
- every major entry point is represented in prose or diagrams;
- every low-confidence architecture claim appears in assumptions or validation notes;
- generated/vendored files are called out when relevant;
- safe-change guidance lists the most relevant commands and tests found in the repository.

If the verifier fails, fix the documentation or explain why a warning is acceptable.

## Quality bar

The final walkthrough should let a reader answer:

- What is this repository for?
- Where do I start reading?
- How do the main pieces fit together?
- How does data move through the system?
- What relationships are directly evidenced, implied, or uncertain?
- How do I run or test it?
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
