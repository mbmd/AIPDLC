# Workspace Detection & Context Loading

## Stage: 1 of 13
## Phase: 🔵 FOUNDATION
## Execution: ALWAYS

---

## Purpose

Detect whether this is a fresh start or resumed workflow, configure the output environment, detect available inputs (PIP, existing architecture, requirements), and establish the Architecture Workbook and ADR structure. This stage produces no architecture artifact — it sets up the workspace for everything that follows.

---

## Depth Adaptation

N/A — this stage is depth-independent. Workspace detection and setup execute identically regardless of project complexity.

---

## Step-by-Step Execution

### Step 1: Check for Existing State

1. Scan for `adlc-state.md` in these locations:
   - `./adlc-state.md`
   - `./{system_name}/adlc-state.md`
   - `./architecture/adlc-state.md`
   - Any directory the user has specified
2. If found → load state and follow **Session Resumption Flow** (see `common/session-continuity.md`)
3. If NOT found → proceed to Step 2 (fresh start)

---

### Step 2: Collect System Identity

Ask the user:

```markdown
### Q-CFG-01: System/Project Name

**Context:** This name will appear in all architecture documents, diagrams, ADRs, and the state file.

**Your input:** What is the name of the system or platform being designed?

**Format expected:** Short identifier (e.g., "Fleet Management System", "Payment Gateway", "Logistics Platform")
```

Wait for response. Store as `{system_name}`.

---

### Step 3: Configure Output Structure

```markdown
### Q-CFG-02: Output Folder Structure

**Context:** All architecture documents and ADRs will be saved to a folder structure.

**Options:**
- (a) **Numbered documents** — `01_Architecture_Vision.md`, `02_System_Context_C4L1.md`, etc. with `ADR/` subfolder
- (b) **Phase folders** — `foundation/`, `decomposition/`, `decisions/`, `design/`, `ADR/`
- (c) **Custom** — Describe your preferred structure

**Recommended:** Option (a)
**Rationale:** Numbered documents make the progression visible and the reading order obvious. ADRs in their own subfolder keeps decisions traceable.

**Your Decision:** _[awaiting input]_
```

---

### Step 4: Configure Output Location

```markdown
### Q-CFG-03: Output Location

**Options:**
- (a) **Current workspace root** — Files created here: `./`
- (b) **Subdirectory** — I'll create: `./{system_name}_Architecture/`
- (c) **Custom path** — Specify

**Recommended:** Option (b)
**Rationale:** Keeps architecture artifacts contained; doesn't pollute workspace root.

**Your Decision:** _[awaiting input]_
```

---

### Step 5: Detect Available Inputs

Scan the workspace for existing context:

#### Check for AI-PILC Output (PIP)

Look for:
- `pilc-state.md` (anywhere in workspace)
- Numbered PIP folders (`01_Requirement_Submission/`, `04_Project_Charter/`, etc.)
- `PROJECT_INITIATION_PACKAGE_README.md`

If found → flag as: "PIP detected at: {path}"

#### Check for Requirements Documents

Look for common patterns:
- `**/requirements*.md`
- `**/PRD*.md`
- `**/__input/**`
- `**/specs/**`

If found → flag as: "Requirements document(s) detected: {paths}"

#### Check for Existing Architecture (Brownfield)

Look for:
- Existing C4 diagrams or architecture docs
- `**/architecture/**`
- `**/ADR/**`
- Previous `adlc-state.md` (archived)

If found → flag as: "Existing architecture artifacts detected: {paths}"

---

### Step 6: Present Detection Results

```markdown
## Workspace Scan Results

| Detected | Path | Usable As |
|----------|------|-----------|
| {PIP / Requirements / Architecture / None} | {path} | {Input for Stage 2} |

**Input mode determined:** {PIP / Document / Verbal / Brownfield}
```

If multiple input sources found, ask:

```markdown
### Q-CFG-04: Primary Input Source

**Context:** I found multiple input sources. Which should I use as the primary reference?

**Found:**
- {Source 1}: {path}
- {Source 2}: {path}

**Options:**
- (a) Use {Source 1} as primary
- (b) Use {Source 2} as primary
- (c) Use both — {Source 1} as primary, {Source 2} as supplementary

**Your Decision:** _[awaiting input]_
```

---

### Step 7: Create Folder Structure

Based on user choices, create:

**If Option (a) — Numbered:**

```
{output_root}/
├── ADR/
│   └── ADR-000_Template.md
├── Architecture_Workbook.md
└── adlc-state.md
```

**If Option (b) — Phase folders:**

```
{output_root}/
├── foundation/
├── decomposition/
├── decisions/
├── design/
├── ADR/
│   └── ADR-000_Template.md
├── Architecture_Workbook.md
└── adlc-state.md
```

---

### Step 8: Create ADR Template

Create `ADR/ADR-000_Template.md` using template `templates/adr-template.md`.

This serves as the reference format for all ADRs produced during the workflow.

---

### Step 9: Create Architecture Workbook

Create `Architecture_Workbook.md` with initial structure:

```markdown
# {system_name} — Architecture Workbook

**Purpose:** Living document tracking architecture decisions backlog, open questions, and discussion notes.

---

## Decision Backlog

| # | Decision Area | Key Question | Priority | Status |
|---|--------------|--------------|:--------:|:------:|
| 1 | _[To be populated during workflow]_ | | | |

---

## Open Questions

_None yet — questions will be added as they arise during design._

---

## Discussion Notes

_Captured during architecture sessions._

---

## Architecture Sessions Log

| Session | Date | Stages Covered | Key Outcomes |
|:-------:|:----:|:---------------|:-------------|
| 1 | {today} | Stage 1: Workspace Detection | Setup complete; input mode: {mode} |

---

*Last Updated: {date}*
```

---

### Step 10: Create State File

Create `{output_root}/adlc-state.md`:

```markdown
# AI-ADLC State — {system_name}

## Configuration

| Key | Value |
|-----|-------|
| System Name | {system_name} |
| Started | {timestamp} |
| Last Updated | {timestamp} |
| Workflow Depth | _[To be determined at Stage 2]_ |
| Output Structure | {numbered / phase-folders / custom} |
| Output Root | {output_root} |
| Input Source | {path or mode} |
| Input Mode | {PIP / Document / Verbal / Brownfield} |
| Current Phase | FOUNDATION |
| Current Stage | 1 |
| Status | In Progress |

## Progress

| Stage # | Stage Name | Status | Completed | Notes |
|:-------:|------------|:------:|:---------:|-------|
| 1 | Workspace Detection | 🔄 Active | — | |
| 2 | Requirements Ingestion | ⏳ Pending | — | |
| 3 | Architecture Vision | ⏳ Pending | — | |
| 4 | System Context (C4 L1) | ⏳ Pending | — | |
| 5 | Container Design (C4 L2) | ⏳ Pending | — | |
| 6 | Technology Stack | ⏳ Pending | — | |
| 7 | Multi-Tenancy & Isolation | ⏳ Pending | — | Conditional |
| 8 | Security & Identity | ⏳ Pending | — | |
| 9 | Data Architecture | ⏳ Pending | — | |
| 10 | API Architecture | ⏳ Pending | — | |
| 11 | Integration & Infrastructure | ⏳ Pending | — | |
| 12 | Component Design (C4 L3) | ⏳ Pending | — | |
| 13 | Package Assembly | ⏳ Pending | — | |

## ADR Register

| ADR # | Title | Stage | Status | Decision Summary |
|:-----:|-------|:-----:|:------:|-----------------|
| — | _None yet_ | — | — | — |

## Architecture Principles

_To be defined in Stage 3._

## Key Constraints

_To be defined in Stage 3._

## Containers

_To be defined in Stage 5._

## Open Questions

_None yet._
```

---

### Step 11: Present Completion

Update state: Stage 1 = ✅ Done. Current Stage = 2.

Display:

```
✅ Stage 1: Workspace Detection — Complete

📋 System: {system_name}
📁 Output: {output_root}/ ({structure_type})
📐 ADR folder: Ready (template created)
📓 Architecture Workbook: Initialized
🔄 State tracking: Active
📄 Input detected: {what was found — mode}

Next → Stage 2: Requirements Ingestion
I'll now load and analyze your input to extract architecture-relevant requirements.

{If PIP detected:}
I found a Project Initiation Package. I'll load the Charter, Scope, NFRs, and constraints from it.

{If document detected:}
I found requirements document(s). I'll analyze them for architecture drivers.

{If nothing detected:}
No existing documents found. I'll interview you to establish the architecture context.

Proceeding...
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| User provides no system name | Use "Untitled System"; note "Rename at any time" |
| Folder creation fails | Inform user; suggest alternative path |
| PIP detected but incomplete | Load what exists; note gaps; supplement in Stage 2 |
| Multiple conflicting architectures found | Ask user which is current; archive others |
| User wants to skip setup | Use defaults (numbered, subdirectory); project name still required |

---

## Defaults (if user says "just use defaults")

| Setting | Default |
|---------|---------|
| Output structure | Numbered documents + ADR/ subfolder |
| Output location | `./{system_name}_Architecture/` |
| System name | Must be provided (no default) |
