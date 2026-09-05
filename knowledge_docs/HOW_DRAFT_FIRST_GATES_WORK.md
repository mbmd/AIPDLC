# How Draft-First Gates Work

**Purpose:** Explains the Draft-First Gate Model that every AI-* PDLC Family package now follows — the AI writes the artifact to disk *before* asking for approval, so you approve the actual document rather than a chat summary — and the gap-marker convention that lets a draft carry the open questions it still needs you to answer.

---

## Who This Is For

Anyone running a PDLC package through its stages who wants to understand exactly what "approve this stage" means, what the AI must have done before it can ask, and how stages that need your input mid-way still honor the model.

---

## The Core Rule

**Every stage writes its artifact to disk before requesting approval.** You approve based on reviewing the real document in your workspace — never a summary in chat. This is the default gate behavior across the family.

Two consequences follow directly:

- Only an **approved** artifact counts as stage-complete.
- Downstream packages **must not consume a `draft` artifact** — the seam boundary trusts only `status: complete`.

To support this, artifacts carry `status` / `approvedOn` in their provenance front-matter, and the state file records `draftedOn` / `approvedOn`. The gate approval is the moment you confirm the written file — the chat is never the deliverable.

---

## Why Draft-First

Approving a chat summary is approving something you cannot later inspect, and it is easy for the summary and the eventual file to diverge. Writing the artifact first makes the thing you approve and the thing that ships the **same object**. It also means an interrupted session leaves a real, reviewable draft on disk rather than a lost conversation.

---

## Stages That Need Your Input — the Four Interaction Scenarios

Not every stage is "AI produces autonomously, writes, you review." Many need input before or after the draft. Draft-First adapts to all of them, with one invariant: **the artifact is the deliverable, not the chat; your approval is always against the file.** Section 21.10 of the gate protocol codifies four patterns:

- **A — Autonomous production.** The AI has everything it needs, writes the draft, and presents it for approval.
- **B — Q&A then produce.** The AI asks its questions first, then writes the draft once you have answered.
- **C — Produce with gaps, ask post-draft.** The AI writes most of the artifact, marks what it cannot fill, asks those questions in chat, and updates the file in place once you answer.
- **D — Post-review clarification.** You review the draft and provide corrections; the AI revises the file.

---

## The Gap-Marker Convention

When the AI produces a draft that still has holes only you can fill, it marks each one in the file:

```
_[USER-INPUT-NEEDED: {description of what's needed}]_
```

This makes a partial draft honest and reviewable — the file exists on disk, and you can see exactly what is complete and what is pending. The rules around it are strict:

1. The Q&A phase precedes **or** follows the draft write — it never replaces it. An artifact is always written to disk before a gate can pass.
2. A draft with gaps is still a draft.
3. The gate approval is always against the file, whether Q&A happened before, after, or both.
4. AI-initiated questions after the draft are part of the revision loop; the artifact stays `draft` until all gaps are resolved and you approve.
5. **No approval without a complete artifact** — the AI must not request gate approval while any `_[USER-INPUT-NEEDED]_` marker remains. All gaps are resolved first, then the artifact is presented.

---

## Relationship to Gate Approval at Boundaries

Per-stage gates validate the written document; the seam between packages still trusts `status: complete` and neither sees nor re-checks individual stage drafts. Draft-First refines the per-stage gate — its approval *is* you confirming the written document — without changing what crosses the boundary between packages.

---

## What Stays the Same

- Gates remain non-negotiable — nothing auto-progresses, and the AI proposes while you decide.
- The change is additive: the scenario guidance and gap-marker convention layer onto the existing gate mechanics without altering how approvals or seams work.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| Pattern: Gate Before Transition | `knowledge_docs/PATTERN_GATE_BEFORE_TRANSITION.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| Why Spec Before Code Matters | `knowledge_docs/WHY_SPEC_BEFORE_CODE_MATTERS.md` |

*Knowledge Document | Created: 2026-09-05 | Updated: 2026-09-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
