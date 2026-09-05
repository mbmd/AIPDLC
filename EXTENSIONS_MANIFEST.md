# Extensions Manifest — PDLC Family

> Declares which optional editor/workspace extensions ship with the AI-* PDLC Family. When you install the family, the extensions marked **Include? = Yes** are provided under the family's `tools/extensions/` folder.

## Extensions

| Extension Code | Name | Include? | Notes |
|---|---|---|---|
| `AIFLC-PDLC-Dashboard` | PDLC Family Dashboard | Yes | Core dashboard for the PDLC family — renders project / portfolio / package status |
| `AIFLC-CommandBoard` | Command Board | Yes | Trigger-key quick-reference UI |
| `AIFLC-HtmlExport` | HTML Export | Yes | Workspace→HTML publishing (`HTM__` trigger) — renders your `.md` artifacts as a browsable site with a Mermaid viewer and a grouped landing page |

## What ships, and where it lands

- Each extension marked **Include? = Yes** is provided under `tools/extensions/{extension-code}/` inside the installed family.
- Extensions marked **Include? = No** are not part of this family.
- Every extension in this family is optional — the packages work without them; the extensions add browsable dashboards, a trigger reference, and HTML publishing on top.

## History

| Date | Change |
|------|--------|
| 2026-07-20 | PDLC ships both AIFLC-PDLC-Dashboard and AIFLC-CommandBoard |
| 2026-07-26 | Added AIFLC-HtmlExport (workspace→HTML publishing) |
