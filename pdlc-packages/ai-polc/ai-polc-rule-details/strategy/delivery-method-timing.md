<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Delivery-Method & AI-Tool Timing — Velocity Model Rules

**Phase:** Strategy (capture at Stage 1; work-class at Stage 5; dual-calc + velocity model at Stage 7; re-derives on cascade)
**Purpose:** Make product timing **adaptive to the delivery method**. Capture how the team builds (manual, AI-assisted, AI-driven, or hybrid — and which AI tool), then compute timing with a work-complexity-aware velocity multiplier, always showing the **manual baseline alongside the chosen-method figures** so the plan is transparent, defensible, and reversible.

---

## MANDATORY: Stage Sub-Role

During velocity-model work, also adopt the **Resource Planner** sub-role (same as Stage 7 release slicing): think in delivery capacity and throughput, balance what we *want* against what we *can* ship, and treat the multiplier as a planning estimate to be reconciled against actuals — never a promise.

---

## Scope Invariant (read first)

The **timing multiplier** lives **entirely on the planning surface** — tool names and multipliers inform **only** POLC (and PILC/PPM) timing math and **never** drive build or governance behaviour. That boundary is absolute: naming a tool here changes *estimates*, never *enforcement*.

Separately, the **build discipline** — captured as `buildProfile` (`spec-driven` / `aidlc` / `freestyle`, or omitted for manual/AI-assisted) — **is** an active governance signal (un-parked 2026-08-09): AI-DWG populates it in the workspace manifest and AI-GCE reads it to tune drift-detection depth + gate cadence. This is a **distinct axis** from the multiplier: *how disciplined/gated* the build is legitimately shapes governance cadence, while *how fast* (the velocity multiplier) never does. When `buildProfile` is omitted (manual / AI-assisted), GCE uses its default **Standard** mode (full governance); only an explicit `freestyle` opt-in lightens it.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Capture delivery method only. If manual → single-track timing, no velocity model. If an AI method → apply the **blended** project multiplier (one number), single side-by-side compression line. No per-team velocity. |
| **Standard** | Full profile (method + tool + maturity + work-mix). Per-work-class multipliers, blended project multiplier, dual-track timing, per-team velocity (baseline + effective) feeding `capacity-planning-matrix.md`. |
| **Comprehensive** | Standard + per-team work-mix (each team's own blended multiplier), what-if on maturity/tool change, sensitivity note on the calibration. |

---

## 1. Delivery Method Profile

Captured once at project start (Stage 1) and persisted to `polc-state.md` → `## Velocity Model`. Four tiers:

| Tier | Meaning | Human role | Bottleneck | Baseline effect |
|------|---------|-----------|-----------|-----------------|
| **Manual / Traditional** | Human-written code, standard SDLC | Author | Coding capacity | 1× (baseline) |
| **AI-Assisted** | AI copilot (inline suggestions); human drives | Author, accelerated | Coding capacity (reduced) | Moderate multiplier |
| **AI-Driven** | AI generates the bulk; human steers & reviews | Reviewer / steerer | **Review & gateway capacity** | High multiplier; review becomes the new constraint |
| **Hybrid** | Mixed per work-type or per-team | Varies | Varies | Blended per segment |

> **Key insight for AI-Driven:** the gain shifts the bottleneck from *writing* to *reviewing/steering*. A tool that emits large batches but forces heavy human review does **not** deliver its raw throughput. The gateway model (§2) captures this.

`Delivery Method` is a **distinct** field from the existing `Delivery Methodology` context factor (Scrum/Kanban/SAFe/Shape Up). They never merge: one is *how code is produced*, the other is *the agile framework*.

---

## 2. AI-Tool "Nature" Model

When any AI method is chosen, capture **which tool** and profile it on the two axes that actually govern timing. Tools are described by *nature*, never ranked — "AI-driven with tool X" ≠ "AI-driven with tool Y".

**2.1 Decomposition model — the unit of work the tool produces**

| Granularity | Character | Throughput effect |
|-------------|-----------|-------------------|
| Line / token | inline autocomplete | Low-moderate — inline acceleration only |
| Edit / file | multi-file edits per prompt | Moderate |
| Spec-task | task-sized structured units | Moderate-high |
| Task / PR | feature-sized autonomous units | High |
| Bolt / increment | large decomposed increments with a defined lifecycle | High |

**2.2 Gateway model — the human checkpoints the tool imposes**

| Gateway cadence | Overhead effect |
|-----------------|-----------------|
| Inline accept/reject | Very low overhead, but low unit size |
| Per-file review | Low-moderate |
| Per-task approval | Moderate — structured gates |
| Per-PR review | Moderate-high — full review per unit |
| Per-bolt gate | Structured, heavier gate per large unit |

Larger units → more work per interaction (raises throughput). More/heavier gateways → more human bottleneck (lowers the *effective* multiplier). A tool's net effect is the balance of the two.

---

## 3. The Effective Multiplier

The multiplier is **never flat** — it varies by work-complexity class, because AI accelerates boilerplate far more than novel logic.

**Shipped default matrix (illustrative, owner-tunable — this table is authoritative; the model is explained in `knowledge_docs/HOW_DELIVERY_METHOD_TIMING_WORKS.md`):**

| Tool profile | Generic / boilerplate | Standard | Complex / novel |
|--------------|:--------------------:|:--------:|:---------------:|
| Manual (baseline) | 1× | 1× | 1× |
| AI-assisted — inline (line/token · inline gate) | 1.8× | 1.4× | 1.15× |
| AI-assisted — file (edit/file · per-file review) | 2.5× | 1.8× | 1.3× |
| AI-driven — task/PR (task · per-PR review) | 3.5× | 2.5× | 1.8× |
| AI-driven — bolt (increment · per-bolt gate) | 4× | 3× | 2× |

> These numbers are **illustrative and calibratable**, never hardcoded as "the" AI figure. The bolt-class row mirrors a field-observed 4× / 3× / 2× blend. Named tools are examples of a *profile*, not a ranking. An owner tunes these numbers in their installed copy of this rule; the model and a worked example are explained in `knowledge_docs/HOW_DELIVERY_METHOD_TIMING_WORKS.md`.

**Team-maturity discount** — a team new to a method realises only part of the theoretical gain. Applied to the *gain above baseline* so the result never drops below 1×:

```
effective_multiplier(work_class) = 1 + ( raw_matrix_value − 1 ) × maturityFactor
maturityFactor:  New 0.7  ·  Practiced 0.85  ·  Expert 1.0
```

Example — bolt-class, generic work (raw 4×): Expert → 4.0× · Practiced → 3.55× · New → 3.1×.

**Blended project multiplier** — weight the per-work-class effective multipliers by the project's work-complexity mix:

```
M_blended = Σ ( share(work_class) × effective_multiplier(work_class) )
```

---

## 4. Work-Complexity Classification (the multiplier's work-class axis)

Each epic is placed in a work-complexity class. **Prefer the architecture signal; fall back to product signal:**

1. **Primary — consume AI-ADLC (when an AP is present).** AI-ADLC emits a per-epic/area **Effort Band (S/M/L/XL) + Technical Risk** signal into `adlc-state.md` (read at Stage 1 workspace-detection, the same channel as the feasibility/cost-risk re-prioritization trigger). Map:
   - **Effort Band → size (SP base):** S=3 · M=5 · L=8 · XL=13 (identical to `team-domain-planning.md` Rule 1 — one shared mapping).
   - **Technical Risk → work class (multiplier column):** 🟢 low → Generic/boilerplate · 🟡 med → Standard · 🔴 high → Complex/novel.
   Effort sizes the work; risk (novelty proxy) picks the acceleration column. Do **not** re-derive complexity independently when the AP signal exists.
2. **Fallback — POLC domain classification.** When no AP is present, use the domain class already produced in `domain-topology-map.md`: Generic/Shared-kernel/Platform → Generic · Supporting → Standard · Core (differentiator) → Complex.

The blended multiplier is therefore a **weighted average over the real epic/domain mix**, not a single guessed constant.

---

## 5. Dual Calculation (mandatory when an AI method is chosen)

Every timing-bearing figure renders **both tracks**:

- **Manual baseline** — what the scope would take traditionally (1×). Always retained, never discarded.
- **Chosen method** — with the effective per-work-class multipliers and maturity discount applied.
- **Delta / compression** — e.g. `Manual = {A} · {method} = {B} · compression {1 − B/A}`.

If **Delivery Method = manual**, only the baseline renders — no dual columns. The dual view activates *only* when an AI method is chosen; artifact structure is unchanged, only the numbers differ.

---

## 6. The `## Velocity Model` Section (written to `polc-state.md`)

This rule owns the section below. It is a **dual-consumer** contract — `team-domain-planning.md` Rule 4 reads **Per-Team Velocity**; the dual-calc figures here and in `release-plan.md` read the **Delivery Method Profile + Multiplier Matrix**. Keep it minimal (additive-only; no restructuring of existing state).

```markdown
## Velocity Model

### Delivery Method Profile
- Delivery Method: {manual | ai-assisted | ai-driven | hybrid}
- AI Tool: {tool name | "n/a"}
- Team AI Maturity: {new | practiced | expert}
- Work-Complexity Mix: generic {x%} / standard {y%} / complex {z%}   ← from ADLC bands (§4) or domain classification

### Effective Multiplier Matrix (after maturity discount)
| Work class | Manual | {method} |
|------------|:------:|:--------:|
| Generic    | 1×     | {m_g}×   |
| Standard   | 1×     | {m_s}×   |
| Complex    | 1×     | {m_c}×   |
- Blended project multiplier: {M}×

### Per-Team Velocity (SP/sprint)
| Team | Baseline (manual) | Effective (AI-adjusted) |
|------|:-----------------:|:-----------------------:|
| {team} | {v}             | {v × team-blended multiplier} |
- plannedVsBaseline: manual {A} · {method} {B} · compression {1 − B/A}
```

- **Per-Team Velocity** baseline is a planning input — a PO assumption at Stage 7, or actuals when the build engine has reported them. The Effective column = baseline × the team's applicable blended multiplier. `capacity-planning-matrix.md` reads this section unchanged and simply renders a **dual capacity** (baseline vs effective).
- **Planned vs actual:** `plannedVelocity` here is the pre-build estimate. It is distinct from the `velocity.trend` enum in the Dashboard Summary (actual, read back from the build engine). At Stage 15 (Acceptance & Feedback), reconcile planned → actual and re-derive if they diverge materially.

---

## 7. Elicitation (structured `### Q` blocks)

Ask at Stage 1 (or inherit from `pilc-state.md` when chained — never re-ask what upstream already captured). Follow the standard question format (Context → Options → Recommended → Rationale → "Your Decision").

### Q-DM1: Delivery method
- **Context:** How will this product be built? This materially changes timing.
- **Options:** (a) Manual / traditional · (b) AI-assisted (copilot) · (c) AI-driven (AI generates, human steers) · (d) Hybrid (mixed).
- **Recommended:** (a) unless the team has already adopted an AI build tool — the baseline is always the honest default.
- **Rationale:** the manual baseline is always computed; an AI choice only *adds* the second track.

### Q-DM2: AI tool (only if b/c/d)
- **Context:** Which tool(s)? The tool's decomposition + gateway nature drives the real multiplier.
- **Options:** offer the shipped profiles (inline · file · task/PR · bolt classes) with example tools; plus **"Other / custom"**.
- **Custom fallback:** for "Other", ask two short questions — (1) what unit of work does it produce (line / file / task / PR / increment)? (2) what human checkpoint does it impose (inline / per-file / per-task / per-PR / per-batch)? — then map to the closest shipped profile. No open-ended modelling.

### Q-DM3: Team AI maturity (only if b/c/d)
- **Options:** New · Practiced · Expert. Sets the maturity discount (§3).

### Q-DM4: Work-complexity mix
- **Context:** Roughly what share of the work is boilerplate vs standard vs novel?
- **Auto-derive:** when AP Effort Bands / domain classification exist, propose the mix from them and ask only to confirm.

Log each confirmed answer in the Decision Log (`POLC-D-NNN`).

---

## 8. Cascade Rule (unified with team-domain planning)

Changing the **delivery method**, the **AI tool**, or the **team-maturity** setting re-derives all timing artifacts. This is the **same mechanism** as the `team-domain-planning.md` cascade (trigger "velocity model updated") — implement once, not twice:

```
delivery-method / tool / maturity change
  → recompute the Velocity Model (polc-state.md)
  → re-derive: release-plan.md, capacity-planning-matrix.md, roadmap.md (dates, if dual-date active), backlog dashboard
  → (chain) refresh PILC resource-budget / business-case timeline / feasibility schedule
  → (portfolio) PPM roll-up refresh
  → log POLC-C-NNN
```

---

## 9. Generic & External-Tool Notes

- **Generic:** no project-specific content; all values are `{placeholders}`. The §3 multiplier table is a shipped default an owner tunes in their installed copy; the model is explained in `knowledge_docs/HOW_DELIVERY_METHOD_TIMING_WORKS.md`.
- **External tools are examples, not endorsements.** Where a named external build tool is used as a profile example (e.g. a bolt-class lifecycle tool¹), it is one profile among many and never "the" AI model.

> ¹ Any externally named AI build lifecycle (e.g. Amazon's AI-DLC) is a third-party product, not part of this family; it is referenced only as an illustrative tool profile.

---

## Governance Spine Entry

Log in the Decision Log when the profile is set or changed:
```
POLC-D-NNN: Delivery method set to {method}{ / tool}. Team AI maturity: {maturity}.
Blended multiplier: {M}×. Manual baseline retained. Dual-track timing {active | n/a (manual)}.
```

---

## Integration Points Summary

| When | Action | Load This File? |
|------|--------|:---------------:|
| Stage 1 (workspace-detection) | Capture/inherit delivery method + tool + maturity; seed the Velocity Model profile | Yes |
| Stage 5 (epic-decomposition) | Assign each epic a work-complexity class (ADLC band → risk column, or domain class) | Yes |
| Stage 7 (release-slicing, post-gate) | Compute multipliers + per-team velocity; write dual-track figures; pairs with `team-domain-planning.md` | Yes |
| Stage 15 (acceptance-feedback) | Reconcile planned vs actual velocity; re-derive on material divergence | Yes |
| Cascade trigger (method/tool/maturity change) | Re-derive all timing artifacts (unified cascade) | Yes |

---

*Detail file for AI-POLC Delivery-Method & AI-Tool Timing | Phase: Strategy | Pairs with `strategy/team-domain-planning.md`*
