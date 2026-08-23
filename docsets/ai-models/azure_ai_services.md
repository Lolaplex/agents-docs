# Azure AI Cloud Services & Infrastructure Guide (2026-08-23)

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
