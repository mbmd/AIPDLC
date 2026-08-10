<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Advanced Discovery (Full Rules)

**Stage:** 4 (Product Discovery & Roadmap)
**Adds:** OKR hierarchy, JTBD framing, opportunity scoring, hypothesis backlog, impact mapping

---

## Additional Steps (append to Stage 4)

### Step 4.E1: Build OKR Hierarchy

For each strategic theme, define Objectives and Key Results:

```
Objective: {Qualitative, inspirational goal}
├── KR1: {Quantitative, measurable result} — Target: {X} by {date}
├── KR2: {Quantitative, measurable result} — Target: {X} by {date}
└── KR3: {Quantitative, measurable result} — Target: {X} by {date}
```

**Rules:**
- 2-4 Objectives per quarter/cycle
- 2-4 Key Results per Objective
- Key Results are MEASURABLE (number, percentage, binary)
- Objectives are ASPIRATIONAL (not "maintain" — push growth)
- OKRs align to product goals (Stage 2) — they're the same goals in OKR format

### Step 4.E2: JTBD Framing

For each user segment, define jobs:

```
When {situation},
I want to {motivation/job},
So I can {expected outcome}.
```

**Job categories:**
- Functional jobs (what they're trying to do)
- Emotional jobs (how they want to feel)
- Social jobs (how they want to be perceived)

Map jobs to epics: which epics address which jobs?

### Step 4.E3: Opportunity Scoring (RICE)

Score each roadmap item:

| Item | Reach | Impact | Confidence | Effort | RICE Score |
|------|:---:|:---:|:---:|:---:|:---:|
| {Capability A} | 5000 users | 3 (high) | 80% | 2 sprints | 6000 |
| {Capability B} | 1000 users | 2 (medium) | 50% | 4 sprints | 250 |

**RICE = (Reach × Impact × Confidence) / Effort**

Use RICE to validate/adjust the roadmap horizon placement.

### Step 4.E4: Hypothesis Backlog

For uncertain capabilities, frame as testable hypotheses:

| # | Hypothesis | Test Method | Success Criteria | Epic Impact |
|---|-----------|------------|-----------------|-------------|
| H1 | Users prefer {X} over {Y} | A/B test | +15% conversion | EPIC-005 |
| H2 | Market wants {feature} | Smoke test landing page | >500 sign-ups/week | EPIC-009 |

**Rules:**
- Hypotheses are tested BEFORE full build commitment
- Failed hypothesis → epic deprioritized or removed
- Validated hypothesis → proceed with confidence

### Step 4.E5: Impact Mapping

Connect goals to deliverables through the behaviours that actually move them. An impact map is a four-level tree — **Goal → Actors (who) → Impacts (how their behaviour changes) → Deliverables (what we build)**:

```
Goal: {measurable business goal — reuse a Stage 2 goal / OKR Objective}
├── Actor: {who can help or hinder the goal?}
│   ├── Impact: {what behaviour change in this actor moves the goal?}
│   │   ├── Deliverable: {what could we build/do to cause that impact?}  → {EPIC-00X}
│   │   └── Deliverable: {alternative — often cheaper}                    → {EPIC-00Y}
│   └── Impact: {another behaviour change}
└── Actor: {another actor}
```

**Rules:**
- Anchor every map on ONE measurable goal (reuse a Stage 2 goal or an OKR Objective — do not invent a new one)
- Deliverables are **hypotheses about impact**, not commitments — the map's power is showing which deliverables you can safely *drop*
- Rank deliverables by expected contribution to the goal; the lowest-contribution branches are your first de-scope candidates
- Every deliverable traces down to an epic (Stage 5) and up to a goal (Stage 2) — no orphan deliverables
- Prefer the cheapest deliverable that could cause a needed impact (impact mapping is a scope-cutting tool first)

**Feeds:** epics (Stage 5) — deliverables become or link to epics; roadmap (Stage 4) — goal-ranked deliverables inform Now/Next/Later; prioritization — low-contribution branches are de-scope candidates. This **operationalizes the "Impact Mapping" method already named in the POLC methodology-alignment line**.

---

## Additional Output

When this extension is active, `roadmap.md` additionally contains:
- OKR section (Objectives + Key Results)
- JTBD mapping (jobs → epics)
- RICE scores (if used for opportunity scoring)
- Hypothesis backlog (linked to relevant epics)
- Impact map (goal → actors → impacts → deliverables; low-contribution branches flagged as de-scope candidates)
