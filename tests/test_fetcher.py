"""Tests for the DocsFetcher with mocked HTTP responses."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agents_docs.fetcher import DocsFetcher
from agents_docs.store import DocsStore


class TestDocsFetcher(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.store = DocsStore(root=self.temp_dir)
        self.fetcher = DocsFetcher(store=self.store)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("agents_docs.fetcher._http_get")
    def test_fetch_llmstxt_full(self, mock_http_get):
        sample_markdown = "# Full Docs\n\nThis is complete documentation in one file."
        mock_http_get.return_value = sample_markdown

        res = self.fetcher.fetch_llmstxt("hono", "https://hono.dev/llms-full.txt")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["files_saved"], 1)

        saved = self.store.get_document("hono", "docs.md")
        self.assertEqual(saved, sample_markdown)

    def test_fetch_bundled_docset(self):
        res = self.fetcher.fetch_llmstxt("ai-models", "bundled://ai-models")
        self.assertEqual(res["status"], "success")
        self.assertIn(res.get("type"), ["bundled", "live_api"])
        self.assertGreaterEqual(res["files_saved"], 5)

        overview = self.store.get_document("ai-models", "overview.md")
        self.assertIsNotNone(overview)
        self.assertIn("Claude", overview)


if __name__ == "__main__":
    unittest.main()
