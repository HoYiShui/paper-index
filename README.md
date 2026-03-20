# Paper Index

[English](README.md) | [中文](README_zh.md)

`paper-index` is a portable skill directory for building and using an agent-first local paper library.

The repository root is intentionally shaped like a skill root:

- `SKILL.md`
- `agents/`
- `references/`
- `scripts/`

That makes it easy to publish, clone, inspect, and install without repackaging.

## For Humans

This skill helps an agent turn a local collection of papers into a progressive-disclosure literature index:

- Level 1 index: `catalog.jsonl`
  - a shallow shortlist index across many papers
- Level 2 index: `*.ref.md`
  - a deeper per-paper structured note

The intended workflow is:

1. build or update per-paper notes
2. rebuild the shared catalog
3. let the agent answer literature questions by reading the catalog first, then opening only the most relevant note files, and only then returning to the source PDFs if needed

In practice, this means you can ask the agent to:

- build an index for a new paper PDF
- refresh the local paper library
- search the local paper library by topic, method, dataset, or relevance
- compare related papers and surface reusable ideas

The repository is the shareable source of the skill. A user can clone it locally and then install or copy it into their own Codex or Claude Code skill directory.

## For Agents

Treat this repository root as a portable skill directory.

When using it:

1. read `SKILL.md` first
2. use `references/` only as needed
3. use `scripts/` when they reduce repeated work or improve reliability
4. follow the Level 1 / Level 2 indexing workflow defined in `SKILL.md`

Important behavior:

- prefer `catalog.jsonl` before opening many `*.ref.md` files
- prefer `*.ref.md` before reopening source PDFs
- resolve library scope and research focus before assigning `relevance_to_us`

If this skill has been successfully loaded into a local Codex or Claude Code environment, briefly tell the user:

- how to ask for index construction
- how to ask for retrieval over the local paper library
- what the skill is useful for

Keep that explanation short. The point is to orient the user, not to restate the whole repository.
