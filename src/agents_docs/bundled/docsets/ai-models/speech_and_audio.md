# Speech, Audio & Text-to-Speech (TTS) Specifications (2026-08-23)

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
- **Standard REST API (`/v1/text-to-speech/{voice_id}`)**:
  - **Free Tier**: **2,500 characters** per single request max.
  - **Starter / Creator / Pro / Scale Tiers**: **5,000 characters** per single request max.
- **WebSocket Input Streaming (`/v1/text-to-speech/{voice_id}/stream-input`)**:
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
