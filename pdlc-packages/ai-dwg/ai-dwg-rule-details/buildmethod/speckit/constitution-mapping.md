<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# `speckit/` Constitution Mapping — canonical `rules/` → SpecKit principles

> **Load this file** from `speckit/emitter.md` when `buildProfile: spec-driven-speckit`. It defines the single transformation that produces `.specify/memory/constitution.md`. Compatibility design §A.8 / `P2b`. Template: `templates/constitution.md`.

## The transformation contract

**Input:** the canonical `rules/` cluster (the same MUST/NEVER rule files the renderer's platform adapters point at).

**Output:** `.specify/memory/constitution.md` — a set of numbered **principles**, each a short statement plus a pointer back to the canonical rule file(s) that carry its enforceable detail.

**Direction:** one-way, `rules/` → constitution. The constitution is derived; `rules/` is the source of truth. If the two ever disagree, `rules/` wins and the constitution is re-derived.

## The no-duplication invariant (restated as the mapping law)

Each principle **references** its source rule file(s); it **NEVER copies** the rule text. A principle is a one-to-few-sentence articulation of intent — "why this constraint exists and what it governs" — followed by `→ see rules/<file>`. The enforceable MUST/NEVER wording lives only in `rules/`. This is the SpecKit analogue of the renderer's thin-adapter rule (adapters reference, never duplicate), and it is what keeps the constitution from drifting when `rules/` is re-derived.

## How rule categories map to principles

Group the canonical rules by category, then emit **one principle per category** (not one per rule — SpecKit constitutions are principle-level, not rule-level). The category → principle mapping:

| Canonical rule category | SpecKit principle (intent statement) | References |
|---|---|---|
| Architecture / boundary rules | "Respect the architected boundaries and layering." | `→ see rules/` architecture files |
| Security rules (SEC-*) | "Security constraints are non-negotiable and precede convenience." | `→ see rules/` security files |
| Data rules (DATA-*) | "Data handling, classification, and retention follow the declared contract." | `→ see rules/` data files |
| Governance / process rules (GOV-*) | "Governed process and traceability apply to every change." | `→ see rules/` governance files |
| Testing / quality rules | "Quality gates are part of done, not optional follow-up." | `→ see rules/` testing files |
| API / integration rules | "Integration contracts are honoured on both sides." | `→ see rules/` API files |

If a category is absent from `rules/` (conditional generation — Rule 4), its principle is **omitted**, not emitted empty. The constitution reflects only what the architecture justified.

## Ordering

Principles are numbered in the order above (Architecture, Security, Data, Governance, Testing, API) so the constitution reads from structural constraints outward to contract constraints — the same priority order SpecKit's planning phase applies. Numbering is stable: if a category is omitted, later principles keep their relative order but renumber contiguously (no gaps).

## What the constitution does NOT contain

- No rule text (references only — the no-duplication invariant).
- No project-specific values beyond the `{placeholder}` fills the template already carries.
- No principles for categories the AP did not justify.
- No enforcement mechanism detail (that is AI-GCE's surface, not the constitution's) — the constitution states intent; `rules/` + the destination workspace's enforcement carry the teeth.

## Reconciliation behaviour

On Mode-2 reconciliation, re-run this mapping only if a whole rule **category** was added or removed. A change *within* an existing category needs no constitution edit, because the principle references the category rather than copying its rules — the pointer still resolves to the updated `rules/` file. This is the reconciliation saving the reference model buys (see `emitter.md`).

---

*Developer-side design detail · AI-DWG `speckit/` constitution mapping · © Mohammad Maheri*
