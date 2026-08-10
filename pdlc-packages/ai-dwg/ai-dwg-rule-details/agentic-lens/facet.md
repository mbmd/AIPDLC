# AGENTIC Facet — AI-DWG

> **Loaded by the lens seam as an INTERSECTION FACET** when `Lens_Status.md` shows **AI-LENS row = `AI-Powered`** AND **Automation row = `Automated`** — for each feature carrying `agenticProfile: true`.
> **Runs alongside** the AI-LENS facet (`ai-lens/facet.md`) and the Automation-LENS facet (`automation-lens/facet.md`). Agentic is **additive** — those two facets already provisioned the model client, the automation runtime, the audit sink, the actor identity, and the loop guards. This facet provisions only the agent-framework layer on top and couriers the agentic guardrails.
> **Integration points:** `mapping/` (new transforms) + `templates/` (agent-framework scaffolding).
> **Persona:** DevOps / Platform Engineer + Senior Architect (primary).

---

## Purpose

Provision the **agent-framework runtime** into the generated workspace (Layer 3) **and courier the agentic guardrails** so the existing dev-side agents can apply their agentic check-sets without reaching back across the hinge. An agent's model serving, RAG, automation runtime, audit sink, identity, and loop guards are already provisioned by the two lens facets; this facet adds the **tool registry, memory store, and loop runner** that turn those parts into a governed agent.

---

## Dual Role

| Role | What it does |
|------|-------------|
| **Provisioner** | Generates the agent-framework scaffolding (tool registry, memory store, loop runner with termination + cost ceiling, reasoning-trace writer) |
| **Courier** | Augments the two existing lens manifests with an `agentic` block per agentic feature — carrying the tool-permission manifest, loop termination, cost ceiling, reasoning-trace requirement, and kill-switch hook |

Both roles activate together, and both build on what the two lens facets already produced.

---

## Guardrail

This facet operates within the DevOps/Platform Engineer's lane, and strictly as a **delta over the two lens facets**:
- Provision **only** the agent-framework layer (tool registry, memory store, loop runner). Reuse the model client (AI facet), the audit sink + actor identity + kill-switch (Automation facet) — do not regenerate them.
- Courier the agentic block **into the two existing manifests** — do NOT create a new lens manifest or a central agentic register (the agentic profile is a derived shadow of the two lens tags).
- **Seed no new agent.** The existing `AIG__`/`AIQ__` (AI) and `ATG__`/`ATQ__` (Automation) — already seeded by the two lens facets — gain agentic check-sets. This facet ensures they receive the agentic context; it does not add a fifth agent or a new trigger.
- DO NOT make architecture decisions (AI-ADLC's agentic facet already did; DWG reads them).
- DO NOT design the agent's control UX (AI-UXD already did).

---

## When This Facet Fires

During workspace generation, when features carrying `agenticProfile: true` exist in the inputs (both lens tags present at threshold):
1. **Scan** for agentic features and read their agent architecture (from the ADLC agentic ADRs).
2. **Provision** the agent-framework scaffolding.
3. **Confirm provisioning readiness** (the action-coverage check at the provisioning altitude).
4. **Courier** the agentic block into both lens manifests.

If zero agentic features: skip this facet entirely.

---

## Step 1: Scan for Agentic Features

For each feature with `agenticProfile: true` (threaded by its existing `aiFeatureId` + `automationFeatureId` — no `agenticFeatureId`), read the agent architecture from the ADLC agentic ADRs:
- Tool registry (tools, effect classes, per-tool permission binding)
- Reasoning-loop pattern + termination contract (max steps, wall-clock, cost ceiling)
- Memory architecture (tiers, retention, PII handling)
- Reasoning-trace requirement (bound to the automation audit sink)

---

## Step 2: Provision the Agent Framework

Build on the two lens facets' output; generate only the agent-specific layer.

### 2.1 Dependencies
Agent/loop-runner library (or a thin in-house runner) + the model client's tool-calling interface (reuse the client the AI facet already generated). Add to the technology-adaptive dependency manifest.

### 2.2 Environment Configuration
Add agent-framework config to `.env.example` (reusing the automation kill-switch + identity slots the Automation facet generated):
```env
# Agent Framework (agentic feature: AIF-{NNN} / AUTO-{NNN})
AGENT_MAX_STEPS={maxSteps}
AGENT_WALLCLOCK_MS={wallClock}
AGENT_COST_CEILING={costCeiling}
AGENT_TOOL_REGISTRY=agent/tool-registry.{ext}
AGENT_MEMORY_STORE={store-placeholder}
AGENT_REASONING_TRACE_SINK={audit-sink-reuse}
```

### 2.3 Scaffolding Files

| File/Folder | Purpose | Generated when |
|-------------|---------|---------------|
| `agent/` | Agent-framework directory (one runner per agentic feature) | Any agentic feature |
| `agent/tool-registry.{ext}` | The closed tool set — names, effect classes, schemas, per-tool permission binding to the actor identity | Always |
| `agent/loop-runner.{ext}` | The reasoning loop with the **termination contract baked in** (step cap, wall-clock, cost ceiling) + exhaustion/escalation path | Always |
| `agent/memory/` | Memory store skeleton (scratchpad + any long-term tier), with retention + redaction hook at the write boundary | Memory tier in architecture |
| `agent/reasoning-trace.{ext}` | Reasoning-trace writer that records each step's decision/tool/result **into the existing audit sink** (not a new store) | Always |

### 2.4 Guard Scaffolding (agentic delta)

| Guard | Generated |
|-------|-----------|
| Step cap + cost ceiling | Baked into `loop-runner` (hard stops → escalation), from the ADLC termination contract |
| Tool-permission binding | Each tool wired to the actor-identity permission (reuse the Automation facet's identity config) — no tool exceeds its backing capability |
| Reasoning-trace capture | Every step writes to the audit sink (reuse the Automation facet's sink) |
| Kill-switch hook | The loop runner consults the Automation facet's kill-switch flag before each step (reuse — not a new switch) |

---

## Step 3: Provisioning Readiness Check (action coverage)

DWG's slice of the coherence readiness family at the provisioning altitude. For each agentic feature, confirm:
- Every tool in the registry maps to a provisioned capability — a declared `provides.writes` slot or a `requires.auth` config stub (no ghost capability that has no provisioning path).
- Every tool's permission maps to the actor identity the Automation facet provisioned.
- The loop runner's termination config values are all present.
- The reasoning-trace sink resolves to the provisioned audit sink.

**If a tool cannot be mapped to a provisioned capability/permission:** flag it — a readiness gap the ADLC action-surface sub-check should have caught. Surface it rather than generating an under-provisioned agent.

---

## Step 4: Courier the Agentic Context (augment both manifests)

The agentic profile is a derived shadow, so it rides the **two existing manifests** — no new manifest. For each agentic feature, add an `agentic` block to its entry in **both** `{slug}-workspace/.ai-lens/manifest.json` and `{slug}-workspace/.automation-lens/manifest.json`:

```json
"agentic": {
  "agenticProfile": true,
  "aiFeatureId": "AIF-{NNN}",
  "automationFeatureId": "AUTO-{NNN}",
  "toolRegistry": [
    { "name": "{tool}", "effectClass": "read|write|external-call", "permission": "{identity-permission}" }
  ],
  "loopTermination": { "maxSteps": {n}, "wallClockMs": {t}, "costCeiling": {c} },
  "reasoningTrace": { "required": true, "sink": "{audit-sink}" },
  "killSwitch": { "reuses": "automation", "reachableWithoutDeploy": true },
  "memory": { "tiers": ["scratchpad"], "retention": "{policy}" }
}
```

### Courier Principle
The block is derived from the two lens tags and dissolves if either drops. `AIG__`/`AIQ__` read it from `.ai-lens/manifest.json`; `ATG__`/`ATQ__` read it from `.automation-lens/manifest.json`. It is the single source the dev-side agents use for their agentic check-sets — they never reach back across the hinge.

---

## Step 5: No New Agent — Extend the Existing Four

The two lens facets already seeded `AIG__`/`AIQ__` (into `.governance/` + `.tge/`) and `ATG__`/`ATQ__`. This facet seeds **nothing new**: those four agents carry agentic check-sets that fire when a feature's manifest entry contains the `agentic` block. DWG's only job here is to guarantee the block is present so the checks can run. No fifth agent, no new trigger, no new registry entry.

---

## Step 6: Mirror to `data-schema/`

Mirror the derived marker into the generated workspace's `data-schema/` for DFE's existing `DAT__` (no DFE change):
- `agenticProfileFeatureIds[]` — the `AIF/AUTO` id pairs that are agentic
- `agentFrameworkProvisioned: true`
- `agenticContextCouriered: true`

---

## Autonomy Calibration

| `automationMode` | Agent-framework scaffolding depth |
|------------------|-----------------------------------|
| `attended` | Loop runner with termination + tool registry + reasoning trace. Human-checkpoint integration point (reuse the Automation approval-queue). Kill-switch reused. |
| `unattended` | Full: termination + cost ceiling + least-privilege tool binding + tool-set SoD enforced by permissions + reasoning trace + kill-switch reachable. |

---

## Co-Provisioning With the Two Lenses

For an agentic feature, all three facets generate into one workspace coherently:
- One workspace, two manifests — each gains the shared `agentic` block; no third manifest.
- Shared infrastructure is not duplicated (one model client, one audit sink, one identity, one kill-switch serve the agent).
- The four existing agents (`AIG__`/`AIQ__` + `ATG__`/`ATQ__`) serve the agent — none added.

---

## What This Facet Does NOT Do

- Does not regenerate the model client, automation runtime, audit sink, identity, or loop guards (the two lens facets did).
- Does not make architecture decisions (reads the ADLC agentic ADRs).
- Does not create a new manifest, agent, trigger, or register (agentic is a derived shadow).
- Does not design the agent's control UX (AI-UXD).
- Does not enforce governance or run tests (the four existing agents do, via their agentic check-sets).
- Does not modify AI-DFE (mirrors fields into `data-schema/` for existing `DAT__`).

---

*AGENTIC Facet — AI-DWG v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) — NOT a third lens | Integration: Workspace generation (agent-framework scaffolding) + courier (augments both lens manifests) + no new agent | Author: Maheri*
