# Paper Index Format

Use this schema unless the user explicitly requests a different one.

## Level Naming

- Level 1 index: `catalog.jsonl`
- Level 2 index: `*.ref.md`
- Source corpus: PDFs and raw paper files

## Level 2 Frontmatter

```yaml
---
schema_version: "paper-index/v1"
paper_id: "unique-paper-id"
title: "Paper English Title"
local_path: "/absolute/path/to/paper.pdf"
year: 2026
venue: "arXiv"
publication_status: "preprint"
authors:
  - "Author One"
  - "Author Two"
keywords:
  - "keyword one"
  - "keyword two"
task_tags:
  - "task tag"
method_tags:
  - "method tag"
dataset_tags:
  - "dataset tag"
domain_tags:
  - "domain tag"
relevance_to_us: "direct | adjacent | weak | irrelevant | unknown"
one_line_summary: "One sentence for Level 1 shortlist retrieval."
has_code: true
codebase_link: "https://..."
indexed_at: "2026-03-20T10:52:50+0800"
source_mtime: "2026-03-19T19:23:31+0800"
---
```

## Frontmatter Rules

- `schema_version`: start with `paper-index/v1`
- `paper_id`: stable identifier such as arXiv id, DOI-derived id, or filename-derived id
- `title`: full English paper title
- `local_path`: absolute path to the source PDF
- `year`: integer year or `null`
- `venue`: short venue name such as `CCS`, `NDSS`, `arXiv`, `Future Internet`
- `publication_status`: prefer `journal`, `conference`, `workshop`, `preprint`, or `unknown`
- `authors`: full author list
- `keywords`: paper keywords or compact extracted topical phrases
- `task_tags`: what problem the paper solves
- `method_tags`: how it solves it
- `dataset_tags`: datasets, benchmarks, or data sources
- `domain_tags`: broader domains such as `web security`, `provenance`, `IoT`, `LLM`
- `relevance_to_us`: coarse retrieval label, not a paragraph
- `one_line_summary`: shortlist-level sentence used in the Level 1 catalog
- `has_code`: boolean
- `codebase_link`: empty string when absent
- `indexed_at`: when the Level 2 note was last updated
- `source_mtime`: modification time of the source PDF when indexing

## Title

Immediately after frontmatter, add:

```md
# Paper English Title
```

## Level 2 Body Template

```md
## Problem

- Unit of analysis:
- Task type:
- In scope:
- Out of scope:

## Claimed Gap

- Prior-work gap:
- Why existing work is insufficient:

## Core Method

- Main pipeline:
- Inputs:
- Outputs:
- Key modules or heuristics:
- Costly or fragile steps:

## Data and Evaluation

- Data sources / datasets:
- Scale:
- Benchmark or measurement:
- Metrics:
- Baselines or comparison targets:

## Key Results

- Most important numbers:
- Case studies or ablations:
- Runtime / throughput:

## Relevance to Our Work

- Relevance level:
- What is reusable:
- What is not aligned:

## Reusable Ideas

- Idea 1:
- Idea 2:

## Limitations

- Limitation 1:
- Limitation 2:
```

## Level 1 Catalog Record

Each `catalog.jsonl` line should be a JSON object derived from Level 2 frontmatter. Include:

- `schema_version`
- `paper_id`
- `title`
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
- `local_path`
- `ref_path`

## Writing Guidance

- Write in English unless the user explicitly requests another language.
- Prefer flat bullets and short factual statements.
- Preserve exact names and numbers.
- Separate paper facts from our own judgment.
- Do not restate generic background if it does not improve retrieval.
- The Level 2 note should be fast to skim by another model.
