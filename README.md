# agents-docs

<p align="left">
  <a href="https://github.com/Lolaplex/agents-docs/releases"><img src="https://img.shields.io/badge/version-0.43.0-blue.svg?style=flat-square" alt="Version 0.43.0"></a>
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-Standard-orange.svg?style=flat-square" alt="MCP"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://pypi.org/project/agents-docs/"><img src="https://img.shields.io/pypi/v/agents-docs.svg?style=flat-square" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg?style=flat-square" alt="License"></a>
</p>

**Local markdown docsets with header-aware BM25 search.**  
Fetch a catalog name or URL into `~/.agents/docs/`. Shared across **Cursor**, **Claude Code**, **Antigravity**, and **Zed**.

## Memory vs Docs

Docs is the historically-true tech-fact register. Memory is user/project fluid facts. Do not merge them.

- Hard tech fact (API, stack rule, model spec, platform truth) → `write_doc` / `python -m agents_docs write NAME CONTENT [CATEGORY]`.
- User prefs, project decisions, identity → agents-memory (`add_memory` / `python -m agents_memory add`).
- Append-mostly. `delete_doc` is for wrong, duplicate, or yanked sheets — not because a model is old.
- Catalog `sync` writes root docsets. It must not rewrite agent sheets under `stacks|models|apis|platforms|custom`.
- Categories: `stacks`, `models`, `apis`, `platforms`, `custom`. Do not dump READMEs into docs.

---

## Quickstart

### 1-Step Setup

```bash
pip install agents-docs && agents-docs init
```

Scaffolds `~/.agents/docs/`, autowires MCP configurations into your installed IDEs, and registers assistant skills. Docsets are fetched on `agents-docs sync <name>`, not seeded at init.

> [!TIP]
> **🤖 Agent-Driven Setup (Zero Friction):**  
> Simply tell your coding agent: **"Install and set up agents-docs for me."**  
> The agent installs the package, runs `agents-docs init`, and automatically retrieves fresh documentation whenever you ask technical stack or model pricing questions.

*Source checkouts can also be installed and managed using [vand](https://github.com/Lolaplex/vand).*

---

## Why `.agents/docs`?

Coding agents frequently hallucinate deprecated APIs (Svelte 4 vs 5 Runes, Tailwind v3 vs v4, React 19 Actions) or reference outdated LLM models and token pricing.

Traditional vector-embedding RAG solutions are bloated: they require Docker containers, hundreds of megabytes of Python dependencies (Chroma, LangChain), and slow API embedding calls that split code blocks in half.

**`agents-docs` applies the Lolaplex philosophy:**
- **Zero Vector DBs**: Header-aware markdown chunking + pure Python lexical BM25 ranking with header match boost (+6.0) and full phrase boost (+10.0).
- **Sub-10ms Search**: Instant retrieval directly from plain markdown files on disk (`~/.agents/docs/`).
- **Live AI Models Registry**: Real-time tracked context windows, benchmarks, and token pricing ($/1M) for Frontier and Open-Weights models (Claude 5/4, GPT-5/o3/o4, Gemini 3.x, DeepSeek V4/R1, Qwen 2.5 Coder).
- **Curated 21+ Framework Catalog**: 1-click sync for official `llms.txt` (TypeScript Handbook, Svelte 5, FastAPI, Tailwind v3/v4, Tauri 2, Next.js, Supabase, Hono, WXT, Netlify, Coolify, Cloudflare, Resend, React, Vite, Zod, Pydantic, shadcn/ui).
- **Deterministic Noise Pruning**: Automatically strips HTML wrappers, link noise, and cookie banners without altering code blocks or tables.
- **Universal MCP Server**: FastMCP stdio interface with auto-sync and dependency manifest inspection.

---

## Architecture & Flow

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                  DOCS & MODEL REGISTRIES                    │
 │    Official llms.txt · TypeScript Handbook · OpenRouter     │
 └──────────────────────────────┬──────────────────────────────┘
                                │  agents-docs sync <name>
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                 DETERMINISTIC NOISE PRUNER                  │
 │    Strips HTML boilerplate while preserving 100% of code    │
 └──────────────────────────────┬──────────────────────────────┘
                                │  Header-aware chunking
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                   LOCAL DOCUMENTATION STORE                 │
 │   ~/.agents/docs/ai-models/       ~/.agents/docs/svelte-5/  │
 │   ~/.agents/docs/typescript/      ~/.agents/docs/fastapi/   │
 └──────────────┬───────────────────────────────┬──────────────┘
                │                               │
                ▼                               ▼
 ┌─────────────────────────────┐ ┌─────────────────────────────┐
 │        LEXICAL BM25         │ │     MCP SERVER & CLERK      │
 │  Header Match Boost (+6.0)  │ │  search_docs · list_docsets │
 │  Sub-10ms Exact Retrieval   │ │  sync_project_docs          │
 └─────────────────────────────┘ └─────────────────────────────┘
```

---

## CLI Reference

| Command | Purpose |
|---------|---------|
| `agents-docs init` | Plug & Play setup: auto-configures MCP across all IDEs and seeds model docs |
| `agents-docs catalog` | Lists all 21+ pre-configured frameworks and model catalogs |
| `agents-docs sync <name>` | 1-click download/update of official framework documentation |
| `agents-docs sync <name> --url <URL>` | Ingests any custom `llms.txt`, `llms-full.txt`, or markdown URL |
| `agents-docs search "<query>"` | Fast BM25 search across all installed docsets |
| `agents-docs search "<query>" --docset <name>` | Scoped search within a specific documentation set |
| `agents-docs write NAME CONTENT [CATEGORY]` | Append a hard tech fact (alias: `add`). `--overwrite` replaces |
| `agents-docs prune` | In-place noise & boilerplate cleaner across all installed docs |
| `agents-docs list` | Lists all installed docsets on disk with file and byte counts |
| `agents-docs serve` | Runs the FastMCP stdio server (default) |

---

## MCP Tools Reference

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `search_docs` | `query`, `category` (default: `"all"`), `top_k` (default: `4`) | Header-aware BM25 over stacks/models/apis/platforms/custom (and catalog docsets). |
| `get_doc` | `name`, `category` | Raw markdown of one fact sheet. |
| `write_doc` | `name`, `content`, `category` (default: `"custom"`), `overwrite` (default: `false`) | Append a dated tech fact. `overwrite=true` replaces. |
| `delete_doc` | `name`, `category` | Delete a wrong/duplicate/yanked sheet. Not for old-but-still-true facts. |
| `list_docs` | `category` (default: `"all"`) | Lists fact sheets with category and size. |
| `list_catalog` | *None* | Curated framework catalog for 1-click sync. |
| `sync_external_doc` | `name`, `url` (optional) | Fetch a catalog item or custom `llms.txt` / markdown URL. |

---

## Supported Ecosystem

- **Claude Code:** Bound via MCP server and `.agents/skills/docs-search`.
- **Google Antigravity:** Integrated via `.gemini/config` rules and `agents-docs` MCP.
- **Cursor:** Automatically configures `.cursor/mcp.json` and agent rules.
- **Zed:** Configures `context_servers` and mirrors assistant skills.
- **VS Code / Windsurf:** Autowires Cline / Roo-Code MCP configuration.

---

## Open ABI Specification

Detailed architectural specifications live in [`abi/`](abi/):
- [`abi/WHY.md`](abi/WHY.md) — Architectural rationale & BM25 vs Vector embeddings.
- [`abi/LAYOUT.md`](abi/LAYOUT.md) — Storage taxonomy in `~/.agents/docs/`.
- [`abi/MCP.md`](abi/MCP.md) — Tool surface definitions and schemas.
- [`abi/CATALOG.md`](abi/CATALOG.md) — Curated catalog schema and supported types.
- [`abi/LLMSTXT.md`](abi/LLMSTXT.md) — Support for the `llms.txt` standard.

---

## Testing & Verification

Run the test suite across all engines:

```bash
python tests/run_all_tests.py
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
