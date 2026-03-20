# Paper Index Extraction Checklist

Use this checklist while building or updating a Level 2 paper index note.

## Scope and Context

- What is the paper-library root for this task?
- Is the user asking for indexing mode or retrieval mode?
- Is the current research focus explicit enough to assign `relevance_to_us`?

## Level 2 Frontmatter

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

## Problem

- What exact problem is being solved?
- What is the unit of analysis?
- Is it detection, tracing, measurement, classification, ranking, generation, or something else?
- What is explicitly out of scope?

## Claimed Gap

- What prior-work gap do the authors claim?
- Is the gap about scale, cost, coverage, latency, explainability, labeling, deployment, or evaluation?
- Is the gap technically meaningful or mostly positioning?

## Core Method

- What is the main pipeline?
- What are the inputs and outputs?
- Which parts are heuristic, learned, hybrid, or manually curated?
- What external tools, APIs, renderers, OCR engines, or parsers are used?
- Which steps are likely expensive or fragile?

## Data and Evaluation

- Dataset or data-source names
- Scale and collection window
- Public versus private data
- Benchmark versus measurement study
- Metrics and confidence intervals
- Baselines or comparison targets
- Runtime or throughput

## Key Results

- Strongest numbers
- Most reusable findings
- Important failure modes
- Longitudinal or robustness results
- Ablations, if any

## Relevance and Reuse

- How directly does this relate to our research?
- Which parts are reusable: task framing, data source, heuristic, evaluation setup, or writing angle?
- What could be turned into a better follow-up project?

## Level 1 Readiness

Before finishing the note, confirm that its frontmatter alone is enough to support shortlist-level retrieval:

- Can another agent infer the paper topic from `task_tags`, `method_tags`, and `one_line_summary`?
- Is `relevance_to_us` defensible?
- Is the note identifiable and traceable from `paper_id`, `local_path`, and `title`?

## Final Sanity Check

A future agent should be able to answer all of the following without reopening the PDF unless absolutely necessary:

- What problem does the paper solve?
- What did the method actually do?
- What are the most important numbers?
- Is it relevant to our work?
- What follow-up ideas are worth keeping?
