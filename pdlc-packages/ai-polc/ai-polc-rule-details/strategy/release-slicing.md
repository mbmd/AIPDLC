<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 7: Release & Increment Slicing

**Phase:** Strategy
**Purpose:** Group prioritized epics into deliverable releases aligned to product goals, define MVP/MMP scope, and establish increment readiness criteria — answering "which stories ship together and when?"

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Resource Planner** sub-role:

### Behavioral Shifts
- Think in terms of delivery capacity: what can actually ship together given dependencies and team bandwidth
- Balance value (what we WANT to ship) against feasibility (what we CAN ship)
- Consider release overhead: each release has a cost (testing, coordination, communication)
- Frame releases as value increments, not arbitrary time-boxes

### Anti-Patterns
- Do NOT slice releases by arbitrary dates alone — slice by value delivered
- Do NOT pack releases so tightly that one slip cascades everything
- Do NOT create releases with no clear value proposition ("release 3 has miscellaneous leftovers")
- Do NOT ignore dependencies when grouping — if Epic A depends on Epic B, they're in the same or sequential releases

### Quality Check
Every release must pass: "Can I articulate in one sentence what value this release delivers to users?" If no → the release boundary is wrong.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | 2-3 releases. MVP scope defined. Simple grouping by priority order. |
| **Standard** | 3-5 releases with value statements. MVP + MMP defined. Dependency-aware grouping. Readiness criteria per release. |
| **Comprehensive** | Full release train with increment readiness gates, rollback criteria, feature-flag strategy, multi-team coordination. |

---

## Steps

### Step 7.1: Define MVP Scope (For New Products)

> **Story-map input (if the User Story Mapping extension ran at Stage 4):** a `story-map.md` exists with release slices. Use its **walking-skeleton slice** as the MVP candidate directly — it is already the thinnest end-to-end path across the whole journey (USM-04 / USM-06). Reconcile it against the MVP criteria below rather than re-deriving the MVP from a flat ranked list.

If Product Maturity = New (0→1), MVP definition is critical:

**MVP Criteria:**
- What is the MINIMUM set of epics that delivers enough value to:
  - [ ] Validate the core value proposition
  - [ ] Allow real users to use the product (not just demo)
  - [ ] Generate feedback for the next iteration
  - [ ] NOT embarrass the brand (minimum quality bar)

Walk through the prioritized backlog top-down:
```
Rank 1: EPIC-003 — Provider Abstraction    → MVP? YES (core functionality)
Rank 2: EPIC-001 — Async Processing        → MVP? YES (performance goal)
Rank 3: EPIC-005 — Onboarding Redesign     → MVP? YES (users need to get in)
Rank 4: EPIC-002 — PayPal Integration      → MVP? NO (Stripe alone is viable for v1)
Rank 5: EPIC-007 — Referral Program        → MVP? NO (growth, not viability)
```

**MVP = Ranks 1-3.** Everything below is post-MVP.

For mature products, define **MMP** (Minimum Marketable Product) for the next version instead.

### Step 7.2: Group Epics Into Releases

> **Story-map input:** if a `story-map.md` exists, its horizontal release slices already group stories across the journey — carry those slices in as the starting release grouping (USM-08), then adjust for dependencies and capacity below.

Based on priority order, dependencies, and capacity:

| Release | Goal | Epics | Value Statement |
|---------|------|-------|-----------------|
| **R1 (MVP)** | Validate core value | EPIC-003, EPIC-001, EPIC-005 | "Users can make payments via Stripe with <2s processing and a clean onboarding flow" |
| **R2** | Expand payment options | EPIC-002, EPIC-004, EPIC-006 | "Users can pay via Stripe, PayPal, or bank transfer" |
| **R3** | Growth & optimization | EPIC-007, EPIC-008 | "Referral program drives user acquisition; analytics inform next priorities" |

**Grouping rules:**
- Respect dependency order (if B depends on A, A ships in same or earlier release)
- Each release has a coherent value statement (not "random collection")
- Release size is achievable (not 20 epics in one release for a small team)
- Critical path identified per release

### Step 7.3: Define Increment Readiness Criteria

For each release, specify what "ready to ship" means:

```
Release R1 (MVP) — Readiness Criteria:
- [ ] All 3 epics at DoD (Definition of Done met)
- [ ] Integration testing complete (all epics work together)
- [ ] Performance goal verified (<2s payment processing under load)
- [ ] No P1/P2 open bugs in release scope
- [ ] Stakeholder demo completed and accepted
- [ ] Release notes drafted
- [ ] Rollback plan documented
```

### Step 7.4: Context-Factor Adaptation

| Context Factor | Release Slicing Impact |
|---|---|
| Release Strategy = Continuous | Per-epic releases; each epic ships independently when done |
| Release Strategy = Scheduled | Batch releases aligned to calendar (sprints, PIs, quarters) |
| Release Strategy = Feature flags | Releases are deployments; features activate separately |
| Architecture = Microservices | Per-service release possible; reduces coordination cost |
| Architecture = Monolith | Whole-product release; increases coordination cost |
| Scale = Multi-team | Align releases to PI boundaries (SAFe) or coordinate cross-team |
| Compliance = Heavy | Add compliance sign-off to readiness criteria |

### Step 7.5: Define Ship/Iterate/Pivot Decision Framework

After each release ships, the PO makes a decision:

| Signal | Decision | Action |
|--------|----------|--------|
| Metrics meet/exceed goals | **Ship + Continue** | Proceed to next release as planned |
| Metrics partially met, learning captured | **Iterate** | Adjust next release based on feedback |
| Metrics significantly missed, assumptions invalidated | **Pivot** | Re-evaluate vision; major re-prioritization |
| External change (market/competitor/regulation) | **Re-assess** | Full re-prioritization against new reality |

### Step 7.6: Persist Release Plan

Write `release-plan.md` with:
- MVP/MMP scope definition (with explicit IN/OUT)
- Release table (release → goal → epics → value statement)
- Readiness criteria per release
- Ship/Iterate/Pivot framework
- Release cadence (derived from delivery methodology context factor)
- Dependencies between releases
- Dual-track timeline + cadence when an AI delivery method is set (manual baseline vs chosen method + compression), per `strategy/delivery-method-timing.md`; manual-only shows a single track

---

### Visualization Pack (depth-gated)

| Depth | Diagram | Mermaid type | Source |
|-------|---------|:------------:|--------|
| Standard | Release roadmap (features by release cadence) | `gantt` | Release plan |
| Comprehensive | Feature-to-value traceability (features → outcomes) | `flowchart` | Traceability matrix |

Emit from the release plan. No new content introduced.

---

## Gate

**Gate 7 — Release Plan Confirmed:**

Present to user:
```
Release plan established:
• Releases defined: {N}
• MVP scope: {epic list} — "{value statement}"
• Release cadence: {continuous | per-sprint | quarterly | PI-aligned}
• Readiness criteria: defined per release

Does this delivery plan make sense for your product?
Approve to proceed to Phase 3 (Governance), or adjust.
```

User must confirm. This is also the **Phase 2 gate** — Strategy complete.

---

### Post-Gate: Derive Release Planning Artifacts

**Condition:** depth >= Standard AND user has approved Gate 7.

After gate approval, load `strategy/team-domain-planning.md` and derive the following artifacts:

**0. Velocity Model refresh (delivery-method timing).** Load `strategy/delivery-method-timing.md`. If a delivery method was captured (Stage 1), (re)compute `polc-state.md` → `## Velocity Model`: per-work-class effective multipliers, blended project multiplier, and per-team **baseline + effective** velocity. When an AI method is set, the artifacts below render **dual-track** (manual baseline vs chosen method + compression); manual → single track. This supplies the velocity the capacity matrix reads.

1. **`release-relevance-grouping.md`** — functional cluster & dependency rationale
   - For each release in `release-plan.md`, collect assigned epics
   - Extract inter-epic dependencies (from Integration sections or `Depends On` fields)
   - Compute build order (topological sort within each release)
   - Identify cross-release dependencies
   - Derive functional theme from BC clusters + strategic themes in `roadmap.md`
   - At Standard+ depth: add descoping options per release
   - Generate Mermaid Gantt (release timeline) + dependency graph

2. **`capacity-planning-matrix.md`** — team capacity vs. epic demand
   - Read `polc-state.md` → `## Velocity Model` section for per-team velocities
   - Calculate demand (committed SP) vs. capacity (velocity × sprints) per team per release
   - Compute utilization %, identify bottlenecks (>80%), underutilized teams (<30%)
   - At Comprehensive depth: generate 3-5 what-if scenarios + sprint allocation guidance
   - Generate Mermaid demand pie + team-activity Gantt

**Write:** Both files to `{outputRoot}/` immediately. Update `polc-state.md` → Planning Artifacts section (set to `generated`, record timestamp).

**Skip conditions:**
- depth = Minimal → skip entirely
- Fewer than 2 releases → skip `release-relevance-grouping.md` (nothing to group)
- Velocity Model section absent in `polc-state.md` → skip `capacity-planning-matrix.md` (cannot calculate capacity without velocity data)

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-006: Release plan established. {N} releases defined.
MVP: {epic list}. MVP value: "{one-line}".
Release cadence: {cadence}. Ship/iterate/pivot framework defined.
```

---

## Transition

→ **Phase 3, Stage 8: Definition of Ready / Done** (Governance begins)

---

*Detail file for AI-POLC Stage 7 | Phase: Strategy*
