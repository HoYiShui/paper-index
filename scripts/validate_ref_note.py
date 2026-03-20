#!/usr/bin/env python3
"""Validate Level 2 paper index notes."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "schema_version",
    "paper_id",
    "title",
    "local_path",
    "year",
    "venue",
    "publication_status",
    "authors",
    "keywords",
    "task_tags",
    "method_tags",
    "dataset_tags",
    "domain_tags",
    "relevance_to_us",
    "one_line_summary",
    "has_code",
    "codebase_link",
    "indexed_at",
    "source_mtime",
]

REQUIRED_SECTIONS = [
    "Problem",
    "Claimed Gap",
    "Core Method",
    "Data and Evaluation",
    "Key Results",
    "Relevance to Our Work",
    "Reusable Ideas",
    "Limitations",
]


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value == "":
        return ""
    if value == "[]":
        return []
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if (
        (value.startswith('"') and value.endswith('"'))
        or (value.startswith("'") and value.endswith("'"))
    ):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")

    data: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[Any] | None = None

    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        if current_key is not None and line.lstrip().startswith("- "):
            assert current_list is not None
            current_list.append(parse_scalar(line.lstrip()[2:]))
            continue

        if current_key is not None:
            data[current_key] = current_list if current_list is not None else []
            current_key = None
            current_list = None

        key_match = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not key_match:
            raise ValueError(f"unsupported frontmatter line: {line}")

        key, value = key_match.groups()
        if value == "":
            current_key = key
            current_list = []
        else:
            data[key] = parse_scalar(value)

    if current_key is not None:
        data[current_key] = current_list if current_list is not None else []

    return data


def find_notes(paths: list[Path]) -> list[Path]:
    notes: list[Path] = []
    for path in paths:
        if path.is_file() and path.name.endswith(".ref.md"):
            notes.append(path)
            continue
        if path.is_dir():
            notes.extend(sorted(p for p in path.rglob("*.ref.md") if p.is_file()))
    return sorted(set(note.resolve() for note in notes))


def missing_fields(data: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            missing.append(field)
            continue
        value = data[field]
        if field == "year":
            continue
        if value in ("", None):
            missing.append(field)
    return missing


def missing_sections(text: str) -> list[str]:
    present = {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    }
    return [section for section in REQUIRED_SECTIONS if section not in present]


def validate_note(path: Path) -> tuple[list[str], str | None]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: {exc}"], None

    missing = missing_fields(frontmatter)
    if missing:
        errors.append(f"{path}: missing frontmatter fields: {', '.join(missing)}")

    sections = missing_sections(text)
    if sections:
        errors.append(f"{path}: missing sections: {', '.join(sections)}")

    paper_id = frontmatter.get("paper_id")
    if not isinstance(paper_id, str) or not paper_id.strip():
        paper_id = None

    return errors, paper_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Level 2 *.ref.md notes.")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to validate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    notes = find_notes([Path(path) for path in args.paths])
    if not notes:
        print("error: no *.ref.md notes found", file=sys.stderr)
        return 1

    duplicate_map: dict[str, list[str]] = defaultdict(list)
    errors: list[str] = []
    for note in notes:
        note_errors, paper_id = validate_note(note)
        errors.extend(note_errors)
        if paper_id is not None:
            duplicate_map[paper_id].append(str(note))

    for paper_id, paths in duplicate_map.items():
        if len(paths) > 1:
            errors.append(f"duplicate paper_id '{paper_id}': " + ", ".join(paths))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(notes)} note(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
