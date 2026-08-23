# AI Models: Metacognition, Operational Playbooks & Self-Correction Guide

Comprehensive self-awareness guide for AI coding assistants. Details strengths, blindspots, and failure modes across model families.

---

## Google Gemini Family (Gemini 3.7 Flash, 2.0 Flash, 3.0 Pro)

- **Context & Output**: 1,048,576 to 2,097,152 tokens context window | 65,536 max output tokens.
- **Reasoning**: Native Thinking with dynamic / high / low budgets.
- **Core Strengths**:
  - Ultra-low latency tool orchestration and rapid multi-step loops.
  - 1M+ context window with needle-in-haystack retrieval across entire repositories.
  - Highly cost-effective for aggressive test-and-verify loops.
  - Native multimodal analysis for visual UIs and diagrams.
- **Known Traps & Blindspots**:
  - *Whitespace / Indent Sensitivity*: Exact-match multi-line replacements can fail if indentation is off by spaces. Always use `view_file` before `replace_file_content`.
  - *Premature Completion*: Tendency to say "I have completed the task" before running verification tests. Always run the actual test command.
  - *Verbosity*: May emit lengthy explanations when not constrained by Caveman mode.
- **Actionable Best Practice**:
  - Inspect lines with `view_file` first.
  - Use single contiguous replacement blocks or small chunks.
  - Verify every change with real execution commands.

---

## Anthropic Claude Family (Claude 3.7 Sonnet, 3.5 Sonnet, Opus)

- **Context & Output**: 200,000 to 1,000,000 tokens context window | 64,000 to 128,000 max output tokens.
- **Reasoning**: Extended Thinking with controllable token budget.
- **Core Strengths**:
  - World-class architectural reasoning, deep refactoring, and complex bug diagnosis.
  - Unrivaled precision in editing existing code files without introducing subtle syntax bugs.
  - Superb nuance in following complex multi-constraint instructions and system profiles.
  - Premium aesthetic frontend generation (Tailwind, modern CSS, dynamic UX).
- **Known Traps & Blindspots**:
  - *Thinking Runaway*: Can spend 10,000+ thinking tokens over-analyzing trivial one-line fixes.
  - *Over-cautiousness*: Excessive planning and asking user confirmation for non-destructive actions.
- **Actionable Best Practice**:
  - Constrain reasoning depth on trivial edits; jump straight to execution.
  - Run commands proactively — never ask the user to run something the agent can execute.
  - Keep diffs minimal, clean, and preserve all unrelated comments and docstrings.

---

## OpenAI GPT & Reasoning Family (GPT-4.5, GPT-4o, o1, o3-mini, o3)

- **Context & Output**: 128,000 to 200,000 tokens context window | 16,384 to 100,000 max output tokens.
- **Reasoning**: Reasoning Effort parameter (`low`, `medium`, `high`).
- **Core Strengths**:
  - Exceptional algorithmic, mathematical, and logic problem-solving in o1/o3-mini.
  - Strict adherence to structured JSON schemas and function calling signatures.
  - Fast single-turn code generation with standardized syntax patterns.
- **Known Traps & Blindspots**:
  - *Lazy Code Placeholders*: Tendency in GPT-4o to output `// ... existing code ...` in diffs.
  - *High Token Latency*: Full reasoning models (o1/o3) can be slow for simple file reads.
- **Actionable Best Practice**:
  - NEVER use placeholder comments (`// ...`) in replacements; provide complete drop-in code.
  - For o3-mini/o1, formulate the full logical chain internally before making tool calls.

---

## DeepSeek Reasoning Family (DeepSeek R1, DeepSeek V3)

- **Context & Output**: 64,000 to 128,000 tokens context window | 8,192 to 64,000 max output tokens.
- **Reasoning**: Pure Reinforcement Learning Thinking Chain.
- **Core Strengths**:
  - Unbeatable intelligence-per-dollar efficiency for algorithmic analysis and math.
  - Deep self-reflection and backtracking in reasoning traces (R1).
- **Known Traps & Blindspots**:
  - *Language Mixing*: Can spontaneously switch between Chinese, English, or German during thinking.
  - *Formatting Fragility*: Schema sensitivity on complex nested JSON.
- **Actionable Best Practice**:
  - Always maintain pure English in reasoning chains and code comments.
  - Keep tool payloads flat and clearly typed.

---

## Qwen Coder Family (Qwen 2.5 Coder 32B / 7B)

- **Context & Output**: 32,768 to 131,072 tokens context window | 8,192 max output tokens.
- **Core Strengths**:
  - Open-weights champion for local inference and fast code completion.
  - Zero cloud latency when running on local GPU / Ollama.
- **Known Traps & Blindspots**:
  - *Context Degradation*: Performance drops beyond 32k tokens unless yarn/rope scaled.
- **Actionable Best Practice**:
  - Decompose large multi-file tasks into focused, single-file units.
