<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Wardley Mapping

**Extension ID:** wardley-mapping
**Version:** 1.1.0
**Rule Prefix:** WDL
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 6 (Technology Stack Selection)
- **Secondary Stages:** Stage 5 (Container Design — informs decomposition)

Wardley Mapping is an **architecture-positioning technique**. It plots value-chain components against an **evolution axis** (genesis → custom-built → product → commodity/utility) to reason about **build-vs-buy**, where to invest custom engineering, and which components to treat as commodities. Its output **feeds** the Technology Stack decision and ADRs; it does not replace them.

This is the **architecture-altitude** use of Wardley (component build/buy/evolution). The **strategy-altitude** use (market positioning, where-to-play) belongs to the Strategy family (SFLC) when built — the same technique at a higher altitude.

---

## Primary Role — CTO / Chief Architect (No New Sub-Role)

This extension does **not** introduce a sub-role. Build/buy and commodity/custom positioning is core **CTO / Chief Architect** judgment, so the primary role leads directly. Apply the primary persona's constraint-awareness and trade-off discipline: every build decision is a commitment of scarce engineering capacity, and every buy decision is a dependency to be governed.

---

## Rules

### Rule WDL-01: Anchor the Map on a User Need

**Statement:** Every Wardley map begins from a **user need** at the top of the value chain. Components exist only insofar as they serve that need; a map with no anchoring user need has no basis for positioning.

**Verification:**
- [ ] The map names the user (or user role) and the need being served
- [ ] The anchoring need traces to a requirement/quality attribute (Stage 2/3) or a container's purpose (Stage 5)
- [ ] The top of the value chain is the need, not a technology

**Anti-Pattern:** Starting from a technology inventory ("we have Kafka, Postgres, …") and mapping components with no line back to a user need.

**ADR Trigger:** No

---

### Rule WDL-02: Lay Out the Value Chain (Visible → Invisible)

**Statement:** Below the user need, place the components required to meet it, ordered by **visibility** — from what the user directly experiences (top) down to the invisible infrastructure that supports it (bottom). Draw the dependency links between components.

**Verification:**
- [ ] Components are stacked by visibility (user-facing at top, infrastructure at bottom)
- [ ] Dependency links connect each component to what it needs below it
- [ ] The value chain includes the significant components of the containers from Stage 5 (no major container omitted)
- [ ] Each component is named in domain/technical terms the team recognizes

**Anti-Pattern:** A flat list of components with no visibility ordering and no dependency links — a bill of materials, not a value chain.

**ADR Trigger:** No

---

### Rule WDL-03: Position Each Component on the Evolution Axis

**Statement:** Each component is positioned on the evolution axis — **Genesis → Custom-Built → Product (incl. rental) → Commodity/Utility** — based on how mature and ubiquitous that capability is in the market, not on how the team currently implements it.

**Verification:**
- [ ] Every component has an evolution-stage position (Genesis / Custom / Product / Commodity)
- [ ] Position reflects market maturity of the capability, not the team's current build state
- [ ] Components whose position is uncertain/contested are flagged (they often hide the biggest decisions)
- [ ] The axis is applied consistently across all components

**Anti-Pattern:** Positioning a component as "custom" merely because the team built it custom, when the capability is actually a market commodity — the exact confusion the map exists to expose.

**ADR Trigger:** No

---

### Rule WDL-04: Classify Build / Buy / Adopt-Commodity per Component

**Statement:** Each component receives an explicit **disposition** — build (custom), buy (product/rental), or adopt-commodity (utility) — justified by its evolution position and its strategic importance to the user need.

**Verification:**
- [ ] Every component has a build / buy / adopt-commodity disposition
- [ ] The disposition is consistent with the component's evolution position (commodity → adopt/buy; genesis of a core differentiator → build)
- [ ] Strategic (differentiating) components are distinguished from context (non-differentiating) components
- [ ] Cost and team-capability implications of each build disposition are noted (a build is a capacity commitment)

**Anti-Pattern:** Deciding build/buy by preference or familiarity rather than by evolution position and strategic value.

**ADR Trigger:** No — captured per-decision under WDL-06.

---

### Rule WDL-05: Flag Custom-Building a Commodity as a Hotspot

**Statement:** Any component positioned as **Product** or **Commodity** but given a **build** disposition must be flagged as a hotspot (anti-pattern), and either justified with an explicit rationale or re-dispositioned to buy/adopt.

**Verification:**
- [ ] Every build-a-commodity case is flagged
- [ ] Each flagged case has either a documented justification (why custom is warranted despite commodity availability) or a corrected disposition
- [ ] The reverse trap is also checked: relying on an immature (genesis) component for something core without acknowledging the risk
- [ ] Flagged hotspots route to an ADR when the decision is contested (WDL-06)

**Anti-Pattern:** Silently custom-building authentication, messaging, storage, or another commodity because "we've always done it that way" — burning engineering capacity on undifferentiated work.

**ADR Trigger:** Yes — when a decision to custom-build a commodity (or depend on a genesis component for a core need) is made deliberately and has long-term impact.

---

### Rule WDL-06: Build/Buy Decisions With Long-Term Impact → ADR

**Statement:** Any build/buy disposition that involves 2+ viable options with long-term cost, lock-in, or capability implications must be recorded as an ADR.

**Verification:**
- [ ] Significant build/buy decisions have an ADR (context, options, decision, consequences)
- [ ] The ADR references the component's evolution position and strategic importance
- [ ] Lock-in, exit cost, and operational ownership are addressed in buy decisions
- [ ] The ADR is listed in the state ADR register

**Anti-Pattern:** Making a years-long build/buy commitment with no recorded rationale, so a future architect cannot reconstruct why.

**ADR Trigger:** Yes — this rule *is* the ADR trigger for build/buy decisions.

---

### Rule WDL-07: Reconcile With the Technology Stack Selection

**Statement:** The map's dispositions must reconcile with the Technology Stack chosen in Stage 6 — every buy/adopt-commodity disposition maps to a selected product/service, and every build disposition maps to a component the team will own.

**Verification:**
- [ ] Each disposition is reflected in the Stage 6 Technology Stack (or the mismatch is explained)
- [ ] Buy/adopt dispositions name the actual product/service selected
- [ ] Build dispositions appear as owned components in the container/component design
- [ ] No component is "buy" on the map but custom-built in the stack (or vice-versa) without rationale

**Anti-Pattern:** A Wardley map that says "buy" while the technology stack quietly builds it anyway — two plans of record that disagree.

**ADR Trigger:** No

---

### Rule WDL-08: Hand-Off Completeness

**Statement:** At stage completion, every component's disposition must be routed to its downstream home; nothing is orphaned. The map exists to drive the stack and the ADRs, not to decorate the design doc.

**Verification:**
- [ ] Every component disposition is reflected in the Technology Stack (Stage 6) — WDL-07
- [ ] Every long-term build/buy decision has an ADR — WDL-06
- [ ] Every hotspot (WDL-05) has a disposition (justified or corrected)
- [ ] Component-evolution notes (which components are expected to move stage, and when) are captured for future reconciliation

**Anti-Pattern:** A completed map whose build/buy conclusions never make it into the stack or the ADRs — a "dead artifact."

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with Wardley Mapping rules active, verify:

- [ ] The map is anchored on a user need (WDL-01) with a visibility-ordered, linked value chain (WDL-02)
- [ ] Every component is positioned on the evolution axis by market maturity (WDL-03)
- [ ] Every component has a build / buy / adopt-commodity disposition (WDL-04)
- [ ] Custom-building-a-commodity cases are flagged and resolved (WDL-05)
- [ ] Long-term build/buy decisions have ADRs (WDL-06)
- [ ] Dispositions reconcile with the Stage 6 Technology Stack (WDL-07)
- [ ] Every disposition/hotspot is routed downstream; evolution notes captured (WDL-08)

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| WDL-05 | A component is deliberately custom-built despite being a commodity (or a core need depends on a genesis component), with long-term impact |
| WDL-06 | Any build/buy decision with 2+ viable options and long-term cost / lock-in / capability implications |

---

## Templates

### Wardley Map — Value Chain × Evolution

The map as a table (authoritative). Evolution stage: Genesis / Custom / Product / Commodity.

```
User need: {who} needs {need}

| Component | Visibility (1=user-facing … 5=infra) | Evolution stage | Disposition (build/buy/adopt) | Rationale | Hotspot? | ADR |
|-----------|:------------------------------------:|-----------------|-------------------------------|-----------|:--------:|-----|
| {Web UI} | 1 | Product | buy (framework) | undifferentiated; mature ecosystem | — | — |
| {Matching engine} | 2 | Genesis | build | core differentiator | — | ADR-{NNN} |
| {Identity} | 4 | Commodity | adopt-commodity (IdP) | never build auth | ⚠ if build | ADR-{NNN} |
| {Datastore} | 5 | Commodity | buy (managed) | operational leverage | — | — |
```

> Optional: render the value chain × evolution as a Mermaid quadrant/flow per `common/diagram-standards.md`. The table is authoritative; the diagram is an aid.

### Build/Buy Disposition Summary

```
| Disposition | Components | Implication |
|-------------|-----------|-------------|
| Build (custom) | {list} | engineering capacity committed; owned long-term |
| Buy (product/rental) | {list} | dependency to govern; watch lock-in/exit cost |
| Adopt (commodity/utility) | {list} | consume as utility; do not differentiate here |
```

### Tag → Artifact Hand-Off Map

```
| Wardley element | Downstream home | Rule / artifact |
|-----------------|-----------------|-----------------|
| Component disposition | Technology Stack (Stage 6) | WDL-04 · WDL-07 |
| Build/buy decision | ADR | WDL-06 |
| Build-a-commodity hotspot | ADR · Architecture Workbook | WDL-05 |
| Component-evolution note | Architecture Workbook (future reconciliation) | WDL-08 |
```
