<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under the Apache License, Version 2.0. See LICENSE. Attribution required - see NOTICE. -->

# PDLC Family Convention — Contextual Prose Accompaniment (CPA)

> **Family-level convention — authored once, referenced by every PDLC package** (sibling to `reference-linking.md` / `content-validation.md`). Load at workflow start. Applies to every artifact a PDLC package writes into `pdlc-ws/`.

## Why this exists

A reader opens a `pdlc-ws/` artifact and encounters cross-reference keys — codes, IDs, `See …` pointers, provenance stamps. The keys are correct and clickable (per `reference-linking.md`). But the surrounding prose is terse: `(See ADR-003)` or `derivedFrom: IDEA-014` tells the reader *where* to look but not *what they'll find* or *why it matters here*.

**The rule fixes that:** whenever a package writes explanatory text that includes or surrounds a cross-reference key, the prose must be **self-sufficient at a glance** — a human reader understands the reference's meaning and relevance without opening another file.

This complements reference-linking: that convention makes codes *clickable*; CPA makes the surrounding prose *readable*.

---

## Core Principles

1. **Keys are sacred** — never eliminate, shorten, relocate, or paraphrase a cross-reference key.
2. **Context accompanies, never replaces** — explanatory text is additive, appearing alongside the key.
3. **Self-sufficient at a glance** — one sentence (or qualifier phrase) of context is the minimum.
4. **Proportional to depth** — Minimal depth gets shorter context; Comprehensive gets richer.
5. **Pattern-based** — every context addition follows one of the 5 patterns below.

---

## The 5 Patterns

### Pattern A — Inline Context Phrase (registers and tables)

**When:** A table cell contains a cross-reference key or `See …` pointer.

**Action:** Add a qualifier phrase to the cell that tells the reader *what* the referenced content says in context.

**Word limits (depth-scaled):**
- Minimal: ≤ 12 words
- Standard: ≤ 25 words
- Comprehensive: ≤ 50 words

**Example (Standard depth):**

```markdown
<!-- BEFORE (bare ref): -->
| R-003 | Integration risk | High | See Business_Case.md §4 |

<!-- AFTER (CPA-compliant): -->
| R-003 | Integration risk — legacy ERP has no documented API, increasing integration uncertainty | High | [Business_Case.md §4](../03_Business_Case/Business_Case.md) — cost-impact quantified at {currency} {amount} |
```

---

### Pattern B — Contextual Sentence (narrative sections)

**When:** Narrative prose contains a `See …` pointer or bare file-path reference.

**Action:** Precede or follow the reference with a sentence stating the *conclusion or key fact* the reader would find at that reference.

**Scale:**
- Minimal: single qualifier phrase (not a full sentence)
- Standard: 1 contextual sentence
- Comprehensive: 1–2 sentences with specifics (numbers, dates, thresholds)

**Example (Standard depth):**

```markdown
<!-- BEFORE: -->
The feasibility assessment scored 78/100 (See Feasibility_Assessment.md).

<!-- AFTER: -->
Feasibility scored **78/100** ({feasibility_level} — above the {threshold} threshold),
confirming technical viability within stated constraints
(See [Feasibility Assessment §3](../04_Feasibility/Feasibility_Assessment.md)).
```

---

### Pattern C — Front-Matter Context Block (state files)

**When:** A state file carries provenance keys (`derivedFrom`, `projectId`, `originType`).

**Action:** Add an HTML comment block below the YAML front-matter that translates machine keys into a human summary.

**Scale:**
- Minimal: omitted (state file stays machine-terse)
- Standard: 2-line comment block
- Comprehensive: 3–4 line comment block with full provenance trail

**Example (Standard depth):**

```yaml
---
derivedFrom: IDEA-014
projectId: PRJ-CRM-2026-001
originType: project
---

<!-- Provenance context:
  - Originated from IDEA-014: "{idea_title}" — approved at gate on {date}.
  - PRJ-CRM-2026-001 threads this entity through the full family chain.
-->
```

---

### Pattern D — Cross-Reference Summary Block (assembled package READMEs)

**When:** An assembled package README lists downstream consumers.

**Action:** Present as a Consumer / What It Reads / Why It Matters table.

**Scale:**
- Minimal: bullet list (existing format acceptable)
- Standard+: full 3-column table

**Example (Standard depth):**

```markdown
## How to Use This Package

| Consumer | What It Reads | Why It Matters |
|----------|---------------|----------------|
| **{downstream_pkg}** | [{artifact}](./{file}) | {one sentence explaining downstream impact without this input} |
```

---

### Pattern E — Decision Reference Expansion (architecture and strategy docs)

**When:** Narrative text references an ADR or formal decision record.

**Action:** Include (a) the decision's title, (b) a brief rationale summary, and (c) the clickable link.

**Scale:**
- Minimal: title + link only (no rationale)
- Standard: title + ≤ 15-word rationale + link
- Comprehensive: title + rationale + alternatives-rejected summary + link

**Example (Standard depth):**

```markdown
<!-- BEFORE: -->
Selected PostgreSQL over DynamoDB (see ADR-003).

<!-- AFTER: -->
Selected **PostgreSQL** over DynamoDB — team's SQL expertise and relational-query needs
([ADR-003: Database Selection](./decisions/ADR-003_Database_Selection.md) —
DynamoDB rejected for query-pattern mismatch).
```

---

## Exemptions (no CPA required)

| Reference type | Why exempt |
|----------------|-----------|
| Same-file references (`See §3 above`) | Reader is already in the document — can scroll |
| The `## References` block (per `REFERENCE_STANDARDS.md`) | Navigational index, not narrative |
| Forward references (`_[To be produced in Stage {n}]_`) | Cannot summarize what doesn't exist — use intent-description instead: *what* the future artifact will contain and *why* |
| YAML front-matter values (inside `---` fences) | Machine-parseable; Pattern C adds context BELOW, never inside |
| Fabric routing metadata (AI-FLO / AI-DFE) | Machine-terse by design, consumed by automation |

---

## Register Column Integrity

CPA Pattern A enriches content WITHIN existing register columns — it NEVER modifies register structure. The column schema per `MANAGEMENT_FRAMEWORK_CONTRACT.md` is locked. Qualifier text goes in existing Description / Context / Notes / Rationale columns. No new columns are added.

---

## Reconciliation (stale context)

At the **assembly stage**, verify CPA context against current source content:
- If the referenced source was modified after this artifact was generated, flag: "Context for `{ref-code}` may be stale — source modified on {date}. Regenerate?"
- Present flagged items at the assembly gate. User chooses: regenerate / keep / acknowledge.

This extends the existing cross-reference integrity check — same mechanism, same pass.

---

## Depth Adaptation Summary

| Depth | Pattern A | Pattern B | Pattern C | Pattern D | Pattern E |
|-------|-----------|-----------|-----------|-----------|-----------|
| **Minimal** | ≤ 12 words | Single phrase | Omitted | Bullet list | Title + link only |
| **Standard** | ≤ 25 words | 1 sentence | 2 lines | Full table | Title + rationale + link |
| **Comprehensive** | ≤ 50 words | 1–2 sentences | 3–4 lines | Table + narrative | Title + rationale + alternatives + link |

---

## Scope

- Applies to **new output** from this version forward.
- Existing `pdlc-ws/` files are retrofitted by `UPG__` — see `MIGRATION_CATALOGUE.md`. Re-running is safe (already-contextualised references are detected and left as-is).
- Templates stay 100% generic: context placeholders use `{placeholder}` forms filled at generation time.

---

## Content Validation (§11)

CPA compliance is validated as **§11** in each package's `common/content-validation.md`:

```
### 11. Contextual Prose Accompaniment (CPA)

Every cross-reference in the artifact must have contextual accompaniment per the CPA
patterns, scaled to the current depth level:
- Table cells with refs → Pattern A qualifier phrase
- Narrative refs → Pattern B contextual sentence
- State file provenance → Pattern C comment block (Standard+ only)
- Package README refs → Pattern D Consumer/Reads/Why table (Standard+ only)
- ADR/decision refs → Pattern E title + rationale

Exempt: same-file refs, ## References block, forward refs, YAML front-matter, fabric metadata.

If violated: flag to user — "Reference {code} at line {N} lacks contextual accompaniment."
```

---

*PDLC family convention · Contextual Prose Accompaniment · authored once, referenced by every package · Author: Maheri*
