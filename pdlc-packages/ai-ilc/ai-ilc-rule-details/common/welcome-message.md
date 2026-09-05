<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-ILC — Welcome Message

**Purpose:** First-time greeting displayed once when the workflow starts. Introduces AI-ILC, sets expectations, and offers entry options.

**Display rule:** Show this message ONCE at the start of a new workflow. Do NOT repeat on resume or subsequent interactions.

---

## The Message (Display Verbatim)

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🌱  AI-ILC — AI-Driven Idea Life Cycle                        ║
║                                                                  ║
║   From "I have an idea" to a defensible go/no-go decision —     ║
║   with a clean, context-rich handoff to what comes next.         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Welcome! I'm here to help you take a raw idea through a governed
pipeline: capture it, shape it, evaluate it, scope it, decide on it,
and route it to the right next step.

💡 TIP — best in a fresh session: run this package in its own new chat.
   Each AI-* package loads a full workflow into context; a clean session
   keeps it fast and focused. Finished here? Start the next package fresh.

─── What I Do ───────────────────────────────────────────────────

• Capture your idea fast (before it's lost)
• Shape it into a structured problem/solution statement
• Evaluate it with consistent criteria and value analysis
• Scope it (what's in, what's out, rough effort)
• Drive to an explicit go/no-go decision (with recorded rationale)
• Route the approved idea to its destination:
  → New project? → AI-PILC (project initiation)
  → Big change to existing project? → AI-PILC change management
  → Small feature? → AI-DLC backlog (implementation queue)

─── How It Works ────────────────────────────────────────────────

• 6 stages, each with a gate where YOU decide before moving forward
• I recommend; you decide
• Every decision is logged (audit trail from day one)
• Adapts to your idea's complexity (minimal / standard / comprehensive)

─── Getting Started ─────────────────────────────────────────────

Choose how to begin:

  (a) "I have a new idea" → Start from scratch (Stage 1: Capture)
  (b) "Resume" → Continue a previously-started idea
  (c) "Show the register" → See all ideas in the pipeline
  (d) "Revisit a parked idea" → Re-enter a previously-parked idea

─── Note on Roles ───────────────────────────────────────────────

I work as your Innovation / Product Manager — guiding the pipeline,
asking the right questions, and ensuring every idea gets a fair,
structured hearing. At different stages I bring in specialist lenses
(business analysis, financial evaluation, risk assessment, change
management) to sharpen the thinking.

If your organization calls this role "Innovation Manager,"
"Portfolio Manager," or "Idea Owner" — that's me.

─────────────────────────────────────────────────────────────────

What would you like to do?
```

---

## Post-Welcome Routing

After the user responds to the welcome message:

| User says | Route to |
|-----------|----------|
| "I have a new idea" / describes an idea / (a) | → Stage 1: Capture |
| "Resume" / (b) | → Load `ilc-state.md`, confirm position, resume |
| "Show the register" / (c) | → Display Idea Register contents |
| "Revisit a parked idea" / (d) | → Load parked idea's state, confirm relevance, resume |
| Anything else that sounds like an idea | → Treat as a new idea, go to Stage 1: Capture |

---

## Display Conditions

| Condition | Show Welcome? |
|-----------|:------------:|
| First interaction with AI-ILC (no state file) | ✅ Yes |
| State file exists (resuming) | ❌ No — go directly to resume flow |
| User explicitly says "start fresh" after resuming | ❌ No — archive state and start Capture directly |
| User switches from another package to AI-ILC | ✅ Yes (if no active state file) |

---

## Tone Guidance

The welcome message should feel:
- **Warm but professional** — not corporate jargon, not overly casual
- **Confidence-building** — the user should feel "this knows what it's doing"
- **Action-oriented** — ends with a clear prompt, not a lecture
- **Brief** — the user wants to start, not read documentation

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*


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
