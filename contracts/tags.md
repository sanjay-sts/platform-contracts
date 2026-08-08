# Tag Vocabulary (v0.1)

Every platform object (agent, mcp-server, skill, prompt, app, policy,
knowledge-bundle) carries a tag set validated by `tags.schema.json`.
Tags are the shared vocabulary that feeds authorization conditions,
planner hints, scope mapping, and metering.

## Grammar

`<namespace>:<value>` — lowercase; namespace `[a-z][a-z0-9_-]*`,
value `[a-z0-9._@/-]+`. Sets are unique (no duplicate strings).

## Reserved namespaces

| Namespace | Values | Meaning |
|---|---|---|
| `risk` | `readonly`, `destructive` | Mirrors MCP `readOnlyHint` / `destructiveHint`. Anything `risk:destructive` requires a human-in-the-loop gate at intake and at invocation planning. |
| `data` | `public`, `internal`, `confidential`, `restricted` | Highest classification of data the object touches. |
| `owner` | free-form id | Accountable owner (person or team id). |
| `env` | `dev`, `staging`, `prod` | Deployment environment. |
| `cost` | `low`, `medium`, `high` | Metering hint for budget/rate policy. |

Unreserved namespaces are open for producers; consumers MUST ignore
namespaces they don't understand.

## Mandatory at intake

Intake (Draft → Submitted) requires at least one tag from each of:
`risk`, `data`, `owner`, `env`.
