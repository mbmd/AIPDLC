<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Code-KB Seeding — 7 of 9 artifacts, greenfield only

> **Load this file** during step 4 of the `aidlc/` emitter. Authority: `common/aidlc-v2-output-contract.md` §5. Establishes the emitter call site, the seeded set, the two hard prohibitions, the per-artifact derivation, and the greenfield-detection wiring (merged item 15).

## Location

`aidlc/spaces/<space>/codekb/<repo>/<canonical-name>.md` — keyed **per repository**, shared across all work items (not per work item).

## Conditions — both must hold

1. **Greenfield only.** On brownfield, **nothing is seeded** — v2's Reverse Engineering stage runs against real code. Seeding a brownfield code KB would fabricate a picture of code that already exists and should be scanned.
2. **AI-ADLC present** among the upstream packages (the seeded artifacts derive from AP content).

When either condition fails, step 4 emits nothing and the bootstrap record's `seeded.codekb` is `false`.

## Greenfield detection — where the greenfield/brownfield decision comes from

The emitter does **not** re-derive greenfield vs brownfield. It reads the single authoritative field that the bootstrap record already carries: **`project_type: greenfield | brownfield`** (contract §6). That field is itself set from the AI-ADLC input-mode / project-context the workspace generation already established — the same fact that drove whether AI-DWG scaffolded a fresh `src/` tree or reconciled against existing code. Reading one resolved field (rather than re-inferring from file presence) keeps the codekb decision and the rest of the generated workspace consistent: they cannot disagree about whether the project is greenfield.

- `project_type: greenfield` **and** AI-ADLC present → seed the 7 artifacts, set `seeded.codekb: true`.
- `project_type: brownfield` → seed nothing, set `seeded.codekb: false`, and the generated workspace instructions state that v2's Reverse Engineering will run against real code.
- AI-ADLC absent → seed nothing (no source), `seeded.codekb: false`.

## The seeded set — 7 of 9

| Canonical artifact | Seeded | Source |
|---|:---:|---|
| `business-overview` | ✅ | AI-POLC product vision + scope & risks |
| `architecture` | ✅ | AI-ADLC C4 context & container views |
| `code-structure` | ✅ | AI-DWG's generated source scaffold + canonical module-structure rules |
| `component-inventory` | ✅ | AI-ADLC C4 level-3 component design |
| `technology-stack` | ✅ | AI-ADLC technology-stack decision record |
| `dependencies` | ✅ | AI-ADLC integration architecture |
| `api-documentation` | ✅ | AI-ADLC API architecture |
| `code-quality-assessment` | ⛔ **NEVER** | Records a real code scan — a fabricated value is a false quality claim |
| `reverse-engineering-timestamp` | ⛔ **NEVER** | Records **when** a scan ran — a fabricated timestamp can cause v2 to **skip a needed scan** |

## Why the two ⛔ artifacts are never seeded — this is a correctness rule, not a scope choice

Both record **facts about a scan that has not happened** on a greenfield project. `code-quality-assessment` would assert quality that was never measured; `reverse-engineering-timestamp` would tell v2 a scan already ran, so v2 skips the scan the project actually needs. Seeding either is worse than omitting it — the omission is visible (v2 runs the scan), the fabrication is silent (v2 trusts a lie). Guarded by `INV-L3-042` (reserved never-write targets) and verified by TR-819 / TR-822.

## Per-artifact derivation — exactly which upstream sections map into each seeded file

Each seeded artifact is **reshaped** from a named upstream section, never authored fresh. Where the named source section is absent, the artifact is written with the content that *is* present plus an inert `<!-- affirm: … -->` marker (the same honest-thin-section discipline as `practices-preseeding.md`), never fabricated — a fabricated code-KB entry is the same class of error as the two ⛔ prohibitions, just less severe.

| Artifact | Reshaped from | What lands in the file |
|---|---|---|
| `business-overview` | AI-POLC product vision + scope-and-risks | Product purpose, target users, in/out-of-scope statement, top risks — the "why this system exists" a code reader needs |
| `architecture` | AI-ADLC C4 **context + container** views | System context (external actors, boundaries) + container decomposition (deployable units and their responsibilities) |
| `code-structure` | AI-DWG's **own generated `src/` scaffold** + canonical module-structure rules | The directory/module layout AI-DWG just scaffolded, plus the module-boundary rules that govern where new code goes |
| `component-inventory` | AI-ADLC C4 **level-3 component** design | Per-container component list: each component's responsibility, its interfaces, and its dependency rules |
| `technology-stack` | AI-ADLC technology-stack decision record | Selected languages, frameworks, datastores, and the recorded reason for each (the ADR-style justification, not just the name) |
| `dependencies` | AI-ADLC **integration architecture** | External systems and internal cross-container dependencies — what talks to what, over which protocol/contract |
| `api-documentation` | AI-ADLC **API architecture** | Endpoint/operation catalogue, request/response contracts, versioning and error conventions |

**The distinction between `architecture` and `component-inventory` is the C4 level.** `architecture` carries C4 L1–L2 (context + container — the coarse shape); `component-inventory` carries C4 L3 (the fine-grained component breakdown inside each container). Emitting the same content into both would duplicate and drift; the split follows AI-ADLC's own C4 layering.

## Front-matter — "designed, not observed" must stay visible

Standard provenance block, `ownership: generated`, and every seeded file names **AI-DWG as generator** and the **specific AI-ADLC document** it was reshaped from. This is not decorative: the seven seeded files sit in the **same directory** a later real Reverse-Engineering scan writes into, so without provenance a reader cannot tell a designed artifact from an observed one. The team owns the KB after generation; v2 updates it during Reverse Engineering on later brownfield cycles, at which point observed content supersedes the seeded (designed) content for the same artifact.

---

*Developer-side design detail · AI-DWG `aidlc/` code-KB seeding · © Mohammad Maheri*
