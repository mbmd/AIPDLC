# AI-ILC — Installation Guide (Kiro IDE)

**Purpose:** Step-by-step instructions to install AI-ILC into your Kiro workspace.

---

## Prerequisites

- Kiro IDE installed and running
- A workspace where you want to manage ideas

---

## Installation Steps

### Step 1: Create the Steering Folder

In your project workspace, ensure this path exists:

```
{your-project}/.kiro/steering/ai-ilc-rules/
```

### Step 2: Copy the Core Workflow

Copy `ai-ilc-rules/core-workflow.md` into:

```
{your-project}/.kiro/steering/ai-ilc-rules/core-workflow.md
```

This is the master orchestration file that Kiro loads automatically.

### Step 3: Copy the Rule Details

Copy the entire `ai-ilc-rule-details/` folder to one of these locations (Kiro checks in order):

| Priority | Location |
|:--------:|----------|
| 1 | `{your-project}/.ai-ilc/ai-ilc-rule-details/` |
| 2 | `{your-project}/.kiro/ai-ilc-rule-details/` |
| 3 | `{your-project}/ai-ilc-rule-details/` |

**Recommended:** Option 2 (keeps everything under `.kiro/`).

### Step 4: Verify Installation

Start a new chat in Kiro and say:

```
I have an idea
```

You should see the AI-ILC welcome message with the pipeline overview and entry options.

---

## What Gets Installed

| Item | Purpose | Location |
|------|---------|----------|
| `core-workflow.md` | Master orchestration (always loaded) | `.kiro/steering/ai-ilc-rules/` |
| `common/` (5 files) | Cross-cutting rules | `ai-ilc-rule-details/common/` |
| `idea-lifecycle/` (6 files) | Stage execution instructions | `ai-ilc-rule-details/idea-lifecycle/` |
| `connectors/` (1 file) | Portfolio connector spec | `ai-ilc-rule-details/connectors/` |
| `templates/` (7 files) | Output templates | `ai-ilc-rule-details/templates/` |

**Total:** 20 files

---

## Configuration (Optional)

### Custom Evaluation Rubric

If your organization wants custom scoring criteria, create:

```
{your-project}/.kiro/steering/ilc-evaluation-config.md
```

Define custom criteria there. AI-ILC's two-source model will use your criteria where provided and fall back to the built-in baseline where you're silent.

### Persona Steering (Optional)

If you want AI-ILC's personas to use your organization's voice/style, ensure the relevant persona files are in your `.kiro/steering/` folder. AI-ILC references:
- `#persona-product-manager` (lead at most stages)
- `#persona-process-designer` (lead at Scope)
- Sub-roles: business-analyst, financial-analyst, resource-planner, risk-analyst, change-manager

---

## Using AI-ILC

After installation, these phrases activate the workflow:

| Say | Effect |
|-----|--------|
| "I have an idea" | Start new idea capture |
| "I have a new idea for..." | Start capture with initial context |
| "Resume" | Continue a previously-started idea |
| "Show the idea register" | Display all ideas in the pipeline |
| "Revisit parked idea" | Re-enter a parked idea |

---

## Standalone vs. Chain Usage

| Mode | Requirements |
|------|-------------|
| **Standalone** | Just AI-ILC installed. Briefs are portable documents. |
| **With AI-PILC** | AI-PILC also installed. Approved Idea Briefs feed directly into project initiation. |
| **Full chain** | AI-PILC + AI-ADLC + AI-DWG + AI-GCE installed. Full pipeline from idea to governed workspace. |

AI-ILC works in all three modes. No dependency on other packages.

---

## Uninstallation

Remove:
- `.kiro/steering/ai-ilc-rules/` folder
- `ai-ilc-rule-details/` folder (wherever you placed it)

Your idea outputs (briefs, registers, state files) remain in your project — they're your artifacts, not the package's.

---

*Version 1.0.0 | AI-ILC — AI-Driven Idea Life Cycle*
