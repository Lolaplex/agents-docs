# Curated catalog

The catalog is the dict in `src/agents_docs/catalog.py`. `list_catalog` and `agents-docs catalog` print it. `sync` / `sync_external_doc` fetch one name.

## Entry

```python
{
    "name": "svelte-5",
    "description": "Svelte 5 Official Documentation, Runes, and Migration Guide",
    "source_type": "llmstxt",
    "url": "https://svelte.dev/docs/llms-full.txt",
    "tags": ["frontend", "svelte", "typescript", "ui"],
    "detect": ["svelte"],
}
```

`source_type` in the catalog is `llmstxt` or `bundled` (`ai-models`, url `bundled://ai-models`). Fetch then records a finer `source_type` on `.meta.json` (`llmstxt_full`, `llmstxt_index`, `llmstxt_raw`, `direct_markdown`, `bundled`).

`detect` is a list of manifest substrings. It does not auto-sync a project. An agent calls `sync_external_doc` or `agents-docs sync` itself.

Unknown name without `--url` / `url` is an error. A custom URL bypasses the catalog.
