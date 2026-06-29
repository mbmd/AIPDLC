<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Product Backlog Package (AI-POLC) → user-stories.md + acceptance examples (POLC CLUSTER)

## Purpose

Transforms the **Tier 2 INVEST stories** produced by AI-POLC (`tier2/story-elaboration.md`) — with Given/When/Then acceptance criteria — into a `user-stories.md` reference plus seeded acceptance-criteria examples in the workspace. This gives AI-DLC v1 ready-to-build, testable stories (not just epics) and gives AI-TGE the Given/When/Then format it derives acceptance tests from. It is generated ONLY when POLC ran Tier 2 (story elaboration is off by default in chain mode).

**Output:**
- `{workspace-root}/user-stories.md` (INVEST stories grouped by epic)
- `{workspace-root}/examples/acceptance/{story-id}.feature.md` (Given/When/Then per story — acceptance skeletons)

**Condition:** Generate IF `polc-state.md` is present AND `tier2/story-elaboration.md` exists (Tier 2 was activated). If POLC present but Tier 2 not run, SKIP and note: "Stories deferred to AI-DLC v1 (POLC Tier 2 not activated)."

**Cluster:** Product — belongs exclusively to the POLC input cluster.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS activity, ALSO adopt the mindset of a **Business Analyst**. ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- A story is a promise of a conversation with a testable outcome — preserve both the narrative and the criteria
- Given/When/Then is a contract — copy it verbatim; AI-TGE turns each line into a test assertion
- INVEST quality is POLC's responsibility — carry it, do not "fix" stories here
- Acceptance criteria are the boundary between "built" and "accepted" — never soften

### Anti-Patterns for This Activity
- Do NOT paraphrase Given/When/Then clauses — exact wording becomes test steps
- Do NOT merge stories or split them — carry the POLC decomposition 1:1
- Do NOT invent acceptance criteria where POLC left a story thin — flag instead

---

## Source Inputs

**Primary source:** AI-POLC → PBP, via `polc-state.md` marker.

| PBP Document | What to Extract | Maps to |
|---|---|---|
| `tier2/story-elaboration.md` | INVEST stories: "As a… I want… so that…" + Given/When/Then | `user-stories.md` rows + `.feature.md` skeletons |
| `strategy/epic-decomposition.md` | Parent epic per story | Story grouping by epic |
| `governance/definition-of-ready-done.md` | DoR/DoD bar | Story readiness checklist reference |

### `polc-state.md` Fields Used

| Field | Used For |
|-------|----------|
| `Tier 2 Activated` | Hard gate — only generate if true |
| `Acceptance Format` | Confirms Given/When/Then (vs other) so skeletons match |
| `Project ID` | Front-matter correlation key |

---

## Target Structure

### user-stories.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-POLC — tier2/story-elaboration.md"
generatedOn: "{generation-date}"
ownership: hybrid
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-POLC Tier 2 Stories | date: {generation-date} -->

# User Stories

> INVEST stories elaborated by AI-POLC. Acceptance criteria are Given/When/Then
> and seed `examples/acceptance/*.feature.md` for AI-TGE test derivation.

## Epic: {epic-id} — {epic-title}
<!-- begin: PBP-sourced -->
### {STORY-id}: {short title}
**As a** {persona/role} **I want** {capability} **so that** {benefit}.

**Acceptance Criteria**
- **Given** {context} **When** {action} **Then** {outcome}
- **Given** … **When** … **Then** …

**DoR met:** {yes/no}  ·  **Story points / size:** {if present}  ·  **Acceptance skeleton:** `examples/acceptance/{STORY-id}.feature.md`
<!-- end: PBP-sourced -->
```

### examples/acceptance/{STORY-id}.feature.md

```markdown
<!-- AI-DWG generated from AI-POLC story {STORY-id} | acceptance skeleton for AI-TGE -->
# {STORY-id}: {title}

Scenario: {scenario name}
  Given {context}
  When {action}
  Then {outcome}

# Additional scenarios elaborated by AI-DLC v1 / AI-TGE during build.
```

---

## Transformation Rules

### Rule 1: Given/When/Then Is VERBATIM
Each clause is copied exactly — it becomes a test step downstream.

### Rule 2: 1:1 Story Carry
Every Tier 2 story produces one `user-stories.md` entry and one `.feature.md` skeleton. No merge, no split.

### Rule 3: Group By Parent Epic
Stories are organized under their epic (IDs consistent with `polc-to-epics-backlog.md`).

### Rule 4: Thin Stories Are Flagged, Not Filled
A story missing acceptance criteria gets `<!-- POLC story lacks acceptance criteria — AI-DLC v1/PO to complete -->`, not invented criteria.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `polc-to-epics-backlog.md` | Stories nest under the epic stubs; epic IDs must match. |
| `quality-to-dod.md` | DoR/DoD bar referenced per story. |
| `polc-to-traceability.md` | Story IDs populate the matrix `Story` column. |
| (AI-TGE downstream) | `.feature.md` skeletons are AI-TGE's acceptance-test seed — keep format clean. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| POLC present, Tier 2 NOT activated | SKIP entirely; note deferral to AI-DLC v1 |
| Acceptance format is not Given/When/Then | Carry POLC's format verbatim; adjust skeleton header accordingly |
| Story has narrative but no criteria | Include story; flag missing criteria |
| Story references unknown epic | Group under `Unassigned`; flag (also a traceability finding) |

---

## Output Validation

- [ ] Generated ONLY when Tier 2 was activated
- [ ] Given/When/Then copied verbatim
- [ ] One `.feature.md` skeleton per story
- [ ] Stories grouped under correct epic IDs
- [ ] Thin stories flagged, not fabricated
- [ ] Provenance front-matter + projectId present
