# App Deploy Push (flow ②, v0.1)

Desktop → server. The desktop builds an app locally (vibe-coding) and
pushes `manifest + tar.gz archive`. The server verifies the archive hash,
builds (Nixpacks or equivalent), hosts, and exposes a URL.

- The **server** picks the deploy backend (docker / coolify / gitea in
  today's implementation); clients never choose infrastructure.
- Poll `GET /v0/deployments/{id}` until `deployed` or `failed`.
  v0.1 is poll-only; push notifications are a later addition.
- Deploying requires an authorized principal (`workload-identity.md`);
  apps enter the registry as `app` objects and MUST satisfy the
  mandatory intake tags (`tags.md`).

## Auth

Requests carry the caller's credential per `workload-identity.md`
(bearer token in v0.1). The OpenAPI document declares `bearerAuth`
(HTTP bearer) globally, so every operation requires a credential by
default: a missing or invalid credential is `401`, and a valid
credential whose principal may not deploy is `403`.

## Status enum

`status` is exactly `queued | building | deployed | failed`, in that
lifecycle order. `queued` and `building` are non-terminal; `deployed`
and `failed` are terminal. `url` is present once (and only once) the
status is `deployed`; `error` carries a human-readable reason when the
status is `failed`. The desktop UI and `agentprint` both bind to this
enum, so it is frozen for v0.1.
