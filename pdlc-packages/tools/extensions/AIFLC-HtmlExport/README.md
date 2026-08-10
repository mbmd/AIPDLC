# AIFLC HTML Export

**Version:** 0.1.0
**Extension Code:** AIFLC-HtmlExport
**Status:** Phase 1 (document mirror) — under active development

---

## What Is This?

A workspace publisher that turns your family workspace (`{family}-ws/`) of Markdown artifacts into a **browsable, self-contained HTML site** — every document rendered with its diagrams, tables, and cross-links intact, plus a grouped landing page in reading order.

It exists because reviewers and stakeholders need to *read and share* the workspace outside a code editor, where raw Markdown does not render Mermaid diagrams, does not resolve `.md` links in a browser, and has no navigable index.

---

## First principle — Markdown is the source of truth; HTML is a shadow

This is the rule the whole tool obeys. Read it before anything else:

| | Rule |
|---|------|
| 1 | **Your `.md` files in `{family}-ws/` are the single source of truth.** Every fact, code, and diagram originates there. |
| 2 | **The generated HTML is a derived, read-only *shadow*** — a projection of your Markdown at a point in time. It has no authority. |
| 3 | **The publisher only ever writes HTML, never `.md`.** Publishing is one-directional: `.md → .html`. |
| 4 | **Nothing reads the HTML back as data.** No workflow, tool, or process extracts information from the shadow — it is for humans to read, not for machines to parse. |
| 5 | **The shadow is disposable.** Delete the whole output folder any time; a single re-run rebuilds it exactly from your Markdown. |
| 6 | **If the HTML and the `.md` ever disagree, the `.md` wins.** You fix the source and re-publish — you never edit the HTML. |

If you want to change what the site says, change the Markdown and re-publish.

---

## Output layout

All output goes under one hidden folder at your workspace root — `.publish/` — which keeps your workspace root clean and works cleanly when several families share one workspace:

```
{workspace-root}/.publish/
├── {family}-html/          ← the site (the shadow — DISPOSABLE; mirrors your {family}-ws/ subfolders)
│   ├── index.html          ← the landing page (grouped, in reading order)
│   └── … one page per source .md …
└── {family}.config.yaml    ← your publish settings (STABLE — a sibling of the site, survives deleting the site)
```

- The `{family}-html/` folder is the shadow — safe to delete, always rebuildable.
- The `{family}.config.yaml` file holds your settings and is **not** inside the shadow, so clearing the site never loses your configuration.

---

## How to run it

### With your AI assistant (recommended)

Type the trigger in a chat prompt:

| Trigger | What it does |
|---------|--------------|
| `HTM__` | Publish the whole workspace: one HTML page per in-scope `.md` + rebuild the landing page. Safe to re-run any time. |
| `HTM__ on` / `HTM__ off` | Turn the **auto-refresh switch** on or off (see "The switch" below). |
| `HTM__ status` | Report the switch state, last publish time, and page count. Reads only — changes nothing. |
| `HTM__ deck` | Build the curated executive presentation deck. *(Planned — Phase 4.)* |
| `HTM__ offline` | Build a fully offline copy (diagrams vendored, no internet needed). *(Planned — Phase 4.)* |

### Directly

```bash
python publish.py [WORKSPACE_ROOT]
```

`WORKSPACE_ROOT` defaults to the family workspace beside the tool. Output is written to `{workspace-root}/.publish/{family}-html/`.

**Requirements:** Python 3.8+, the `markdown` package (`pip install markdown`). `PyYAML` is optional (nicer document-metadata cards). Diagrams render from a CDN on first view unless you build the offline copy.

---

## What it produces (Phase 1 — the document mirror)

- **One HTML page per `.md`**, mirroring your workspace's subfolders, each numbered `NN_` in reading order.
- **A grouped landing page** (`index.html`) — documents grouped by workflow stage, each card showing its sequence number, title, stage, and filename. Any new `.md` you add appears here automatically on the next publish.
- **Faithful rendering** of what Markdown loses in a plain browser:
  - **Mermaid diagrams** render correctly (labels preserved) with a **full-screen viewer** — drag to pan, scroll to zoom, double-click to fit, Esc to close.
  - **Links work:** internal `.md` links resolve to the published pages **with their section anchors preserved**; external links open in a new tab; bare `https://` URLs become clickable.
  - **Document metadata** (front-matter such as `stage` / `status`) is surfaced as a reader header and as a badge on each landing-page card.

The curated **executive deck** and the **offline bundle** are planned for a later phase and are documented here so the contract is complete.

---

## The switch (auto-refresh)

`HTM__ on` sets `enabled: true` and `autoRefresh: true` in your `{family}.config.yaml`. While the switch is on, the site + landing page regenerate automatically **after every workflow stage/gate completes**, and any time you run `HTM__`. This behaves identically across every AI assistant.

`HTM__ off` stops the automatic refresh (the site stays as a frozen snapshot; `HTM__` on demand still works). Setting `enabled: false` turns everything off.

> On the Kiro platform an optional file-save hook is available (regenerate on every `.md` save). It ships **disabled** and is not required — the switch works the same everywhere without it.

---

## Configuration

Settings live in `{workspace-root}/.publish/{family}.config.yaml`, generated with sensible defaults on first run. Highlights:

- `landing.title` / `landing.subtitle` — the landing-page heading.
- `landing.hideFromLanding` — groups to publish but keep off the landing page (still directly linkable).
- `scope.exclude` — glob patterns to skip (state markers and routing artifacts are skipped by default).
- `taxonomy` — the folder→stage grouping; defaults are derived from your family's structure and are overridable.
- `git.commitShadow` — `false` by default (the site is git-ignored as build output); set `true` if you want to commit it (e.g. for GitHub Pages).

Reading order and grouping are **deterministic**: they follow your family's workflow-stage order (not file timestamps), so the same workspace always publishes in the same order, and adding a new group appends it without renumbering the rest.

---

## What it does NOT do

- It does **not** modify, move, or delete any `.md` file — ever.
- It is **not** a data source. Nothing downstream reads the HTML; it is a read-only view for people.
- It does **not** invent content. Everything on a page comes from the Markdown that produced it.

---

## Error handling and safety

The engine fails safe and never leaves your source at risk:

| Situation | Behavior |
|-----------|----------|
| `markdown` package missing | Stops immediately with a one-line install hint (`pip install markdown`); nothing is written. |
| `PyYAML` missing | Continues with built-in defaults; front-matter cards and the config file are ignored (a note is printed). Publishing still works. |
| `{family}.config.yaml` invalid or unparseable | Falls back to defaults and prints a note — a broken config never aborts a publish. |
| One `.md` fails to convert | That page is reported as `[FAIL]` and skipped; the rest of the site and the landing page still build (one bad file never aborts the run). |
| Output would land inside the source workspace | **Refuses** and exits — the shadow must stay separate from the source of truth (SSOT-Shadow). |
| Diagram CDN unreachable at view time | The page still renders; only the Mermaid diagram is affected. Use `HTM__ offline` (planned) to vendor the renderer for air-gapped viewing. |

The shadow folder is cleared and fully rebuilt on every run, so the site is always an exact, orphan-free mirror of the current Markdown — no stale or renamed pages linger. Because the rebuild is total and one-directional, an interrupted run is recovered simply by running `HTM__` again.

---

## Family-aware defaults, fully overridable

One copy of this tool serves every AIFLC family. It ships with built-in stage taxonomies for each family (so it works correctly with zero configuration), but every label, colour, order, and description is overridable via `taxonomy.groups` in your config. The engine detects the family from your workspace folder name and applies the matching defaults.

---

## Roadmap

| Phase | Scope |
|-------|-------|
| **1 (now)** | Document mirror — per-page HTML, deterministic ordering, Mermaid viewer, link fidelity, grouped landing page. |
| 2 | The switch + config (auto-refresh after gates + on-demand; scope/visibility toggles; render-safety rules). |
| 3 | Registration across all families + retrofit of existing workspaces. |
| 4 | Curated executive **deck** mode + fully **offline** bundle. |
