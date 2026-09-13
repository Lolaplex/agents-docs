"""
FastMCP Server for agents-docs.
Technical Reference & Hard-Fact Register for AI coding agents.
Categories: stacks, models, apis, platforms, custom.
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
def search_docs(query: str, category: str = "all", top_k: int = 4) -> str:
    """
    Search hard technical facts, API specs, stack rules, model capabilities, and playbooks using header-aware BM25 ranking.
    
    Args:
        query: Keywords, function signatures, syntax, or technical questions (e.g. 'runes $state', 'HTTPException', 'coolify postgres port', 'cdp tab focus')
        category: Target category ('stacks', 'models', 'apis', 'platforms', 'custom', or specific docset name, or 'all' to search everything).
        top_k: Number of relevant sections to return (default 4).
    """
    clean_cat = category.strip().lower()
    if clean_cat != "all" and clean_cat != "*":
        _ensure_docset_fresh(clean_cat)

    search_data = engine.search_detailed(docset=clean_cat, query=query, top_k=top_k)
    results = search_data["results"]
    missing_terms = search_data.get("missing_terms", [])

    if not results:
        installed = [d["name"] for d in store.list_docs()]
        msg = f"No matching sections found in '{category}' for query: '{query}'."
        if installed:
            sample = installed[:10]
            msg += f"\nSample installed docs: {', '.join(sample)}..."
        msg += "\nTip: Run `list_docs()` to check available technical docs, or `write_doc()` to file a new hard fact."
        return msg

    formatted = []
    for r in results:
        formatted.append(
            f"### [{r['docset']}] {r['file']}#L{r['line']} — {r['header']} (Score: {r['score']})\n\n{r['snippet']}\n"
        )
    output = "\n---\n\n".join(formatted)

    if missing_terms:
        meaningful_missing = [t for t in missing_terms if len(t) > 2 and t not in {"the", "and", "for", "with", "how", "all", "get", "api", "use"}]
        if meaningful_missing:
            output += (
                f"\n---\n💡 [agents-docs notice]: No direct matches for term(s): {', '.join(meaningful_missing)} in searched docs.\n"
                f"• Check `list_docs()` or query specific category: `search_docs(query='...', category='stacks|models|apis|platforms|custom')`.\n"
            )

    return output


@mcp.tool()
def get_doc(name: str, category: str = "all") -> str:
    """
    Fetch the complete raw markdown of a technical fact sheet, spec, or playbook.
    
    Args:
        name: Name or relative path of the doc (e.g. 'tailwind-v3', 'stacks/fastapi.md', 'coolify-db', 'ai-models/pricing_and_specs.md')
        category: Optional category filter ('stacks', 'models', 'apis', 'platforms', 'custom', or 'all').
    """
    content = store.get_doc(name=name, category=category)
    if content is None:
        return f"Error: Document '{name}' not found in category '{category}'."
    return content


@mcp.tool()
def write_doc(
    name: str,
    content: str,
    category: str = "custom",
    overwrite: bool = False,
) -> str:
    """
    Append a durable technical fact (API spec, stack rule, model capability, platform note).

    Default appends a dated section. Does not clobber. Use overwrite=True only to replace a wrong sheet.
    Hard tech facts belong here. User prefs and project fluid facts belong in agents-memory, not docs.
    delete_doc is for wrong/duplicate/yanked sheets — not for an old model that is still true.

    Args:
        name: Short document identifier (e.g. 'powershell-gotchas', 'ahasend-api', 'coolify-db-ports')
        content: Markdown fact to append (or full replacement when overwrite=True)
        category: One of 'stacks' (frameworks/libs), 'models' (LLM specs), 'apis' (protocol/APIs), 'platforms' (OS/Infra/DB), 'custom'
        overwrite: False (default) appends. True replaces the entire file.
    """
    try:
        saved_path = store.save_doc(
            name=name,
            content=content,
            category=category,
            overwrite=overwrite,
        )
        return f"Saved technical doc '{name}' to {saved_path}"
    except Exception as e:
        return f"Error saving technical doc: {e}"


@mcp.tool()
def delete_doc(name: str, category: str = "custom") -> str:
    """
    Delete a technical fact sheet that is wrong, duplicate, or yanked.

    Do not delete because a fact is old. Old-but-still-true model/API notes stay.
    
    Args:
        name: Document identifier to delete
        category: Category where the doc resides ('stacks', 'models', 'apis', 'platforms', 'custom')
    """
    try:
        removed = store.delete_doc(name=name, category=category)
        if removed:
            return f"Deleted document '{name}' from '{category}'."
        return f"Document '{name}' not found in '{category}'."
    except Exception as e:
        return f"Error deleting document: {e}"


@mcp.tool()
def list_docs(category: str = "all") -> str:
    """
    List all indexed technical documents, fact sheets, API specs, and playbooks with category and size.
    
    Args:
        category: Filter by category ('stacks', 'models', 'apis', 'platforms', 'custom', or 'all')
    """
    docs = store.list_docs(category=category)
    if not docs:
        return json.dumps({
            "message": f"No documents found in category '{category}'. Use write_doc() to add technical facts.",
            "docs": [],
            "docs_root": str(store.root),
        }, indent=2)
    return json.dumps({"docs": docs, "count": len(docs), "docs_root": str(store.root)}, indent=2)


@mcp.tool()
def sync_external_doc(name: str, url: Optional[str] = None) -> str:
    """
    Fetch/synchronize an external documentation set from curated catalog or custom llms.txt URL.
    
    Args:
        name: Name of the catalog item (e.g. 'svelte-5', 'fastapi', 'tailwind-v3') or custom identifier.
        url: Optional custom URL (pointing to llms.txt, llms-full.txt, or raw markdown).
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
def list_catalog() -> str:
    """
    List curated pre-configured framework docsets available for 1-click sync.
    Includes Svelte 5, FastAPI, Next.js, Supabase, Tailwind v3/v4, Tauri 2, Hono, MCP, WXT.
    """
    entries = list_catalog_entries()
    return json.dumps({"catalog": entries, "count": len(entries)}, indent=2)


@mcp.tool()
def get_model_playbook(model: str = "auto") -> str:
    """
    Get self-awareness operational playbooks, strengths, traps, and best practices for AI models.
    Enables models to understand their own capabilities and optimize tool execution patterns.
    
    Args:
        model: Model name or family (e.g. 'gemini-3.7-flash', 'claude-3.7-sonnet', 'gpt-4o', 'deepseek-r1', 'qwen', or 'auto').
    """
    from .playbooks import resolve_model_playbook
    return resolve_model_playbook(model_query=model)


