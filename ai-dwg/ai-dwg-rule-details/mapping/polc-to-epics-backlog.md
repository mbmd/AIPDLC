<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Product Backlog Package (AI-POLC) → epics-and-backlog.md + backlog/ seed (POLC CLUSTER)

## Purpose

Transforms the epic decomposition produced by AI-POLC (`strategy/epic-decomposition.md`) into a **backlog scaffold** in the destination workspace: an epic overview document plus a `backlog/` folder structure that AI-DLC v1 fills with stories during build. This gives the build workspace a ready-made, prioritized backbone of work — goals decomposed into epics with acceptance criteria and a stable order — instead of starting from an empty backlog.

**Output:**
- `{workspace-root}/epics-and-backlog.md` (the epic overview + prioritized order)
- `{workspace-root}/backlog/` (one stub file per epic: `EPIC-{id}-{slug}.md`)

**Condition:** Generate IF `polc-state.md` is present AND the PBP contains epic decomposition.

**Cluster:** Product — belongs exclusively to the POLC input cluster.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS activity, ALSO adopt the mindset of a **Business Analyst** (with a resource-planning lens for ordering). ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- Epics are containers of value, not feature buckets — preserve the goal each epic serves
- Acceptance criteria at the epic level define "done for the epic" — copy them; do not soften
- Prioritization order is a decision, not a suggestion — preserve WSJF/MoSCoW rank verbatim
- The scaffold seeds work; it does NOT pre-write stories AI-DLC v1 should elaborate

### Anti-Patterns for This Activity
- Do NOT re-prioritize epics — copy POLC's order exactly
- Do NOT invent epics not in the PBP
- Do NOT pre-decompose epics into stories unless POLC's Tier 2 already did (then carry them; otherwise leave a `## Stories (elaborated by AI-DLC v1)` placeholder)

---

## Source Inputs

**Primary source:** AI-POLC → PBP, via `polc-state.md` marker.

| PBP Document | What to Extract | Maps to |
|---|---|---|
| `strategy/epic-decomposition.md` | Epic IDs, titles, parent goal, acceptance criteria | Epic stubs + overview rows |
| `strategy/value-prioritization.md` | WSJF/MoSCoW rank + rationale | Prioritized Order section |
| `strategy/release-slicing.md` | MVP/MMP groupings | Release column |
| `tier2/story-elaboration.md` (if present) | Elaborated stories per epic | Epic stub `## Stories` section |

---

## Target Structure

### epics-and-backlog.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — strategy/epic-decomposition.md + value-prioritization.md"
generatedOn: "{generation-date}"
ownership: hybrid
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-POLC Epic Decomposition | date: {generation-date} -->

# Epics & Backlog

> Prioritized epic backbone seeded from the Product Backlog Package.
> AI-DLC v1 elaborates stories into `backlog/EPIC-*.md`; order is POLC-authoritative.

## Prioritized Order
<!-- begin: PBP-sourced -->
| Rank | Epic ID | Epic | Parent Goal | Priority Model | Release | Stub |
|------|---------|------|-------------|----------------|---------|------|
| 1 | {epic-id} | {title} | {goal-id} | {WSJF=.. / Must} | {MVP} | `backlog/EPIC-{id}-{slug}.md` |
| ... | ... | ... | ... | ... | ... | ... |
<!-- end: PBP-sourced -->

## Prioritization Rationale
<!-- begin: PBP-sourced -->
{verbatim rationale from value-prioritization.md — why this order}
<!-- end: PBP-sourced -->
```

### backlog/EPIC-{id}-{slug}.md (one per epic)

```markdown
---
generatedBy: AI-DWG
source: "AI-POLC — epic-decomposition.md"
ownership: hybrid
epicId: "{epic-id}"
parentGoal: "{goal-id}"
---

# EPIC-{id}: {title}

**Parent Goal:** {goal-id} — {goal}
**Priority:** {rank} ({model})  ·  **Release:** {release}

## Epic Acceptance Criteria
<!-- begin: PBP-sourced -->
- {criterion 1}
- {criterion 2}
<!-- end: PBP-sourced -->

## Stories
<!-- If POLC Tier 2 elaborated stories, list them here; else leave for AI-DLC v1 -->
{elaborated stories OR "_Stories elaborated by AI-DLC v1 during build._"}
```

---

## Transformation Rules

### Rule 1: Order Is VERBATIM
Copy POLC's prioritization rank exactly. Never re-rank.

### Rule 2: One Stub Per Epic
Every epic in the PBP gets exactly one `backlog/EPIC-*.md`. No epic dropped, none invented.

### Rule 3: Acceptance Criteria Copied, Not Paraphrased
Epic-level acceptance criteria are quoted verbatim.

### Rule 4: Stories Deferred Unless Already Elaborated
In chain mode POLC defers stories to AI-DLC v1 — leave the placeholder. Only carry stories if POLC Tier 2 produced them.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `polc-to-traceability.md` | Epic IDs here MUST match the traceability matrix `Epic` column. |
| `polc-to-user-stories.md` | Story stubs/specs land under each epic stub when Tier 2 stories exist. |
| `quality-to-dod.md` | Epic acceptance criteria reference the same DoD bar. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| POLC present, no epic decomposition | Skip backlog seed; flag: "PBP has no epics — backlog left empty for AI-DLC v1" |
| Epics have no rank | Use document order; mark `Priority Model = unranked (PO to confirm)` |
| Tier 2 stories present | Populate each epic stub `## Stories`; cross-link to `polc-to-user-stories.md` output |
| Epic references missing goal | Keep epic; flag goal gap (also surfaces in traceability matrix) |

---

## Output Validation

- [ ] One `backlog/EPIC-*.md` per PBP epic (exhaustive)
- [ ] Prioritized order matches POLC rank verbatim
- [ ] Epic acceptance criteria copied verbatim
- [ ] Epic IDs consistent with traceability matrix
- [ ] Stories placeholder left when not elaborated
- [ ] Provenance front-matter + projectId present
