"""
MCP Server implementation for agents-docs.
Exposes documentation listing, searching, and ingestion tools.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP
from .engine import DocsEngine, get_default_docs_root

mcp = FastMCP("agents-docs")
engine = DocsEngine()


@mcp.tool()
def list_docsets() -> str:
    """List all available documentation sets in ~/.agents/docs/ with file counts."""
    docsets = engine.list_docsets()
    if not docsets:
        return json.dumps({
            "message": "No docsets found. Use ingest_local_folder or add markdown folders to ~/.agents/docs/",
            "docsets": [],
            "docs_root": str(engine.docs_root),
        }, indent=2)
    return json.dumps({"docsets": docsets, "docs_root": str(engine.docs_root)}, indent=2)


@mcp.tool()
def search_docs(docset: str, query: str, top_k: int = 4) -> str:
    """
    Search a documentation set using header-aware BM25 lexical ranking.
    Returns the most relevant markdown sections and code blocks in milliseconds.
    
    Args:
        docset: Name of the docset (e.g. 'svelte-5', 'fastapi', 'tailwind-v3')
        query: Keywords or questions (e.g. '$state runes', 'dependency injection', 'glassmorphism')
        top_k: Number of relevant sections to return (default 4)
    """
    results = engine.search(docset=docset, query=query, top_k=top_k)
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
        docset: Name of the docset
        rel_path: Relative path to the markdown file within the docset
    """
    content = engine.get_page(docset=docset, rel_path=rel_path)
    if content is None:
        return f"Error: Page '{rel_path}' not found in docset '{docset}'."
    return content


@mcp.tool()
def ingest_local_folder(name: str, source_path: str) -> str:
    """
    Ingest a local folder containing markdown/mdx files into ~/.agents/docs/<name>.
    
    Args:
        name: Identifier name for the docset (e.g. 'tauri-2', 'omnus-docs')
        source_path: Absolute or relative local directory path
    """
    try:
        res = engine.ingest_local_folder(name=name, source_path=source_path)
        return json.dumps(res, indent=2)
    except Exception as e:
        return f"Ingestion failed: {str(e)}"
