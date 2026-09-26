# CLI

Installed command: `agents-docs`. Machine-readable catalog: `python -m agents_docs --help-json`.

No subcommand starts the stdio MCP server (`serve`).

## Subcommands

- `agents-docs init` — create `~/.agents/docs/` and the five category dirs, copy `docs-search` and `docs-sync`, prune installed docsets, merge MCP where the host config directory already exists. Does not download a catalog docset.
- `agents-docs catalog` — print the curated names.
- `agents-docs sync <name> [--url URL]` — fetch a catalog item or a custom `llms.txt` / markdown URL. Refuses to write into a category dir.
- `agents-docs ingest <name> <path>` — copy a local markdown folder into `~/.agents/docs/<name>/`.
- `agents-docs search "<query>" [--docset NAME] [--top N]` — header-aware BM25. `--docset` defaults to `all`. `--top` defaults to 3. MCP `search_docs` calls this `category` and defaults `top_k` to 4.
- `agents-docs list` — docset directories with file and byte counts. Not the fact-sheet list (`list_docs` is MCP-only).
- `agents-docs write NAME CONTENT [CATEGORY]` — append a dated fact. Alias: `add`. Category defaults to `custom`. `--overwrite` replaces the file.
- `agents-docs playbook [model]` — same text as MCP `get_model_playbook`. Default model `auto`.
- `agents-docs prune` — strip boilerplate in docsets. Skips category sheets.
- `agents-docs serve` — FastMCP stdio.
- `agents-docs skills` — copy skills again.
- `agents-docs sync-mcp` — merge MCP config again.

`delete_doc` has no CLI mirror.
