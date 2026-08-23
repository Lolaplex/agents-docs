# AI Models & Multi-Modal Intelligence Landscape (Live Updated: 2026-08-23)

## Overview
This documentation set provides live and accurate specifications of current frontier and open-weights Artificial Intelligence (AI) models, reasoning engines, image & vision generators, speech/audio synthesis & transcription services, embedding & reranking models, and cloud AI platforms (Azure AI, OpenAI, Google, Anthropic, ElevenLabs).

AI assistants and developer agents reference these documents to query exact limits, request constraints, rate limits, token and character pricing, and task routing.

## Multi-Modal Landscape (2026-08-23)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI MODALITIES & CAPABILITIES                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. FRONTIER LLMS & REASONING                                                │
│    • Anthropic: Claude Sonnet 5 / 3.7 / 4.6 (Agentic coding, hybrid think)  │
│    • OpenAI: o3, o3-pro, o4-mini (Test-time compute reasoning), GPT-5/4.5   │
│    • Google: Gemini 3.7 Flash & 3.1 Pro (1M-2M context, native multimodal)  │
│    • DeepSeek: V4 Flash, V3.2, DeepSeek R1 (MLA high-throughput reasoning)  │
│    • Open Weights: Qwen 2.5 Coder 32B, Gemma 4, Llama 3.3 70B               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. SPEECH, AUDIO & TTS ENGINES                                              │
│    • Azure AI Speech: Neural voices, SSML (64k chars), REST (10k chars)     │
│    • ElevenLabs: Turbo v2.5, Flash v2.5 (2.5k - 10k chars, WebSocket stream)│
│    • OpenAI: tts-1, tts-1-hd (4,096 chars limit), Whisper (25MB audio limit)│
│    • Google Cloud TTS: Journey/Neural2 (5,000 chars limit), Gemini Live     │
│    • Ultra-Low Latency: Cartesia Sonic (~90ms), Deepgram Aura (~100ms)      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. IMAGE, VISION & DESIGN GENERATION                                        │
│    • Black Forest Labs: FLUX.1 [schnell, dev, pro], FLUX 1.1 Pro (2K res)  │
│    • Midjourney: v6.1, v7, Niji 6 (Photorealism, aesthetic control)         │
│    • Ideogram: v2 & v2 Turbo (Industry gold standard for image typography)  │
│    • DALL-E 3 & Google Imagen 3 (Prompt fidelity, HD rendering)             │
│    • Recraft v3 (Native Vector SVG, brand palettes, icons)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. EMBEDDINGS, VECTOR SEARCH & RERANKERS                                    │
│    • OpenAI: text-embedding-3-small (1536d) & large (3072d, 8191 tokens)   │
│    • Cohere: Embed v3 (1024d) & Rerank v3.5 (4096 tokens cross-encoder)     │
│    • Voyage AI: voyage-3 (1024d, 32k tokens), voyage-code-3 (1536d, code)   │
│    • Open Weights: BGE-M3 (dense/sparse/colbert), Jina Embeddings v3        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. CLOUD AI ECOSYSTEMS (AZURE AI & OPENAI)                                  │
│    • Azure OpenAI Service: TPM/RPM quotas, PTU provisioning, content safety │
│    • Azure AI Search: Hybrid search, BM25 + Vector + Semantic Ranker        │
│    • Azure Document Intelligence & Computer Vision OCR                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Navigation
- [Frontier Closed Models](frontier_models.md)
- [Open-Weights & Local Deployment](open_weights.md)
- [Speech, Audio & TTS Systems](speech_and_audio.md)
- [Image, Vision & Art Generation](image_and_vision.md)
- [Embeddings, Vector Search & Rerankers](embeddings_and_search.md)
- [Azure AI Services & Ecosystem](azure_ai_services.md)
- [Leaderboards & Benchmarks](benchmarks.md)
- [Agent Task Routing Matrix](routing_guide.md)
- [Live Pricing & Specs Matrix](pricing_and_specs.md)
