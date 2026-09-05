# Artifact Mandatory Sections

> **Base standard:** the AIFLC artifact-sections standard — defines the mandatory structural sections every generated artifact must include. This file is a per-package reminder; the base standard is authoritative.

Every artifact produced by this package MUST include the following structural sections (IMP-001–005, 019):

## Required Sections Checklist

- [ ] **[IMP-001] "What This Analysis Means"** — at the TOP (after title/blockquote, before section 1) for any artifact with quantitative analysis. Includes: plain-language summary + concrete example + business implication.
- [ ] **[IMP-002] "Completeness & Downstream Resolution"** — after main content, before Glossary. States what's complete, what's partial (and where gaps get filled), what's out of scope.
- [ ] **[IMP-003] Back-propagation** — after each gate, update earlier artifacts' "Completeness" tables from "pending" to "✅ Completed."
- [ ] **[IMP-004] Key expansion** — first use of any package code includes parenthetical name: `AI-{XXX} ({Full Name})`.
- [ ] **[IMP-005] "Glossary"** — last section before Sources/footer. Table of all abbreviations and technical terms used in the document.
- [ ] **[IMP-019] Column legends** — immediately after every register-style table (4+ columns with ID column). Blockquote with Column/Description table.

## Placement Order

`Title → Blockquote → [What This Means] → Metadata → Main Content → [Completeness] → [Glossary] → Sources → Footer`

## On Failure

All rules are **BLOCKING** — artifact fails gate validation without compliance. See `common/content-validation.md` for enforcement details.

---

*Artifact Mandatory Sections · common rule · 2026-08-15*
