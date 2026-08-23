# Embeddings, Vector Search & Rerankers (2026-08-23)

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
