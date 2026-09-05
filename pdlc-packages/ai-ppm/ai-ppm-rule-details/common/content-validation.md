<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-PPM — Content Validation Rules

**Purpose:** Define quality standards for all AI-PPM output. Every artifact produced by this engine must meet these rules before being presented to the user.

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

## Universal Rules (Apply to ALL Output)

### 1. Portfolio Scope Only

- Every statement must be about the **portfolio as a whole** or about **projects in comparison to each other**
- Never produce single-project analysis (that's PILC/POLC/ADLC territory)
- Test: "Does this require knowledge of multiple projects?" If no → wrong scope

### 2. No Project-Specific Content in Templates

- Templates use `{placeholder}` for values filled during generation
- Templates use `_[TBD]_` for values the user provides later
- Zero hardcoded project names, dates, budgets, or team names in any template
- Test: "Could I use this template for any portfolio?" If no → too specific

### 3. Provenance Front-Matter (Mandatory)

Every generated `.md` file must include:

```yaml
---
generatedBy: AI-PPM
generatedVersion: 1.0.0
source: {upstream-doc-path or "portfolio-governance"}
generatedOn: {ISO-date}
ownership: generated | hybrid | user
---
```

### 4. Source-Driven — Never Fabricate Data

- All portfolio data must trace back to: PIP sources (read from `pilc-state.md`), ILC briefs, FLO roll-ups, or user-provided information
- Never invent project status, budget figures, risk scores, or health indicators
- If data is unavailable, state: "Data not available — manual update needed" (never guess)

### 5. Quantified Over Qualitative

- Prefer numbers over adjectives: "3 of 7 projects are at-risk" over "several projects have issues"
- Always include the denominator: "4/10 aligned" not "4 aligned"
- Scores must show the scale: "Strategic alignment: 18/25" not just "18"

### 6. Comparative Framing

- When discussing a project, always relate it to the portfolio: "ranks #3 of 8" not just "high priority"
- Dashboard views must show all projects (or a meaningful subset) — never just one in isolation
- Governance decisions must state impact on OTHER projects: "admitting X delays Y by 2 sprints"

---

## Artifact-Specific Rules

### Portfolio Register

- Every row must have: Project ID, Name, State, Priority Rank, Strategic Alignment Score, Health (RAG), Last Updated
- States are ONLY: `Registered` | `Prioritized` | `Authorized` | `Active` | `Paused` | `Retired`
- Priority rank must be unique (no ties without explicit tie-breaking rationale)
- "Last Updated" reflects the most recent data refresh (from FLO or manual)

### Governance Decision Records

- Must include: Decision type, Project affected, Rationale, Conditions, Review date
- Rationale must reference at least one data point (score, threshold, comparison)
- Must state WHO made the decision (user, portfolio manager)
- Must state WHAT changes as a result (state transition, resource release, etc.)
- Sequential numbering: PGD-001, PGD-002, …

### Prioritization Scorecard

- Must show the model used (Value/Effort, Weighted, WSJF, etc.)
- Must show per-project scores on each dimension
- Must show the composite calculation
- Must show the resulting rank order
- If a rank differs from pure score (governance override), state the override rationale

### Portfolio Dashboards

- Must have a generation timestamp
- Must show the data source (FLO roll-up vs. manual entry) per project
- Must flag stale data (>2 weeks since last refresh)
- Must include executive summary (3-5 bullet points) before detail tables
- RAG colors: 🟢 On Track | 🟡 At Risk | 🔴 Off Track | ⚪ No Data

### Dispatch Authorizations

- Must include: Project ID, Priority Rank, Authorization Scope, Constraints, Required Packages
- Must be self-contained — FLO reads only this document, not the full portfolio
- Must reference the governance decision that authorized it (PGD-{NNN})

### Strategic Alignment Map

- Must show organizational objectives (rows) × projects (columns)
- Must show per-cell alignment score
- Must show weighted total per project
- Must highlight low-alignment projects (candidates for retirement)

---

## Cross-Reference Integrity

| When Referencing | Verify |
|---|---|
| A project's budget | Matches the value in PIP (from `pilc-state.md`) |
| A project's health | Matches the latest FLO roll-up (or manual update) |
| A governance decision | PGD-{NNN} exists in `portfolio-decisions/` |
| Strategic objectives | Match the list in `ppm-state.md` |
| Priority rank | Matches `prioritization-scorecard.md` |

---

## Validation Checklist (Run Before Presenting Any Artifact)

- [ ] Portfolio scope (not single-project analysis)
- [ ] No hardcoded project names in templates
- [ ] Provenance front-matter present
- [ ] All data traceable to source (PIP, FLO, user input)
- [ ] Numbers have denominators and scales
- [ ] Projects shown in comparative context
- [ ] Cross-references are valid
- [ ] No `{placeholder}` left unresolved in generated output (only in templates)
- [ ] No `_[TBD]_` left unresolved without flagging to user
- [ ] Governance cadence respected (appropriate frequency for the action)

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

*Apply these rules to every output. They ensure AI-PPM produces governance-grade artifacts, not casual summaries.*

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
