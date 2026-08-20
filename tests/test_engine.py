"""Tests for DocsEngine sectioning and BM25 ranking."""

import shutil
import tempfile
import unittest
from pathlib import Path

from agents_docs.engine import DocsEngine
from agents_docs.store import DocsStore


class TestDocsEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.store = DocsStore(root=self.temp_dir)
        self.engine = DocsEngine(store=self.store)

        # Sample docset
        svelte_md = """# Svelte 5 Documentation

Welcome to the new Svelte 5 release.

## Runes $state
Use `$state()` to declare reactive state variables in Svelte 5.
```svelte
<script>
  let count = $state(0);
</script>
```

## Runes $derived
Use `$derived()` to compute values based on reactive state.
```svelte
<script>
  let double = $derived(count * 2);
</script>
```

## Legacy Syntax
In Svelte 4 you used `let count = 0;` which is now deprecated.
"""
        self.store.save_document("svelte-5", "runes.md", svelte_md)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_search_exact_runes_match(self):
        results = self.engine.search(docset="svelte-5", query="$state runes")
        self.assertGreater(len(results), 0)
        top = results[0]
        self.assertIn("Runes $state", top["header"])
        self.assertIn("let count = $state(0)", top["snippet"])

    def test_search_derived_match(self):
        results = self.engine.search(docset="svelte-5", query="derived values")
        self.assertGreater(len(results), 0)
        self.assertIn("Runes $derived", results[0]["header"])

    def test_search_cross_docset(self):
        self.store.save_document("fastapi", "routes.md", "# FastAPI Routes\n\nUse `@app.get` for HTTP GET endpoints.")
        results = self.engine.search(docset="all", query="FastAPI Routes")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["docset"], "fastapi")


if __name__ == "__main__":
    unittest.main()
