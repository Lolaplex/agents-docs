# Image & Vision AI Models: Specifications & Limits (2026-08-23)

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
