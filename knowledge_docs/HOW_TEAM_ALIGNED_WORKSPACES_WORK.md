# How Team-Aligned Workspaces Work

**Purpose:** Explains how the AI-* PDLC Family models Team Topologies and generates one clean, contract-first workspace **per team** — a Layer-2 control plane that owns the shared contracts and Layer-3 per-team workspaces that consume them — via the DEFINE → GENERATE → ENFORCE relay across AI-Driven Architecture Design Life Cycle (AI-ADLC), AI-Driven Product Ownership Life Cycle (AI-POLC), AI-Driven UX Design (AI-UXD), AI-Driven Workspace Generator (AI-DWG), and AI-Driven Governance & Compliance Engine (AI-GCE).

---

## Who This Is For

Organizations designing around **Team Topologies** — stream-aligned, platform, enabling, and complicated-subsystem teams — who want each team to own an isolated workspace rather than sharing one large monorepo, while keeping the seams between teams governed and safe.

---

## The Default Is Unchanged

This is a fully **opt-in** capability. If you do nothing, AI-DWG generates the single monorepo workspace it always has. Team-aligned generation only happens when you choose it, and only when the architecture justifies it — so existing single-workspace projects are unaffected.

---

## The Two-Layer Model

Team-aligned generation splits a project into two layers with a strict one-way boundary:

- **Layer 2 — the control plane** (`{slug}-management/`). The management surface the architects and owners work in. It holds the **authoritative contract registry**, the **workspace-set manifest** listing every team workspace, and a set-level context map. It is not a development workspace — no code, no companion engines live here.
- **Layer 3 — the per-team workspaces** (`{slug}-workspaces/{team}/`). One clean, self-contained workspace per team, each with its own tri-input slice, its own guardrails, and a **read-only, version-pinned copy** of only the contracts that team produces and consumes.

The boundary is one-way: **Layer 2 pushes guardrails and contracts down, and reads team status down; Layer 3 never reaches up.** Maximum management sits in Layer 2; Layer 3 stays a clean place to build.

---

## DEFINE → GENERATE → ENFORCE

The capability is delivered across the chain rather than bolted on in one place.

### DEFINE — mint the shared identities

- **AI-ADLC** gains an opt-in **`team-topologies`** extension (rule prefix `TT-`) that models the team types and interaction modes and aligns them to the architecture (Conway's Law made explicit). It mints a shared identity vocabulary — `TEAM-*` (teams), `BC-*` (bounded contexts), `SVC-*` (services) — that the rest of the chain references.
- **AI-POLC** promotes **Owning Team** and **Bounded Context** to first-class fields on epics, so the backlog is partitionable by team.
- **AI-UXD** adds an opt-in `BC-*` / `TEAM-*` tag on flows, journeys, and wireframes, with a persona → epic → bounded-context fallback so UX work routes to the right team.

### GENERATE — build the control plane and the team workspaces

AI-DWG's **Config Gate Q4** asks the workspace topology (offered only when the architecture justifies it):

| Choice | `workspaceTopology` | Result |
|--------|---------------------|--------|
| Single workspace / monorepo | `single` | Today's behavior — one workspace, unchanged (**default**) |
| Per-team workspaces | `per-team` | N isolated team workspaces + the L2 control plane |
| Hybrid | `hybrid` | A monorepo core plus extracted team workspaces |

A sub-question sets the physical layout — `subfolder` (a monorepo of workspaces) or `polyrepo` (separate repositories). On `per-team` or `hybrid`, AI-DWG:

1. Partitions the tri-input (Architecture Package + Product Backlog Package + UX Package) by `TEAM-*`.
2. Builds the **workspace-set manifest** (`{slug}-management/workspace-set-manifest.yaml`) — the authoritative index of every member workspace.
3. Builds the **contract registry** (`{slug}-management/contracts/registry.yaml`) — every shared contract with exactly one owning team, a version, and its consumers — and pushes a **read-only, version-pinned copy** of the relevant contracts into each team's `contracts/` folder.
4. Generates each team workspace with a **`TEAM_CHARTER.md`**, its tri-input slice, a team-scoped relevance map, and the same four-layer anti-drift guardrails every workspace gets.

Contract-first is the seam: **the only sanctioned coupling between isolated team workspaces is a published, versioned contract.** A team cannot edit a contract it does not own; a need to change a shared contract surfaces as drift that Layer 2 observes and re-governs, after which AI-DWG re-pushes the updated copy.

### ENFORCE — govern the seams

**AI-GCE** extends its rule set with `GOV-TT-008/009/010`:

- **Contract compatibility** at the gate — a change that breaks a consumed contract is caught.
- **No cross-workspace source import** — a team workspace may depend on another team only through a published contract, never by reaching into its source.
- **Interaction-mode conformance** — the actual dependencies match the declared Team Topologies interaction modes.

AI-GCE produces a **cross-workspace roll-up** by reading each member workspace *down* from Layer 2 — the governance view lives in the control plane, consistent with the one-way boundary.

---

## Where Things Live

```
{project_root}/
├── {slug}-management/                 ← Layer 2 control plane (architects/owners)
│   ├── workspace-set-manifest.yaml    ← authoritative list of all team workspaces
│   ├── contracts/registry.yaml        ← authoritative contract registry (owning team + version + consumers)
│   └── WORKSPACE_SET_CONTEXT_MAP.md   ← single-pane index across the set
└── {slug}-workspaces/                 ← Layer 3 per-team workspaces
    ├── {team-a}/
    │   ├── TEAM_CHARTER.md            ← this team's mandate + boundaries
    │   ├── contracts/                 ← read-only, version-pinned copy (produces + consumes only)
    │   └── … (full clean workspace)
    └── {team-b}/ …
```

*(`{slug}` and `{team}` are placeholders filled at generation time — e.g. `PRJ-ACME-2026-001`.)*

---

## What Stays the Same

- Single-workspace generation is untouched and remains the default.
- Team-aligned generation reuses the existing chain — the same tri-input, the same guardrails, the same companions — partitioned per team rather than replaced.
- Team Topologies is an opt-in extension; declining it costs nothing.

---

## Related Documents

| Document | Location |
|----------|----------|
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How to Prepare a Development Workspace | `knowledge_docs/HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md` |
| How POLC Product Ownership Works | `knowledge_docs/HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |

*Knowledge Document | Created: 2026-09-05 | Updated: 2026-09-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
