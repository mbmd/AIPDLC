<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-ILC — Content Validation

**Purpose:** Quality rules for all artifacts AI-ILC produces. Every output must pass these checks before being finalized and presented to the user.

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

## Validation Checklist (Apply to Every Output)

Before presenting any artifact to the user, verify:

### Completeness
- [ ] All required sections present (per the relevant template)
- [ ] No `{placeholder}` values left unfilled (unless marked `_[TBD]_` for user's later input)
- [ ] All referenced decisions exist in the Decision Log
- [ ] State file is current (reflects this stage's completion)

### Accuracy
- [ ] All claims trace back to user-provided input or documented decisions
- [ ] No invented scope, features, or requirements — only what the user stated or confirmed
- [ ] Score rationale references actual content from shaping (not generic statements)
- [ ] Routing decision is supported by the impact assessment answers

### Consistency
- [ ] Idea name matches across all artifacts (state file, register, briefs, decisions)
- [ ] Depth level matches what was agreed at capture (or explicitly adjusted at a gate)
- [ ] No contradiction between evaluation findings and scope decisions
- [ ] Decision Log numbering is sequential with no gaps

### Formatting
- [ ] Markdown renders correctly (headers, tables, lists)
- [ ] Tables have consistent column alignment
- [ ] No broken links or file references
- [ ] Question numbers follow Q-{nn} convention
- [ ] Decision numbers follow D-{nn} convention

### Tone & Voice
- [ ] Content matches the stage's assigned persona voice (see persona map in core-workflow)
- [ ] Professional but accessible — not academic, not casual
- [ ] Value-first framing (lead with what matters, details follow)
- [ ] Actionable language ("do X" rather than "it is recommended that X be done")

---

## File Naming Convention

Shared artifacts use fixed names and stay flat at `{output_root}/`. Per-idea artifacts live inside the idea's subfolder `{NNN}-{idea-slug}/` and are prefixed with the same `{NNN}-{idea-slug}_` stem (see `core-workflow.md` → "MANDATORY: Output Folder Structure").

| Artifact | Location | Filename Pattern | Example |
|----------|----------|-----------------|---------|
| State file | `{output_root}/` | `ilc-state.md` | `ilc-state.md` (fixed name) |
| Idea Register | `{output_root}/` | `Idea_Register.md` | `Idea_Register.md` (fixed name) |
| Decision Log | `{output_root}/management_framework/` | `Decision_Log.md` | `Decision_Log.md` (fixed name) |
| Idea Statement | `{NNN}-{idea-slug}/` | `Idea_Statement.md` | `001-mobile-app/Idea_Statement.md` |
| Go/No-Go Record | `{NNN}-{idea-slug}/` | `{NNN}-{idea-slug}_GoNoGo_Decision_Record.md` | `001-mobile-app/001-mobile-app_GoNoGo_Decision_Record.md` |
| Approved Idea Brief | `{NNN}-{idea-slug}/` | `{NNN}-{idea-slug}_Approved_Idea_Brief.md` | `001-mobile-app/001-mobile-app_Approved_Idea_Brief.md` |
| Change Request Brief | `{NNN}-{idea-slug}/` | `{NNN}-{idea-slug}_Change_Request_Brief.md` | `001-mobile-app/001-mobile-app_Change_Request_Brief.md` |
| Feature Brief | `{NNN}-{idea-slug}/` | `{NNN}-{idea-slug}_Feature_Brief.md` | `001-mobile-app/001-mobile-app_Feature_Brief.md` |

**Idea folder/slug rules:**
- `{NNN}` = the idea's Register ID, zero-padded to 3 digits (`001`, `002`, …) — a stable key, never reused, never changed for status
- `{idea-slug}` = idea title lower-cased, spaces → hyphens, special characters stripped (`Mobile App` → `mobile-app`)
- Keep the slug short but recognizable (3-4 words max), derived from the title confirmed at Capture
- The artifact-type suffix (`_Approved_Idea_Brief`, etc.) keeps its underscore form for readability

---

## Content Rules by Artifact

### Idea Register Entry
- One row per idea — never split an idea across rows
- Status must be a valid value from the state transition table
- Score column stays empty until Evaluate completes
- Route column stays empty until Route & Handoff completes

### Decision Log Entry
- Every entry has: ID, date, question reference, decision, rationale
- Rationale is mandatory — never log a bare decision without "why"
- Include who decided (user confirmed vs. AI recommended + user accepted)

### Go/No-Go Decision Record
- Must be produced for ALL outcomes (approve, park, reject) — not just approvals
- Includes: idea summary, score, key risks, decision, rationale, conditions (if any), next step
- Parked ideas must have a revisit date
- Rejected ideas must have a clear "why not" that someone else could read and understand

### Briefs (Approved Idea / Change Request / Feature)
- Must carry forward ALL context from shaping + evaluation + scope
- Zero information loss at handoff — the successor never starts cold
- Must be self-contained: readable without needing to open the state file or register
- Must explicitly state the routing destination and why

---

## Depth-Specific Quality Expectations

| Depth | Content Length | Detail Level | Iteration |
|-------|:-------------:|:------------:|:---------:|
| **Minimal** | Concise (1-2 pages per brief) | Essentials only — problem, value, scope, decision | Single pass (present once, user approves) |
| **Standard** | Moderate (2-4 pages per brief) | Full structured content with rationale at each section | One iteration (present, collect feedback, finalize) |
| **Comprehensive** | Detailed (4-6 pages per brief) | Deep analysis, multiple perspectives, explicit trade-offs | Multiple iterations (draft → feedback → revise → finalize) |

---

### Contextual Prose Accompaniment (CPA)

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

If any check fails:

1. **Do NOT present the artifact to the user yet**
2. Fix the issue silently (if it's a formatting or consistency error the AI can resolve)
3. If it requires user input to resolve (e.g., missing decision), ask the specific question
4. Re-validate after fix
5. Only present when all checks pass

**Never ship an incomplete artifact with "I'll fix this later."** Every output is final when presented.

---

## Cross-Reference Integrity

When an artifact references another artifact or decision:

| Reference Type | Validation Rule |
|----------------|----------------|
| "As decided in Q-03..." | Verify Q-03 exists in the Decision Log with that answer |
| "Score: 28/35" | Verify the score in the state file matches |
| "Per the scope definition..." | Verify scope was actually defined (Stage 4 completed) |
| "Route: New Project" | Verify ilc-state.md Route field matches |
| "See Idea Register" | Verify the idea has an entry with matching status |

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Produce content the user didn't ask for | AI-ILC is governed, not generative-at-will |
| Fill in `_[TBD]_` fields without asking | Those are explicitly user-provided-later markers |
| Use vague rationale ("it seems good") | Every rationale must reference specific evidence |
| Leave the state file stale | State must always reflect the latest completed stage |
| Produce briefs with generic/boilerplate sections | Every section must be specific to THIS idea |
| Ignore depth level | Minimal ≠ shorter Standard; it's a genuinely different interaction model |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*

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
