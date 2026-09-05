<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Content Validation

## Purpose

Before creating or saving ANY deliverable file, the AI MUST validate its content against the rules in this document. This ensures all outputs are professional, consistent, complete, and correctly formatted.

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

## Validation Checklist (Apply to Every Deliverable)

### 1. Document Metadata

Every deliverable MUST include:

- [ ] Document title (H1 heading)
- [ ] Project name (generic placeholder `{project_name}` in templates; actual name in generated outputs)
- [ ] Version number
- [ ] Date (ISO format or localized per user preference)
- [ ] Author / Prepared By
- [ ] Status (Draft / Awaiting Approval / Approved / Superseded)
- [ ] Reference to source document or predecessor deliverable

**Validation rule:** If any metadata field is unknown, use `_[TBD]_` or `_[Pending]_` — never leave it blank or omit the field.

---

### 2. Structural Completeness

- [ ] All sections defined in the template are present (even if marked N/A for this project)
- [ ] No orphaned headers (header with no content below it)
- [ ] Tables have consistent column counts (no ragged rows)
- [ ] All numbered lists are sequential (no gaps: 1, 2, 4)
- [ ] Cross-references to other documents use correct file names
- [ ] All placeholder tokens are properly formatted: `_[TBD]_`, `_[Pending]_`, `{variable_name}`

---

### 3. Content Quality

- [ ] No project-specific content in template files (templates must be generic)
- [ ] Generated deliverables reference the source document — never invent scope
- [ ] Recommendations include rationale (never "because it's best practice" without explanation)
- [ ] Quantitative claims have basis stated (even if estimated/assumed)
- [ ] Risk/impact assessments use the defined scoring scales (not ad-hoc language)
- [ ] No contradictions with previously approved deliverables in the same workflow
- [ ] Acronyms defined on first use (or in a glossary section for long documents)

---

### 4. Markdown Formatting

#### Tables

```markdown
<!-- CORRECT: aligned pipes, header separator, consistent columns -->
| Column A | Column B | Column C |
|----------|:--------:|----------|
| Data 1   | Center   | Data 3   |
| Data 2   | Center   | Data 4   |

<!-- INCORRECT: missing separator, ragged columns -->
| Column A | Column B
| Data 1 | Data 2 | Extra |
```

**Rules:**
- Always include the header separator row (`|---|---|`)
- Align pipe characters for readability
- Use `:---:` for center alignment, `---:` for right alignment, only when semantically appropriate
- No empty tables — if no data yet, use a single row with `_[To be populated]_`

#### Headings

- H1 (`#`) — document title only (one per file)
- H2 (`##`) — major sections
- H3 (`###`) — subsections
- H4 (`####`) — sub-subsections (use sparingly)
- Never skip levels (e.g., H1 → H3 with no H2)

#### Lists

- Use `-` for unordered lists (not `*` or `+`)
- Use `1.` for ordered lists (auto-numbered, not manual numbers)
- Nested lists indent by 2 spaces (for Markdown compatibility)
- Lists of 10+ items should be in a table instead

#### Emphasis

- `**bold**` for key terms, field names, and important callouts
- `_italic_` for placeholder values and document references
- `` `code` `` for file paths, technical identifiers, and field values
- Never use ALL CAPS for emphasis

---

### 5. Diagram Validation

If a deliverable includes diagrams (ASCII, Mermaid, or textual):

#### ASCII Diagrams

```
<!-- CORRECT: box-drawing characters, consistent spacing -->
┌──────────────┐     ┌──────────────┐
│   Phase 1    │────►│   Phase 2    │
└──────────────┘     └──────────────┘

<!-- ALSO ACCEPTABLE: simple characters for portability -->
+----------------+     +----------------+
|   Phase 1      |---->|   Phase 2      |
+----------------+     +----------------+
```

**Rules:**
- Use consistent character set within a single diagram (don't mix box-drawing and ASCII)
- Ensure alignment is preserved (monospace assumption)
- Provide a text description below complex diagrams for accessibility
- Keep diagrams under 80 characters wide for terminal/email compatibility

#### Mermaid Diagrams (if platform supports)

```markdown
```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
```​
```

**Rules:**
- Validate syntax before saving (no orphan nodes, closed brackets)
- Always provide a text alternative below the diagram
- Keep diagrams simple — max 15 nodes for readability

---

### 6. Cross-Reference Integrity

When a deliverable references another document:

- [ ] Referenced file exists (or is planned to exist in a future stage)
- [ ] File name matches exactly (case-sensitive)
- [ ] Referenced section/heading exists within the target document
- [ ] Forward references (to not-yet-created documents) are marked: `_[To be produced in Stage {n}]_`

**Format for cross-references:**
- Same folder: `See Feasibility_Assessment.md §3`
- Different folder: `See ../03_Business_Case/Business_Case.md §2`
- Future document: `See Risk_Register.md _[To be produced in Stage 13]_`

---

### 7. Consistency Checks

Before saving, verify consistency with:

| Check Against | What to Verify |
|---------------|---------------|
| Source document | Scope items match; no invented requirements |
| Requirement Intake Form | Stakeholder names consistent; project name matches |
| Decision Log | Decisions referenced in deliverables match logged decisions |
| Previous deliverables | No contradictions in scope, timeline, budget, or priority |
| State file | Stage status is accurate; project metadata matches |

**If inconsistency found:**
1. Flag to user: "I noticed {deliverable A} says X but {deliverable B} says Y. Which is correct?"
2. Do NOT save until resolved
3. Update all affected documents to be consistent
4. Log the correction in Change Log if it changes a previously approved artifact

---

### 8. Placeholder Hygiene

#### Valid placeholder formats

| Format | Usage |
|--------|-------|
| `_[TBD]_` | Value not yet determined; will be filled later |
| `_[Pending]_` | Awaiting approval or external input |
| `_[To be confirmed]_` | Provisional value needing stakeholder validation |
| `{variable_name}` | Template variable (only in template files) |
| `_[See Action A-{nnn}]_` | Linked to a tracked action for resolution |

#### Placeholder tracking

- Every `_[TBD]_` in a final deliverable MUST have a corresponding Action Item
- At Package Assembly (Stage 16), all remaining placeholders are reported as open items
- Templates may contain unlimited placeholders; generated deliverables should minimize them

---

### 9. File Naming Conventions

| Rule | Example |
|------|---------|
| Use Title_Case with underscores | `Business_Case.md` |
| No spaces in file names | ✅ `Risk_Register.md` ❌ `Risk Register.md` |
| Folder names match phase | `08_Risk_Management/` |
| State file is always `pilc-state.md` | Lowercase, hyphenated |
| Management registers use Title_Case | `Decision_Log.md` |
| Drafts marked with suffix | `Business_Case_DRAFT.md` |
| Archived files with timestamp | `pilc-state-20260603T1430.archived.md` |

---

### 10. Sensitive Content

Before saving any file, verify it does NOT contain:

- [ ] Real passwords, API keys, or credentials
- [ ] Personal data beyond professional role information (no home addresses, personal phone numbers)
- [ ] Financial figures marked as confidential by the user
- [ ] Content from the source document marked as restricted

**If user provides sensitive information during the workflow:**
- Store only the minimum necessary for the deliverable
- Use role references instead of names where possible in templates
- Flag to user if a deliverable would contain information they may not want in a shareable document


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

If validation fails on any check:

1. **Do NOT save the file**
2. Identify the specific failure(s)
3. Fix automatically if the fix is unambiguous (e.g., missing separator row in table)
4. Ask user if the fix requires a judgment call (e.g., inconsistency between documents)
5. Re-validate after fix
6. Only save when all checks pass

---

## Template vs. Generated Output Rules

| Rule | Templates | Generated Outputs |
|------|-----------|-------------------|
| Project-specific content | ❌ Never | ✅ Required |
| Placeholder variables `{...}` | ✅ Expected | ❌ Must be resolved |
| `_[TBD]_` markers | ✅ In optional fields | ✅ Only where truly unknown |
| Instructional comments | ✅ Guide the user | ❌ Remove before saving |
| Example data | ✅ Illustrative | ❌ Replace with real data |
| Section markers like `<!-- REMOVE -->` | ✅ For template guidance | ❌ Must be cleaned |

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
