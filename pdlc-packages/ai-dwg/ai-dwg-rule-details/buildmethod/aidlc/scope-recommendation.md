<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Scope Recommendation — one field + one start instruction

> **Load this file** alongside `bootstrap-record.md` during step 6 of the `aidlc/` emitter. This is Proposal 4 (`P4`) in its **rewritten** form. Authority for the field: `common/aidlc-v2-output-contract.md` §6. Verified by `TR-822`.

## Why this is one field, not a scope file

The original Proposal 4 — author a custom `pdlc-prepared` v2 scope — is **cancelled** (design §5.7). Three verified facts cancel it, the decisive one being that **stage membership is declared on the stage side** (each stage's own `scopes:` front-matter) and compiled into a generated grid. A scope file authored from outside AI-DLC v2 therefore contains **zero stages** — it cannot work at all. So AI-DWG authors no scope file; it makes a **recommendation** and nothing more.

## The single field

AI-DWG records exactly one field in the bootstrap record (`bootstrap-record.md`, contract §6):

```yaml
recommended_scope: classic          # v2 STOCK scope — skips all 7 Ideation stages
```

**Always a v2 stock scope, never a custom one.** `classic` is the right recommendation because its entire purpose is to run the lifecycle without Ideation ceremony — the seven Ideation stages it skips (intent capture, market research, feasibility, scope definition, team formation, rough mockups, approval & hand-off) are precisely the ones the PDLC chain already completed upstream in AI-ILC, AI-PILC, AI-POLC, and AI-UXD.

**Reverse Engineering needs no special handling.** It is a conditional stage in v2: greenfield self-skips at runtime, brownfield runs against real code. Either is correct without our intervention (this is the same fact code-KB seeding relies on — merged item 15).

## The one start instruction the generated workspace carries

The generated workspace's onboarding text tells the team, in one line, how to begin:

> **Start AI-DLC with `/aidlc --scope classic`.** Ideation is skipped because the product design already exists (produced upstream by the PDLC chain). v2 will confirm the choice by naming the stage and gate counts it computes from its own compiled grid — so the team sees exactly what they are consenting to.

That is the whole of item 18's user-facing surface: the field plus this single instruction. AI-DWG does **not** compute or assert stage counts itself (those are v2's to declare from its compiled grid) — it names the scope and lets v2 confirm.

## What this does NOT do

- No custom scope file (cancelled — §5.7).
- No stage-count assertion by AI-DWG (v2 owns that from its grid).
- No depth or test-strategy claim here — those are their own bootstrap fields (`recommended_depth`, `recommended_test_strategy`), owned by `bootstrap-record.md`.

---

*Developer-side design detail · AI-DWG `aidlc/` scope recommendation · © Mohammad Maheri*
