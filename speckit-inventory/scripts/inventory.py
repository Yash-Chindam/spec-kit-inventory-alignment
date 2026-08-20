#!/usr/bin/env python3
"""Extract a deterministic, read-only inventory from Spec Kit Markdown artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ID_PATTERN = re.compile(r"\b(?:FR|NFR|SC|AC|T)-\d+\b", re.IGNORECASE)
TASK_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\[[ xX]\]\s*)?(T\d+)\b"
    r"(?:\s*[-:.)]\s*)?(.*)$",
    re.IGNORECASE,
)
REQUIREMENT_PREFIXES = ("FR-", "NFR-", "SC-", "AC-")

# Requirement IDs are harvested from both artifacts so the inventory covers every
# live ID, but `spec.md` is scanned first so it wins as the definition site when
# the same ID is also referenced from `tasks.md`.
REQUIREMENT_SOURCES = ("spec.md", "tasks.md")


def _read(path: Path) -> str:
    """Read a UTF-8 Markdown file, returning an empty string when absent."""
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _normalize_task_id(raw: str) -> str:
    """Return a task ID in the canonical zero-padded `T000` form.

    Accepts the shapes a user may type or a document may contain (`T14`, `t014`,
    `TASK-14`) so command-line lookups agree with the generated inventory.
    """
    digits = re.sub(r"\D", "", raw)
    if not digits:
        msg = f"{raw!r} does not contain a task number"
        raise ValueError(msg)
    return f"T{int(digits):03d}"


def _requirements(sources: dict[str, str]) -> list[dict[str, Any]]:
    """Return unique requirement IDs with their source artifact, line, and text."""
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for source in REQUIREMENT_SOURCES:
        for line_number, line in enumerate(sources[source].splitlines(), start=1):
            for match in ID_PATTERN.finditer(line):
                identifier = match.group(0).upper()
                if not identifier.startswith(REQUIREMENT_PREFIXES):
                    continue
                if identifier in seen:
                    continue
                seen.add(identifier)
                result.append(
                    {
                        "id": identifier,
                        "source": source,
                        "line": line_number,
                        "text": line.strip(),
                    }
                )
    return result


def _tasks(text: str) -> list[dict[str, Any]]:
    """Return unique task IDs with their source line, text, and covered IDs."""
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = TASK_PATTERN.match(line)
        if not match:
            continue
        identifier = _normalize_task_id(match.group(1))
        if identifier in seen:
            continue
        seen.add(identifier)
        result.append(
            {
                "id": identifier,
                "source": "tasks.md",
                "line": line_number,
                "text": match.group(2).strip(),
                "covers": sorted(
                    {
                        item.upper()
                        for item in ID_PATTERN.findall(line)
                        if item.upper().startswith(REQUIREMENT_PREFIXES)
                    }
                ),
            }
        )
    return result


def build_inventory(feature_dir: Path) -> dict[str, Any]:
    """Build an inventory for one feature directory."""
    sources = {name: _read(feature_dir / name) for name in REQUIREMENT_SOURCES}
    return {
        "schema_version": "1",
        "feature_dir": str(feature_dir),
        "requirements": _requirements(sources),
        "tasks": _tasks(sources["tasks.md"]),
    }


def context_pack(inventory: dict[str, Any], task: str) -> dict[str, Any]:
    """Narrow an inventory to one task and the requirements that task covers.

    Raises:
        LookupError: If the task ID is absent from the inventory.
        ValueError: If the task ID contains no task number.
    """
    task_id = _normalize_task_id(task)
    record = next((item for item in inventory["tasks"] if item["id"] == task_id), None)
    if record is None:
        msg = f"task {task_id} was not found"
        raise LookupError(msg)
    covered = set(record["covers"])
    return {
        "schema_version": inventory["schema_version"],
        "feature_dir": inventory["feature_dir"],
        "task": record,
        "requirements": [
            item for item in inventory["requirements"] if item["id"] in covered
        ],
    }


def main() -> None:
    """Parse arguments and print an inventory or task context pack as JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature-dir", type=Path, required=True)
    parser.add_argument("--task", help="Return only the context pack for this task ID")
    args = parser.parse_args()
    inventory = build_inventory(args.feature_dir)
    if args.task:
        try:
            inventory = context_pack(inventory, args.task)
        except (LookupError, ValueError) as error:
            parser.error(f"{error} in {args.feature_dir / 'tasks.md'}")
    print(json.dumps(inventory, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
