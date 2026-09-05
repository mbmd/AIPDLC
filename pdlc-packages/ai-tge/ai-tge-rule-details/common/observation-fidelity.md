<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Observation Fidelity

## Purpose

AI-TGE adapts to whatever inputs a workspace provides — that adaptability is the engine's Adaptive Engine Principle and it is deliberate (, OR-input). **This file governs the other half of that principle: when the engine substitutes for an input it could not resolve, the substitution MUST be visible in its output.**

Adaptation without disclosure is not resilience. A stage that cannot find its declared input, silently substitutes a heuristic, and then emits a well-formed report has converted *"I could not find the input"* into *"here is your answer"*. The report looks identical to a real one, so nobody investigates. That is a worse failure than an error, because an error is self-reporting and a plausible report is not.

**Governed by `INV-L2-021`** [loud-degradation]. This file is the canonical definition that invariant is checked against; every stage that can degrade points here rather than restating the rule, so there is one statement to keep correct instead of six that drift.

**Load at engine start**, alongside `common/process-overview.md` — fidelity is assessed in Stage 1 and re-assessed in Stage 7, so it must be resident before either runs.

---

## The three values

Observation Fidelity is a single recorded value describing whether the current run resolved the inputs its selected mode declares.

| Value | Meaning | Effect on output |
|-------|---------|------------------|
| **✅ Full** | Every input the selected mode declares resolved at its expected location. Nothing was substituted. | Figures stand unqualified. No banner. |
| **⚠️ Degraded** | At least one declared input did not resolve, and the stage proceeded on a substitute — a heuristic, a partial scan, or a skip. | Banner in the artifact and the report; every figure derived from a substitute carries the degraded marker. |
| **❌ Unknown** | Fidelity was not assessed. | **Treated as Degraded by every consumer.** |

---

## Two fail-closed rules

These are what make the disclosure trustworthy. Both are **MUST**.

### Rule F1 — Unknown is read as Degraded, never as Full

A consumer of Observation Fidelity — the coverage report, the state file, the in-session report, the quality dashboard, the `TGV__` and `CVR__` agents — MUST treat `❌ Unknown` exactly as it treats `⚠️ Degraded`. **Absence of an assessment is NEVER read as an absence of degradation.**

The initial value written at Stage 1 is `❌ Unknown`. It becomes `✅ Full` only by an assessment that positively resolved every declared input. A stage that fails to record fidelity therefore produces a report marked degraded.

> **Why this direction.** The failure mode of the disclosure mechanism itself must be a visible over-warning, never a silent under-warning. A spurious banner is a five-minute investigation; a missing banner is a wrong decision taken with confidence.

### Rule F2 — A skip is disclosed by cause, not by outcome

A conditional stage skips for one of two reasons, and they are **not** the same finding. The engine MUST distinguish them.

| Cause | Example | Disclosure |
|-------|---------|------------|
| **Trigger legitimately does not hold** — the input location resolved, and the project genuinely has nothing there | The user-story location exists and contains no story files. No defect has been reported. | **Silent.** Record `⏭️ Skipped` in the state file Progress table with the reason. Fidelity unaffected. |
| **Declared location did not resolve** — the place the stage was told to look does not exist in this workspace | The stage's story location is absent from the workspace layout entirely | **Disclosed.** Fidelity → `⚠️ Degraded`. Named in all three destinations. |

**NEVER report an unresolved location as an empty one.** *"No user stories detected"* is a reassurance when the location was checked and *"the location does not exist here"* is a finding — collapsing them is precisely the defect this file exists to prevent.

---

## Declared inputs — assessed per mode, not in absolute terms

Degradation is measured against **the inputs the selected mode declares**, never against the union of every input AI-TGE can read. A mode that does not declare an input is not degraded by its absence.

| Mode | Declared inputs |
|------|-----------------|
| **Full Chain** | Architecture Package · Development Workspace · build state · unit-progress vocabulary · user-story location · non-functional-requirement location |
| **Architecture Only** | Architecture Package |
| **Brownfield** | Existing test locations |
| **Observation Only** | Build state · unit-progress vocabulary · user-story location |

**If the mode itself is unresolved, fidelity is `❌ Unknown`** — and by Rule F1 that reads as Degraded. Mode is never inferred silently.

### The Observation-phase input register

Each row names the input by **semantic role**, its current expected location, the substitute that fires when it does not resolve, and — the column that matters most — what becomes unmeasured as a result.

> **The "Expected at" column is the *fallback / disclosure* location, not the primary lookup.** Each input is resolved first by its **manifest key** — see `common/manifest-resolution.md` for the role → manifest-key → fallback map (build state → `manifest.files.buildState`, user-story location → `manifest.paths.backlog`, NFR location → `manifest.paths.requirements`). The literal path below is what the engine falls back to when no manifest exists, and it is what the fidelity block reports to the user as "expected at". This register answers *how an unresolved input is disclosed*; `manifest-resolution.md` answers *where it is looked up*.

| # | Input (semantic role) | Consumed by | Expected at | Substitute if unresolved | Unmeasured consequence |
|:-:|---|:---:|---|---|---|
| 1 | **Build state** — which units and stages are complete | Stage 7 | `aidlc-docs/aidlc-state.md` | Scan for test files changed since the last observation; use file modification timestamps as a proxy for build progress | Unit completion is **inferred from file timestamps, not read**. A completed unit whose files were not touched is invisible; a touched file that completes nothing registers as progress. The observation delta is a filesystem event, not a build fact. |
| 2 | **Unit-progress vocabulary** — the per-unit stage names | Stage 7 | The stage names carried in the build state file | Treat every completion as generic; no per-unit stage position | **Per-unit stage position is unavailable.** The engine can say a unit changed but not which stage it reached, so stage-conditional register updates cannot fire. |
| 3 | **User-story location** — stories and their acceptance criteria | Stage 8 | `aidlc-docs/inception/user-stories/` | Stage 8 skips | **Story-derived acceptance coverage is zero, not complete.** No acceptance-test register entries exist, so the Acceptance row of every coverage view reports an absence of *data* while looking like an absence of *tests*. |
| 4 | **Non-functional-requirement location** — NFR criteria carried with stories | Stage 8 | `aidlc-docs/inception/requirements/` | Skip NFR extraction from stories; AP-derived NFR requirements are unaffected | **Story-carried NFR criteria are unmeasured.** NFR coverage reflects the Architecture Package only. |

> **Column legend**
>
> | Column | Description |
> |--------|-------------|
> | Input (semantic role) | What the engine needs, named by role rather than by path |
> | Consumed by | The Observation-phase stage that reads it |
> | Expected at | Where this release looks for it |
> | Substitute if unresolved | The documented fallback that fires — never a crash |
> | Unmeasured consequence | What the run genuinely cannot know, stated plainly enough to appear verbatim in the artifact |

**Row 2 is the one most easily missed.** It is a vocabulary, not a path — it fails when the build state file *is* present but its stage names are not the expected set. A path check passes and the observation is still wrong.

---

## Assessment procedure

| When | Stage | Action |
|------|-------|--------|
| **Initialisation** | Stage 1 — Workspace Detection | Write `Fidelity: ❌ Unknown` into the state file. Record each declared input's resolution as it is detected. This is the earliest point at which degradation is knowable, so it is stated here rather than discovered later. |
| **Re-assessment** | Stage 7 — State Observation | Re-resolve every declared input at the start of each observation cycle. A location that existed last cycle may not exist now. Update the fidelity block **before** any figure is derived from it. |
| **Propagation** | Stage 9 — Coverage Reporting | Read fidelity; compile it into the artifact; lead the summary with it when it is not `✅ Full`. Never recompute it — Stage 9 reports fidelity, it does not assess it. |

**MUST:** fidelity is recorded before the first figure that depends on it is calculated. A report is never assembled from an unassessed run.

---

## The three disclosure destinations

`INV-L2-021` requires disclosure in **all three** places at once. One is not enough — a user reading a report should not have to open a state file to learn the report is qualified.

| Destination | Where | Carries |
|-------------|-------|---------|
| **The produced artifact** | `.governance/test/coverage-report.md` | The banner above the Executive Summary, the `### Observation Fidelity` subsection inside the mandatory `## Completeness & Downstream Resolution` section (IMP-002), and the degraded marker on every affected figure |
| **The state file** | `.governance/test/tge-state.md` | The `## Observation Fidelity` block, including per-input resolution — the durable record |
| **The user-facing report** | The in-session stage report blocks (Stages 7, 8, 9) and the quality dashboard `## Current State` | The banner, first, before any figure |

### Canonical block 1 — the banner

Fires on a **fresh assessment** that returns `⚠️ Degraded` or `❌ Unknown`. It appears **before** any coverage figure, never after.

**The content below is canonical; the presentation adapts to the surface** — a markdown blockquote in written artifacts, plain indented lines in an in-session report. What must not vary is which facts appear: how many declared inputs failed, which ones, where each was sought, what substituted, and what is therefore unmeasured.

```markdown
> ⚠️ **DEGRADED OBSERVATION — these figures are incomplete.**
> {n} of {N} declared inputs for {mode} mode did not resolve:
> {for each unresolved input: **{role}** — expected at `{path}`; substituted with {substitute}}
>
> **Therefore unmeasured:** {for each: {unmeasured consequence}}
>
> Per-input detail: `.governance/test/tge-state.md` → Observation Fidelity.
```

When fidelity is `❌ Unknown`, the first line is followed by: `Fidelity was not assessed for this run, so it is reported as degraded.`

### Canonical block 2 — the state-file block

```markdown
## Observation Fidelity

| Field | Value |
|-------|-------|
| **Fidelity** | {✅ Full / ⚠️ Degraded / ❌ Unknown} |
| **Assessed At** | {ISO timestamp or "not assessed"} |
| **Assessed By** | Stage {1 / 7} |
| **Mode Assessed Against** | {Full Chain / Architecture Only / Brownfield / Observation Only} |
| **Declared Inputs Resolved** | {n} of {N} |

### Per-Input Resolution

| Input | Expected At | Resolved | Substitute Used | Unmeasured Consequence |
|-------|-------------|:-------:|-----------------|------------------------|
| {role} | {path or "not declared by this mode"} | {✅ / ❌ / n/a} | {— / description} | {— / consequence} |
```

### Canonical block 3 — the figure marker

Any figure derived wholly or partly from a substitute carries the marker inline. A qualified number is never presented bare.

```markdown
{n}% ⚠️ (degraded — see Observation Fidelity)
```

Applies to: overall coverage, the Acceptance row of any coverage-by-level view, the observation delta, and any trend computed across a cycle whose fidelity was not `✅ Full`.

---

## What this does NOT change — the silent-when-complete tenet stands

AI-TGE's key principle **"Silent when complete"** is unaffected, and the distinction is load-bearing:

| Situation | Behaviour |
|-----------|-----------|
| All required tests exist and pass — **nothing to report** | **Silent.** Unchanged. This is the tenet, and it is preserved exactly. |
| Inputs did not resolve — **nothing measured** | **Discloses.** Never silent. |

*Nothing to report* and *nothing measured* are different claims about the world. The first is a result; the second is the absence of one. A degradation banner on a fully-resolved clean run would be noise and would breach the tenet — which is why fidelity is assessed per declared input rather than by looking for problems.

---

## Validation

Every item is **BLOCKING** for any Observation-phase run.

- [ ] Fidelity holds one of exactly three values; no fourth state and no blank
- [ ] Initial value is `❌ Unknown`, written at Stage 1
- [ ] `✅ Full` is reachable only by positively resolving every input the selected mode declares
- [ ] `❌ Unknown` is handled identically to `⚠️ Degraded` by every consumer (Rule F1)
- [ ] Every documented fallback in the Observation phase names its substitute **and** its unmeasured consequence
- [ ] A skip is classified by cause before it is recorded (Rule F2); an unresolved location is never reported as an empty one
- [ ] When fidelity is not `✅ Full`, the banner appears in the artifact **and** the state file **and** the user-facing report — all three, not any one
- [ ] The banner precedes the first coverage figure in every surface that carries both
- [ ] Every figure derived from a substitute carries the inline marker
- [ ] A fully-resolved run emits **no** banner and **no** marker

---

## Interaction with other files

| Related | Relationship |
|---------|--------------|
| `common/session-continuity.md` | Authoritative state-file schema — hosts canonical block 2 |
| `templates/tge-state.md` | The emitted state-file template — mirrors block 2 |
| `strategy/workspace-detection.md` | Stage 1 — initialises fidelity to `❌ Unknown`; records per-input resolution |
| `observation/state-observation.md` | Stage 7 — re-assesses fidelity; inputs 1 and 2 above |
| `observation/story-acceptance-mapping.md` | Stage 8 — inputs 3 and 4; applies Rule F2 |
| `observation/coverage-reporting.md` | Stage 9 — compiles fidelity into the artifact and leads the summary with it |
| `templates/coverage-report.md` | The produced artifact — hosts the banner and the fidelity section |
| `templates/quality-dashboard-template.md` | `## Current State` — carries fidelity so the dashboard cannot report a fabricated figure |
| `common/artifact-sections.md` | IMP-002 "Completeness & Downstream Resolution" — the mandated home for what is partial; the fidelity section satisfies it for the coverage report |
| `templates/agents/coverage-review-agent.md` · `test-governance-agent.md` | `CVR__` / `TGV__` verify the disclosure landed — the on-demand check behind this rule (a principle with no check is a hope) |

---

*Observation Fidelity · common rule · 2026-09-01*
