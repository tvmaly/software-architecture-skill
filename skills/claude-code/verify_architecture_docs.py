#!/usr/bin/env python3
"""Verify repository architecture walkthrough docs.

Assumptions:
- Python 3.10.2+
- Standard library only
- Run from the repository root that contains ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Iterable

ARCHITECTURE = Path("ARCHITECTURE.md")
DIAGRAMS = Path("ARCHITECTURE_DIAGRAMS.md")

REQUIRED_ARCHITECTURE_HEADINGS = [
    "Executive Summary",
    "Repository Purpose",
    "Audience Guide",
    "System Context",
    "Main Entry Points",
    "Major Components",
    "Data and Control Flow",
    "Runtime, Configuration, and Deployment",
    "Testing and Verification",
    "How to Navigate the Codebase",
    "Safe Change Guide for Humans and AI Agents",
    "Assumptions and Items Needing Human Validation",
    "Suggested Architecture Improvements",
    "Glossary",
    "Appendix: Evidence Map",
]

REQUIRED_DIAGRAM_HEADINGS = [
    "Architecture Diagrams",
]

PATH_LIKE_RE = re.compile(r"`([^`]+)`")
MERMAID_FENCE_RE = re.compile(r"```mermaid\b|```", re.IGNORECASE)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text()


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^\d+(\.\d+)*\.\s*", "", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return text.strip()


def headings_in(markdown: str) -> set[str]:
    headings: set[str] = set()
    for line in markdown.splitlines():
        if line.lstrip().startswith("#"):
            headings.add(normalize_heading(line))
    return headings


def check_required_headings(markdown: str, required: Iterable[str]) -> list[str]:
    found = headings_in(markdown)
    missing = []
    for heading in required:
        if normalize_heading(heading) not in found:
            missing.append(heading)
    return missing


def check_mermaid_fences(markdown: str) -> list[str]:
    errors: list[str] = []
    in_mermaid = False
    start_line = 0

    for line_number, line in enumerate(markdown.splitlines(), start=1):
        stripped = line.strip().lower()
        if not in_mermaid and stripped.startswith("```mermaid"):
            in_mermaid = True
            start_line = line_number
        elif in_mermaid and stripped == "```":
            in_mermaid = False

    if in_mermaid:
        errors.append(f"Unclosed Mermaid code fence starting near line {start_line}.")

    return errors


def looks_like_local_path(value: str) -> bool:
    if " " in value:
        return False
    if value.startswith(("http://", "https://", "mailto:", "#")):
        return False
    if value.startswith(("$", "--", "-")):
        return False
    if value in {"ARCHITECTURE.md", "ARCHITECTURE_DIAGRAMS.md"}:
        return True
    if "/" in value:
        return True
    suffixes = (
        ".py", ".go", ".js", ".ts", ".vue", ".sql", ".md", ".toml", ".json",
        ".yaml", ".yml", ".ini", ".cfg", ".txt", ".sh", ".bat", ".ps1",
        ".html", ".css", ".scss", ".java", ".kt", ".rb", ".pl",
    )
    return value.endswith(suffixes)


def check_referenced_paths(markdown: str) -> list[str]:
    warnings: list[str] = []
    seen: set[str] = set()

    for match in PATH_LIKE_RE.finditer(markdown):
        raw = match.group(1).strip()
        if not raw or raw in seen or not looks_like_local_path(raw):
            continue
        seen.add(raw)

        # Allow simple placeholders in templates or unresolved examples.
        if any(part in raw for part in ("path/to/", "example/", "<", ">")):
            continue

        # Handle references with line numbers or anchors.
        clean = raw.split("#", 1)[0].split(":", 1)[0]
        clean_path = Path(clean)
        if not clean_path.exists():
            warnings.append(f"Referenced path does not exist: `{raw}`")

    return warnings


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not ARCHITECTURE.exists():
        errors.append("Missing ARCHITECTURE.md")
    if not DIAGRAMS.exists():
        errors.append("Missing ARCHITECTURE_DIAGRAMS.md")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    architecture_text = read_text(ARCHITECTURE)
    diagrams_text = read_text(DIAGRAMS)

    missing_arch_headings = check_required_headings(
        architecture_text, REQUIRED_ARCHITECTURE_HEADINGS
    )
    for heading in missing_arch_headings:
        errors.append(f"ARCHITECTURE.md missing required heading: {heading}")

    missing_diagram_headings = check_required_headings(
        diagrams_text, REQUIRED_DIAGRAM_HEADINGS
    )
    for heading in missing_diagram_headings:
        errors.append(f"ARCHITECTURE_DIAGRAMS.md missing required heading: {heading}")

    errors.extend(f"ARCHITECTURE.md: {msg}" for msg in check_mermaid_fences(architecture_text))
    errors.extend(f"ARCHITECTURE_DIAGRAMS.md: {msg}" for msg in check_mermaid_fences(diagrams_text))

    warnings.extend(check_referenced_paths(architecture_text))
    warnings.extend(check_referenced_paths(diagrams_text))

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Architecture documentation verification passed.")
    if warnings:
        print(f"Completed with {len(warnings)} warning(s). Review warnings for stale paths or placeholders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
