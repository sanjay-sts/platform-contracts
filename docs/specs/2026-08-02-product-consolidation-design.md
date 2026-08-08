# Product Consolidation Design — Two Products, One Protocol

**Date:** 2026-08-02
**Status:** Approved in brainstorming/grilling session; awaiting spec review
**Scope:** Consolidate the 5 FoundryCore repos (excluding `deeppockets`, which is unrelated) into two open-source products plus a contracts repo, with a commercial tier to follow.

---

## 1. Goals and drivers

Three drivers, weighted equally:

1. **Coherent public story** — an open-source launch that visitors understand in one sentence.
2. **Sustainable maintenance** — one maintainer; fewer live surfaces.
3. **Commercial path clarity** — a visible, defensible seam between free and paid.

The launch story: *"Chat with your server's agents from any browser or phone; sync skills and knowledge to your laptop and go fully offline; vibe-code an app locally and ship it to your server in one click."*

## 2. Product structure

| Repo | Fate |
|---|---|
| `agentprint` | **Product 1 — server platform.** Python engine + web UI (chat + management), reachable from any browser/phone on the network. Absorbs POCForge's vibe-coding pipeline, SkillHub's skill serving, and the entraid POC's Cedar/identity patterns. |
| `sts-adk-go-local-install-agent` | **Product 2 — desktop platform.** Fully sovereign offline Go engine (Wails). Rename pending branding. |
| **New: contracts repo** | The treaty both products implement: registry sync API, app deploy push API, A2A agent-card profile, tag vocabulary, workload-identity schema (X.509-capable), OKF serving conventions. Schema-first, versioned, Apache 2.0. |
| `sts-entraid-single-a2a-adkagent-mcp-poc` | Archived when Cedar/identity patterns graduate into agentprint. README points to destination. |
| `sts-local-draftbox-poc` | Archived when vibe-coding pipeline graduates into agentprint. README points to destination. |
| `sts-mcp-skills-fastmcp3-poc` | Archived when skill-serving graduates into agentprint's registry. README points to destination. |

POCs are archived **when ready** — after their patterns have graduated, not before.

## 3. Architecture: one platform contract, two engine implementations

Rejected framing: "one engine, two interfaces" (the desktop is not a thin interface — its offline/air-gapped value requires local execution).

Adopted framing:

- The **"engine" is a protocol surface** — the contracts repo (A2A + MCP + registry/deploy/identity schemas), not a single codebase.
- **agentprint** is the *server* engine (Python/FastAPI/SurrealDB), with its web UI as the native interface.
- **Desk agent** embeds a *local* engine (Go/ADK/Postgres+pgvector), with the Wails desktop UI as its native interface. Fully functional with zero network.
- Federation principle preserved: every agent remains a standalone container with its own A2A endpoint; state flows via message-passing.

## 4. Platform objects

Seven registry object types: **agents, MCP servers, skills, prompts, apps, policies, knowledge bundles.**

- Skills follow the agentskills.io pattern (SkillHub's serving model graduates into agentprint's registry).
- Knowledge bundles use **Google's Open Knowledge Format (OKF)** — directories of Markdown + YAML frontmatter, no embeddings in the bundle. Each engine builds its own local embedding index (SurrealDB server-side; pgvector on desktop). OKF's trust/lifecycle frontmatter (`generated`, `verified`, `sources`, `status`, `stale_after`) is adopted as-is. Native OKF support is a launch differentiator (spec is v0.2, ~2 months old, no established server ecosystem).

## 5. Desktop ↔ server integration

Four flows on the roadmap; **v1 builds flows 1 and 2 only**:

1. **Registry pull** (server → desktop): skills, prompts, agent definitions, knowledge bundles synced for offline use. One-directional in v1 — server is source of truth; desktop never pushes registry objects back. "Publish from desktop" is a named, deferred v2 feature.
2. **App deploy push** (desktop → server): vibe-coded app ships to agentprint for hosting.
3. **Remote agent invocation (A2A)** — deferred; requires the full identity-propagation story.
4. **Policy/identity push** (server → desktop) — deferred; commercial tier.

**Desktop sign-in:** browser-based OAuth 2.1 PKCE against agentprint (the Claude Code / Amazon Q pattern). agentprint brokers all IdPs; the desktop never contains per-IdP code. Air-gapped desktops use local accounts, no IdP. Desk agent's Phase 7 MCP auth pyramid already implements PKCE machinery.

## 6. Vibe-coding

- Graduates into **agentprint at launch** (POCForge pipeline: OpenCode subprocess management, chat-to-code UI, live preview, three deploy modes).
- Behind a **thin coding-backend adapter**: start session, send prompt, stream events, get changed files. OpenCode is the sole launch implementation; the seam enables user-selectable coding tools later (Claude Code CLI, Aider, …) and is a contributor entry point.
- **Desktop vibe-coding is deferred** to a later phase (the partial Go implementation is parked). Reuses the adapter contract once agentprint has productized it.
- **Ollama is a first-class optional provider in both engines**: offline chat + embeddings on desktop (makes air-gapped real); provider option via the adapter and AI-assist creation flows (agents/MCP/skills/prompts) in agentprint.

## 7. Identity and governance

Patterns adopted from AWS Loom and LiteLLM ("best of both, not the platforms" — Loom is AgentCore-centric; our stack stays Cedar/FastAPI/SurrealDB):

- **Three Cedar principal types:** `User`, `Agent`, `MCPServer`.
- **Tools are Cedar resources** (e.g. `Tool::"github/delete_repo"`) → tool-level restriction per role/agent. (entraid POC's `require_cedar()` proves this.)
- **Workload identity:** the registry issues stable IDs + client credentials to agents and MCP servers at intake approval — never before.
- **Mandatory tagging** (Loom pattern): `readonly`/`destructive`, data classification, owner, environment. Tags feed Cedar conditions, planner hints, and scope mapping (desk agent's Phase 7 tag bag becomes the shared vocabulary).
- **Intake state machine:** Draft → Submitted → automated checks (manifest validation, tool-annotation scan, image scan) → Approved → Deployed → Deprecated. HITL gate on destructive-tagged capabilities.
- **Metering separate from authorization** (LiteLLM pattern): virtual keys per agent with model allowlists, budgets, rate limits. Cedar answers "may this principal invoke this tool"; LiteLLM answers "at what cost ceiling."
- **mTLS:** contracts define workload identity as expressible as X.509 client cert (SPIFFE-style), not just bearer tokens — schema hook now; implementation is a commercial multi-host deployment feature. OSS v1: TLS everywhere + workload tokens. Desk agent already speaks mTLS client-side.

## 8. Open source / commercial split

| Open source (Apache 2.0) | Commercial (closed, separate private repo) |
|---|---|
| Local users + API keys, single OIDC provider | Multi-IdP dispatch (Entra + Cognito + …) |
| Cedar RBAC (tool-level), three principals | Cedar ABAC on runtime attributes (`X-Abac-Attrs` chain) |
| Workload identity + tagging | RFC 8693 delegation chains, OBO token exchange |
| Single-admin intake (register → validate → approve) | Multi-stage approval workflows, audit trails |
| Desktop local-only ACL | Policy/identity push to desktops (flow 4) |
| TLS + workload tokens | mTLS multi-host deployments |
| — | Budget/rate-limit enforcement |

**Licensing:** Apache 2.0 for both product cores and the contracts repo (contracts must be maximally permissive). Contributions under **DCO** (not CLA). Commercial modules are separable from day one — the OSS repos never contain paid code. **Trademark on the eventual brand is the real moat**; register it.

## 9. Sequencing

- **Phase 0 — Foundations.** Contracts repo v0.1 drafts (tag vocabulary, registry sync, deploy push, agent-card profile, workload-identity schema). GitHub org creation. *Branding decision gates launch, not build.*
- **Phase 1 — agentprint: unified registry + chat.** Absorb SkillHub; add prompts + OKF knowledge bundles; ship chat surface in web UI.
- **Phase 2 — agentprint: identity core.** Cedar RBAC, three principals, workload identity issuance, tagging, single-admin intake. (Deliberately before vibe-coding: no auth retrofit on a public API.)
- **Phase 3 — agentprint: vibe-coding.** Coding-backend adapter + OpenCode implementation; POCForge pipeline + deploy modes fold in.
- **Phase 4 — Desktop integration.** Flows 1+2, PKCE login, Ollama provider + local embedding index, desktop renamed under new brand.
- **Public launch gate: end of Phase 4** — the integrated demo is the story. Repos stay public during the build; the announcement waits.
- **Commercial modules begin only after launch traction.**

## 10. Open items (decisions only Sanjay can make)

- Brand / GitHub org name (gates launch; register trademark).
- Desk agent product name.
- Timing of each POC's archive (owner's call, "when ready").

## 11. References

- OKF spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- OKF announcement: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- AWS Loom: https://github.com/awslabs/loom/ · https://aws.amazon.com/blogs/opensource/building-secure-ai-agents-at-scale-introducing-loom-for-aws/
- LiteLLM virtual keys/budgets: https://docs.litellm.ai/docs/proxy/users
- IAM Identity Center PKCE: https://aws.amazon.com/about-aws/whats-new/2024/05/aws-iam-identity-pkce-authorizations-aws-applications/
- Claude Code auth: https://code.claude.com/docs/en/authentication
