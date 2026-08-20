"""
HTTP and Git fetchers for downloading markdown docsets.
Zero external dependencies — uses Python standard library.
"""

from __future__ import annotations

import gzip
import io
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .store import DocsStore

USER_AGENT = "agents-docs/1.0 (+https://github.com/Lolaplex/agents-docs)"


def prune_markdown(text: str) -> str:
    """
    Deterministic noise cleaner for documentation markdown.
    Removes HTML comments, script/style wrappers, and navigation breadcrumbs
    while strictly preserving code blocks, tables, and technical headers.
    """
    if not text:
        return ""

    # 1. Protect code blocks during cleaning
    code_blocks: List[str] = []

    def save_block(match: Any) -> str:
        code_blocks.append(match.group(0))
        return f"___CODE_BLOCK_{len(code_blocks)-1}___"

    protected = re.sub(r"```[\s\S]*?```", save_block, text)
    protected = re.sub(r"`[^`\n]+`", save_block, protected)

    # 2. Strip HTML comments <!-- ... -->
    cleaned = re.sub(r"<!--[\s\S]*?-->", "", protected)

    # 3. Strip noisy script, style, and svg tags
    cleaned = re.sub(r"<(script|style|svg)[\s\S]*?</\1>", "", cleaned, flags=re.IGNORECASE)

    # 4. Strip common navigation boilerplate lines
    noise_patterns = [
        r"(?i)^.*edit this page on (github|gitlab).*$",
        r"(?i)^.*(previous|next)\s+page\s*:?.*$",
        r"(?i)^.*was this page helpful\?.*$",
        r"(?i)^.*copyright\s+\d{4}.*all rights reserved.*$",
    ]
    for pat in noise_patterns:
        cleaned = re.sub(pat, "", cleaned, flags=re.MULTILINE)

    # 5. Normalize excessive blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # 6. Restore protected code blocks in a single O(N) pass
    cleaned = re.sub(r"___CODE_BLOCK_(\d+)___", lambda m: code_blocks[int(m.group(1))], cleaned)

    return cleaned.strip()


def _http_get(url: str, timeout: int = 15) -> str:
    """Fetch URL content as UTF-8 string, handling gzip compression."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/markdown, text/plain, text/html, */*",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        if resp.info().get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return data.decode("utf-8", errors="replace")


class DocsFetcher:
    def __init__(self, store: Optional[DocsStore] = None):
        self.store = store or DocsStore()

    def fetch_bundled(self, name: str) -> Dict[str, Any]:
        """Load a pre-bundled docset or live-update models from package assets/API into store."""
        if name == "ai-models":
            try:
                from .models_updater import sync_live_models_to_store
                return sync_live_models_to_store(self.store)
            except Exception:
                pass

        search_dirs = [
            Path(__file__).parent / "bundled" / "docsets" / name,
            Path(__file__).resolve().parents[2] / "docsets" / name,
        ]
        source_dir = None
        for cand in search_dirs:
            if cand.exists() and cand.is_dir():
                source_dir = cand
                break

        if not source_dir:
            raise FileNotFoundError(f"Bundled docset '{name}' not found in package assets.")

        saved_files = 0
        total_bytes = 0
        for doc_file in sorted(source_dir.rglob("*.md")):
            if doc_file.is_file():
                rel_path = doc_file.relative_to(source_dir).as_posix()
                content = doc_file.read_text(encoding="utf-8", errors="replace")
                self.store.save_document(name, rel_path, content)
                saved_files += 1
                total_bytes += len(content.encode("utf-8"))

        self.store.save_metadata(name, {
            "source": f"bundled://{name}",
            "source_type": "bundled",
            "file_count": saved_files,
        })
        return {
            "status": "success",
            "docset": name,
            "type": "bundled",
            "bytes_downloaded": total_bytes,
            "files_saved": saved_files,
        }

    def fetch_typescript_handbook(self) -> Dict[str, Any]:
        """Download complete TypeScript Handbook chapters from Microsoft repository."""
        base_url = "https://raw.githubusercontent.com/microsoft/TypeScript-New-Handbook/master/chapters"
        chapters = [
            "Basics.md",
            "Everyday Types.md",
            "Narrowing.md",
            "Object Types.md",
            "More on Functions.md",
            "Classes.md",
            "Modules.md",
            "Types from Transformation.md",
            "Type Declarations.md",
            "Understanding Errors.md",
        ]
        saved = 0
        total_bytes = 0
        for ch in chapters:
            url = f"{base_url}/{urllib.parse.quote(ch)}"
            try:
                content = _http_get(url)
                cleaned = prune_markdown(content)
                slug = ch.lower().replace(" ", "-")
                self.store.save_document("typescript", slug, cleaned)
                saved += 1
                total_bytes += len(cleaned.encode("utf-8"))
            except Exception:
                pass

        self.store.save_metadata("typescript", {
            "source": base_url,
            "source_type": "github_chapters",
            "file_count": saved,
        })
        return {
            "status": "success",
            "docset": "typescript",
            "type": "github_chapters",
            "bytes_downloaded": total_bytes,
            "files_saved": saved,
        }

    def fetch_llmstxt(self, name: str, url: str) -> Dict[str, Any]:
        """
        Fetch from an llms.txt, llms-full.txt endpoint, or bundled docset asset.
        If llms-full.txt: saves consolidated docs.md.
        If index llms.txt: parses sub-links and downloads referenced markdown files.
        """
        if url.startswith("bundled://") or url == "bundled":
            bundled_name = url.replace("bundled://", "").strip() or name
            return self.fetch_bundled(bundled_name)

        if name == "typescript":
            return self.fetch_typescript_handbook()

        raw_text = _http_get(url)
        
        # Check if it is a single consolidated file (llms-full.txt or large markdown)
        if "llms-full.txt" in url or len(raw_text.splitlines()) > 500 or "# " in raw_text[:500]:
            cleaned_text = prune_markdown(raw_text)
            self.store.save_document(name, "docs.md", cleaned_text)
            self.store.save_metadata(name, {
                "source": url,
                "source_type": "llmstxt_full",
                "file_count": 1,
            })
            return {
                "status": "success",
                "docset": name,
                "type": "llmstxt_full",
                "bytes_downloaded": len(cleaned_text.encode("utf-8")),
                "files_saved": 1,
            }

        # Otherwise parse index links
        links = self._extract_markdown_links(raw_text, base_url=url)
        if not links:
            # Fallback: save as docs.md
            cleaned_text = prune_markdown(raw_text)
            self.store.save_document(name, "docs.md", cleaned_text)
            self.store.save_metadata(name, {
                "source": url,
                "source_type": "llmstxt_raw",
                "file_count": 1,
            })
            return {
                "status": "success",
                "docset": name,
                "type": "llmstxt_raw",
                "bytes_downloaded": len(cleaned_text.encode("utf-8")),
                "files_saved": 1,
            }

        # Download up to 50 sub-pages concurrently
        saved_files = 0
        total_bytes = 0

        def download_page(item: Tuple[str, str]) -> Tuple[str, str, int]:
            title, link_url = item
            slug = re.sub(r"[^\w\-]", "_", title.strip().lower()).strip("_") or "doc"
            content = _http_get(link_url)
            cleaned = prune_markdown(content)
            return f"{slug}.md", cleaned, len(cleaned.encode("utf-8"))

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_link = {executor.submit(download_page, link): link for link in links[:50]}
            for future in as_completed(future_to_link):
                try:
                    filename, content, size = future.result()
                    self.store.save_document(name, filename, content)
                    saved_files += 1
                    total_bytes += size
                except Exception:
                    pass

        # Also save the index
        self.store.save_document(name, "_index.md", prune_markdown(raw_text))

        self.store.save_metadata(name, {
            "source": url,
            "source_type": "llmstxt_index",
            "file_count": saved_files + 1,
        })

        return {
            "status": "success",
            "docset": name,
            "type": "llmstxt_index",
            "bytes_downloaded": total_bytes,
            "files_saved": saved_files + 1,
        }

    def _extract_markdown_links(self, text: str, base_url: str) -> List[Tuple[str, str]]:
        """Extract [Title](URL) markdown links."""
        link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\s\)]+|\/[^\s\)]+)\)")
        matches = link_pattern.findall(text)
        links = []
        for title, rel_or_abs in matches:
            abs_url = urllib.parse.urljoin(base_url, rel_or_abs)
            if abs_url.endswith(".md") or abs_url.endswith(".txt") or "/docs/" in abs_url:
                links.append((title, abs_url))
        return links

    def fetch_direct_markdown(self, name: str, url: str) -> Dict[str, Any]:
        """Fetch a single raw markdown file from URL."""
        content = _http_get(url)
        cleaned = prune_markdown(content)
        self.store.save_document(name, "docs.md", cleaned)
        self.store.save_metadata(name, {
            "source": url,
            "source_type": "direct_markdown",
            "file_count": 1,
        })
        return {
            "status": "success",
            "docset": name,
            "type": "direct_markdown",
            "bytes_downloaded": len(cleaned.encode("utf-8")),
            "files_saved": 1,
        }

    def fetch_with_browser(self, name: str, url: str) -> Dict[str, Any]:
        """Fetch dynamic JS-rendered documentation using agents-browser (if available)."""
        try:
            import asyncio
            from agents_browser.cdp import CDPClient

            async def _scrape() -> str:
                client = CDPClient()
                await client.open(url)
                return await client.read_article()

            content = asyncio.run(_scrape())
            if not content or len(content.strip()) < 50:
                raise ValueError("Browser returned empty or insufficient content.")

            cleaned = prune_markdown(content)
            self.store.save_document(name, "docs.md", cleaned)
            self.store.save_metadata(name, {
                "source": url,
                "source_type": "browser_scrape",
                "file_count": 1,
            })
            return {
                "status": "success",
                "docset": name,
                "type": "browser_scrape",
                "bytes_downloaded": len(cleaned.encode("utf-8")),
                "files_saved": 1,
            }
        except ImportError:
            # Fallback to direct HTTP
            return self.fetch_llmstxt(name, url)
        except Exception as e:
            # Fallback to direct HTTP
            return self.fetch_llmstxt(name, url)
