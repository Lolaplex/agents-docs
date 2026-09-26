# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.44.0] - 2026-09-26

### Added
- Support for uniform `docs:` locator prefix and section anchors in `get_doc` and `delete_doc` (e.g. `docs:stacks/fastapi.md#section`).
- `search_docs` results include `[docs:<docset>]` locator for clean cross-brain referencing.
- CLI `write` (alias `add`) so Cordis can shell `python -m agents_docs write NAME CONTENT [CATEGORY]`.

### Changed
- CI runs only on pull requests to `main` with strict bundled verification.
- `write_doc` / CLI `write` default to append a dated section instead of clobbering. Pass `overwrite=True` / `--overwrite` to replace a wrong sheet.
- Catalog prune and `save_document` skip/refuse the category dirs so agent sheets in `stacks|models|apis|platforms|custom` are not wiped.
- Cleaned emojis in playbooks and server notices, sanitized docstrings and example identifiers across server modules.
- `--help-json` lists subcommands including `write` / `add`.

### Removed
- GitHub Release is no longer cut automatically on `v*.*.*` tags (manual `gh release create` from CHANGELOG instead).

## [0.43.0] - 2026-09-05

### Added
- Categorized Hard-Fact register on disk: `stacks/`, `models/`, `apis/`, `platforms/`, `custom/`.
- CRUD for agents and humans: `write_doc`, `get_doc`, `delete_doc`, `list_docs`, and `sync_external_doc`.
- Category-aware BM25 plus exact keyword retrieval across the local fact sheets.

### Changed
- Role is an active technical knowledge base, not a passive framework downloader.

## [0.42.0] - 2026-08-20

### Added
- Header-aware BM25 over local markdown (no vector database); header boost for section hits.
- Curated 21+ framework catalog with one-command sync of official llms.txt and markdown handbooks.
- Live AI models registry: context windows, benchmark scores, and token pricing.
- In-place noise pruner that strips HTML wrappers and nav clutter without touching code blocks or tables.
- Multi-IDE MCP and skills autowire (Cursor, Antigravity, Claude Desktop, Zed).

[Unreleased]: https://github.com/Lolaplex/agents-docs/compare/v0.44.0...HEAD
[0.44.0]: https://github.com/Lolaplex/agents-docs/compare/v0.43.0...v0.44.0
[0.43.0]: https://github.com/Lolaplex/agents-docs/compare/v0.42.0...v0.43.0
[0.42.0]: https://github.com/Lolaplex/agents-docs/releases/tag/v0.42.0
