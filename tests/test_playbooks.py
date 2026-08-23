"""Tests for model metacognition playbooks and self-awareness tools."""

import unittest
from unittest.mock import patch

from agents_docs.mcp_server import get_model_playbook
from agents_docs.playbooks import (
    PLAYBOOKS,
    detect_environment_model,
    format_all_playbooks_summary,
    format_playbook_markdown,
    match_playbook,
    resolve_model_playbook,
)


class TestPlaybooks(unittest.TestCase):
    def test_playbooks_structure(self):
        self.assertIn("gemini", PLAYBOOKS)
        self.assertIn("claude", PLAYBOOKS)
        self.assertIn("openai", PLAYBOOKS)
        self.assertIn("deepseek", PLAYBOOKS)
        self.assertIn("qwen", PLAYBOOKS)

        for key, p in PLAYBOOKS.items():
            self.assertIn("family", p)
            self.assertIn("strengths", p)
            self.assertIn("traps_and_blindspots", p)
            self.assertIn("rules_of_engagement", p)
            self.assertGreater(len(p["strengths"]), 0)
            self.assertGreater(len(p["traps_and_blindspots"]), 0)

    def test_match_playbook_direct_and_fuzzy(self):
        # Exact and alias
        self.assertEqual(match_playbook("gemini")["id"], "gemini")
        self.assertEqual(match_playbook("gemini-3.7-flash")["id"], "gemini")
        self.assertEqual(match_playbook("flash")["id"], "gemini")
        self.assertEqual(match_playbook("claude-3.7-sonnet")["id"], "claude")
        self.assertEqual(match_playbook("sonnet")["id"], "claude")
        self.assertEqual(match_playbook("gpt-4o")["id"], "openai")
        self.assertEqual(match_playbook("o3-mini")["id"], "openai")
        self.assertEqual(match_playbook("deepseek-r1")["id"], "deepseek")
        self.assertEqual(match_playbook("r1")["id"], "deepseek")
        self.assertEqual(match_playbook("qwen-2.5-coder")["id"], "qwen")

    def test_auto_detect_fallback(self):
        with patch.dict("os.environ", {"AGENTS_ACTIVE_MODEL": "gemini-3.7-flash"}):
            self.assertEqual(detect_environment_model(), "gemini-3.7-flash")
            matched = match_playbook("auto")
            self.assertIsNotNone(matched)
            self.assertEqual(matched["id"], "gemini")

    def test_resolve_model_playbook_output(self):
        out_gemini = resolve_model_playbook("gemini-3.7-flash")
        self.assertIn("Google Gemini", out_gemini)
        self.assertIn("Core Operational Strengths", out_gemini)
        self.assertIn("Known Traps & Failure Modes", out_gemini)
        self.assertIn("Whitespace", out_gemini)

        out_claude = resolve_model_playbook("claude-3.7-sonnet")
        self.assertIn("Anthropic Claude", out_claude)
        self.assertIn("Thinking runaway", out_claude)

        # Overview fallback
        with patch.dict("os.environ", {}, clear=True):
            out_all = resolve_model_playbook("auto")
            self.assertIn("AI Model Metacognition & Operational Playbooks Index", out_all)

    def test_mcp_tool_get_model_playbook(self):
        res = get_model_playbook("gemini")
        self.assertIn("Google Gemini", res)
        self.assertIn("Actionable Rules of Engagement", res)


if __name__ == "__main__":
    unittest.main()
