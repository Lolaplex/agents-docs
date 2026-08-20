"""Tests for CLI arguments and sub-commands."""

import unittest
from unittest.mock import patch

from agents_docs.__main__ import main


class TestCLI(unittest.TestCase):
    def test_cli_catalog(self):
        with patch("sys.argv", ["agents-docs", "catalog"]):
            code = main()
            self.assertEqual(code, 0)

    def test_cli_list(self):
        with patch("sys.argv", ["agents-docs", "list"]):
            code = main()
            self.assertEqual(code, 0)

    def test_cli_help_json(self):
        with patch("sys.argv", ["agents-docs", "--help-json"]):
            code = main()
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
