<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
package: AI-POLC
version: 1.0.0
status: "{in-progress | ready | operating}"
projectId: "{correlation key from pilc-state.md or user-assigned}"
project-name: "{product/project name}"
---

# AI-POLC State — {Product Name}

## Current State

- Phase: {1-6}
- Stage: {1-16}
- Depth: {minimal | standard | comprehensive}
- Mode: {standalone | chain}
- Tier 2: {active | inactive}
- Active Extensions: [{list or "none"}]

## Context Factors

- Architecture Pattern: {monolith | modular | DDD | microservices | "unknown"}
- Team Topology: {stream-aligned | platform | enabling | complicated-subsystem | "unknown"}
- Delivery Methodology: {Scrum | Kanban | SAFe | Shape Up | Hybrid | "unknown"}
- Scale: {single-team | multi-team | enterprise | "unknown"}
- Product Maturity: {new | growth | mature | sunset | "unknown"}
- Market/User Type: {B2C | B2B | internal | platform | "unknown"}
- Regulatory/Compliance: {none | light | heavy | "unknown"}
- Funding Model: {project | product | capacity | "unknown"}
- Stakeholder Density: {low | medium | high | "unknown"}
- Tech Debt Burden: {low | medium | high | "unknown"}
- Data-Driven Capability: {full | limited | none | "unknown"}
- Release Strategy: {continuous | scheduled | feature-flags | big-bang | "unknown"}
- Outsourcing/Distribution: {co-located | distributed | outsourced | "unknown"}

## Backlog Summary

- Total Epics: {N}
- Prioritized: {N}
- In Release Plan: {N}
- Current Priority Model: {WSJF | MoSCoW | value-effort | custom | "not yet selected"}

## Upstream Reads (last timestamps)

- pilc-state.md: {ISO-date or "not detected"}
- adlc-state.md: {ISO-date or "not detected"}
- uxd-state.md: {ISO-date or "not detected"}
- ilc-state.md: {ISO-date or "not detected"}
- aidlc-docs/: {ISO-date or "not detected"}

## DoR/DoD Version

- DoR: {version or "not defined"}
- DoD: {version or "not defined"}

## Dashboard Summary (machine-readable — AI-DFE reads this)

> A small structured block for the dashboard `po` pane (PO tab). Capture the few facts that are otherwise only in free-form docs. AI-DFE reads this when present and falls back to safe defaults otherwise. Keep it current at Governance/Assembly.

```yaml
dashboard-summary:
  vision:
    status: "{draft | approved}"
    statement: "{one-line product vision}"
  velocity:
    trend: "{stable | up | down}"
    method: "{manual | ai-assisted | ai-driven | hybrid}"   # delivery method when set (dashboard-facing subset of ## Velocity Model); omit/manual otherwise
    plannedVsBaseline: "{compression e.g. 0.52 when an AI method is set; omit for manual}"
  acceptance:
    totalCriteria: {N}
    validated: {N}
```

## Velocity Model

> Populated when a delivery method is captured (Stage 1) and/or per-team capacity planning runs (Stage 7). **Absent by default** — when absent, `capacity-planning-matrix.md` is skipped (graceful). Manual-only projects render the Baseline column/track only; the dual view activates only when an AI method is chosen. Full rules: `strategy/delivery-method-timing.md`.

### Delivery Method Profile
- Delivery Method: {manual | ai-assisted | ai-driven | hybrid}
- AI Tool: {tool name | "n/a"}
- Team AI Maturity: {new | practiced | expert | "n/a"}
- Work-Complexity Mix: generic {x}% / standard {y}% / complex {z}%   ← from AI-ADLC Effort Bands when present, else domain classification

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
| {team} | {v} | {v × team-blended multiplier} |
- plannedVsBaseline: manual {A} · {method} {B} · compression {1 − B/A}

## Planning Artifacts

- team-epic-distribution: {generated | stale | not-generated}
- domain-topology-map: {generated | stale | not-generated}
- release-relevance-grouping: {generated | stale | not-generated}
- capacity-planning-matrix: {generated | stale | not-generated}
- Last Derived: {ISO-date or "never"}

## Pending Decisions

- {List of decisions awaiting user input, or "none"}

## Last Session Summary

- Date: {ISO-date}
- What was done: {brief summary}
- Next action: {what should happen next}
