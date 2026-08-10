# Automation-LENS Facet — AI-UXD

> **Loaded by the lens seam** when `Lens_Status.md` Automation row = `Automated`.
> **Integration points:** `define/` (interaction requirements), `design/` (patterns + design system), `validate/` (a11y + trust).
> **Persona:** UX Designer / Design System Lead (primary; sub-role `#persona-subrole-ux-designer` for flows, `#persona-subrole-audit-specialist` for validate).

---

## Purpose

Design how humans **configure, watch, approve, and stop** each automated feature. Automation UX is fundamentally about **trust, visibility, and control** — the user must be able to see what the automation did, understand why, intervene when needed, and stop it entirely.

---

## Guardrail

This facet operates strictly within the UX Designer's lane:
- Design **what the human sees and controls**.
- Define interaction patterns, information architecture, and design-system components for automation.
- DO NOT specify orchestration engines, queue mechanics, retry logic, or audit-log storage (AI-ADLC).
- DO NOT define the business rules the automation follows (AI-POLC authored the AC; ADLC implements the logic).

---

## When This Facet Fires

For each `automationFeature`-tagged item from the PBP:

1. **During define:** capture the human-control requirements (who configures, who monitors, who approves, who can stop).
2. **During design:** design the four UX surfaces (config, monitoring, approval, override) + add automation components to the design system.
3. **During validate:** verify accessibility of automation status/feedback + verify the trust model holds.

---

## Step 1: Read the Tagged Features

For each epic/story with `automationFeature: true`, read:
- `automationMode` (assisted / attended / unattended) — this drives how much UX is needed
- `automationPattern` — the nature of the work
- `automationTrigger` — how it fires
- `automationAcceptanceCriteria` — especially exception handling, human fallback, reversibility

### UX Depth by Sub-Mode

| Sub-mode | UX emphasis |
|----------|-------------|
| **Assisted** | The human is doing the work — automation UX is **inline assistance**. Light: a suggestion, a pre-fill, a shortcut. No monitoring dashboard needed. |
| **Attended** | The human triggers/approves — automation UX centers on the **approval queue + exception handling**. Medium: trigger control, approval interface, exception dashboard. |
| **Unattended** | No human in the loop during execution — automation UX centers on **observability + emergency control**. Heavy: run history, live status, alerting, kill-switch, audit view. |

---

## Step 2: Design the Four UX Surfaces

### 2.1 Configuration UX (`automationConfigModel`)

How does a user set up and parameterize the automation?

| Model | When to use | Design notes |
|-------|-------------|--------------|
| `form-based` | Few, simple parameters | Standard form; validation inline; sensible defaults |
| `rule-builder` | Conditional logic the user defines | Visual condition builder; if/then blocks; preview of matched items |
| `wizard` | Multi-step setup with dependencies | Progressive disclosure; step validation; summary before activation |
| `api-only` | Configured by developers, not end-users | No UI needed; document the config contract |

**Design requirements:**
- Show the **effect of the configuration** before activation ("this rule would match 47 of your current tickets").
- Make **activation explicit** — never auto-activate on save. A separate "activate" action with confirmation.
- Show **current state clearly** — is this automation on or off, right now?

### 2.2 Monitoring UX (`automationMonitoringModel`)

How does a user see what the automation is doing/has done?

| Model | When to use | Design notes |
|-------|-------------|--------------|
| `run-history` | Discrete runs (scheduled, event-triggered) | Chronological list; per-run status, duration, items processed, errors |
| `live-dashboard` | Continuous/high-volume | Real-time counters, throughput graph, queue depth, error rate |
| `queue-view` | Work-item automation (routing, approval) | Items in flight, items pending, items failed; filterable |
| `notification-only` | Low-frequency, low-stakes | Digest notifications; no persistent dashboard |

**Design requirements:**
- Every automated action must be **traceable** — the user can find "what happened to item X?"
- Show **why** the automation did what it did (which rule matched, what data drove the decision).
- **Failures must be visible** — never silently fail. Surface errors where the user will see them.
- Distinguish **automated vs. manual** actions visually (badge, icon, label).

### 2.3 Approval / Exception UX (`automationApprovalModel`)

Required for **Attended** mode; recommended for exception paths in Unattended mode.

| Model | When to use | Design notes |
|-------|-------------|--------------|
| `approval-queue` | Batch of items awaiting human decision | List with bulk actions; per-item detail on demand; approve/reject/defer |
| `inline-approve` | Approval within an existing workflow view | Approve/reject buttons in context; no separate queue |
| `batch-review` | Periodic review of automated decisions (audit-style) | Sampled or full list; "confirm all" with per-item override |
| `none` | Unattended with no approval step | Exception handling still needed — route failures somewhere visible |

**Design requirements:**
- Approvals must show **enough context to decide** without navigating away.
- **Exception queue is mandatory** for any automation with an unhappy path — items the automation couldn't handle must land somewhere a human sees them, with a clear "why it failed" reason.
- Support **bulk actions** where volume warrants, but never make bulk-approve the default (encourage review).

### 2.4 Override & Stop Controls (`automationOverrideControl`)

The human's off-switch. **Mandatory for Unattended mode.**

| Control | When to use | Design notes |
|---------|-------------|--------------|
| `pause-button` | Temporarily halt without losing state | Clear "paused" state; queued items held, not lost; resume restores |
| `kill-switch` | Emergency full stop (Unattended, controlled/safety-critical class) | Prominent, confirmable, immediate; document what happens to in-flight work |
| `per-item-cancel` | Stop one item's automation, not the whole feature | Item-level action; reverts or halts just that instance |
| `schedule-hold` | Suspend scheduled runs without disabling config | Skip next N runs; clear indication of held state |

**Design requirements:**
- The stop control must be **findable in an emergency** — not buried in settings.
- Show **what stopping does** — will in-flight work complete, roll back, or be abandoned?
- **Reversibility surfaces here** — if the AC says an automated action is reversible, the UI must expose the undo.
- For `controlled` / `safety-critical` control class: kill-switch is non-negotiable and must be reachable within 2 clicks.

---

## Step 3: Transparency — "Done Automatically"

Every automated action visible to a user must be **labeled as automated**. This is the automation analog of AI disclosure.

**Requirements:**
- A consistent visual treatment (badge, icon, or label) meaning "this was done by automation, not a person."
- Where a human would normally be the actor, name the automation instead ("Auto-assigned" not "Assigned by System").
- Provide a path to **"why?"** — one click to see the rule/logic that drove the action.

---

## Step 4: Design-System Additions

Add these automation components to the design system (only those the project needs):

| Component | Purpose |
|-----------|---------|
| **Automation status badge** | Indicates an item/action was automated; variants for success/failed/pending |
| **Run-history list** | Reusable chronological run display with status, duration, counts |
| **Queue/exception panel** | List of items needing attention, with reason + action |
| **Approval card** | Item awaiting decision with context + approve/reject actions |
| **Stop/pause control** | Standardized automation control with confirmation pattern |
| **Automation indicator (live)** | "Running" / "Paused" / "Error" state pill |
| **Rule-match explainer** | Compact "why this happened" disclosure |

Document each in the design system with states, variants, and accessibility requirements.

---

## Step 5: Validate — Accessibility & Trust

### Accessibility requirements

- **Status changes must be announced** — automation state changes (started, completed, failed) need ARIA live regions so screen-reader users are informed.
- **Automation badges need text alternatives** — an icon alone is insufficient; provide accessible labels.
- **Stop controls must be keyboard-reachable** — emergency controls cannot be mouse-only.
- **Run-history tables need proper headers and scope** — data tables must be navigable.
- **Error states must not rely on color alone** — pair color with icon + text.

### Trust validation

Ask (and design to answer):
1. Can the user tell **what the automation did**? (traceability)
2. Can the user tell **why**? (explainability)
3. Can the user **intervene**? (override)
4. Can the user **stop it**? (kill-switch)
5. Can the user **undo it**? (reversibility, where AC requires)
6. Does the user know **when it failed**? (error visibility)

If any answer is "no" for an Unattended feature, the UX is incomplete.

---

## Step 6: Record & Inform Downstream

Record per feature in the UXP:

```yaml
---
automationFeature: true
automationFeatureId: AUTO-{NNN}
automationConfigModel: {form-based | rule-builder | wizard | api-only}
automationMonitoringModel: {run-history | live-dashboard | queue-view | notification-only}
automationApprovalModel: {approval-queue | inline-approve | batch-review | none}
automationOverrideControl: {pause-button | kill-switch | per-item-cancel | schedule-hold}
---
```

Inform: "Automation Lens: control UX designed for {N} features — {list of automationFeatureIds}."

Downstream: AI-ADLC reads the control model to ensure the architecture supports it (e.g., a kill-switch requires an architectural circuit-breaker; a pause requires state preservation).

---

## Co-Design with AI-LENS

For a feature carrying both tags, design both UX layers coherently:
- AI disclosure ("AI-generated") + automation disclosure ("done automatically") should not produce two competing badges — design a combined treatment.
- AI HITL level and automation approval model must agree (e.g., AI `review-before-action` + automation `unattended` is a contradiction — flag it).

Flag any AI/automation UX contradiction to the user; it likely indicates a design conflict that the Coherence Gate will catch at ADLC.

---

## What This Facet Does NOT Do

- Does not choose orchestration engines, queues, or schedulers (AI-ADLC).
- Does not define retry/compensation logic (AI-ADLC).
- Does not implement the audit log (AI-ADLC designs it; AI-DWG provisions it).
- Does not write the business rules (AI-POLC).
- Does not verify the UX in the built product (AI-TGE `ATQ__`).

---

*Automation-LENS UXD Facet v1.0.0 | Integration: define + design + validate | Author: Maheri*
