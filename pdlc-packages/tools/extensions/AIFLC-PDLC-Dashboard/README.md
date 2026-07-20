# AIFLC PDLC Dashboard

**Version:** 0.1.0
**Extension Code:** AIFLC-PDLC-Dashboard

---

## What Is This?

An interactive HTML dashboard + VS Code extension for visualizing your PDLC family project lifecycle. Shows chain progress, package status, blockers, management framework, and more — all generated from `*-state.md` files in your workspace.

---

## Dual-Mode Access

### Browser Mode (zero dependencies)

Open the HTML file directly:

```
tools/extensions/AIFLC-PDLC-Dashboard/ui/index.html
```

Works offline, no server needed. Data is embedded in the HTML or loaded from a companion `dashboard-data.json`.

### VS Code Extension Mode

Install the `.vsix` package:

```bash
code --install-extension tools/extensions/AIFLC-PDLC-Dashboard/extension/AIFLC-PDLC-Dashboard.vsix
```

Then open the command palette and run: **AIFLC: Open Dashboard**

The extension reads your `*-state.md` files live and renders the dashboard inside VS Code as a webview panel. Auto-refreshes when state files change.

---

## What It Shows

- **Portfolio view** — all projects with status indicators
- **Package progress** — per-package phase/stage/artifact tracking
- **Chain diagram** — Mermaid flow visualization of the PDLC chain
- **Management framework** — decisions, risks, actions, issues, lessons
- **Ideas kanban** — idea lifecycle from capture to routing
- **PO view** — product vision, roadmap, backlog health, acceptance criteria
- **Architecture view** — C4 progress, ADRs, tech stack, integrations, NFRs
- **UX view** — personas, journeys, IA, flows, design system, accessibility
- **Statistics** — charts for status distribution and progress

---

## Data Contract

The dashboard expects data in the format defined by `data-contract/dashboard-data-schema.json`. This data is:
- **Browser mode:** Embedded as `var D = {...}` in the HTML, or loaded from a sibling `dashboard-data.json`
- **VS Code mode:** Generated live from workspace `*-state.md` files by the extension

---

## Generating Fresh Data

Use the AIFLC trigger in your AI assistant:

```
VSC__
```

This regenerates the dashboard data from your current project state.

---

## Theme Support

- Dark theme (default)
- Light theme (toggle via ☀/🌙 button)
- Respects VS Code theme in extension mode

---

## Requirements

- **Browser mode:** Any modern browser
- **VS Code mode:** VS Code 1.80+
- **Mermaid CDN:** Required for chain diagrams (loaded from `cdn.jsdelivr.net`)

---

*Part of [AIFLC](../../README.md) — the AI-* PDLC Family*
