# Lens Registry — PDLC Family

> **Canonical registry** of every cross-cutting lens on the generic lens seam. The seam reads this file at each stage boundary to know which lenses exist, when they activate, and where their facets live. Adding a lens = appending a row here — **zero core edits**.

**Family:** PDLC (the AI-* PDLC Family of AIFLC)
**Status:** Canonical (family)
**Related:** `ai-packagebuilder/lens-seam/LENS_STATUS_MECHANISM.md` (current-mode SSOT) · `ai-packagebuilder/lens-seam/LENS_COHERENCE_PROTOCOL.md` (shared coherence layer)

---

## 1. What a lens is

A **lens** is a cross-cutting mode that, when active, makes every design-chain package apply a domain-specific facet as it designs its slice of the product. One switch; a different facet per package. Lenses are orthogonal — a feature may carry several lens tags at once, and each lens designs its own slice independently.

Lenses plug into the **generic lens seam** — the stage-boundary hook defined once in the `core-workflow` and `core-generator` templates (§19a of `CANONICAL_SLIM_CORE_TEMPLATE.md`). The seam is feature-agnostic: it reads this registry and loads whatever facets the active lenses declare. Engine cores (`core-engine` — GCE/TGE/DFE) carry no seam; their lens work is delivered as manually-triggered agents.

### Intersection facets (a distinct kind — composed, not a lens)

An **intersection facet** is a facet COMPOSED from two or more lenses — it fires only when those lenses are co-active. It is **not a lens**: it has no mode switch, no `Lens_Status.md` row, and no feature id of its own. Its activation is **derived** (`activateWhen`, a predicate over lens modes), and its per-feature marker is a **shadow** of the composed lens tags that dissolves if either drops. The seam evaluates intersection-facet entries after the active-lens pass (§3). The first is the **agentic** facet (AI ∩ Automation) — see `ai-packagebuilder/agentic-lens/AGENTIC_FACET_SPEC.md`. Teaching the seam this kind is a **one-time** logic extension; thereafter a new intersection facet is a registry-only addition, same zero-core-edit promise as lenses.

---

## 2. The Registry

```yaml
lenses:
  - id: ai-lens
    name: AI Lens
    modeOnValue: AI-Powered          # from Lens_Status.md; OFF value = No-AI
    featureTag: aiFeature
    featureIdPrefix: AIF
    facet: {pkg}-rule-details/ai-lens/facet.md
    agents:
      governance: AIG__              # AI-GCE
      quality:    AIQ__              # AI-TGE
    utilityKey: _AILENS_
    protocol: ai-packagebuilder/ai-lens/AI_LENS_PROTOCOL.md
    manifest: .ai-lens/manifest.json

  - id: automation-lens
    name: Automation Lens
    modeOnValue: Automated           # from Lens_Status.md; OFF value = Manual
    featureTag: automationFeature
    featureIdPrefix: AUTO
    facet: {pkg}-rule-details/automation-lens/facet.md
    agents:
      governance: ATG__              # AI-GCE
      quality:    ATQ__              # AI-TGE
    utilityKey: _AUTOLENS_
    protocol: ai-packagebuilder/automation-lens/AUTOMATION_LENS_PROTOCOL.md
    manifest: .automation-lens/manifest.json

# Facets COMPOSED from ≥2 lenses. NOT lenses: no mode switch, no Lens_Status.md row,
# no feature id. Activation is DERIVED (activateWhen over lens modes). See §1 + §3.
intersection-facets:
  - id: agentic-lens
    name: Agentic (intersection facet)
    kind: intersection-facet
    derivesFrom: [ai-lens, automation-lens]
    activateWhen: "ai-lens Mode == AI-Powered AND automation-lens Mode == Automated"   # read from Lens_Status.md
    featureThreshold: "aiSubMode in {augmented,native} AND automationMode in {attended,unattended}"
    featureMarker: agenticProfile        # DERIVED shadow of the two lens tags; dissolves if either drops below threshold
    threadedBy: [aiFeatureId, automationFeatureId]   # NO agenticFeatureId, NO register (INV [agentic-tag-integrity])
    facet: {pkg}-rule-details/agentic-lens/facet.md
    agents:                              # EXTENDS the two lenses' agents — no new pair
      quality:    [AIQ__, ATQ__]         # + trajectory eval / step-cap test
      governance: [AIG__, ATG__]         # + tool-permission / excessive-agency / kill-switch
    spec: ai-packagebuilder/agentic-lens/AGENTIC_FACET_SPEC.md
    coherence: "LENS_COHERENCE_PROTOCOL.md §3.1 (intra-feature action-surface sub-check)"
```

---

## 3. How the seam uses this registry

At each stage boundary, a design/generation core (`core-workflow` / `core-generator`):

1. Reads `management_framework/Lens_Status.md` (the current-mode SSOT).
2. For each **lens** row whose `modeOnValue` matches the mode recorded for that lens → loads `{pkg}-rule-details/{lens-id}/facet.md` for the current package.
3. **Then, for each `intersection-facets` entry whose `activateWhen` predicate holds** against the same `Lens_Status.md` modes (e.g. agentic = `ai-lens` ON **and** `automation-lens` ON) → loads its `facet` for the current package too. (A derived, composed facet — not a lens; per-feature it applies to artifacts carrying its `featureMarker`.)
4. If no mode row exists, or the mode is the OFF value, or no intersection predicate holds → no-op (zero facet load).

Engine cores do not consult this registry for facets. The `agents` entries are listed only for discoverability/registration — the agents are seeded into the Layer-3 workspace by AI-DWG and invoked manually.

---

## 4. Field definitions

| Field | Meaning |
|-------|---------|
| `id` | Registry id + facet-folder name (`{pkg}-rule-details/{id}/`) |
| `name` | Human-readable lens name |
| `modeOnValue` | The `Lens_Status.md` Mode value that means "active" for this lens |
| `featureTag` | The boolean front-matter tag marking an artifact as belonging to this lens |
| `featureIdPrefix` | The stable thread-id prefix (`AIF-{NNN}` / `AUTO-{NNN}`) |
| `facet` | Facet path template (`{pkg}` resolves to the current package's rule-details root) |
| `agents.governance` / `agents.quality` | The Layer-3 GCE / TGE agent triggers |
| `utilityKey` | The `_X_`-class report+toggle key |
| `protocol` | The canonical lens protocol (build-side) |
| `manifest` | The courier manifest AI-DWG writes into the Layer-3 workspace |

---

## 5. Adding a new lens (the zero-core-edit promise)

To add a lens (e.g. a future Security Lens or Accessibility Lens):

1. Author its protocol under `ai-packagebuilder/{lens}/`.
2. Append a row to §2 here.
3. Author its facets under each `{pkg}-rule-details/{lens-id}/`.
4. Add its `Lens_Status.md` row semantics + `data-schema/` fields.
5. Register its utility key + agents in `TRIGGER_KEYS_REFERENCE.md`.

No edit to any core file is required — the seam already reads this registry. This is the promise the seam was built for; the Automation Lens (the second row) validated it.

**Adding an intersection facet** (a facet composed from ≥2 existing lenses): author its spec under `ai-packagebuilder/{id}/`, append an `intersection-facets` entry to §2 (with `derivesFrom` + `activateWhen`), author its facet under each `{pkg}-rule-details/{id}/`, and add its derived `featureMarker` + `data-schema/` field. The **first** intersection facet (agentic) also required a one-time seam-logic extension (§3 step 3) to teach the seam this kind; **subsequent** intersection facets are registry-only additions (zero core edits), exactly like lenses.

---

## 6. Governance

- The seam scope is enforced by **INV-L3-034** (seam only in workflow/generator cores; engines carry none).
- The shared coherence layer is single-sourced per **INV-L4-012** (`LENS_COHERENCE_PROTOCOL.md`).
- Every lens feature tag must carry a resolvable feature id (**INV-L2-016** for AI; the Automation analog).

---

*Lens Registry v1.0.0 | Family: PDLC | Canonical registry of seam lenses.*
