"""Tests for CLI arguments and sub-commands."""

import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agents_docs.__main__ import main
from agents_docs.store import DocsStore


class TestCLI(unittest.TestCase):
    def test_cli_catalog(self):
        with patch("sys.argv", ["agents-docs", "catalog"]):
            code = main()
            self.assertEqual(code, 0)

    def test_cli_list(self):
        with patch("sys.argv", ["agents-docs", "list"]):
            code = main()
            self.assertEqual(code, 0)

    def test_cli_help_json_includes_write(self):
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(["--help-json"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        names = [c["name"] for c in payload.get("commands", [])]
        self.assertIn("write", names)
        self.assertIn("add", names)
        self.assertIn("search", names)

    def test_cli_write_appends(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {"AGENTS_DOCS_PATH": tmp}
            with patch.dict(os.environ, env, clear=False):
                self.assertEqual(
                    main(["write", "coolify-db", "# Postgres 18 on 5432", "platforms"]),
                    0,
                )
                self.assertEqual(
                    main(["add", "coolify-db", "host port still 5432", "platforms"]),
                    0,
                )
            store = DocsStore(root=Path(tmp))
            body = store.get_doc("coolify-db", "platforms")
            self.assertIn("Postgres 18", body)
            self.assertIn("host port still 5432", body)
            self.assertNotEqual(body.strip(), "host port still 5432")


if __name__ == "__main__":
    unittest.main()
