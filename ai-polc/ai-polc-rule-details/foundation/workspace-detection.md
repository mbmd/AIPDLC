# Stage 1: Workspace Detection & Intake

**Phase:** Foundation
**Purpose:** Detect the operating mode (chain/standalone), establish context factors, scan for upstream changes, and determine the workflow's starting point.

---

## MANDATORY: Stage Sub-Role

None required — primary Product Owner persona is sufficient for workspace detection.

---

## Purpose

This is the orientation stage. Before any product work begins, AI-POLC must understand:
- What upstream input is available (chain mode) or absent (standalone)
- What context factors shape the product's governance needs
- Whether this is a cold start or a resume with upstream changes

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Quick scan, accept defaults for unknown context factors, proceed fast |
| **Standard** | Full scan, ask user for missing context factors, confirm mode |
| **Comprehensive** | Full scan + detailed exploration of each context factor's impact on governance |

---

## Steps

### Step 1.1: Detect Operating Mode

Scan the workspace for upstream markers:

| Marker | If Found | Mode Implication |
|--------|----------|-----------------|
| `pilc-state.md` | PIP available | Chain (has project initiation context) |
| `adlc-state.md` | AP available | Chain (has architecture context) |
| `uxd-state.md` | UXP available | Chain (has UX research context) |
| None of the above | No upstream | Standalone |

**Record** the mode in `polc-state.md`: `Mode: chain` or `Mode: standalone`

### Step 1.2: Extract Upstream Context (Chain Mode)

If upstream markers detected, read and extract:

**From `pilc-state.md` / PIP:**
- Project ID (correlation key — Lesson 43)
- Project name
- Business objectives / scope statement
- Stakeholder register (names, interests, influence)
- Project-level risks
- Depth level used in PILC
- Scale (single team / multi-team / enterprise)

**From `adlc-state.md` / AP:**
- Architecture pattern (monolith / modular / DDD / microservices)
- Brownfield flag
- Tech debt assessment
- Bounded contexts (if DDD)
- Enabled extensions

**From `uxd-state.md` / UXP:**
- Personas (user segments)
- Journey maps
- Research findings

### Step 1.3: Establish Context Factors

For each of the 13 context factors, determine the value:

| Factor | Auto-Detected From | If Not Detectable |
|--------|-------------------|-------------------|
| Architecture Pattern | `adlc-state.md` | Ask user |
| Team Topology | PIP or user | Ask user |
| Delivery Methodology | User | Ask user (🔴 Required) |
| Scale | `pilc-state.md` | Ask user |
| Product Maturity | User | Ask user (🔴 Required) |
| Market/User Type | User | Ask user (🔴 Required) |
| Regulatory/Compliance | AI-GCE presence + PIP risks | Ask user |
| Funding Model | User | Ask user (🟡 Optional — default: product) |
| Stakeholder Density | Stakeholder Register count | Ask user |
| Tech Debt Burden | `adlc-state.md` brownfield | Ask user (🟡 Optional — default: low) |
| Data-Driven Capability | User | Ask user (🟡 Optional — default: limited) |
| Release Strategy | User | Ask user (🟡 Optional — default: scheduled) |
| Outsourcing/Distribution | User | Ask user (🟡 Optional — default: co-located) |

At **Minimal** depth: ask only 🔴 Required; use defaults for 🟡 Optional.
At **Standard** depth: ask all, offer defaults.
At **Comprehensive** depth: ask all, explain impact of each.

### Step 1.4: Scan for Upstream Changes (Resume Only)

If `polc-state.md` already exists (resume session), run the session-start routine:

1. Check `ilc-state.md` for Route=feature (new feature brief?)
2. Check governance spine for new PILC-C entries since last read
3. Check `uxd-state.md` timestamp vs. recorded
4. Check `aidlc-docs/` for changes since last review

Present detected changes to user. User decides: process now or defer.

### Step 1.5: Determine Depth Level

Based on context factors, recommend a depth level:

| Signal | Recommended Depth |
|--------|------------------|
| Small product, low complexity, few stakeholders, clear intent | **Minimal** |
| Normal product, moderate complexity, standard team | **Standard** |
| Enterprise, multi-team, heavy compliance, high uncertainty | **Comprehensive** |

Present recommendation. User confirms or overrides.

### Step 1.6: Check for Brownfield

If user states an existing backlog exists (or files suggest one), flag brownfield mode:

- "I see you have an existing backlog. Would you like me to audit and adopt it under AI-POLC governance, or start fresh?"
- If brownfield: set a flag in state, adjust Phase 2 behavior (audit before decompose)

### Step 1.7: Initialize State File

Create `polc-state.md` with all established values. If chain mode, copy the `project-id` from `pilc-state.md`. If standalone, ask user for a project identifier or generate one.

---

## Gate

**Gate 1 — Context Established:**

Present to user:
```
Context established:
• Mode: {chain | standalone}
• Depth: {minimal | standard | comprehensive}
• Key context: {2-3 most impactful factors}
• Upstream input: {what was found}
• Brownfield: {yes/no}

Proceed to Stage 2 (Product Vision & Goals)?
```

User must confirm before proceeding.

---

## Transition

→ **Stage 2: Product Vision & Goals** (Foundation continues)

---

*Detail file for AI-POLC Stage 1 | Phase: Foundation*
