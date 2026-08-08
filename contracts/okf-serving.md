# OKF Serving Conventions (v0.1)

Knowledge bundles are Google Open Knowledge Format (OKF) directories —
Markdown files with YAML frontmatter. Spec:
https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

## Rules

1. A bundle is a registry object of type `knowledge-bundle`, synced via
   the Registry Sync API like any other object; its manifest follows
   `knowledge-manifest.schema.json`.
2. Bundle root MUST contain `index.md`; its frontmatter SHOULD declare
   `okf_version`, which the manifest mirrors.
3. **Documents only.** Bundles never contain embeddings, vector indexes,
   or other derived artifacts. Each engine builds its own local index
   (SurrealDB server-side, pgvector + local embedding model on desktop)
   the way a database builds its own btrees.
4. Manifest `files` entries are Markdown only (`.md` / `.markdown`).
   Non-Markdown assets are out of scope for v0.1.
5. OKF trust frontmatter (`generated`, `verified`, `sources`, `status`,
   `stale_after`) passes through untouched; engines MAY surface it but
   MUST NOT rewrite it.
6. Consumers verify every file's `sha256` before indexing.
