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

Avoid:

- "obviously"
- "clearly" unless the evidence is direct
- "just"
- unsupported claims like "well-architected" or "bad architecture"
- speculative rewrites
- generic advice that is not tied to repository evidence

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

## Improvement Recommendation Style

Each recommendation must include two rationales:

- **Senior developer rationale**: correctness, coupling, cohesion, observability, testing, maintainability, operational safety.
- **Manager rationale**: onboarding speed, delivery predictability, risk reduction, support cost, auditability, business continuity.

Prefer:

- small documentation improvements
- clearer module boundaries
- explicit entry points
- test gaps that affect confidence
- configuration clarity
- better naming where it reduces confusion
- extraction only when repeated behavior or unsafe coupling is evident

Avoid:

- framework migrations without strong evidence
- large rewrites
- speculative microservices
- adding abstractions before repeated needs exist
- diagramming everything
