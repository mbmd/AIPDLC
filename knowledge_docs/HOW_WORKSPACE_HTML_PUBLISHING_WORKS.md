# How Workspace HTML Publishing Works

**Purpose:** Explains how the AI-* PDLC Family publishes your workspace Markdown as a browsable HTML site via the `HTM__` trigger and the `AIFLC-HtmlExport` extension — and the single rule that keeps it safe: Markdown is the source of truth, HTML is a disposable shadow.

---

## Who This Is For

Anyone who wants a readable, navigable view of a workspace — for review, sharing, or a stakeholder walkthrough — without turning the HTML into a second copy of the truth that can drift from the Markdown.

---

## The First Principle — Markdown Is the Source of Truth, HTML Is a Shadow

This is the rule the whole tool obeys (the **SSOT-Shadow** invariant):

1. Your `.md` files in `{family}-ws/` are the **single source of truth** — every fact, code, and diagram originates there.
2. The generated HTML is a **derived, read-only shadow** — a projection of your Markdown at a point in time, with no authority of its own.
3. The publisher only ever writes HTML, never `.md`. Publishing is one-directional: `.md → .html`.
4. Nothing reads the HTML back as data — it is for humans to read, not for machines to parse.
5. The shadow is **disposable** — delete the whole output folder any time; one re-run rebuilds it exactly.
6. If the HTML and the `.md` ever disagree, the `.md` wins — you fix the source and re-publish, never the HTML.

The publisher **refuses to run** if its output would land inside the source workspace, precisely to keep the shadow separate from the source.

---

## The `HTM__` Trigger

Publishing is driven by one trigger and a few sub-commands:

| Trigger | Type | Does |
|---------|------|------|
| `HTM__` | Operation | Full idempotent publish — one HTML page per in-scope `.md` plus a grouped landing page. Safe to re-run. |
| `HTM__ on` | Switch | Enable auto-refresh (gate-driven + on-demand) and run one full publish. |
| `HTM__ off` | Switch | Disable auto-refresh — the shadow stays as a frozen snapshot; manual `HTM__` still works. |
| `HTM__ status` | Report | Switch state, last publish time, page count. Read-only. |
| `HTM__ deck` | Operation | Build/refresh a curated executive presentation deck. *(Planned — Phase 4.)* |
| `HTM__ offline` | Operation | Offline build with a vendored diagram renderer, so no internet is needed at view time. *(Planned — Phase 4.)* |

---

## What Gets Published, and Where

The site is written to a `.publish/` folder **outside** your source workspace:

```
{workspace-root}/.publish/
├── {family}-html/          ← the site (the shadow — DISPOSABLE; mirrors your {family}-ws/ subfolders)
│   ├── index.html          ← the landing page (grouped, in reading order)
│   └── … one page per source .md …
└── {family}.config.yaml    ← your settings — NOT inside the shadow, so clearing the site never loses config
```

- **Reading order and grouping are deterministic** — they follow your family's workflow-stage order, not file timestamps. The same workspace always publishes in the same order, and adding a new group appends it without renumbering the rest.
- **Scope is configurable** — `scope.exclude` glob patterns skip files (state markers and routing artifacts are skipped by default); `taxonomy` sets the folder → stage grouping.
- The shadow folder is **cleared and fully rebuilt on every run**, so the site is always an exact, orphan-free mirror of the current Markdown — no stale or renamed pages linger. An interrupted run is recovered simply by running `HTM__` again.

By default the site is treated as build output and is git-ignored; set `git.commitShadow: true` if you want to commit it (for example, to serve it from GitHub Pages).

---

## Resilience

The publisher is built to never fail loudly for a small problem:

- An invalid config falls back to defaults with a note — a broken config never aborts a publish.
- If one `.md` fails to convert, that page is reported as `[FAIL]` and skipped; the rest of the site and the landing page still build.
- If a diagram renderer is unreachable at view time, the page still renders — only that one diagram is affected (the planned `HTM__ offline` vendors the renderer for air-gapped viewing).

---

## What Stays the Same

- The extension is opt-in per family — it is declared in the family's extensions manifest and only ships where included.
- Publishing changes nothing in your workspace — it only ever writes into the separate `.publish/` shadow.
- Your Markdown remains the one place you edit; the HTML is always regenerated, never hand-tuned.

---

## Related Documents

| Document | Location |
|----------|----------|
| Reference Map — Triggers | `knowledge_docs/REFERENCE_MAP_TRIGGERS.md` |
| How to Use the Dashboard | `knowledge_docs/HOW_TO_USE_THE_DASHBOARD.md` |
| How to Run the Data Fabric | `knowledge_docs/HOW_TO_RUN_THE_DATA_FABRIC.md` |
| How to Onboard a New Team Member | `knowledge_docs/HOW_TO_ONBOARD_A_NEW_TEAM_MEMBER.md` |

*Knowledge Document | Created: 2026-09-05 | Updated: 2026-09-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
