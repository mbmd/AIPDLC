# SOURCE_MAP — AI-DWG

> Declares where AI-DWG's raw output lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`. AI-DWG is a one-time generator — it has no `*-state.md`; its marker is the generated `workspace-rules.md`.

**Package:** AI-DWG — AI-Driven Workspace Generator
**Schema:** `dwg-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** per-project (the generated dev workspace = one project)

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/rules/workspace-rules.md` | `status: not-run` → the dev workspace hasn't been generated; payload `null` |

> AI-DWG output is the generated dev workspace, opened separately. From the planning workspace (`pdlc-ws/`) it is reachable at `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/`.

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/rules/workspace-rules.md` | provenance front-matter + Identity Assembly (Project ID, system/product identity), steering header |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `projectId` | 1 | Identity Assembly → `Project ID` line (immutable correlation key) |
| `generatedBy` | 1 | Front-matter `generatedBy` (= AI-DWG) |
| `generatedVersion` | 1 | Front-matter `generatedVersion` |
| `generatedOn` | 1 | Front-matter `generatedOn` |
| `source` | 1 | Front-matter `source` (upstream AP artifact) |
| `identityType` | 1 | Which identity block is present: `architecture` (ADLC) \| `product` (POLC-only) \| `none` (UXD-only) |
| `systemName` | 1 | Architecture Identity → `System` (if identityType = architecture) |
| `architectureStyle` | 1 | Architecture Identity → `Architecture style` |
| `primaryTechnology` | 1 | Architecture Identity → `Primary technology` |
| `deploymentModel` | 1 | Architecture Identity → `Deployment model` |
| `productName` | 1 | Product Identity → `Product` (if identityType = product) |
| `workspaceGenerated` | 1 | `true` if marker exists |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- DWG is a generator with no state file. Its "data" is the fact that a dev workspace exists + the identity it embedded. This lets a dashboard show "workspace generated: yes/no" and the tech identity.
- The full steering set (tech-stack, coding-standards, etc.) inside `{slug}-workspace/rules/` is not machine-extracted — too varied. DFE captures the identity block, which is the structured, predictable part.
- `workspace-rules.md` carries `ownership: hybrid` — teams edit it. DFE reads it read-only and never writes back.

---

## AI-LENS Fields (AI_LENS_PROTOCOL §6.2)

> Present when the generated workspace was scaffolded for a project with AI features. DWG acts as the courier — it carries AI context across the DWG hinge.

| Field path (in `data`) | Source | Extraction rule |
|------------------------|--------|-----------------|
| `aiLens.aiFeaturesCouriered` | Generated workspace `data-schema/` or AI feature manifest | Count of distinct `aiFeatureId` values couriered. `null` if no AI features. |
| `aiLens.aiFeatureIds[]` | Generated workspace AI feature manifest | List of `AIF-{NNN}` IDs couriered into the workspace. |
| `aiLens.aiScaffoldingGenerated` | Generated workspace file scan | `true` if AI-specific scaffolding files exist (eval harness, prompts/, LLM client, vector-DB config). |
| `aiLens.aiContextCouriered` | Generated workspace AI context manifest | `true` if the full AI-feature context (AC + architecture + EU-AI-Act) was carried across the hinge for `AIG__`/`AIQ__`. |

> **Source:** The generated workspace (`{slug}-workspace/`) — AI feature manifest + scaffolding files presence check.


## Automation-LENS Fields (AUTOMATION_LENS_PROTOCOL §6.2)

> Present when the workspace was generated for a project that has automation features.

| Field path (in `data`) | Source | Extraction rule |
|------------------------|--------|-----------------|
| `automationLens.automationFeaturesCouriered` | workspace-manifest or automation-context files | Count of automation features couriered into this workspace. `null` if no automation features. |
| `automationLens.automationFeatureIds` | workspace-manifest or automation-context files | Array of `automationFeatureId` values couriered (`AUTO-{NNN}`). Empty array if none. |
| `automationLens.automationScaffoldingGenerated` | workspace file structure | `true` if automation-specific scaffolding (engine config, scheduler, queue, connector stubs) was generated; `false`/`null` otherwise. |
| `automationLens.automationContextCouriered` | automation-context files | `true` if the full automation-feature context (AC, architecture, control-class) was couriered for `ATG__`/`ATQ__`; `false`/`null` otherwise. |

> **Source:** Generated workspace identity + automation-feature manifest/context files placed by AI-DWG during generation.
