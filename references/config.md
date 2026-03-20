# Optional Config File

The skill can use an optional `paper-index.config.yaml` file when the paper-library scope or research focus should be stable across sessions.

## Recommended Fields

```yaml
library_roots:
  - "/absolute/path/to/ref"
catalog_path: "/absolute/path/to/ref/catalog.jsonl"
research_focus: "anomaly detection, provenance, and security measurement for IoT and web systems"
preferred_relevance_labels:
  - "direct"
  - "adjacent"
  - "weak"
  - "irrelevant"
  - "unknown"
```

## Usage Rules

- If the user explicitly provides paths or a research focus in the current prompt, that overrides config.
- If config exists and the prompt is ambiguous, use config before guessing.
- If neither prompt nor config is enough, ask one short clarifying question only when necessary.
