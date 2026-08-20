# Filesystem Layout

All documentation sets reside under the global agent documentation directory:

`~/.agents/docs/` (Configurable via `$env:AGENTS_DOCS_PATH`)

## Directory Hierarchy

```
~/.agents/docs/
  ├── svelte-5/
  │   ├── .meta.json           # Ingestion metadata (source URL, timestamp, version)
  │   ├── overview.md
  │   ├── runes/
  │   │   ├── state.md
  │   │   └── derived.md
  │   └── ...
  ├── fastapi/
  │   ├── .meta.json
  │   ├── tutorial.md
  │   └── advanced.md
  └── tailwind-v3/
      ├── .meta.json
      └── docs.md
```

## `.meta.json` Schema

Each docset directory can optionally include `.meta.json`:

```json
{
  "name": "svelte-5",
  "source": "https://svelte.dev/docs/llms-full.txt",
  "source_type": "llmstxt",
  "updated_at": "2026-08-20T03:00:00Z",
  "version": "5.x"
}
```
