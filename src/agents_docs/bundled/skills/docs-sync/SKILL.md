---
name: docs-sync
description: Synchronize and maintain fresh framework documentation in ~/.agents/docs/ using agents-docs catalog or custom URLs.
---

# Docs Sync Skill

Use this skill when a new package or framework is added to a project's `package.json`, `requirements.txt`, or `Cargo.toml`.

## Workflows

### 1. Sync from Curated Catalog
Check if the framework is in the built-in catalog:
- Tool: `list_catalog()`
- Tool: `sync_docset(name="supabase")`

### 2. Sync from Custom URL (llms.txt / GitHub)
If the framework is not in the default catalog, sync from its official `llms.txt` or markdown URL:
- Tool: `sync_docset(name="my-lib", url="https://my-lib.dev/llms.txt")`
- Or via CLI: `agents-docs sync my-lib --url https://my-lib.dev/llms.txt`
