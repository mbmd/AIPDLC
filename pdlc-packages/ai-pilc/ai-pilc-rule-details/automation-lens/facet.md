# Automation-LENS Facet — AI-PILC

> **Loaded by the lens seam** when `Lens_Status.md` Automation row = `Automated` (or when no mode exists yet — PILC promotes the mode into the project spine).
> **Integration points:** `inception/` (Stage 1–3), `assessment/` (Stage 4–7), `justification/` (Stage 8).
> **Persona:** PMO Professional / Senior Project Manager (primary; sub-role `#persona-subrole-risk-analyst` for suitability/risk, `#persona-subrole-financial-analyst` for ROI/business case).

---

## Purpose

Promote the Automation-LENS mode into the project's governance spine as a formal `Decision_Log` row, then assess the automation dimension across process suitability, ROI, and control classification. PILC is where the idea-level posture becomes a project-level commitment with business-case justification and governance depth.

---

## When This Facet Fires

1. **During inception (Stage 1–3):** promote the automation mode into the spine `Decision_Log` + update `Lens_Status.md`.
2. **During assessment (Stage 4–7):** process suitability assessment.
3. **During justification (Stage 8):** automation ROI and control-class classification in the business case.

---

## Step 1: Mode Promotion (at Inception)

### If an Idea Brief with Automation Posture exists (chain mode from ILC):

- Read the `automationPosture` from the Idea Brief.
- Promote it into the project's `Decision_Log.md` as a formal row:

```markdown
| PILC-{ABBREV}-D-{N} | PILC | {date} | Automation-LENS mode set: Automated ({sub-modes}) | Promoted from Idea Brief Automation Posture: {posture} | Manual / Automated (multi-select) | Automated: {sub-modes} | Idea Brief assessment + process-efficiency alignment | {user} |
```

- **Dual-write:** also upsert `Lens_Status.md` (per `LENS_STATUS_MECHANISM.md` §4):
  - Upsert the Automation row: `| Automation | Automated | {sub-modes} | {date} | PILC-{ABBREV}-D-{N} | PILC |`
- Create the spine and/or `Lens_Status.md` if absent (per MF §4: create-if-absent).

### If no Idea Brief (standalone / direct entry):

- Run the full Resolution Protocol (as defined in `AUTOMATION_LENS_PROTOCOL.md` §2):
  - Ask: "Manual, or Automated? If Automated, which stances? (Assisted / Attended / Unattended — multi-select)"
  - Record the choice as a `Decision_Log` row + upsert `Lens_Status.md` (same dual-write).

### Inform & Proceed

After recording, inform:
```
Automation Lens: Automated — {sub-modes}, recorded as PILC-{ABBREV}-D-{N}.
Change anytime with _AUTOLENS_.
```

---

## Step 2: Process Suitability Assessment (at Assessment Stage)

When the assessment phase runs and the mode = `Automated`, add an automation-specific suitability dimension:

### Suitability Criteria

| Criterion | Key question | Good signal | Bad signal |
|-----------|-------------|-------------|------------|
| **Process stability** | Is the process well-defined and stable, or still evolving? | Documented, stable for 6+ months | Ad-hoc, changes monthly, undefined |
| **Rules-based** | Can the logic be expressed as deterministic rules? | Clear decision trees, policy tables | Judgment calls, contextual intuition |
| **Volume** | Is it high-volume enough to justify automation investment? | Hundreds/thousands per day/week | A few times a month (manual is fine) |
| **Structured input** | Is the input data structured and machine-readable? | Forms, structured tickets, API payloads | Free-form email, phone calls, PDFs |
| **Exception rate** | How often does the happy path NOT apply? | < 15% exceptions (automatable majority) | > 40% exceptions (automation drowns in edge cases) |
| **Current cost** | How much human effort does this consume today? | Multiple FTEs, measurable hours/week | Trivial effort (automation ROI negligible) |

### Suitability Score

Rate each criterion: ✅ Suitable / ⚠️ Partial / ❌ Not suitable.

| Score | Meaning |
|-------|---------|
| 5–6 ✅ | Highly automatable — strong ROI case |
| 3–4 ✅ + ⚠️ | Automatable with caveats — note the gaps |
| ≤ 2 ✅ | Weak automation candidate — consider Manual (or Assisted only) |

### Recording

Add to the PIP's feasibility section under `## Process Suitability for Automation`:

```markdown
## Process Suitability for Automation

| Criterion | Assessment | Notes |
|-----------|-----------|-------|
| Process stability | {✅/⚠️/❌} | {detail} |
| Rules-based | {✅/⚠️/❌} | {detail} |
| Volume | {✅/⚠️/❌} | {detail} |
| Structured input | {✅/⚠️/❌} | {detail} |
| Exception rate | {✅/⚠️/❌} | {detail} |
| Current cost | {✅/⚠️/❌} | {detail} |

**Overall suitability:** {Highly automatable / Automatable with caveats / Weak candidate}
```

If overall = `Weak candidate`, inform the user; they may choose to flip the mode to `Manual` or downgrade to `Assisted` only (append a new Decision_Log row + upsert Lens_Status).

---

## Step 3: Automation ROI (at Justification Stage)

When building the business case and the mode = `Automated`, add automation-specific ROI dimensions. Automation's business case is **ROI-led** (concrete, measurable operational savings):

### ROI Categories

| Category | What to capture | How to measure |
|----------|-----------------|----------------|
| **Hours saved** | Human labor eliminated per period | hours/week × hourly cost |
| **FTE displacement** | Full-time equivalents freed up | FTEs × loaded annual cost |
| **Error-rate reduction** | Fewer human errors in the process | current error rate × cost-per-error × volume |
| **Cycle-time improvement** | Faster end-to-end process completion | current duration → automated duration |
| **Compliance improvement** | Reduced audit findings / policy violations | current non-compliance cost |
| **Scalability** | Volume can grow without proportional staff growth | projected growth × per-unit-manual-cost avoided |

### Recording

Add to the business case under `## Automation ROI`:

```markdown
## Automation ROI

| Metric | Current state | Automated state | Annual saving |
|--------|--------------|-----------------|---------------|
| Hours saved | {hours/week manual} | {hours/week remaining} | {annual value} |
| Error reduction | {current rate} | {target rate} | {annual cost avoided} |
| Cycle time | {current duration} | {automated duration} | {throughput gain value} |
| Scalability | {manual cost/unit} | {automated cost/unit} | {projected savings at growth} |

**Total annual ROI estimate:** {sum}
**Payback period:** {months} (implementation cost / annual saving)
**Break-even volume:** {units/period at which automation cost < manual cost}
```

---

## Step 4: Automation Control Class (at Assessment Stage)

Classify the automation's control/regulatory posture. This is the automation analog of the EU AI Act class — it determines governance depth downstream.

### Classification Guide

| Class | Criteria | Governance implications |
|-------|----------|------------------------|
| **Informational** | Automation only reads/reports; does not mutate business state | Light governance; audit trail recommended |
| **Operational** | Automation performs standard business operations (assignments, notifications, status updates) | Standard governance; audit trail required; reversibility required |
| **Controlled** | Automation handles regulated operations (financial transactions, HR actions, compliance submissions, SOX-scope processes) | Heavy governance; **segregation of duties mandatory**; dual-control/four-eyes; full audit trail; periodic human review |
| **Safety-critical** | Automation impacts physical safety, life/health, or critical infrastructure | Maximum governance; fail-safe mandatory; human-in-the-loop override; regulatory conformity assessment; kill-switch with SLA |

### Recording

Add to the PIP feasibility section under `## Automation Control Class`:

```markdown
## Automation Control Class

| Feature/Process | Proposed class | Rationale | Key governance obligation |
|-----------------|---------------|-----------|---------------------------|
| {process name} | {informational/operational/controlled/safety-critical} | {one-line reasoning} | {primary obligation} |

**Highest class across features:** {class}
**Governance depth for this project:** {light / standard / heavy / maximum}
```

If any feature = `safety-critical`: flag immediately. The user must confirm they are prepared for the full regulatory/safety governance burden. `ATG__` will later enforce the complete obligation set.

If any feature = `controlled`: note that segregation-of-duties and dual-control requirements will be enforced by AI-GCE's `ATG__` agent during development.

---

## What This Facet Does NOT Do

- Does not identify individual automated features in the backlog (AI-POLC).
- Does not design configuration, monitoring, or approval UX (AI-UXD).
- Does not make orchestration/engine/infrastructure decisions (AI-ADLC).
- Does not provision runtime infrastructure (AI-DWG).
- Does not enforce SoD, audit-trail, or kill-switch compliance (AI-GCE `ATG__`).
- Does not verify idempotency, exception paths, or loop termination (AI-TGE `ATQ__`).

---

*Automation-LENS PILC Facet v1.0.0 | Integration: Inception (mode promotion) + Assessment (suitability/control-class) + Justification (ROI) | Author: Maheri*
