# Agent Task Model Routing Matrix (2026-08-20)

Actionable decision matrix for agents and developers to choose the best model for any task.

---

## Decision Matrix

```
┌───────────────────────────────────────┬────────────────────────────────────────────────────────┐
│ TASK SCENARIO                         │ RECOMMENDED MODEL(S)                                  │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. Complex Full-Stack Architecture /  │ Claude Sonnet 5 / Claude 3.7 Sonnet (Thinking enabled) │
│    Multi-file Refactoring & Bugs      │ OpenAI o3 / o3-pro / o4-mini (High reasoning)          │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 2. Frontend UI / Premium Design /     │ Claude Sonnet 5 / Claude Sonnet 4.6                    │
│    CSS Tokens & Animations            │ (Highest visual aesthetics, zero generic placeholder)  │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 3. Huge Codebase Context Ingestion    │ Gemini 3.1 Pro / Gemini 2.5 Pro (1M - 2M tokens)       │
│    (Entire repos, 100+ files, specs)  │ DeepSeek V4 Flash (1.3M tokens)                        │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 4. Sub-Second Interactive Diffs /     │ Gemini 3.7 Flash ($0.38/1M) / Claude Haiku 4.5         │
│    Autocomplete & Fast Edits          │ Qwen 2.5 Coder 14B / 32B                               │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 5. High-Throughput Batch Processing / │ DeepSeek V4 Flash ($0.09/1M) / Gemini 2.5 Flash Lite   │
│    Memory Extraction / Tagging        │ OpenAI gpt-oss-120b / gpt-4o-mini                      │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 6. Formal Logic / Math Verification   │ OpenAI o3-pro / o3 / DeepSeek R1                       │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ 7. 100% Offline / Private Local Work  │ Qwen 2.5 Coder 32B (via Ollama on 24GB GPU)            │
│                                       │ DeepSeek-R1-Distill-Qwen-32B / Gemma 4 31B             │
└───────────────────────────────────────┴────────────────────────────────────────────────────────┘
```
