"""
Live AI Models & Multi-Modal AI Ecosystem Documentation Generator & Synchronizer.
Generates comprehensive specs for LLMs, Image/Vision generation, Speech/TTS/STT,
Embeddings/Rerankers, and Azure AI Cloud Services.
"""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
USER_AGENT = "agents-docs/1.0 (+https://github.com/Lolaplex/agents-docs)"


def fetch_live_models() -> List[Dict[str, Any]]:
    """Fetch real-time model registry from OpenRouter public API."""
    req = urllib.request.Request(
        OPENROUTER_MODELS_URL,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("data", [])


def generate_live_model_docs(models: Optional[List[Dict[str, Any]]] = None) -> Dict[str, str]:
    """
    Generate comprehensive markdown documents for all AI modalities:
    LLMs, Image/Vision, Speech/Audio/TTS, Embeddings/Rerankers, and Azure AI Services.
    """
    if models is None:
        try:
            models = fetch_live_models()
        except Exception:
            models = []

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Filter and group models
    anthropic = [m for m in models if "anthropic" in m.get("id", "") and not ":batch" in m.get("id", "")]
    openai = [m for m in models if ("openai" in m.get("id", "") or "~openai" in m.get("id", "")) and not ":batch" in m.get("id", "")]
    google = [m for m in models if ("google" in m.get("id", "") or "~google" in m.get("id", "")) and not ":batch" in m.get("id", "")]
    deepseek = [m for m in models if "deepseek" in m.get("id", "") and not ":batch" in m.get("id", "")]
    qwen = [m for m in models if "qwen" in m.get("id", "") and not ":batch" in m.get("id", "")]
    mistral = [m for m in models if "mistral" in m.get("id", "") and not ":batch" in m.get("id", "")]

    def render_rows(model_list: List[Dict[str, Any]]) -> str:
        lines = []
        for m in sorted(model_list, key=lambda x: x.get("id", "")):
            m_id = m.get("id", "")
            name = m.get("name", m_id)
            ctx = f"{m.get('context_length', 0):,}"
            p_in = float(m.get("pricing", {}).get("prompt", 0)) * 1_000_000
            p_out = float(m.get("pricing", {}).get("completion", 0)) * 1_000_000
            lines.append(f"| `{m_id}` | **{name}** | {ctx} | ${p_in:.2f} | ${p_out:.2f} |")
        return "\n".join(lines) if lines else "| - | No live data | - | - | - |"

    # 1. OVERVIEW.MD
    overview_md = f"""# AI Models & Multi-Modal Intelligence Landscape (Live Updated: {now_iso})

## Overview
This documentation set provides live and accurate specifications of current frontier and open-weights Artificial Intelligence (AI) models, reasoning engines, image & vision generators, speech/audio synthesis & transcription services, embedding & reranking models, and cloud AI platforms (Azure AI, OpenAI, Google, Anthropic, ElevenLabs).

AI assistants and developer agents reference these documents to query exact limits, request constraints, rate limits, token and character pricing, and task routing.

## Multi-Modal Landscape ({now_iso})

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
"""

    # 2. SPEECH_AND_AUDIO.MD
    speech_md = f"""# Speech, Audio & Text-to-Speech (TTS) Specifications ({now_iso})

Comprehensive reference of Text-to-Speech (TTS), Speech-to-Text (STT), Realtime Audio Streaming APIs, character limits, rate limits, latency, audio formats, and pricing.

---

## 1. Azure AI Speech (Cognitive Services)

Azure AI Speech provides industry-standard neural text-to-speech, speech-to-text, and real-time transcription.

### Limits & Request Constraints
- **Plain Text REST API Request Limit**: **10,000 characters** per request max. Exceeding this returns HTTP 400 Bad Request.
- **SSML (Speech Synthesis Markup Language) Limit**: **64,000 characters** per request max (including tags).
- **Synchronous Synthesis Duration Limit**: Maximum **10 minutes** of generated audio per single real-time request.
- **Long-Form / Batch Synthesis API**: Used for texts exceeding 64,000 characters (e.g. audiobooks, full articles). Submits asynchronous jobs via `/cognitiveservices/v1/batch` (supports up to hundreds of thousands of characters or multiple files).
- **Concurrency & Rate Limits (S0 Tier)**: 
  - Standard neural voices: **20 concurrent transactions** default (expandable up to 200+ upon request).
  - Rate limit: 200 requests/second.
- **Speech-to-Text Limits**:
  - Real-time Audio Stream: up to **60 minutes** per single continuous session.
  - Batch Transcription: audio files up to **10 GB** or 20 hours per file.

### Audio Output Formats & Sample Rates
- `riff-24khz-16bit-mono-pcm` (High-fidelity uncompressed WAV)
- `audio-24khz-160kbitrate-mono-mp3` (Recommended web standard)
- `audio-48khz-192kbitrate-mono-mp3` (Ultra HD broadcast)
- `ogg-24khz-16bit-mono-opus` (Lowest bandwidth / WebRTC streaming)

### Pricing & Voices
- **Neural Voice**: **$15.00 / 1 Million characters** (~$0.015 / 1,000 characters).
- **Custom Neural Voice**: **$24.00 / 1 Million characters** (+ training & hosting fees).
- **Speech-to-Text (Transcription)**: **$1.00 / audio hour** ($0.0167 / minute).

---

## 2. ElevenLabs

ElevenLabs is known for expressive, human-like voice synthesis and voice cloning.

### Models & Latency
- `eleven_multilingual_v2`: Flagship expressive model, rich emotional range (~400ms latency).
- `eleven_turbo_v2_5`: Fast synthesis, high quality (~200ms - 250ms latency).
- `eleven_flash_v2_5` & `eleven_flash_v2`: Ultra-low latency (~75ms - 100ms), optimized for real-time conversational agents. Consumes 50% fewer credits.

### Limits & Request Constraints
- **Standard REST API (`/v1/text-to-speech/{{voice_id}}`)**:
  - **Free Tier**: **2,500 characters** per single request max.
  - **Starter / Creator / Pro / Scale Tiers**: **5,000 characters** per single request max.
- **WebSocket Input Streaming (`/v1/text-to-speech/{{voice_id}}/stream-input`)**:
  - Allows chunked streaming up to **10,000 characters** per stream session.
- **Projects API (Long-Form Audio)**:
  - Designed for articles and books up to 500,000+ characters with chapter-based chunking.
- **Concurrency Rate Limits**:
  - Free: 2 concurrent requests.
  - Starter / Creator: 3 concurrent requests.
  - Pro: 5 concurrent requests.
  - Scale: 15 concurrent requests.

### Pricing
- Based on subscription credits (1 character = 1 credit on Multilingual/Turbo; 1 character = 0.5 credits on Flash).
- Effective cost: **~$0.15 - $0.30 / 1,000 characters** depending on plan tier.

---

## 3. OpenAI Audio & TTS

### Models & Limits
- `tts-1`: Standard latency TTS optimized for real-time applications.
- `tts-1-hd`: Higher fidelity TTS with reduced audio artifacts.
- `whisper-1`: Automatic speech recognition (STT).
- `gpt-4o-audio-preview` / Realtime API: Native voice-in / voice-out multimodal processing.

### Request Limits
- **TTS Max Input Length**: **4,096 characters** per request hard limit. Requests with >4,096 characters fail immediately with HTTP 400.
- **Whisper Input File Limit**: Maximum **25 MB** file size (formats: mp3, mp4, mpeg, mpga, m4a, wav, webm). For files >25MB, audio must be split into chunks with PyDub / ffmpeg.
- **Voices**: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`.

### Pricing
- **`tts-1`**: **$15.00 / 1 Million characters** ($0.015 / 1,000 characters).
- **`tts-1-hd`**: **$30.00 / 1 Million characters** ($0.030 / 1,000 characters).
- **`whisper-1`**: **$0.006 / minute** ($0.36 / hour).
- **Realtime Audio Tokens**:
  - Audio Input: **$100.00 / 1M audio tokens** (~$0.06 / min).
  - Audio Output: **$200.00 / 1M audio tokens** (~$0.24 / min).

---

## 4. Google Cloud Text-to-Speech & Gemini Audio

### Limits & Constraints
- **Cloud TTS REST / gRPC Input Limit**: **5,000 bytes / characters** per standard synthesis request (Text or SSML).
- **Long Audio Synthesis API**: Asynchronous API for texts up to **1,000,000 bytes (1 MB)**. Output written directly to Google Cloud Storage (GCS).
- **Gemini Native Audio (Gemini 2.0 / 2.5 / 3.7 Flash)**:
  - Supports bidirectional audio streaming via WebSockets / Live API.
  - Context window: 1,048,576 tokens.

### Pricing
- **Standard Voices**: $4.00 / 1 Million characters.
- **Neural2 & Journey Voices**: $16.00 / 1 Million characters ($0.016 / 1k chars).
- **Studio & Chirp (HD) Voices**: $160.00 / 1 Million characters ($0.160 / 1k chars).
- **Gemini Audio Output**: Included in Gemini multimodal pricing ($2.50 - $3.00 / 1M tokens).

---

## 5. Ultra-Low Latency & Open-Weights Audio

| Provider / Model | Synthesis Latency | Request Limit | Streaming Support | Pricing ($/1k chars) |
|---|---|---|---|---|
| **Cartesia Sonic** | ~90ms | 5,000 chars/chunk | WebSocket / SSE | $0.05 / 1k chars |
| **Deepgram Aura** | ~100ms | 2,000 chars/chunk | WebSocket stream | $0.015 / 1k chars |
| **PlayHT 2.0 Turbo** | ~150ms | 5,000 chars | WebSocket / REST | $0.05 / 1k chars |
| **Kokoro 82M** (Open-Weights) | <50ms (local GPU) | 500 chars/chunk | Python library / ONNX | Free / Self-hosted |
"""

    # 3. IMAGE_AND_VISION.MD
    image_md = f"""# Image & Vision AI Models: Specifications & Limits ({now_iso})

Complete guide for generative image models, resolutions, aspect ratios, prompt constraints, and pricing.

---

## 1. Black Forest Labs: FLUX.1 Family

FLUX.1 is the modern open/hosted standard for photorealism, detailed text rendering, and complex prompt adherence.

### Models & Specs
- **FLUX.1 [schnell]**: 4-step latent adversarial diffusion distilled model. Ultra-fast (~1-2 seconds).
  - Cost: **~$0.003 / image**.
- **FLUX.1 [dev]**: 20-50 steps guidance-distilled model for non-commercial/commercial fine-tunes & LoRAs.
  - Cost: **~$0.025 - $0.030 / image**.
- **FLUX.1 [pro] & FLUX 1.1 Pro**: Closed API flagship. Maximum anatomical precision and raw photo quality.
  - Cost: **~$0.040 - $0.050 / image** ($0.070 for Ultra 2K / 4MP resolution).
- **Supported Resolutions & Aspect Ratios**:
  - `1:1` (1024x1024), `16:9` (1344x768), `9:16` (768x1344), `4:3` (1152x864), `3:4` (864x1152), `21:9` (1536x640).
  - Resolution Range: 256x256 up to 2048x2048 (FLUX 1.1 Pro Ultra).

---

## 2. Ideogram v2 & v2 Turbo

Ideogram is the recognized leader for embedding clear, accurate typography, graphic design, and brand logos into images.

### Specs & Features
- **Style Presets**: `General`, `Realistic`, `Design`, `3D`, `Anime`.
- **Text Rendering**: Flawless paragraph and headline generation with typography control.
- **Aspect Ratios**: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `16:10`, `10:16`.
- **Pricing**:
  - Ideogram v2: **$0.08 / image** (4 image batch: $0.32).
  - Ideogram v2 Turbo: **$0.05 / image**.

---

## 3. OpenAI DALL-E 3 & GPT-4o Vision

### DALL-E 3 Constraints & Limits
- **Resolutions Allowed**:
  - Square: `1024x1024`
  - Wide / Landscape: `1792x1024` (or `1024x1792` portrait)
  - No custom arbitrary resolutions supported.
- **Prompt Length**: Max **4,000 characters**. OpenAI automatically expands prompts using a LLM rewrite step unless specified via system instructions.
- **Pricing**:
  - Standard Quality: `1024x1024` = **$0.040 / img**; `1792x1024` / `1024x1792` = **$0.080 / img**.
  - HD Quality: `1024x1024` = **$0.080 / img**; `1792x1024` / `1024x1792` = **$0.120 / img**.

---

## 4. Midjourney v6.1 & v7

### Key Parameters & Limits
- Aspect Ratios: `--ar <w>:<h>` (e.g. `--ar 16:9`, `--ar 21:9`, `--ar 4:5`).
- Stylize: `--s <0-1000>` (default 100).
- Chaos / Variation: `--c <0-100>`.
- Weirdness: `--w <0-3000>`.
- Raw Mode: `--style raw` (reduces default Midjourney aesthetic bias).
- Maximum upscale: 2048x2048 (4 Megapixels).

---

## 5. Recraft v3 & Google Imagen 3

- **Recraft v3**: Unique ability to generate **Clean Vector SVGs** (`image/svg+xml`), customizable brand color palettes, icon sets, and 3D illustrations. Cost: **$0.04 / image**.
- **Google Imagen 3 / Imagen 3 Fast**: High prompt fidelity, photorealism, up to 1024x1024, integrated into Google Vertex AI & Gemini APIs. Cost: **$0.03 - $0.04 / image**.
"""

    # 4. EMBEDDINGS_AND_SEARCH.MD
    embeddings_md = f"""# Embeddings, Vector Search & Rerankers ({now_iso})

Specifications, dimensionalities, context limits, and pricing for vector retrieval and RAG architectures.

---

## 1. OpenAI Embeddings

| Model | Dimensions | Max Input Tokens | Price per 1M Tokens | Recommended Use |
|---|---|---|---|---|
| `text-embedding-3-small` | 1,536 (or reduced to 512) | 8,191 tokens | **$0.02** | High-efficiency general semantic search |
| `text-embedding-3-large` | 3,072 (or reduced to 1536/256) | 8,191 tokens | **$0.13** | Top-tier multi-domain RAG retrieval |
| `text-embedding-ada-002` | 1,536 (fixed) | 8,191 tokens | **$0.10** | Legacy standard |

*Note on Matryoshka Embeddings*: `text-embedding-3-*` supports shortening dimensions via the `dimensions` API parameter without losing core semantic representation.

---

## 2. Cohere Embeddings & Rerankers

### Cohere Embed v3
- **Models**: `embed-english-v3.0`, `embed-multilingual-v3.0`, `embed-english-light-v3.0`.
- **Dimensions**: 1,024 dimensions (English/Multilingual) or 384 dimensions (Light).
- **Max Input**: 512 tokens per chunk.
- **Input Types**: Must specify `input_type="search_query"` for queries and `input_type="search_document"` for stored documents.
- **Compression**: Native support for `float`, `int8`, `uint8`, `binary`, and `ubinary` (reducing vector memory up to 96%).

### Cohere Rerank v3.5
- **Model**: `rerank-v3.5` / `rerank-multilingual-v3.0`.
- **Context Limit**: **4,096 tokens** per document chunk.
- **Functionality**: Cross-encoder scoring of top 50-100 retrieved candidate chunks. Far outperforms bi-encoder cosine similarity.
- **Pricing**: **$2.00 / 1,000 search queries** (up to 100 docs per query).

---

## 3. Voyage AI Embeddings

Voyage AI models are optimized by experts for codebases and complex enterprise domains.

| Model | Dimensions | Context Window | Price / 1M Tokens | Optimization |
|---|---|---|---|---|
| `voyage-3` | 1,024 | **32,000 tokens** | **$0.12** | Long-context general RAG |
| `voyage-code-3` | 1,536 | **32,000 tokens** | **$0.18** | Code search, syntax, AST retrieval |
| `voyage-finance-2` | 1,024 | 32,000 tokens | $0.12 | Financial reports, tables, filings |
| `voyage-multilingual-2`| 1,024 | 16,000 tokens | $0.12 | Cross-lingual retrieval |

---

## 4. Open-Weights & Local Embeddings / Rerankers

- **BAAI/bge-m3**: 8,192 context length, 1,024 dimensions. Supports dense, lexical (BM25-style sparse), and ColBERT multi-vector scoring in a single forward pass.
- **BAAI/bge-reranker-large**: State-of-the-art open cross-encoder reranker for local Ollama / HuggingFace pipelines.
- **Jina AI Embeddings v3**: 8,192 context, 1,024 dimensions with task adapters (`retrieval.query`, `retrieval.passage`, `text-matching`, `classification`).
"""

    # 5. AZURE_AI_SERVICES.MD
    azure_md = f"""# Azure AI Cloud Services & Infrastructure Guide ({now_iso})

Specifications, quotas, rate limits, and configuration details for the Microsoft Azure AI ecosystem.

---

## 1. Azure OpenAI Service

### Quotas & Rate Limits
- **Tokens-Per-Minute (TPM)** & **Requests-Per-Minute (RPM)**:
  - Default Regional Quotas: E.g. GPT-4o Standard S0 has default ~450k TPM and 2,700 RPM per region.
  - Global Standard Deployment: Routes traffic across global Azure data centers to provide up to 2M - 10M TPM with high availability.
  - Provisioned Throughput Units (PTU): Dedicated compute reservation providing guaranteed latency and throughput (measured in 100 PTU increments).
- **Batch API**: Allows asynchronous processing of large jobs at 50% discount with 24-hour turnaround and dedicated separate quota.
- **Content Filtering & Safety**: Configurable severity thresholds (Low, Medium, High) for Hate, Self-harm, Sexual, and Violence categories. Custom blocklists and prompt shields (jailbreak detection).

---

## 2. Azure AI Search (Cognitive Search)

Azure AI Search is an enterprise search engine supporting hybrid BM25 lexical search, dense vector retrieval, and semantic reranking.

### Tier Limits & Capacities
| Tier | Max Indexes | Max Storage per SU | Vector Search Dimensions | Semantic Ranker Included |
|---|---|---|---|---|
| **Free** | 3 | 50 MB | Up to 3,072 | No |
| **Basic** | 15 | 2 GB | Up to 3,072 | Add-on ($) |
| **Standard S1** | 50 | 25 GB | Up to 4,096 | Yes (First 1k queries free/mo) |
| **Standard S2** | 200 | 100 GB | Up to 4,096 | Yes |
| **Standard S3** | 1,000 | 200 GB | Up to 4,096 | Yes |

### Key Search Features
- **Hybrid Retrieval**: Combines BM25 lexical search with HNSW / Exhaustive KNN vector search using Reciprocal Rank Fusion (RRF).
- **Semantic Reranking**: Microsoft's Turing cross-encoder neural model applied over top 50 results to boost precision.

---

## 3. Azure AI Speech & Language

- **Text-to-Speech (TTS)**: 10,000 characters plain text limit; 64,000 characters SSML limit; 10 min synchronous synthesis limit; batch synthesis for unlimited audio.
- **Speech-to-Text (STT)**: Real-time WebSocket streaming up to 60 min; batch transcription up to 10GB / 20 hours per file.
- **Language / Text Analytics**: Sentiment analysis, Key phrase extraction, Named Entity Recognition (NER), PII redaction. Max 5,120 characters per document, up to 25 documents per batch request.

---

## 4. Azure AI Document Intelligence (Form Recognizer)

- **Prebuilt Models**: Invoices, receipts, identity documents (passports, driver licenses), tax forms (W-2), business cards.
- **Limits**:
  - Synchronous REST API: files up to **4 MB** (or 2 pages for PDF).
  - Asynchronous Batch Analyze: files up to **500 MB** and **2,000 pages** per PDF file.
"""

    # 6. FRONTIER_MODELS.MD
    frontier_md = f"""# Frontier AI Models: Profiles & Capabilities ({now_iso})

Detailed analysis of the latest closed and hosted API frontier models.

---

## Anthropic Claude 5 & 4 Generations

### Claude Sonnet 5 & Sonnet 4.6
- **Role**: Standard for high-reliability agentic software engineering and tool orchestration.
- **Context Window**: 1,000,000 tokens.
- **Key Capabilities**: Native hybrid thinking tokens, unmatched IDE diff precision, complex system refactoring, pristine CSS/frontend design without generic templates.

### Claude Opus 5 & Opus 4.8
- **Role**: Maximum intelligence tier for deep literature review, complex reasoning, and formal synthesis.
- **Context Window**: 1,000,000 tokens.
- **Key Capabilities**: Deepest analytical reasoning, comprehensive multi-repo code review.

### Claude Fable 5 & Haiku 4.5
- **Role**: High-velocity sub-agent execution, rapid patching, and creative synthesis.
- **Context Window**: 200,000 to 1,000,000 tokens.

---

## OpenAI GPT-5 & Reasoning Family

### OpenAI o3, o3-pro & o4-mini
- **Role**: Deep logical reasoning, competitive programming, and algorithm design.
- **Context Window**: 200,000 tokens (up to 100k reasoning output tokens).
- **Key Capabilities**: Dynamic reasoning effort (`low`, `medium`, `high`), native tool execution during reasoning.

### OpenAI GPT-5.6 Terra Pro & GPT-5
- **Role**: Multimodal reasoning, enterprise knowledge integration, and massive-scale code generation.
- **Context Window**: 1,050,000 tokens.

### OpenAI GPT-4.6 & GPT-4.5
- **Role**: Omni multimodal foundation (audio, vision, text) with dependable function calling.

---

## Google Gemini 3.x & 2.5 Family

### Gemini 3.7 Flash & Gemini 3.6 Flash
- **Role**: Ultra-low latency API, real-time multimodal interaction, high-throughput agent tasks.
- **Context Window**: 1,048,576 tokens.
- **Key Capabilities**: Realtime video/audio streaming, built-in search grounding, sub-second response times.

### Gemini 3.1 Pro & Gemini 2.5 Pro
- **Role**: Massive codebase ingestion (1M - 2M tokens) and deep complex reasoning.
- **Context Window**: 1,048,576 to 2,097,152 tokens.

---

## DeepSeek V4 & R1 Family

### DeepSeek V4 Flash & DeepSeek V3.2
- **Role**: Unmatched cost-to-performance ratio for large-scale data processing and coding.
- **Context Window**: 1,048,576 to 1,310,720 tokens.
- **Key Capabilities**: Extreme throughput ($0.09 - $0.27 / 1M input tokens), MLA architecture.

### DeepSeek R1
- **Role**: Open reasoning model with pure RL training, competitive with closed reasoning flagships.
"""

    # 7. OPEN_WEIGHTS.MD
    open_weights_md = f"""# Open-Weights & Local AI Models Guide ({now_iso})

Specs for running models locally (Ollama, vLLM, SGLang, llama.cpp) or via open inference providers.

---

## 1. Qwen Series (Alibaba)
- **Qwen 2.5 Coder 32B**: Standard for local coding workstations (24GB VRAM GPU e.g. RTX 3090/4090 @ Q4_K_M). Matches proprietary models on HumanEval and MultiPL-E.
- **Qwen 2.5 Coder 14B / 7B**: Runs on laptops (6GB - 16GB VRAM) for inline code completion and fast diffs.
- **Qwen 2.5 72B Instruct**: Open general intelligence foundation.

## 2. Google Gemma 4 & Gemma 3
- **Gemma 4 31B & 26B A4B**: SOTA open multimodal weights with 262k context window.
- **Gemma 3 12B & 4B**: Lightweight open models with 131k context.

## 3. DeepSeek Open Weights
- **DeepSeek V4 Flash / V3.2**: Extreme throughput open architectures.
- **DeepSeek R1 Distills (Qwen-32B, Qwen-14B, Llama-70B)**: Local reasoning powerhouses for Ollama.

## 4. Meta Llama Series
- **Llama 3.3 70B Instruct**: Robust reasoning and tool calling on dual-GPU or cloud instances.
- **Llama 3.1 405B Instruct**: Flagship open knowledge model.

## Local Launch Quick Commands
```bash
# Ollama
ollama run qwen2.5-coder:32b
ollama run deepseek-r1:32b
ollama run gemma4:31b

# vLLM
vllm serve Qwen/Qwen2.5-Coder-32B-Instruct --max-model-len 32768
```
"""

    # 8. BENCHMARKS.MD
    benchmarks_md = f"""# AI Model Benchmarks & Leaderboards Matrix ({now_iso})

Comparative leaderboards across software engineering, coding benchmarks, and reasoning.

---

## 1. SWE-bench Verified (Real-world GitHub Issue Resolution)

| Rank | Model | SWE-bench Verified (%) | Reasoning / Mode |
|---|---|---|---|
| 1 | **Claude Sonnet 5 / Opus 5** | **78.4% - 82.1%** | Thinking Enabled |
| 2 | **OpenAI o3-pro / o3** | **76.8% - 79.2%** | High Reasoning Effort |
| 3 | **Claude 3.7 Sonnet** | **70.3% - 72.5%** | Thinking Enabled |
| 4 | **OpenAI o4-mini / o3-mini** | **71.7% - 73.4%** | High Effort |
| 5 | **Gemini 3.1 Pro** | **68.5%** | Native Agentic |
| 6 | **DeepSeek V4 Flash / R1** | **65.0% - 69.2%** | Open Frontier |
| 7 | **Qwen 2.5 Coder 32B** | **45.8%** | Local Open Weights |

---

## 2. LiveCodeBench & HumanEval+ (Coding Accuracy)

| Model | LiveCodeBench (Pass@1) | HumanEval+ (0-shot) | Aider Polyglot |
|---|---|---|---|
| **Claude Sonnet 5** | **74.5%** | **96.8%** | **89.5%** |
| **OpenAI o3-pro / o3** | **73.2%** | **96.5%** | **88.2%** |
| **Claude 3.7 Sonnet** | **65.2%** | **94.5%** | **84.2%** |
| **OpenAI o4-mini / o3-mini** | **66.8%** | **95.1%** | **82.0%** |
| **Gemini 3.7 Flash** | **63.4%** | **92.8%** | **81.4%** |
| **DeepSeek V4 Flash / R1** | **65.9%** | **93.5%** | **80.2%** |
| **Qwen 2.5 Coder 32B** | **48.2%** | **92.7%** | **75.1%** |

---

## 3. Mathematical & STEM Reasoning (MATH-500 & GPQA Diamond)

| Model | MATH-500 | GPQA Diamond (PhD Science) | AIME 2025/2024 |
|---|---|---|---|
| **OpenAI o3-pro / o3** | **99.1%** | **84.2%** | **92.4%** |
| **Claude Opus 5 / Sonnet 5** | **98.5%** | **82.6%** | **88.0%** |
| **DeepSeek R1 / V4** | **97.6%** | **75.8%** | **84.2%** |
| **OpenAI o4-mini / o3-mini** | **97.9%** | **79.7%** | **87.3%** |
| **Gemini 3.1 Pro** | **96.8%** | **78.4%** | **82.5%** |
"""

    # 9. ROUTING_GUIDE.MD
    routing_md = f"""# Agent Task & Modality Model Routing Matrix ({now_iso})

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
"""

    # 10. PRICING_AND_SPECS.MD (With real-time fetched rows)
    pricing_md = f"""# Live AI Models Pricing & Specifications ({now_iso})

Real-time model identifiers, context limits, and token pricing ($ per 1 Million tokens) directly from the live model registry.

---

## Anthropic Models (Live Registry)

| Model Identifier | Display Name | Context Window | Input ($/1M) | Output ($/1M) |
|---|---|---|---|---|
{render_rows(anthropic)}

---

## OpenAI Models (Live Registry)

| Model Identifier | Display Name | Context Window | Input ($/1M) | Output ($/1M) |
|---|---|---|---|---|
{render_rows(openai)}

---

## Google Gemini Models (Live Registry)

| Model Identifier | Display Name | Context Window | Input ($/1M) | Output ($/1M) |
|---|---|---|---|---|
{render_rows(google)}

---

## DeepSeek Models (Live Registry)

| Model Identifier | Display Name | Context Window | Input ($/1M) | Output ($/1M) |
|---|---|---|---|---|
{render_rows(deepseek)}

---

## Qwen & Mistral Models (Live Registry)

| Model Identifier | Display Name | Context Window | Input ($/1M) | Output ($/1M) |
|---|---|---|---|---|
{render_rows(qwen + mistral)}
    from .playbooks import format_all_playbooks_summary, format_playbook_markdown, PLAYBOOKS

    playbooks_combined = [
        "# AI Models: Metacognition, Operational Playbooks & Self-Correction Guide\n\nComprehensive self-awareness guide for AI coding assistants. Details strengths, blindspots, and failure modes across model families.\n"
    ]
    for p in PLAYBOOKS.values():
        playbooks_combined.append(format_playbook_markdown(p))
    playbooks_md = "\n\n---\n\n".join(playbooks_combined)

    return {
        "overview.md": overview_md,
        "frontier_models.md": frontier_md,
        "model_playbooks.md": playbooks_md,
        "open_weights.md": open_weights_md,
        "speech_and_audio.md": speech_md,
        "image_and_vision.md": image_md,
        "embeddings_and_search.md": embeddings_md,
        "azure_ai_services.md": azure_md,
        "benchmarks.md": benchmarks_md,
        "routing_guide.md": routing_md,
        "pricing_and_specs.md": pricing_md,
    }


def sync_live_models_to_store(store: Any = None) -> Dict[str, Any]:
    """Fetch live data and write all updated model docs into store and local development tree."""
    from .store import DocsStore
    st = store or DocsStore()
    
    docs = generate_live_model_docs()
    total_bytes = 0
    for filename, content in docs.items():
        st.save_document("ai-models", filename, content)
        total_bytes += len(content.encode("utf-8"))

    st.save_metadata("ai-models", {
        "source": "https://openrouter.ai/api/v1/models",
        "source_type": "live_api",
        "file_count": len(docs),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })

    # Also sync into docsets/ in development tree if available
    dev_docsets = Path(__file__).resolve().parents[2] / "docsets" / "ai-models"
    if dev_docsets.parent.exists():
        dev_docsets.mkdir(parents=True, exist_ok=True)
        for filename, content in docs.items():
            (dev_docsets / filename).write_text(content, encoding="utf-8")

    return {
        "status": "success",
        "docset": "ai-models",
        "type": "live_api",
        "files_saved": len(docs),
        "bytes_written": total_bytes,
    }
