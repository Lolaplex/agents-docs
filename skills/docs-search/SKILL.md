---
name: docs-search
description: Search and file historically-true tech facts via agents-docs MCP. Hard tech facts go to write_doc; user/project fluid facts go to agents-memory. Do not dump READMEs into docs.
---

# Docs Search

Local hard-fact register (`~/.agents/docs/`). Not memory. Append-mostly.

## Where facts go

- Hard tech fact (API, stack rule, model spec, platform truth) → `write_doc` / `python -m agents_docs write NAME CONTENT [CATEGORY]`
- User prefs, project decisions, identity → agents-memory (`add_memory` / `mcp.memory.add`)
- Do not dump READMEs, chat logs, or fluid notes into docs.
- Old-but-still-true facts stay. `delete_doc` only for wrong, duplicate, or yanked sheets.
- Catalog sync must not wipe agent sheets in `stacks|models|apis|platforms|custom`.

## Search

1. `list_docs()` then `search_docs(query="...", category="stacks|models|apis|platforms|custom|all")`
2. `get_doc(name="...", category="...")` for the full sheet
3. Missing catalog framework: `sync_external_doc(name="svelte-5")` or `list_catalog()`
4. Model playbooks: `get_model_playbook(model="auto")`

## Write

`write_doc(name="coolify-postgres", content="...", category="platforms")` appends a dated section.
`overwrite=True` only to replace a wrong sheet, never because a fact is old.
