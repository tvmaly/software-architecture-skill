# Architecture Walkthrough Language Guide

Use this vocabulary when writing `ARCHITECTURE.md` and `ARCHITECTURE_DIAGRAMS.md`.

## Confidence Labels

- **High confidence**: directly supported by source code, tests, config, docs, or clear framework convention.
- **Medium confidence**: strongly implied by naming, structure, or common convention, but not directly documented.
- **Low confidence**: plausible inference that needs human validation.

## Preferred Wording

Use:

- "The repository appears to..." for medium confidence.
- "This likely means..." for low confidence.
- "Needs human validation" when the consequence of being wrong is meaningful.
- "Entry point" for where execution starts.
- "Component" for a cohesive module, package, app, or subsystem.
- "Boundary" for a line between responsibilities.
- "Seam" for a place where behavior can be tested, replaced, or refactored safely.
- "Dependency direction" for which layer imports or calls another layer.
- "Runtime path" for what happens during execution.
- "Operational concern" for deployment, scheduling, logging, monitoring, retries, secrets, and failure handling.
- "Boundary clarity" for how obvious it is where a change belongs.
- "Public contract" for a typed, schema-backed, validated, or documented interface between components or systems.
- "Side-effect boundary" for the narrow place where core logic touches databases, networks, files, subprocesses, environment, queues, time, or randomness.
- "Context layer" for durable repo files that guide humans and AI agents, such as `AGENTS.md`, `CLAUDE.md`, ADRs, local READMEs, specs, and architecture docs.
- "Guardrail" for an enforceable check such as a test, contract test, import rule, type check, linter, CI check, or verifier.
- "Vertical slice" only when the repo is organized by feature or workflow and evidence supports that term.
- "Bounded context" only when the repo shows a domain boundary with its own language, ownership, and rules.

Avoid:

- "obviously"
- "clearly" unless the evidence is direct
- "just"
- unsupported claims like "well-architected" or "bad architecture"
- unsupported claims like "AI-friendly" or "AI-hostile"
- speculative rewrites
- generic advice that is not tied to repository evidence
- recommending a named architecture pattern as a goal by itself

## Audience Style

### New Developers

- Explain where to start.
- Explain what each major piece owns.
- Mention tests and safe first tasks.
- Avoid assuming domain knowledge.

### Managers and Business Stakeholders

- Explain business purpose.
- Explain support and operational risk.
- Explain onboarding and bus-factor concerns.
- Translate technical debt into delivery predictability and maintenance cost.

### AI Agents

- List files to read before editing.
- Identify generated files.
- Identify commands to run.
- Identify assumptions and risky areas.
- Preserve domain terms exactly.
- Avoid broad rewrites unless explicitly requested.
- Identify the context files and local docs to read before editing.
- Explain intended edit scopes and when scope expansion needs human review.
- Prefer specific local guardrails over broad architectural advice.

## Improvement Recommendation Style

Each recommendation must include two rationales:

- **Senior developer rationale**: correctness, coupling, cohesion, observability, testing, maintainability, operational safety.
- **Manager rationale**: onboarding speed, delivery predictability, risk reduction, support cost, auditability, business continuity.

Each recommendation must use one category:

- Documentation/context
- Boundary/modularity
- Contract/schema
- Verification/guardrail
- Runtime/operations
- Security/data safety
- Dependency risk

Prefer:

- small documentation improvements
- clearer module boundaries
- explicit entry points
- explicit public contracts, schemas, validators, typed payloads, or documented interface shapes
- focused tests, contract tests, import rules, type checks, and CI checks that make architecture enforceable
- context files and local READMEs that reduce future agent guesswork
- test gaps that affect confidence
- configuration clarity
- better naming where it reduces confusion
- extraction only when repeated behavior or unsafe coupling is evident
- side-effect isolation when direct infrastructure access makes core behavior hard to test

Avoid:

- framework migrations without strong evidence
- large rewrites
- speculative microservices
- adding abstractions before repeated needs exist
- diagramming everything
- describing Clean, Hexagonal, DDD, or vertical slices as inherently required
- replacing a concrete local fix with a broad pattern recommendation
- architecture recommendations that cannot be checked by a reviewer or future agent
