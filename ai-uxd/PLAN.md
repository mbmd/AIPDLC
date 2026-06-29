# AI-UXD — Design Plan

**Package:** AI-UXD (AI-Driven UX Design Life Cycle)
**Version:** 1.0.0
**Date:** 2026-06-12
**Author:** Maheri
**Status:** Complete (v1.0.0)

---

## 1. Problem Space

### The Gap

The AI-* Family chain produces software through a governed pipeline — but the **user experience** has no producer. UX surfaces only as downstream code standards (AI-DWG `frontend-standards.md`, AI-GCE `frontend-compliance.md`) authored in an engineering voice. The actual design discipline — research, personas, journeys, information architecture, user flows, design systems, design tokens, accessibility-by-design — is undefined and ungoverned.

Three structural mismatches result:

1. **Ordering inversion** — UX is wired downstream (frontend code) when real UX runs upstream and parallel to architecture (research → IA → flows → wireframes → design system → validation).
2. **No persona** — every package has a domain-expert persona; there is no `#persona-ux-designer`, so frontend output reads like infrastructure, not design.
3. **Missing producer** — AI-DWG's `frontend-standards.md`, AI-GCE's `frontend-compliance.md`, and the accessibility expectation all assume design tokens, a component inventory, interaction patterns, and a WCAG baseline already exist. Nothing emits them.

### Identity Spine (Lesson 36)

> AI-UXD turns business intent and user research into a governed UX Design Package, and is the single source of truth for *how the product looks, feels, and behaves for the humans who use it*.

**Inclusion rule:** in scope = *how does the user experience this / what does it look and behave like / can everyone use it*. Out = *what/why/order* (AI-POLC), *how it's built/deployed* (AI-ADLC/AI-DLC v1), *runtime compliance* (AI-GCE).

---

## 2. Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-UXD |
| **Full Title** | AI-Driven UX Design Life Cycle |
| **Package Type** | Interactive workflow (lifecycle) |
| **Input** | PIP (AI-PILC) and/or AP (AI-ADLC); strategy exchange with AI-POLC; standalone: product/brand brief |
| **Output** | UX Design Package (UXP) |
| **Primary Persona** | `#persona-ux-designer` |
| **Marker File** | `uxd-state.md` |
| **Family Position** | Project layer — parallel to AI-ADLC and AI-POLC |

### Name Challenge (Lesson 12)

| Candidate | Verdict |
|-----------|---------|
| **AI-UXD** ✓ | 3 letters, "UX Design" — accurate, pronounceable, family-parallel |
| AI-UXLC | Redundant — "LC" already in package type |
| AI-XDLC | Obscure — "XD" not immediately recognizable |
| AI-DXG | Implies "generator" — this is a lifecycle, not a one-shot |

---

## 3. Phase / Stage Summary

5 phases, 16 stages. Inspired by the Double Diamond (Discover → Define → Develop → Deliver) adapted to produce governed artifacts with gates.

| Phase | Stages | Key Deliverable |
|-------|--------|-----------------|
| **1. Discover** | 1-3 | Personas + research synthesis |
| **2. Define** | 4-6 | Journeys + IA + user flows |
| **3. Design** | 7-10 | Wireframes + design system + components + theming |
| **4. Validate** | 11-13 | Accessibility baseline + usability plan + design QA |
| **5. Assemble** | 14-16 | Handoffs + package README |

See `core-workflow.md` for full stage definitions, steps, and orchestration logic.

---

## 4. Design Decisions

### 4.1 Modes (Lesson 6 — OR-Input)

| Mode | Input | Behavior |
|------|-------|----------|
| A | Full chain (PIP + AP) | Reads PIP for business context + AP for technical constraints |
| B | PIP only | Reads PIP; no technical constraints |
| C | Standalone (product/brand brief) | Manual brief; full UX lifecycle |
| D | Brownfield (existing design system/UI) | Map → gap → govern from current state |

### 4.2 Depth Adaptation

| Level | Trigger | Behavior |
|-------|---------|----------|
| Minimal | Simple app, ≤2 user types, clear scope | 2-3 personas, 1-2 journeys, essential tokens |
| Standard | Typical product, 3-5 user types | Full set across all stages |
| Comprehensive | Complex platform, accessibility-critical | Extended research, service blueprints, empathy maps, multi-brand |

### 4.3 Conditional Generation (Lesson 7)

| Output | Condition |
|--------|-----------|
| Multi-brand theming + dark mode | IF >1 brand OR color modes in brief |
| i18n/RTL/localization tokens | IF >1 locale OR multi-language mentioned |
| Service blueprints | IF Comprehensive + service-oriented |
| Empathy maps | IF Comprehensive depth |

### 4.4 Multi-Brand Theming in Core (not extension)

Moved into core because color modes (dark/light) are universal enough that most products encounter them. Stage 10 is CONDITIONAL — skipped for single-brand, single-mode products, but available without extensions.

### 4.5 Design QA in Core (not extension)

Defines the *governance framework* for design-to-code drift detection — what to compare, severity model, report format. Doesn't require AI-DLC v1 to be running; it sets up the rules for when it does.

### 4.6 i18n/RTL/Localization in Core (conditional)

A section within Design System Foundation (Stage 8). Covers text expansion rules, bidirectional layout tokens, locale-aware spacing. Conditional on multi-language need — skipped for single-locale products.

---

## 5. Chain Contracts

| Contract | Value |
|----------|-------|
| **I Read** | `pilc-state.md` + PIP (Mode A/B); `adlc-state.md` + AP (Mode A); product brief (Mode C); existing design artifacts (Mode D) |
| **I Produce** | `uxd-state.md` + UXP folder |
| **My Marker** | `uxd-state.md` |
| **Detection** | User provides path → scan for `uxd-state.md` → ask user |
| **Downstream Consumers** | AI-POLC (personas/journeys), AI-DWG (design system + tokens → `design-system.md` + `frontend-standards.md`), AI-GCE (accessibility baseline → `accessibility-compliance`) |

### Producer/Consumer Handoffs

| Handoff | What flows | Direction |
|---------|-----------|-----------|
| AI-UXD → AI-POLC | Personas, journey maps, JTBD | Producer → Consumer |
| AI-POLC → AI-UXD | Value goals, OKRs (focus research) | Strategy exchange |
| AI-UXD → AI-DWG | Design system, tokens, accessibility baseline | Producer → Consumer |
| AI-UXD → AI-GCE | Accessibility baseline, component standards | Producer → Consumer |
| AI-DLC v1 → AI-UXD | Usability/accessibility signals, behavioral analytics | Feedback channel |

---

## 6. Brownfield Mode (Lesson 23)

| Aspect | Greenfield | Brownfield |
|--------|-----------|-----------|
| Research | "Who are the users?" | "Who uses this today? What works/doesn't?" |
| Design system | Create from scratch | Map existing → gap → augment |
| Tokens | Define new | Extract existing → normalize → govern |
| Components | Define new | Inventory existing → classify → standardize |
| Accessibility | Set baseline from WCAG | Audit existing → baseline current state → improve |

---

## 7. Extensions (v1.1+)

| Extension | Trigger | What it adds |
|-----------|---------|-------------|
| Hi-fi prototype integration | Deep Figma/tool round-tripping | Governed tool sync, variant mapping, drift alerts |
| Motion design | Complex animation needs | Motion tokens, easing library, choreography rules, prefers-reduced-motion |
| Data visualization design | Dashboard/analytics products | Chart patterns, data-ink ratio rules, visualization tokens |
| Conversational UI | Chatbots, voice assistants | Dialog flow patterns, conversation tokens, VUI principles |

---

## 8. Prior Art / Research Sources

- Double Diamond (UK Design Council, 2005) — Discover/Define/Develop/Deliver
- Atomic Design (Brad Frost) — atoms/molecules/organisms/templates/pages
- W3C Design Tokens Format Module (2025.10 stable spec) — vendor-neutral token format
- WCAG 2.2 (W3C, 2023) — 86 success criteria, POUR principles
- Rosenfeld & Morville — 4 IA systems (organization, labeling, navigation, search)
- Nielsen's 10 Usability Heuristics — heuristic evaluation framework
- NNGroup — wireflows, journey maps, IA study guide
- Jobs-to-be-Done framework — persona/journey grounding
- Jeff Patton Story Mapping — shared vocabulary with AI-POLC

---

## 9. Build Sequence

| # | File | Step |
|---|------|------|
| 1 | `PLAN.md` | ← This document |
| 2 | `core-workflow.md` | Step 4 — master orchestration |
| 3 | Common files (6) | Step 5 |
| 4 | Phase detail files (16) | Step 6 — one at a time |
| 5 | Templates (15) | Step 7 |
| 6 | Agent + shortcut block | Lesson 49-51 |
| 7 | README + LICENSE + INSTALL | Step 8 |
| 8 | `#persona-ux-designer` reference file | Persona creation |
| 9 | Dry Test | Step 9 |

---

## 10. Applicable Lessons

| Lesson | Application |
|--------|-------------|
| 1 | "Life Cycle" correct — interactive multi-phase with gates |
| 6 | OR-input: chain OR standalone |
| 7 | Conditional generation (theming, i18n, service blueprints) |
| 9 | Extensions for the 20% (motion, prototype integration) |
| 12 | Name challenged — AI-UXD confirmed |
| 13 | Chain contracts explicit (I Read / I Produce) |
| 14 | Detection by marker (`uxd-state.md`) |
| 23 | Brownfield is first-class |
| 25 | Two-source model not needed (UXD is not an enforcement engine) |
| 26 | Plan = summary; core-workflow = spec |
| 28 | Reference read first (online research — no local ref exists) |
| 33 | Persona embedded self-contained, no skills list |
| 36 | Identity spine + inclusion rule defined |
| 38 | Standalone confirmed via coupling analysis (idea 010) |
| 45 | Governance spine: append-if-exists, POLC-* prefix |
| 51 | Ships own agent (UXC__) |

---

*Created: 2026-06-12 | Source: Idea 010 (Approved 2026-06-10) + online UX research*
