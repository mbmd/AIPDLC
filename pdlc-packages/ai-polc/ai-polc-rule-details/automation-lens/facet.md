# Automation-LENS Facet — AI-POLC

> **Loaded by the lens seam** when `Lens_Status.md` Automation row = `Automated`.
> **Integration points:** `strategy/epic-decomposition.md` (Stage 5, Step 5.7+) and `tier2/story-elaboration.md`.
> **Persona:** Product Manager / Product Ownership Lead (primary; no sub-role override).

---

## Purpose

Identify which epics and stories in the Product Backlog Package (PBP) are automated features/processes, classify each into its sub-mode and pattern, apply the `automationFeature` tag, and author product-level automation acceptance criteria. This is the **origin point** where automated features enter the backlog as first-class tagged items; downstream packages (UXD, ADLC, DWG, GCE, TGE) key off these tags.

---

## Guardrail

This facet operates strictly within the Product Manager's lane:
- Identify **what** is automated and **why** (process efficiency, error reduction, scale).
- Define **what good looks like** (acceptance criteria from the user/process-owner's perspective).
- Author **intent-level** `requires`/`provides` (what data it needs, what it triggers) — high-level, not technical.
- DO NOT prescribe **how** it is orchestrated (no engine choice, no queue topology, no retry strategy, no actor-identity model). That is AI-ADLC's responsibility.

---

## When This Facet Fires

1. **During epic decomposition (Stage 5):** after epics are identified and before prioritization, scan each epic for automation signals.
2. **During story elaboration (Tier 2, if active):** when elaborating stories from an automation-tagged epic, carry the `automationFeatureId` forward and write story-level automation acceptance criteria.

---

## Step 1: Automation-Opportunity Scan

For each epic (or story, in Tier 2), scan for signals that the feature/process involves or could benefit from automation:

### Signal Indicators

| Signal category | Examples |
|-----------------|----------|
| **Explicit automation intent** | "automatically…", "scheduled…", "triggered when…", "no manual intervention", "straight-through processing" |
| **Repetitive process** | High-volume, rules-based, same steps every time, currently done manually by staff |
| **Time/event trigger** | "every night", "when a ticket is created", "on file arrival", "at end of billing period" |
| **Routing/assignment** | "assign to the right team", "route to the appropriate queue", "escalate if unresolved after X" |
| **Approval/workflow** | "requires manager approval", "multi-step review chain", "escalation path" |
| **Integration glue** | "sync data between systems", "push to CRM when…", "notify Slack channel" |
| **Self-healing/remediation** | "retry failed jobs", "auto-recover", "compensate on failure" |

### Scan Behavior

- Read the epic/story description, acceptance criteria, and any context notes.
- Match against the signal indicators above.
- For each match, note which automation pattern from the taxonomy (below) it maps to.
- If zero signals detected: skip this epic/story (it is not an automated feature). Move to the next.
- If signals detected: proceed to Step 2.

---

## Step 2: Propose Classification

For each detected automation opportunity, propose:

1. **That it IS an automated feature** (explain the signal in one sentence).
2. **Which sub-mode** from the active palette applies to THIS feature:
   - `assisted` — automation helps but the human still performs and controls the task
   - `attended` — automation performs it but needs a human trigger, approval, or supervision
   - `unattended` — automation runs end-to-end with no human in the loop

3. **Which primary pattern** from the Automation-Pattern Taxonomy:

| # | Pattern | Use when… |
|---|---------|-----------|
| 1 | `workflow-orchestration` | The feature coordinates a multi-step process across systems or actors |
| 2 | `task-automation` | The feature automates a discrete, repetitive task (RPA-style single unit) |
| 3 | `data-pipeline` | The feature moves and transforms data (ETL/ELT/stream) |
| 4 | `integration` | The feature connects systems and exchanges data/calls (API glue) |
| 5 | `rules-decision` | The feature decides via a deterministic rules/policy engine |
| 6 | `routing-assignment` | The feature routes, assigns, or dispatches work items |
| 7 | `approval-workflow` | The feature manages multi-step approval, review, or escalation |
| 8 | `notification` | The feature sends automated alerts, reminders, or messages |
| 9 | `document-generation` | The feature assembles documents, reports, or correspondence |
| 10 | `intake-processing` | The feature captures and processes inbound items (forms, email, tickets) |
| 11 | `reconciliation-matching` | The feature matches/reconciles records across sources |
| 12 | `remediation` | The feature takes corrective action in response to a detected condition |
| 13 | `state-transition` | The feature progresses an entity's lifecycle/status automatically |

4. **Which trigger** fires this automation:
   - `scheduled` — fires on a clock/cron (nightly, hourly, end-of-period)
   - `event` — fires in response to an external event (ticket created, file arrived, threshold breached)
   - `manual` — fires when a human explicitly starts it (attended mode)
   - `continuous` — long-running, always active (watching, streaming)

### Presentation Format

```
Automation Feature Detected:
  Epic/Story: {epic-id} — {title}
  Signal: "{quoted text or paraphrase from the requirement}"
  Proposed sub-mode: {assisted | attended | unattended}
  Proposed pattern: {taxonomy value}
  Proposed trigger: {scheduled | event | manual | continuous}
  Rationale: {one sentence explaining why this classification}

Confirm? (yes / change sub-mode / change pattern / change trigger / not automation)
```

Wait for user confirmation before proceeding.

---

## Step 3: Apply the `automationFeature` Tag

On user confirmation, apply the tag to the epic/story front-matter:

```yaml
---
automationFeature: true
automationMode: {confirmed sub-mode}
automationPattern: {confirmed pattern}
automationTrigger: {confirmed trigger}
automationFeatureId: AUTO-{NNN}
---
```

### Minting `automationFeatureId`

- Scan all existing `AUTO-*` tags across the project's backlog artifacts.
- Take the highest `{NNN}` found.
- Assign `{NNN} + 1` (or `001` if none exist).
- One `automationFeatureId` per feature; if the same automation spans multiple stories, they share the ID (the epic holds the canonical tag; stories inherit via `derivedFrom`).

---

## Step 4: Write Automation Acceptance Criteria

For each confirmed automation feature, write **product-level** acceptance criteria that define "what good looks like" from the process-owner's perspective.

### Required Automation Acceptance Criteria Categories

| Category | What it defines | Example |
|----------|-----------------|---------|
| **Throughput / SLA** | How fast and how much it must handle | "Assigns incoming tickets within 5 seconds of creation; handles 200 tickets/hour at peak" |
| **Exception handling** | What happens on the unhappy path | "If no routing rule matches, place in the unmatched queue and notify the team lead within 1 minute" |
| **Human fallback / override** | How a human can intervene or take over | "Any auto-assignment can be manually reassigned by a team lead at any time; reassignment logged" |
| **Straight-through rate** | Target for fully automated success | "≥ 90% of standard tickets are auto-assigned without human intervention" |
| **Reversibility** | Can the automated action be undone | "Every auto-assignment is reversible; reassignment takes effect immediately with full audit trail" |
| **Audit / transparency** | What evidence is recorded | "Every assignment decision is logged with timestamp, rule matched, and ticket context" |

### Writing Rules

- Write from the **process-owner's perspective** (what they need the automation to achieve), not the system's (how it's orchestrated).
- Use measurable thresholds where possible (seconds, percentages, counts, rates).
- Every criterion must be **testable** — AI-TGE will later derive verification harnesses from these.
- Do NOT mention orchestration engines, queue technologies, retry configurations, or actor identities (that's ADLC's job).
- Place criteria in the epic/story body under a `## Automation Acceptance Criteria` heading (or as an `automationAcceptanceCriteria` array in front-matter for machine extraction).

### Format

```markdown
## Automation Acceptance Criteria

- **Throughput/SLA:** {performance bound}
- **Exception handling:** {unhappy-path behavior}
- **Human fallback:** {override/intervention mechanism}
- **Straight-through rate:** {automation success target}
- **Reversibility:** {undo capability}
- **Audit:** {evidence/transparency requirement}
```

Not every category applies to every feature. Include only those relevant; minimum 3 categories per automation feature.

---

## Step 5: Author Intent-Level `requires` / `provides`

For each confirmed automation feature, author a **high-level** declaration of what the automation needs and what it produces. This is the intent that AI-ADLC will later formalize into the technical trigger-effect graph.

```yaml
requires:
  data:   [ticket, agent]              # entities/streams it reads
  events: [ticket.created]             # what triggers it
provides:
  writes: [ticket.assignee]            # entities/fields it mutates
  emits:  [ticket.assigned]            # events it raises
```

### Writing Rules

- Use **domain language** (entity names, event names the user would recognize), not technical infrastructure names.
- Keep it intent-level: "needs ticket data" not "needs a Kafka consumer on topic X."
- `requires.auth` and `requires.roles` are ADLC/DWG concerns — leave them out here (they'll be added downstream).
- Place in the epic/story front-matter as part of the tag block.

---

## Step 6: Prioritization Impact

After tagging, note the prioritization impact of the sub-mode:

| Sub-mode | Priority signal |
|----------|-----------------|
| `assisted` | No priority change; treat as a productivity enhancement |
| `attended` | Moderate priority boost — formalizes an existing human process into a governed workflow |
| `unattended` | High priority boost — removes human dependency entirely; highest ROI but highest governance overhead |

Inform the user of the priority signal so they can factor it into the prioritization model (Stage 5 scoring). Do not auto-override scores.

---

## Step 7: Inform Downstream

After all automation features in this batch are tagged:

1. **Summary line:** "Automation Lens: {N} features tagged across {M} epics — {list of automationFeatureIds}."
2. **Downstream signal:** these tags will be consumed by:
   - AI-UXD (config, monitoring, approval, override UX per tagged feature)
   - AI-ADLC (orchestration, idempotency, retry/compensation, audit architecture per tagged feature)
   - AI-DWG (provisioning + courier)
   - AI-GCE `ATG__` (automation governance)
   - AI-TGE `ATQ__` (automation verification)
3. **DFE derivation:** `automationFeatureId` + `automationMode` + `automationPattern` + `automationTrigger` + `automationAcceptanceCriteria` are exposed via POLC's `data-schema/` for the cross-lifecycle traceability JSON.

---

## Tier 2 Behavior (Story Elaboration)

When Tier 2 is active and the user elaborates stories from an automation-tagged epic:

- Each story inherits the epic's `automationFeatureId` (via `derivedFrom`).
- Each story MAY carry `automationFeature: true` in its own front-matter if it is a distinct automation unit; otherwise, the epic-level tag is sufficient.
- Write story-level automation acceptance criteria where they differ from the epic level (e.g., a specific story handles the exception queue; another handles the approval step).
- Stories that are NOT automated within an automation-tagged epic do NOT get the tag (e.g., a reporting story in a routing-assignment epic).

---

## Co-Tagging with AI-LENS

A feature may carry BOTH `aiFeature` and `automationFeature` tags (they are orthogonal axes). Example: an AI-powered auto-routing feature is both `aiFeature` (uses a model for classification) and `automationFeature` (runs unattended, assigns without human action). Each lens independently tags, classifies, and writes its own acceptance criteria. Their interaction (an AI effect feeding an automation trigger) is detected at the Design Coherence Gate (ADLC, §8 of the coherence protocol).

---

## What This Facet Does NOT Do

- Does not prescribe orchestration engine, queue topology, retry strategy, or actor identity (AI-ADLC).
- Does not design configuration UX, monitoring dashboards, or approval interfaces (AI-UXD).
- Does not provision infrastructure or courier context (AI-DWG).
- Does not enforce audit, SoD, or kill-switch compliance (AI-GCE `ATG__`).
- Does not verify idempotency, exception paths, or loop termination (AI-TGE `ATQ__`).
- Does not modify AI-DFE (shared fabric; used as-is).

---

*Automation-LENS POLC Facet v1.0.0 | Integration: Stage 5 (epic-decomposition) + Tier 2 (story-elaboration) | Author: Maheri*
