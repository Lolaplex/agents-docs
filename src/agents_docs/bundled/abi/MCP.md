# MCP surface

The Python server in this repository (`python -m agents_docs serve`, FastMCP) is the live tool list. `src/agents_docs/server.py` is not mounted.

## Tools

### `search_docs(query, category="all", top_k=4)`

Header-aware BM25 over fact sheets and docsets.

- `category`: `all`, one of `stacks|models|apis|platforms|custom`, or a docset name (`svelte-5`, `ai-models`, …).
- A catalog docset is fetched when missing and refreshed when stale (7 days; `ai-models` 1 day).

Returns markdown sections with a `docs:<docset>` locator, file, line, and header.

### `get_doc(name, category="all")`

Raw markdown of one sheet. `name` may be a stem, `category/file.md`, or a `docs:` locator with an optional `#section` anchor.

### `write_doc(name, content, category="custom", overwrite=false)`

Append a dated section. `overwrite=true` replaces the file. Hard tech facts only. User and project fluid facts belong in agents-memory.

### `delete_doc(name, category="custom")`

Delete a wrong, duplicate, or yanked sheet. Not for an old fact that is still true. No CLI mirror.

### `list_docs(category="all")`

JSON list of fact sheets with category and size. This is not `agents-docs list` (that command counts docset files).

### `list_catalog()`

JSON catalog: 21 names, descriptions, source URLs. Fetch with `sync_external_doc` or `agents-docs sync`.

### `sync_external_doc(name, url=None)`

Fetch a catalog item or a custom `llms.txt` / markdown URL into `~/.agents/docs/<name>/`. Does not rewrite category fact sheets.

### `get_model_playbook(model="auto")`

Operational playbook for a model name or family. CLI mirror: `agents-docs playbook`.
