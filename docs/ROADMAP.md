# Roadmap — daisy-cotton

**Date:** 2026-09-26

This document was designed against [GOALS.md](../GOALS.md). See also [CONTEXT.md](../CONTEXT.md) for domain terminology and [CONSTITUTION.md](../CONSTITUTION.md) for project standards.

## Versioning

| Version | Gate |
|---------|------|
| `0.0.x` | Building toward the Essential goals. Expect churn. Install from git only; nothing is published. |
| `0.1.0` | All Essential goals delivered. The minimum usable release and the first publish. |
| `0.1.x` → `0.x` | Advancing the Expected goals, at whatever granularity the work takes. Patches are fixes. |
| `1.0.0` | All Expected goals delivered. The complete, dependable release. |
| `1.x` | Stable line: non-breaking fixes and additive features only. |
| `2.0` | Next major: breaking changes. |

A goal is not one minor release. Some take several, and one minor can move two. Once `1.0` ships, a breaking change never goes out as `1.x`; it waits for the next major.

Aspirational goals may be developed against v2 or v1 as required.

## Essential and Expected goals: v0.1.0

Every component, documented in the gallery and accessible, for the first published release.

### R1 — Development environment on the component gallery

*feature · advances G1, G2*

Every later item adds components, and each one has to be seen, documented and linted the same way. This item makes the component gallery the whole development and demo environment before any new component is written, so the first group starts from a working loop rather than building it.

**Deliverables:**

- The demo project is the component gallery alone, running on a bare Cotton and daisyUI page with a theme switcher and no other host package.
- Every existing component carries the gallery annotations the constitution requires.
- The gallery's linter passes with no errors or warnings and runs as part of the test suite, so CI fails when a component breaks it.
- Contributor docs say how to run the gallery and the linter.
- The README, CONTEXT, AGENTS notes, brainstorm, ADR 0001 and CHANGELOG name no other package as a host or consumer.
- The docs record that `alert`'s dismiss button needs Alpine on the page.

Serves G1 and G2. Out of scope: new components, and gallery features the gallery package doesn't already provide.

### R2 — Navigation

*feature · advances G1, G2, G3*

Breadcrumbs, dock, link, megamenu, menu, navbar, pagination, steps and tabs. Breadcrumbs, dock and link exist. Menu and navbar are the frame most pages sit in, so this group sets the attribute pattern the later groups follow.

**Deliverables:**

- A Cotton component for every Navigation component that qualifies under G1, annotated and lint-clean.
- The existing breadcrumbs, dock and link brought in line with the constitution's attribute vocabulary.
- Every component in the group, new or existing, emits accessible markup: labels tied to controls, correct roles and states, keyboard reach and visible focus.
- The group's page in the gallery shows each component's variants and states rendered, so an adopter can choose attributes without opening the template.
- Components in the group that don't qualify are listed with the reason.

Serves G1, G2 and G3. Out of scope: menu configuration and driving pagination from a Django paginator.

### R3 — Layout

*feature · advances G1, G2, G3*

Divider, drawer, footer, hero, indicator, join, mask and stack. Divider exists. Drawer and footer complete the page frame Navigation starts, and join, indicator and stack are how later groups combine components.

**Deliverables:**

- A Cotton component for every Layout component that qualifies under G1, annotated and lint-clean.
- Every component in the group, new or existing, emits accessible markup: labels tied to controls, correct roles and states, keyboard reach and visible focus.
- The group's page in the gallery shows each component's variants and states rendered, so an adopter can choose attributes without opening the template.
- Components in the group that don't qualify are listed with the reason.

Serves G1, G2 and G3. Out of scope: page compositions built from these components.

### R4 — Actions

*feature · advances G1, G2, G3*

Button, dropdown, FAB, modal, swap and theme controller. Button, dropdown and modal exist.

**Deliverables:**

- A Cotton component for every Actions component that qualifies under G1, annotated and lint-clean.
- The existing button, dropdown and modal brought in line with the constitution's attribute vocabulary.
- Every component in the group, new or existing, emits accessible markup: labels tied to controls, correct roles and states, keyboard reach and visible focus.
- The group's page in the gallery shows each component's variants and states rendered, so an adopter can choose attributes without opening the template.
- Components in the group that don't qualify are listed with the reason.

Serves G1, G2 and G3. Out of scope: JavaScript behaviour beyond what daisyUI's CSS provides.

### R5 — Data display

*multi-feature · advances G1, G2, G3*

Accordion, avatar, aura, badge, card, carousel, chat bubble, collapse, countdown, diff, hover 3D card, hover gallery, kbd, list, stat, status, table, text rotate and timeline. Avatar, badge and card exist. Each component ships accessible and shown in the gallery with its variants and states, as in the groups before it.

Serves G1, G2 and G3. Out of scope: rendering querysets or model instances.

### R6 — Feedback

*feature · advances G1, G2, G3*

Alert, loading, progress, radial progress, skeleton, toast and tooltip. Alert exists. Each component ships accessible and shown in the gallery with its variants and states, as in the groups before it.

Serves G1, G2 and G3. Out of scope: wiring toasts or alerts to Django's messages framework.

### R7 — Data input

*multi-feature · advances G1, G2, G3*

Calendar, checkbox, fieldset, file input, filter, label, radio, range, rating, select, text input, textarea, toggle, validator and OTP. `form.field` covers part of fieldset today. Each component ships accessible and shown in the gallery with its variants and states, as in the groups before it.

Serves G1, G2 and G3. Out of scope: rendering Django forms or form fields, which is the project's job.

### R8 — Mockup

*Delivered · needs verification · advances G1*

The browser, code, phone and window mockups all exist, carried over with the first components.

Serves G1.

## Aspirational goals: v2.0

### R9 — Stylesheet carries only the components in use

*multi-feature · advances G4*

A project's built stylesheet includes the daisyUI CSS for the components it actually renders and nothing more.

Serves G4.
