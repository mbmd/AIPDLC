# AIFLC AI Governance — Agent Template

> **Trigger:** `AIG__` (manual invocation)
> **Owner:** AI-GCE
> **Type:** Audit
> **Core impact:** None — the GCE core stays AI-agnostic. This agent is invoked manually by the user.
> **Dependency:** OI-200 (engine agnostic agent-hosting capability). Built against documented interface; final integration pending OI-200 delivery.

---

## Purpose

Perform AI-specific governance checks on the development workspace, using the couriered AI-feature context from `{slug}-workspace/.ai-lens/manifest.json`. Writes results into `.governance/`.

This is the **enforcement half** of the govern+test bracket around the (un-lensed) builder. It checks that architectural commitments, responsible-AI obligations, and regulatory requirements are being followed during development.

---

## When to Invoke

- After significant AI-feature implementation milestones (model integration, RAG pipeline, prompt system)
- Before PR/merge of AI-feature code
- Before any release containing AI features
- Periodically during active AI development (weekly recommended for `augmented`/`native` features)

---

## Consequences of Skipping

- EU AI Act obligations may be unmet at release (legal/compliance risk)
- Responsible-AI guardrails may be missing or incomplete
- PII may reach the model boundary unredacted
- Model versioning and prompt-change governance may lapse
- Audit trail gaps — no evidence of governance for compliance review

---

## Recovery

If `AIG__` has not been run and compliance gaps exist:
1. Run `AIG__` immediately to assess current state
2. Address CRITICAL findings before next release
3. Log governance gap as a `Decision_Log` entry with remediation plan

---

## Input

Reads from `{slug}-workspace/.ai-lens/manifest.json` (the couriered context from AI-DWG):
- Feature list with `aiFeatureId`, `aiSubMode`, `euAiActClass`
- Architecture decisions (model strategy, security controls, RAI posture)
- Acceptance criteria (HITL level, quality thresholds)
- The `agentic` block (when present) — tool registry + permissions, reasoning-trace requirement — needed for the agentic check-set (Category 4)

Also reads from the live workspace:
- `.governance/` existing rules and results
- Source code / config for evidence of compliance
- `prompts/` directory for prompt governance checks
- AI config files for model/endpoint verification

---

## Checks Performed

### Category 1: EU AI Act Obligations

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **Transparency disclosure** | `euAiActClass` = `limited` or `high` | AI disclosure is implemented in the user-facing surface |
| **Risk management documentation** | `euAiActClass` = `high` | Risk management system exists and is documented |
| **Human oversight architecture** | `euAiActClass` = `high` | HITL enforcement is architecturally real (not just UX) |
| **Data governance** | `euAiActClass` = `high` | Training/knowledge data is documented, versioned, bias-assessed |
| **Accuracy monitoring** | `euAiActClass` = `high` | Performance metrics are tracked with defined thresholds |

### Category 2: Responsible AI

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **Guardrails present** | All AI features | Input/output filtering is implemented (not just documented) |
| **Bias testing evidence** | `aiSubMode` = `augmented` or `native` | Bias evaluation has been run; results documented |
| **Model card maintained** | `aiSubMode` = `augmented` or `native` | Living model card exists with current data |
| **Explainability implemented** | Architecture specifies attribution/reasoning | RAG citations or reasoning trace are functional |

### Category 3: Operational Governance

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **PII boundary enforced** | Architecture specifies PII redaction | PII does not reach the model in prompts (code evidence) |
| **Model version pinned** | Any managed-API or self-hosted feature | Model version is explicit (not "latest"); change = reviewed |
| **Prompt change reviewed** | Any feature with `prompts/` directory | Prompt changes go through review process (git history / PR) |
| **AI output logged** | All AI features | AI requests/responses are logged for audit (not necessarily stored permanently) |
| **Cost controls active** | Architecture specifies token budgets | Rate limiting or budget caps are configured |

### Category 4: Agentic Governance (when the feature carries the `agentic` block)

Applies when `agentic.agenticProfile: true`. Governs the agent's action surface — the **excessive-agency** risk class.

| Check | Applies when | Verifies |
|-------|-------------|----------|
| **Tool-permission least-privilege** | All agentic | Each tool's permission matches its backing capability — no wildcard, no tool exceeding its `provides.writes` / `requires.auth` |
| **No excessive agency** | All agentic | The tool registry is closed and bounded; no ghost capability (a callable tool with no declared backing); high-risk / irreversible tools are gated |
| **Reasoning-trace present** | All agentic | Every action the agent takes writes a reasoning trace (the "why") into the audit sink — code evidence, not just design |

Agentic findings are reported in the same `aig-findings.json` array (threaded by `aiFeatureId` + `automationFeatureId`).

---

## Output

Results written to `.governance/ai-lens/`:

```
.governance/ai-lens/
├── aig-report-{date}.md          ← Full governance report (human-readable)
├── aig-findings.json             ← Machine-readable findings for dashboard/DFE
└── model-cards/                   ← Model card documents (living, updated per run)
    └── AIF-{NNN}-model-card.md
```

### Report Format

```markdown
# AI Governance Report — {date}

**Agent:** AIFLC AI Governance (AIG__)
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

### {Feature name} (AIF-{NNN}) — {sub-mode}

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
| **CRITICAL** | Compliance or safety violation; must fix before release | Block release; immediate remediation |
| **WARNING** | Gap or weakness; should fix; does not block | Remediate within sprint; log as risk |
| **PASS** | Check satisfied; evidence found | None |
| **SKIPPED** | Check not applicable to this feature's classification | None |

---

## Automation (v1 vs future)

| Version | Behavior |
|---------|----------|
| **v1 (current)** | Manual trigger only (`AIG__`). User invokes when ready. No auto-firing. |
| **v2 (deferred)** | Auto-invocation on PR / pre-release gate. Requires OI-200 engine capability. |

---

## Related

- **AI_LENS_PROTOCOL.md** §6.2 (AI-GCE contract)
- **AI-TGE `AIQ__`** — the evaluation counterpart (quality/drift; `AIG__` = governance)
- **AI-DWG `.ai-lens/manifest.json`** — the couriered context this agent reads (incl. the `agentic` block)
- **`agentic-lens/architecture/tool-use.md` + `reasoning-loop.md`** — the design rules the agentic check-set (Category 4) enforces
- **OI-200** — engine agnostic agent-hosting capability (build dependency)

---

*AIFLC AI Governance Agent v1.0.0 | Trigger: AIG__ | Owner: AI-GCE | Author: Maheri*
