# A2A Agent-Card Profile (v0.1)

Every agent in the platform is a standalone container with its own A2A
endpoint and publishes a card at `/.well-known/agent-card.json`. This
profile adds platform constraints on top of the upstream A2A card; extra
upstream fields are permitted and ignored by this validation.

Rules:

- `description` is the **routing** description — used to decide whether a
  task should go to this agent. It is never the agent's instruction /
  system prompt; conflating the two is a known anti-pattern.
- `x-platform.identity_id` binds the card to the workload identity the
  registry issued at intake (`workload-identity.md`). Consumers resolve
  the id against the registry before trusting the card.
- `x-platform.tags` follow `tags.md` and MUST include the mandatory
  intake namespaces (`risk`, `data`, `owner`, `env`).

Remote invocation (flow ③) is deferred; this profile exists now so both
engines publish compatible cards from day one.
