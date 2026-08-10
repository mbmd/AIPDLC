# Automation-LENS Facet — AI-DWG

> **Loaded by the lens seam** when `Lens_Status.md` Automation row = `Automated`.
> **Integration points:** `mapping/` (new transforms) + `templates/` (config/compose/steering).
> **Persona:** DevOps / Platform Engineer + Senior Architect (primary).

---

## Purpose

Provision automation runtime scaffolding into the generated development workspace (Layer 3) **and act as the courier** — carry all automation-feature context across the DWG hinge so that AI-GCE (`ATG__`) and AI-TGE (`ATQ__`) have full context without reaching back to the design workspace. DWG is the **Layer-2 → Layer-3 hinge**.

---

## Dual Role

| Role | What it does |
|------|-------------|
| **Provisioner** | Generates automation-specific files (engine config, scheduler, queue/event-bus, connector stubs, retry/idempotency skeletons, audit sink) |
| **Courier** | Carries the automation-feature context (tags + AC + architecture + guards + control class) into the generated workspace |

Both roles activate together.

---

## Guardrail

This facet operates within the DevOps/Platform Engineer's lane:
- Provision **infrastructure and scaffolding** for automated features.
- Courier **context + guards** for downstream agents.
- **Scope boundary:** this provisions the **product's automation runtime** (the workflow engine, queues, schedulers the *product* uses to run its automated features) — NOT the delivery pipeline (CI/CD, IaC), which is out of the Automation Lens's scope (D2) and owned by standard DWG DevOps output.
- DO NOT make architecture decisions (AI-ADLC already did; DWG reads them).
- DO NOT design control UX (AI-UXD already did).
- DO NOT enforce governance (AI-GCE `ATG__` consumes the couriered context).

---

## When This Facet Fires

During workspace generation, when `automationFeature`-tagged items exist in the AP/PBP/UXP inputs:
1. **Scan inputs** for `automationFeature: true` artifacts.
2. **Generate automation scaffolding** based on the ADLC architecture decisions.
3. **Confirm provisioning readiness** (the coherence readiness check at the provisioning altitude).
4. **Courier automation context + guards** into a manifest inside the generated workspace.

---

## Step 1: Scan for Automation Features

Read the 3 peer inputs (AP, PBP, UXP — subset-tolerant) and collect per feature:
- All `automationFeatureId` values
- `automationMode`, `automationPattern`, `automationTrigger`, `automationAcceptanceCriteria[]` (from POLC)
- Architecture decisions — engine, idempotency, retry/compensation, actor identity, audit, loop guards (from ADLC ADRs)
- `automationControlClass` (from PILC/PIP)
- Control UX — config/monitoring/approval/override models (from UXD)
- Formalized `requires` / `provides` (from ADLC)

If zero automation features found: skip this facet entirely.

---

## Step 2: Generate Automation Scaffolding

Based on the ADLC architecture decisions, generate:

### 2.1 Dependencies

| Architecture decision (`automationEngineStrategy`) | Generated dependencies |
|---------------------------------------------------|------------------------|
| `workflow-engine` | Workflow-engine SDK/client (Temporal, Camunda, Step Functions client) + config |
| `scheduler` | Scheduler library or platform cron config |
| `event-consumer` | Message-broker client (Kafka/SQS/PubSub/RabbitMQ) + consumer config |
| `queue-worker` | Job-queue library (BullMQ, Celery, Sidekiq) + config |
| Vector/state store (if used) | Client library + connection config |

Generate into `package.json` / `requirements.txt` / `pom.xml` (technology-adaptive per existing DWG logic).

### 2.2 Environment Configuration

Generate `.env.example` entries for automation infrastructure:
```env
# Automation Runtime (AUTO-{NNN}: {feature name})
AUTOMATION_ENGINE={engine}
QUEUE_URL={queue-url-placeholder}
EVENT_BUS_ENDPOINT={endpoint-placeholder}
AUTOMATION_SERVICE_ACCOUNT={identity-placeholder}
AUTOMATION_MAX_RETRIES={budget}
AUTOMATION_HOP_BUDGET={maxHops}
AUTOMATION_KILL_SWITCH=off
AUDIT_SINK_URL={audit-sink-placeholder}
```

### 2.3 Scaffolding Files

| File/Folder | Purpose | Generated when |
|-------------|---------|---------------|
| `automation/` | Automation handlers directory (one per feature) | Any automation feature |
| `automation/{feature}/handler.{ext}` | Handler skeleton with idempotency guard + audit hook wired in | Per feature |
| `automation/config.{ext}` | Central automation config (engine, retry budget, hop budget, kill-switch) | Always |
| `docker-compose.automation.yml` | Local automation infra (broker, queue, scheduler) | Self-hosted engine/broker in architecture |
| `automation/dead-letter/` | Dead-letter handling skeleton | Any feature with `dead-letter-reprocess` or retry |
| `automation/compensations/` | Compensation action skeletons | Any `saga-*` retry/compensation strategy |
| `audit/` | Audit sink skeleton (schema + writer) | Always (every automation audits) |

### 2.4 Guard Scaffolding (from loop-guards architecture)

Generate the loop-guard machinery the ADLC designed:

| Guard | Generated |
|-------|-----------|
| `causedBy` stamp | Event-envelope helper that stamps `causedBy` + `causalHops` on emit; trigger filter that drops self-caused events |
| Hop budget | Config value `AUTOMATION_HOP_BUDGET` + the check-and-increment helper |
| Circuit breaker | Circuit-breaker wrapper skeleton with the ADLC-specified thresholds |
| Kill switch | The config-flag check the running automation consults before each execution |

### 2.5 Automation Steering (for GCE to govern)

Generate steering file:
```markdown
---
generatedBy: AI-DWG
source: Automation-LENS architecture decisions (ADLC ADRs)
ownership: generated
---

# Automation Feature Governance — Steering

## Active Automation Features
{list automationFeatureId + pattern + sub-mode + control class}

## Architectural Commitments
{per-feature: engine, idempotency, retry/compensation, actor identity, audit, loop guards}

## Governance Obligations
{per-feature by control class: audit trail, SoD, kill-switch, fail-safe, reversibility}
```

---

## Step 3: Provisioning Readiness Check (Coherence)

This is DWG's slice of the coherence layer (`LENS_COHERENCE_PROTOCOL.md` readiness family, provisioning altitude). For each feature, confirm:

- Every `requires.auth` has a provisioning slot (an `.env` entry / vault reference / IAM binding).
- Every declared connector/external system in the architecture has a config stub.
- Every `requires.roles` actor identity has a config placeholder (never the actual credential).
- The audit sink is provisioned.
- Every loop guard has its config value.

**If a `requires` cannot be satisfied** (e.g. an auth with no provisioning path): flag it. This is a readiness gap the ADLC Coherence Gate should have caught — surface it rather than generating a broken workspace.

---

## Step 4: Courier Automation Context (Cross-Hinge)

Generate the **automation feature manifest** inside the workspace:

### File: `{slug}-workspace/.automation-lens/manifest.json`

```json
{
  "automationLensVersion": "1.0.0",
  "generatedOn": "{ISO-date}",
  "generatedBy": "AI-DWG",
  "projectId": "{project-id}",
  "automationMode": "automated",
  "automationSubModes": ["{sub-modes}"],
  "features": [
    {
      "automationFeatureId": "AUTO-001",
      "automationMode": "{sub-mode}",
      "automationPattern": "{value}",
      "automationTrigger": "{value}",
      "automationControlClass": "{value}",
      "acceptanceCriteria": ["{AC from POLC}"],
      "architecture": {
        "engineStrategy": "{from ADLC}",
        "idempotencyStrategy": "{from ADLC}",
        "retryCompensationStrategy": "{from ADLC}",
        "actorIdentity": "{from ADLC}",
        "auditStrategy": "{from ADLC}",
        "loopGuardStrategy": "{from ADLC}"
      },
      "guards": {
        "causedBy": true,
        "hopBudget": {maxHops},
        "circuitBreaker": { "threshold": "{value}", "reset": "{policy}" },
        "killSwitch": { "mechanism": "{value}", "inFlightPolicy": "{value}" }
      },
      "requires": { "...": "formalized from ADLC" },
      "provides": { "...": "formalized from ADLC" },
      "ux": {
        "configModel": "{from UXD}",
        "monitoringModel": "{from UXD}",
        "approvalModel": "{from UXD}",
        "overrideControl": "{from UXD}"
      }
    }
  ]
}
```

### Courier Principle

The manifest is the **single source of truth** for dev-side agents. `ATG__` and `ATQ__` read this manifest; they never reach back across the hinge. Everything they need — especially the **guards** they must verify — is here.

---

## Step 5: Seed the Dev-Side Agents

Place the `ATG__` (governance) and `ATQ__` (quality) agent files into the generated workspace's governance/test engine slots, so the Layer-3 GCE/TGE engines can dispatch them via their existing Command Dispatch. (This is how the lens agents reach Layer 3 — DWG seeds them; the engines dispatch them. No separate engine capability required.)

- `ATG__` agent → `{slug}-workspace/.governance/engine/agents/atg-agent.md`
- `ATQ__` agent → `{slug}-workspace/.tge/engine/agents/atq-agent.md`
- Register both in the workspace's agent registry.

---

## Step 6: Mirror to `data-schema/`

Mirror automation-feature fields into the generated workspace's `data-schema/` for DFE's `DAT__`:
- `automationFeatureIds[]`
- `automationScaffoldingGenerated: true`
- `automationContextCouriered: true`

---

## Sub-Mode Calibration

| Sub-mode | Scaffolding depth |
|----------|-------------------|
| `assisted` | Minimal: handler skeleton + audit hook. No engine/queue infra, no guards (no unattended execution). |
| `attended` | Medium: handler + approval-queue integration point + audit + exception handling. Kill-switch config. |
| `unattended` | Full: all applicable scaffolding + complete guard machinery (causedBy, hop budget, circuit breaker, kill switch) + dead-letter + compensations + full audit. |

---

## Co-Provisioning with AI-LENS

For a feature carrying both tags, generate both scaffolding sets coherently:
- One workspace, two manifests (`.ai-lens/manifest.json` + `.automation-lens/manifest.json`).
- Shared infrastructure is not duplicated (e.g. one audit sink serves both).
- Both agent sets seeded (`AIG__`/`AIQ__` + `ATG__`/`ATQ__`).

---

## What This Facet Does NOT Do

- Does not make architecture decisions (reads them from ADLC ADRs).
- Does not identify or tag automation features (reads from POLC).
- Does not provision the delivery pipeline / CI/CD (out of scope — D2).
- Does not enforce governance (generates steering + seeds `ATG__`; GCE enforces).
- Does not run verification (seeds `ATQ__`; TGE runs it).
- Does not modify AI-DFE (mirrors fields into `data-schema/` for existing `DAT__`).

---

*Automation-LENS DWG Facet v1.0.0 | Integration: Workspace generation (mapping + templates) + courier + agent-seeding | Author: Maheri*
