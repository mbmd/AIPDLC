<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-UXD — Content Validation Rules

**Purpose:** Quality rules that every AI-UXD artifact must pass before stage gate approval. Use this as a checklist for artifact review.

---

## Pre-Gate Structural Lint

Before presenting a completed artifact at a gate, run this mechanical 6-point check on the full `.md` file and silently fix the auto-fixable issues. These are formatting/structure checks — they run alongside the semantic checks below, not in place of them.

1. **Monotonic headings** — sections stay in order (no §5.6 after §7). *(flag)*
2. **Single footer** — exactly one closing footer; remove duplicates. *(auto-fix)*
3. **Status consistency** — status strings agree with the current state. *(auto-fix)*
4. **List blank-line** — every list has a blank line before its first item. *(auto-fix)*
5. **xychart axis range** — the y-axis spans the actual data values. *(auto-fix)*
6. **Heading-level sanity** — no level jumps (H2 → H4) and only one H1. *(flag)*

Record a one-line result — "Pre-gate lint: {N} passed, {M} auto-fixed, {K} flagged." — and flag the non-auto-fixable issues (checks 1, 6) with the artifact.

---

## Universal Rules (Apply to ALL Artifacts)

### Formatting
- [ ] Markdown format with proper heading hierarchy (H1 = document title, H2 = sections)
- [ ] Tables use consistent column widths and alignment
- [ ] Code blocks use proper language identifiers where applicable
- [ ] No orphaned links (every link resolves to an existing artifact or external resource)
- [ ] Consistent date format: ISO 8601 (`YYYY-MM-DD`)

### Content Quality
- [ ] Zero project-specific hardcoded content — all project values use `{placeholder}` syntax
- [ ] No lorem ipsum or filler text — every content slot has either real content or `{placeholder}`
- [ ] Professional language — no casual tone, no hedging ("maybe", "perhaps", "could be")
- [ ] Actionable — every section tells the reader what to DO, not just what to know
- [ ] Concise — no redundant explanations; say it once, clearly

### Traceability
- [ ] Every artifact references its source (which stage produced it, what input informed it)
- [ ] Personas referenced by name (not "User Type 1")
- [ ] Journeys reference their owning persona
- [ ] Flows reference their owning journey stage
- [ ] Components reference the flows/screens where they appear
- [ ] Tokens reference the design principles they serve

### Provenance (NAMING_AND_OWNERSHIP.md §5.2)
- [ ] Front-matter present on all generated artifacts:
```yaml
---
generatedBy: AI-UXD
generatedVersion: 1.0.0
source: {upstream-doc-path}
generatedOn: {ISO-date}
ownership: generated | hybrid | user
---
```

---

## Per-Artifact-Type Rules

### Personas
- [ ] Each persona has: Name, Role/Context, Goals (≥2), Pain Points (≥2), Behaviors, Quoted Need
- [ ] Goals are outcome-oriented ("Complete X in Y time") not feature-oriented ("Use button Z")
- [ ] No demographic-only personas — must include behavioral data
- [ ] At Comprehensive depth: includes empathy map (Think/Feel/Say/Do)
- [ ] JTBD framing present: "When {situation}, I want to {motivation}, so I can {expected outcome}"

### Journey Maps
- [ ] Structured as: Stages → Actions → Touchpoints → Emotions → Opportunities
- [ ] Each journey has: owning persona, starting trigger, end state
- [ ] Emotions mapped per stage (positive/neutral/negative with intensity)
- [ ] Opportunities linked to design decisions downstream
- [ ] Error/edge-case paths explicitly shown (not just the happy path)
- [ ] Onboarding represented as an explicit journey where relevant

### Information Architecture
- [ ] Contains all four IA systems: Organization, Labeling, Navigation, Search
- [ ] Site map present with clear hierarchy (max 3 levels deep for navigation)
- [ ] Navigation model specified (global + local + contextual + utility)
- [ ] Labeling system defined (terminology glossary for the product)
- [ ] Validated against personas: "Can {persona} complete {goal} via this structure?"

### User Flows
- [ ] Each flow has: entry point, exit point(s), decision diamonds, error branches
- [ ] Flow type declared: Task Flow (single path) / User Flow (multi-path) / Wireflow (with UI)
- [ ] All decision points have both Yes/No (or equivalent) paths drawn
- [ ] Error paths lead to recovery (never dead-end)
- [ ] Mapped back to journey stage (traceability)
- [ ] States identified: what data is the system in at each step?

### Design System
- [ ] Design principles: 4-6 principles, each with a "This means..." concrete implication
- [ ] Color system: palette + semantic roles + contrast ratios documented
- [ ] Typography: complete type ramp with sizes, weights, line heights, use cases
- [ ] Spatial system: grid definition + breakpoints + responsive behavior rules
- [ ] Iconography: style guide + sizing scale + usage rules
- [ ] Voice & tone: principles + patterns per context (error, success, empty, onboarding, CTA)
- [ ] All values expressed as tokens (Global → Semantic → Component tiers)

### Design Tokens
- [ ] Follows W3C Design Tokens Format Module structure
- [ ] Token naming convention defined and consistent (e.g., `color.primary.500`)
- [ ] Three tiers present: Global (raw), Alias/Semantic (purpose), Component (scoped)
- [ ] Every token has: name, value, type, description
- [ ] No magic numbers — every dimension traces to a token

### Component Library
- [ ] Each component has: visual spec, ALL states, interactions, responsive behavior, accessibility
- [ ] States covered: default, hover, focus, active, disabled, loading, error, empty, skeleton
- [ ] Keyboard interaction defined for every interactive component
- [ ] ARIA roles/properties specified
- [ ] Atomic Design level declared (atom/molecule/organism)
- [ ] Content constraints defined (character limits, truncation, overflow behavior)

### Accessibility Baseline
- [ ] WCAG conformance target stated (Level AA minimum)
- [ ] Organized by POUR principles
- [ ] Per-component accessibility requirements defined
- [ ] Keyboard interaction patterns documented
- [ ] Screen reader expectations per component
- [ ] Color contrast ratios verified against token values
- [ ] Motion accessibility addressed (prefers-reduced-motion)

### Wireframes
- [ ] Screen inventory complete (every unique state from flows)
- [ ] Layout zones defined (header, nav, content, sidebar, footer patterns)
- [ ] Content hierarchy visible (what's primary, secondary, tertiary)
- [ ] Interaction points marked (what's clickable/tappable)
- [ ] Responsive behavior annotated per breakpoint

---

## Cross-Reference Validation

After all stages complete, verify the following cross-references are intact:

| From | To | Check |
|------|----|-------|
| Persona | Journey | Every persona has ≥1 journey |
| Journey | Flow | Every journey stage maps to ≥1 flow |
| Flow | Screen | Every flow step maps to a screen in the inventory |
| Screen | Component | Every screen uses only components from the library |
| Component | Token | Every component value traces to a token |
| Token | Principle | Every semantic token connects to a design principle |
| Component | Accessibility | Every interactive component has accessibility spec |

---

## File Naming Convention

| Artifact Type | Pattern | Example |
|---------------|---------|---------|
| Persona | `Persona_{NN}_{Name}.md` | `Persona_01_Healthcare_Admin.md` |
| Journey | `Journey_{NN}_{Persona}_{Goal}.md` | `Journey_01_Admin_Onboarding.md` |
| Flow | `Flow_{NN}_{Task}.md` | `Flow_01_Create_Patient_Record.md` |
| Component | `Component_{Name}.md` | `Component_Button.md` |
| Wireframe | `Wireframe_{Screen}.md` | `Wireframe_Dashboard_Home.md` |

---

### 11. Contextual Prose Accompaniment (CPA)

**Detects:** Cross-reference keys or `See …` pointers that lack explanatory context.

**Rule:** Every cross-reference in the artifact must have contextual accompaniment per the CPA patterns (see `common/contextual-prose-accompaniment.md`), scaled to the current depth level:

| Pattern | Applies to | Minimal | Standard | Comprehensive |
|---------|-----------|---------|----------|---------------|
| **A** (qualifier phrase) | Table cells with refs | ≤ 12 words | ≤ 25 words | ≤ 50 words |
| **B** (contextual sentence) | Narrative refs | Single phrase | 1 sentence | 1–2 sentences |
| **C** (provenance block) | State file front-matter | Omitted | 2-line comment | 3–4 line comment |
| **D** (Consumer/Reads/Why) | Package README refs | Bullet list | Full table | Table + narrative |
| **E** (decision expansion) | ADR/decision refs | Title + link only | Title + ≤ 15-word rationale + link | Title + rationale + alternatives + link |

**Exempt:** Same-file references, the `## References` block, forward references (`_[To be produced in Stage {n}]_`), YAML front-matter values, fabric routing metadata.

**Auto-fixable:** ❌ (requires semantic understanding of the referenced content)

**Action if violated:** Flag to user: "Reference {code} at line {N} lacks contextual accompaniment. Add a qualifier explaining what this reference means here."

---

*Part of AI-UXD v1.0.0 | Reference: core-workflow.md § Key Principles*

---

## Artifact Content Rules (IMP-001–005, 015, 016, 019)

> Added 2026-08-15 from user-workspace field validation. These are **BLOCKING** rules — an artifact fails validation without compliance.

### IMP-001: Self-Explanatory Quantitative Artifacts

Every artifact containing quantitative analysis (scores, rankings, matrices, assessments) MUST include a **"What This Analysis Means"** section placed AFTER the document title/introductory blockquote but BEFORE the first numbered section (`## 1. ...`).

The section MUST include:
1. **Plain-language summary** — what the numbers mean in business terms
2. **Concrete example** — one specific finding from the analysis explained simply
3. **Business implications** — what action or decision the analysis supports

**Blocking:** Artifact fails validation if quantitative analysis is present but no interpretation section exists at the top.

---

### IMP-002: Completeness & Downstream Resolution

Every artifact MUST include a **"Completeness & Downstream Resolution"** section (placed after the main content, before Glossary/Sources) that answers three questions:

1. **What's complete here?** — which aspects are fully covered in this document
2. **What's partial and why?** — what is shown as representative samples vs exhaustive, and the rationale
3. **Where/when does each gap get resolved?** — downstream package/stage that fills each gap (with package code + stage reference)

**Blocking:** Artifact fails validation without this section.

---

### IMP-003: Back-Propagate "Gap Filled" Status

After each stage writes its artifact, scan all earlier-stage artifacts in the same package for "Completeness & Downstream Resolution" sections that reference the just-completed stage. Update those references:
- FROM: "Where gaps get filled → {Package} Stage N"
- TO: "✅ Completed — see `{artifact-path}`"

Stale "where gaps get filled" references pointing to already-completed stages are a **validation failure**.

**Post-gate check:** After each gate approval, verify no earlier artifact references the just-completed stage as "pending."

---

### IMP-004: Human-Readable Package Key Expansion

First mention of any package code in an artifact MUST include a parenthetical plain-language description.

**Pattern:** `AI-{XXX} ({Human-Readable Purpose})`

**Examples:**
- `AI-AAG (Governance & Handoff)` — not just `AI-AAG`
- `AI-INT (Integration Architecture)` — not just `AI-INT`
- `TALC (Technology Architecture Life Cycle)` — not just `TALC`

Subsequent mentions in the same document may use the bare code after first-use expansion.

**Blocking:** First-use bare codes without expansion are a validation failure.

---

### IMP-005: Mandatory Glossary Section

Every artifact MUST include a **"Glossary"** section at the bottom of the document (before Sources Used or doc signature/footer). The glossary MUST:

1. Appear as the last major section before Sources/footer
2. Contain a table with **Term** and **Meaning** columns
3. Cover ALL abbreviations (e.g., K8s, mTLS, GPU, RAG, SWOT) and domain-specific technical terms used in the document
4. Be tailored to each document's actual content — not a generic copy-paste

**Blocking:** Artifact fails validation without a document-specific glossary.

---

### IMP-015: Rank-Score Consistency

In any table with both a **Rank** column and a numeric **Score/Significance** column:

1. Rank MUST be in **descending score order** (highest score = rank 1)
2. If a dependency or business override changes the rank, an explicit **override column or footnote** MUST explain WHY (e.g., "GATE-ZERO prerequisite", "Blocked by #1")
3. **Equal scores** MUST use tied ranks (e.g., 1, 1, 1, 4 — not 1, 2, 3, 4)

**Blocking:** Rank/score mismatch without documented justification is a validation failure.

---

### IMP-016: Key-Reference Traceability (CRITICAL)

Every reference to a key (`OBJ-01`, `CAP-05`, `REQ-D-03`, `THEME-02`, `SD-001`, `GAP-04`, etc.) in any artifact MUST be a markdown link pointing to the source document where that key is formally defined.

**Pattern:** `[KEY-ID](relative-path-to-source#anchor)`

**Rules:**
1. Every register/definition document MUST define anchors for every key (`<a id="key-id"></a>`)
2. Every reference to a key in any other artifact MUST be a markdown link to the source anchor
3. **Bare key codes without links are NOT acceptable** in final artifacts — only in draft state
4. Each stage's post-write checklist must include a "Link Validation" step verifying all keys are linked

**Key prefixes requiring anchors and links:** `OBJ-`, `THEME-`, `SD-`, `CAP-`, `REQ-`, `REQ-D-`, `REQ-T-`, `CC`, `CON-`, `GAP-`, `DEBT-`, `RDR-`, `ST-`, `SO-`, `WO-`, `WT-`, `INFRA-`, `SEC-`, `RES-`, `GPU-`

**Blocking (CRITICAL):** Bare key references without links are a validation failure.

---

### IMP-019: Column Legend for Register-Style Tables

Every **register-style table** (4+ columns with an ID/identifier column or technical register structure) MUST be followed immediately by a blockquote column legend.

The legend MUST:
1. Be inside a `>` blockquote
2. Start with `**Column Legend:**`
3. Contain a two-column table (Column / Description)
4. Describe ALL columns including value-set meanings (e.g., "Priority: Critical = must resolve before deployment, High = must resolve before production")

**Excluded:** Simple key-value tables (Field/Value format) and prose checklists.

**Blocking:** Register-style tables without a column legend are a validation failure.
