"""Tests for MCP server tool endpoints."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agents_docs.mcp_server import (
    delete_doc,
    get_doc,
    get_model_playbook,
    list_catalog,
    list_docs,
    search_docs,
    sync_external_doc,
    write_doc,
)


class TestMCPServer(unittest.TestCase):
    def test_list_catalog_tool(self):
        res = list_catalog()
        data = json.loads(res)
        self.assertIn("catalog", data)
        self.assertGreaterEqual(data["count"], 5)

    def test_list_docs_tool(self):
        res = list_docs()
        data = json.loads(res)
        self.assertTrue("docs" in data or "message" in data)

    def test_search_docs_tool_empty(self):
        res = search_docs(category="non-existent-lib", query="random test query")
        self.assertIn("No matching sections found", res)

    def test_write_get_delete_doc_flow(self):
        # 1. Write doc
        res_write = write_doc(
            name="test-cdp-spec",
            content="# Chrome DevTools Protocol\n\n## Page Domain\n\nPage.enable starts page events.",
            category="apis",
        )
        self.assertIn("Saved technical doc 'test-cdp-spec'", res_write)

        # 2. Get doc
        content = get_doc(name="test-cdp-spec", category="apis")
        self.assertIn("Chrome DevTools Protocol", content)

        # 3. Search doc
        res_search = search_docs(query="Page.enable page events", category="apis")
        self.assertIn("Chrome DevTools Protocol", res_search)

        # 4. Delete doc
        res_del = delete_doc(name="test-cdp-spec", category="apis")
        self.assertIn("Deleted document 'test-cdp-spec'", res_del)

    def test_model_playbook_tool(self):
        res = get_model_playbook(model="gemini-3.7-flash")
        self.assertIn("gemini", res.lower())


if __name__ == "__main__":
    unittest.main()
