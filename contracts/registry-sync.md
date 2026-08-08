# Registry Sync (flow ①, v0.1)

Server → desktop, strictly one-way. The server registry is the source of
truth. A desktop that edits a synced object edits its **local copy**;
publishing back to the server is a named, deferred v2 feature — not part
of this contract.

## Sync algorithm (client side)

1. `GET /v0/registry/objects?since=<cursor>` — page through changes.
2. For each changed entry, `GET .../{type}/{name}` for the manifest.
3. Download files listed in the manifest; verify each `sha256`.
4. Store the new cursor. Offline reads come from the local store.

This is the SkillHub sync-catalog-to-disk pattern generalized to all
seven object types. Knowledge bundles additionally follow
`okf-serving.md`.

## Auth

Requests carry the caller's credential per `workload-identity.md`
(bearer token in v0.1). Anonymous read MAY be allowed for
`data:public` objects; everything else requires auth.
