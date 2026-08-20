"""
Filesystem storage manager for agents-docs.
Manages ~/.agents/docs/ directory hierarchy and docset metadata.
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def get_default_docs_root() -> Path:
    """Returns the root directory where all markdown docsets are stored."""
    override = os.getenv("AGENTS_DOCS_PATH")
    if override:
        return Path(override)
    return Path.home() / ".agents" / "docs"


class DocsStore:
    def __init__(self, root: Optional[Path] = None):
        self.root = (root or get_default_docs_root()).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def get_docset_dir(self, name: str) -> Path:
        """Returns the directory path for a named docset."""
        clean_name = name.strip().lower().replace(" ", "-")
        return self.root / clean_name

    def list_docsets(self) -> List[Dict[str, Any]]:
        """List all docsets in the store with file stats and metadata."""
        if not self.root.exists():
            return []

        docsets = []
        for item in sorted(self.root.iterdir()):
            if item.is_dir() and not item.name.startswith("."):
                files = list(item.rglob("*.md")) + list(item.rglob("*.mdx"))
                meta = self.get_metadata(item.name)
                total_bytes = sum(f.stat().st_size for f in files if f.is_file())
                docsets.append({
                    "name": item.name,
                    "path": str(item),
                    "file_count": len(files),
                    "total_bytes": total_bytes,
                    "metadata": meta,
                })
        return docsets

    def get_metadata(self, name: str) -> Dict[str, Any]:
        """Read .meta.json for a docset if present."""
        meta_file = self.get_docset_dir(name) / ".meta.json"
        if meta_file.exists():
            try:
                return json.loads(meta_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

    def save_metadata(self, name: str, data: Dict[str, Any]) -> None:
        """Save metadata dictionary to .meta.json."""
        target_dir = self.get_docset_dir(name)
        target_dir.mkdir(parents=True, exist_ok=True)
        meta_file = target_dir / ".meta.json"
        payload = {
            "name": name,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            **data,
        }
        meta_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def save_document(self, docset: str, rel_path: str, content: str) -> Path:
        """Save a single markdown document within a docset."""
        target_file = self.get_docset_dir(docset) / rel_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")
        return target_file

    def get_document(self, docset: str, rel_path: str) -> Optional[str]:
        """Fetch the contents of a specific document within a docset."""
        base_dir = self.get_docset_dir(docset).resolve()
        target_file = (base_dir / rel_path).resolve()
        if not str(target_file).startswith(str(base_dir)):
            return None  # Path traversal protection
        if not target_file.exists() or not target_file.is_file():
            return None
        return target_file.read_text(encoding="utf-8", errors="replace")

    def prune_all_docsets(self) -> Dict[str, Any]:
        """In-place prune all markdown files in the store to eliminate boilerplate noise."""
        from .fetcher import prune_markdown

        files_pruned = 0
        bytes_before = 0
        bytes_after = 0

        for item in sorted(self.root.iterdir()):
            if item.is_dir() and not item.name.startswith("."):
                for doc_file in item.rglob("*.md"):
                    if doc_file.is_file():
                        try:
                            content = doc_file.read_text(encoding="utf-8", errors="replace")
                            b_len = len(content.encode("utf-8"))
                            bytes_before += b_len
                            cleaned = prune_markdown(content)
                            a_len = len(cleaned.encode("utf-8"))
                            bytes_after += a_len
                            if cleaned != content:
                                doc_file.write_text(cleaned, encoding="utf-8")
                            files_pruned += 1
                        except Exception:
                            pass

        return {
            "status": "success",
            "files_pruned": files_pruned,
            "bytes_before": bytes_before,
            "bytes_after": bytes_after,
            "bytes_saved": max(0, bytes_before - bytes_after),
        }

    def delete_docset(self, name: str) -> bool:
        """Remove a docset directory entirely."""
        target_dir = self.get_docset_dir(name)
        if target_dir.exists() and target_dir.is_dir():
            shutil.rmtree(target_dir, ignore_errors=True)
            return True
        return False
