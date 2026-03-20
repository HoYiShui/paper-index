# Tooling Guide

This skill is intentionally lightweight. For most papers, local command-line tools are enough.

## Preferred Tool Chain

### 1. PDF metadata

Use:

- `pdfinfo <paper.pdf>`

Typical purpose:

- title
- page count
- author field if present

### 2. Primary text extraction

Use:

- `pdftotext <paper.pdf> -`

Typical purpose:

- abstract
- method overview
- experiment section
- conclusion

This should be the default path for born-digital PDFs.

### 3. Section search

Use:

- `rg -n "Abstract|Introduction|Method|Experiment|Conclusion|Dataset|Benchmark" <text>`

Typical purpose:

- jump to informative sections quickly
- avoid linear reading

### 4. OCR fallback

Use only when needed:

- `pdftoppm`
- `tesseract`

Typical triggers:

- scanned PDF
- image-heavy pages
- severely broken `pdftotext` output

## Agent-Facing Scripts

### `scripts/build_ref_catalog.py`

Purpose:

- scan Level 2 notes
- parse frontmatter
- emit the Level 1 `catalog.jsonl`

Use it when:

- notes were added or updated
- the catalog is missing
- retrieval needs a fresh shortlist layer

### `scripts/validate_ref_note.py`

Purpose:

- validate Level 2 notes against the expected schema and section set
- detect missing frontmatter fields
- detect missing required sections
- detect duplicate `paper_id` values when checking a directory

Use it when:

- a new note was created
- a note schema changed
- catalog generation fails or returns suspicious results

## When To Add More Scripts

Add more scripts only when the workflow becomes repetitive enough to justify them, for example:

- batch note initialization
- systematic tag normalization
- repeated OCR fallback pipelines

Do not over-automate single-paper note writing.
