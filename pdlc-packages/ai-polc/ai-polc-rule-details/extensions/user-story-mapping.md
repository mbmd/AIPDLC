<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: User Story Mapping (Full Rules)

**Extension ID:** user-story-mapping
**Version:** 1.1.0
**Rule Prefix:** USM
**Status:** Active
**Stage:** 4 (Product Discovery & Roadmap) — the map is built here; its release slices feed Stage 7 (Release & Increment Slicing)
**Adds:** a journey backbone, task/story decomposition, release slicing (walking skeleton first), and a `story-map.md` artifact

---

## Activation Point

- **Primary stage:** Stage 4 (Product Discovery & Roadmap) — the map is built once the strategic themes and epics are in view.
- **Feeds forward:** Stage 7 (Release & Increment Slicing) — the map's horizontal slices seed MVP definition (Step 7.1) and release grouping (Step 7.2).
- **Blocking when active:** once the user opts in, the story map is a required Stage 4 artifact. The USM rules below are verified at the Stage 4 gate; a story map that leaves items unranked, unsliced, or untraceable is a blocking finding, not a suggestion.

Story mapping is a **discovery-and-planning technique**, not a new deliverable schema. It arranges what AI-POLC already produces — goals, epics, stories — into a plannable, journey-shaped view. If neither Tier 2 (story elaboration) nor the release plan is active, the map still stands alone as a scope-and-MVP aid whose slices reconcile with the Now/Next/Later roadmap.

---

## MANDATORY: Extension Sub-Role — Business Analyst (Story-Map Facilitator)

When this extension is active, ALSO adopt the mindset of a **Business Analyst facilitating a story-mapping session**. This does NOT replace your primary role (Product Manager / Product Ownership Lead) — it ADDS a thinking dimension for the duration of User Story Mapping rule enforcement. (This is the same **Business Analyst** sub-role used in Stage 4 discovery.) When you reach the release-slicing step (USM-04 / USM-06), shift toward the **Resource Planner** lens that leads Stage 7 — slicing is a capacity-and-sequencing judgment, not a discovery one.

### Behavioral Shifts
- Think in the user's narrative first — "what does a person do, and then what do they do next?" — before ranking or estimating anything.
- Map the whole journey before going deep on any one step; breadth-first exposes gaps that a ranked list hides.
- Treat the backbone as stable and the body as negotiable — priority and scope are cut vertically (within an activity), releases are cut horizontally (across the map).
- Make the walking skeleton thin and end-to-end — a release that covers the whole backbone shallowly beats one that finishes a single activity perfectly.

### Anti-Patterns for This Stage
- Do NOT let the map become a flat backlog with extra decoration — if there is no narrative left-to-right flow, it is not a story map.
- Do NOT slice releases feature-by-feature down a single activity ("depth-first") — that produces a demo, not a usable product increment.
- Do NOT allow orphan stories — every card on the map traces up to a goal/epic and forward to a release slice.
- Do NOT freeze the map as a wall decoration — its only value is what it feeds into the release plan and story elaboration.

### Quality Check
A good story map at this stage sounds like:
- "Backbone of 6 activities in journey order; 3 release slices with a walking-skeleton MVP that touches every activity; every story traces to an epic and a goal; slices reconcile with the Now/Next/Later roadmap and hand off to the Stage 7 release plan."

---

## The Technique

A story map has four parts:

```
        (narrative flow →)
BACKBONE:   [Activity A] ──── [Activity B] ──── [Activity C] ──── [Activity D]
              │                 │                 │                 │
TASKS:      task A1           task B1           task C1           task D1
            task A2           task B2                             task D2
              │                 │                 │                 │
  ── R1 (MVP / walking skeleton) ── thinnest end-to-end slice across all activities ──
STORIES     story A1.1         story B1.1        story C1.1        story D1.1
(ranked  ── R2 ──────────────────────────────────────────────────────────────────────
 top-      story A2.1         story B2.1                          story D2.1
 down)   ── R3 ──────────────────────────────────────────────────────────────────────
            story A2.2                                            story D2.2
```

- **Backbone** — user *activities* left-to-right in the order a user experiences them (the narrative flow).
- **Tasks** — the steps under each activity (what the user does to accomplish the activity).
- **Stories** — ranked top-to-bottom under each task (highest priority nearest the backbone).
- **Release slices** — horizontal cuts across the whole map; the first (top) slice is the *walking skeleton* — the thinnest path that touches every activity end-to-end.

---

## Additional Steps (append to Stage 4)

### Step 4.M1: Build the Activity Backbone

Lay out the user's journey as a left-to-right sequence of **activities** (large goals the user accomplishes), in narrative order.

```
Backbone (journey order):
[Discover] → [Sign up] → [Configure] → [Transact] → [Review] → [Get support]
```

- Derive activities from personas/journeys (AI-UXD input if present), the epics (Stage 5), and the strategic themes (Stage 2).
- 4–8 activities is typical; more than ~10 usually means activities are really tasks.

### Step 4.M2: Decompose Activities Into Tasks

Under each activity, list the **tasks** — the concrete steps a user takes to complete that activity.

```
[Sign up]
  ├── Create account
  ├── Verify email
  └── Complete profile
```

### Step 4.M3: Populate and Rank Stories

Under each task, place the candidate **stories**, ranked top-to-bottom by priority (most essential nearest the backbone). Reuse existing epics/stories — do not invent a parallel backlog.

### Step 4.M4: Draw Release Slices (Walking Skeleton First)

Cut horizontal lines across the map to define releases. The **top slice is the walking skeleton**: the thinnest set of stories that lets a real user go end-to-end across *every* activity.

```
── R1 (MVP): one story per activity → user can complete the whole journey, minimally
── R2: depth added to the highest-value activities
── R3: remaining enhancements
```

### Step 4.M5: Reconcile With Roadmap and Trace to Goals

- Map each release slice onto the Now/Next/Later roadmap (R1 = Now, etc.).
- Confirm every story on the map traces up to an epic and a goal; flag any card that does not.

### Step 4.M6: Hand Off

- Record the map as `story-map.md` and register it in `polc-state.md` (Active Extensions + artifact list).
- Carry the slices to Stage 7 (release plan) and, if Tier 2 is active, hand the per-slice stories to story elaboration.

---

## Rules

### Rule USM-01: Backbone Is User Activities in Narrative Order

**Statement:** The map's backbone is a left-to-right sequence of user activities in the order the user experiences them — not a feature list, a component list, or a team's backlog order.

**Verification:**
- [ ] The backbone reads as a coherent user journey left-to-right
- [ ] Backbone items are activities (user goals), not features or system modules
- [ ] Ordering reflects narrative/temporal flow, not priority

**Anti-Pattern:** A "backbone" that is really a prioritized feature list with no narrative flow.

---

### Rule USM-02: Tasks Decomposed Under Activities

**Statement:** Each activity is decomposed into the tasks a user performs to accomplish it. Tasks sit directly under their activity.

**Verification:**
- [ ] Every activity has at least one task beneath it
- [ ] Tasks describe user behaviour ("verify email"), not system internals ("call auth API")

**Anti-Pattern:** Jumping straight from activities to stories with no task layer, losing the "how the user does this" structure.

---

### Rule USM-03: Stories Ranked Top-Down Within a Task

**Statement:** Stories are placed under their task and ranked vertically — the most essential story sits nearest the backbone, lower-priority variations below.

**Verification:**
- [ ] Stories are ordered by priority within each task column (essential → optional)
- [ ] Vertical position is meaningful (higher = more essential), not arbitrary

**Anti-Pattern:** An unordered pile of stories under a task, so a slice cannot be cut meaningfully.

---

### Rule USM-04: Release Slices Are Horizontal Cuts, Walking Skeleton First

**Statement:** Releases are defined as horizontal slices across the map. The first slice is the walking skeleton — the thinnest set of stories that spans every backbone activity end-to-end.

**Verification:**
- [ ] Release slices are horizontal (cross multiple activities), not vertical (one activity finished at a time)
- [ ] The first slice touches every activity on the backbone
- [ ] Each slice has a coherent release goal

**Anti-Pattern:** Depth-first slicing — completing one activity fully before starting the next — which yields a partial product no user can actually use.

---

### Rule USM-05: Every Story Traces Up to a Goal/Epic

**Statement:** Each story on the map traces upward to an epic (Stage 5) and a product goal (Stage 2). No orphan cards.

**Verification:**
- [ ] Every story links to an epic ID
- [ ] Every activity/theme links to a goal
- [ ] Orphans (stories with no parent goal/epic) are flagged and resolved

**Anti-Pattern:** Stories invented on the map that exist nowhere in the backlog and serve no stated goal.

---

### Rule USM-06: MVP = Thinnest End-to-End Slice

**Statement:** The MVP is the walking-skeleton slice — minimal but complete across the journey — not "the top N ranked backlog items."

**Verification:**
- [ ] The MVP slice lets a real user complete the whole journey (not just a demo)
- [ ] The MVP is justified as the *thinnest viable* path, with de-scoped items explicitly below the line
- [ ] MVP boundary reconciles with Stage 7 Step 7.1 MVP criteria

**Anti-Pattern:** Declaring the top of the ranked backlog "the MVP" when it over-invests in one activity and never reaches the end of the journey.

---

### Rule USM-07: Map Reconciles With the Now/Next/Later Roadmap

**Statement:** The release slices reconcile with the roadmap horizons produced in Stage 4 — slices and horizons tell the same story.

**Verification:**
- [ ] Each slice maps to a roadmap horizon (Now/Next/Later)
- [ ] No slice contradicts the roadmap sequencing without a logged rationale (Decision Log)

**Anti-Pattern:** A story map that implies a release order at odds with the roadmap, leaving two conflicting plans of record.

---

### Rule USM-08: Hand-Off Completeness

**Statement:** Every element of the map routes to a downstream home — release slices to the Stage 7 release plan, per-slice stories to Tier 2 elaboration (when active), and the goal→activity→story chain to the traceability matrix.

**Verification:**
- [ ] Release slices are carried into the Stage 7 release plan
- [ ] Per-slice stories are queued for Tier 2 (if Tier 2 is active)
- [ ] The traceability chain (goal → activity → story) is recorded
- [ ] `story-map.md` is registered in `polc-state.md`

**Anti-Pattern:** A finished map that never feeds the release plan or elaboration — a "dead artifact" whose planning value is lost.

---

## Artifact: `story-map.md`

When this extension is active, produce `story-map.md` alongside the roadmap:

```markdown
# Story Map — {Product}

## Backbone (journey order)
| # | Activity | Serves Goal(s) | Epic(s) |
|---|----------|----------------|---------|
| 1 | {Activity A} | {G1} | {EPIC-00X} |
| 2 | {Activity B} | {G2} | {EPIC-00Y} |

## Map Body (tasks → ranked stories)
### {Activity A}
- Task A1: {task}
  - {STORY-…} {story} — _rank 1_
  - {STORY-…} {story} — _rank 2_

## Release Slices
| Slice | Horizon | Goal | Stories (by activity) | Walking skeleton? |
|-------|---------|------|-----------------------|:-----------------:|
| R1 (MVP) | Now | {release goal} | A1.1, B1.1, C1.1, D1.1 | ✅ |
| R2 | Next | {release goal} | A2.1, B2.1 | — |

## Traceability
Goal → Activity → Story chain recorded for the traceability matrix.
```

---

## Depth Adaptation

| Depth | Story Mapping Behavior |
|-------|------------------------|
| **Minimal** | Backbone + a single MVP (walking-skeleton) slice. No deep task layer; stories referenced by epic. |
| **Standard** | Full map (backbone → tasks → ranked stories) + 2–3 release slices reconciled with the roadmap. |
| **Comprehensive** | Multi-release map + alternative slicing options + dependency notes across activities + explicit de-scope rationale per slice. |

---

## Feeds / Hand-Off

| Target | What flows | Rule |
|--------|-----------|------|
| Stage 7 — Release & Increment Slicing | Release slices → MVP (Step 7.1) + release grouping (Step 7.2) | USM-04, USM-06, USM-08 |
| Tier 2 — Story Elaboration | Per-slice stories → INVEST + Given/When/Then (when Tier 2 active) | USM-08 |
| Traceability matrix | Goal → activity → story chain | USM-05, USM-08 |
| Roadmap (Now/Next/Later) | Slice ↔ horizon reconciliation | USM-07 |

---

## Verification Checklist (Stage Completion)

Before completing Stage 4 with User Story Mapping active, verify:

- [ ] Backbone is a narrative-ordered set of user activities (USM-01)
- [ ] Activities decomposed into tasks (USM-02)
- [ ] Stories ranked top-down under each task (USM-03)
- [ ] Release slices are horizontal, walking skeleton first (USM-04)
- [ ] Every story traces to an epic and a goal — no orphans (USM-05)
- [ ] MVP is the thinnest end-to-end slice (USM-06)
- [ ] Slices reconcile with the Now/Next/Later roadmap (USM-07)
- [ ] Map hands off to release plan + Tier 2 + traceability; `story-map.md` registered in `polc-state.md` (USM-08)

---

## Composition

- **+ Advanced Discovery:** OKRs/JTBD frame the *why* (goals, jobs); the story map arranges the *what and when* (activities → slices). Backbone activities trace up to jobs; slices trace up to OKRs.
- **+ Tier 2 (Story Elaboration):** stories placed on the map are elaborated into INVEST + Given/When/Then per slice — the map decides *what to elaborate next*.
- **Stands alone:** with neither active, the map still produces an MVP and release slices that reconcile with the roadmap and feed Stage 7.
- **Rule-ID namespace:** `USM-01 … USM-08` — does not overlap any existing POLC rule identifiers.
