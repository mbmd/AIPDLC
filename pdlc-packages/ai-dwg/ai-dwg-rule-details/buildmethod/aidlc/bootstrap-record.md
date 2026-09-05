<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Bootstrap Record Emission — `.governance/aidlc-bootstrap.yaml`

> **Load this file** during step 6 (the last step) of the `aidlc/` emitter. This is Proposal 8 (`P8`). It emits the bootstrap record per the **frozen schema** in `common/aidlc-v2-output-contract.md` §6 — the schema is the authority; this file is the emission step that populates it. Verified by `TR-822`.

## What it is, and who reads it

`.governance/aidlc-bootstrap.yaml` records **what AI-DWG did** — the recommendations it made and what it actually seeded. It lives in AI-DWG's governance area, **never inside `aidlc/`**.

**AI-DLC v2 does NOT read this file** — v2 has no bootstrap concept. Its three readers are: the **human** (to see what was set up), **AI-GCE** (to know what the tree contains and to verify sensor wiring landed — contract §7 / §7a Clause 3), and **AI-TGE** (to read the test-strategy recommendation). Writing it for v2 would be a category error; it is a hand-over note between the PDLC engines, not a v2 input.

## Why it emits LAST

Step 6 runs after steps 1–5, and that ordering is load-bearing: the `seeded:` block must record **what was actually written**, not what was intended. If code-KB self-skipped on a brownfield project (step 4), `seeded.codekb` must read `false` — and the only way to know that reliably is to write the record after step 4 has run and reported its outcome. Emitting the record early would force it to *predict* the seeded state, which drifts from reality the moment any step conditionally skips.

## Field-by-field — where each value comes from

Every field is populated from an already-resolved source, never guessed:

| Field | Value source |
|---|---|
| `bootstrapVersion` | Fixed `1` (schema version, not the package version) |
| `generatedBy` / `generatedVersion` / `generatedOn` | AI-DWG identity + version + ISO-8601 emission timestamp (standard provenance) |
| `projectId` | The project identifier already assigned upstream (`PRJ-{ABBREV}-{YYYY}-{NNN}`) — read, not minted here |
| `recommended_scope` | **Always a v2 stock scope** — `classic` for a PDLC-prepared chain. **Never a custom scope.** The rationale + the `/aidlc --scope classic` workspace start instruction are owned by `scope-recommendation.md` (merged item 18); this record carries the field. |
| `recommended_depth` | v2's **scope depth** (report/output verbosity for the run) — `minimal` / `standard` / `comprehensive`, from the depth the chain implies |
| `recommended_test_strategy` | v2's **test volume** (tests-per-requirement/component) — `minimal` / `standard` / `comprehensive`. From **AI-TGE's advice when active**, else inherited from `recommended_depth` as a *v2-internal* default. ⚠️ This is v2's test-volume field; it is **NOT** AI-TGE's own test-governance depth (a different concept — see the two-field rule below). |
| `tge_governance_depth` | **AI-TGE's test-governance depth** (how much detail AI-TGE's own engine produces + which of its 12 stages run) — `minimal` / `standard` / `comprehensive`. Present only when AI-TGE is active. **Independent of `recommended_test_strategy`** — auto-scored from five system-complexity factors, carries no test-volume commitment (merged item 22, ledger B13). |
| `project_type` | `greenfield` / `brownfield` — the same resolved field code-KB seeding (merged item 15) reads; set once, read everywhere |
| `pdlc_chain_completeness` | Per upstream package: `complete` / `partial` / `absent` — reflects which chain members actually produced input (`dwg: complete` always, since AI-DWG is running) |
| `seeded` | **Recorded from the actual outcome of steps 1–5** (see below) — the reason this step runs last |
| `waivers` | `peerCoverage` (full/partial — was every expected upstream present?) + `enforcementCoverage` (full / advisory-only — did any enforcement fall back to advisory?) |

## The `seeded:` block — recorded, not predicted

| Key | Set to | From the step |
|---|---|---|
| `memory` | `true` | Step 1 always writes `memory/` under `aidlc` |
| `phases` | `true` | Step 1 (`phase-rules.md`) always writes the four phase files |
| `knowledge` | `true` \| `false` | Step 2 — `true` if any agent directory got content, else `false` (conditional emission) |
| `documents` | `true` \| `false` | Step 3 — `true` if any narrative document was placed |
| `codekb` | `true` \| `false` | Step 4 — `false` on brownfield or when AI-ADLC is absent (merged item 15) |
| `sensors` | `manifests-only` \| `wired` \| `none` | Step 5 — `manifests-only` after AI-DWG emits manifests + the wiring file (AI-DWG never applies the wiring); becomes `wired` only once the team applies it and AI-GCE confirms |

`sensors: manifests-only` is the honest default: it tells AI-GCE the manifests exist but stage wiring has not been applied, so AI-GCE **reports on that** rather than assuming the checks are live (contract §6 / §7).

## Test-governance depth vs test volume — two independent fields, never one (merged item 22, ledger B13)

`tge_governance_depth` and `recommended_test_strategy` share all three value names (`minimal` / `standard` / `comprehensive`) but mean **different things**, so **neither is derived from the other** (design §8.6 — the mapping between them is not semantically valid):

| | `tge_governance_depth` (AI-TGE's depth) | `recommended_test_strategy` (v2's test strategy) |
|---|---|---|
| **Controls** | How much detail AI-TGE's engine produces + which of its 12 stages run | Test **volume** (tests per requirement / per component) |
| **Chosen by** | Auto-scoring five system-complexity factors (components, integrations, security surface, data complexity, team size), 5–25 points | Selected as a testing budget, or inherited from the scope's depth |
| **Volume commitment** | **None** — only per-commitment hints ("2–4 tests per API endpoint") | Explicit — 1 per requirement · 5–8 per component · 10–15 per component |

A complex system scores AI-TGE **Comprehensive** (fuller reports, more stages) — which says **nothing** about wanting 10–15 tests per component. A team could legitimately want AI-TGE Comprehensive with v2 test-strategy Minimal. So the two are recorded as **independent bootstrap fields**, and generated output disambiguates the label: **"test-governance depth"** (AI-TGE) versus **"test volume strategy"** (v2). When AI-TGE is inactive, `tge_governance_depth` is absent and `recommended_test_strategy` falls back to v2's own scope-depth default — never to a nonexistent AI-TGE depth.

## Provenance header — do-not-edit

The record carries the `# Generated by AI-DWG — DO NOT EDIT MANUALLY` header from the frozen schema. It is `generated`-owned: on Mode-2 reconciliation AI-DWG rewrites it from the current outcome (it is a status record, not a hand-editable rule file — the one file in the tree that is safe to fully regenerate, because it asserts nothing a human authored).

## Ownership

`generated` — AI-DWG owns it end-to-end and regenerates it on every run. Unlike the `hybrid` tree files, there is no team content to preserve here: it is a factual record of the generation, so a full rewrite on reconciliation is correct, not destructive.

---

*Developer-side design detail · AI-DWG `aidlc/` bootstrap record · © Mohammad Maheri*
