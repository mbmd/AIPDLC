# AIFLC Automation Governance — Agent Template

> **Trigger:** `ATG__` (manual invocation)
> **Owner:** AI-GCE
> **Type:** Audit
> **Core impact:** None — the GCE core stays concern-agnostic. This agent is seeded into the Layer-3 workspace by AI-DWG and dispatched by GCE's existing Command Dispatch.

---

## Purpose

Perform automation-specific governance checks on the development workspace, using the couriered automation-feature context from `{slug}-workspace/.automation-lens/manifest.json`. Writes results into `.governance/`.

This is the **enforcement half** of the govern+verify bracket around the (un-lensed) builder. It observes that the automation's architectural guards, audit obligations, and control-class requirements are actually present and honored in the implementation — a Layer-3 implementation-compliance check, NOT the Layer-2 design-coherence check (coherence was settled at the ADLC Coherence Gate).

---

## When to Invoke

- After significant automation implementation milestones (handler, engine integration, guard wiring)
- Before PR/merge of automation-feature code
- Before any release containing automated features
- Periodically during active automation development (weekly recommended for `unattended` / `controlled`+ features)

---

## Consequences of Skipping

- Audit-trail gaps — automated actions unaccountable at release (compliance/forensic risk)
- Kill-switch or loop guards may be missing — runaway-automation risk in production
- Segregation of duties may be violated for `controlled`-class automation (regulatory risk)
- Least-privilege may not be honored — over-privileged automation identity (security risk)
- Reversibility promised in the AC may not be implemented

---

## Recovery

If `ATG__` has not been run and governance gaps exist:
1. Run `ATG__` immediately to assess current state
2. Address CRITICAL findings before next release (especially missing kill-switch / audit / SoD)
3. Log the governance gap as a `Decision_Log` entry with a remediation plan

---

## Input

Reads from `{slug}-workspace/.automation-lens/manifest.json` (couriered by AI-DWG):
- Feature list with `automationFeatureId`, `automationMode`, `automationPattern`, `automationControlClass`
- Architecture decisions (engine, idempotency, retry/compensation, actor identity, audit, loop guards)
- The **guards** block (causedBy, hop budget, circuit breaker, kill switch) — the primary thing to verify
- Acceptance criteria (reversibility, audit, straight-through expectations)
- The `agentic` block (when present) — tool registry + permissions, kill-switch reuse — needed for the agentic check-set (Category 5)

Also reads from the live workspace:
- `.governance/` existing rules and results
- Source code / config for evidence of guard + audit + identity implementation
- `automation/` handlers, `audit/` sink, `automation/config.*` for verification

---

## Checks Performed

### Category 1: Audit & Accountability

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **Audit trail present** | All automation features | Every state-mutating action produces an audit record (code evidence) |
| **Audit record completeness** | All | Records include the required fields — especially the `decision` rationale |
| **Audit immutability** | `operational`+ | The automation identity has no UPDATE/DELETE on audit records |
| **Retention configured** | `controlled`+ | Retention meets the control-class minimum; enforced technically (lifecycle rule) |

### Category 2: Control & Safety

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **Kill switch present** | `unattended`; mandatory `controlled`+ | The kill-switch config flag is checked by the running automation (not just a UI toggle) |
| **Kill-switch reachability** | `controlled`+ | Kill switch works without a deploy; meets the documented latency SLA |
| **Circuit breaker active** | External-dependency or high-volume automation | Rate-based breaker configured with the ADLC thresholds |
| **Fail-safe defaults** | `unattended` | On error/ambiguity, the automation defaults to the safe action (stop/park, not proceed) |
| **Reversibility implemented** | AC specifies reversibility | The undo path exists and is exposed |

### Category 3: Loop Guards

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **causedBy stamping** | `event`-triggered that emits events | Emitted events carry `causedBy`; the trigger filter drops self-caused events |
| **Hop budget enforced** | `event`-triggered that emits events | Events carry `causalHops`; the budget check-and-increment is wired; exhaustion alerts |
| **Cycle guards match design** | Feature flagged in a cycle at the Coherence Gate | The designed guards are all present in the implementation |

### Category 4: Identity & Authorization

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **Least privilege** | All | The automation identity's permissions match its `provides.writes` — no wildcards, no admin |
| **Segregation of duties** | `controlled`+ | The initiating identity cannot also approve; enforced by permissions, not logic |
| **No credentials in source** | Any stored-secret identity | No keys/passwords in code, config, or committed env files |
| **Correct attribution** | All | Audit records name the automation identity — actions not falsely attributed to a human |
| **Tenant isolation** | Multi-tenant automation | Queries are scoped; no cross-tenant access |

### Category 5: Agentic Control (when the feature carries the `agentic` block)

Applies when `agentic.agenticProfile: true`. Governs the autonomous agent's control surface — building on the kill-switch and SoD checks above, extended to the agent's **tool set**.

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **Kill-switch reaches the agent loop** | All agentic; mandatory `unattended` | The loop runner consults the kill-switch before each step; flipping it halts the agent (reuses the automation kill-switch — reachable without a deploy) |
| **Tool-set segregation of duties** | `unattended` agentic | The tool set does not let the agent both initiate and approve the same effect — SoD enforced by tool permissions, not prompt/logic |
| **No excessive agency** | All agentic | The tool-permission set is least-privilege and bounded (no wildcard, no ghost tool) — the governance mirror of the ADLC action-surface sub-check |

Agentic findings are reported in the same `atg-findings.json` array (threaded by `automationFeatureId` + `aiFeatureId`).

---

## Output

Results written to `.governance/automation-lens/`:

```
.governance/automation-lens/
├── atg-report-{date}.md          ← Full governance report (human-readable)
├── atg-findings.json             ← Machine-readable findings for dashboard/DFE
└── control-attestations/          ← Control-class attestation documents (living)
    └── AUTO-{NNN}-attestation.md
```

### Report Format

```markdown
# Automation Governance Report — {date}

**Agent:** AIFLC Automation Governance (ATG__)
**Manifest version:** {from manifest}
**Features assessed:** {count}

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | {n} |
| WARNING | {n} |
| PASS | {n} |
| SKIPPED | {n} |

## Findings

### {Feature name} (AUTO-{NNN}) — {sub-mode} / {control class}

| # | Check | Category | Result | Detail |
|---|-------|----------|--------|--------|
| 1 | {check name} | {category} | PASS / WARNING / CRITICAL | {detail} |

## Recommendations
{prioritized list of actions}
```

---

## Severity Model

| Severity | Meaning | Action required |
|----------|---------|-----------------|
| **CRITICAL** | Control/compliance violation or missing safety guard; must fix before release | Block release; immediate remediation |
| **WARNING** | Gap or weakness; should fix; does not block | Remediate within sprint; log as risk |
| **PASS** | Check satisfied; evidence found | None |
| **SKIPPED** | Check not applicable to this feature's sub-mode/control class | None |

**Escalation rule:** for `unattended` + `controlled`/`safety-critical` features, a missing kill switch, missing audit trail, or SoD violation is ALWAYS CRITICAL — never downgrade. For an `unattended` **agentic** feature this extends to the agent loop: a kill-switch that does not reach the reasoning loop, or a tool-set SoD violation, is likewise ALWAYS CRITICAL.

---

## Automation (v1 vs future)

| Version | Behavior |
|---------|----------|
| **v1 (current)** | Manual trigger only (`ATG__`). User invokes when ready. No auto-firing. |
| **v2 (deferred)** | Auto-invocation on PR / pre-release gate. |

---

## Related

- **AUTOMATION_LENS_PROTOCOL.md** §6.2 (AI-GCE contract)
- **AI-TGE `ATQ__`** — the quality/verification counterpart (`ATG__` = governance)
- **AI-DWG `.automation-lens/manifest.json`** — the couriered context (incl. guards + the `agentic` block) this agent reads
- **`automation-lens/architecture/loop-guards.md` + `actor-identity.md` + `audit-observability.md`** — the design rules this agent verifies were implemented
- **`agentic-lens/architecture/tool-use.md`** — the tool-permission + tool-set SoD design the agentic check-set (Category 5) verifies

---

*AIFLC Automation Governance Agent v1.0.0 | Trigger: ATG__ | Owner: AI-GCE | Author: Maheri*
