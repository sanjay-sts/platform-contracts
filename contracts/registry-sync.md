# Registry Sync (flow ①, v0.1)

Server → desktop, strictly one-way. The server registry is the source of
truth. A desktop that edits a synced object edits its **local copy**;
publishing back to the server is a named, deferred v2 feature — not part
of this contract.

## Sync algorithm (client side)

1. `GET /v0/registry/objects?since=<cursor>` — keep paging until a response
   comes back with an empty `entries` array; that means the client is caught
   up. Every response carries a `next` cursor, including that last one.
2. Entries with `deleted: true` are tombstones: remove the object from the
   local store instead of fetching it, and skip the remaining steps for it.
3. For each remaining changed entry, `GET .../{object_type}/{name}` for the
   manifest.
4. Download files listed in the manifest; verify each file's `sha256`. The
   catalog `etag` is compared for equality only — never recomputed.
5. Store the `next` cursor from every response — including empty pages — and
   resume from it on the next poll. Offline reads come from the local store.

This is the SkillHub sync-catalog-to-disk pattern generalized to all
seven object types. Knowledge bundles additionally follow
`okf-serving.md`.

## Auth

Requests carry the caller's credential per `workload-identity.md`
(bearer token in v0.1). The OpenAPI document declares `bearerAuth`
(HTTP bearer) globally, so every operation requires a credential by
default and each returns `401` without one.

Anonymous read MAY be allowed for `data:public` objects; everything else
requires auth. That allowance is a **server-side relaxation** of the
globally declared requirement — the YAML states the strict default, and a
server choosing to serve `data:public` objects unauthenticated is
conforming, not deviating.
