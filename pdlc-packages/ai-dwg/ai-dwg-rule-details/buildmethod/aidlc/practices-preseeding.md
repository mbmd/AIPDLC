<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Practices Pre-Seeding — the five-section `memory/team.md` completeness contract

> **Load this file** during step 1 of the `aidlc/` emitter, immediately after `memory-mapping.md` routes the team-file rules. This is Proposal 3 of the compatibility design — the pre-seed that lets v2's **Practices Discovery (Stage 2.2)** *affirm* what is already present instead of interviewing the team from scratch. Authority for paths/headings/front-matter: `common/aidlc-v2-output-contract.md` §2.

## What this file adds over `memory-mapping.md`

`memory-mapping.md` routes each **rule** to its frozen heading and writes a heading only when the present inputs supply content (conditional emission). That is correct for `project.md`. For `team.md` there is one extra obligation, and it is what this file owns:

**`memory/team.md` is pre-seeded with all five sections that v2's Stage 2.2 expects — as a complete unit — so the stage recognises a populated file and fast-affirms it.** The five sections are the exact set Stage 2.2 would itself produce:

| # | Section | Assembled from (all raw data already exists — §5.5 map row G5) |
|---|---|---|
| 1 | `## Way of Working` | AI-ADLC git workflow + AI-DWG contributing / team-agreement + AI-POLC definition of done |
| 2 | `## Walking Skeleton` | AI-ADLC delivery strategy (vertical-slice vs horizontal-layer + reference module) |
| 3 | `## Testing Posture` | AI-ADLC quality attributes, or AI-TGE `## Testing Posture` when AI-TGE is active |
| 4 | `## Deployment` | AI-ADLC infrastructure decisions + AI-DWG CI/CD mapping |
| 5 | `## Code Style` | AI-ADLC technology stack + naming conventions |

This is **assembly, not authorship** — every field is reshaped from an existing PDLC artifact (§5.5 classifies G5 as `RESHAPE`, all raw data present). AI-DWG never invents a practice the chain did not produce.

## The section-replace-safety constraint — why the five sections must match Stage 2.2's own structure

We do not control, and cannot assume, *how* Stage 2.2 writes into a pre-existing `memory/team.md`. It could **append**, **overwrite the whole file**, or **replace section-by-section**. The pre-seed must produce a correct result under **all three** behaviours, and there is exactly one way to guarantee that:

> **Emit the five sections with the same headings, in the same order, in the same prose-under-level-two-heading shape that Stage 2.2 itself uses.**

Under that structural parity:
- **append** → v2 finds every expected section already present and has nothing to add (fast-affirm);
- **overwrite** → v2 replaces our file with a structurally identical one (no information lost that the chain owns — the content it writes is what we seeded from);
- **section-replace** → each of v2's sections maps one-to-one onto one of ours, so the merge is clean, section for section.

Any structural mismatch (a missing section, a renamed heading, a different nesting) breaks at least one of the three behaviours — a missing section defeats append-affirm, a renamed heading defeats section-replace. **So all five headings are always emitted for `team.md`**, even where a section's content is thin: a section we cannot fully populate is written with the fields we do have plus an explicit affirm-me marker (below), never omitted. This is the one place the emitter departs from `memory-mapping.md`'s conditional-heading rule, and it departs deliberately.

## The affirm-me marker — honest thin sections

Where the chain supplies only partial content for a section, emit what exists and append a single marker line so v2's Stage 2.2 knows to confirm rather than assume:

```markdown
## Deployment
- Deploy frequency: on-demand        <!-- from AI-ADLC infrastructure decisions -->
<!-- affirm: rollback target and environment promotion not specified upstream — confirm at Practices Discovery -->
```

The marker is a comment, so it is inert to any tool that does not read it, and it degrades loudly to a human reviewer. It never fabricates a value to fill a gap — a fabricated practice is worse than an affirm prompt, because v2 would affirm a falsehood.

## The no-duplication constraint still holds

The practices sections are **behavioural rules**, not knowledge — they carry the prescriptive extract (what the team does), and `rules/` remains the single source of truth (contract §2 / Proposal 2). Reference prose *about* those practices (rationale, background) goes to `knowledge/`, not here. Do not restate a framework default v2's org layer already supplies (additive-chain discipline, `memory-mapping.md`): if trunk-based development is an org default, do not re-seed it under `## Way of Working` — seed only the team's genuine specialization.

## Generation-time only

This pre-seed runs **at generation time**, never as a later user-triggered step (design OQ-3). v2 loads `memory/` at the start of every stage, so a `team.md` that arrives after generation misses Stage 2.2 entirely — the exact stage it exists to accelerate. A complete tree before v2's first run is the whole value.

## Ownership + front-matter

`memory/team.md` is `hybrid` (AI-DWG seeds, team and v2 amend). It carries the mandatory rule-file front-matter (`status:` + `pairing:`) per `memory-mapping.md` — practices rules are `feedforward-only` unless a sensor covers one.

---

*Developer-side design detail · AI-DWG `aidlc/` practices pre-seeding · © Mohammad Maheri*
