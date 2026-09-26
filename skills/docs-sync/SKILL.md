---
name: docs-sync
description: Synchronize and maintain fresh framework documentation in ~/.agents/docs/ using agents-docs catalog or custom URLs.
---

# Docs Sync Skill

Use this skill when a project needs an official framework docset that is not already under `~/.agents/docs/`.

## Workflows

### 1. Sync from Curated Catalog
Check if the framework is in the built-in catalog:
- Tool: `list_catalog()`
- Tool: `sync_external_doc(name="supabase")`

### 2. Sync from Custom URL (llms.txt / markdown)
If the framework is not in the catalog, pass its official `llms.txt` or markdown URL:
- Tool: `sync_external_doc(name="my-lib", url="https://my-lib.dev/llms.txt")`
- Or via CLI: `agents-docs sync my-lib --url https://my-lib.dev/llms.txt`

Catalog sync writes a docset folder. It does not rewrite agent fact sheets under `stacks|models|apis|platforms|custom`.
