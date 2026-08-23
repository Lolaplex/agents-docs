# Agent Task & Modality Model Routing Matrix (2026-08-23)

Actionable decision matrix for agents and developers to choose the best model for any task across all modalities.

---

## 1. LLM & Reasoning Routing Matrix

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

---

## 2. Speech, Image & Vector Modality Routing Matrix

```
┌───────────────────────────────────────┬────────────────────────────────────────────────────────┐
│ MODALITY & USE CASE                   │ RECOMMENDED PROVIDER & MODEL                           │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ A. Long-Form Text-to-Speech           │ Azure AI Speech (Neural Voices, SSML 64k chars) /      │
│    (Articles, Narrations, Budget TTS) │ ElevenLabs Projects API / OpenAI tts-1 (4,096 chars)   │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ B. Realtime Conversational Voice      │ Cartesia Sonic (~90ms) / Deepgram Aura (~100ms) /      │
│    (Sub-second Voice Agent Loops)     │ ElevenLabs Flash v2.5 (~75ms) / Gemini 2.0/3.7 Live    │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ C. Image Generation with Typography   │ Ideogram v2 / Ideogram v2 Turbo (flawless text)        │
│    (Posters, Logos, UI Cards)         │ Recraft v3 (Vector SVG, brand styles)                  │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ D. Photorealistic Image Generation    │ FLUX.1 [dev/pro] / FLUX 1.1 Pro Ultra / Midjourney v6.1│
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ E. Codebase Semantic Search (Vectors) │ Voyage AI voyage-code-3 (32k context) / BGE-M3         │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ F. Hybrid RAG Search & Reranking      │ Azure AI Search (Hybrid BM25 + Vector + Semantic) /    │
│                                       │ Cohere Rerank v3.5 + OpenAI text-embedding-3-small     │
└───────────────────────────────────────┴────────────────────────────────────────────────────────┘
```
