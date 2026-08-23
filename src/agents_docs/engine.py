"""
Core engine for agents-docs.
Pure Python, zero-bloat markdown parser, chunker, and BM25/keyword ranker.
"""

from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .store import DocsStore, get_default_docs_root


@dataclass
class DocSection:
    docset: str
    rel_path: str
    header: str
    level: int
    content: str
    line_number: int


class DocsEngine:
    def __init__(self, store: Optional[DocsStore] = None):
        self.store = store or DocsStore()
        self.docs_root = self.store.root

    def list_docsets(self) -> List[Dict[str, Any]]:
        """List all available documentation sets and their file/section stats."""
        return self.store.list_docsets()

    def _split_markdown_sections(self, docset: str, file_path: Path) -> List[DocSection]:
        """Split markdown file into sections by headers (#, ##, ###)."""
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return []

        docset_dir = self.store.get_docset_dir(docset)
        try:
            rel_path = str(file_path.relative_to(docset_dir)).replace("\\", "/")
        except ValueError:
            rel_path = file_path.name

        lines = text.splitlines()
        sections: List[DocSection] = []

        header_stack: List[Tuple[int, str]] = []
        current_header = file_path.stem
        current_level = 1
        current_lines: List[str] = []
        start_line = 1

        header_pattern = re.compile(r"^(#{1,6})\s+(.*)$")

        for idx, line in enumerate(lines, start=1):
            match = header_pattern.match(line)
            if match:
                if current_lines:
                    content = "\n".join(current_lines).strip()
                    if content:
                        sections.append(DocSection(
                            docset=docset,
                            rel_path=rel_path,
                            header=current_header,
                            level=current_level,
                            content=content,
                            line_number=start_line,
                        ))
                hashes, title = match.groups()
                current_level = len(hashes)
                clean_title = title.strip()

                # Maintain hierarchical breadcrumb stack
                while header_stack and header_stack[-1][0] >= current_level:
                    header_stack.pop()
                header_stack.append((current_level, clean_title))

                # Build breadcrumb (e.g. "1. Azure AI Speech > Limits & Request Constraints")
                current_header = " > ".join(t for _, t in header_stack)
                current_lines = [line]
                start_line = idx
            else:
                current_lines.append(line)

        if current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                sections.append(DocSection(
                    docset=docset,
                    rel_path=rel_path,
                    header=current_header,
                    level=current_level,
                    content=content,
                    line_number=start_line,
                ))

        return sections

    def _get_target_docsets(self, docset: str) -> List[str]:
        if docset.strip().lower() in ["all", "*"]:
            return [d["name"] for d in self.list_docsets()]
        return [docset.strip().lower()]

    def search_detailed(self, docset: str, query: str, top_k: int = 4) -> Dict[str, Any]:
        """
        Fast BM25 + Header-Boost + Term Coverage Lexical Search over markdown sections.
        Returns results along with missing query term diagnostics.
        """
        target_docsets = self._get_target_docsets(docset)
        if not target_docsets:
            return {"results": [], "missing_terms": [], "searched_docsets": []}

        all_sections: List[DocSection] = []
        for ds in target_docsets:
            ds_dir = self.store.get_docset_dir(ds)
            if not ds_dir.exists():
                continue
            md_files = list(ds_dir.rglob("*.md")) + list(ds_dir.rglob("*.mdx"))
            for mf in md_files:
                if mf.name.startswith("."):
                    continue
                all_sections.extend(self._split_markdown_sections(ds, mf))

        if not all_sections:
            return {"results": [], "missing_terms": [], "searched_docsets": target_docsets}

        # Tokenize query
        query_terms = [t.lower() for t in re.findall(r"[\w\$@\-]+", query) if len(t) > 1]
        if not query_terms:
            return {"results": [], "missing_terms": [], "searched_docsets": target_docsets}

        # Document frequencies for terms
        df: Dict[str, int] = {}
        for term in query_terms:
            count = 0
            for s in all_sections:
                if term in s.content.lower() or term in s.header.lower():
                    count += 1
            df[term] = count

        missing_terms = [term for term in query_terms if df.get(term, 0) == 0]

        total_docs = len(all_sections)
        k1 = 1.5
        b = 0.75
        doc_lengths = [len(re.findall(r"[\w\$@\-]+", s.content)) for s in all_sections]
        avg_dl = sum(doc_lengths) / max(len(doc_lengths), 1)

        scored_candidates: List[Tuple[float, DocSection, List[str]]] = []

        query_lower = query.lower()

        for s, doc_len in zip(all_sections, doc_lengths):
            text_lower = s.content.lower()
            header_lower = s.header.lower()
            score = 0.0
            matched_terms = []

            for term in query_terms:
                tf = text_lower.count(term)
                in_header = term in header_lower

                if in_header:
                    score += 6.0
                    matched_terms.append(term)
                elif tf > 0:
                    matched_terms.append(term)

                if tf > 0 or in_header:
                    effective_tf = max(tf, 1 if in_header else 0)
                    n = df.get(term, 0)
                    idf = math.log((total_docs - n + 0.5) / (n + 0.5) + 1.0)
                    denom = effective_tf + k1 * (1 - b + b * (doc_len / max(avg_dl, 1)))
                    score += idf * ((effective_tf * (k1 + 1)) / max(denom, 0.001))

            if query_lower in text_lower:
                score += 12.0
            if query_lower in header_lower:
                score += 18.0

            # Term coverage bonus (strongly rewards matching multiple distinct concepts)
            if matched_terms:
                coverage_ratio = len(set(matched_terms)) / len(query_terms)
                score *= (1.0 + 2.5 * (coverage_ratio ** 1.5))

            if score > 0.1:
                scored_candidates.append((score, s, list(set(matched_terms))))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        # Diversity-aware top_k selection: prevent a single topic from monopolizing compound queries
        selected: List[Tuple[float, DocSection, List[str]]] = []
        covered_terms_overall: set[str] = set()

        for score, s, matched in scored_candidates:
            if len(selected) >= top_k:
                break

            # If we still have slots and this candidate brings new uncovered query terms
            new_terms = set(matched) - covered_terms_overall
            is_duplicate_header = any(
                sel[1].docset == s.docset and sel[1].rel_path == s.rel_path and sel[1].header == s.header
                for sel in selected
            )

            if is_duplicate_header:
                continue

            selected.append((score, s, matched))
            covered_terms_overall.update(matched)

        # If diversity selection didn't fill top_k, fill with remaining highest scores
        if len(selected) < top_k:
            for score, s, matched in scored_candidates:
                if len(selected) >= top_k:
                    break
                if not any(sel[1] == s for sel in selected):
                    selected.append((score, s, matched))

        formatted_results = [
            {
                "docset": s.docset,
                "file": s.rel_path,
                "header": s.header,
                "line": s.line_number,
                "score": round(sc, 2),
                "matched_terms": matched,
                "snippet": s.content[:2500] + ("..." if len(s.content) > 2500 else ""),
            }
            for sc, s, matched in selected
        ]

        return {
            "results": formatted_results,
            "missing_terms": missing_terms,
            "searched_docsets": target_docsets,
        }

    def search(self, docset: str, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Fast BM25 + Header-Boost Lexical Search over markdown sections.
        Returns top matching snippets with headers and line numbers.
        """
        detailed = self.search_detailed(docset=docset, query=query, top_k=top_k)
        return detailed["results"]

    def get_page(self, docset: str, rel_path: str) -> Optional[str]:
        """Fetch the full content of a specific doc page."""
        return self.store.get_document(docset, rel_path)

    def ingest_local_folder(self, name: str, source_path: str | Path) -> Dict[str, Any]:
        """Copy a local markdown folder into the docs store."""
        import shutil
        src = Path(source_path).resolve()
        if not src.exists() or not src.is_dir():
            raise ValueError(f"Source path {src} does not exist or is not a directory.")

        target_dir = self.store.get_docset_dir(name)
        target_dir.mkdir(parents=True, exist_ok=True)

        copied = 0
        for item in src.rglob("*"):
            if item.is_file() and item.suffix.lower() in [".md", ".mdx", ".txt"]:
                rel = item.relative_to(src)
                dest = target_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                copied += 1

        self.store.save_metadata(name, {
            "source": str(src),
            "source_type": "local_folder",
            "file_count": copied,
        })

        return {
            "status": "success",
            "docset": name,
            "target": str(target_dir),
            "files_copied": copied,
        }
