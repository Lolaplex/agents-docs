# Why: Markdown + Lexical BM25 vs Vector RAG

## The Problem with Vector RAG for Code Documentation
1. **Embedding Blindness on Syntax & Versions**: Vector embeddings match generic semantics rather than exact function signatures, flags, or version changes (e.g. Svelte 4 `export let` vs Svelte 5 `$state()`).
2. **Chunk Fragmentation**: Naive fixed-size chunking (e.g. 500 tokens) cuts code blocks, tables, and headers in half, losing vital structural context.
3. **Heavy Infrastructure Overhead**: Setting up Chroma, Qdrant, Milvus, or LangChain requires Docker, persistent daemons, hundreds of megabytes in dependencies, and cloud embedding API keys.
4. **Latency & Cost**: Embedding every doc page costs API dollars and takes minutes. Searching takes 200-500ms network round-trips.

## The agents-docs Approach
1. **Header-Aware Chunking**: Markdown is parsed into natural semantic sections defined by `#`, `##`, and `###` headers. Code blocks and explanations remain intact.
2. **BM25 + Header Boosting**: Lexical BM25 search scores exact keywords with massive boost factors for matches inside headers and title lines.
3. **Sub-10ms Latency**: In-memory or on-disk ripgrep-style scan runs in under 10 milliseconds locally without any background server.
4. **Human-Readable & Transparent**: All docs live as plain `.md` files in `~/.agents/docs/`. Developers can open, edit, or git-track them at any time.
