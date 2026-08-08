# platform-contracts

**Two products, one protocol.** This repository is the published treaty
implemented by both halves of the platform:

- the **server platform** (`agentprint`) — Python engine, web UI, registry, hosting
- the **desktop platform** (working name "desk agent") — sovereign offline Go engine

> Status: **v0.1 draft**. Interfaces will change. The repo name is a
> brand-neutral placeholder; the project brand is not yet decided.

## Contracts

| File | Defines |
|---|---|
| `contracts/tags.md` + `tags.schema.json` | Tag vocabulary — mandatory tagging for every platform object |
| `contracts/workload-identity.schema.json` + `workload-identity.md` | Identity for `user` / `agent` / `mcp-server` principals, X.509-capable |
| `contracts/registry-sync.openapi.yaml` + `registry-sync.md` | One-way catalog sync (server → desktop), 7 object types |
| `contracts/deploy-push.openapi.yaml` + `deploy-push.md` | App deploy push (desktop → server hosting) |
| `contracts/agent-card.md` + `agent-card.schema.json` | A2A agent-card profile both engines publish |
| `contracts/okf-serving.md` + `knowledge-manifest.schema.json` | How knowledge bundles (Google OKF) are served and synced |

## Design docs

The consolidation design that produced these contracts lives in
`docs/specs/`. Read `docs/specs/2026-08-02-product-consolidation-design.md` first.

## Validating

```bash
uv sync
uv run pytest
```

Every schema and every example is validated in CI.

## License

Apache 2.0. Contributions require DCO sign-off (`git commit -s`) — see CONTRIBUTING.md.
