<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Phase-Rules Emission — the four `memory/phases/` files

> **Load this file** during step 1 of the `aidlc/` emitter, after `memory-mapping.md` has routed the team/project rules. This is Proposal 6 (`P6`). It emits the four v2 phase-rule files from the phase-vocabulary mapping AI-GCE's `phase-gates-generator.md` authored (merged item 7). Authority for filenames/paths/front-matter: `common/aidlc-v2-output-contract.md` §2. Verified by `TR-830`.

## The emitter reads the mapping — it never re-derives it

The 5-grouping → 4-file routing is a **fixed fact on both sides** (AI-GCE has five `PG-*`/`CM-*` phase groupings; v2 exposes exactly four phase-rule files with fixed filenames). AI-GCE's `phase-gates-generator.md` is the single authority for that routing. This emitter **reads** it and produces the files; if the two ever disagree, the generator's mapping wins and this step is re-run. Re-deriving the routing here would create a second copy that drifts.

## Exactly four files — no more, no fewer

```
aidlc/spaces/<space>/memory/phases/
├── ideation.md
├── inception.md
├── construction.md
└── operation.md
```

The filenames are **fixed by contract §2 / §18** — a v2 phase rule attaches to a stage **by filename**, so a differently-named file (e.g. `integration.md`, `go-live.md`) attaches to nothing and silently governs nothing. Emit these four names verbatim; never add a fifth, never rename one to match an AI-GCE phase.

## What lands in each file (read from item 7's mapping)

| File | Receives | Originating AI-GCE grouping |
|---|---|---|
| `ideation.md` | **No AI-GCE gate rules** — emitted with a stated reason (see trap 1) | *(none — ideation precedes governance)* |
| `inception.md` | `PG-INCEP-*` (requirements spec, API contract, domain model documented) | Construction, inception half |
| `construction.md` | `PG-DOM-*`, `PG-APP-*`, `PG-PRES-*`, `PG-TEST-*` (build half) **+** `PG-CONST-*` (integration) | Construction (build half) **and** Integration — two groupings (see trap 3) |
| `operation.md` | `PG-INTEG-*` (E2E, security audit, UAT, rollback) **+** `CM-*` | Go-Live |

`PG-SETUP-*` and `PG-FOUND-*` go to **no phase file** — they are preconditions satisfied before v2's first stage, recorded in the bootstrap record and re-formed as `memory/team.md` behavioural rules (see trap 2). They are **not** dropped.

## The three traps this step must not fall into (TR-830's three negative assertions)

1. **`ideation.md` is legitimately empty of AI-GCE rules — and MUST NOT ship silently blank.** Ideation is idea-shaping, upstream of governance; AI-GCE has no gate there, and inventing one would fabricate a rule to fill a file. But §18 fixes all four filenames, so the file **is** emitted — **with a stated reason**, e.g. a single line: *"No AI-GCE phase gates apply at ideation; this phase precedes governance."* A zero-byte `ideation.md` reads as a failed generation; a reasoned one reads as a correct, deliberate emptiness. **TR-830 negative assertion (1):** `ideation.md` exists, is non-empty, and contains a reason rather than a fabricated rule.

2. **`PG-SETUP-*` / `PG-FOUND-*` having "no phase file" MUST NOT be read as "delete these rules."** They are preconditions, re-formed into the bootstrap record + `memory/team.md`, not obligations v2 re-evaluates per phase (§0.1 principle 4: re-formed, not dropped). Emitting them into a phase file would gate a running lifecycle on setup work that is already complete; dropping them entirely would lose governance the chain owns. **TR-830 negative assertion (2):** no phase file contains a `PG-SETUP-*` or `PG-FOUND-*` rule, **and** those rules are present in the bootstrap/`team.md` surface (a ledger breach if absent from both — ledger row A36).

3. **`construction.md` receives rules from TWO AI-GCE groupings** — the build half of Construction *and* all of Integration — which MUST be **grouped and labelled by originating grouping** inside the file. Without the labels, a later reader cannot tell why a cross-module event-flow gate (`PG-CONST-*`) sits beside a DTO-validation gate (`PG-APP-*`), and the next re-derivation will assume one is misfiled and "correct" it. Emit two labelled subsections (e.g. `### From Construction (build)` / `### From Integration`). **TR-830 negative assertion (3):** `construction.md`'s two source groupings are visibly separated and labelled, not merged into one undifferentiated list.

## Front-matter — mandatory on every phase file

Same rule-file block as `memory-mapping.md`:

```yaml
---
status: active
pairing: feedforward-only         # or the sensor id that verifies this file's rules
---
```

`ideation.md` carries the same front-matter even though its body is the stated-reason line — `status: active`, `pairing: feedforward-only`. An emitted-with-reason file is still a valid, active phase file.

## Ownership + reconciliation

`hybrid` — AI-DWG seeds, team and v2 amend. On Mode-2 reconciliation, preserve `<!-- custom -->` blocks and v2-appended dated learning entries; re-derive only un-hand-edited seeded content. The four filenames are stable across regenerations — never rename on reconciliation.

---

*Developer-side design detail · AI-DWG `aidlc/` phase-rules emission · © Mohammad Maheri*
