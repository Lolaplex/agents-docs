# llms.txt & llms-full.txt Standard

`agents-docs` natively ingests documents structured according to the `llms.txt` proposal.

## Format Overview

- `llms.txt`: A concise index file containing links to specific markdown docs along with brief summaries.
- `llms-full.txt`: A single consolidated markdown document containing the complete documentation set for LLM consumption.

## Parsing Strategy

1. If the URL points to `llms-full.txt` (or a single aggregated markdown document):
   - Saved directly as `docs.md` or split into thematic markdown files based on top-level `#` sections.
2. If the URL points to an index `llms.txt`:
   - Follows relative links specified in markdown lists and downloads sub-documents into the docset folder.
