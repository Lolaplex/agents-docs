"""Tests for DocsStore filesystem interactions."""

import shutil
import tempfile
import unittest
from pathlib import Path

from agents_docs.store import DocsStore


class TestDocsStore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.store = DocsStore(root=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_get_document(self):
        saved = self.store.save_document("test-lib", "index.md", "# Welcome to test-lib")
        self.assertTrue(saved.exists())
        content = self.store.get_document("test-lib", "index.md")
        self.assertEqual(content, "# Welcome to test-lib")

    def test_list_docsets(self):
        self.store.save_document("svelte-5", "overview.md", "# Svelte 5 Overview")
        self.store.save_document("fastapi", "guide.md", "# FastAPI Guide")
        docsets = self.store.list_docsets()
        self.assertEqual(len(docsets), 2)
        names = [d["name"] for d in docsets]
        self.assertIn("svelte-5", names)
        self.assertIn("fastapi", names)

    def test_metadata_persistence(self):
        self.store.save_metadata("tauri-2", {"version": "2.0", "source": "https://v2.tauri.app"})
        meta = self.store.get_metadata("tauri-2")
        self.assertEqual(meta.get("version"), "2.0")
        self.assertEqual(meta.get("source"), "https://v2.tauri.app")

    def test_delete_docset(self):
        self.store.save_document("temp-lib", "a.md", "content")
        self.assertTrue(self.store.delete_docset("temp-lib"))
        self.assertFalse(self.store.get_docset_dir("temp-lib").exists())

    def test_category_save_get_list_delete(self):
        # 1. Save doc in category stacks
        saved = self.store.save_doc("tailwind-v3", "# Tailwind v3 rules", category="stacks")
        self.assertTrue(saved.exists())
        self.assertEqual(saved.name, "tailwind-v3.md")

        # 2. Get doc
        doc = self.store.get_doc("tailwind-v3", category="stacks")
        self.assertEqual(doc, "# Tailwind v3 rules")

        # 3. Get doc across all categories
        doc_all = self.store.get_doc("tailwind-v3")
        self.assertEqual(doc_all, "# Tailwind v3 rules")

        # 4. List docs
        docs = self.store.list_docs(category="stacks")
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["name"], "tailwind-v3")
        self.assertEqual(docs[0]["category"], "stacks")

        # 5. Delete doc
        self.assertTrue(self.store.delete_doc("tailwind-v3", category="stacks"))
        self.assertIsNone(self.store.get_doc("tailwind-v3"))


if __name__ == "__main__":
    unittest.main()
