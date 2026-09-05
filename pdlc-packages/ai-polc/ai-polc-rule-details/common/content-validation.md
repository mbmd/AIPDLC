<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-POLC — Content Validation Rules

**Purpose:** Quality rules that every AI-POLC output must satisfy. The AI checks these before presenting any artifact to the user.

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

## Universal Rules (Apply to ALL Outputs)

### 1. Source-Driven Content

Every claim, scope item, or backlog entry MUST trace to one of:
- User's stated requirements (verbal or documented)
- PIP content (from AI-PILC)
- Architecture Package decisions (from AI-ADLC)
- UX research findings (from AI-UXD)
- User's explicit approval during this session

**Never fabricate scope.** If something seems needed but wasn't stated by the user or found in upstream input, flag it as a recommendation — don't silently add it to the backlog.

### 2. Generic — No Project-Specific Hardcoding

When working with **templates** (the package source), content must be 100% generic:
- Use `{placeholder}` for values filled during generation
- Use `_[TBD]_` for values the user provides later
- Zero project names, company names, or domain-specific content

When working with **runtime output** (actual project execution), content IS project-specific — that's the point. But still: derive from user input, never invent.

### 3. Value Justification

Every epic and prioritization decision must have explicit value justification:
- **Epic:** "This epic serves Goal X because {reason}. Without it, {consequence}."
- **Priority position:** "Ranked at position N because {model says X}. Rationale: {one sentence}."
- **Backlog admission:** Nothing enters the backlog without answering "why does this serve the product vision?"

Items without justification are flagged for user review, not silently admitted.

### 4. Acceptance Criteria Quality

All acceptance criteria (epic-level in Tier 1, story-level in Tier 2) must be:
- **Testable:** Someone can unambiguously determine pass/fail
- **Specific:** No "the system should work well" — measurable or observable
- **Independent of implementation:** Describe the WHAT, not the HOW

**Tier 1 (epic AC):** May be broader — "All 3 payment providers integrated and passing health checks" is acceptable at epic level.
**Tier 2 (story AC):** Must be Given/When/Then format — "Given a user with valid credentials, When they submit payment via Stripe, Then a confirmation email is sent within 5 seconds."

### 5. Traceability Links

Every artifact must maintain its traceability chain:
- **Epic → Goal:** Which product goal does this epic serve?
- **Epic → Release:** Which release is this epic sliced into?
- **Epic → Priority:** What position in the prioritization register?
- **DoR/DoD → Epic:** Which epics does this quality bar apply to?

If a link is missing, flag it before presenting the artifact.

### 6. Terminology Consistency

Within a single PBP:
- One term for each concept (don't alternate between "user story" and "requirement" and "feature")
- Priority model vocabulary used consistently (if WSJF, always use "cost of delay" and "job duration" — don't switch to MoSCoW terms mid-document)
- Epic naming convention consistent (if using `EPIC-NNN_{name}`, every epic follows that pattern)

### 7. Provenance Front-Matter

Every generated `.md` file must include:

```yaml
---
generatedBy: AI-POLC
generatedVersion: 1.0.0
source: {upstream-doc-path or "user-input"}
generatedOn: {ISO-date}
ownership: generated | hybrid | user
---
```

---

## Per-Artifact Rules

### Product Vision

- [ ] One sentence that passes the "a stranger can understand the product's purpose" test
- [ ] Measurable goals (not aspirational — each goal has a success metric)
- [ ] Time-bounded where appropriate (OKR cadence stated)
- [ ] Aligned to PIP business objectives (if PIP available)

### Epic Definitions

- [ ] Clear name (action-oriented: "Enable multi-currency payments" not "Payments")
- [ ] Goal linkage explicit
- [ ] Epic-level acceptance criteria (testable, boundary-defining)
- [ ] No implementation prescription (says WHAT, not HOW)
- [ ] Estimated complexity tier (S/M/L/XL) if methodology supports it

### Prioritization Register

- [ ] Model stated explicitly (WSJF / MoSCoW / value-effort / custom)
- [ ] Every ranked item has rationale (one sentence minimum)
- [ ] No duplicate rankings (each position is unique)
- [ ] Re-prioritization history visible (previous position, if changed)

### Release Plan

- [ ] Each release has: name/number, goal alignment, epic list, readiness criteria
- [ ] MVP scope clearly bounded (what's IN vs. what's explicitly OUT)
- [ ] Releases are ordered and time-hinted (even if rough: "Q3" / "Sprint 4-6")
- [ ] No orphan epics (every prioritized epic appears in exactly one release)

### DoR / DoD Checklists

- [ ] Each item is a verifiable checkbox (can answer yes/no)
- [ ] No vague items ("adequate" is not verifiable — "reviewed by PO" is)
- [ ] DoR and DoD are distinct (DoR = before dev starts; DoD = before increment ships)
- [ ] Appropriate for stated depth (Minimal DoR has 3-5 items; Comprehensive has 8-12)

### Governance Spine Entries

- [ ] ID follows `POLC-{TYPE}-{NNN}` format
- [ ] Phase column = "POLC" or "AI-POLC"
- [ ] Date in ISO format
- [ ] Status column present (Open / Closed / Superseded)
- [ ] Never edits another phase's entries

---

## Depth-Adapted Quality Bar

| Aspect | Minimal | Standard | Comprehensive |
|--------|---------|----------|---------------|
| Epic count | 3-8 | 5-15 | 10-30+ |
| AC per epic | 2-3 | 3-5 | 5-8 |
| Rationale depth | One sentence | Paragraph with model reference | Full analysis with alternatives considered |
| Risk items | 3-5 | 5-10 | 10-20 with scoring |
| Traceability | Goal→Epic only | Goal→Epic→Release | Goal→Epic→Story→AC→Release→Outcome |
| Stakeholder map | Names + interest level | Full power/interest matrix | Matrix + communication plan + cadence |

---

## Validation Checklist (Run Before Presenting Any Major Artifact)

Before presenting a stage output to the user, verify:

- [ ] Source-driven (nothing fabricated)
- [ ] Value-justified (nothing admitted without rationale)
- [ ] Traceable (links maintained up and down)
- [ ] Terminology consistent (no mixed vocabulary)
- [ ] Depth-appropriate (not over-engineering for minimal, not thin for comprehensive)
- [ ] Provenance header present
- [ ] No implementation prescription (WHAT, not HOW)
- [ ] Acceptance criteria are testable
- [ ] Governance spine entries properly formatted

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

*Reference this file when producing any output. Run the validation checklist at every stage gate.*

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
