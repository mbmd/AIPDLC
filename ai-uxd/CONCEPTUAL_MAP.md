# AI-UXD Conceptual Map

> **What this file is:** A navigational guide to AI-UXD's internal structure. It answers "where does each UX design concern live?" and helps you find the right file across 5 phases and 16 stages.

---

## How to Read This

AI-UXD is an **interactive lifecycle workflow** with 5 phases containing 16 stages, plus a set of conditional generators (multi-brand theming, i18n/RTL, service blueprints, empathy maps) and one governance agent. This map organizes files by *concern domain* — so you can find what you need based on what you're trying to design.

**Key principle:** AI-UXD turns business intent and user research into a governed UX Design Package (UXP). Everything traces from persona → journey → flow → screen → component → token → principle. Break any link and the system loses its rationale.

---

## Concern → Location Map

### Users & Research (Phase 1: Discover)

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Workspace setup & input ingestion | Discover | `discover/workspace-detection.md` | `uxd-state.md`, mode + depth detection |
| Research planning & synthesis | Discover | `discover/research-planning.md` | Research synthesis (findings, themes, opportunities) |
| Persona definition | Discover | `discover/persona-definition.md` | Evidence-backed personas (goals, pain points, JTBD) |

### Structure & Paths (Phase 2: Define)

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Journey mapping | Define | `define/journey-mapping.md` | Journey maps (touchpoints, emotions, error paths) |
| Information architecture | Define | `define/information-architecture.md` | Site map, navigation model, taxonomy, search strategy |
| User flow design | Define | `define/user-flow-design.md` | Task flows, user flows, wireflows with edge cases |

### System & Surface (Phase 3: Design)

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Wireframe & screen inventory | Design | `design/wireframe-inventory.md` | Screen inventory + low-fidelity wireframe specs |
| Design system foundation | Design | `design/design-system-foundation.md` | Principles, color, type, spatial, icons, voice & tone, tokens |
| Component library | Design | `design/component-library.md` | Component inventory with all states, interactions, ARIA |
| Multi-brand theming | Design | `design/multi-brand-theming.md` | Token inheritance + color-mode architecture (conditional) |

### Proof & Quality (Phase 4: Validate)

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Accessibility baseline | Validate | `validate/accessibility-baseline.md` | WCAG 2.2 baseline mapped to POUR principles |
| Usability validation plan | Validate | `validate/usability-validation.md` | Heuristic checklist + test plan + feedback intake |
| Design QA framework | Validate | `validate/design-qa-framework.md` | Design-to-code drift rules, severity model, report format |

### Handoff & Assembly (Phase 5: Assemble)

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| AI-POLC handoff | Assemble | `assemble/polc-handoff.md` | Personas + journeys packaged for prioritization |
| AI-DWG / AI-GCE handoff | Assemble | `assemble/dwg-gce-handoff.md` | Design system + tokens + accessibility baseline |
| Package assembly & UXP README | Assemble | `assemble/package-assembly.md` | Assembled UXP + `UXP_README.md` |

### Workspace & Session Management

| Concern | Phase | File | Purpose |
|---------|-------|------|---------|
| Workspace detection & setup | Discover | `discover/workspace-detection.md` | Detect mode/depth, create output folder structure |
| Session continuity | Common | `common/session-continuity.md` | Resume logic, `uxd-state.md` management |
| Content validation | Common | `common/content-validation.md` | Quality rules for all deliverables |
| Design standards | Common | `common/design-standards.md` | Cross-cutting design discipline rules |
| Process overview | Common | `common/process-overview.md` | High-level run-through of the lifecycle |
| Question format guide | Common | `common/question-format-guide.md` | How the workflow asks for input |
| Welcome message | Common | `common/welcome-message.md` | First-interaction greeting (shown once) |

---

## Cross-Cutting Mechanisms

### Phase Flow

```
Discover → Define → Design → Validate → Assemble
    │         │        │         │           │
    │         │        │         │           └── Package & hand off (POLC, DWG, GCE)
    │         │        │         └── Prove it works (accessibility, usability, QA)
    │         │        └── Build the system (wireframes, tokens, components)
    │         └── Structure it (journeys, IA, flows)
    └── Understand the users (research, personas)
```

### Adaptive Depth

| Depth Level | When Applied | Effect |
|-------------|-------------|--------|
| Minimal | Simple app, ≤2 user types, clear scope | 2-3 personas, 1-2 journeys, essential tokens only |
| Standard | Typical product, 3-5 user types | Full persona set, journeys per persona, complete design system |
| Comprehensive | Complex multi-user platform, accessibility-critical, enterprise | Extended research, empathy maps, service blueprints, multi-brand tokens |

### Gate Model

Every stage ends with a gate — the user must approve before proceeding. The gate presents:
1. Summary of the deliverable produced
2. Explicit approval request ("Approve and proceed to Stage {N+1}? [Y/N/Revise]")
3. Option to revise (iterate on the current stage) or skip (Stage 10 only)

### Conditional Generation

| Output | Condition |
|--------|-----------|
| Multi-brand theming + dark mode | IF >1 brand OR color modes required |
| i18n/RTL/localization tokens | IF >1 locale OR multi-language mentioned |
| Service blueprints | IF Comprehensive depth + service-oriented |
| Empathy maps | IF Comprehensive depth |

### Templates (Deliverable Structures)

All 15 templates live in `templates/` — one per UXP deliverable (persona, journey map, IA, user flow, wireframe spec, design system, design tokens, component inventory, multi-brand tokens, voice & tone, accessibility baseline, usability test plan, design QA framework, `uxd-state.md`, UXP README). They define the exact structure of each output document (generic, `{placeholder}` based).

### Cross-Cutting Spines

| Mechanism | Where Defined | How It Works |
|-----------|--------------|--------------|
| **Adaptive depth** | `core-workflow.md` | Minimal/Standard/Comprehensive — scales to product complexity |
| **Identity spine** | `core-workflow.md` | "How it looks/feels/behaves + can everyone use it = in; what/why/order, how-built, runtime compliance = out" (L36) |
| **Traceability spine** | `core-workflow.md` | persona → journey → flow → screen → component → token → principle |
| **Accessibility-by-design** | every stage; consolidated in `validate/accessibility-baseline.md` | WCAG 2.2 considered at each stage; Stage 11 consolidates, never starts from zero |
| **AI-POLC strategy exchange** | `assemble/polc-handoff.md` | UXD ⇢ POLC personas/journeys; POLC ⇢ UXD value goals focus research |
| **AI-DLC v1 feedback channel** | `validate/usability-validation.md` | Runtime usability/accessibility signals flow back into the UXP |
| **Session continuity** | `common/session-continuity.md` | `uxd-state.md` preserves mode, depth, progress, downstream signals |
| **Governance agent (L51)** | `templates/agents/ux-consistency-agent.md` | Ships `ux-consistency-agent` (`UXC__`, AG-ID `UXD-AG-01`) |

---

## Common Questions

### "Where do personas get created?"

→ `discover/persona-definition.md` — evidence-backed personas with goals, pain points, context, and JTBD framing. They flow to AI-POLC at Stage 14. Demographic-only personas are an anti-pattern.

### "Where is the design system defined?"

→ `design/design-system-foundation.md` covers principles, color, typography, spatial grid, iconography, and voice & tone — all expressed as W3C-aligned design tokens (global → semantic → component). `design/component-library.md` then defines every component with its full state set.

### "How does AI-UXD connect to AI-POLC?"

→ `assemble/polc-handoff.md` — UXD produces personas and journey maps that AI-POLC consumes for value-based prioritization. The exchange is bidirectional: POLC's value goals focus UXD research priorities. See also the Chain Contract in `core-workflow.md`.

### "How does AI-UXD feed AI-DWG and AI-GCE?"

→ `assemble/dwg-gce-handoff.md` — the design system and tokens seed AI-DWG's `design-system.md` + `frontend-standards.md`; the accessibility baseline seeds AI-GCE's `accessibility-compliance` rule. The component inventory feeds AI-DWG structure generation.

### "When is multi-brand theming generated?"

→ `design/multi-brand-theming.md` (Stage 10) is the only conditional stage — it executes when more than one brand OR color modes (dark/light) are required, and is skipped for single-brand, single-mode products.

### "Where does accessibility live?"

→ Everywhere. It's embedded at every stage — from persona definition (include users with disabilities) through component design (states, ARIA, keyboard) to `validate/accessibility-baseline.md`, which consolidates the WCAG 2.2 conformance target against POUR principles. It is never a bolt-on phase.

### "What's the final output?"

→ `assemble/package-assembly.md` assembles all artifacts into the UX Design Package (UXP) and generates `UXP_README.md` (reading guide, artifact index, traceability map). This is what AI-DWG, AI-POLC, and AI-GCE receive.

### "Where is session state managed?"

→ `common/session-continuity.md` defines the `uxd-state.md` structure (mode, depth, current phase/stage, conditional features, downstream signals), resume flow, and edge cases for interrupted sessions.

### "How does the correlation key work?"

→ AI-UXD threads the `projectId` (camelCase) front-matter key in `uxd-state.md`. When a PIP is present, `projectId` is extracted from `pilc-state.md`; otherwise it is generated. The key correlates the UXP with sibling Project-layer outputs (`adlc-state.md`, `polc-state.md`) that all feed AI-DWG.

### "Does AI-UXD install a governance agent?"

→ Yes. At package assembly (Stage 16), AI-UXD installs the `ux-consistency-agent` (`UXC__`, AG-ID `UXD-AG-01`) into `.kiro/agents/`. It validates UXP internal consistency, traceability, token alignment, accessibility spec match, and handoff consumability on demand. See `templates/agents/ux-consistency-agent.md` for the check set and `templates/agents/shortcut-rules-block.md` for the workspace-rules injection.

---

## File Relationships

```
CONCEPTUAL_MAP.md  ← You are here (navigation)
README.md          ← What this package does (external audience)
PLAN.md            ← Design rationale and decisions (deep dive)
USER_GUIDE.md      ← How to run it (end-user walkthrough)
core-workflow.md   ← How it executes (runtime orchestration — THE spec)
```

---

*Created: 2026-06-12 | Package: AI-UXD v1.0.0*

---

## AI-DFE Data Interface (`ai-uxd-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/uxd-data.json`.

| File | Purpose |
|------|---------|
| `uxd-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
