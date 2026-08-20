"""
Curated Catalog of popular modern frameworks and libraries for 1-click sync.
Now features auto-detection from project manifests AND local agents-memory project maps.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

CURATED_CATALOG: Dict[str, Dict[str, Any]] = {
    "svelte-5": {
        "name": "svelte-5",
        "description": "Svelte 5 Official Documentation, Runes ($state, $derived, $effect), and Migration Guide",
        "source_type": "llmstxt",
        "url": "https://svelte.dev/docs/llms-full.txt",
        "tags": ["frontend", "svelte", "typescript", "ui"],
        "detect": ["svelte", "svelte 5", "svelte5"],
    },
    "fastapi": {
        "name": "fastapi",
        "description": "FastAPI modern, high-performance web framework for Python",
        "source_type": "llmstxt",
        "url": "https://fastapi.tiangolo.com/llms-full.txt",
        "tags": ["backend", "python", "api", "async"],
        "detect": ["fastapi"],
    },
    "nextjs": {
        "name": "nextjs",
        "description": "Next.js App Router, Server Components, and API reference",
        "source_type": "llmstxt",
        "url": "https://nextjs.org/docs/llms.txt",
        "tags": ["frontend", "react", "fullstack", "nextjs"],
        "detect": ["next", "next.js", "nextjs"],
    },
    "supabase": {
        "name": "supabase",
        "description": "Supabase client libraries, Auth, Database, Storage, and Edge Functions",
        "source_type": "llmstxt",
        "url": "https://supabase.com/docs/llms.txt",
        "tags": ["backend", "database", "auth", "postgres"],
        "detect": ["supabase", "@supabase/supabase-js"],
    },
    "tauri-2": {
        "name": "tauri-2",
        "description": "Tauri v2 Desktop and Mobile application development framework",
        "source_type": "llmstxt",
        "url": "https://v2.tauri.app/llms.txt",
        "tags": ["desktop", "mobile", "rust", "frontend"],
        "detect": ["tauri", "tauri 2", "tauri v2", "@tauri-apps/api"],
    },
    "tailwind-v3": {
        "name": "tailwind-v3",
        "description": "Tailwind CSS v3 utility-first CSS framework documentation",
        "source_type": "llmstxt",
        "url": "https://v3.tailwindcss.com/llms.txt",
        "tags": ["css", "styling", "frontend"],
        "detect": ["tailwind", "tailwind v3", "tailwindcss"],
    },
    "tailwind-v4": {
        "name": "tailwind-v4",
        "description": "Tailwind CSS v4 CSS-first configuration and engine",
        "source_type": "llmstxt",
        "url": "https://tailwindcss.com/docs/llms.txt",
        "tags": ["css", "styling", "frontend"],
        "detect": ["tailwind v4", "@tailwindcss/vite"],
    },
    "hono": {
        "name": "hono",
        "description": "Hono ultrafast web framework for Cloudflare Workers, Deno, Bun, and Node",
        "source_type": "llmstxt",
        "url": "https://hono.dev/llms-full.txt",
        "tags": ["backend", "typescript", "serverless", "edge"],
        "detect": ["hono"],
    },
    "mcp": {
        "name": "mcp",
        "description": "Model Context Protocol (MCP) specification, Python & TypeScript SDKs",
        "source_type": "llmstxt",
        "url": "https://modelcontextprotocol.io/llms-full.txt",
        "tags": ["agents", "mcp", "ai", "protocol"],
        "detect": ["@modelcontextprotocol/sdk", "mcp", "fastmcp"],
    },
    "wxt": {
        "name": "wxt",
        "description": "WXT Next-gen Web Extension Framework for Chrome, Firefox, Safari",
        "source_type": "llmstxt",
        "url": "https://wxt.dev/llms.txt",
        "tags": ["browser-extension", "typescript", "vite"],
        "detect": ["wxt"],
    },
    "typescript": {
        "name": "typescript",
        "description": "TypeScript Handbook: Types, Generics, Narrowing, Interfaces, Utility Types, and tsconfig",
        "source_type": "llmstxt",
        "url": "https://raw.githubusercontent.com/microsoft/TypeScript-New-Handbook/master/chapters/Basics.md",
        "tags": ["languages", "typescript", "types", "frontend", "backend"],
        "detect": ["typescript", "tsc", "@types/node"],
    },
    "netlify": {
        "name": "netlify",
        "description": "Netlify modern web hosting, Edge Functions, redirects, headers, and form handling",
        "source_type": "llmstxt",
        "url": "https://docs.netlify.com/llms.txt",
        "tags": ["hosting", "deployment", "serverless", "edge", "cloud"],
        "detect": ["netlify", "netlify-cli", "@netlify/functions"],
    },
    "coolify": {
        "name": "coolify",
        "description": "Coolify self-hosted PaaS documentation, Docker deployments, services, databases, and APIs",
        "source_type": "llmstxt",
        "url": "https://coolify.io/docs/llms.txt",
        "tags": ["devops", "self-hosted", "docker", "deployment", "paas"],
        "detect": ["coolify"],
    },
    "resend": {
        "name": "resend",
        "description": "Resend transactional email API, React Email, domains, webhooks, and SDKs",
        "source_type": "llmstxt",
        "url": "https://resend.com/docs/llms.txt",
        "tags": ["email", "backend", "api", "communication"],
        "detect": ["resend", "@react-email/components"],
    },
    "cloudflare": {
        "name": "cloudflare",
        "description": "Cloudflare Workers, Pages, KV, D1 SQL Database, Queues, and Hyperdrive",
        "source_type": "llmstxt",
        "url": "https://developers.cloudflare.com/llms.txt",
        "tags": ["cloud", "serverless", "edge", "database", "workers"],
        "detect": ["wrangler", "@cloudflare/workers-types"],
    },
    "react": {
        "name": "react",
        "description": "React 19, Server Actions, Hooks (use, useEffect, useState), Suspense, and Components",
        "source_type": "llmstxt",
        "url": "https://react.dev/llms.txt",
        "tags": ["frontend", "react", "ui", "javascript", "typescript"],
        "detect": ["react", "react-dom"],
    },
    "vite": {
        "name": "vite",
        "description": "Vite Next Generation Frontend Tooling, HMR, plugins, build optimizations, and SSR",
        "source_type": "llmstxt",
        "url": "https://vite.dev/llms.txt",
        "tags": ["bundler", "frontend", "tooling", "build"],
        "detect": ["vite", "@vitejs/plugin-react"],
    },
    "pydantic": {
        "name": "pydantic",
        "description": "Pydantic V2 data validation and settings management using Python type annotations",
        "source_type": "llmstxt",
        "url": "https://docs.pydantic.dev/latest/llms.txt",
        "tags": ["backend", "python", "validation", "types"],
        "detect": ["pydantic", "pydantic-settings", "pydantic-core"],
    },
    "zod": {
        "name": "zod",
        "description": "Zod TypeScript-first schema declaration and static type inference validation library",
        "source_type": "llmstxt",
        "url": "https://zod.dev/llms.txt",
        "tags": ["typescript", "validation", "schema", "types"],
        "detect": ["zod"],
    },
    "shadcn-ui": {
        "name": "shadcn-ui",
        "description": "shadcn/ui accessible and customizable Tailwind UI components and Radix Primitives",
        "source_type": "llmstxt",
        "url": "https://ui.shadcn.com/llms.txt",
        "tags": ["ui", "components", "tailwind", "react"],
        "detect": ["shadcn", "shadcn-ui", "@radix-ui/react-slot"],
    },
    "ai-models": {
        "name": "ai-models",
        "description": "Comprehensive reference of Frontier & Open-Weights AI Models (Claude 3.7/3.5, GPT-4.5/o1/o3, Gemini 2.0/3.0/3.7, DeepSeek V3/R1, Qwen 2.5 Coder, Llama 3.3), specs, benchmarks, pricing, and task routing",
        "source_type": "bundled",
        "url": "bundled://ai-models",
        "tags": ["ai", "models", "benchmarks", "llm", "routing", "pricing", "frontier"],
        "detect": ["ai-models", "models", "llms", "ki-modelle", "frontier-models", "llm-models", "anthropic", "openai", "deepseek", "gemini", "qwen", "claude"],
    },
}


def get_catalog_entry(name: str) -> Optional[Dict[str, Any]]:
    """Look up a framework in the curated catalog, including alias matches."""
    clean_name = name.strip().lower()
    if clean_name in CURATED_CATALOG:
        return CURATED_CATALOG[clean_name]

    # Alias search
    for entry in CURATED_CATALOG.values():
        if clean_name in [d.lower() for d in entry.get("detect", [])]:
            return entry
    return None


def list_catalog_entries() -> List[Dict[str, Any]]:
    """Return all catalog entries sorted by name."""
    return sorted(CURATED_CATALOG.values(), key=lambda x: x["name"])


def get_memory_root() -> Path:
    """Location of local agents-memory store: ~/.agents/memory/"""
    override = os.getenv("AGENTS_MEMORY_PATH")
    if override:
        return Path(override)
    return Path.home() / ".agents" / "memory"


def detect_memory_docsets() -> List[str]:
    """
    Scan ~/.agents/memory/ (PROJECTS.md, USER.md, and projects/*.md)
    and return catalog docset names matching frameworks referenced in agent memory.
    """
    mem_root = get_memory_root()
    if not mem_root.exists():
        return []

    combined_text = []

    # Read PROJECTS.md and USER.md
    for f in ["PROJECTS.md", "USER.md"]:
        target = mem_root / f
        if target.exists():
            try:
                combined_text.append(target.read_text(encoding="utf-8", errors="replace").lower())
            except Exception:
                pass

    # Read projects/*.md
    projects_dir = mem_root / "projects"
    if projects_dir.exists():
        for pf in projects_dir.rglob("*.md"):
            try:
                combined_text.append(pf.read_text(encoding="utf-8", errors="replace").lower())
            except Exception:
                pass

    full_blob = "\n".join(combined_text)

    matched_docsets: set[str] = set()
    for entry in CURATED_CATALOG.values():
        for d in entry.get("detect", []):
            if d.lower() in full_blob:
                matched_docsets.add(entry["name"])

    return sorted(matched_docsets)


def detect_project_docsets(project_path: str | Path) -> List[str]:
    """
    Inspect project manifests (package.json, requirements.txt, pyproject.toml, Cargo.toml)
    and return catalog docset names matching detected dependencies.
    """
    root = Path(project_path).resolve()
    detected_keys: set[str] = set()

    # 1. package.json
    pkg_file = root / "package.json"
    if pkg_file.exists():
        try:
            content = json.loads(pkg_file.read_text(encoding="utf-8"))
            deps = {
                **content.get("dependencies", {}),
                **content.get("devDependencies", {}),
            }
            for dep_name in deps.keys():
                detected_keys.add(dep_name.lower())
        except Exception:
            pass

    # 2. requirements.txt / pyproject.toml
    req_file = root / "requirements.txt"
    if req_file.exists():
        try:
            for line in req_file.read_text(encoding="utf-8").splitlines():
                pkg = line.split("==")[0].split(">=")[0].split("<=")[0].strip().lower()
                if pkg:
                    detected_keys.add(pkg)
        except Exception:
            pass

    pyproject_file = root / "pyproject.toml"
    if pyproject_file.exists():
        try:
            text = pyproject_file.read_text(encoding="utf-8").lower()
            for key in ["fastapi", "mcp", "pydantic", "httpx", "svelte"]:
                if key in text:
                    detected_keys.add(key)
        except Exception:
            pass

    # 3. Cargo.toml
    cargo_file = root / "Cargo.toml"
    if cargo_file.exists():
        try:
            text = cargo_file.read_text(encoding="utf-8").lower()
            if "tauri" in text:
                detected_keys.add("tauri")
        except Exception:
            pass

    # Match detected keys to catalog docsets
    matched_docsets: set[str] = set()
    for entry in CURATED_CATALOG.values():
        for d in entry.get("detect", []):
            if d.lower() in detected_keys:
                matched_docsets.add(entry["name"])

    return sorted(matched_docsets)
