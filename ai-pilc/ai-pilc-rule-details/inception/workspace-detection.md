# Workspace Detection

## Stage: 1 of 16
## Phase: 🔵 INCEPTION
## Execution: ALWAYS

---

## Purpose

Detect whether this is a fresh start or a resumed workflow, configure the output environment, and establish the management framework. This stage produces no project deliverable — it sets up the workspace for everything that follows.

---

## Depth Adaptation

N/A — This stage is depth-independent. Workspace setup is identical regardless of project complexity. Depth level is determined at Stage 2 (Source Document Ingestion) after assessing the source material.

---

## Step-by-Step Execution

### Step 1: Check for Existing State

1. Scan the workspace for `pilc-state.md` in these locations (in order):
   - `./pilc-state.md`
   - `./pilc-docs/pilc-state.md`
   - `./01_Requirement_Submission/../pilc-state.md` (numbered folder root)
   - Any directory the user has specified as output root
2. If found → load state and follow **Session Resumption Flow** (see `common/session-continuity.md`)
3. If NOT found → proceed to Step 2 (fresh start)

---

### Step 2: Collect Project Identity

Ask the user:

```markdown
### Q-CFG-01: Project Name

**Context:** This name will appear in all deliverables, the state file, and folder structure.

**Your input:** What is the name of this project or initiative?

**Format expected:** Short title (e.g., "CRM Platform Upgrade", "Digital Transformation Programme", "Cloud Migration")

**Note:** This can be changed later — it's not a binding decision.
```

Wait for response. Store as `{project_name}`.

---

### Step 2a: Mint the Project ID (Correlation Key)

The **Project ID** is the unique key that threads this project through the entire AI-* Family — it is the value AI-FLO routes on and AI-PPM aggregates portfolio roll-ups against. It MUST be minted now (Stage 1), not deferred to the Charter, and once set it is **immutable** (the Charter later confirms it, never regenerates it).

1. Auto-generate a candidate using the format: `PRJ-{ABBREV}-{YYYY}-{NNN}`
   - `{ABBREV}` — 3–5 uppercase letters derived from the project name (e.g., "CRM Platform Upgrade" → `CRM`)
   - `{YYYY}` — current year
   - `{NNN}` — sequence, default `001` in standalone mode
2. Confirm with the user:

```markdown
### Q-CFG-01b: Project ID

**Context:** This is the project's unique identifier — the correlation key used across every package in the AI-* Family (routing, portfolio roll-up, cross-document consistency). It is set once and never changes.

**Proposed ID:** `{generated_project_id}`

**Options:**
- (a) Accept the proposed ID
- (b) Provide your own ID (e.g., an existing PMO/portfolio code)

**Recommended:** Option (a)
**Rationale:** The generated ID follows the family convention `PRJ-{ABBREV}-{YEAR}-{NNN}` and is guaranteed unique within a standalone run.

**Note:** If this project is governed by AI-PPM (portfolio), the portfolio may assign or reconcile the `{NNN}` sequence to guarantee uniqueness across the whole portfolio.

**Your Decision:** _[awaiting input]_
```

Wait for response. Store as `{project_id}`.

3. **Optional — Idea lineage:** If this project originated from an AI-ILC Approved Idea Brief, capture the originating idea reference so the idea → project → portfolio chain is traceable:

```markdown
### Q-CFG-01c: Originating Idea (Optional)

**Context:** If this project came from an approved idea (AI-ILC), recording the idea reference preserves the idea → project → portfolio lineage.

**Your input:** Idea ID / brief reference, or "none".
```

Store as `{idea_ref}` (default: `none`).

The Project ID and idea lineage are recorded as Decision `D-002` when the Decision Log is created (Step 6).

---

### Step 3: Configure Output Structure

Ask the user:

```markdown
### Q-CFG-02: Output Folder Structure

**Context:** All deliverables will be saved to a folder structure. Choose the layout that suits your organization.

**Options:**
- (a) **Numbered folders** — `01_Requirement_Submission/`, `02_Screening_Prioritization/`, ..., `10_Project_Kickoff/`, `management_framework/`
- (b) **Flat docs folder** — `pilc-docs/inception/`, `pilc-docs/assessment/`, ..., `pilc-docs/mobilization/`, `management_framework/`
- (c) **Custom** — Describe your preferred structure and I'll adapt

**Recommended:** Option (a)
**Rationale:** Numbered folders make the sequential flow visible and are familiar to PMO teams. Each folder clearly maps to a lifecycle phase.

**Your Decision:** _[awaiting input]_
```

Wait for response. Store choice in state.

---

### Step 4: Configure Output Location

Ask the user:

```markdown
### Q-CFG-03: Output Location

**Context:** Where should I create the output folders?

**Options:**
- (a) **Current workspace root** — Files created here: `./`
- (b) **Subdirectory** — I'll create a project folder: `./{project_name}/`
- (c) **Custom path** — Specify the path

**Recommended:** Option (b)
**Rationale:** Keeps project initiation artifacts contained in their own directory, avoiding clutter in the workspace root.

**Multi-project note:** If this workspace will hold more than one initiated project, use a `{project_id}`-keyed folder (e.g., `./{project_id}/`) so each project has a clean, collision-free boundary that AI-PPM and AI-FLO can address by ID.

**Your Decision:** _[awaiting input]_
```

Wait for response. Store as `{output_root}`.

---

### Step 5: Create Folder Structure

Based on user's choices, create the output structure.

**If Option (a) — Numbered folders:**

```
{output_root}/
├── 01_Requirement_Submission/
├── 02_Screening_Prioritization/
├── 03_Business_Case/
├── 04_Project_Charter/
├── 05_Stakeholder_Management/
├── 06_Scope_Planning/
├── 07_Resource_Budget/
├── 08_Risk_Management/
├── 09_Governance_Communication/
├── 10_Project_Kickoff/
├── management_framework/
└── pilc-state.md
```

**If Option (b) — Flat docs:**

```
{output_root}/
├── pilc-docs/
│   ├── inception/
│   ├── assessment/
│   ├── justification/
│   ├── authorization/
│   ├── planning/
│   └── mobilization/
├── management_framework/
└── pilc-state.md
```

**If Option (c) — Custom:**

- Ask user to describe structure
- Create as specified
- Ensure `management_framework/` and `pilc-state.md` are always present regardless of custom layout

---

### Step 6: Create Management Registers

Create the six management registers using templates from `templates/`:

1. `management_framework/Decision_Log.md` — from `templates/decision-log.md`
2. `management_framework/Change_Log.md` — from `templates/change-log.md`
3. `management_framework/Issue_Log.md` — from `templates/issue-log.md`
4. `management_framework/Action_Items.md` — from `templates/action-items.md`
5. `management_framework/Assumptions_Dependencies.md` — from `templates/assumptions-dependencies.md`
6. `management_framework/Lessons_Learned.md` — from `templates/lessons-learned.md`

**Populate with initial entries:**

- Decision Log → D-001: "Output structure chosen: {option}. Project name: {project_name}."
- Decision Log → D-002: "Project ID assigned: {project_id}. Originating idea: {idea_ref}."
- Assumptions → ASM-001: "Source requirement document is available and represents stakeholder intent."

---

### Step 7: Create State File

Create `{output_root}/pilc-state.md` with initial content:

```markdown
# AI-PILC State — {project_name}

## Configuration

| Key | Value |
|-----|-------|
| Project Name | {project_name} |
| Project ID | {project_id} |
| Originating Idea | {idea_ref} |
| Started | {current_timestamp} |
| Last Updated | {current_timestamp} |
| Workflow Depth | _[To be determined at Stage 2]_ |
| Output Structure | {numbered / flat / custom} |
| Output Root | {output_root} |
| Source Document | _[To be provided at Stage 2]_ |
| Current Phase | INCEPTION |
| Current Stage | 1 |
| Status | In Progress |

## Progress

| Stage # | Stage Name | Status | Completed | Notes |
|:-------:|------------|:------:|:---------:|-------|
| 1 | Workspace Detection | 🔄 Active | — | Setting up |
| 2 | Source Document Ingestion | ⏳ Pending | — | |
| 3 | Requirement Structuring | ⏳ Pending | — | |
| 4 | Requirements Analysis | ⏳ Pending | — | |
| 5 | Clarification Cycle | ⏳ Pending | — | Conditional |
| 6 | Feasibility Assessment | ⏳ Pending | — | |
| 7 | Prioritization | ⏳ Pending | — | |
| 8 | Business Case Development | ⏳ Pending | — | |
| 9 | Project Charter | ⏳ Pending | — | |
| 10 | Stakeholder Management | ⏳ Pending | — | |
| 11 | Scope Definition | ⏳ Pending | — | |
| 12 | Resource & Budget Planning | ⏳ Pending | — | |
| 13 | Risk Management | ⏳ Pending | — | |
| 14 | Governance & Communication | ⏳ Pending | — | |
| 15 | Kickoff Preparation | ⏳ Pending | — | |
| 16 | Package Assembly | ⏳ Pending | — | |

## Decisions Made

| Decision ID | Stage | Summary |
|:-----------:|:-----:|---------|
| D-001 | 1 | Output structure: {choice}. Project: {project_name}. |
| D-002 | 1 | Project ID assigned: {project_id}. Originating idea: {idea_ref}. |

## Open Items

_None yet._

## Register Counts

| Register | Entries |
|----------|:-------:|
| Decisions | 2 |
| Changes | 0 |
| Issues | 0 |
| Actions | 0 |
| Assumptions | 1 |
| Lessons | 0 |
```

---

### Step 8: Present Completion

Update state: Stage 1 = ✅ Done. Current Stage = 2.

Display:

```
✅ Stage 1: Workspace Detection — Complete

📋 Project: {project_name}
🆔 Project ID: {project_id}
📁 Output: {output_root}/ ({structure_type})
📊 Management registers: 6 created
🔄 State tracking: Active

Next → Stage 2: Source Document Ingestion
I need your source requirement document to continue.

How would you like to provide it?
  (a) File path in this workspace
  (b) Paste the content here
  (c) Describe your project idea verbally

Which works for you?
```

---

## Automatic Proceed

This stage auto-proceeds to Stage 2 after user provides their source preference. There is no separate gate between Stage 1 and Stage 2 — the completion message naturally transitions into Stage 2's intake.

---

## Error Handling

| Situation | Response |
|-----------|----------|
| User provides no project name | Use "Untitled Project" and note: "You can rename at any time" |
| Folder creation fails (permissions) | Inform user; suggest alternative path; do NOT proceed without a writable output location |
| State file already exists but user says "fresh start" | Archive existing: rename to `pilc-state-{timestamp}.archived.md`; create new |
| User wants to skip setup questions | Use defaults (numbered folders, workspace root); log as decision |

---

## Configuration Defaults

If user says "just use defaults" or "skip setup":

| Setting | Default Value |
|---------|---------------|
| Output structure | Numbered folders (option a) |
| Output location | `./{project_name}/` |
| Project name | Must still be provided (no default) |
| Project ID | Auto-generated `PRJ-{ABBREV}-{YEAR}-001` from project name; user may override |
| Originating idea | `none` |
