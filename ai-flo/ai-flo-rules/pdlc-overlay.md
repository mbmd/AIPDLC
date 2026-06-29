# AI-FLO — PDLC Family Overlay

> **Purpose:** Family-specific routing behaviors for PDLC that FLO's universal core engine does not contain. Loaded when FLO operates on the PDLC family (detected via `FAMILY_INTERFACE.md` family: PDLC).

---

## PDLC-Specific Entity Type

PDLC's primary entity is a **project**, identified by `projectId` (format: `PRJ-{ABBREV}-{YYYY}-{NNN}`). This maps to the universal `entityId` field in markers.

Secondary entity: **idea** (from AI-ILC), identified by `ideaId`. Ideas transform into projects at AI-PILC (lineage: `derivedFrom: {ideaId}`).

---

## PDLC Dispatch Model (PPM -> Project Layer)

PDLC uses AI-PPM (portfolio engine) to authorize entity flow. When AI-PPM produces a dispatch authorization (`DA-*.md`), FLO reads it as a routing trigger:

**What FLO reads:**
- `pdlc-ws/portfolio/ppm-state.md` — portfolio state marker
- `dispatch-authorizations/DA-*.md` — per-entity authorization (carries entityId + constraints)

**What FLO does:**
- On detecting a new `DA-*.md`: register the entity in `flo-state.md` with initial position = first edge from PILC
- Apply any constraints from the authorization (e.g., skip list)
- Alert operator: "New entity authorized: {entity-id}. Initial routing targets: {edges from bindings}"

> This is an **overlay trigger** — the core engine's `advance` command does the actual routing. The overlay just defines how PDLC entities enter the graph.

---

## PDLC Skip Profiles

PDLC supports per-entity skip profiles (e.g., "backend service — skip AI-UXD"):

```yaml
# In flo-state.md entity entry:
skip: [AI-UXD]    # edges to these packages are suppressed for this entity
```

**Effect on gate matching:** When `check` evaluates outbound edges, skipped packages are excluded. The entity advances to the next non-skipped edge.

**How set:** Operator command: `override [entity-id] skip [package]` or from PPM dispatch authorization constraints.

---

## PDLC Fan-In Specifics

From `FAMILY_BINDINGS.md`:

| Consumer | Waits For | Gate Behavior |
|----------|-----------|---------------|
| AI-DWG | AI-ADLC + AI-POLC + AI-UXD | All-3 required (AP mandatory; PBP/UXP = enrichment) |
| AI-POLC | AI-PILC + AI-ADLC + AI-UXD | Accept-any (enrichment from each) |
| AI-PPM | AI-ILC + AI-PILC | Accept-any (registers both ideas and projects) |

**Refinement:** For AI-DWG's fan-in, AI-ADLC is mandatory (gate step 4 BLOCK if absent); AI-POLC and AI-UXD are optional (gate step 5 DEGRADE). This is already encoded in AI-DWG's gate contract — FLO reads it naturally.

---

## PDLC Marker Sources

| Package | Marker | Entity Field |
|---------|--------|-------------|
| AI-ILC | `ilc-state.md` | `ideaId` |
| AI-PILC | `pilc-state.md` | `projectId` |
| AI-ADLC | `adlc-state.md` | `projectId` |
| AI-UXD | `uxd-state.md` | `projectId` |
| AI-POLC | `polc-state.md` | `projectId` |
| AI-DWG | `dwg-state.md` | `projectId` |
| AI-GCE | `gce-state.md` | `projectId` |
| AI-TGE | `tge-state.md` | `projectId` |
| AI-PPM | `ppm-state.md` | `projectId` |
| AI-DFE | `dfe-state.md` | — (family-scoped) |

---

## PDLC Roll-Up (to PPM)

When AI-PPM requests a portfolio roll-up, FLO compiles:
- All tracked project entities, their current positions, and days-in-stage
- Any active conflicts or holds
- Entities ready to advance but awaiting operator confirmation

This is a **read** from `flo-state.md` — no family-specific logic needed beyond knowing PPM is the consumer.

---

## PDLC Governance Spine Integration

PDLC uses a shared governance spine (`management_framework/`). FLO appends:
- `FLO-D-NNN` — Routing decisions (overrides, holds, releases)
- `FLO-I-NNN` — Flow issues (conflicts, stalls)

Routine hops logged ONLY in `routing-log.md` — not in the spine.

---

*PDLC overlay for AI-FLO | Loaded when family: PDLC detected | Author: Maheri*
