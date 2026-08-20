"""Tests for the curated catalog definitions."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agents_docs.catalog import CURATED_CATALOG, detect_memory_docsets, get_catalog_entry, list_catalog_entries


class TestCatalog(unittest.TestCase):
    def test_catalog_entries_exist(self):
        entries = list_catalog_entries()
        self.assertGreaterEqual(len(entries), 8)
        names = [e["name"] for e in entries]
        self.assertIn("svelte-5", names)
        self.assertIn("fastapi", names)
        self.assertIn("tailwind-v3", names)
        self.assertIn("tauri-2", names)
        self.assertIn("ai-models", names)

    def test_get_catalog_entry(self):
        entry = get_catalog_entry("FastAPI")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["name"], "fastapi")
        self.assertTrue(entry["url"].startswith("http"))

        model_entry = get_catalog_entry("ai-models")
        self.assertIsNotNone(model_entry)
        self.assertEqual(model_entry["name"], "ai-models")
        self.assertTrue(model_entry["url"].startswith("bundled://"))

    def test_detect_memory_docsets(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "PROJECTS.md").write_text("| slug | stack |\n| --- | --- |\n| lolax | React, Tailwind v3, Vite |\n| dumbo | Svelte 5, Tauri 2 |\n", encoding="utf-8")
        
        with patch("agents_docs.catalog.get_memory_root", return_value=tmp):
            detected = detect_memory_docsets()
            self.assertIn("svelte-5", detected)
            self.assertIn("tauri-2", detected)
            self.assertIn("tailwind-v3", detected)


if __name__ == "__main__":
    unittest.main()
