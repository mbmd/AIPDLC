<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# `speckit/` Emitter — generates the GitHub SpecKit constitution

> **Load this file** when `buildProfile: spec-driven-speckit` and AI-DWG is generating or reconciling. It is the second emitter leaf of the `buildmethod/` subsystem (dispatched from `buildmethod-model.md`). Compatibility design §A.8 / `P2b`.

## Preconditions

1. `.governance/workspace-manifest.yaml` exists and `buildProfile: spec-driven-speckit`.
2. The canonical `rules/` cluster has been generated (the constitution is derived from it).

If `buildProfile` ≠ `spec-driven-speckit`, this emitter does not run.

## What it emits — one file

| Output | Path |
|---|---|
| The SpecKit constitution | `.specify/memory/constitution.md` |

That is the whole surface. Unlike `aidlc`, SpecKit needs no tree — GitHub SpecKit reads a single constitution file from `.specify/memory/`.

## The emission step

Run `constitution-mapping.md`: it maps the canonical `rules/` into SpecKit's constitution format — a set of numbered **principles** the SpecKit workflow reads before planning and implementing. The template is `templates/constitution.md`.

## The no-duplication invariant — the one rule that matters here

**The constitution REFERENCES the canonical rules; it does NOT duplicate them.** SpecKit's constitution is a thin, principle-level document that points back at `rules/` for the enforceable detail — exactly as the renderer's platform adapters point back at `rules/` rather than copying rule text. Duplicating the rules into the constitution would create a second copy that drifts the moment `rules/` is re-derived. So each principle in the constitution is a short statement plus a pointer to the canonical rule file(s) that carry its enforceable form.

**Why this matters for reconciliation.** Because the constitution references rather than copies, AI-DWG's Mode-2 reconciliation does not need to re-derive the constitution's *content* when a rule changes — only refresh the principle set if a whole rule category was added or removed. A copied constitution would need a full re-derivation on every rule edit. The reference model is what keeps the constitution cheap to keep current.

## Ownership

`.specify/memory/constitution.md` is `hybrid` — AI-DWG seeds it, the team may hand-edit principles, and SpecKit's own workflow may amend it. Reconciliation preserves team edits (the standard non-destructive merge), same as the `aidlc/` memory files.

## Why this ships independently of the rest of Phase 3

Per the design's build order, the SpecKit constitution (`P2b`) delivers value to SpecKit users without waiting for the `aidlc/` tree work — it is a small, self-contained emitter leaf. A team on the SpecKit build method gets its constitution the moment this leaf exists.

---

*Developer-side design detail · AI-DWG `speckit/` emitter · © Mohammad Maheri*
