<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: User Story Mapping (Opt-In Prompt)

**Trigger:** User mentions "story map", "user story mapping", "walking skeleton", "journey backbone", or "slice releases by activity"
**Stage:** 4 (Product Discovery & Roadmap) — the map is built here; its release slices feed Stage 7 (Release & Increment Slicing)

---

## When This Extension Applies

A story map helps when:
- The backlog is a flat list and it is hard to see the end-to-end user journey or what a coherent release actually contains
- You need to carve a genuine MVP (a thin walking skeleton across the whole journey) rather than "the top N ranked items"
- Stakeholders disagree about scope and need a shared, visual picture of activities → tasks → releases
- Epics exist but the narrative flow that connects them (what the user does, and in what order) is implicit

Skip it if: the product is a single small capability, or release boundaries are already obvious from the ranked backlog.

## Detection

Present this prompt if any of the following are true:
- The user explicitly asks for a story map / walking skeleton / journey-based slicing
- Depth = Comprehensive and the roadmap spans multiple user activities or releases
- Stage 7 is approaching and the MVP / release boundaries are still unclear

## Activation Prompt

```
I detect you'd benefit from the User Story Mapping extension.

This adds to Stage 4:
• A journey backbone — user activities arranged left-to-right in narrative order
• Task/story decomposition — stories ranked top-to-bottom under each activity
• Release slices — horizontal cuts across the map, walking skeleton first
• A story-map.md artifact that seeds MVP + release grouping in Stage 7

Useful for turning a flat backlog into a plannable shape, carving a true MVP,
and giving stakeholders a shared visual of scope.

Activate User Story Mapping? (yes/no)
```

If yes → load `user-story-mapping.md`

## Relationship to Other Stages & Extensions

- **Feeds Stage 7 (Release & Increment Slicing):** the map's release slices become the MVP and the release grouping — the story map is never a dead artifact; its walking skeleton seeds Steps 7.1–7.2.
- **Complements Advanced Discovery:** when OKRs / JTBD are active, backbone activities trace up to jobs and goals — story mapping arranges the *what and when*, advanced discovery frames the *why*.
- **Complements Tier 2 (Story Elaboration):** stories placed on the map are elaborated into INVEST + Given/When/Then when Tier 2 is active.
