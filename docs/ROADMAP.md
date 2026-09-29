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

*delivered in [#10](https://github.com/SamuelJennings/daisy-cotton/issues/10), [#11](https://github.com/SamuelJennings/daisy-cotton/issues/11) · advances G1, G2*

The demo project is the component gallery alone, on a bare Cotton and daisyUI page with a theme switcher. Every component carries the gallery annotations the constitution requires, the gallery's linter runs in the test suite with no errors or warnings, and the contributor docs say how to run both.

Serves G1 and G2.

### R2 — Navigation

*delivered in [#12](https://github.com/SamuelJennings/daisy-cotton/issues/12) · advances G1, G2, G3*

Breadcrumbs, dock, link, megamenu, menu, navbar, steps and tabs are Cotton components, annotated, lint-clean, accessible and shown in the gallery with their variants and states. Pagination has no component: daisyUI builds it from `join` and `btn`.

Serves G1, G2 and G3. Out of scope: menu configuration and driving pagination from a Django paginator.

### R3 — Layout

*delivered in [#13](https://github.com/SamuelJennings/daisy-cotton/issues/13) · advances G1, G2, G3*

Divider, drawer, footer, hero, indicator, join, mask and stack are Cotton components, annotated, lint-clean, accessible and shown in the gallery with their variants and states.

Serves G1, G2 and G3. Out of scope: page compositions built from these components.

### R4 — Actions

*delivered in [#14](https://github.com/SamuelJennings/daisy-cotton/issues/14) · advances G1, G2, G3*

Button, dropdown, FAB, modal and swap are Cotton components, annotated, lint-clean, accessible and shown in the gallery with their variants and states. The theme controller is a swap with the `theme-controller` class on its checkbox, so it has no component of its own.

Serves G1, G2 and G3. Out of scope: JavaScript behaviour beyond what daisyUI's CSS provides.

### R5 — Data display

*delivered in [#15](https://github.com/SamuelJennings/daisy-cotton/issues/15), [#16](https://github.com/SamuelJennings/daisy-cotton/issues/16) · advances G1, G2, G3*

Accordion, avatar, badge, card, carousel, chat bubble, collapse, countdown, diff, hover 3D card, hover gallery, kbd, list, stat, status, table, text rotate and timeline are Cotton components, accessible and shown in the gallery with their variants and states. Aura only decorates another element, so it has no component.

Serves G1, G2 and G3. Out of scope: rendering querysets or model instances.

### R6 — Feedback

*delivered in [#17](https://github.com/SamuelJennings/daisy-cotton/issues/17) · advances G1, G2, G3*

Alert, loading, progress, radial progress, skeleton, toast and tooltip are Cotton components, accessible and shown in the gallery with their variants and states.

Serves G1, G2 and G3. Out of scope: wiring toasts or alerts to Django's messages framework.

### R7 — Data input

*delivered in [#18](https://github.com/SamuelJennings/daisy-cotton/issues/18), [#19](https://github.com/SamuelJennings/daisy-cotton/issues/19) · advances G1, G2, G3*

Every data-input component is a Cotton component under the `form.` namespace: calendar, checkbox, fieldset, file input, filter, label, OTP, radio, range, rating, select, text input, textarea and toggle, each accessible and shown in the gallery with its variants and states. The calendar emits the markup daisyUI styles for Cally, which the project loads. Validator has no component: it is a class added to a control.

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
