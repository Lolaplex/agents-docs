# Curated Catalog Specification

The built-in catalog provides zero-effort access to official documentation for standard modern developer stacks.

## Catalog Schema

Each catalog item definition in `catalog.py`:

```python
{
    "name": "svelte-5",
    "description": "Svelte 5 Official Documentation & Runes Guide",
    "source_type": "llmstxt" | "github" | "markdown_url",
    "url": "https://svelte.dev/docs/llms-full.txt",
    "tags": ["frontend", "svelte", "javascript", "typescript"]
}
```

## Supported Source Types
1. `llmstxt`: Single or multi-file `llms.txt` or `llms-full.txt` endpoints.
2. `github`: GitHub repository docs folder or raw markdown release.
3. `markdown_url`: Direct link to an aggregated markdown resource.
