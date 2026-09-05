<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Content Validation

## Purpose

Before creating or saving ANY architecture document, the AI MUST validate its content against the rules in this document. Architecture documents have additional quality requirements beyond standard document formatting — they must be technically consistent, constraint-compliant, and diagrammatically correct.

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

## Validation Checklist (Apply to Every Architecture Document)

### 1. Document Metadata

Every architecture document MUST include:

- [ ] Document title (H1 heading)
- [ ] Document status (Draft / Review / Approved)
- [ ] Version number
- [ ] Date
- [ ] Author role (e.g., "CTO", "Architecture Lead")
- [ ] System/project name

**Format:**
```markdown
# {Document Title}

**Document Status:** {Draft / Review / Approved}
**Version:** {n.n}
**Date:** {YYYY-MM-DD}
**Author:** {Role}
```

---

### 2. Architectural Consistency Checks

Before saving any document, verify it is consistent with:

| Check Against | What to Verify |
|---------------|---------------|
| Architecture Principles (Stage 3) | No recommendation contradicts a defined principle |
| Constraints (Stage 3) | No technology or pattern violates a constraint |
| System Context (Stage 4) | External systems referenced exist in C4 L1 |
| Container list (Stage 5) | Containers referenced match those defined in C4 L2 |
| Technology Stack (Stage 6) | Technologies mentioned match the selected stack |
| ADRs | Decisions in documents match accepted ADR decisions |
| Previous documents | No contradictions with earlier approved artifacts |

**If inconsistency found:**
1. Flag to user: "This recommendation conflicts with {Principle Pn / Constraint Cn / ADR-nnn}. Should I adjust?"
2. Do NOT save until resolved
3. If user overrides a principle → log in Architecture Workbook as a principle revision candidate

---

### 3. Constraint Compliance Gate

CRITICAL: Every architectural recommendation MUST pass a constraint check:

```
For each recommendation:
  For each constraint in state file:
    Does this recommendation violate this constraint?
    If YES → DO NOT RECOMMEND. Find an alternative that complies.
    If MAYBE → Flag to user with explanation.
    If NO → Proceed.
```

**Common constraint violations to catch:**
- Recommending a cloud-managed service when "on-premises only" is a constraint
- Recommending a commercial/proprietary tool when "open-source only" is a constraint
- Recommending a pattern that can't meet stated performance targets
- Recommending a technology the team doesn't have skills for (without acknowledging the gap)

---

### 4. Diagram Validation

Architecture documents heavily use diagrams. All diagrams must be validated.

#### C4 Diagrams (Mermaid)

```markdown
```mermaid
C4Context
    title {System Name} — System Context
    Person(user, "User", "Description")
    System(sys, "System", "Description")
    System_Ext(ext, "External", "Description")
    Rel(user, sys, "Uses", "HTTPS")
```​
```

**C4 validation rules:**
- [ ] Every Person/System has a description
- [ ] Every Relationship has a label and protocol/technology
- [ ] System names match those defined in earlier C4 levels
- [ ] No orphan nodes (everything has at least one relationship)
- [ ] Title matches the document context
- [ ] Boundary boxes used for grouping where appropriate

#### ASCII Diagrams (Alternative)

```
┌──────────────────┐         ┌──────────────────┐
│   Component A    │────────►│   Component B    │
│   (NestJS API)   │  REST   │   (PostgreSQL)   │
└──────────────────┘         └──────────────────┘
```

**ASCII diagram rules:**
- [ ] Consistent character set (box-drawing OR simple +/- characters — don't mix)
- [ ] Technology labels on boxes
- [ ] Protocol/pattern labels on arrows
- [ ] Under 100 characters wide
- [ ] Text description provided below for accessibility

#### Diagram Consistency Across Documents

- [ ] C4 L2 containers must be a subset of what's inside C4 L1 system boundary
- [ ] C4 L3 components must exist within a C4 L2 container
- [ ] Technology labels on diagrams match ADR decisions
- [ ] External system names consistent across all diagrams

---

### 5. ADR Validation

Every ADR file must:

- [ ] Follow the template structure (Context, Drivers, Options, Decision, Rationale, Consequences)
- [ ] Have a unique sequential number (no gaps, no duplicates)
- [ ] Have a status (Proposed / Accepted / Deprecated / Superseded)
- [ ] List at least 2 options that were genuinely considered
- [ ] Include both positive AND negative consequences
- [ ] Reference the decision drivers that justified the choice
- [ ] Be cross-referenced in the parent architecture document
- [ ] Be registered in the state file ADR register

---

### 6. Technical Accuracy

Architecture documents must be technically sound:

| Check | What to Verify |
|-------|---------------|
| **Technology names** | Correct spelling, correct version numbers, official names (not nicknames) |
| **Protocol references** | Correct protocol names (REST, gRPC, AMQP, not "API calls") |
| **Port numbers** | Standard ports cited correctly (5432 for PostgreSQL, 6379 for Redis, etc.) |
| **License claims** | If claiming "MIT licensed" — verify it's actually MIT (not MIT-0, not Apache, not AGPL) |
| **Performance claims** | If citing benchmarks, qualify with "under typical conditions" or reference source |
| **Ecosystem claims** | If claiming "largest ecosystem" or "most popular" — be accurate or hedge |
| **Version currency** | Recommend current/LTS versions, not outdated ones |

---

### 7. Completeness Per Document Type

#### Architecture Vision Document
- [ ] Vision statement present (1-2 sentences)
- [ ] Principles listed with ID, name, statement, and rationale
- [ ] Constraints table with source and impact
- [ ] Quality attributes with priority levels
- [ ] Stakeholder concerns mapping

#### C4 Diagrams (L1, L2, L3)
- [ ] Diagram present (Mermaid or ASCII)
- [ ] Every element described in a table below the diagram
- [ ] Relationships documented with technology/protocol
- [ ] Narrative explanation accompanies the diagram

#### Technology Stack Document
- [ ] Every container has technology selected
- [ ] Each selection has rationale (even if brief)
- [ ] Key selections reference their ADR
- [ ] Alternatives considered (at least mentioned)
- [ ] Stack compatibility verified (no conflicting choices)

#### Security Architecture
- [ ] Authentication methods defined
- [ ] Authorization model defined
- [ ] Encryption (at rest + in transit) specified
- [ ] Audit logging approach defined
- [ ] OWASP Top 10 considerations addressed (at minimum acknowledged)

---

### 8. Cross-Reference Integrity

When an architecture document references another:

- [ ] Referenced document exists (or is planned in a future stage)
- [ ] ADR numbers cited exist in the ADR folder
- [ ] Principle IDs (P1, P2, etc.) match those in the Vision document
- [ ] Constraint IDs (if used) match state file
- [ ] Container names match C4 L2 exactly (case-sensitive)
- [ ] Component names match C4 L3 exactly

**Format for references:**
- Same folder: `See 04_Technology_Stack.md`
- ADR reference: `See ADR/ADR-001_Technology_Stack.md`
- Principle reference: `(Principle P3: {name})`
- Future document: `_[To be detailed in Stage {n}]_`

---

### 9. File Naming Conventions

| Rule | Example |
|------|---------|
| Numbered documents: 2-digit prefix | `01_Architecture_Vision.md` |
| ADRs: ADR-{NNN}_{Title} | `ADR-001_Technology_Stack.md` |
| Underscores for spaces | `Security_Identity_Architecture.md` |
| No spaces in file names | ✅ `Data_Architecture.md` ❌ `Data Architecture.md` |
| State file lowercase hyphenated | `adlc-state.md` |
| Workbook title case | `Architecture_Workbook.md` |
| Drafts marked | `03_Container_Diagram_DRAFT.md` |

---

### 10. Placeholder Hygiene

Architecture documents should have fewer placeholders than PMO documents (because the architect IS making the decisions), but some are acceptable:

| Acceptable Placeholders | Context |
|------------------------|---------|
| `_[To be detailed in Stage {n}]_` | Forward reference to a future stage |
| `_[Pending team input]_` | Requires developer team consultation |
| `_[TBD — depends on ADR-{nnn}]_` | Blocked by an upstream decision |
| `_[Performance target: validate in load test]_` | Architecture assumption to be verified |

**Unacceptable in architecture documents:**
- `_[TBD]_` without explanation (must say WHY it's TBD)
- Placeholder for a technology choice (the CTO must decide, not defer)
- Placeholder for a pattern (the architect must choose)

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

## Validation Failure Handling

If validation fails:

1. **Constraint violation:** DO NOT save. Alert user. Propose compliant alternative.
2. **Diagram syntax error:** Fix automatically if unambiguous. Re-validate.
3. **Cross-reference mismatch:** Alert user. Ask which document is authoritative.
4. **ADR inconsistency:** Flag the conflict. Ask if earlier ADR should be superseded.
5. **Technical inaccuracy:** Correct silently if factual (e.g., wrong port number). Flag if judgment-based.

---

## Architecture Document vs. PMO Document Rules

| Rule | Architecture Docs | PMO Docs (AI-PILC) |
|------|------------------|---------------------|
| Placeholders allowed? | Minimal — architect decides | More acceptable — decisions may be pending |
| Diagrams required? | Yes — at least one per stage | Optional |
| ADR cross-references? | Required for major decisions | N/A |
| Technical specificity? | High — name specific technologies, versions, patterns | Low — high-level statements |
| Constraint checking? | Mandatory on every recommendation | Applies to scope only |

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
