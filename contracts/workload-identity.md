# Workload Identity (v0.1)

The registry is the issuer of workload identities. An identity is minted
when an object passes intake (state `Approved`) — never before.

- **Principals:** `user`, `agent`, `mcp-server`. Agents and MCP servers are
  first-class principals in authorization policy, not anonymous workloads.
- **Credential types:**
  - `bearer-token` — default for v0.1 open-source deployments (TLS + token).
  - `client-credentials` — OAuth2 client-credentials grant for services.
  - `x509-svid` — SPIFFE-style X.509 identity. **v0.1 defines the shape
    only**; mTLS issuance/rotation is a later multi-host deployment
    feature. The hook exists now so the schema never breaks when it lands.
- **Tags** on an identity follow `tags.md` and feed authorization
  conditions (e.g. deny `risk:destructive` invocation without a HITL gate).

Authorization semantics (which principal may invoke which tool) are
policy-engine concerns (Cedar in the server product) and are intentionally
out of scope for this contract; this file defines only the identity shape
exchanged between engines.
