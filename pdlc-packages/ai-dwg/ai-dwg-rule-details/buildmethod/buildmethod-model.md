<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Build-Method Subsystem — model & the seam to `rendering/`

> **Load this file** whenever AI-DWG generates and the workspace manifest's `buildProfile` calls for a build-method-specific output surface. This is the subsystem contract; the per-method emitters live under `aidlc/` and `speckit/`.

## What this subsystem is

`buildmethod/` is a **new subsystem sibling to `rendering/`**. The two key off different manifest fields and answer different questions:

| Subsystem | Keys off | Question it answers |
|---|---|---|
| `rendering/` (existing, unchanged) | `platformTargets` | "How do I wire the one canonical rule set into each AI platform (Kiro/Claude/Cursor/Codex/Generic)?" |
| `buildmethod/` (this, new) | `buildProfile` | "Does this build method need an extra output surface beyond the workspace, and if so, what shape?" |

**The renderer is NOT modified.** It stays at **seven output categories** and five thin adapters. This subsystem does not add an eighth renderer category — see "Why a separate subsystem" below.

## Why a separate subsystem, not an eighth renderer category

The renderer's governing invariant is that adapters are **thin wiring** that point back at the canonical `rules/`, and that **no adapter ever contains original rule text**. The `aidlc/` tree breaks that invariant on its face:

- The behavioural-rules files (`memory/team.md`, `memory/project.md`, the phase files) are a **freshly derived prescriptive extract** — new content produced by transformation.
- The per-agent knowledge files are **freshly written reference summaries** — also new content, not pointers.

Housing these in the renderer would require rewriting the invariant that makes the renderer coherent. So they live here. (Full rationale + the two rejected alternatives: compatibility design §16 Decision 1.)

## The dispatch — which emitter runs

Read `buildProfile` from `.governance/workspace-manifest.yaml` (the five valid values are fixed by the frozen contract). Dispatch:

| `buildProfile` | Emitter | Emits |
|---|---|---|
| `aidlc` | `aidlc/emitter.md` | the full `aidlc/` tree — behavioural rules, per-agent knowledge, narrative documents, code KB (greenfield), sensor manifests + wiring file, bootstrap record |
| `spec-driven-speckit` | `speckit/emitter.md` | `.specify/memory/constitution.md` — a principle-level constitution that **references** the canonical `rules/`, never duplicates them |
| `spec-driven-kiro` | — | no build-method surface; the workspace's Kiro steering *is* the surface |
| `freestyle` | — | no build-method surface; a rules doc only |
| `manual` | — | no build-method surface; names the previously-implicit unset state |

**The everything-it-emits invariant:** every file this subsystem writes under the `aidlc/` tree conforms to the **frozen output contract** `common/aidlc-v2-output-contract.md`. That contract is the authority for paths, filenames, front-matter, the sensor-manifest field set, the code-KB seeded set, and the bootstrap schema. This subsystem is the *producer*; that file is the *contract*.

## The seam to `rendering/` — path resolution only

The `aidlc/` tree is **tool-neutral**: `memory/`, `knowledge/`, `documents/`, and `codekb/` sit at fixed paths with no platform involvement. **Only sensor manifests** are tool-scoped (they live under the platform-specific sensors directory). For those — and only those — the emitter calls the active platform adapter as a **path-resolution service**: it asks "where does a tool-scoped file go for this platform?" and writes there.

The renderer gains **no new category and no new responsibility** beyond exposing that path lookup. This is the entire seam.

## Emission trigger

The build method being `aidlc` (or `spec-driven-speckit` for the SpecKit emitter). Per §16 Decision 2, `buildProfile` is asked explicitly on first generation and confirmed on every regeneration — a build-method change can add or remove a whole output tree, so it is never inferred silently.

## Reconciliation (Mode 2)

The `aidlc/` tree is `hybrid`-owned: AI-DWG seeds it, and both the team and v2's learning loop write into it afterward. On regeneration, the emitter's reconciliation treats the tree as **team-modified** and preserves additions (the same non-destructive merge AI-DWG applies to canonical `rules/`). Never overwrite a `<!-- custom -->` block or a v2-appended dated learning entry.

## Files in this subsystem

```
buildmethod/
├── buildmethod-model.md        ← this file — subsystem contract + seam to rendering/
├── aidlc/
│   ├── emitter.md              ← orchestrates the aidlc/ tree emission
│   ├── memory-mapping.md       ← canonical rules/ → memory/{team,project}.md + phases/
│   ├── practices-preseeding.md ← team.md five-section completeness (Proposal 3, Stage 2.2 fast-affirm)
│   ├── phase-rules.md          ← the four memory/phases/ files from item 7's mapping (Proposal 6, 3 emission traps)
│   ├── knowledge-routing.md    ← which content goes to which agent directory
│   ├── documents-placement.md  ← full narrative docs → knowledge/documents/
│   ├── codekb-seeding.md       ← 7 of 9 artifacts, greenfield only (per-artifact derivation + greenfield detection)
│   ├── sensor-manifests.md     ← manifest emission + wiring instruction file (renders FROM the neutral intermediate; item 25 complete)
│   ├── bootstrap-record.md     ← .governance/aidlc-bootstrap.yaml (Proposal 8, emits last — seeded: records actual outcome)
│   ├── scope-recommendation.md ← recommended_scope: classic field + /aidlc --scope classic start instruction (Proposal 4)
│   └── templates/
│       └── aidlc-tree.md       ← output templates for the tree
└── speckit/                    ← the SpecKit emitter leaf (buildProfile: spec-driven-speckit)
    ├── emitter.md              ← emits .specify/memory/constitution.md (single file)
    ├── constitution-mapping.md ← canonical rules/ → numbered principles (reference, not duplicate)
    └── templates/
        └── constitution.md     ← the constitution template (provenance front-matter + principle blocks)
```

---

*Developer-side design detail · AI-DWG build-method subsystem · © Mohammad Maheri*
