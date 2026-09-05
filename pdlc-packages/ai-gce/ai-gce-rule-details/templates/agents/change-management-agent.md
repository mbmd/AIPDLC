<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: change-management-agent
description: >
  Validates change management compliance before releases — change plan existence,
  UAT traceability, stakeholder sign-off, rollback criteria, and training completion.
generatedBy: AI-GCE
generatedVersion: "{version}"
source: ai-gce-rules/core-engine.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read", "shell"]
trigger: CMG__
tier: 3
type: process
---

# Change Management Agent

## Purpose

Validates change management governance compliance before any release or deployment reaches production. Checks that a change management plan exists, UAT is traceable to requirements, stakeholder sign-off is documented, rollback criteria are defined, and training completion is verified. Prevents ungoverned changes from reaching production.

## When to Invoke

Call this agent **before any release or deployment** — after development is complete but before pushing to production.

- **Trigger:** Type `CMG__` in the chat prompt
- **Cadence:** Every release cycle (could be weekly, bi-weekly, or per-feature)
- **Process point:** After final testing, before production deployment

**Concrete examples:**
- "Release v1.3.0 is ready to deploy" → call `CMG__` first
- "Hotfix going to prod" → call `CMG__` (even hotfixes need governance)
- "Feature flag flip for Feature X" → call `CMG__` if it exposes new functionality to users
- "Database migration to production" → call `CMG__` (infrastructure changes count)

## Consequences of Skipping

**Immediate impact:**
- Changes reach production without documented plan
- No rollback criteria defined → if things break, ad-hoc recovery
- Stakeholders surprised by changes they didn't approve
- UAT not traceable → "did we actually test this?"

**Accumulated debt (3+ missed releases):**
- Cannot demonstrate controlled change process (regulatory finding)
- Incident response hampered — no rollback playbook exists
- Stakeholder trust erodes — they learn about changes after the fact
- SOX/ISO compliance gap: "no evidence of change authorization"
- Audit score critically low in "change management" category

## Recovery

If you missed `CMG__` before a deployment:

1. **If not yet in production:** STOP. Run `CMG__` now. Fix gaps. Then deploy.
2. **If already in production:**
   - Run `CMG__` retroactively — document the change post-facto
   - Log as a **change management exception** in compliance-log:
     ```json
     {"type": "EXCEPTION", "ruleId": "CM-001", "justification": "Deployed without CMG gate — retroactive documentation"}
     ```
   - Write the change plan retroactively (document what changed, why, rollback option)
   - Conduct a brief post-mortem: why was the gate skipped? (time pressure? forgotten? process unclear?)
   - Update the release checklist to include `CMG__` as a mandatory step
3. For recurring skips: escalate to team lead — may need to enforce via CI pipeline gate

## Checks Performed

1. **Change plan exists:** Is there a documented change plan for this release? (what's changing, why, risk level, rollback)
2. **UAT traceability:** Can every feature in the release be traced back to:
   - A user story or requirement (what was requested)
   - A test case (how it was verified)
   - A test execution result (proof it passed)
3. **Stakeholder sign-off:** Is there documented approval from the required stakeholders? (per the project's change authority matrix)
4. **Rollback criteria:** Are rollback conditions defined? (what signals trigger a rollback, who decides, what's the procedure)
5. **Rollback procedure:** Is the actual rollback method documented and tested? (not just "we'll figure it out")
6. **Training completion:** If the change affects end-users, is training/documentation updated?
7. **Communication plan:** Are affected parties notified? (operations team, support team, end-users if applicable)
8. **Deployment window:** Is there an agreed deployment window? (not during peak usage, not on a Friday afternoon)

## Output

- **If all checks pass:** Confirmation — "Change management gate: ✅ Release {version} cleared for deployment."
- **If violations found:**
  - Per-check report with severity (🔴 Critical = deployment should not proceed)
  - Compliance log entry appended to `compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, hook: `change-management-agent`, result: `pass|fail|warn`
  - For missing rollback criteria: result is `fail` (blocking recommendation)

**Output location:** `.governance/compliance-log/events/`

## Related

- **Steering source:** `project-governance.md` (phase gates), `git-workflow.md` (deployment strategy) — AI-DWG output
- **Rules enforced:** `CM-001`, `CM-002`, `CM-004`, `CM-005`, `CM-006`, `CM-010` — the six the `change-management-gen.md` generator actually produces. ⚠️ **This line previously read "CM-01 through CM-08", wrong three ways:** two-digit padding (the `CM-*` family is three-digit, like every `GOV-*`/process-governance family — see the note below); a contiguous 01–08 range (the generator emits six non-contiguous IDs — `003`, `007`, `008`, `009` do not exist); and a ceiling of `08` that excludes the real `CM-010`. Cite the generator's set, never a range.

> **Padding — code-level families take two digits, process/governance families take three.** `SEC-01`, `DATA-02`, `MOD-01`, `DOM-05`, `NC-01`, `ERR-01` are code-level and two-digit. `GOV-*`, `CM-*` and instantiated `PG-*` are process/governance and three-digit. `CM-` is change *management* — process governance — so `CM-001` is correct and this agent was the outlier, not the generator. *(This reverses an earlier plan to normalise `CM-*` down to two digits: the generator is right; the fix is to bring the agent up to it.)*
- **Hooks (complementary):** `change-readiness-gate.json` (Tier 3, `preTaskExecution`) enforces the same `CM-*` family at a task boundary; this agent is the on-demand review of the same concern. ⚠️ **This line previously claimed to replace a former `change-management.json` hook. No such hook ever existed** — it was never declared in the hook inventory and never had a template. This agent was authored as an agent from the start, so there is nothing to record as a conversion.
- **Registers affected:** Change Register (change plan logged), Decision Register (deployment go/no-go)
- **Contract:** Agent Governance Contract §5, §6
