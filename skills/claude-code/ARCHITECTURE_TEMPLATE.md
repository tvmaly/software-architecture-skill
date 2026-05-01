# Architecture Walkthrough

> This document explains the repository for new developers, managers, and AI coding agents. It should describe the current architecture as it exists today, not an idealized version.

## 1. Executive Summary

Briefly explain:

- what this repository does
- who uses it
- what business or technical capability it supports
- the most important architectural idea to understand first
- the highest-confidence risks or improvement opportunities

## 2. Repository Purpose

Describe the repository in plain language.

Include:

- system type: app, service, library, batch job, report, frontend, backend, data pipeline, monorepo, or mixed
- primary users or downstream systems
- business capability
- important constraints

## 3. Audience Guide

### For New Developers

Explain what they should read first and what they should ignore at first.

### For Managers and Business Stakeholders

Explain value, ownership, risk, operational shape, and support burden without implementation-heavy language.

### For AI Coding Agents

Explain the safest way to navigate and modify the repository.

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

| Component | Responsibility | Important Files | Depends On | Notes |
|---|---|---|---|---|
| Component name | What it owns | `path` | Other components/systems | Key facts |

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
- test commands to run after changes
- important naming or domain conventions
- boundaries that should not be crossed
- areas where human confirmation is required

## 12. Assumptions and Items Needing Human Validation

List anything that is inferred but not directly proven.

| Item | Assumption or Question | Why It Matters | Confidence |
|---|---|---|---|
| Topic | What needs validation | Risk or impact | Low/Medium |

## 13. Suggested Architecture Improvements

Recommend practical improvements. Favor KISS and YAGNI. Avoid speculative rewrites.

| Recommendation | Evidence | Senior Developer Rationale | Manager Rationale | Effort | Risk | Priority |
|---|---|---|---|---|---|---|
| Small change | Files or behavior observed | Why it improves correctness/testability/maintainability | Why it improves predictability/risk/onboarding/cost | S/M/L | Low/Med/High | P1/P2/P3 |

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
