# AGENTIC Facet — AI-UXD

> **Loaded by the lens seam as an INTERSECTION FACET** when `Lens_Status.md` shows **AI-LENS row = `AI-Powered`** AND **Automation row = `Automated`** — for each feature carrying `agenticProfile: true`.
> **Runs after** the AI-LENS facet (`ai-lens/facet.md`) and the Automation-LENS facet (`automation-lens/facet.md`) have designed their own UX. Agentic is a **thin delta** — it reuses their patterns and adds only what an autonomous agent needs.
> **Integration points:** `define/` (interaction requirements) + `design/` (patterns + design system) + `validate/` (a11y + trust).
> **Persona:** UX Designer / Design System Lead (primary; sub-role `#persona-subrole-ux-designer` for flows, `#persona-subrole-audit-specialist` for validate).

---

## Purpose

Design how a user **perceives, trusts, steers, and stops** an autonomous agent — a feature that both reasons (AI Lens) and acts across multiple steps on its own (Automation Lens).

Most of the agent's UX already exists in the two lens facets: the AI facet designed disclosure, HITL, confidence, and fallback; the automation facet designed configuration, monitoring, approval, and override/stop. An agent needs only a **delta** on top: making a *multi-step, self-directed* process legible and interruptible. This facet designs that delta and nothing the two lenses already cover.

---

## Guardrail

This facet operates strictly within the UX Designer's lane, and strictly as a **delta over the two lenses**:
- Design **only** agent-specific interaction: reasoning/tool-use transparency, agent working-states, mid-task interruptibility, and a single combined disclosure.
- **DO NOT re-document** the AI HITL/disclosure/confidence/fallback UX or the automation monitoring/approval/override UX — reference them.
- DO NOT design the agent's architecture (AI-ADLC owns tool-use, reasoning loop, memory).
- DO NOT write acceptance criteria (AI-POLC authored the agentic acceptance criteria — read them).
- DO NOT create a new mode or badge system — the agentic treatment composes the two existing ones.

---

## When This Facet Fires

For each `agenticProfile: true` feature, during define/design/validate, **after** the two UXD lens facets have run:

1. **Define:** capture the transparency + interruptibility requirements from the agentic acceptance criteria (autonomy scope, escalation path).
2. **Design:** design the four delta patterns (§Step 2) + add agent components to the design system.
3. **Validate:** verify the agent's states and controls are accessible and the trust model holds.

---

## The UX Reuse Map (inherit — do not re-document)

| Agent UX need | Reused from (already designed — reference) | New delta (this facet owns) |
|---------------|--------------------------------------------|-----------------------------|
| "This is AI" disclosure | `ai-lens/facet.md` (disclosure types, badge) | Folded into the **combined badge** (§2.4) |
| Approve/edit/monitor an AI output | `ai-lens/facet.md` (HITL levels) | Extended to **mid-task** approval within the loop |
| Confidence + fallback display | `ai-lens/facet.md` (confidence, fallback states) | Fallback extended to **escalation** display (§2.1) |
| Watch what automation did/does | `automation-lens/facet.md` (monitoring models, run-history) | Agent **working-state** + **reasoning/activity** view (§2.1–2.2) |
| Approve automated actions | `automation-lens/facet.md` (approval models) | Per-step / consequential-action approval in-loop (§2.2) |
| Stop / pause / override | `automation-lens/facet.md` (override controls, kill-switch) | **Interruptibility mid-loop** + resume/restart semantics (§2.3) |
| "Done automatically" labeling | `automation-lens/facet.md` (automation disclosure) | Folded into the **combined badge** (§2.4) |

---

## Step 1: Consume Upstream

For each agentic feature (threaded by its existing `aiFeatureId` + `automationFeatureId`; no `agenticFeatureId`), read:
- The AI-LENS UXP fields (`aiHitlLevel`, `aiDisclosureType`, confidence/fallback) and the Automation UXP fields (`automationMonitoringModel`, `automationApprovalModel`, `automationOverrideControl`).
- The **agentic acceptance criteria** from AI-POLC: **autonomy scope** (what the agent may do end-to-end vs. what needs a human) and the **escalation path** (what happens when it can't complete). These drive where approval gates and escalation surfaces appear.

---

## Step 2: Design the Agentic Delta

### 2.1 Reasoning & Tool-Use Transparency

The user must be able to see **what the agent is doing and why** — the human-facing surface of the reasoning trace that `ai-adlc/.../agentic-lens/architecture/reasoning-loop.md` captures.

| Element | Requirement |
|---------|-------------|
| **Activity narration** | Show the current step in human terms ("Looking up the order…", "Drafting the reply…") — not raw chain-of-thought |
| **Action visibility** | Surface which tools/actions the agent is taking, especially consequential ones ("Issued a refund of {amount}") |
| **"Why" on demand** | One affordance to see the reasoning/rationale behind an action (reuses the AI explainability/disclosure pattern) |
| **Escalation surface** | When the agent escalates (from the POLC escalation path), show it clearly and route to the human/fallback — this extends the AI fallback UX |

**Rule:** show progress and decisions at a **human** level of abstraction. Dumping raw model reasoning is neither trustworthy nor accessible.

### 2.2 Agent Working States

An agent is a process with a lifecycle the UI must reflect. Define the state model and its visual treatment:

| State | Meaning | UX |
|-------|---------|----|
| `planning` | Agent is deciding what to do | Working indicator + "planning" narration |
| `acting` | Agent is executing a step/tool | Activity narration + action visibility |
| `waiting-approval` | Agent paused for a human decision (attended) | Approval surface (reuses automation approval model) |
| `escalated` | Agent handed off (couldn't complete / hit a budget) | Escalation surface + hand-off destination |
| `done` | Task complete | Result + summary of what was done |
| `stopped` | Interrupted by a human | Clear stopped state + what was/wasn't completed |

The state must be perceivable at a glance and announced on change (§Step 4).

### 2.3 Interruptibility

An autonomous multi-step agent must be **steerable and stoppable mid-task** — this extends the automation override/kill-switch UX to the running loop.

| Control | Requirement |
|---------|-------------|
| **Pause** | Halt the agent between steps without losing task state (reuses automation `pause-button`); resume continues from where it stopped |
| **Stop / interrupt** | Stop the current task now (reuses automation `kill-switch`); show what completed and what was rolled back or left partial (from the architecture's exhaustion/compensation behavior) |
| **Take over** | Hand control from the agent to the human mid-task (attended) — the human finishes the step the agent was on |

**Rules:**
- The stop/interrupt control must be **findable during a run**, not buried in settings — the automation "reachable in an emergency" rule applies.
- Show the **consequence of stopping** truthfully (in-flight work completes / rolls back / left partial) — mirror what the architecture actually does.
- For `unattended` agents, interrupt + kill-switch are mandatory surfaces.

### 2.4 Combined Disclosure (one badge, not three)

The feature carries AI disclosure ("AI-generated") **and** automation disclosure ("done automatically"). Do not stack competing badges. Design **one coherent treatment** that communicates: this was done by an autonomous agent (AI + acting on its own). One badge, with a path to "why" that reveals both the AI and automation nature on demand.

---

## Step 3: Coherence With the Two Lenses

An agent's HITL/approval design can contradict itself across lenses. Extend the automation facet's co-design check:

- **Flag AI-HITL vs. automation-approval contradictions.** Example: AI `review-before-action` (a human must approve each AI output) combined with automation `unattended` (no human in the loop) is a **contradiction** for an agent — it cannot be both fully supervised and fully autonomous. Surface it to the user; it signals a design conflict the ADLC Design Coherence Gate will also catch.
- The agent's autonomy UX must match its **autonomy scope** from POLC — the UI must not let the agent act beyond what the acceptance criteria permit unsupervised.

---

## Step 4: Validate — Accessibility & Trust

**Accessibility:**
- **Working-state changes must be announced** — use ARIA live regions so screen-reader users know the agent moved from `acting` to `waiting-approval` or `escalated`.
- **Interrupt / stop controls must be keyboard-reachable** — an emergency control cannot be mouse-only.
- **Activity narration must be perceivable** — not conveyed by animation/color alone.
- **The combined badge needs a text alternative** — an icon alone is insufficient.

**Trust (agent-specific, on top of the two lenses' trust checks):**
1. Can the user tell **what the agent is doing right now**? (working state)
2. Can the user tell **why** it took an action? (reasoning transparency)
3. Can the user **interrupt** it mid-task? (interruptibility)
4. Does the user know **when it gave up / handed off**? (escalation surface)
5. On stop, does the user know **what was and wasn't done**? (truthful consequence)

If any answer is "no" for an `unattended` agent, the UX is incomplete.

---

## Step 5: Design-System Additions

Add only the agent-specific components the project needs (reuse the AI + automation components already specified):

| Component | Purpose |
|-----------|---------|
| **Agent working-state indicator** | Reflects `planning / acting / waiting-approval / escalated / done / stopped` |
| **Reasoning / activity view** | Human-level narration of steps + action visibility + "why" on demand |
| **Interrupt / take-over control** | Pause / stop / take-over during a run, with consequence disclosure |
| **Combined agent badge** | The single AI+automation disclosure treatment (§2.4) |

Document each with states, variants, and accessibility requirements.

---

## Record & Inform Downstream

Record per agentic feature in the UXP (derived; no new id):

```yaml
---
agenticProfile: true                 # derived; dissolves if either lens tag drops below threshold
aiFeatureId: AIF-{NNN}
automationFeatureId: AUTO-{NNN}
agentTransparencyLevel: {narration | narration + action-visibility + why}
agentWorkingStates: [planning, acting, waiting-approval, escalated, done, stopped]
agentInterruptModel: {pause+resume | stop | take-over}
combinedDisclosure: true
---
```

Inform: "Agentic facet: agent-interaction UX designed for {N} features — {list of ids}." Flag any AI-HITL/automation-approval contradiction found (§Step 3).

**Downstream:** AI-ADLC's agentic facet ensures the architecture supports these surfaces (interruptibility needs a kill-switch/pause hook in the loop runner; working-states need the reasoning trace). A contradiction flagged here should be resolved before the Design Coherence Gate.

---

## What This Facet Does NOT Do

- Does not re-document the AI or automation UX (references them via the Reuse Map).
- Does not identify or tag agentic features (AI-POLC).
- Does not design the agent's architecture — tool-use, reasoning loop, memory (AI-ADLC).
- Does not write acceptance criteria (reads the agentic acceptance criteria from POLC).
- Does not generate workspace scaffolding (AI-DWG).
- Does not create a new mode, id, or badge system — the agentic UX composes the two existing lenses.

---

*AGENTIC Facet — AI-UXD v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) — NOT a third lens | Integration: define + design + validate | Thin delta over the AI + Automation UXD facets | Author: Maheri*
