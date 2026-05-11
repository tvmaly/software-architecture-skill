#!/usr/bin/env python3
"""Verify repository architecture walkthrough docs.

Assumptions:
- Python 3.10.2+
- Standard library only
- Run from the repository root that contains ARCHITECTURE.md and ARCHITECTURE_DIAGRAMS.md
"""

from __future__ import annotations

import re
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

SECTION_HEADING_RE = re.compile(r"^##\s+(?:\d+\.\s*)?(.+?)\s*$", re.MULTILINE)
TABLE_LINE_RE = re.compile(r"^\|(.+)\|\s*$", re.MULTILINE)


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


def section_text(markdown: str, heading: str) -> str:
    wanted = normalize_heading(heading)
    matches = list(SECTION_HEADING_RE.finditer(markdown))
    for index, match in enumerate(matches):
        if normalize_heading(match.group(1)) != wanted:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        return markdown[start:end].strip()
    return ""


def table_headers(section: str) -> list[list[str]]:
    headers: list[list[str]] = []
    for match in TABLE_LINE_RE.finditer(section):
        cells = [cell.strip() for cell in match.group(1).split("|")]
        if cells:
            headers.append(cells)
    return headers


def has_table_header(section: str, required_columns: Iterable[str]) -> bool:
    required = {normalize_heading(column) for column in required_columns}
    for header in table_headers(section):
        normalized = {normalize_heading(column) for column in header}
        if required.issubset(normalized):
            return True
    return False


def check_suggested_improvements(markdown: str) -> list[str]:
    section = section_text(markdown, "Suggested Architecture Improvements")
    if not section:
        return ["Suggested Architecture Improvements section is empty or missing."]
    if "no recommendations" in section.lower():
        return []
    required = [
        "Category",
        "Recommendation",
        "Evidence",
        "Senior Developer Rationale",
        "Manager Rationale",
        "Effort",
        "Risk",
        "Priority",
    ]
    if not has_table_header(section, required):
        return [
            "Suggested Architecture Improvements table must include columns: "
            + ", ".join(required)
        ]
    return []


def check_safe_change_guidance(markdown: str) -> list[str]:
    section = section_text(markdown, "Safe Change Guide for Humans and AI Agents")
    if not section:
        return ["Safe Change Guide for Humans and AI Agents section is empty or missing."]
    lowered = section.lower()
    if "agent" not in lowered and "ai" not in lowered:
        return ["Safe change guidance should include explicit guidance for AI agents."]
    return []


def check_evidence_map(markdown: str) -> list[str]:
    section = section_text(markdown, "Appendix: Evidence Map")
    if not section:
        return ["Evidence map section is empty or missing."]
    if "path/to/" in section or "architectural claim" in section.lower():
        return ["Evidence map still appears to contain template placeholder content."]
    for match in PATH_LIKE_RE.finditer(section):
        raw = match.group(1).strip()
        if not raw or raw in {"ARCHITECTURE.md", "ARCHITECTURE_DIAGRAMS.md"}:
            continue
        if looks_like_local_path(raw) and not any(part in raw for part in ("path/to/", "<", ">")):
            return []
    if "limited" in section.lower() or "not applicable" in section.lower() or "n/a" in section.lower():
        return []
    return ["Evidence map does not include concrete local file/config/test references."]


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
    errors.extend(f"ARCHITECTURE.md: {msg}" for msg in check_suggested_improvements(architecture_text))
    errors.extend(f"ARCHITECTURE.md: {msg}" for msg in check_safe_change_guidance(architecture_text))

    warnings.extend(check_referenced_paths(architecture_text))
    warnings.extend(check_referenced_paths(diagrams_text))
    warnings.extend(f"ARCHITECTURE.md: {msg}" for msg in check_evidence_map(architecture_text))

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
