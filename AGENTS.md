# AGENTS.md — agents-docs Developer Guidelines

## Architecture Principles
- **Zero Heavy Dependencies**: Pure Python standard library + `mcp>=1.0.0,<2`. No vector DBs, no embeddings, no bloated HTTP frameworks.
- **Filesystem-First**: All docsets reside in `~/.agents/docs/<name>/`. Plain markdown, human-readable, editable.
- **Header-Aware BM25**: Section parsing uses `#`, `##`, `###` headers to preserve code block integrity.

## Commands
- Run test suite: `python tests/run_all_tests.py`
- Sync bundled assets: `python scripts/sync_bundled.py`
- Test CLI: `python -m agents_docs catalog`
- Start FastMCP: `python -m agents_docs serve`
