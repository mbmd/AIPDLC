# EP-001: Core Request Module

## Summary

| Field | Value |
|-------|-------|
| **Epic ID** | EP-001 |
| **Status** | In Progress |
| **Owner** | Product Owner |
| **Stories** | 18 total, 12 done |
| **Priority** | P1 — Critical Path |

## Description

Build the foundational request engine that handles request creation, assignment, status transitions, SLA tracking, and basic automation rules.

## Acceptance Criteria

- Requests can be created via portal, email, and API
- Auto-assignment based on category and availability
- SLA timers start on creation, pause on "waiting" states
- Full audit trail for all state transitions
- Sub-request and linked-request support
- Bulk operations (assign, close, escalate)

## Stories (12/18 complete)

- [x] Request data model and persistence
- [x] Create request flow (portal)
- [x] Create request flow (email parsing)
- [x] Assignment engine (round-robin + skills)
- [x] Status transition state machine
- [x] SLA timer service
- [x] Notification on assignment
- [x] Notification on SLA warning (80%)
- [x] Request search and filtering
- [x] Request detail view
- [x] Comments and internal notes
- [x] Attachment support
- [ ] Bulk operations UI
- [ ] Linked requests
- [ ] Sub-requests
- [ ] Request templates
- [ ] Auto-escalation rules
- [ ] SLA breach webhook

## Dependencies

- Auth service (SSO) — resolved
- Notification service — in progress
- Search index — ready

---

*Last updated: 2026-06-15*
