# Filesystem layout

Root: `~/.agents/docs/` (override `AGENTS_DOCS_PATH`).

Two kinds of trees live side by side. Catalog sync and `prune` must not rewrite the category trees.

## Fact sheets

Created on `init`. Agents file these with `write_doc` / `agents-docs write`.

```
~/.agents/docs/
  stacks/
  models/
  apis/
  platforms/
  custom/
```

One markdown file per sheet: `<category>/<stem>.md`. Default write appends a dated section. `overwrite` replaces the file.

## Docsets

One directory per catalog name, custom sync name, or `ingest` name. Not inside the five category dirs. `save_document` refuses a docset name that is a category.

```
~/.agents/docs/
  svelte-5/
    .meta.json
    docs.md
  typescript/
    .meta.json
    Basics.md
```

`llms-full.txt` and single markdown URLs land in `docs.md`. An `llms.txt` index follows its links into separate files. `ingest` copies a local folder as-is.

## `.meta.json`

Written by fetch. Readers tolerate a missing file.

```json
{
  "name": "svelte-5",
  "source": "https://svelte.dev/docs/llms-full.txt",
  "source_type": "llmstxt_full",
  "updated_at": "2026-09-26T12:00:00+00:00"
}
```

`updated_at` is ISO-8601 from the writer. `search_docs` on a catalog name refetches when the docset is missing or older than 7 days (`ai-models`: 1 day).
