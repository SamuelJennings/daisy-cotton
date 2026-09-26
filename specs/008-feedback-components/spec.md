# Feature Specification: Feedback components

**Feature Branch**: `008-feedback-components`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2, G3 · **Roadmap**: R6 · **Depends on**: #11 (gallery annotations and the lint check in CI)

**Input**: Issue #17, "Feedback components": alert, loading, progress, radial progress, skeleton, toast and tooltip as Cotton components. Alert already exists. Each should be accessible and shown in the gallery with its variants and states.

## Scope

daisyUI's Feedback group has seven members, and each one gets a Cotton component:

| Component | State today | This feature |
|---|---|---|
| Alert | exists | brought to the attribute vocabulary and the accessibility bar |
| Loading | missing | new |
| Progress | missing | new |
| Radial progress | missing | new |
| Skeleton | missing | new |
| Toast | missing | new |
| Tooltip | missing | new |

Out of scope:

- Any JavaScript. The alert's dismiss button still relies on Alpine.js, which the host project loads. The package does not ship it.
- Wiring toasts or alerts to Django's messages framework. A project loops over its messages and renders `<c-alert>` inside `<c-toast>` itself.
- Stacking, queueing or timing toasts. The toast is daisyUI's positioning wrapper and nothing more.

## Clarifications

### Session 2026-09-26

- Q: Does the alert keep its Alpine-driven dismiss button and `delay`? → A: Yes, both. Neither works without Alpine.js on the page, and the README already says so. The dismiss button is now drawn by `<c-button>`, has the translatable accessible name "Dismiss", and hides its ✕ glyph from assistive technology. The documentation warns against `delay` on messages the reader has to act on, because the message can disappear before some people have read it.
- Q: Should every alert be announced as urgent? → A: No. The alert keeps daisyUI's `role="alert"` by default, and a caller can pass `role="status"` for a message that should be announced politely. The component emits exactly one `role`.
- Q: How does the alert take daisyUI's direction modifiers? → A: As `horizontal` and `vertical`, each taking either a boolean or a breakpoint name, the convention the navigation and layout groups use. `horizontal="sm"` gives `sm:alert-horizontal`, daisyUI's own responsive pattern.
- Q: Loading has six mutually exclusive animations. One attribute or six booleans? → A: Six booleans named as daisyUI names them (`spinner`, `dots`, `ring`, `ball`, `bars`, `infinity`), per Article XIV's rule for style modifiers. Unlike the mask's fourteen shapes, all six are plain words. With none given, daisyUI draws the spinner.
- Q: Loading, radial progress and skeleton have no daisyUI colour classes. Do they take `variant`? → A: No. Article XIV reserves `variant` for daisyUI's colour modifier, and these components have none. daisyUI colours them with text or background utilities, which pass through `class`.
- Q: How are the radial progress's size and thickness set? → A: Through the `--size` and `--thickness` CSS variables daisyUI documents, set by the caller with a class such as `[--size:8rem]`. The component does not take `size`, because Article XIV reserves it for the `xs`–`xl` scale and daisyUI gives radial progress no size class.
- Q: What gives loading, progress and radial progress an accessible name? → A: A `label` attribute, the name the swap already uses for an accessible name. Loading defaults to the translatable "Loading". Progress and radial progress have no default, and the documentation says to give one.
- Q: The skeleton's modifier is `skeleton-text`, but `text` on the button and dropdown means "the content". Which meaning wins? → A: Both work. `text` given as a bare attribute adds `skeleton-text` to the slot content. `text` given a string adds `skeleton-text` and renders that string as the content. Either way it is daisyUI's text skeleton, and `text="Loading data…"` reads the way it does on a button.
- Q: Is a skeleton read out by assistive technology? → A: A shape skeleton is not. It is hidden, because it carries no information. A text skeleton is read, because its text is the only thing on screen saying the content is loading.
- Q: Does the toast announce its contents? → A: No. The toast is a positioning wrapper with no role of its own. The alerts inside it carry their own roles, and a live region on the wrapper as well would announce each message twice.
- Q: How does a tooltip reach assistive technology, given that daisyUI's `data-tip` text lives in CSS and is not reliably read? → A: The tooltip text always renders as daisyUI's `tooltip-content` element with `role="tooltip"`, never as `data-tip`. That puts the text in the page, where a screen reader can find it. The component cannot add `aria-describedby` to a trigger it receives as a slot, so `id` goes on the content element and the documentation shows the trigger pointing at it.
- Q: How is the tooltip's placement named? → A: `placement`, taking one side (top, bottom, left, right) and one alignment (start, center, end), the same shape as the dropdown's. The toast's `placement` works the same way with its own values.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Alert (Priority: P1)

A developer shows the result of an action, such as "Saved" or "Payment failed", in the colour and style daisyUI offers, with an optional icon and an optional dismiss button, using the same attribute names as every other component here.

**Why this priority**: Nearly every application reports success and failure, and the alert is the only feedback component that exists today. The toast is built around it.

**Independent Test**: Render `<c-alert>` with each attribute and check the classes, role and children it emits. Open the alert's gallery entry and see every colour, style, direction and the dismissible state.

**Acceptance Scenarios**:

1. **Given** `<c-alert variant="success" soft>Saved.</c-alert>`, **When** it renders, **Then** it is a `<div role="alert">` carrying `alert`, `alert-success` and `alert-soft`, with "Saved." as its content.
2. **Given** `outline` or `dash`, **When** it renders, **Then** the root carries `alert-outline` or `alert-dash`.
3. **Given** `vertical`, **When** it renders, **Then** the root carries `alert-vertical`. **Given** `vertical horizontal="sm"`, **Then** it carries `alert-vertical` and `sm:alert-horizontal`.
4. **Given** `role="status"`, **When** it renders, **Then** the root carries `role="status"` and no other role.
5. **Given** `icon="..."`, or a `variant` with no `icon`, **When** it renders, **Then** `<c-icon>` draws the icon before the content and the icon is hidden from assistive technology.
6. **Given** `dismissible`, **When** it renders, **Then** a `<c-button>` dismiss control follows the content with the translatable accessible name "Dismiss", and in a browser with Alpine.js loaded, activating it by pointer or keyboard removes the alert.
7. **Given** `class="mt-4" data-test="x"`, **When** it renders, **Then** `mt-4` is in the root's own class list and `data-test="x"` is on the root.
8. **Given** the alert's gallery entry, **When** a developer opens it, **Then** every colour, every style (plain, soft, outline, dash), both directions, a responsive direction, an alert with an icon and a dismissible alert are shown.

---

### User Story 2 - Loading (Priority: P1)

A developer shows that something is in progress, inside a button while a form submits or in place of content still arriving, in any of daisyUI's animations and sizes. Screen-reader users hear that something is loading.

**Why this priority**: Every form submit and every slow request needs a busy indicator.

**Independent Test**: Render `<c-loading>` with each animation and size and check the classes, role and accessible name.

**Acceptance Scenarios**:

1. **Given** `<c-loading />`, **When** it renders, **Then** it is a `<span>` carrying `loading`, with `role="status"` and the translatable accessible name "Loading".
2. **Given** `dots size="lg"`, **When** it renders, **Then** it carries `loading-dots` and `loading-lg`, and each of spinner, dots, ring, ball, bars and infinity maps to its daisyUI class.
3. **Given** `label="Saving"`, **When** it renders, **Then** its accessible name is "Saving".
4. **Given** `class="text-primary"`, **When** it renders, **Then** `text-primary` is in the root's class list and the animation takes the primary colour.
5. **Given** a loading indicator in a button's slot, **When** it renders, **Then** it sits inside the button and the button stays a single control.
6. **Given** the loading gallery entry, **When** a developer opens it, **Then** every animation at every size is shown, plus a coloured example and one inside a button.

---

### User Story 3 - Tooltip (Priority: P2)

A developer explains a control, such as an icon-only button, with a short hint that appears on hover and on keyboard focus, on any side of the control, in any daisyUI colour. Screen-reader users can reach the hint too.

**Why this priority**: Tooltips explain icon-only controls in most applications, and the FAB's gallery entry uses them.

**Independent Test**: Render `<c-tooltip>` around a button, hover it and tab to it in a browser, and check the hint appears both ways and is in the accessibility tree.

**Acceptance Scenarios**:

1. **Given** `<c-tooltip tip="Copy link">` wrapping a `<c-button>`, **When** it renders, **Then** the root carries `tooltip`, wraps the button, and holds a `tooltip-content` element with `role="tooltip"` and the text "Copy link".
2. **Given** a rendered tooltip in a browser, **When** the pointer rests on the trigger or a keyboard user tabs to it, **Then** the hint appears.
3. **Given** `placement="bottom end"`, **When** it renders, **Then** the root carries `tooltip-bottom` and `tooltip-end`, and every side and alignment maps to its daisyUI class.
4. **Given** `variant="error"`, **When** it renders, **Then** the root carries `tooltip-error`.
5. **Given** `open`, **When** it renders, **Then** the root carries `tooltip-open` and the hint shows without hover or focus.
6. **Given** a `content` slot, **When** it renders, **Then** the slot content fills the `tooltip-content` element in place of `tip`.
7. **Given** `id="copy-hint"`, **When** it renders, **Then** the `tooltip-content` element carries that id, so the trigger can reference it with `aria-describedby`.
8. **Given** the tooltip's gallery entry, **When** a developer opens it, **Then** every side, alignment and colour, the open state, rich content, and an icon-only button with both an accessible name and a tooltip describing it are shown.

---

### User Story 4 - Progress and radial progress (Priority: P2)

A developer shows how far a task has got, as a bar or as a ring with the percentage in its centre, or as a bar that only shows work is under way when the total is unknown. Screen-reader users hear the value.

**Why this priority**: Uploads, imports and multi-step forms need it, though fewer pages need it than need an alert or a loading indicator.

**Independent Test**: Render `<c-progress>` and `<c-radial-progress>` with values and labels and check the elements, classes, values and accessible names.

**Acceptance Scenarios**:

1. **Given** `<c-progress value="40" label="Upload" variant="primary" />`, **When** it renders, **Then** it is a native `<progress>` carrying `progress` and `progress-primary`, with `value="40"`, `max="100"` and the accessible name "Upload".
2. **Given** `max="5" value="2"`, **When** it renders, **Then** it carries those values.
3. **Given** a progress with no `value`, **When** it renders, **Then** it has no `value` attribute, so the browser shows daisyUI's indeterminate animation and reports no value.
4. **Given** each of neutral, primary, secondary, accent, info, success, warning and error, **When** it renders, **Then** the bar carries that colour's daisyUI class.
5. **Given** `<c-radial-progress value="70" label="Profile complete" />`, **When** it renders, **Then** it is a `<div>` carrying `radial-progress`, with `role="progressbar"`, `--value:70`, `aria-valuenow="70"`, `aria-valuemin="0"`, `aria-valuemax="100"`, the accessible name "Profile complete" and the visible text "70%".
6. **Given** a radial progress with slot content, **When** it renders, **Then** the slot replaces the visible "70%" text and the value attributes are unchanged.
7. **Given** a radial progress with `class="[--size:8rem] text-primary"` and a `style` attribute, **When** it renders, **Then** both classes are on the root, and the caller's style is kept alongside `--value` rather than replacing it.
8. **Given** the gallery entries, **When** a developer opens them, **Then** progress shows every colour, several values and the indeterminate state, and radial progress shows several values, a custom size and thickness, a coloured ring and custom centre content.

---

### User Story 5 - Toast (Priority: P2)

A developer pins one or more messages to a corner or edge of the screen, usually alerts reporting what just happened, wherever the layout has room.

**Why this priority**: Toasts are the usual home for flash messages after a redirect. They only arrange alerts, so they follow the alert in priority.

**Independent Test**: Render `<c-toast>` holding two `<c-alert>`s in each placement and check the classes and that the alerts stack in the chosen position.

**Acceptance Scenarios**:

1. **Given** `<c-toast>` holding two alerts, **When** it renders, **Then** the root carries `toast`, contains both alerts in order, and sits in daisyUI's default position (bottom end).
2. **Given** `placement="top center"`, **When** it renders, **Then** the root carries `toast-top` and `toast-center`, and each of top, middle and bottom and each of start, center and end maps to its daisyUI class.
3. **Given** a toast, **When** it renders, **Then** it carries no role or live-region attribute of its own, and each alert inside keeps its own role.
4. **Given** a toast holding a dismissible alert, **When** the alert is dismissed in a browser with Alpine.js loaded, **Then** the remaining alerts stay in place.
5. **Given** the toast's gallery entry, **When** a developer opens it, **Then** every placement is shown with stacked alerts, including a dismissible one, and the documentation shows a project rendering its own messages into a toast.

---

### User Story 6 - Skeleton (Priority: P3)

A developer fills the space of content that has not arrived yet, such as a card, an avatar or a paragraph, with placeholder shapes or placeholder text sized with utility classes.

**Why this priority**: A polish item. Many applications use a loading indicator instead, or no placeholder at all.

**Independent Test**: Render `<c-skeleton>` as a shape and as text and check the classes and what assistive technology is told.

**Acceptance Scenarios**:

1. **Given** `<c-skeleton class="h-32 w-full" />`, **When** it renders, **Then** it is a `<div>` carrying `skeleton`, `h-32` and `w-full`, hidden from assistive technology.
2. **Given** `<c-skeleton text="Loading data…" />`, **When** it renders, **Then** it carries `skeleton` and `skeleton-text`, its content is "Loading data…", and it is not hidden from assistive technology.
3. **Given** `<c-skeleton text>Loading data…</c-skeleton>`, **When** it renders, **Then** the result is the same as in scenario 2.
4. **Given** the skeleton's gallery entry, **When** a developer opens it, **Then** a shape, a text skeleton and a composed card placeholder (image, avatar and text lines) are shown.

---

### Edge Cases

- A `variant`, `size` or `placement` value daisyUI does not define for that component emits no class for it and raises no error.
- An alert given more than one style (`soft` and `outline`) emits every class given. The component does not pick between them.
- An alert with `dismissible` on a page without Alpine.js renders its dismiss button, and the button does nothing. The README says so.
- An alert whose `variant` has no matching icon in the project's `<c-icon>` renders an empty, hidden icon element. That is the icon extension point working as ADR 0001 describes.
- `delay` removes the alert after the given time whether or not anyone has read it. The documentation warns against using it on errors or on anything the reader must act on.
- A progress `value` greater than `max`, or a radial progress `value` outside 0–100, is rendered as given. The browser and daisyUI limit the drawing, and the documentation states the ranges.
- A progress or radial progress with no `label` has no accessible name, and the component cannot invent one. The documentation and every gallery example give one.
- A tooltip on an element that cannot take focus, such as plain text, shows on hover only. The documentation says to wrap a focusable trigger.
- A tooltip cannot be dismissed with Escape while its trigger keeps focus. That takes a script, which the project supplies if it needs one.
- The tooltip is a description, not a name. An icon-only button inside a tooltip still needs its own `aria-label`, and the gallery shows both.
- Two toasts with the same placement overlap. Placing them is the project's job.
- A toast with no content renders an empty wrapper that takes no visible space.

## Requirements *(mandatory)*

### Functional Requirements

**Every component in the group**

- **FR-001**: Alert, loading, progress, radial progress, skeleton, toast and tooltip MUST each exist as a Cotton component (`<c-alert>`, `<c-loading>`, `<c-progress>`, `<c-radial-progress>`, `<c-skeleton>`, `<c-toast>`, `<c-tooltip>`) emitting the markup and classes daisyUI documents. *(US1–US6)*
- **FR-002**: Each MUST follow Article XIV: `variant` for colour where daisyUI has colour classes, `size` on daisyUI's `xs`–`xl` scale where daisyUI has size classes, daisyUI's modifier names as boolean attributes, `placement` for placement, `horizontal` and `vertical` for direction (each taking a boolean or a breakpoint name), `class` merged into the root element's class list, and every other attribute passed through to the root element unless this spec names another element for it. *(US1–US6)*
- **FR-003**: Each MUST take its colours from daisyUI's semantic roles only, and MUST NOT emit a literal colour or a class daisyUI does not define for that component. *(US1–US6)*
- **FR-004**: Each MUST carry the gallery annotations Article XVI requires, and `cotton_lint --warnings-as-errors` MUST pass. *(US1–US6)*
- **FR-005**: Each MUST have a gallery entry that renders its variants and states, so a developer can choose attributes without reading the template. *(US1–US6)*
- **FR-006**: Each MUST emit accessible markup by default: correct roles, states and values, keyboard reach for anything interactive, and a visible focus indicator. Decorative icons and shapes MUST be hidden from assistive technology. Every accessible name the package writes itself MUST be translatable. *(US1–US6)*
- **FR-007**: A component that draws an icon or a button MUST do so through `<c-icon>` or `<c-button>` (Article XV). *(US1)*
- **FR-008**: The package MUST ship no JavaScript for this group. *(US1–US6)*
- **FR-009**: Every change to the alert's existing attributes or markup MUST be listed in the CHANGELOG, and the README MUST list the new components and describe the alert as it now is, including its Alpine.js requirement. *(US1–US6)*

**Alert**

- **FR-010**: `<c-alert>` MUST render a `<div>` carrying `alert` with `role="alert"` by default. A caller-given `role` MUST replace it, so exactly one `role` is emitted. *(US1)*
- **FR-011**: `variant` MUST accept info, success, warning and error. `soft`, `outline` and `dash` MUST map to their daisyUI classes. `horizontal` and `vertical` MUST map to `alert-horizontal` and `alert-vertical`, behind a breakpoint prefix when given a breakpoint name. *(US1)*
- **FR-012**: `icon`, or `variant` when no `icon` is given, MUST be drawn by `<c-icon>` before the default slot and hidden from assistive technology. *(US1)*
- **FR-013**: `dismissible` MUST render a dismiss control drawn by `<c-button>` after the default slot, with the translatable accessible name "Dismiss" and its glyph hidden from assistive technology, which removes the alert when Alpine.js is on the page. `delay` MUST keep removing the alert after the given number of milliseconds under the same condition. *(US1)*

**Loading**

- **FR-014**: `<c-loading>` MUST render a `<span>` carrying `loading`, with `role="status"` and an accessible name from `label`, defaulting to the translatable "Loading". *(US2)*
- **FR-015**: `spinner`, `dots`, `ring`, `ball`, `bars` and `infinity` MUST map to their `loading-*` classes, and `size` MUST map to `loading-xs` through `loading-xl`. *(US2)*

**Tooltip**

- **FR-016**: `<c-tooltip>` MUST render a wrapper carrying `tooltip` around the default slot (the trigger), and a `tooltip-content` element with `role="tooltip"` holding `tip` or, when given, the `content` slot. It MUST NOT use `data-tip`. *(US3)*
- **FR-017**: `placement` MUST accept one side (top, bottom, left, right) and one alignment (start, center, end), each mapped to daisyUI's tooltip class. `variant` MUST map to daisyUI's seven tooltip colours, and `open` to `tooltip-open`. *(US3)*
- **FR-018**: `id` MUST land on the `tooltip-content` element, not the wrapper. The documentation MUST show a trigger referencing it with `aria-describedby`. *(US3)*

**Progress and radial progress**

- **FR-019**: `<c-progress>` MUST render a native `<progress>` carrying `progress`, with `max` defaulting to 100, `value` when given and omitted otherwise, `variant` mapped to daisyUI's eight progress colours, and an accessible name from `label`. *(US4)*
- **FR-020**: `<c-radial-progress>` MUST render a `<div>` carrying `radial-progress` with `role="progressbar"`, the `--value` CSS variable, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`, and an accessible name from `label`. `value` MUST be required. *(US4)*
- **FR-021**: The radial progress MUST show the value followed by "%" by default, and the default slot MUST replace that text. A caller's `style` attribute MUST be combined with `--value`, not replace it. *(US4)*

**Toast**

- **FR-022**: `<c-toast>` MUST render a `<div>` carrying `toast` around the default slot, with no role or live-region attribute of its own. *(US5)*
- **FR-023**: `placement` MUST accept one vertical position (top, middle, bottom) and one horizontal position (start, center, end), each mapped to daisyUI's toast placement class. *(US5)*

**Skeleton**

- **FR-024**: `<c-skeleton>` MUST render a `<div>` carrying `skeleton`, hidden from assistive technology unless `text` is given. *(US6)*
- **FR-025**: `text` MUST add `skeleton-text`. When `text` carries a string, that string MUST be rendered as the content. Otherwise the default slot is the content. *(US6)*

### Key Entities

- **Accessible name**: what assistive technology announces for a component. The package writes one only where it knows it ("Loading", "Dismiss"). Everywhere else the caller supplies it through `label` or `aria-label`.
- **Trigger**: the element a tooltip describes. It arrives in the tooltip's slot, so the component can wrap it but not change it.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every class daisyUI lists for alert, loading, progress, radial progress, skeleton, toast and tooltip is reachable through a documented attribute or slot.
- **SC-002**: `cotton_lint --warnings-as-errors` reports zero errors and zero warnings for all seven components.
- **SC-003**: None of the seven components ships a script. The alert's dismiss button and `delay` are the only behaviour that needs one, and the README names it.
- **SC-004**: Every gallery example of loading, progress, radial progress and tooltip exposes a name or value to assistive technology, and every component's gallery entry shows each of its variants and states.
- **SC-005**: A developer upgrading from the previous alert finds every change to its attributes and markup in the CHANGELOG.

## Assumptions

- #11 lands first, so the gallery annotations, the lint check in CI and the documentation on running the gallery already exist.
- The host project runs daisyUI 5, the version whose class reference this spec follows.
- The package is below 0.1.0, so breaking changes to the alert are acceptable when the CHANGELOG lists them.
- `<c-button>` and `<c-icon>` are the components the alert calls. Changes to their attributes in other features do not change what this feature asks of them.
- The demo loads Alpine.js, so the dismissible alert works in the gallery.
