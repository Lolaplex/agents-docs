# MCP Tool Surface Specification

The `agents-docs` server exposes the following MCP tools for AI coding agents:

## 1. `list_docsets`
- **Description**: Returns all installed framework docsets with file and section counts.
- **Parameters**: None.
- **Returns**: JSON array of docset descriptors.

## 2. `search_docs`
- **Description**: Fast BM25 + header-boost search across a specific docset or across all docsets.
- **Parameters**:
  - `docset` (string): Target docset name (e.g. `'svelte-5'`, `'fastapi'`, or `'all'`).
  - `query` (string): Keywords, function names, or natural language query.
  - `top_k` (integer, optional): Maximum sections to return (default: 4).
- **Returns**: Formatted markdown snippets containing file path, line numbers, header, and code examples.

## 3. `get_doc_page`
- **Description**: Retrieves the raw content of a specific documentation file.
- **Parameters**:
  - `docset` (string): Docset name.
  - `rel_path` (string): Relative file path within the docset.
- **Returns**: Markdown content string.

## 4. `list_catalog`
- **Description**: Lists curated pre-configured framework docsets available for 1-click sync.
- **Parameters**: None.
- **Returns**: JSON object with framework names, descriptions, and source types.

## 5. `sync_docset`
- **Description**: Synchronizes or updates a docset from the curated catalog or a custom source URL.
- **Parameters**:
  - `name` (string): Name of the catalog item or custom identifier.
  - `url` (string, optional): Custom URL (`llms.txt`, GitHub repository, or raw markdown) if not using catalog name.
- **Returns**: Status and number of files/bytes synced.

## 6. `sync_project_docs`
- **Description**: Inspects project manifests (`package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`), detects frameworks, and auto-syncs official docsets.
- **Parameters**:
  - `project_path` (string): Path to project root.
- **Returns**: JSON object with detected and synced docsets.

## 7. `sync_memory_docs`
- **Description**: Scans `~/.agents/memory/PROJECTS.md` and auto-syncs matching documentation sets.
- **Parameters**: None.
- **Returns**: Status and list of synced docsets.

