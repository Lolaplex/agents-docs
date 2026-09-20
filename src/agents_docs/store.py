"""
Filesystem storage manager for agents-docs.
Manages ~/.agents/docs/ directory hierarchy (stacks/, models/, apis/, platforms/, custom/)
and technical reference fact sheets.
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_CATEGORIES = ("stacks", "models", "apis", "platforms", "custom")


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
        self._ensure_categories()

    def _ensure_categories(self) -> None:
        """Ensure standard category directories exist."""
        for cat in DEFAULT_CATEGORIES:
            (self.root / cat).mkdir(parents=True, exist_ok=True)

    def _clean_stem(self, name: str) -> str:
        clean = name.strip()
        if clean.startswith("docs:"):
            clean = clean[len("docs:") :].strip()
        if "#" in clean:
            clean = clean.split("#")[0].strip()
        clean = clean.replace("\\", "/").strip("/")
        if clean.lower().endswith(".md"):
            clean = clean[:-3]
        elif clean.lower().endswith(".mdx"):
            clean = clean[:-4]
        return clean.lower().replace(" ", "-")

    def get_docset_dir(self, name: str) -> Path:
        """Root-level catalog/legacy dir. Never resolves into category folders."""
        clean_name = name.strip().lower().replace(" ", "-")
        return self.root / clean_name

    def save_doc(
        self,
        name: str,
        content: str,
        category: str = "custom",
        overwrite: bool = False,
    ) -> Path:
        """
        Write a technical markdown fact-sheet.
        Default: append a dated section if the file exists. overwrite=True replaces.
        """
        clean_cat = category.strip().lower() if category.strip() else "custom"
        if clean_cat not in DEFAULT_CATEGORIES:
            clean_cat = "custom"

        cat_dir = self.root / clean_cat
        cat_dir.mkdir(parents=True, exist_ok=True)

        stem = self._clean_stem(name)
        target_file = cat_dir / f"{stem}.md"
        body = content if content.endswith("\n") else content + "\n"

        if target_file.exists() and not overwrite:
            existing = target_file.read_text(encoding="utf-8")
            stamp = datetime.now(timezone.utc).date().isoformat()
            block = f"\n## {stamp}\n\n{body}"
            target_file.write_text(existing.rstrip() + "\n" + block, encoding="utf-8")
            return target_file

        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(body, encoding="utf-8")
        return target_file

    def get_doc(self, name: str, category: str = "all") -> Optional[str]:
        """
        Retrieve markdown content of a fact sheet by name or relative path.
        """
        clean_name = name.strip()
        if clean_name.startswith("docs:"):
            clean_name = clean_name[len("docs:") :].strip()
        if "#" in clean_name:
            clean_name = clean_name.split("#")[0].strip()
        stem = self._clean_stem(clean_name)
        clean_cat = category.strip().lower()

        # 1. Direct path lookup if name contains category/slash
        if "/" in clean_name or "\\" in clean_name:
            direct_path = (self.root / clean_name).resolve()
            if not str(direct_path).startswith(str(self.root)):
                return None  # traversal protection
            if direct_path.is_file():
                return direct_path.read_text(encoding="utf-8", errors="replace")
            if (direct_path.with_suffix(".md")).is_file():
                return (direct_path.with_suffix(".md")).read_text(encoding="utf-8", errors="replace")

        # 2. Specific category lookup
        if clean_cat in DEFAULT_CATEGORIES:
            cat_file = self.root / clean_cat / f"{stem}.md"
            if cat_file.is_file():
                return cat_file.read_text(encoding="utf-8", errors="replace")
            # Subdirectory check (e.g. stacks/tailwind-v3/docs.md)
            cat_sub = self.root / clean_cat / stem
            if cat_sub.is_dir():
                for md in sorted(cat_sub.glob("*.md")):
                    return md.read_text(encoding="utf-8", errors="replace")

        # 3. Search across all categories and root
        for cat in DEFAULT_CATEGORIES:
            cat_file = self.root / cat / f"{stem}.md"
            if cat_file.is_file():
                return cat_file.read_text(encoding="utf-8", errors="replace")
            cat_sub = self.root / cat / stem
            if cat_sub.is_dir():
                for md in sorted(cat_sub.glob("*.md")):
                    return md.read_text(encoding="utf-8", errors="replace")

        # 4. Legacy root-level docsets check (e.g. ~/.agents/docs/ai-models/)
        root_target = self.root / stem
        if root_target.is_dir():
            for md in sorted(root_target.glob("*.md")):
                return md.read_text(encoding="utf-8", errors="replace")
        elif (self.root / f"{stem}.md").is_file():
            return (self.root / f"{stem}.md").read_text(encoding="utf-8", errors="replace")

        return None

    def delete_doc(self, name: str, category: str = "custom") -> bool:
        """
        Delete a technical fact sheet or docset.
        """
        stem = self._clean_stem(name)
        clean_cat = category.strip().lower()

        # Check in specified category
        if clean_cat in DEFAULT_CATEGORIES:
            cat_file = self.root / clean_cat / f"{stem}.md"
            if cat_file.is_file():
                cat_file.unlink()
                return True
            cat_sub = self.root / clean_cat / stem
            if cat_sub.is_dir():
                shutil.rmtree(cat_sub, ignore_errors=True)
                return True

        # Check across all categories
        for cat in DEFAULT_CATEGORIES:
            cat_file = self.root / cat / f"{stem}.md"
            if cat_file.is_file():
                cat_file.unlink()
                return True
            cat_sub = self.root / cat / stem
            if cat_sub.is_dir():
                shutil.rmtree(cat_sub, ignore_errors=True)
                return True

        # Check root legacy
        root_dir = self.root / stem
        if root_dir.is_dir() and stem not in DEFAULT_CATEGORIES:
            shutil.rmtree(root_dir, ignore_errors=True)
            return True

        return False

    def list_docs(self, category: str = "all") -> List[Dict[str, Any]]:
        """
        List all registered technical docs, fact sheets, and specs categorized.
        """
        clean_cat = category.strip().lower()
        items = []

        categories_to_check = (
            [clean_cat] if clean_cat in DEFAULT_CATEGORIES else list(DEFAULT_CATEGORIES)
        )

        for cat in categories_to_check:
            cat_dir = self.root / cat
            if not cat_dir.exists():
                continue
            for p in sorted(cat_dir.rglob("*.md")):
                if p.is_file() and not p.name.startswith("."):
                    rel = str(p.relative_to(self.root)).replace("\\", "/")
                    stat = p.stat()
                    items.append({
                        "name": p.stem,
                        "category": cat,
                        "rel_path": rel,
                        "size_bytes": stat.st_size,
                        "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    })

        # If checking 'all', also check legacy root docsets not inside standard categories
        if clean_cat in ["all", "*"]:
            for item in sorted(self.root.iterdir()):
                if item.is_dir() and item.name not in DEFAULT_CATEGORIES and not item.name.startswith("."):
                    for p in sorted(item.rglob("*.md")):
                        if p.is_file() and not p.name.startswith("."):
                            rel = str(p.relative_to(self.root)).replace("\\", "/")
                            stat = p.stat()
                            items.append({
                                "name": f"{item.name}/{p.stem}",
                                "category": "legacy",
                                "rel_path": rel,
                                "size_bytes": stat.st_size,
                                "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                            })

        return items

    def list_docsets(self) -> List[Dict[str, Any]]:
        """List all docsets in the store with file stats and metadata."""
        if not self.root.exists():
            return []

        docsets = []
        # Categories as docsets
        for cat in DEFAULT_CATEGORIES:
            cat_dir = self.root / cat
            if cat_dir.is_dir():
                files = list(cat_dir.rglob("*.md")) + list(cat_dir.rglob("*.mdx"))
                if files:
                    total_bytes = sum(f.stat().st_size for f in files if f.is_file())
                    docsets.append({
                        "name": cat,
                        "path": str(cat_dir),
                        "file_count": len(files),
                        "total_bytes": total_bytes,
                        "metadata": {"type": "category"},
                    })

        # Legacy root items
        for item in sorted(self.root.iterdir()):
            if item.is_dir() and item.name not in DEFAULT_CATEGORIES and not item.name.startswith("."):
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
        """Save a catalog/legacy page at store root. Refuses category names."""
        clean = docset.strip().lower().replace(" ", "-")
        if clean in DEFAULT_CATEGORIES:
            raise ValueError(
                f"Refusing catalog write into category '{clean}'. "
                "Agent sheets live in stacks|models|apis|platforms|custom."
            )
        target_file = self.root / clean / rel_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")
        return target_file

    def get_document(self, docset: str, rel_path: str) -> Optional[str]:
        """Fetch the contents of a specific document within a docset (legacy compatibility)."""
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

        for item in sorted(self.root.rglob("*.md")):
            if not item.is_file() or item.name.startswith("."):
                continue
            try:
                rel = item.relative_to(self.root)
            except ValueError:
                continue
            if rel.parts and rel.parts[0] in DEFAULT_CATEGORIES:
                continue
            try:
                content = item.read_text(encoding="utf-8", errors="replace")
                b_len = len(content.encode("utf-8"))
                bytes_before += b_len
                cleaned = prune_markdown(content)
                a_len = len(cleaned.encode("utf-8"))
                bytes_after += a_len
                if cleaned != content:
                    item.write_text(cleaned, encoding="utf-8")
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

