# How Artifact-Quality Rules Work

**Purpose:** Explains the blocking artifact-quality rules that every AI-* PDLC Family package applies to the documents it generates — self-explanatory metrics, completeness tracking, glossaries, traceable key references, consistent rankings, and column legends — so a generated artifact is understandable and navigable on its own, without the reader needing outside context.

---

## Who This Is For

Anyone who consumes the artifacts the family produces — backlogs, analyses, registers, matrices — and anyone who wants to understand why those artifacts are structured the way they are.

---

## Why These Rules Exist

An artifact that scores, ranks, or cross-references things is only useful if a reader can understand it **without asking the author**. These rules come from real user-workspace feedback: readers hit tables of numbers with no explanation of what "good" looks like, keys like `OBJ-01` with nowhere to look them up, and rankings that did not match their scores. Each rule closes one of those gaps. They are **blocking** — an artifact that violates one fails validation rather than shipping unclear.

---

## The Rules

| Rule | What it requires |
|------|------------------|
| **Self-explanatory quantitative artifacts** | Any artifact with scores, rankings, matrices, or assessments carries a **"What This Analysis Means"** section up front — before the first numbered section — so a reader knows how to read the numbers before meeting them. |
| **Completeness & downstream resolution** | Each artifact states what is complete here, what is intentionally deferred, and where any deferred gap gets filled downstream — so nothing looks missing when it is actually scheduled elsewhere. |
| **Back-propagate "gap filled" status** | When a later stage fills a gap an earlier artifact pointed to, the earlier artifact's "where this gets filled" reference is updated to "✅ Completed — see …", so the trail never points at work that is already done. |
| **Mandatory glossary** | Each artifact ends with a **Glossary** tailored to its own content (not a generic copy-paste), so the terms and abbreviations it uses are defined in place. |
| **Rank-score consistency** | In any table with both a Rank column and a numeric Score column, the ranking must actually follow the scores, and equal scores use tied ranks — a mismatch without a documented reason fails. |
| **Key-reference traceability** *(critical)* | Every reference to a key (`OBJ-01`, `CAP-05`, `REQ-D-03`, `GAP-04`, …) is a markdown link to the document where that key is formally defined — so a reader can always jump to the source. |
| **Column legend for register-style tables** | Every register-style table (an ID column plus several others) is followed by a **Column Legend** blockquote explaining every column, including what each value means — so a dense table is readable without guesswork. |

---

## How They're Applied

These rules live in each package's content-validation rule set and run as **blocking** checks when an artifact is produced or revised — an artifact does not pass its gate while a rule is violated. They pair with a shared artifact-sections standard that gives every package a runtime checklist of the sections an artifact of its type must contain, so the requirements are consistent across the family rather than reinvented per package.

Because they operate at artifact-production time, they apply to **new and revised** artifacts going forward; running a package that regenerates an artifact brings it up to standard. The family upgrade path (`UPG__`) can retrofit these output-feature improvements into an existing workspace non-destructively.

---

## What Stays the Same

- The rules govern the **shape and readability** of generated artifacts — they do not change what a package analyzes or decides.
- They are additive quality gates layered onto the existing content validation; they do not replace any package's domain rules.
- They apply family-wide, so an artifact from any package reads with the same navigational conventions.

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Manage Product Backlog | `knowledge_docs/HOW_TO_MANAGE_PRODUCT_BACKLOG.md` |
| How Draft-First Gates Work | `knowledge_docs/HOW_DRAFT_FIRST_GATES_WORK.md` |
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| How to Use the Dashboard | `knowledge_docs/HOW_TO_USE_THE_DASHBOARD.md` |
| How Provenance Tracking Works | `knowledge_docs/HOW_PROVENANCE_TRACKING_WORKS.md` |

*Knowledge Document | Created: 2026-09-05 | Updated: 2026-09-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
