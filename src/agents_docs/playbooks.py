"""
Model Metacognition & Operational Playbooks for agents-docs.
Provides structured profiles, strengths, blindspots, failure modes, and operational
best practices for all major frontier and open-weight AI coding models.
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

PLAYBOOKS: Dict[str, Dict[str, Any]] = {
    "gemini": {
        "id": "gemini",
        "family": "Google Gemini",
        "models": ["gemini-3.7-flash", "gemini-3.7-flash-high", "gemini-2.0-flash", "gemini-3.0-pro", "gemini-2.5-pro"],
        "aliases": ["gemini", "google", "flash", "gemini-flash", "gemini-pro", "antigravity"],
        "specs": {
            "context_window": "1,048,576 to 2,097,152 tokens",
            "max_output": "65,536 tokens",
            "reasoning_modes": "Native Thinking (Dynamic / High / Low)",
            "tool_calling": "Fast parallel function calling, structured outputs",
        },
        "strengths": [
            "Ultra-low latency with high reasoning throughput — ideal for rapid multi-step tool loops.",
            "Massive 1M+ context window with near-perfect needle-in-a-haystack retrieval across whole codebases.",
            "Cost-effective execution: enables aggressive read-verify-test iterations without token anxiety.",
            "Strong multimodal reasoning for visual UI review, diagrams, and frontend inspection.",
        ],
        "traps_and_blindspots": [
            "Whitespace & indentation mismatch: Multi-line string replacements can fail if indentation isn't exact.",
            "Premature completion claims: Tendency to state a task is finished before actually running verification commands.",
            "Planning verbosity: When unconstrained, can generate overly verbose plans instead of executing immediately.",
            "Regex precision: Complex regex replacements should be verified with view_file first.",
        ],
        "rules_of_engagement": [
            "Always inspect target file lines via `view_file` before calling `replace_file_content`.",
            "Prefer single contiguous replacement chunks or small targeted edits to avoid offset drift.",
            "Always run the project's test suite or verification commands before ending the turn.",
            "Follow Caveman / dense communication style: zero fluff, direct answers, all code/symbols linked.",
        ],
    },
    "claude": {
        "id": "claude",
        "family": "Anthropic Claude",
        "models": ["claude-3.7-sonnet", "claude-3.5-sonnet", "claude-3.5-haiku", "claude-opus-4", "claude-3-opus"],
        "aliases": ["claude", "anthropic", "sonnet", "haiku", "opus", "claude-3.7", "claude-3.5"],
        "specs": {
            "context_window": "200,000 to 1,000,000 tokens",
            "max_output": "64,000 to 128,000 tokens",
            "reasoning_modes": "Extended Thinking (Budget-controllable tokens)",
            "tool_calling": "State-of-the-art tool orchestration and precise diff generation",
        },
        "strengths": [
            "World-class architectural reasoning, deep refactoring, and complex bug diagnosis.",
            "Unrivaled precision in editing existing code files without introducing subtle syntax bugs.",
            "Superb nuance in following complex multi-constraint instructions and system profiles.",
            "Premium aesthetic frontend generation (Tailwind, modern CSS, dynamic UX).",
        ],
        "traps_and_blindspots": [
            "Thinking runaway: Can spend 10k+ thinking tokens over-analyzing trivial one-line fixes.",
            "Over-cautiousness: Excessive planning and asking user confirmation for non-destructive actions.",
            "Reluctance to take bold leaps: May produce overly conservative solutions when simple rewrite is better.",
        ],
        "rules_of_engagement": [
            "Constrain reasoning depth on trivial edits; jump straight to execution.",
            "Run commands proactively — never ask the user to run something the agent can execute.",
            "Keep diffs minimal, clean, and preserve all unrelated comments and docstrings.",
            "Strictly avoid generic corporate filler phrases or recap novels.",
        ],
    },
    "openai": {
        "id": "openai",
        "family": "OpenAI GPT & Reasoning",
        "models": ["gpt-4.5", "gpt-4o", "o1", "o3-mini", "o3", "gpt-4o-mini"],
        "aliases": ["openai", "gpt", "gpt-4o", "gpt-4.5", "o1", "o3", "o3-mini", "chatgpt"],
        "specs": {
            "context_window": "128,000 to 200,000 tokens",
            "max_output": "16,384 to 100,000 tokens",
            "reasoning_modes": "Reasoning Effort (low / medium / high in o1/o3)",
            "tool_calling": "Strict JSON Schema validation & structured outputs",
        },
        "strengths": [
            "Exceptional algorithmic, mathematical, and logic problem-solving in o1/o3-mini.",
            "Strict adherence to structured JSON schemas and function calling signatures.",
            "Fast single-turn code generation with standardized syntax patterns.",
        ],
        "traps_and_blindspots": [
            "Lazy code placeholders: Tendency in GPT-4o to output `// ... existing code ...` in diffs.",
            "High token latency on full reasoning models (o1/o3) for simple file reads.",
            "Context compaction loss when conversational history grows past 64k tokens.",
        ],
        "rules_of_engagement": [
            "NEVER use placeholder comments (`// ...`) in replacements; provide complete drop-in code.",
            "For o3-mini/o1, formulate the full logical chain internally before making tool calls.",
            "Explicitly verify all types and imports before finalizing edits.",
        ],
    },
    "deepseek": {
        "id": "deepseek",
        "family": "DeepSeek Reasoning & Coder",
        "models": ["deepseek-r1", "deepseek-v3", "deepseek-coder"],
        "aliases": ["deepseek", "r1", "v3", "deepseek-r1", "deepseek-v3"],
        "specs": {
            "context_window": "64,000 to 128,000 tokens",
            "max_output": "8,192 to 64,000 tokens",
            "reasoning_modes": "Pure Reinforcement Learning Thinking Chain",
            "tool_calling": "Multi-head latent attention (MLA) with fast token streaming",
        },
        "strengths": [
            "Unbeatable intelligence-per-dollar efficiency for algorithmic analysis and math.",
            "Deep self-reflection and backtracking in reasoning traces (R1).",
            "Clean, idiomatic implementations of complex data structures and algorithms.",
        ],
        "traps_and_blindspots": [
            "Language mixing: Can spontaneously switch between Chinese, English, or German during thinking.",
            "Tool call schema formatting fragility if parameters are deeply nested.",
            "Quality degradation when context approaches maximum limit.",
        ],
        "rules_of_engagement": [
            "Always maintain pure English in reasoning chains and code comments.",
            "Keep tool payloads flat and clearly typed.",
            "Distill conversation context aggressively to avoid token boundary degradation.",
        ],
    },
    "qwen": {
        "id": "qwen",
        "family": "Qwen Coder & Open Weights",
        "models": ["qwen-2.5-coder-32b", "qwen-2.5-coder-7b", "qwen-2.5-72b"],
        "aliases": ["qwen", "qwen-coder", "qwen-2.5", "qwen-2.5-coder", "alibaba"],
        "specs": {
            "context_window": "32,768 to 131,072 tokens",
            "max_output": "8,192 tokens",
            "reasoning_modes": "Standard autoregressive code generation",
            "tool_calling": "Hermes-compatible / standard JSON function calling",
        },
        "strengths": [
            "Open-weights champion for local inference and fast code completion.",
            "Strong understanding of Python, TypeScript, Rust, and Go idiom.",
            "Zero cloud latency when running on local GPU / Ollama.",
        ],
        "traps_and_blindspots": [
            "Context window sensitivity: Performance drops beyond 32k tokens unless yarn/rope scaled.",
            "Complex multi-turn tool orchestration can lose track of prior tool outputs.",
        ],
        "rules_of_engagement": [
            "Decompose large multi-file tasks into focused, single-file units.",
            "Keep tool call arguments simple and deterministic.",
        ],
    },
}


def detect_environment_model() -> Optional[str]:
    """Inspect environment variables for active model hints."""
    env_keys = [
        "AGENTS_ACTIVE_MODEL",
        "ACTIVE_MODEL",
        "MODEL",
        "LLM_MODEL",
        "GEMINI_MODEL",
        "ANTHROPIC_MODEL",
        "OPENAI_MODEL",
        "DEFAULT_MODEL",
    ]
    for k in env_keys:
        val = os.environ.get(k)
        if val and val.strip():
            return val.strip().lower()

    # Heuristic based on available keys
    if os.environ.get("GEMINI_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
        return "gemini-3.7-flash"
    if os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("GEMINI_API_KEY"):
        return "claude-3.7-sonnet"
    if os.environ.get("OPENAI_API_KEY") and not (os.environ.get("GEMINI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")):
        return "gpt-4o"

    return None


def match_playbook(query: str) -> Optional[Dict[str, Any]]:
    """Match a user/model string to a known playbook via exact, model ID, or alias matching."""
    q = query.strip().lower()
    if not q or q in {"auto", "self", "me", "current", "whoami", "*"}:
        detected = detect_environment_model()
        if detected:
            q = detected
        else:
            return None

    # 1. Exact key match
    if q in PLAYBOOKS:
        return PLAYBOOKS[q]

    # 2. Match in aliases
    for p in PLAYBOOKS.values():
        if q in p.get("aliases", []):
            return p

    # 3. Match in model list
    for p in PLAYBOOKS.values():
        for m in p.get("models", []):
            if q == m or q in m or m in q:
                return p

    # 4. Substring / regex fuzzy search
    for p in PLAYBOOKS.values():
        for alias in p.get("aliases", []):
            if alias in q or q in alias:
                return p

    return None


def format_playbook_markdown(p: Dict[str, Any]) -> str:
    """Format a single playbook dictionary into high-signal, actionable markdown."""
    specs = p.get("specs", {})
    strengths = p.get("strengths", [])
    traps = p.get("traps_and_blindspots", [])
    rules = p.get("rules_of_engagement", [])
    models_str = ", ".join(f"`{m}`" for m in p.get("models", []))

    lines = [
        f"# Model Playbook: {p.get('family', 'AI Model')}",
        "",
        f"**Covered Models:** {models_str}  ",
        f"**Context Window:** {specs.get('context_window', 'N/A')} | **Max Output:** {specs.get('max_output', 'N/A')}  ",
        f"**Reasoning:** {specs.get('reasoning_modes', 'Standard')} | **Tool Calling:** {specs.get('tool_calling', 'Standard')}",
        "",
        "---",
        "",
        "## Core Operational Strengths",
        "",
    ]
    for s in strengths:
        lines.append(f"- **Advantage**: {s}")

    lines.extend([
        "",
        "## Known Traps & Failure Modes (Self-Correction)",
        "",
    ])
    for t in traps:
        lines.append(f"- **Watch out**: {t}")

    lines.extend([
        "",
        "## Actionable Rules of Engagement",
        "",
    ])
    for r in rules:
        lines.append(f"1. {r}")

    lines.append("")
    return "\n".join(lines)


def format_all_playbooks_summary() -> str:
    """Format a compact index of all available model playbooks."""
    lines = [
        "# AI Model Metacognition & Operational Playbooks Index",
        "",
        "To inspect detailed strengths, traps, and best practices for your model, call `get_model_playbook(model='...')`.",
        "",
        "| Family | Top Models | Core Strength | Key Trap / Watchout |",
        "|---|---|---|---|",
    ]
    for p in PLAYBOOKS.values():
        family = p["family"]
        models_sample = p["models"][0]
        strength_short = p["strengths"][0].split("—")[0].strip()
        trap_short = p["traps_and_blindspots"][0].split(":")[0].strip()
        lines.append(f"| **{family}** | `{models_sample}` | {strength_short} | {trap_short} |")

    lines.extend([
        "",
        "---",
        "",
        "💡 *Pass your model name (e.g. `get_model_playbook('gemini-3.7-flash')` or `get_model_playbook('claude')`) for the full playbook.*",
        "",
    ])
    return "\n".join(lines)


def resolve_model_playbook(model_query: str = "auto") -> str:
    """Resolve and return formatted markdown for a requested model query or auto-detection."""
    matched = match_playbook(model_query)
    if matched:
        return format_playbook_markdown(matched)

    # Fallback: if query was specific but not found
    q_clean = model_query.strip().lower()
    if q_clean and q_clean not in {"auto", "self", "me", "current", "whoami", "*"}:
        summary = format_all_playbooks_summary()
        return f"Notice: No exact playbook matched '{model_query}'. Available model playbooks:\n\n{summary}"

    # Default auto overview
    return format_all_playbooks_summary()
