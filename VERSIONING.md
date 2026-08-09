# Versioning

Contracts follow SemVer, versioned as a set: one version number for the
whole repo, git-tagged (`v0.1.0`).

- **Patch** — wording, examples, docs; no schema change.
- **Minor** — backward-compatible additions (new optional field, new
  endpoint, new tag namespace).
- **Breaking** — anything that makes a currently-valid instance invalid
  or changes endpoint semantics. Requires a major bump and an issue
  discussing migration before merge.
- **Pre-1.0** — minor versions MAY tighten validation (make previously-valid
  instances invalid); consumers should pin minor versions.

Products declare which contract version they implement in their own
READMEs. Independent SemVer per product with a published compatibility
matrix remains the workspace-level leaning.
