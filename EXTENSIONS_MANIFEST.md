# Extensions Manifest — PDLC Family

> Declares which extensions from `1.dev/tools/` are cloned into this family at `DEV__ promote` time.
> This file is the per-family tool inventory — analogous to how `_fabric/MANIFEST.md` governs fabric cloning.

## Model

- **Canonical source:** `1.dev/tools/extensions/{ext-code}/`
- **Promote target:** `2.assemble/pdlc/pdlc-packages/tools/extensions/{ext-code}/`
- **Trigger:** `DEV__ promote pdlc` (after domain-package sync, after fabric clone, before license sync)

## Extensions

| Extension Code | Name | Include? | Notes |
|---|---|---|---|
| `AIFLC-PDLC-Dashboard` | PDLC Family Dashboard | Yes | Core dashboard for the PDLC family — renders project/portfolio/package status |
| `AIFLC-CommandBoard` | Command Board | Yes | Trigger key quick-reference UI |
| `AIFLC-HtmlExport` | HTML Export | Yes | Workspace→HTML publishing (HTM__ trigger) — renders .md artifacts as a browsable site with Mermaid viewer + grouped landing page |

## Inclusion Rules

1. **All listed extensions with `Include? = Yes`** are copied verbatim from `1.dev/tools/extensions/{code}/` into `2.assemble/pdlc/pdlc-packages/tools/extensions/{code}/` during promote.
2. **Excluded extensions** (`Include? = No`) are skipped — they don't ship with this family.
3. **New extensions** added to `1.dev/tools/extensions/` are NOT auto-included — they must be explicitly added to this manifest first.
4. The promote script reads this manifest to determine what to copy. It does NOT scan `1.dev/tools/extensions/` blindly.

## Promote Behavior

At `DEV__ promote pdlc`:

1. Read `1.dev/pdlc/EXTENSIONS_MANIFEST.md` → list of included extension codes.
2. For each included code:
   - Source: `1.dev/tools/extensions/{code}/`
   - Target: `2.assemble/pdlc/pdlc-packages/tools/extensions/{code}/`
   - Copy all files (exclude `.git/`, any `.gitkeep`).
3. Report: "Extensions cloned: {list}. Skipped: {list}."

## History

| Date | Change |
|------|--------|
| 2026-07-20 | Created — PDLC ships both AIFLC-PDLC-Dashboard and AIFLC-CommandBoard |
| 2026-07-26 | Added AIFLC-HtmlExport (workspace→HTML publishing, OI-197) |
