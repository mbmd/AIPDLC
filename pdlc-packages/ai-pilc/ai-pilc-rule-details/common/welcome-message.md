<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Welcome Message

## Display Instructions

This message is shown ONCE at the start of a new AI-PILC workflow. Do NOT display on session resumption (use session-continuity resumption message instead).

---

## Message Content

Display the following to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI-PILC — AI-Driven Project Initiation Life Cycle
  Version 1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Welcome. I'll guide you through a structured project initiation
process — from raw requirement to a complete, professional
Project Initiation Package ready for execution.

💡 TIP — best in a fresh session: run this package in its own new chat.
   Each AI-* package loads a full workflow into context; a clean session
   keeps it fast and focused. Finished here? Start the next package fresh.

📋 WHAT WE'LL PRODUCE:
   • Requirement Intake Form
   • Feasibility Assessment & Prioritization
   • Business Case
   • Project Charter
   • Stakeholder Register
   • Scope Statement & WBS
   • Resource & Budget Plan
   • Risk Register
   • RACI Matrix & Governance Plan
   • Kickoff Agenda
   • Management Registers (Decision, Change, Issue, Action, Assumptions, Lessons)

⚙️  HOW IT WORKS:
   • I work through 6 phases, 16 stages — sequentially with gates
   • At each gate, I present my work and you approve before we move on
   • I adapt depth to your project's complexity (minimal → comprehensive)
   • You can skip, revisit, reorder, or stop at any time
   • All progress is saved — you can resume across sessions

🎯 WHAT I NEED FROM YOU:
   1. A source requirement (document, brief, or verbal description)
   2. Your decisions at each gate (I'll recommend; you decide)
   3. Context I can't infer (stakeholder names, budget constraints, dates)

🛡️  PRINCIPLES:
   • I recommend; you decide — I never proceed without your approval
   • I reference your source document — I never invent scope
   • Every decision is logged with rationale — full audit trail
   • Professional PMO quality — industry-standard governance alignment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to begin? I'll start by setting up your workspace.

To get started, I need:

  (a) The path to your source requirement document (if you have one)
  (b) Paste the requirement text directly here
  (c) Describe your project idea verbally — I'll help structure it

Which works for you?
```

---

## Trigger Conditions

Display this message when ALL of the following are true:

1. User has initiated a project initiation request (explicit or inferred)
2. No `pilc-state.md` file exists (this is a fresh start)
3. The welcome message has not been shown in this session

## Do NOT Display When:

- `pilc-state.md` exists (use session-continuity resumption flow instead)
- User is asking a general question, not starting a workflow
- User explicitly says "skip intro" or "just start"

---

## Post-Welcome Flow

After user responds to the welcome message:

1. If user provides source document path → proceed to Stage 1 (Workspace Detection) then Stage 2 (Source Ingestion)
2. If user pastes content → proceed to Stage 1, then Stage 2 with inline content
3. If user describes verbally → proceed to Stage 1, then Stage 2 in "verbal intake" mode
4. If user asks a question about the process → answer it, then re-present the "Ready to begin?" prompt
5. If user says "skip intro" or equivalent → proceed directly to Stage 1 without re-displaying

---

## Customization Note

This welcome message is the ONLY place where the workflow introduces itself. All subsequent interactions should be direct and task-focused — no re-explaining the process unless the user asks "what's next?" or "how does this work?"


---

## Post-Welcome: HTML Publishing Bootstrap (silent — do NOT display to user)

**Purpose:** Ensure the workspace HTML shadow is initialized so gate-driven auto-refresh (`GATE_PROTOCOL.md` §4.1) works from the first stage completion.

**Trigger:** Immediately after displaying the welcome message (first run only — same display condition as the welcome itself).

**Detection:** Check whether `.publish/pdlc.config.yaml` exists at the workspace root.

**Action:**
- If the config **exists** → no-op (already bootstrapped).
- If the config is **absent** AND the `AIFLC-HtmlExport` tool is present under `tools/extensions/AIFLC-HtmlExport/` → run `HTM__ on` silently (creates config with `autoRefresh: true` + builds the initial shadow). Do NOT announce this to the user — it is infrastructure housekeeping.
- If the tool is **absent** → skip silently (the workspace was installed without the extension; no error).

**Rules:**
- This step is invisible to the user — no message, no confirmation prompt.
- It runs ONCE (same lifecycle as the welcome message — first-run only, never on resume).
- It never modifies `.md` source files (SSOT-Shadow, INV-L4-011).
- If `HTM__ on` fails (e.g. Python not installed), log a note in the session but do not block the workflow.
