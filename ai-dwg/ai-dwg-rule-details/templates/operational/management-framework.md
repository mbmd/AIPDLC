# Template: management_framework/ (Development Phase Registers)

These registers track governance during the development/build phase. They are lighter than AI-PILC's full PMO registers — focused on implementation decisions, blockers, and lessons.

---

## Decision_Log.md

```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->

# Decision Log — Development Phase

Tracks implementation decisions made during development that are below ADR threshold but still worth recording.

**When to log:** Library choices, pattern selections within a module, test strategy adjustments, tooling decisions.
**NOT for:** Architecture decisions (use ADRs) or project governance decisions (those were in AI-PILC).

| # | Date | Decision | Context | Options Considered | Chosen | Rationale | Made By |
|---|------|----------|---------|-------------------|--------|-----------|---------|
| D-001 | | | | | | | |
```

---

## Change_Log.md

```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->

# Change Log — Development Phase

Tracks scope, approach, or timeline changes during the build phase.

| # | Date | Change | Reason | Impact | Approved By |
|---|------|--------|--------|--------|-------------|
| C-001 | | | | | |
```

---

## Issue_Log.md

```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->

# Issue Log — Development Phase

Tracks blockers, problems, and technical issues encountered during development.

| # | Date | Issue | Severity | Module | Status | Resolution | Resolved |
|---|------|-------|:--------:|--------|:------:|-----------|----------|
| I-001 | | | H/M/L | | Open/Closed | | |
```

---

## Lessons_Learned.md

```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->

# Lessons Learned — Development Phase

Captured during sprints, retros, and sessions. Inform future work.

| # | Date | Lesson | Context | Action Taken |
|---|------|--------|---------|-------------|
| L-001 | | | | |
```

---

## Generation Rules

1. **ALWAYS generated** — every development workspace gets these registers
2. Registers start EMPTY (header + one blank row) — populated during development
3. Entries are append-only — never delete logged items
4. Each entry is sequentially numbered within its register
5. AI-DLC sessions should log decisions and lessons as they arise
6. Sprint retros feed into Lessons_Learned.md

## Relationship to Other Packages

| Package | Its Governance Mechanism | Scope |
|---------|------------------------|-------|
| AI-PILC | `management_framework/` (6 registers) | Project initiation decisions |
| AI-ADLC | `ADR/` + `Architecture_Workbook.md` + `management_framework/` (4 registers) | Architecture decisions |
| **AI-DWG** | **`management_framework/` (4 registers)** | **Development/build decisions** |
| AI-GCE | (future) | Compliance decisions |
