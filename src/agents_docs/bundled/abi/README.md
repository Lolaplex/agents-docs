# agents-docs ABI v1.0

Specification of the `agents-docs` filesystem layout, ingestion contracts, search protocols, and MCP tools.

## Documents in this ABI

- `VERSION`: ABI version identifier.
- `WHY.md`: Rationale — why pure markdown + BM25 beats bloated vector DBs for coding agents.
- `LAYOUT.md`: Structure of `~/.agents/docs/` and docset conventions.
- `MCP.md`: Live MCP tool surface.
- `CLI.md`: Live CLI. No-args default is `serve`.
- `CATALOG.md`: Curated catalog schema (`llmstxt` and `bundled`).
- `LLMSTXT.md`: `llms.txt` / `llms-full.txt` fetch.
