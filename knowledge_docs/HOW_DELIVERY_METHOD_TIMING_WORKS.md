# How Delivery-Method Timing Works

**Purpose:** Explains how the AI-Driven Product Ownership Life Cycle (AI-POLC) makes product timing **adaptive to the delivery method** — capturing whether a team builds manually, AI-assisted, or AI-driven, then computing release/capacity timing with a work-complexity-aware velocity multiplier while always showing the manual baseline alongside the chosen-method figures.

---

## Why Delivery Method Changes Timing

Two teams building identical scope on different delivery methods operate on completely different throughput curves. A team writing every line by hand, a team using an inline copilot, and a team steering an autonomous agent that generates large increments will not finish the same backlog in the same time. Traditional planning assumes a single (implicitly manual) model and bakes that assumption into every date. AI-POLC makes the assumption explicit and adjustable.

The model rests on three ideas:

1. **The multiplier is never flat.** AI accelerates boilerplate far more than novel logic, so the speed-up varies by work-complexity class (generic vs standard vs complex).
2. **AI tools differ by nature.** A tool's *decomposition model* (how big a unit of work it produces) and its *gateway model* (how much human review it forces) drive its real impact — not a single "AI is faster" constant.
3. **The manual baseline is always kept.** When an AI method is chosen, every timing figure shows both tracks plus the compression delta, so the plan stays transparent, defensible, and reversible.

---

## The Delivery-Method Tiers

| Tier | Who does the work | Where the bottleneck moves |
|------|-------------------|----------------------------|
| **Manual / Traditional** | Humans author the code | Coding capacity (the baseline, 1×) |
| **AI-Assisted** | AI suggests, humans drive | Coding capacity, reduced |
| **AI-Driven** | AI generates, humans steer & review | **Review & gateway capacity** — reviewing becomes the new constraint |
| **Hybrid** | Mixed per work-type or team | Varies per segment |

The key insight for AI-driven delivery: the gain shifts the bottleneck from *writing* to *reviewing*. A tool that emits huge batches but forces heavy human review does not deliver its raw throughput — the model accounts for that.

---

## How the Multiplier Is Built

The effective speed-up for a piece of work is a function of the tool's nature and the work's complexity, discounted by how experienced the team is with the method:

```
effective_multiplier(work_class) = 1 + ( raw_gain(tool, work_class) − 1 ) × maturityFactor
maturityFactor:  New 0.7  ·  Practiced 0.85  ·  Expert 1.0
```

- **raw_gain** comes from a tool × work-class table (a shipped, tunable default).
- **maturityFactor** reflects that a team new to a method captures only part of the theoretical gain (and the "1 +" form keeps the result from ever dropping below the manual baseline).
- The **blended project multiplier** is the weighted average across the project's actual mix of generic / standard / complex work.

> The authoritative, tunable default table (and the full rules) live in the AI-POLC rule `strategy/delivery-method-timing.md`. Owners adjust the numbers in their installed copy to match their own observed velocity — the numbers shipped are illustrative starting points, never fixed truth. Named tools (including any external build lifecycle) are examples of a *profile*, not a ranking or an endorsement.

---

## Where the Work-Complexity Class Comes From

Each epic is placed in a work-complexity class without asking the user a new question:

| Source (in priority order) | Signal | Maps to work class |
|-----------------------------|--------|--------------------|
| AI-Driven Architecture Design Life Cycle (AI-ADLC), when present | per-epic **Technical Risk** flag | 🟢 low → Generic · 🟡 med → Standard · 🔴 high → Complex |
| AI-POLC domain classification (fallback) | domain type | Generic/Platform → Generic · Supporting → Standard · Core → Complex |

The architecture package's **Effort Band** (S/M/L/XL) separately sizes the work (S=3 · M=5 · L=8 · XL=13 story points), while the risk flag picks the acceleration column. This reuses signals the chain already produces rather than inventing a parallel estimate.

---

## How It Flows Through the Lifecycle

| When | What happens |
|------|--------------|
| **Intake (Stage 1)** | Capture the delivery method + AI tool + team maturity — or inherit them from the upstream project-initiation state. Manual is the default. |
| **Epic decomposition (Stage 5)** | Each epic gets its work-complexity class (derived, above). |
| **Release slicing (Stage 7)** | Compute the multipliers and per-team velocity; write the `## Velocity Model` and render dual-track release, capacity, and (optionally) roadmap-date figures. |
| **Acceptance & feedback (Stage 15)** | Reconcile the planned velocity against the actuals reported by the build engine; re-derive if they diverge. |
| **Any change** | Changing the method, tool, or maturity re-derives every timing artifact through one unified cascade. |

The captured profile lives in the product state's `## Velocity Model` section, which is the single source both the capacity-planning view and the dual-calc figures read.

---

## A Worked Example

A team plans a release of mixed work — say 50% generic, 30% standard, 20% complex — with a baseline team velocity of 20 story points per sprint.

- **Manual baseline:** 20 SP/sprint (1× across the board).
- **AI-driven with a task/PR-class tool, practiced team:** the blended multiplier works out to roughly 2.6×, so effective velocity ≈ 52 SP/sprint.
- **Result shown to stakeholders:** "Manual = 8 sprints · AI-driven = ~3 sprints · ~60% compression." Both tracks are shown; the team can defend the plan either way, and if they revert to manual the baseline is already there.

*(Illustrative only — real numbers depend on the tuned multiplier table and the team's own velocity.)*

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Always keep the manual baseline | Transparency and reversibility — stakeholders see what the choice buys |
| Multiplier varies by work class | AI helps boilerplate far more than novel logic; a flat number misleads |
| Tool profiled by decomposition + gateway | Captures why "AI-driven" with different tools yields different throughput |
| Reuse architecture Effort Band + Risk | No parallel complexity estimate; one source of truth |
| Keep S/M/L/XL sizing | No story-point overhead; the same size→points mapping the planning views already use |
| Planning-surface only | Tool names and multipliers inform estimates, never build or governance enforcement |

---

## Anti-Patterns

| Anti-Pattern | Why it's wrong |
|-------------|----------------|
| One flat "AI is 3× faster" number | Ignores work complexity and tool nature — over-promises on novel work |
| Dropping the manual baseline | Removes the ability to defend or reverse the plan |
| Letting the tool choice change enforcement | Timing is a planning concern; governance stays build-method-agnostic |
| Treating shipped multipliers as fixed truth | They are tunable starting points — calibrate against real velocity |
| Asking the user to hand-classify every epic | The class is derived from signals the chain already has |

---

## Related Documents

| Document | Location |
|----------|----------|
| How product ownership works | [`HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md`](HOW_POLC_PRODUCT_OWNERSHIP_WORKS.md) |
| How to manage a product backlog | [`HOW_TO_MANAGE_PRODUCT_BACKLOG.md`](HOW_TO_MANAGE_PRODUCT_BACKLOG.md) |
| How depth levels work | [`HOW_DEPTH_LEVELS_WORK.md`](HOW_DEPTH_LEVELS_WORK.md) |
| How state files work | [`HOW_STATE_FILES_WORK.md`](HOW_STATE_FILES_WORK.md) |
| Why lifecycle sequence matters | [`WHY_LIFECYCLE_SEQUENCE_MATTERS.md`](WHY_LIFECYCLE_SEQUENCE_MATTERS.md) |

*Knowledge Document | Created: 2026-08-09 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
