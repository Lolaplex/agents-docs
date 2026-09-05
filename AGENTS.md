# AGENTS.md — agents-docs Developer Guidelines

## Architecture Principles
- **Hard-Fact & Tech Reference Register**: Objective technical facts, framework specs, model playbooks, API specs, and platform truths.
- **Categorized Store**: `~/.agents/docs/` with `stacks/`, `models/`, `apis/`, `platforms/`, `custom/`.
- **Full Agent CRUD**: Agents & humans can write/edit/search/delete durable technical facts via `write_doc`, `get_doc`, `delete_doc`, `list_docs`, `search_docs`.
- **Zero Heavy Dependencies**: Pure Python standard library + `mcp>=1.0.0,<2`. No vector DBs, no heavy embeddings.
- **Header-Aware BM25**: Section parsing uses hierarchical header breadcrumbs preserving code blocks.

## Commands
- Run test suite: `python tests/run_all_tests.py`
- Sync bundled assets: `python scripts/sync_bundled.py`
- Test CLI: `python -m agents_docs catalog`
- Start FastMCP: `python -m agents_docs serve`
