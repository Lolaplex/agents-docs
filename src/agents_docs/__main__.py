"""CLI and FastMCP server entrypoint for agents-docs."""

from __future__ import annotations

import argparse
import json
import sys
import warnings

# Force UTF-8 on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Suppress upstream pydantic_settings forward-ref warnings
warnings.filterwarnings("ignore", message=".*IncompleteFieldDefinitionWarning.*")
warnings.filterwarnings("ignore", message=".*Field 'lifespan' has an incomplete definition.*")

from . import __version__
from .catalog import get_catalog_entry, list_catalog_entries
from .cli_help import emit_help_json
from .engine import DocsEngine
from .fetcher import DocsFetcher
from .mcp_server import mcp
from .store import DocsStore
from .sync import merge_agent_mcp, sync_bundled_docsets, sync_skills


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agents-docs",
        description="Ultra-fast, zero-bloat local markdown documentation RAG for AI coding agents.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"agents-docs {__version__}",
    )
    parser.add_argument(
        "--help-json",
        action="store_true",
        help="Emit machine-readable CLI spec as JSON and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Init sub-command
    subparsers.add_parser("init", help="Plug & Play setup: auto-configure MCP in all IDEs and sync skills")

    # Serve sub-command
    subparsers.add_parser("serve", help="Start FastMCP server via stdio")

    # List sub-command
    subparsers.add_parser("list", help="List all indexed framework docsets in ~/.agents/docs/")

    # Search sub-command
    search_p = subparsers.add_parser("search", help="Search documentation using BM25 ranking")
    search_p.add_argument("query", help="Search keywords or question")
    search_p.add_argument("--docset", default="all", help="Target docset (default: all)")
    search_p.add_argument("--top", type=int, default=3, help="Number of results (default: 3)")

    # Catalog sub-command
    subparsers.add_parser("catalog", help="List curated pre-configured framework docsets")

    # Sync sub-command
    sync_p = subparsers.add_parser("sync", help="Synchronize a docset from catalog or URL")
    sync_p.add_argument("name", help="Framework/docset name")
    sync_p.add_argument("--url", help="Custom llms.txt or markdown URL", default=None)

    # Ingest local sub-command
    ingest_p = subparsers.add_parser("ingest", help="Ingest a local folder into ~/.agents/docs/<name>")
    ingest_p.add_argument("name", help="Docset name")
    ingest_p.add_argument("path", help="Local directory path")

    # Prune sub-command
    subparsers.add_parser("prune", help="In-place prune and clean all installed docsets in ~/.agents/docs/")

    # Skills sub-command
    subparsers.add_parser("skills", help="Sync docs-search & docs-sync skills into IDE agent config")

    # Sync-MCP sub-command
    subparsers.add_parser("sync-mcp", help="Auto-inject agents-docs into Cursor, Antigravity, Claude Desktop, Zed")

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])

    if argv and argv[0] in ("version",):
        print(f"agents-docs {__version__}")
        return 0
    if argv and argv[0] in ("help",):
        argv = ["--help"]

    parser = build_parser()

    if "--help-json" in argv:
        emit_help_json(argv, parser, name="agents-docs")
        return 0

    args = parser.parse_args(argv)
    store = DocsStore()
    engine = DocsEngine(store=store)
    fetcher = DocsFetcher(store=store)

    if args.command == "init":
        print("=== Initializing agents-docs (Plug & Play) ===\n")
        synced = sync_skills()
        print(f"1. Synced {len(synced)} agent skills:")
        for s in synced:
            print(f"   * {s}")

        docsets = sync_bundled_docsets(store=store)
        print(f"\n2. Synced {len(docsets)} built-in docsets:")
        for d in docsets:
            print(f"   * {d}")

        pruned = store.prune_all_docsets()
        print(f"\n3. Pruned {pruned['files_pruned']} docs files ({round(pruned['bytes_saved']/1024, 1)} KB boilerplate cleaned).")

        mcp_res = merge_agent_mcp()
        print(f"\n4. Auto-configured MCP servers in {len(mcp_res)} IDE config files:")
        for r in mcp_res:
            print(f"   * {r}")

        print("\n[OK] Plug & Play setup complete. Reload your IDE/Agent to start using agents-docs.")
        return 0

    elif args.command == "serve" or args.command is None:
        mcp.run()
        return 0

    elif args.command == "list":
        docsets = store.list_docsets()
        print(f"Docs store root: {store.root}\n")
        if not docsets:
            print("No docsets installed yet. Install one with:")
            print("  agents-docs sync svelte-5")
            print("  agents-docs sync fastapi")
            print("  agents-docs catalog")
        else:
            for d in docsets:
                kb = round(d["total_bytes"] / 1024, 1)
                print(f" * {d['name']:<15} {d['file_count']} files ({kb} KB)")
        return 0

    elif args.command == "catalog":
        entries = list_catalog_entries()
        print(f"Curated Framework Catalog ({len(entries)} available):\n")
        for e in entries:
            tags = f"[{', '.join(e['tags'])}]"
            print(f" * {e['name']:<15} {e['description']}")
            print(f"   Tags: {tags} | URL: {e['url']}\n")
        print("Install any item with: agents-docs sync <name>")
        return 0

    elif args.command == "sync":
        name = args.name.strip().lower()
        url = args.url
        if not url:
            entry = get_catalog_entry(name)
            if not entry:
                print(f"Error: '{name}' not found in catalog. Available items:")
                for c in list_catalog_entries():
                    print(f" - {c['name']}")
                print("\nOr provide an explicit --url https://...")
                return 1
            url = entry["url"]

        print(f"Syncing '{name}' from {url} ...")
        res = fetcher.fetch_llmstxt(name=name, url=url)
        print(f"[OK] Synced successfully: {res.get('files_saved', 1)} files ({round(res.get('bytes_downloaded', 0)/1024, 1)} KB).")
        return 0

    elif args.command == "search":
        results = engine.search(docset=args.docset, query=args.query, top_k=args.top)
        if not results:
            print(f"No results found for query: '{args.query}' in docset: '{args.docset}'.")
            return 0
        for r in results:
            print(f"\n========================================================")
            print(f"[{r['docset']}] {r['file']}#L{r['line']} -- {r['header']} (Score: {r['score']})")
            print(f"========================================================")
            print(r["snippet"])
        return 0

    elif args.command == "ingest":
        res = engine.ingest_local_folder(name=args.name, source_path=args.path)
        print(f"[OK] Ingested {res['files_copied']} files into {res['target']}")
        return 0

    elif args.command == "prune":
        res = store.prune_all_docsets()
        print(f"[OK] In-place pruning complete:")
        print(f" * Files scanned/pruned: {res['files_pruned']}")
        print(f" * Size before:          {round(res['bytes_before']/1024, 1)} KB")
        print(f" * Size after:           {round(res['bytes_after']/1024, 1)} KB")
        print(f" * Boilerplate cleaned:  {round(res['bytes_saved']/1024, 1)} KB")
        return 0

    elif args.command == "skills":
        synced = sync_skills()
        print(f"Synced {len(synced)} skill files into agent customization roots.")
        return 0

    elif args.command == "sync-mcp":
        res = merge_agent_mcp()
        print(f"Configured MCP servers across {len(res)} host configs:")
        for r in res:
            print(f" * {r}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
