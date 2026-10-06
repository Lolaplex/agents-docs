<h1 align="center">.agents / docs</h1>

<p align="center">
  <a href="https://github.com/Lolaplex/agents-docs/releases"><img src="https://img.shields.io/badge/version-0.45.0-blue.svg?style=flat-square" alt="Version 0.45.0"></a>
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-Standard-orange.svg?style=flat-square" alt="MCP"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://pypi.org/project/agents-docs/"><img src="https://img.shields.io/pypi/v/agents-docs.svg?style=flat-square" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg?style=flat-square" alt="License"></a>
</p>

<p align="center">
  <strong>Local markdown docsets with header-aware BM25 search.</strong><br>
  Hard tech facts on disk. Shared across every agent that can speak MCP.
</p>

## Quickstart

```bash
pip install agents-docs && agents-docs init
```

Creates `~/.agents/docs/` (category dirs only), copies skills, and merges MCP into host configs whose directories already exist. Docsets are not seeded. Fetch one with `agents-docs sync <name>`.

> [!TIP]
> **🤖 Agent-Driven Setup:**
> Give your coding agent **this repo** (clone or URL), then tell it to **"install and set up agents-docs."**

Source checkouts can also be installed and managed with [vand](https://github.com/Lolaplex/vand).

---

## What it does

Markdown on disk is the store (`~/.agents/docs/`, override `AGENTS_DOCS_PATH`). Search is header-aware BM25 in-process. No vector database, no embeddings.

| Layer | Where | What lives there |
| --- | --- | --- |
| **Fact sheets** | `stacks/` `models/` `apis/` `platforms/` `custom/` | Append-mostly notes agents file with `write_doc` |
| **Docsets** | one folder per catalog name or ingest | Fetched `llms.txt` / markdown, or a local folder |

**Search.** `search_docs` ranks sections, not whole files. A named catalog docset is fetched when missing and refreshed when stale (7 days, `ai-models` 1 day).

**Catalog sync does not rewrite fact sheets.** `sync` / `prune` leave `stacks|models|apis|platforms|custom` alone.

**Memory is a different store.** User prefs, project decisions, and identity go to [agents-memory](https://github.com/Lolaplex/agents-memory). Do not dump READMEs or chat logs here. `delete_doc` is for a wrong, duplicate, or yanked sheet — not because a model is old.

---

## Where it runs

**Floor:** any MCP client or a terminal. `python -m agents_docs serve` is enough.

`init` autowires hosts it finds. It does not install an IDE.

| Layer | What you get | Who |
| --- | --- | --- |
| **Vault + MCP/CLI** | Full tools, or the CLI mirrors below | Any MCP host / any shell |
| **Autowire on init** | Merge `agents-docs` into the host MCP file when that config directory already exists; copy `docs-search` and `docs-sync` | Cursor, Claude Desktop, Zed (`context_servers`), Antigravity / Gemini, Windsurf, Codex, Roo, Cline. Skills land in `~/.agents/skills`, `~/.cursor/skills`, `~/.gemini/config/skills` |

**MCP without autowire:** point the host at `python -m agents_docs serve`.

---

## MCP tools

Primary surface. Agents file and search facts here.

| Tool | What it does |
| :--- | :--- |
| `search_docs` | Header-aware BM25. `category` is `all`, a fact category, or a docset name |
| `get_doc` | Raw markdown of one sheet |
| `write_doc` | Append a dated section. `overwrite=true` replaces a wrong sheet |
| `delete_doc` | Drop a wrong, duplicate, or yanked sheet. No CLI mirror |
| `list_docs` | Fact sheets with category and size |
| `list_catalog` | The 21 names `sync` can fetch with no URL |
| `sync_external_doc` | Fetch a catalog name or a custom `llms.txt` / markdown URL |
| `get_model_playbook` | Model playbook text (`model`, default `auto`) |

Eight tools. Full contract: [`abi/MCP.md`](abi/MCP.md).

---

## CLI

Ops / install / batch. Vault writes mirror MCP. Machine-readable catalog: `python -m agents_docs --help-json` (do not scrape `--help`).

| Command | Purpose |
| --- | --- |
| `agents-docs init` | Categories, skills, MCP merge. No docset download |
| `agents-docs catalog` | List the 21 catalog names |
| `agents-docs sync <name> [--url URL]` | Fetch a catalog item or a custom URL |
| `agents-docs ingest <name> <path>` | Copy a local markdown folder into the store |
| `agents-docs search "<query>" [--docset NAME] [--top N]` | BM25. CLI flag is `--docset` (MCP calls it `category`) |
| `agents-docs list` | Installed docsets with file and byte counts |
| `agents-docs write NAME CONTENT [CATEGORY]` | Append a fact. Alias: `add`. `--overwrite` replaces |
| `agents-docs playbook [model]` | Same text as `get_model_playbook` |
| `agents-docs prune` | Strip boilerplate in installed docsets |
| `agents-docs serve` | stdio MCP. Also the default when you pass no command |
| `agents-docs skills` / `sync-mcp` | Re-copy skills, or re-merge MCP, without the rest of `init` |

---

## ABI

Layout and contracts in [`abi/`](abi/):

- [`WHY.md`](abi/WHY.md) — markdown + BM25 instead of a vector database
- [`LAYOUT.md`](abi/LAYOUT.md) — `~/.agents/docs/` taxonomy
- [`MCP.md`](abi/MCP.md) — tool surface
- [`CLI.md`](abi/CLI.md) — commands
- [`CATALOG.md`](abi/CATALOG.md) — catalog schema
- [`LLMSTXT.md`](abi/LLMSTXT.md) — `llms.txt` fetch

---

## Tests

```bash
python tests/run_all_tests.py
```

---

## License

MIT. See [LICENSE](LICENSE).
