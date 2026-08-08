# Contributing

## Developer Certificate of Origin (DCO)

Every commit must be signed off:

```bash
git commit -s -m "your message"
```

This adds a `Signed-off-by:` trailer certifying you wrote the change or
have the right to submit it under Apache 2.0 (see
https://developercertificate.org/). PRs with unsigned commits will fail CI.

## What belongs here

Contract documents (Markdown), JSON Schemas, OpenAPI specs, and examples —
plus the tests that validate them. No runtime code: implementations live in
the product repos.

## Making a change

1. Change or add a schema/spec under `contracts/`.
2. Add or update the matching example under `examples/`.
3. `uv run pytest` — everything must pass.
4. Contract changes follow SemVer: breaking change → major bump discussion first (open an issue).
