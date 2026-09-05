<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Content Validation

## Purpose

Before creating or saving ANY test governance artifact, AI-TGE MUST validate its content against the rules in this document. Test governance artifacts have specific quality requirements — they must be traceable, risk-scored, and consistent with the architecture they govern.

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

## Validation Checklist (Apply to Every TGE Output)

### 1. Document Metadata

Every TGE output document MUST include:

- [ ] Document title (H1 heading)
- [ ] Document type (Strategy / Register / Coverage Report / Debt Scorecard / Defect Log)
- [ ] Generation timestamp (ISO 8601)
- [ ] Engine version (AI-TGE v1.0.0)
- [ ] Mode active when generated (Full Chain / Architecture Only / Brownfield / Observation Only)
- [ ] Depth level (Minimal / Standard / Comprehensive)

**Format:**
```markdown
# {Document Title}

**Type:** {Strategy / Register / Coverage Report / Debt Scorecard / Defect Log}
**Generated:** {YYYY-MM-DDTHH:MM:SSZ}
**Engine:** AI-TGE v1.0.0
**Mode:** {Full Chain / Architecture Only / Brownfield / Observation Only}
**Depth:** {Minimal / Standard / Comprehensive}
```

---

### 2. Traceability Checks

Every test requirement in the register MUST be traceable to a source:

| Check | What to Verify |
|-------|---------------|
| Source field populated | Every register entry has Source = Architecture / Baseline / Story / Manual / Reconciliation |
| Commitment ID links to real artifact | If Source = Architecture, the referenced AP artifact must exist |
| Baseline ID is valid | If Source = Baseline, the ID must match a rule in `two-source-model.md` |
| Story ID is valid | If Source = Story, the referenced story file must exist in aidlc-docs |
| Manual entries have rationale | If Source = Manual, a user-provided rationale must be present |
| No orphan entries | Every entry links to something; no "floating" requirements with no origin |

**If traceability fails:**
1. Flag to user: "Register entry {ID} has no valid source link. Was this derived from {X}?"
2. Do NOT include in coverage calculations until resolved
3. Mark as `Source: Unresolved` temporarily

---

### 3. Risk Score Validation

Every register entry with Status = Missing MUST have a valid risk score:

| Check | What to Verify |
|-------|---------------|
| All 4 factors scored | Architectural Risk × Blast Radius × Logic Complexity × Change Frequency |
| Each factor 1-5 | No factor outside the 1-5 range |
| Composite calculated correctly | Product of 4 factors (not sum) |
| Bucket assigned correctly | 400-625 = Critical, 150-399 = High, 50-149 = Medium, 1-49 = Low |
| Rationale provided for scores ≥4 | Any factor scored 4 or 5 must have a brief justification |

**Scoring integrity rules:**
- Never score ALL factors at 5 without justification (625 is the maximum — reserved for genuinely critical gaps)
- Never score ALL factors at 1 (if truly all-1, question whether the test is needed at all)
- Architectural Risk should be highest for: auth, data integrity, core business logic
- Blast Radius should be highest for: shared components, platform layers, API gateways
- Logic Complexity should be highest for: state machines, algorithms, concurrent operations
- Change Frequency should be highest for: actively developed code, feature-flagged areas

---

### 4. Classification Consistency

Every register entry must follow the taxonomy defined in `test-taxonomy.md`:

| Check | What to Verify |
|-------|---------------|
| Test Level valid | Must be one of: Unit / Integration / System / Acceptance |
| Test Type valid | Must be one of: Functional / Non-Functional / Structural |
| Sub-Type valid | Must match a sub-type under the chosen Type (see taxonomy) |
| Level matches scope | Unit = isolated; Integration = cross-boundary; System = full stack; Acceptance = business value |
| Type matches focus | Functional = correctness; Non-Functional = quality attribute; Structural = internal quality |
| No level/type mismatch | e.g., "Unit + Non-Functional + Performance" is invalid (performance requires system scope) |

**Common misclassification patterns to catch:**

| Wrong | Correct | Why |
|-------|---------|-----|
| Unit + Performance | System + Performance | Performance requires realistic load conditions (not isolated) |
| Acceptance + Security | System + Security | Security tests verify system-level controls, not user-facing business value |
| Unit + Contract | Integration + Contract | Contracts are between components (by definition cross-boundary) |
| Integration + Business Logic | Unit + Business Logic | Pure business rules are tested in isolation (no dependency needed) |
| System + Boundary | Unit + Boundary | Boundary/edge cases are best caught at the unit level |

---

### 5. Register Consistency Checks

The test register must be internally consistent:

| Check | What to Verify |
|-------|---------------|
| No duplicate entries | Same commitment + same test name = duplicate (merge or remove) |
| Status values valid | Required / Exists / Missing / Failing / Deprecated / Overridden |
| Deprecated entries excluded from coverage | Coverage % uses only active entries (not deprecated/overridden) |
| Commitment IDs unique per source | No two entries from the same AP artifact share the same commitment ID |
| Missing tests have risk scores | Every Missing entry has a valid composite risk score |
| Existing tests have verification note | How was existence confirmed? (file path, test name match, etc.) |

---

### 6. Coverage Report Validation

Coverage reports must be mathematically correct and multi-dimensional:

| Check | What to Verify |
|-------|---------------|
| Percentage calculation correct | Coverage = (Tests Existing / Tests Required) × 100 — exclude Deprecated and Overridden |
| Multiple views present | By commitment, by component, by test type, by risk level (minimum 3 views for Standard+) |
| No 100% claim without verification | If claiming 100% coverage on a commitment, every derived test must have Status = Exists |
| Gap identification specific | Don't say "coverage is low" — say "API-USERS endpoint missing contract tests for 3/5 error codes" |
| Trend data included (if prior reports exist) | Show delta: "Coverage improved from 42% → 58% since last report" |

---

### 7. Strategy Document Validation

The test strategy must be complete and actionable:

| Check | What to Verify |
|-------|---------------|
| Test pyramid ratios defined | Unit : Integration : System : Acceptance percentages |
| Test types relevant to project | Only include types that apply (don't list "Accessibility tests" if no UI exists) |
| Tools/frameworks identified | From DW tech stack — not invented (use what the workspace provides) |
| Coverage goals per level | Specific targets, not vague ("≥80% unit coverage" not "good coverage") |
| Entry/exit criteria defined | What must be true before tests can run; what must be true after |
| Test data strategy addressed | How test data is created, managed, and cleaned up |
| Automation approach stated | Which tests are automated vs. manual (and why) |

---

### 8. Defect Log Validation

Every defect entry must be complete:

| Check | What to Verify |
|-------|---------------|
| Defect ID unique and sequential | DEF-001, DEF-002, ... — no gaps, no duplicates |
| Severity assigned | Critical / High / Medium / Low |
| Category assigned | Functional / Performance / Security / Data / Integration |
| Linked Component present | Which architectural component is affected |
| Status valid | Open / Investigating / Fixed / Verified / Closed |
| Root Cause populated (when known) | Once investigation completes, root cause must be documented |
| Linked Test noted | Which test caught it, OR "manual discovery" if found outside testing |

---

### 9. Architecture Alignment

TGE outputs must be consistent with the Architecture Package they govern:

| Check | What to Verify |
|-------|---------------|
| Component names match AP exactly | If AP says "UserService" — register says "UserService" (not "User Service" or "users") |
| API endpoint paths match | If AP defines `POST /api/v1/users` — register uses the same path |
| ADR references valid | If citing ADR-003 — that ADR must exist in the AP |
| Integration names match | External system names consistent between AP and register |
| NFR values match | If AP says "p95 ≤ 200ms" — strategy/register uses the same target |
| Tech stack references accurate | Testing frameworks mentioned must match what DW actually provides |

**If misalignment found:**
1. Flag to user: "Register uses '{X}' but AP defines '{Y}'. Which is current?"
2. Update register to match AP (AP is authoritative for architecture naming)
3. If AP itself is wrong, recommend user update AP first, then reconcile

---

### 10. Depth Level Compliance

Output detail must match the active depth level:

| Artifact | Minimal | Standard | Comprehensive |
|----------|---------|----------|---------------|
| Test Strategy | 1-2 page summary; pyramid ratios; tool list | Full strategy; all sections from validation §7 | + detailed test data strategy; automation roadmap; environment plan |
| Test Register | Commitment + test name + status + source | + risk score + level/type + linked component | + detailed assertions + test preconditions + data requirements |
| Coverage Report | Single percentage + gap list | Multi-view (3+ dimensions) + trend | + traceability matrix + heat map by component + historical trend |
| Debt Scorecard | Risk buckets with counts | + individual scoring per missing test | + remediation suggestions + effort estimates + sprint mapping |
| Defect Log | Basic fields (ID, severity, status) | + linked component + root cause | + timeline + linked tests + regression prevention note |

---

### 11. Naming Conventions

| Rule | Example |
|------|---------|
| TGE output folder | `.governance/test/` (dotfolder, lowercase) |
| State file | `tge-state.md` (lowercase, hyphenated) |
| Strategy file | `test-strategy.md` (lowercase, hyphenated) |
| Register file | `test-register.md` (lowercase, hyphenated) |
| Coverage report | `coverage-report.md` (lowercase, hyphenated) |
| Debt scorecard | `debt-scorecard.md` (lowercase, hyphenated) |
| Defect log | `defect-log.md` (lowercase, hyphenated) |
| Commitment IDs | `{CATEGORY}-{NNN}` (e.g., API-001, SEC-003, DATA-012) |
| Baseline IDs | `BASE-{CATEGORY}-{NN}` (e.g., BASE-API-01, BASE-SEC-02) |
| Defect IDs | `DEF-{NNN}` (e.g., DEF-001, DEF-042) |
| Story references | `STORY-{ID}-AC{N}` (e.g., STORY-012-AC3) |

---

### 12. Placeholder Hygiene

TGE outputs should have MINIMAL placeholders — the engine derives content from existing sources:

| Acceptable Placeholders | Context |
|------------------------|---------|
| `_[Pending AP reconciliation]_` | AP changed but reconciliation not yet run |
| `_[Test existence unverified — scan needed]_` | Brownfield detected but not yet assessed |
| `_[Risk score pending — requires depth ≥ Standard]_` | Depth is Minimal; risk scoring not active |
| `_[Root cause: investigating]_` | Defect logged but root cause not yet determined |

**Unacceptable in TGE outputs:**
- `_[TBD]_` without explanation (must say why it's pending)
- Placeholder for a test requirement (either derive it or don't include it)
- Empty risk scores on Missing entries (if Missing → must be scored)
- Blank commitment IDs (every entry must be identified)

---

### 13. Contextual Prose Accompaniment (CPA)

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

| Failure Type | Action |
|-------------|--------|
| Traceability broken | Alert user; mark entry as `Source: Unresolved`; exclude from coverage |
| Risk score invalid | Recalculate from factors; if factors missing, prompt user for assessment |
| Classification mismatch | Correct automatically if clear (e.g., Unit+Performance → System+Performance); flag if ambiguous |
| Duplicate entries | Merge (keep the one with more detail); alert user |
| AP alignment drift | Flag specific mismatches; update register to match current AP |
| Coverage math wrong | Recalculate from register data (register is source of truth) |
| Depth violation | Either upgrade output detail OR explain why depth was reduced |
| Missing metadata | Add metadata from state file (engine always knows current mode/depth/version) |

---

## Cross-Artifact Consistency

When multiple TGE artifacts reference each other:

| Reference | Source of Truth |
|-----------|----------------|
| Register entry count | `test-register.md` (actual entries counted) |
| Coverage percentage | Calculated from register (Exists / Required) |
| Risk score | `debt-scorecard.md` (latest scoring) |
| Defect count by severity | `defect-log.md` (actual entries counted) |
| Strategy tools/frameworks | `test-strategy.md` (derived from DW tech stack) |
| State statistics | Recalculated from artifacts (never manually maintained) |

**Rule:** State file statistics are DERIVED from artifacts, not the other way around. If state says "Coverage: 58%" but register calculation shows 62%, update state (register is authoritative).

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
