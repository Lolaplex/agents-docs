# AGENTS.md — agents-docs Developer Guidelines

## Architecture Principles
- **Hard-Fact & Tech Reference Register**: Objective technical facts, framework specs, model playbooks, API specs, and platform truths. Append-mostly.
- **Categorized Store**: `~/.agents/docs/` with `stacks/`, `models/`, `apis/`, `platforms/`, `custom/`.
- **Full Agent CRUD**: Agents & humans can write/edit/search/delete durable technical facts via `write_doc`, `get_doc`, `delete_doc`, `list_docs`, `search_docs`.
- **Zero Heavy Dependencies**: Pure Python standard library + `mcp>=1.0.0,<2`. No vector DBs, no heavy embeddings.
- **Header-Aware BM25**: Section parsing uses hierarchical header breadcrumbs preserving code blocks.

## Memory vs Docs
- Docs = historically-true tech facts (API, stack, model, platform). Append. `delete_doc` only for wrong/dup/yanked.
- Memory = user prefs, project decisions, fluid facts. Do not merge the two.
- Hard tech fact → `write_doc` / `python -m agents_docs write`. User fact → `add_memory`.
- Catalog `sync` writes root docsets. Never rewrite agent sheets under `stacks|models|apis|platforms|custom`.
- `write_doc` default is append (dated section). Explicit `overwrite=True` replaces.

## Commands
- Run test suite: `python tests/run_all_tests.py`
- Sync bundled assets: `python scripts/sync_bundled.py`
- Test CLI: `python -m agents_docs catalog`
- Start FastMCP: `python -m agents_docs serve`
