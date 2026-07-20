# EP-001: Core Ticketing Module

## Summary

| Field | Value |
|-------|-------|
| **Epic ID** | EP-001 |
| **Status** | In Progress |
| **Owner** | Product Owner |
| **Stories** | 18 total, 12 done |
| **Priority** | P1 — Critical Path |

## Description

Build the foundational ticketing engine that handles ticket creation, assignment, status transitions, SLA tracking, and basic automation rules.

## Acceptance Criteria

- Tickets can be created via portal, email, and API
- Auto-assignment based on category and availability
- SLA timers start on creation, pause on "waiting" states
- Full audit trail for all state transitions
- Sub-ticket and linked-ticket support
- Bulk operations (assign, close, escalate)

## Stories (12/18 complete)

- [x] Ticket data model and persistence
- [x] Create ticket flow (portal)
- [x] Create ticket flow (email parsing)
- [x] Assignment engine (round-robin + skills)
- [x] Status transition state machine
- [x] SLA timer service
- [x] Notification on assignment
- [x] Notification on SLA warning (80%)
- [x] Ticket search and filtering
- [x] Ticket detail view
- [x] Comments and internal notes
- [x] Attachment support
- [ ] Bulk operations UI
- [ ] Linked tickets
- [ ] Sub-tickets
- [ ] Ticket templates
- [ ] Auto-escalation rules
- [ ] SLA breach webhook

## Dependencies

- Auth service (Azure AD) — resolved
- Notification service — in progress
- Search index (Elasticsearch) — ready

---

*Last updated: 2026-06-15*
