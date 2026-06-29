<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Tier 2: Story Elaboration

**Activation:** User-enabled. Off by default in chain mode (AI-DLC v1 Inception handles story creation). Active by user choice in standalone mode.
**Purpose:** Decompose epics into INVEST-compliant user stories with Given/When/Then acceptance criteria — the full PO authoring function for teams without AI-DLC v1.

---

## Activation Rules

| Context | Tier 2 Status | Rationale |
|---------|:---:|---|
| Chain with AI-DLC v1 (default) | ⬜ OFF | DLC Inception creates stories from epics |
| Chain + user explicitly enables | ✅ ON | User wants PO-quality pre-elaboration before DLC |
| Standalone (user enables) | ✅ ON | No DLC — POLC must produce implementation-ready stories |
| Standalone (user declines) | ⬜ OFF | User produces stories themselves or uses another tool |

**Activation trigger:** User says "elaborate stories" / "write user stories" / "I need stories not just epics" / enables Tier 2 in settings.

---

## De-Duplication Rule (Chain + Tier 2 Active)

When BOTH AI-POLC Tier 2 AND AI-DLC v1 are in play:
- AI-POLC produces stories first (PO-quality, value-framed)
- AI-DLC v1 Inception may further refine or re-elaborate
- **POLC's stories take precedence** on acceptance criteria and value framing
- **DLC's refinement takes precedence** on implementation decomposition (units of work)
- If DLC produces a story that contradicts POLC's AC → flag for PO review

---

## Story Writing Rules

### INVEST Criteria

Every story must satisfy:

| Letter | Criterion | Test |
|:---:|---|---|
| **I** | Independent | Can be developed without depending on another story in the same sprint |
| **N** | Negotiable | Details can be discussed; it's not a rigid spec |
| **V** | Valuable | Delivers value to a user or business stakeholder |
| **E** | Estimable | Team can size it (enough clarity to estimate) |
| **S** | Small | Fits in one sprint (if too big → split) |
| **T** | Testable | Clear criteria for pass/fail |

### Story Format

```markdown
## Story: {Title}

**Epic:** EPIC-{NNN}
**Priority:** {rank from register}

### User Story
As a {user role},
I want to {action/capability},
So that {benefit/value}.

### Acceptance Criteria

**AC1:** {Title}
- Given {precondition}
- When {action}
- Then {expected outcome}

**AC2:** {Title}
- Given {precondition}
- When {action}
- Then {expected outcome}

**AC3:** {Title}
- Given {precondition}
- When {action}
- Then {expected outcome}

### Notes
- {Any context, constraints, or out-of-scope clarifications}
- {Edge cases to consider}

### Size Estimate
- Points: {N} (or T-shirt: {S|M|L})
```

### Acceptance Criteria Rules

- **Minimum 3 AC per story** (happy path + edge case + error case)
- **Given/When/Then format mandatory** — no prose acceptance criteria
- **Each AC must be independently testable** — pass/fail deterministic
- **No implementation language** — describe behavior, not code
- **Measurable where possible** — "response within 2 seconds" not "fast response"

---

## Elaboration Process (Per Epic)

### Step T2.1: Identify Stories From Epic

For each epic, ask: "What are the distinct user-facing behaviors this epic delivers?"

```
EPIC-003: Provider Abstraction Layer
├── Story: Configure payment provider via admin panel
├── Story: Process payment through abstraction (provider-agnostic)
├── Story: Handle provider failover transparently
├── Story: View payment provider health status
└── Story: Switch active provider without downtime
```

### Step T2.2: Write Each Story

Apply the format above. Ensure INVEST compliance for each.

### Step T2.3: Validate Story Set

Per epic:
- [ ] Stories cover all epic acceptance criteria
- [ ] No gaps (epic AC not addressed by any story)
- [ ] No overlaps (two stories addressing the same AC)
- [ ] All stories are independent (can be built in any order within the epic)
- [ ] Total size is reasonable (not 20 stories for an M-sized epic)

### Step T2.4: Check Against DoR

Every story must meet the Definition of Ready (Stage 8) before it's considered sprint-ready:
- [ ] Clear description (WHAT, not HOW)
- [ ] AC defined and testable
- [ ] Goal/epic linkage documented
- [ ] No unresolved blocking dependencies
- [ ] Size estimated

---

## Output Location

Stories are stored under the epic folder:
```
epics/
├── EPIC-001_async-processing.md          ← Epic definition
├── EPIC-001_stories/                     ← Tier 2 output
│   ├── STORY-001-01_configure-async.md
│   ├── STORY-001-02_process-async.md
│   └── STORY-001-03_monitor-async.md
├── EPIC-002_stripe-integration.md
├── EPIC-002_stories/
│   └── ...
```

---

## Interaction With Stage 5

When Tier 2 is active, Stage 5 (Epic Decomposition) gains an additional step:
- After each epic is confirmed → immediately elaborate into stories
- Present stories for user review before moving to next epic
- This makes Stage 5 longer but produces a more complete PBP

---

*Tier 2 detail file for AI-POLC | Loaded when Tier 2 is activated*
