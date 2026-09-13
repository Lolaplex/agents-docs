"""Tests for MCP server tool endpoints."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agents_docs.engine import DocsEngine
from agents_docs.mcp_server import (
    delete_doc,
    get_doc,
    get_model_playbook,
    list_catalog,
    list_docs,
    search_docs,
    write_doc,
)
from agents_docs.store import DocsStore


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

    def test_write_doc_appends_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_store = DocsStore(root=Path(tmp))
            with patch("agents_docs.mcp_server.store", tmp_store):
                write_doc(name="coolify-db", content="# Postgres 18\nport 5432", category="platforms")
                write_doc(name="coolify-db", content="still public 5432", category="platforms")
                body = get_doc(name="coolify-db", category="platforms")
            self.assertIn("Postgres 18", body)
            self.assertIn("port 5432", body)
            self.assertIn("still public 5432", body)
            self.assertNotEqual(body.strip(), "still public 5432")

    def test_write_get_delete_doc_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_store = DocsStore(root=Path(tmp))
            tmp_engine = DocsEngine(store=tmp_store)
            with patch("agents_docs.mcp_server.store", tmp_store), patch(
                "agents_docs.mcp_server.engine", tmp_engine
            ):
                res_write = write_doc(
                    name="test-cdp-spec",
                    content="# Chrome DevTools Protocol\n\n## Page Domain\n\nPage.enable starts page events.",
                    category="apis",
                )
                self.assertIn("Saved technical doc 'test-cdp-spec'", res_write)
                content = get_doc(name="test-cdp-spec", category="apis")
                self.assertIn("Chrome DevTools Protocol", content)
                res_search = search_docs(query="Page.enable page events", category="apis")
                self.assertIn("Chrome DevTools Protocol", res_search)
                res_del = delete_doc(name="test-cdp-spec", category="apis")
                self.assertIn("Deleted document 'test-cdp-spec'", res_del)

    def test_model_playbook_tool(self):
        res = get_model_playbook(model="gemini-3.7-flash")
        self.assertIn("gemini", res.lower())


if __name__ == "__main__":
    unittest.main()
