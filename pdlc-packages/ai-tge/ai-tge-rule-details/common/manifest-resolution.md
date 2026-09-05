<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Manifest Resolution — the single discovery contract for every AI-TGE stage

## Why this file exists

AI-TGE's Chain Contract declares discovery is **manifest-driven** and states **"NEVER hardcode paths."** Historically only Stage 1 honoured it — the other eleven stages read inputs from literal locations (`aidlc-docs/…`, bare steering filenames, `tests/`, `aidlc-docs/inception/user-stories/`). That is the defect this file closes.

**Every stage resolves an external input through this one contract**, rather than each stage restating the manifest shape (which would create eleven drift points — the exact anti-pattern the hook-inventory and lens-output reconciliations fought). A stage names the **semantic role** it needs; this file says which manifest key carries it, what the legacy fallback is, and — non-negotiably — that an unresolved role is a **disclosed degradation**, never a silent fall-through to a hardcoded literal.

> **Scope boundary — read this first.** This contract governs **INPUT reads only** — what AI-TGE reads from AI-DWG / AI-DLC output. It does **NOT** govern AI-TGE's own **OUTPUT writes**, which are fixed by the P3 single-home contract at `.governance/test/`, `.governance/agents/`, `.governance/engine/ai-tge/`. Output literals are correct and are never manifest-resolved.

---

## Step 0 — the discovery contract (run at the start of every stage that reads an external input)

```
1. Locate .governance/workspace-manifest.yaml (primary marker).
2. Resolve the input this stage needs BY SEMANTIC ROLE (table below) — never by a literal path.
3. If the manifest is absent      → legacy fallback: scan the fallback location + warn "legacy workspace" (a DISCLOSED degradation, not a silent read).
4. If the manifest is present but the role is absent/unresolved → ⚠️ Degraded for that input:
   disclose in all three places INV-L2-021 requires (artifact + tge-state.md + user report), per common/observation-fidelity.md.
5. NEVER read the hardcoded literal as if it were the resolved role. The literal is the fallback of last resort, and using it is itself the degradation to disclose.
```

---

## The semantic-role → manifest-key map

Every external input AI-TGE reads, the manifest key that carries it, the legacy-fallback location (used only when no manifest exists, and disclosed when used), and which stage consumes it.

| Semantic role | Manifest key | Legacy fallback location | Consumed by | On unresolved |
|---|---|---|---|---|
| **Canonical rules** (tech-stack, testing-strategy, module-structure, coding-standards, workspace-rules) | `manifest.paths.rules` | `rules/` (NOT the `.kiro/steering/` adapter) | Stages 2, 5 | ⚠️ Degraded — DW enrichment context unavailable; AP-derived requirements unaffected |
| **Backlog / user stories + ACs** | `manifest.paths.backlog` (honour `manifest.storyStyle`) | `aidlc-docs/inception/user-stories/` | Stages 2, 8 | ⚠️ Degraded — story-derived acceptance coverage is **zero, not complete** |
| **NFR / requirements carried with stories** | `manifest.paths.requirements` (or `files.requirements`) | `aidlc-docs/inception/requirements/` | Stage 8 | ⚠️ Degraded — story-carried NFR criteria unmeasured; AP-derived NFR unaffected |
| **Architecture Package** | `manifest.paths.architecture` | AP-derived reference / `architecture/` | Stages 2, 10 | ⚠️ Degraded — reconciliation cannot distinguish "AP unchanged" from "AP unreadable" (Stage 10 rule) |
| **AI-DLC build state** | `manifest.files.buildState` (AI-DLC state role) | `aidlc-docs/aidlc-state.md` | Stages 7, 12 | ⚠️ Degraded — unit completion inferred from file timestamps, not read (Stage 7 rule); Change Frequency carried forward, not recalculated (Stage 12 rule) |
| **Unit-progress vocabulary** | carried in the build-state file (`manifest.files.buildState`) | the stage names inside `aidlc-state.md` | Stage 7 | ⚠️ Degraded — per-unit stage position unavailable; stage-conditional register updates cannot fire |
| **Existing tests** (brownfield) | `manifest.paths.tests` | the test-directory/pattern set (`tests/`, `test/`, `__tests__/`, `spec/`, `*.test.*`, `*_test.*`, `cypress/`, `e2e/`, …) | Stage 4 | ⚠️ Degraded — existing-test inventory is a filesystem guess, not a declared location |
| **Platform targets** | `manifest.platformTargets` | (none — required for P2 rendering) | Agent install | render TGE's own agents per platform |
| **Governance roots** (where TGE writes) | `manifest.governance.*` | `.governance/test/`, `.governance/agents/`, `.governance/engine/ai-tge/` | all output | OUTPUT — P3 fixed; not an input read |

---

## Multi-Workspace Set (per-team topology — mode-transparent, Q-D6)

When AI-DWG generated a **per-team set** (`workspaceTopology ∈ {per-team, hybrid}`), a Layer-2 `workspace-set-manifest.yaml` lists the member L3 workspaces (each with its own per-member `.governance/workspace-manifest.yaml`). AI-TGE governs the set through the **same single discovery contract**, mode-transparently (mirrors AI-GCE):

- **Subfolder layout →** ONE AI-TGE instance iterates the members listed in the set-manifest, resolving each member's inputs through that member's per-member manifest (Step 0, unchanged, per member).
- **Polyrepo layout →** ONE AI-TGE per member repo (each self-tests) + a set-level contract/integration view read from the L2 registry.
- **Same interface both ways:** every member exposes the identical per-member manifest; TGE reads `physicalLayout` from the set-manifest ONLY to resolve each member's governance home (folder path vs repo URL). It never branches on mode beyond path resolution.
- **Contract + integration testing across the set** reads the L2 `contracts/registry.yaml` (producer/consumer + pinned versions) to derive cross-team contract tests (consumer-driven, MS-10). Per-member unit/integration testing is unchanged.
- **Single workspace:** no set-manifest → today's behavior exactly (one member).

---

## The two manifest fields that were declared but never consumed

The Chain Contract lists `storyStyle` and `clusters` as available manifest keys, but until item 6 no stage read them. Both are now wired:

### `manifest.storyStyle` — consumed by Stage 8 (Story Acceptance Mapping)

`storyStyle` names the **format** the backlog stories are written in (`ears`, `invest`, free-form, …). Stage 8 MUST branch its acceptance-criterion extraction on it rather than assuming a single fixed story structure:

| `storyStyle` | Acceptance-criterion shape Stage 8 parses |
|---|---|
| `ears` | EARS clauses — `WHEN {trigger} the system SHALL {response}`; each clause is one testable assertion |
| `invest` | Given/When/Then scenarios — each scenario is one acceptance test; compound Whens decompose |
| free-form / absent | The classic `AC1/AC2/…` bullet list under `## Acceptance Criteria` (the historical default) |

**On absent `storyStyle`:** default to free-form parsing (the historical behaviour) — this is a benign default, not a degradation, because the manifest simply did not narrow the format. The story *location* not resolving is the degradation (above); the *style* being unset is not.

---

## The Build-Engine Layout Descriptor (Observation phase — merged item 11 / Improvement 4b)

**Why this exists.** AI-TGE's Observation phase reads four things from the build engine's workspace: the build **state file**, the **story** location, the **NFR** location, and the per-unit **progress vocabulary**. These differ **by build method** — AI-DLC v1 used a flat `aidlc-docs/` tree; AI-DLC v2 uses the `aidlc/spaces/<space>/` tree with per-work-item intent records. AI-TGE historically **hardcoded the v1 layout with silent fallbacks**, so on a v2 workspace it produced a confident-looking coverage report derived from a file-timestamp heuristic with zero story coverage. The descriptor replaces those four literals with **one resolved layout per build method** — the structural half of `INV-L2-021` / TR-821 (item 1 delivered the disclosure half).

**Scope vs observation (the split item 11 corrected).** Test *scope* is delivery-method-invariant (it derives from architectural commitments). The *observation mechanism* is not — it depends entirely on the build engine's layout. So scope needs no delivery-method field; **observation resolves this descriptor.**

### Descriptor schema — four fields

| Field | What it locates | Resolved via |
|---|---|---|
| `stateFile` | the build state file (which units/stages are complete) | `manifest.files.buildState` |
| `stories` | user-story location | `manifest.paths.backlog` |
| `nfr` | non-functional-requirement location | `manifest.paths.requirements` |
| `progressVocabulary` | the per-unit stage-name set the state file uses | carried in the descriptor per build method |

### One descriptor per supported build method

| Build method | `stateFile` | `stories` | `nfr` | `progressVocabulary` |
|---|---|---|---|---|
| **`aidlc`** (AI-DLC v2) | `aidlc/spaces/<space>/intents/<record>/` build state (per the frozen output contract) — **NOT** `aidlc-docs/` (v1, does not exist in v2) | `aidlc/spaces/<space>/intents/<record>/inception/user-stories/` | `aidlc/spaces/<space>/intents/<record>/inception/requirements-analysis/` | Construction slugs **3.1–3.7** (verified current, 2026-08-31): `functional-design`, `nfr-requirements`, `nfr-design`, `infrastructure-design`, `code-generation`, `build-and-test`, `ci-pipeline` |
| `spec-driven-kiro` · `spec-driven-speckit` | the spec workflow's task/plan state (per its own convention) | the workspace `backlog/` | the workspace requirements | spec-task lifecycle states |
| `freestyle` · `manual` | no build-engine state file | the workspace `backlog/` if present | the workspace requirements if present | none — observation is register-only; no per-unit progress to read |

> ⚠️ **Vocabulary provenance.** The `aidlc` progress slugs are the **Construction phase** (v2's 33-stage vocabulary, §3.4 / §24 of the compatibility design). The 32→33-stage correction changed **Inception** names only (2.6 → Domain Design, new 2.8 Contract Design, Delivery Planning → 2.9); the Construction slugs above were untouched. **Do NOT source these from the compatibility design's cancelled §5.7 block**, which still carries pre-correction Inception names.

### Resolution + degradation

The descriptor is resolved **once** at the start of the Observation phase from `buildProfile` + the manifest roles above. When a field cannot resolve (e.g. the `aidlc` state file is absent), that is a **disclosed `⚠️ Degraded`** verdict per `observation-fidelity.md` — never a silent fall-through to the old `aidlc-docs/` literal or a timestamp heuristic. The literal v1 paths are retained **only** as the legacy fallback of last resort, and using one is itself the degradation to disclose. There is **no version pin** — the old `v0.1.8+ aidlc-docs` compatibility pin is retired.

### `manifest.clusters` — consumed by Stage 1 (Workspace Detection)

`clusters` is the manifest's own declaration of **which input groups this workspace actually has**. Stage 1 MUST consult it to decide which inputs to expect, rather than discovering presence purely by filesystem scan. Its purpose is to **skip absent inputs cleanly**: a role the manifest's `clusters` marks absent is *known-absent* (silent, a project fact), whereas a role `clusters` marks present but which does not resolve is a *degradation* (disclosed). This is exactly the fail-closed F2 distinction from `observation-fidelity.md` — "the location resolved and is empty" vs "the location did not resolve" — sourced from the manifest instead of guessed.

---

## Relationship to `observation-fidelity.md`

This file answers **"where does each input live, and what is its fallback?"** `observation-fidelity.md` answers **"how is an unresolved input disclosed?"** They are two halves of one contract: a stage resolves its input through *this* file, and when resolution fails it discloses through *that* one. A missing manifest role is an `⚠️ Degraded` verdict recorded in all three destinations — never a silent hardcoded-path read.

---

*Developer-side design detail · AI-TGE · © Mohammad Maheri*
