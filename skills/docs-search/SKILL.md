---
name: docs-search
description: Search local framework documentation (Svelte 5, FastAPI, Tailwind, Tauri, Next.js, Supabase) and AI Models documentation (Claude 3.7/3.5, GPT-4.5/o1/o3, Gemini 2.0/3.0/3.7, DeepSeek V3/R1, Qwen 2.5 Coder, Image/Vision models, Speech/TTS limits, Embeddings, Azure AI, benchmarks, pricing, routing) via agents-docs MCP before guessing API methods or hallucinating stale model knowledge.
---

# Docs Search Skill

Use this skill when you need accurate, version-specific framework syntax, API signatures, code examples, or up-to-date AI model capabilities, benchmarks, image/vision models, speech/TTS limits, vector embeddings, and routing suggestions.

## How to use `agents-docs`

1. First, check available documentation sets:
   - Tool: `list_docsets()`
2. For Frameworks & Libraries:
   - Tool: `search_docs(docset="svelte-5", query="$state runes")`
   - Tool: `search_docs(docset="fastapi", query="HTTPException status_code")`
   - Tool: `search_docs(docset="all", query="OAuth flow")`
3. For AI Models, Multi-Modal Systems & Cloud AI Services:
   - **LLMs & Reasoning**: `search_docs(docset="ai-models", query="claude 3.7 sonnet thinking reasoning")`
   - **Speech, Audio & TTS Limits**: `search_docs(docset="ai-models", query="azure speech limits elevenlabs gemini tts")`
   - **TTS Request & Character Caps**: `search_docs(docset="ai-models", query="elevenlabs 5000 character limit openai tts-1 4096")`
   - **Image & Vision Generators**: `search_docs(docset="ai-models", query="flux 1.1 pro ideogram v2 midjourney resolutions aspect ratios")`
   - **Embeddings & Vector Rerankers**: `search_docs(docset="ai-models", query="text-embedding-3 voyage-code-3 cohere rerank v3.5 dimensions")`
   - **Azure AI & Cloud Services**: `search_docs(docset="ai-models", query="azure openai tpm quotas azure search hybrid vector limits")`
4. For Model Metacognition & Self-Knowledge:
   - Tool: `get_model_playbook(model="auto")` or `get_model_playbook(model="gemini-3.7-flash")`
   - Retrieve operational strengths, failure modes, whitespace gotchas, and tool-calling strategies tailored to your exact model.
5. If querying multiple distinct providers/libraries:
   - Run compound searches or query each provider specifically (e.g. `query="azure speech limits"`, `query="elevenlabs request limits"`).
   - If a catalog docset is not installed, sync it in 1 second from the curated catalog:
     - Tool: `sync_docset(name="ai-models")` or `sync_docset(name="svelte-5")`
6. Read the exact section snippets returned by `search_docs` and apply the verified limits and specifications.

