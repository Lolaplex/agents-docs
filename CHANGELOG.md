# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
- GitHub Release is no longer cut automatically on `v*.*.*` tags (manual `gh release create` from CHANGELOG instead).

## [0.43.0] - 2026-09-05

### Added
- Categorized Technical Reference & Hard-Fact Register structure (`stacks/`, `models/`, `apis/`, `platforms/`, `custom/`).
- Full CRUD tools for agents and humans: `write_doc`, `get_doc`, `delete_doc`, `list_docs`, and `sync_external_doc`.
- Category-aware BM25 and exact keyword retrieval across all technical documentation and fact sheets.

### Changed
- Reworked `agents-docs` role from passive framework downloader to durable, active Hard-Fact Knowledge Base.
- Streamlined `mcp_server.py` and updated test suites.

## [0.42.0] - 2026-03-20

### Added
- Curated framework catalog with 20+ framework entries.
- BM25 header-aware search engine.
- AI models pricing, specs, and playbooks integration.
