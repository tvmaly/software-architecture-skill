# Architecture Documentation Guidance

When asked to explain, document, map, onboard to, or review the architecture of this repository, use the `$repo-architecture-walkthrough` skill.

Expected outputs:

- `ARCHITECTURE.md`
- `ARCHITECTURE_DIAGRAMS.md`

The architecture walkthrough should be useful for:

- new developers
- engineering managers and business stakeholders
- future AI coding agents
- human reviewers of AI-assisted code

Before generating the files, ask how familiar the user is with the repository: none, some, or very familiar.

The generated docs should clearly mark assumptions, safe edit areas, protected areas, evidence from files, and suggested architecture improvements with both senior developer and manager rationale.

Suggested improvements should be categorized as Documentation/context, Boundary/modularity, Contract/schema, Verification/guardrail, Runtime/operations, Security/data safety, or Dependency risk. Prefer small evidence-backed guardrails over broad rewrites or named architecture-pattern recommendations.

The walkthrough should identify the context files, public contracts, dependency direction, side-effect boundaries, generated files, and verification commands future AI agents need before making changes.
