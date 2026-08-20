# Open-Weights & Local AI Models Guide (2026-08-20)

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
