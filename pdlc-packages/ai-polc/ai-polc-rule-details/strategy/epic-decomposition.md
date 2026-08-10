<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 5: Epic Decomposition

**Phase:** Strategy
**Purpose:** Break product goals into epics — the structural hierarchy that makes every story traceable to business value. Each epic is a governed unit with clear acceptance criteria and goal linkage.

---

## MANDATORY: Stage Sub-Role

During this stage, also adopt the **Business Analyst** sub-role:

### Behavioral Shifts
- Think in terms of requirement decomposition: goal → capability → epic → (story)
- Ensure each epic is bounded, testable, and independently valuable
- Challenge epics that are too broad ("improve user experience") or too narrow ("change button color")
- Map dependencies between epics explicitly

### Anti-Patterns
- Do NOT produce epics that are just re-worded goals — epics are concrete capabilities, not aspirations
- Do NOT prescribe implementation decomposition — that's AI-DLC v1's job (epic-to-story breakdown is DLC Inception)
- Do NOT create epics without acceptance criteria — every epic needs a testable definition of "done at epic level"
- Do NOT skip dependency mapping — undetected dependencies cause sprint failures

### Quality Check
Every epic must pass: "Can a development team read this and understand WHAT to deliver (not how) and WHEN it's done (acceptance criteria)?" If no → refine.

---

## Depth Adaptation

| Depth | Behavior | Classification axes (Step 5.2) |
|-------|----------|--------------------------------|
| **Minimal** | 3-8 epics. One-line AC per epic. Minimal dependency mapping. | Epic Intent only |
| **Standard** | 5-15 epics. 3-5 AC per epic. Dependency matrix. Size estimation (S/M/L/XL). | + Value Type, Persona/Segment |
| **Comprehensive** | 10-30 epics. Detailed AC. Full dependency graph. Risk per epic. Cross-team coordination epics identified. | + Kano, Journey Stage, Business Capability |

---

## Steps

### Step 5.1: Identify Epics From Goals and Roadmap

For each product goal and roadmap "Now" item, ask: "What capabilities must exist for this goal to be achieved?"

> **Discovery input — big-picture event storming (optional).** If the team has run a big-picture EventStorming session (or any domain-event / process-flow discovery), use its **business-level** outputs — candidate domain events, pivotal events, and process flows — as a source for identifying capabilities and epics here. Event storming is a *discovery method that feeds* decomposition; its design-level vocabulary (aggregates, commands, policies, read models) is **not** tagged on epics — that model lives in AI-ADLC. Keep only the WHAT (the business capability an event implies), never the HOW (the domain model).

```
Goal: "Reduce payment processing time to <2s"
├── Epic: Enable async payment processing
├── Epic: Implement payment provider caching
└── Epic: Add payment performance monitoring

Goal: "Support 3 payment providers"
├── Epic: Build provider abstraction layer
├── Epic: Integrate Stripe
├── Epic: Integrate PayPal
└── Epic: Integrate Bank Transfer
```

**Rules:**
- Each epic serves exactly one goal (or clearly stated multiple goals)
- Each epic is independently deliverable (not dependent on ALL other epics completing first)
- Each epic name starts with a verb (Enable, Build, Integrate, Implement, Create, Establish)

### Step 5.2: Write Epic Definitions

For each epic, create a definition file in `epics/EPIC-NNN_{name}.md`:

```markdown
---
generatedBy: AI-POLC
generatedVersion: 1.0.0
source: {goal reference}
generatedOn: {ISO-date}
ownership: hybrid
---

# EPIC-{NNN}: {Epic Name}

## Goal Linkage
- Serves: {Goal name + metric}
- Theme: {Strategic theme}
- Roadmap Horizon: {Now | Next | Later}

## Classification
<!-- WHAT-level tags only. Depth-gated: Intent = all depths; Value Type + Persona = Standard+; Kano + Journey + Capability = Comprehensive. -->
- Epic Intent: {Business | Enabler:Architectural | Enabler:Infrastructure | Enabler:Exploration | Enabler:Compliance}   <!-- ALL depths -->
- Value Type: {Revenue | Cost-saving | Risk-reduction | Acquisition | Retention | Experience}   <!-- Standard+ -->
- Persona / Segment: {reference to AI-UXD persona, or segment name, or n/a}   <!-- Standard+ -->
- Kano Category: {Basic | Performance | Delighter}   <!-- Comprehensive — feeds Stage 6 prioritization -->
- Journey Stage: {Acquisition | Onboarding | Activation | Core-use | Retention | Expansion | Offboarding}   <!-- Comprehensive -->
- Business Capability: {capability-map node — a business function, not a technical component}   <!-- Comprehensive -->

## Description
{2-3 sentences: what this epic delivers, why it matters, who benefits}

## Acceptance Criteria (Epic Level)
- [ ] {Criterion 1 — testable}
- [ ] {Criterion 2 — testable}
- [ ] {Criterion 3 — testable}

## Dependencies
- Depends on: {EPIC-XXX or "none"}
- Blocks: {EPIC-YYY or "none"}
- External: {any external dependency}

## Size Estimate
- Complexity: {S | M | L | XL}
- Rationale: {one sentence why this size}

## Context-Aware Notes
{Any notes from context factors — e.g., "DDD architecture means this epic maps to the Payment bounded context"}
```

> **Work-complexity class (for delivery-method timing).** Beyond the size estimate, each epic carries an implicit work-complexity class — **Generic / Standard / Complex** — consumed by the velocity multiplier (`strategy/delivery-method-timing.md`). It is **derived, not elicited**: from the AI-ADLC Effort Band's **Technical Risk** flag when an AP is present (🟢 → Generic · 🟡 → Standard · 🔴 → Complex), else from the domain class in `domain-topology-map.md` (Generic/Platform → Generic · Supporting → Standard · Core → Complex). No new question and no new epic field required unless the team wants it explicit.

### Step 5.3: Map Dependencies

Build a dependency matrix:

| Epic | Depends On | Blocks | External Deps |
|------|-----------|--------|---------------|
| EPIC-001 | — | EPIC-003 | — |
| EPIC-002 | — | EPIC-004 | Payment provider API access |
| EPIC-003 | EPIC-001 | — | — |
| EPIC-004 | EPIC-002 | — | — |

Flag circular dependencies as errors. Flag long dependency chains (>3 deep) as risks.

### Step 5.4: Context-Factor Adaptation

| Context Factor | Epic Decomposition Impact |
|---|---|
| Architecture = DDD | Epics should align to bounded contexts where natural |
| Architecture = Microservices | Epics may span services — flag coordination needs |
| Scale = Multi-team | Add "coordination epics" for cross-team work |
| Compliance = Heavy | Add mandatory compliance epics (audit trail, data retention, consent) |
| Tech Debt = High | Identify refactoring epics; mark them explicitly as tech-debt |

### Step 5.5: Validate Epic Set

Check the complete epic set against:
- [ ] Every "Now" roadmap item has at least one epic
- [ ] Every product goal has at least one epic serving it
- [ ] No orphan epics (every epic links to a goal)
- [ ] No duplicate/overlapping epics
- [ ] Dependencies are acyclic
- [ ] Size distribution is reasonable (not all XL; not all S)
- [ ] Every epic has an **Epic Intent** (Business, or an Enabler subtype)
- [ ] Business-to-Enabler ratio is healthy — enablers support, not dominate, delivered value (flag if enablers outnumber business epics)
- [ ] At Standard+ every epic has a **Value Type**; at Comprehensive every epic also has Kano, Journey Stage, and Business Capability set

### Step 5.6: Tier 2 Integration Point

If Tier 2 is active (story elaboration enabled):
- After each epic is confirmed, decompose it into INVEST-compliant stories
- Load `tier2/story-elaboration.md` for story writing rules
- Stories become sub-items under the epic

If Tier 2 is inactive (default in chain mode):
- Epics are the terminal output of this stage
- AI-DLC v1's Inception will decompose epics into stories later

**On-the-fly Tier 2 offer:** POLC does NOT silently assume the Tier 2 setting. At the Stage 5 gate (Step 5.7 below), it explicitly asks the user whether to keep Tier 2 off (epics are the handoff) or turn it on now (elaborate stories). The user can flip this decision at any time during the workflow, not only here — if they later say "elaborate stories", activate Tier 2 and return to this integration point for the confirmed epics.

### Step 5.7: Offer Tier 2 at the Gate

Before closing the stage, surface the Tier 2 choice as a structured question so the user makes an informed, explicit decision:

```
### Q-5T: Story elaboration (Tier 2)

Context: Epics are confirmed. By default I stop at the epic level — in chain
mode AI-DLC v1 elaborates these into user stories during its Inception phase.
You can keep it there, or have me (POLC) write PO-quality user stories now.

Options:
  a) No — keep Tier 2 OFF; epics are the handoff artifact
  b) Yes — turn Tier 2 ON now; I'll elaborate stories (you'll then pick the format)

Recommended: (a) in chain mode with AI-DLC v1 present · (b) in standalone mode
or when you want PO-quality pre-elaboration before development.

Rationale: {state-derived — mention detected mode and whether AI-DLC v1 is chained}

Your Decision: _[awaiting input]_
```

- **On (a) "No":** set `Tier 2: inactive` in `polc-state.md`, log the decision, proceed to Gate 5.
- **On (b) "Yes":** set `Tier 2: active` in `polc-state.md`, load `tier2/story-elaboration.md`, ask the story-format question (Q2), then elaborate stories per confirmed epic before proceeding.
- Skip Q-5T only if the user has ALREADY explicitly set the Tier 2 state earlier in the session (then just confirm the recorded setting in one line).

---

## Gate

**Gate 5 — Epics Confirmed:**

Present to user:
```
Epic decomposition complete:
• Total epics: {N}
• By theme: {Theme A: N, Theme B: N, ...}
• By intent: {Business: N, Enabler: N}
• Dependencies: {N} inter-epic dependencies identified
• Size distribution: {S: N, M: N, L: N, XL: N}
• Coverage: All {N} goals have serving epics ✅
• Tier 2 (story elaboration): {ON — format: {style} | OFF — epics are the handoff}

Review the epic list. Any additions, removals, or adjustments?
Approve to proceed to Prioritization.
```

User must confirm before proceeding.

---

### Step 5.8: Derive Team-Domain Planning Artifacts (Post-Gate)

**Condition:** depth >= Standard AND user has approved Gate 5.

After gate approval, load `strategy/team-domain-planning.md` and derive the following artifacts:

1. **`team-epic-distribution.md`** — team load & ownership map
   - Scan all `epics/EPIC-NNN_*.md` files for team assignment, SP, release, shared ownership
   - Build the overview table, per-team detail, and load balance analysis
   - Generate Mermaid pie chart (team load) + ownership graph (shared epics)

2. **`domain-topology-map.md`** — bounded context & integration topology
   - Extract BC names from all epic files (`Bounded Context` field)
   - If Tier 2 is ON: extract full DDD Alignment (domain type, integration events, producers/consumers) → full event-flow topology
   - If Tier 2 is OFF: produce basic BC-to-team ownership map only (no event topology)
   - Generate Mermaid cluster graph (+ event-flow diagram if Tier 2 ON)

**Write:** Both files to `{outputRoot}/` immediately. Update `polc-state.md` → Planning Artifacts section (set both to `generated`, record timestamp).

**Skip conditions:**
- depth = Minimal → skip entirely (no planning artifacts at this stage)
- Fewer than 2 teams → skip `team-epic-distribution.md` (single-team product has no distribution to show)
- No BC fields populated in any epic → skip `domain-topology-map.md`

> **Q-5T enrichment (informed consent):** The Tier 2 offer (Step 5.7) should include the planning-artifact impact — with Tier 2 OFF the domain topology is basic (BC-to-team map only); with Tier 2 ON it includes full event-flow analysis, integration seams, and coupling assessment. Add this note to Q-5T's context block.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-004: Epic decomposition complete. {N} epics defined across {N} themes.
Intent split: {Business: N, Enabler: N}. Size distribution: {summary}. Dependencies: {N} identified.
All product goals covered.
```

---

## Transition

→ **Stage 6: Value-Based Prioritization** (Strategy continues)

---

*Detail file for AI-POLC Stage 5 | Phase: Strategy*
