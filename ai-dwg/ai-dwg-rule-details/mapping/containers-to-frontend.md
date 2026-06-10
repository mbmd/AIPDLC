# Mapping: Container Design (UI Containers) → frontend-standards.md (CONDITIONAL)

## Purpose

Transforms frontend/UI container definitions from C4 L2 into a steering file governing component patterns, state management, accessibility, and UI conventions.

**Output:** `.kiro/steering/frontend-standards.md`

**Condition:** Generate IF Container Design (C4 L2) includes SPA/UI containers OR BFF Pattern extension was active.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think about frontend architecture as a separate discipline — component patterns, state management, and accessibility require specialized rules
- Enforce accessibility (WCAG) as non-negotiable — it's not a nice-to-have; failing accessibility is failing users
- Separate concerns: server state belongs in query libraries (React Query/SWR), not global stores; forms have their own state management
- Write performance rules with measurable targets — bundle size limits, code splitting requirements, image optimization standards
- Only generate this file when UI containers exist in C4 L2 — don't assume frontend from any other signal

### Anti-Patterns for This Activity
- Do NOT generate frontend-standards.md for backend-only systems — this is strictly conditional on UI containers in C4 L2
- Do NOT write framework-agnostic frontend rules — standards must match the specific UI framework from the AP (React vs Vue vs Angular patterns differ fundamentally)
- Do NOT skip accessibility — WCAG compliance is architecture-level, not a post-launch polish item

### Quality Check
A good output from this activity sounds like:
- "FE-A11Y-01: WCAG 2.1 Level AA compliance target. FE-A11Y-03: ALL interactive elements keyboard-accessible. FE-A11Y-08: EVERY input has associated label — no placeholder-only."
- "FE-STATE-02: Server state managed via React Query — not Redux. FE-STATE-05: NEVER duplicate server data in global state — API is the single source of truth."

---

## Source

**From:** Container Diagram (C4 L2) — UI container definitions
**Also from:** Technology Stack (UI framework), API Architecture (BFF endpoints if applicable)

---

## Target: frontend-standards.md

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Container Design (C4 L2) + Technology Stack | date: {generation-date} -->

# Frontend Standards

## Frontend Identity

**Framework:** {from AP — e.g., React 18 / Vue 3 / Angular 17 / Next.js}
**State management:** {from AP — e.g., Zustand / Redux Toolkit / Pinia / built-in}
**Styling:** {from AP — e.g., Tailwind CSS / CSS Modules / Styled Components}
**Bundler:** {from AP — e.g., Vite / Webpack / Turbopack}
**Testing:** {from AP — e.g., Vitest + Testing Library + Playwright}

---

## Component Architecture

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| FE-COMP-01 | Component structure: {from AP — e.g., atomic design (atoms → molecules → organisms → templates → pages)} |
| FE-COMP-02 | Component file convention: {from AP — e.g., one component per file, co-located styles + tests} |
| FE-COMP-03 | Smart vs. Presentational: separate data-fetching (smart/container) from rendering (presentational/dumb) |
| FE-COMP-04 | Props: typed with {from AP — e.g., TypeScript interfaces / PropTypes} — no `any` types |
| FE-COMP-05 | Component size: max ~200 lines — split if larger |
| FE-COMP-06 | Reusable components: extract to shared library when used in 3+ places |

<!-- end: AP-sourced -->

---

## State Management

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| FE-STATE-01 | Global state: ONLY for truly global concerns (auth, theme, tenant context) |
| FE-STATE-02 | Server state: use {from AP — e.g., React Query / SWR / TanStack Query} — not global store |
| FE-STATE-03 | Form state: use {from AP — e.g., React Hook Form / Formik} — not manual state |
| FE-STATE-04 | Local component state: prefer local over global — lift only when needed |
| FE-STATE-05 | NEVER duplicate server data in global state — single source of truth is the API |

<!-- end: AP-sourced -->

---

## API Communication

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| FE-API-01 | HTTP client: {from AP — e.g., Axios / fetch wrapper} — single configured instance |
| FE-API-02 | Base URL + auth token: configured once in client instance — not repeated per call |
| FE-API-03 | Error handling: global interceptor maps API errors to user-friendly messages |
| FE-API-04 | Loading states: EVERY async operation shows loading indicator |
| FE-API-05 | Optimistic updates: {from AP — e.g., allowed for simple mutations / not used} |
| FE-API-06 | BFF endpoints: {if BFF — call BFF, NEVER call backend services directly from frontend} |

<!-- end: AP-sourced -->

---

## Accessibility (WCAG)

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| FE-A11Y-01 | Target: {from AP — e.g., WCAG 2.1 Level AA compliance} |
| FE-A11Y-02 | Semantic HTML: use correct elements (button, nav, main, article) — not div for everything |
| FE-A11Y-03 | Keyboard navigation: ALL interactive elements must be keyboard-accessible |
| FE-A11Y-04 | ARIA labels: add when semantic HTML isn't sufficient — never redundant ARIA |
| FE-A11Y-05 | Color contrast: meet AA ratio (4.5:1 for text, 3:1 for large text) |
| FE-A11Y-06 | Focus management: visible focus indicators, logical tab order |
| FE-A11Y-07 | Screen reader testing: verify key flows with screen reader before release |
| FE-A11Y-08 | Form labels: EVERY input has associated label — no placeholder-only |

<!-- end: AP-sourced -->

---

## Performance

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| FE-PERF-01 | Bundle size: {from AP — e.g., <200KB initial JS (gzipped)} |
| FE-PERF-02 | Code splitting: lazy-load routes and heavy components |
| FE-PERF-03 | Images: use modern formats (WebP/AVIF), responsive sizes, lazy loading |
| FE-PERF-04 | Memoization: use for expensive computations — not by default on everything |
| FE-PERF-05 | Re-renders: avoid unnecessary — profile with React DevTools (or framework equivalent) |

<!-- end: AP-sourced -->

---

## Testing

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| FE-TEST-01 | Unit tests: test component logic and state (Testing Library approach — test behavior, not implementation) |
| FE-TEST-02 | Integration tests: test page-level flows with mocked API |
| FE-TEST-03 | E2E tests: critical user journeys only (login, main business flow) |
| FE-TEST-04 | Coverage target: {from AP — e.g., 70% for components / no specific target} |
| FE-TEST-05 | Visual regression: {from AP — e.g., Chromatic / Percy / not used} |

<!-- end: AP-sourced -->

---

## Anti-Patterns

1. **NEVER** use `any` type in component props or state
2. **NEVER** make API calls directly in components — use service layer / hooks
3. **NEVER** store sensitive data (tokens) in localStorage — use httpOnly cookies
4. **NEVER** disable ESLint rules inline without documented justification
5. **NEVER** use inline styles for anything beyond truly dynamic values
6. **NEVER** skip loading/error states — every async operation has three states
```

---

## Transformation Rules

| AP Content | Output |
|-----------|--------|
| UI framework from Technology Stack | Frontend Identity |
| Component patterns from C4 L3 (if detailed) | FE-COMP rules |
| State management choice | FE-STATE rules |
| BFF pattern (if extension active) | FE-API-06 |
| Accessibility requirements from Quality Attributes | FE-A11Y rules |
| Performance targets (page load time) | FE-PERF rules |
