# Architecture Walkthrough

> This document explains the repository for new developers, managers, and AI coding agents. It should describe the current architecture as it exists today, not an idealized version.

## 1. Executive Summary

Briefly explain:

- what this repository does
- who uses it
- what business or technical capability it supports
- the most important architectural idea to understand first
- the highest-confidence risks or improvement opportunities
- the strongest evidence about whether future AI-assisted changes are easy to localize and verify

## 2. Repository Purpose

Describe the repository in plain language.

Include:

- system type: app, service, library, batch job, report, frontend, backend, data pipeline, monorepo, or mixed
- primary users or downstream systems
- business capability
- important constraints
- out-of-scope responsibilities when the repository boundary is easy to confuse

## 3. Audience Guide

### For New Developers

Explain what they should read first and what they should ignore at first.

### For Managers and Business Stakeholders

Explain value, ownership, risk, operational shape, and support burden without implementation-heavy language.

### For AI Coding Agents

Explain the safest way to navigate and modify the repository. Include context files or local docs to read first, intended edit-scope expectations, protected areas, and verification commands.

## 4. System Context

Describe how this repository fits into the larger ecosystem.

Include known or inferred:

- upstream systems
- downstream systems
- databases
- APIs
- batch inputs and outputs
- UI clients
- external services
- scheduled jobs

See `ARCHITECTURE_DIAGRAMS.md` for diagrams.

## 5. Main Entry Points

List the main ways code execution starts.

| Entry Point | Type | Purpose | Evidence | Confidence |
|---|---|---|---|---|
| `path/to/file` | CLI/API/job/UI/test | What starts here | File, function, config, route, command | High/Medium/Low |

## 6. Major Components

Explain the major modules, packages, apps, or services.

Call out boundary clarity. Note whether each component has an obvious public interface, whether its dependencies point in an intentional direction, and whether shared/common/helper code hides ownership.

| Component | Responsibility | Public Interface / Entry | Important Files | Depends On | Boundary Notes |
|---|---|---|---|---|---|
| Component name | What it owns | API, command, route, schema, function, or module boundary | `path` | Other components/systems | Clear/mixed/unclear, with evidence |

## 7. Data and Control Flow

Explain the normal flow through the system.

Include:

- request lifecycle, job lifecycle, or command lifecycle
- data inputs
- transformations
- persistence
- outputs
- error handling
- retries or recovery behavior when visible
- side effects such as database writes, network calls, file I/O, subprocesses, queues, time, randomness, and environment access
- contract points such as schemas, validators, typed payloads, SQL row shapes, or external API expectations

## 8. Runtime, Configuration, and Deployment

Explain how the system runs.

Include:

- local development commands
- test commands
- build commands
- deployment hints
- environment variables
- config files
- database migrations
- operational concerns
- startup validation, secrets handling, logging, monitoring, rollback, and failure-mode signals when visible

## 9. Testing and Verification

Explain the test strategy visible in the repo.

Include:

- unit tests
- integration tests
- acceptance tests
- frontend tests
- SQL validation
- fixture strategy
- commands to run
- gaps or missing verification
- contract tests, architecture/import rules, type checks, linting, snapshot/golden tests, performance checks, and CI checks when visible
- the fastest focused verification path a future agent should run after a small change

## 10. How to Navigate the Codebase

Give a practical reading order.

Example:

1. Start with `README.md`.
2. Read `path/to/entrypoint` to understand startup.
3. Read `path/to/domain` for business logic.
4. Read `path/to/tests` to understand expected behavior.
5. Read deployment/config files last.

## 11. Safe Change Guide for Humans and AI Agents

Explain how to make changes safely.

Include:

- files to read before editing
- files likely to be generated
- files that should not be edited casually
- context files such as `AGENTS.md`, `CLAUDE.md`, `.codex/`, `.agents/`, `.cursor/`, local READMEs, ADRs, specs, or architecture docs
- intended edit scopes for common change types
- when scope expansion must be explained to a human reviewer
- test commands to run after changes
- important naming or domain conventions
- boundaries that should not be crossed
- public contracts or schemas that must remain backward compatible
- side-effect boundaries that should not leak into core logic
- areas where human confirmation is required

## 12. Assumptions and Items Needing Human Validation

List anything that is inferred but not directly proven.

| Item | Assumption or Question | Why It Matters | Confidence |
|---|---|---|---|
| Topic | What needs validation | Risk or impact | Low/Medium |

## 13. Suggested Architecture Improvements

Recommend practical improvements. Favor KISS and YAGNI. Avoid speculative rewrites.

Every recommendation must be evidence-backed and categorized. Use only these categories: Documentation/context, Boundary/modularity, Contract/schema, Verification/guardrail, Runtime/operations, Security/data safety, Dependency risk.

Prefer small enforceable changes such as documenting a boundary, adding a focused test, introducing an import rule, clarifying an owner, adding a schema, or isolating a visible side effect. Do not recommend a named architecture pattern, microservices, or a framework migration unless the evidence shows smaller local improvements are insufficient.

| Category | Recommendation | Evidence | Senior Developer Rationale | Manager Rationale | Effort | Risk | Priority |
|---|---|---|---|---|---|---|---|
| Documentation/context | Small change | Files or behavior observed | Why it improves correctness/testability/maintainability/AI-agent safety | Why it improves predictability/risk/onboarding/cost | S/M/L | Low/Med/High | P1/P2/P3 |

## 14. Glossary

Define domain terms, acronyms, internal libraries, service names, and abbreviations.

| Term | Meaning | Evidence | Confidence |
|---|---|---|---|
| Term | Definition | Where it appears | High/Medium/Low |

## 15. Appendix: Evidence Map

Map important claims to files.

| Claim | Evidence | Confidence |
|---|---|---|
| Architectural claim | `path/to/file`, function, config, test, or doc | High/Medium/Low |
