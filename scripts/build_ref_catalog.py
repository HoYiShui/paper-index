#!/usr/bin/env python3
"""Build a Level 1 catalog from Level 2 paper index notes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


CATALOG_FIELDS = [
    "schema_version",
    "paper_id",
    "title",
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
    "local_path",
    "ref_path",
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


def first_present(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] not in ("", None):
            return data[key]
    return None


def ensure_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [value]


def note_stem(note_path: Path) -> str:
    name = note_path.name
    if name.endswith(".ref.md"):
        return name[:-7]
    return note_path.stem


def normalize_record(data: dict[str, Any], note_path: Path) -> dict[str, Any]:
    codebase_link = first_present(data, "codebase_link")
    record = {
        "schema_version": first_present(data, "schema_version") or "paper-index/v1",
        "paper_id": first_present(data, "paper_id") or note_stem(note_path),
        "title": first_present(data, "title", "name") or "",
        "year": first_present(data, "year"),
        "venue": first_present(data, "venue") or "",
        "publication_status": first_present(data, "publication_status") or "unknown",
        "authors": ensure_list(first_present(data, "authors", "author")),
        "keywords": ensure_list(first_present(data, "keywords", "key_words")),
        "task_tags": ensure_list(first_present(data, "task_tags")),
        "method_tags": ensure_list(first_present(data, "method_tags")),
        "dataset_tags": ensure_list(first_present(data, "dataset_tags")),
        "domain_tags": ensure_list(first_present(data, "domain_tags")),
        "relevance_to_us": first_present(data, "relevance_to_us") or "unknown",
        "one_line_summary": first_present(data, "one_line_summary") or "",
        "has_code": bool(first_present(data, "has_code")) or bool(codebase_link),
        "codebase_link": codebase_link or "",
        "indexed_at": first_present(data, "indexed_at") or "",
        "source_mtime": first_present(data, "source_mtime") or "",
        "local_path": first_present(data, "local_path") or "",
        "ref_path": str(note_path.resolve()),
    }
    return record


def find_notes(paths: list[Path]) -> list[Path]:
    notes: list[Path] = []
    for path in paths:
        if path.is_file() and path.name.endswith(".ref.md"):
            notes.append(path)
            continue
        if path.is_dir():
            notes.extend(sorted(p for p in path.rglob("*.ref.md") if p.is_file()))
    return sorted(set(note.resolve() for note in notes))


def validate_record(record: dict[str, Any]) -> list[str]:
    missing = []
    for field in ("schema_version", "paper_id", "title", "local_path", "ref_path"):
        value = record.get(field)
        if value in ("", None, []):
            missing.append(field)
    return missing


def build_catalog(paths: list[Path], strict: bool) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for note_path in find_notes(paths):
        text = note_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        record = normalize_record(frontmatter, note_path)
        missing = validate_record(record)
        if missing and strict:
            raise ValueError(f"{note_path}: missing required catalog fields: {', '.join(missing)}")
        records.append(record)
    return records


def write_jsonl(records: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            ordered = {field: record.get(field) for field in CATALOG_FIELDS}
            handle.write(json.dumps(ordered, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Level 1 catalog.jsonl from Level 2 *.ref.md notes.")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to scan for *.ref.md notes.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="catalog.jsonl",
        help="Output JSONL path. Default: ./catalog.jsonl",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if required catalog fields are missing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        records = build_catalog([Path(path) for path in args.paths], strict=args.strict)
        write_jsonl(records, Path(args.output))
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {len(records)} record(s) to {Path(args.output).resolve()}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
