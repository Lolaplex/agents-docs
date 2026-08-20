"""Tests for MCP server tool endpoints."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agents_docs.mcp_server import list_catalog, list_docsets, search_docs, sync_project_docs


class TestMCPServer(unittest.TestCase):
    def test_list_catalog_tool(self):
        res = list_catalog()
        data = json.loads(res)
        self.assertIn("catalog", data)
        self.assertGreaterEqual(data["count"], 5)

    def test_list_docsets_tool(self):
        res = list_docsets()
        data = json.loads(res)
        self.assertTrue("docsets" in data or "message" in data)

    def test_search_docs_tool_empty(self):
        res = search_docs(docset="non-existent-lib", query="random test query")
        self.assertIn("No matching sections found", res)

    def test_sync_project_docs(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "package.json").write_text(json.dumps({"dependencies": {"svelte": "^5.0.0", "fastapi": "^0.100.0"}}), encoding="utf-8")
        
        with patch("agents_docs.mcp_server._ensure_docset_fresh") as mock_fresh:
            res = sync_project_docs(str(tmp))
            data = json.loads(res)
            self.assertEqual(data["status"], "success")
            self.assertIn("svelte-5", data["synced_docsets"])


if __name__ == "__main__":
    unittest.main()
