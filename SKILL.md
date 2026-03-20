---
name: paper-index
description: Create, update, and use agent-first paper indexes when the user asks for a paper index, paper ref, literature card, structured paper note, innovation-mining note, searchable local paper library, or wants paper PDFs turned into reusable `.ref.md` files plus a `catalog.jsonl` shortlist index. Use this skill when the goal is persistent machine-readable indexing and later retrieval, not a one-off paper summary.
---

# Paper Index

## Overview

This skill teaches an agent how to build and use a local paper index in a progressive-disclosure workflow. The goal is not to imitate a human reading workflow. The goal is to let future agents answer natural-language literature questions from a local paper library with minimal reopening of PDFs.

## Index Levels

Use this naming consistently:

- Source corpus: local PDFs and other raw paper files. These are not indexes.
- Level 1 index: `catalog.jsonl`. This is the shallow shortlist layer across many papers.
- Level 2 index: per-paper `*.ref.md` notes. This is the deeper per-paper retrieval layer.

The agent should usually consult Level 1 first, then Level 2, and only then return to the source PDF if needed.

## When To Use

Use this skill when the user wants a persistent local literature index, especially for requests like:

- "构建论文索引"
- "整理成本地论文库"
- "做一个 paper ref"
- "把这篇论文整理成 agent 可读的笔记"
- "帮我检索本地论文库"
- "build a paper index for this PDF"
- "search my local paper library"

Do not use this skill when the user only wants:

- a one-off summary in chat
- translation of a small excerpt
- a quick relevance check with no persistent artifact

## Operating Modes

This skill has two modes.

### 1. Indexing Mode

Use when the user wants to ingest or refine papers.

Outputs:

- Level 2 note: `*.ref.md`
- refreshed Level 1 catalog: `catalog.jsonl`

### 2. Retrieval Mode

Use when the user wants to search, compare, shortlist, or query a local paper library.

Workflow:

1. Read `catalog.jsonl`
2. Filter likely candidates using frontmatter-level fields
3. Open only the most relevant `*.ref.md` notes
4. Return to PDFs only if the notes are insufficient

Do not skip directly to bulk-opening many notes if the catalog is available.

## Library Scope Resolution

Before indexing or retrieval, determine the paper-library scope using this priority order:

1. Paths explicitly given by the user in the prompt
2. `paper-index.config.yaml` if present in the current directory tree or target library root
3. Common paper-library directories such as `ref/`, `refs/`, `papers/`, `literature/`, or `bib/`
4. The current project root as a fallback library scope

Ask the user a brief clarifying question only when multiple plausible library roots exist and choosing the wrong one would materially change the result.

## Research Focus Resolution

`relevance_to_us` is meaningful only if "us" is defined. Determine it using this priority order:

1. Explicit user-stated research focus in the current prompt
2. `paper-index.config.yaml`
3. Current project and conversation context
4. If still unclear, set `relevance_to_us` to `unknown` rather than guessing

## Level 2 Schema

Each per-paper `*.ref.md` note must contain these frontmatter fields:

- `schema_version`
- `paper_id`
- `title`
- `local_path`
- `year`
- `venue`
- `publication_status`
- `authors`
- `keywords`
- `task_tags`
- `method_tags`
- `dataset_tags`
- `domain_tags`
- `relevance_to_us`
- `one_line_summary`
- `has_code`
- `codebase_link`
- `indexed_at`
- `source_mtime`

Use explicit missing values instead of guessing:

- `year`: `null`
- unknown strings: `""` or `unknown`, depending on the field
- unknown lists: `[]`

## Level 2 Body Design

The Level 2 note body is for deeper retrieval after catalog-level filtering. It should be concise, factual, and English-first.

Use stable sections:

- `Problem`
- `Claimed Gap`
- `Core Method`
- `Data and Evaluation`
- `Key Results`
- `Relevance to Our Work`
- `Reusable Ideas`
- `Limitations`

Prefer bullet lists and short factual statements over narrative prose. The note should answer future agent questions quickly, not mirror the paper's own section layout.

## Level 1 Catalog Design

`catalog.jsonl` is the first-stop retrieval layer. Each line should be derivable from Level 2 frontmatter and should be cheap to scan, grep, or embed. The catalog should not require reading note bodies.

Include, at minimum:

- schema and identity fields
- venue and time fields
- shortlist-level topical tags
- `relevance_to_us`
- `one_line_summary`
- `local_path`
- `ref_path`

## Language Policy

Use English for both frontmatter and body unless the user explicitly asks otherwise.

Reasons:

- source papers are usually English
- methods, datasets, venues, and metrics already have stable English names
- English reduces translation drift
- search, tagging, clustering, and embedding are easier with one dominant language

## Agent-Facing Scripts

Scripts in `scripts/` exist for the agent, not for the user. Use them when they reduce repeated work or improve reliability.

Available scripts:

- `scripts/build_ref_catalog.py`
  - scans `*.ref.md`
  - extracts Level 1 records
  - writes `catalog.jsonl`
- `scripts/validate_ref_note.py`
  - validates Level 2 notes
  - checks required frontmatter and required sections
  - can catch duplicate `paper_id` values when validating a directory

Do not tell the user how to run these scripts unless the user explicitly asks.

## Tooling and Fallbacks

This skill does not depend on a separate PDF skill. Prefer the lightest reliable local tool:

- `pdfinfo` for PDF metadata
- `pdftotext` for primary text extraction
- `rg` for section search inside extracted text
- `pdftoppm` plus `tesseract` only when OCR is necessary

## Indexing Workflow

1. Resolve the paper-library scope.
2. Resolve the relevant research focus if `relevance_to_us` matters.
3. For each target paper, create or update the Level 2 note.
4. Validate the Level 2 note.
5. Rebuild the Level 1 catalog.
6. Confirm that the catalog alone is enough to shortlist the paper later.

## Retrieval Workflow

1. Resolve the paper-library scope.
2. Look for an existing `catalog.jsonl`.
3. If the catalog is missing or obviously stale, rebuild it before broad retrieval.
4. Search the catalog first.
5. Open only the most relevant Level 2 notes.
6. Open source PDFs only when the note is insufficient for the user request.

## User Orientation

After this skill is successfully used in a session, briefly tell the user:

- how to ask for Level 2 note construction
- how to ask for Level 1 retrieval over the local paper library
- what the skill is good for

Keep this short and practical.

## References

- Schema and template: `references/format.md`
- Extraction checklist: `references/checklist.md`
- Tooling guide: `references/tooling.md`
- Optional config file: `references/config.md`
