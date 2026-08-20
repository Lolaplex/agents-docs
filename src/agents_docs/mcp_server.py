"""
FastMCP Server for agents-docs.
Exposes documentation listing, searching, catalog browsing, and syncing.
Features Auto-Sync on search, Auto-Refresh, Project Dependency Syncing, and Memory Integration.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .catalog import detect_memory_docsets, detect_project_docsets, get_catalog_entry, list_catalog_entries
from .engine import DocsEngine
from .fetcher import DocsFetcher
from .store import DocsStore

mcp = FastMCP("agents-docs")
store = DocsStore()
engine = DocsEngine(store=store)
fetcher = DocsFetcher(store=store)


def _ensure_docset_fresh(name: str) -> None:
    """Auto-fetch if missing, or auto-refresh if older than 7 days."""
    cat_entry = get_catalog_entry(name)
    if not cat_entry:
        return

    canonical_name = cat_entry["name"]
    meta = store.get_metadata(canonical_name)
    docset_dir = store.get_docset_dir(canonical_name)

    needs_sync = False
    if not docset_dir.exists() or not list(docset_dir.glob("*.md")):
        needs_sync = True
    elif "updated_at" in meta:
        try:
            last_updated = datetime.fromisoformat(meta["updated_at"])
            age_days = (datetime.now(timezone.utc) - last_updated).days
            max_age = 1 if canonical_name == "ai-models" else 7
            if age_days >= max_age:
                needs_sync = True
        except Exception:
            pass

    if needs_sync:
        try:
            fetcher.fetch_llmstxt(name=canonical_name, url=cat_entry["url"])
        except Exception:
            pass


@mcp.tool()
def list_docsets() -> str:
    """
    List all indexed framework/library docsets in ~/.agents/docs/ with file stats and metadata.
    """
    docsets = store.list_docsets()
    if not docsets:
        return json.dumps({
            "message": "No docsets installed yet. Use sync_docset(name='...') or list_catalog() to install official docs.",
            "docsets": [],
            "docs_root": str(store.root),
        }, indent=2)
    return json.dumps({"docsets": docsets, "docs_root": str(store.root)}, indent=2)


@mcp.tool()
def search_docs(query: str, docset: str = "all", top_k: int = 4) -> str:
    """
    Search local documentation sets using header-aware BM25 lexical ranking.
    Auto-fetches missing catalog docsets on demand in 1 second.
    
    Args:
        query: Keywords, function signatures, or questions (e.g. '$state runes', 'HTTPException', 'glassmorphism')
        docset: Target docset name (e.g. 'svelte-5', 'fastapi', 'tailwind-v3') or 'all' to search all installed docs.
        top_k: Number of relevant sections to return (default 4).
    """
    clean_docset = docset.strip().lower()
    if clean_docset != "all" and clean_docset != "*":
        _ensure_docset_fresh(clean_docset)

    results = engine.search(docset=clean_docset, query=query, top_k=top_k)
    if not results:
        return f"No matching sections found in docset '{docset}' for query: '{query}'."

    formatted = []
    for r in results:
        formatted.append(
            f"### [{r['docset']}] {r['file']}#L{r['line']} — {r['header']} (Score: {r['score']})\n\n{r['snippet']}\n"
        )
    return "\n---\n\n".join(formatted)


@mcp.tool()
def get_doc_page(docset: str, rel_path: str) -> str:
    """
    Fetch the complete raw markdown of a specific documentation page.
    
    Args:
        docset: Name of the docset (e.g. 'svelte-5')
        rel_path: Relative path to the markdown file within the docset (e.g. 'docs.md' or 'runes/state.md')
    """
    content = store.get_document(docset=docset, rel_path=rel_path)
    if content is None:
        return f"Error: Page '{rel_path}' not found in docset '{docset}'."
    return content


@mcp.tool()
def list_catalog() -> str:
    """
    List curated pre-configured framework docsets available for 1-click sync.
    Includes Svelte 5, FastAPI, Next.js, Supabase, Tailwind v3/v4, Tauri 2, Hono, MCP, WXT.
    """
    entries = list_catalog_entries()
    return json.dumps({"catalog": entries, "count": len(entries)}, indent=2)


@mcp.tool()
def sync_docset(name: str, url: Optional[str] = None) -> str:
    """
    Synchronize or update a documentation set from the curated catalog or a custom URL.
    
    Args:
        name: Name of the catalog item (e.g. 'svelte-5', 'fastapi', 'tailwind-v3') or a custom docset identifier.
        url: Optional custom URL (pointing to llms.txt, llms-full.txt, or raw markdown) if name is not in catalog.
    """
    target_url = url
    if not target_url:
        cat_entry = get_catalog_entry(name)
        if not cat_entry:
            available = [c["name"] for c in list_catalog_entries()]
            return f"Error: '{name}' is not in the curated catalog. Available catalog items: {', '.join(available)}. Or provide an explicit 'url'."
        target_url = cat_entry["url"]

    try:
        res = fetcher.fetch_llmstxt(name=name, url=target_url)
        return json.dumps(res, indent=2)
    except Exception as e:
        return f"Failed to sync '{name}' from '{target_url}': {str(e)}"


@mcp.tool()
def sync_project_docs(project_path: str) -> str:
    """
    Inspect a project directory (package.json, requirements.txt, pyproject.toml, Cargo.toml),
    detect used frameworks/libraries, and auto-sync all matching official documentation sets.
    
    Args:
        project_path: Absolute or relative path to project root folder
    """
    detected = detect_project_docsets(project_path)
    if not detected:
        return f"No catalog-matched framework dependencies detected in '{project_path}'."

    synced_results = []
    for docset_name in detected:
        _ensure_docset_fresh(docset_name)
        synced_results.append(docset_name)

    return json.dumps({
        "status": "success",
        "project_path": project_path,
        "synced_docsets": synced_results,
    }, indent=2)


@mcp.tool()
def sync_memory_docs() -> str:
    """
    Scan local agents-memory (~/.agents/memory/PROJECTS.md & projects/*.md),
    detect all active tech stacks/frameworks, and auto-sync matching documentation sets.
    """
    detected = detect_memory_docsets()
    if not detected:
        return "No catalog-matched framework stacks found in agents-memory."

    synced_results = []
    for docset_name in detected:
        _ensure_docset_fresh(docset_name)
        synced_results.append(docset_name)

    return json.dumps({
        "status": "success",
        "source": "~/.agents/memory/",
        "synced_docsets": synced_results,
    }, indent=2)
