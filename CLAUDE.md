# platform-contracts — repo map

The published treaty between the server platform (`agentprint`) and the
desktop platform. Schemas + docs only; no runtime code.

- `contracts/` — one contract per concern: paired `.md` (prose) + `.schema.json` or `.openapi.yaml` (machine-checkable).
- `examples/` — one valid instance per schema; tests validate each pair.
- `docs/specs/` — the consolidation design docs (canonical).
- `tests/` — pytest harness; `uv run pytest` validates all schemas, specs, and examples.

Rules:
- Every commit: `git commit -s` (DCO).
- JSON Schema draft 2020-12, OpenAPI 3.0.3, no cross-file `$ref` in v0.1.
- Object-type enum everywhere: `agent`, `mcp-server`, `skill`, `prompt`, `app`, `policy`, `knowledge-bundle`.
- Agent-card `description` is for routing; never store agent instructions in it.
