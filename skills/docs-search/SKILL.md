---
name: docs-search
description: Search local framework documentation (Svelte 5, FastAPI, Tailwind, Tauri, Next.js, Supabase) and AI Models documentation (Claude 3.7/3.5, GPT-4.5/o1/o3, Gemini 2.0/3.0, DeepSeek V3/R1, Qwen 2.5 Coder, benchmarks, pricing, routing) via agents-docs MCP before guessing API methods or hallucinating stale model knowledge.
---

# Docs Search Skill

Use this skill when you need accurate, version-specific framework syntax, API signatures, code examples, or up-to-date AI model capabilities, benchmarks, and routing suggestions.

## How to use `agents-docs`

1. First, check available documentation sets:
   - Tool: `list_docsets()`
2. For Frameworks & Libraries:
   - Tool: `search_docs(docset="svelte-5", query="$state runes")`
   - Tool: `search_docs(docset="fastapi", query="HTTPException status_code")`
   - Tool: `search_docs(docset="all", query="OAuth flow")`
3. For AI Models, LLMs, Benchmarks & Model Routing:
   - Tool: `search_docs(docset="ai-models", query="best model for coding refactoring")`
   - Tool: `search_docs(docset="ai-models", query="claude 3.7 sonnet thinking reasoning")`
   - Tool: `search_docs(docset="ai-models", query="SWE-bench leaderboards")`
   - Tool: `search_docs(docset="ai-models", query="qwen 2.5 coder 32b hardware vram")`
   - Tool: `search_docs(docset="ai-models", query="pricing context window token limits")`
4. If a catalog docset is not installed, sync it in 1 second from the curated catalog:
   - Tool: `sync_docset(name="ai-models")` or `sync_docset(name="svelte-5")`
5. Read the exact section snippet returned by `search_docs` and apply the verified specifications.

