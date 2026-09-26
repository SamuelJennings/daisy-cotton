# Feature Specification: Action components

**Feature Branch**: `005-action-components`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2, G3 · **Roadmap**: R4 · **Depends on**: #11 (gallery annotations and the lint check in CI)

**Input**: Issue #14, "Action components": button, dropdown, FAB, modal and swap as Cotton components. Button, dropdown and modal already exist and are brought in line with the constitution's attribute vocabulary. Each is accessible and shown in the gallery with its variants and states.

## Scope

daisyUI's Actions group has six members. Five get a Cotton component:

| Component | State today | This feature |
|---|---|---|
| Button | exists | brought to the attribute vocabulary and the accessibility bar |
| Dropdown | exists | brought to the attribute vocabulary and the accessibility bar |
| Modal | exists | brought to the attribute vocabulary and the accessibility bar |
| FAB | missing | new |
| Swap | missing | new |

**Theme controller is excluded.** daisyUI defines it as a class added to a checkbox, radio or toggle input, so it modifies other components and gets no Cotton component of its own (README, *Scope & philosophy*). The swap's documentation shows how to build a theme toggle from it instead (FR-024).

Out of scope: any JavaScript. Where a component needs behaviour daisyUI's CSS does not give, the component emits the markup daisyUI documents and the host project supplies the script.

## Clarifications

### Session 2026-09-26

- Q: Which of the button's current attributes survive? → A: The ones that name a daisyUI modifier, plus `text`, `icon` and `href`. `full` becomes `block` (daisyUI's name). `align`, `reverse` and `condition` are removed: layout classes pass through `class`, an icon after the text goes in the default slot, and a conditional button is an `{% if %}` around the tag. The removals and the rename are listed in the CHANGELOG.
- Q: How does the dropdown open without script, and how does it tell assistive technology whether it is open? → A: With the popover method daisyUI documents first: the trigger is a button that targets a popover panel. The browser then handles opening by click and keyboard, closing on Escape or a click outside, and reporting the open state, with no script. The trigger stays a `<c-button>`.
- Q: Does the dropdown keep `hover`? → A: No. daisyUI's rules for the popover method allow only the button and the `dropdown` class, and hover-to-open needs the older focus method, which cannot report whether the panel is open. `dropdown-open` and `dropdown-close` are not offered for the same reason. A project that wants hover-to-open overrides the component.
- Q: What are the dropdown's placement and the modal's position called? → A: `placement`, daisyUI's own name for both class groups. It replaces the dropdown's `valign` and `halign` and the modal's `position`. A dropdown takes one side and one alignment together, for example `placement="top end"`.
- Q: Does the modal keep wrapping its content in a card? → A: No. It renders daisyUI's own modal structure, a box with an actions row. It keeps a `title`, which becomes the heading that names the dialog. The card-only slots (`footer`, `footer_end`) and the `icon` attribute go. A project that wants a card inside a modal puts `<c-card>` in the default slot.
- Q: Does the modal keep `size`? → A: No. daisyUI has no modal size modifier, and the constitution reserves `size` for daisyUI's size scale. Width comes from classes on the box.
- Q: Which element receives `class` and pass-through attributes when a component has an inner surface (the dropdown panel, the modal box, the swap checkbox)? → A: The root element, per Article XIV. The dropdown panel and the modal box accept extra classes through `content_class`, the name the dropdown already uses for its panel.
- Q: Which swap attributes reach the checkbox rather than the wrapper? → A: The control's state and form attributes (`checked`, `disabled`, `name`, `value`) and its accessible name. Everything else goes to the wrapper.
- Q: What does the FAB's trigger look like by default? → A: daisyUI's documented FAB trigger, a large circular button. As with the dropdown, `<c-button>` draws the trigger from attributes forwarded to it, and a `button` slot replaces it entirely.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Button (Priority: P1)

A developer building any page needs buttons, and links styled as buttons, in every colour, size and style daisyUI offers, using the same attribute names as every other component here.

**Why this priority**: The button is the most used component in any application, and the dropdown and FAB draw their triggers with it. Its attribute changes are breaking, so they land first.

**Independent Test**: Render `<c-button>` with each attribute and check the classes and attributes on the element it emits. Open the button's gallery entry and see every variant, size, style and state.

**Acceptance Scenarios**:

1. **Given** `<c-button variant="primary" size="xl" soft>Save</c-button>`, **When** it renders, **Then** it is a `<button>` carrying `btn`, `btn-primary`, `btn-xl` and `btn-soft`, with "Save" as its content.
2. **Given** `<c-button href="/next" text="Next">`, **When** it renders, **Then** it is an `<a>` with that `href` and the `btn` class.
3. **Given** `<c-button disabled>`, **When** it renders, **Then** it is a `<button>` with the native `disabled` attribute.
4. **Given** `<c-button href="/next" disabled>`, **When** it renders, **Then** the link carries `btn-disabled`, `aria-disabled="true"`, `role="button"` and `tabindex="-1"`, so it is announced as disabled and Tab skips it.
5. **Given** `<c-button icon="..." circle aria-label="Add">`, **When** it renders, **Then** the icon is hidden from assistive technology and the button's accessible name is "Add".
6. **Given** `<c-button class="mt-4" data-test="x">`, **When** it renders, **Then** `mt-4` is in the element's own class list and `data-test="x"` is on the element.
7. **Given** the button's gallery entry, **When** a developer opens it, **Then** every colour, size, style (outline, dash, soft, ghost, link), behaviour (active, disabled) and modifier (wide, block, square, circle) is shown rendered, including an icon-only button with its accessible name.

---

### User Story 2 - Modal (Priority: P2)

A developer needs a dialog for confirmations and short forms. It opens from a button, keeps focus inside while open, closes on Escape, and is announced with a name.

**Why this priority**: Nearly every application needs a confirmation dialog, and the existing modal's structure and attributes change, so adopters need the new shape early.

**Independent Test**: Render `<c-modal>` with a title, body and actions, open it in a browser with a trigger, and check it is named, closes on Escape and on the backdrop, and returns focus to the trigger.

**Acceptance Scenarios**:

1. **Given** `<c-modal id="confirm" title="Delete item?">…</c-modal>`, **When** it renders, **Then** it is a `<dialog>` with id `confirm` and the `modal` class, its box contains the body, and the heading "Delete item?" names the dialog.
2. **Given** a modal with an `actions` slot, **When** it renders, **Then** the actions appear in daisyUI's actions row at the foot of the box.
3. **Given** `placement="bottom"`, **When** it renders, **Then** the dialog carries `modal-bottom`, and each of top, middle, bottom, start and end maps to its daisyUI class.
4. **Given** `closable`, **When** it renders, **Then** a close button with the translatable accessible name "Close" closes the dialog without script.
5. **Given** an open modal, **When** the user presses Escape or clicks the backdrop, **Then** it closes and focus returns to the element that opened it.
6. **Given** `open`, **When** the page loads, **Then** the modal is already shown, so a server can re-render a dialog after a failed form submission.
7. **Given** the modal's gallery entry, **When** a developer opens it, **Then** each placement, the closable variant and a modal with actions can each be opened from a trigger button, and the entry shows how the trigger opens the dialog.

---

### User Story 3 - Dropdown (Priority: P2)

A developer needs a button that opens a menu or panel on any side of it. Keyboard and screen-reader users can open it, use it and close it, with no script.

**Why this priority**: Dropdowns carry account menus, row actions and filters in most applications. The move to the popover method affects every existing use.

**Independent Test**: Render `<c-dropdown text="Options">` with a menu in its slot, open and close it by keyboard and pointer in a browser, and check the trigger reports its state.

**Acceptance Scenarios**:

1. **Given** `<c-dropdown text="Options" variant="primary">…</c-dropdown>`, **When** it renders, **Then** `<c-button>` draws the trigger with that text and colour, and the trigger targets the panel holding the slot content.
2. **Given** two dropdowns on one page with no `id` given, **When** they render, **Then** each trigger opens its own panel and never the other's.
3. **Given** a rendered dropdown in a browser, **When** a keyboard user focuses the trigger and presses Enter or Space, **Then** the panel opens and the trigger reports it as expanded. Escape closes it and returns focus to the trigger.
4. **Given** an open dropdown, **When** the user clicks outside it, **Then** it closes.
5. **Given** `placement="top end"`, **When** it renders, **Then** the panel carries `dropdown-top` and `dropdown-end`, and every side (top, bottom, left, right) and alignment (start, center, end) maps to its daisyUI class.
6. **Given** a `button` slot, **When** it renders, **Then** the slot content replaces the default trigger, and the documentation states what a custom trigger must carry to open the panel.
7. **Given** the dropdown's gallery entry, **When** a developer opens it, **Then** each placement, a menu panel, a non-menu panel and a custom trigger are shown working.

---

### User Story 4 - Swap (Priority: P3)

A developer needs a control that flips between two pieces of content, such as a sun and a moon or play and pause, driven by a checkbox and carrying a name assistive technology can read.

**Why this priority**: Less common than the components above, but it is the usual way to build a theme toggle, which this package deliberately does not ship.

**Independent Test**: Render `<c-swap>` with `on` and `off` slots and a label, toggle it in a browser by pointer and keyboard, and check the content flips and the control is named.

**Acceptance Scenarios**:

1. **Given** `<c-swap label="Dark mode">` with `on` and `off` slots, **When** it renders, **Then** it is daisyUI's swap markup: a wrapper with the `swap` class, a checkbox, and the two slots in `swap-on` and `swap-off`.
2. **Given** a rendered swap, **When** a keyboard user tabs to it and presses Space, **Then** the content flips, the control shows a visible focus indicator, and it is announced as a checkbox named "Dark mode" with its checked state.
3. **Given** `rotate` or `flip`, **When** it renders, **Then** the wrapper carries `swap-rotate` or `swap-flip`.
4. **Given** `active`, **When** it renders, **Then** the wrapper carries `swap-active`, which a project's script may toggle.
5. **Given** an `indeterminate` slot, **When** it renders, **Then** that content sits in `swap-indeterminate`.
6. **Given** `checked name="theme" value="dark"`, **When** it renders, **Then** those land on the checkbox, and any other attribute lands on the wrapper.
7. **Given** the swap's documentation, **When** a developer wants a theme toggle, **Then** it shows how to add daisyUI's theme-controller class to the swap's checkbox.
8. **Given** the swap's gallery entry, **When** a developer opens it, **Then** the plain, rotate and flip styles, the checked and active states and the indeterminate slot are shown.

---

### User Story 5 - FAB (Priority: P3)

A developer needs a floating action button in a corner of the screen that reveals further actions when it is clicked or focused, arranged in a column or a quarter-circle.

**Why this priority**: Mostly a mobile and dashboard pattern. Fewer applications need it than any other component here.

**Independent Test**: Render `<c-fab>` with actions in its slot, focus its trigger in a browser by keyboard and by click, and check the actions appear and can be reached.

**Acceptance Scenarios**:

1. **Given** `<c-fab icon="..." aria-label="Actions">` with three `<c-button>` actions in its slot, **When** it renders, **Then** it is daisyUI's FAB markup: a wrapper with the `fab` class, a large circular trigger drawn by `<c-button>`, and the three actions.
2. **Given** a rendered FAB, **When** a keyboard user tabs to the trigger, **Then** the actions appear and each can be reached by Tab and activated.
3. **Given** a FAB with no actions, **When** it renders, **Then** it is a single floating button, daisyUI's one-button form.
4. **Given** `flower`, **When** it renders, **Then** the wrapper carries `fab-flower`.
5. **Given** a `close` slot or a `main_action` slot, **When** it renders, **Then** the content sits in `fab-close` or `fab-main-action` and takes the trigger's place while the FAB is open.
6. **Given** a `button` slot, **When** it renders, **Then** it replaces the default trigger.
7. **Given** the FAB's gallery entry, **When** a developer opens it, **Then** the column and flower arrangements, labelled actions, actions with tooltips, the close button and the main action are all shown, with accessible names on every icon-only button.

---

### Edge Cases

- A `variant`, `size` or `placement` value daisyUI does not define emits no class for that attribute and raises no error.
- A button given more than one style attribute (`outline` and `ghost`) emits every class given. The component does not pick between them.
- An icon-only button, FAB trigger or FAB action with no text and no `aria-label` has no accessible name, and the component cannot invent one. The documentation and every gallery example show the name being given.
- A modal with neither `title` nor `aria-label` is unnamed. The documentation says to give one or the other.
- A modal needs an `id` so a trigger can open it. Without one it renders a dialog nothing can open, so the documentation marks `id` as required.
- A dropdown inside an open modal still opens above the modal's content.
- The dropdown relies on the browser's popover support, and on CSS anchor positioning for placement. In a browser without anchor positioning the panel still opens and closes but may not sit beside its trigger. That is a limit of daisyUI's method, and the documentation says so.
- The FAB opens while its trigger has focus. Some browsers do not focus a clicked button unless it is explicitly focusable, so the trigger is made explicitly focusable.
- Two FABs on one page share the same corner. Placing them is the project's job.
- A swap's indeterminate state can only be set from script. The slot renders, and the project supplies the script.

## Requirements *(mandatory)*

### Functional Requirements

**Every component in the group**

- **FR-001**: Button, dropdown, FAB, modal and swap MUST each exist as a Cotton component (`<c-button>`, `<c-dropdown>`, `<c-fab>`, `<c-modal>`, `<c-swap>`) emitting the markup and classes daisyUI documents. *(US1–US5)*
- **FR-002**: Each MUST follow Article XIV: `variant` for colour, `size` on daisyUI's `xs`–`xl` scale where daisyUI has a size modifier, daisyUI's modifier names as boolean attributes, `class` merged into the root element's class list, and every other attribute passed through to the root element unless this spec names another element for it. *(US1–US5)*
- **FR-003**: Each MUST carry the gallery annotations Article XVI requires, including `@trigger` for the modal, and `cotton_lint --warnings-as-errors` MUST pass. *(US1–US5)*
- **FR-004**: Each MUST have a gallery entry that renders its variants and states, so a developer can choose attributes without reading the template. *(US1–US5)*
- **FR-005**: Each MUST emit accessible markup by default: correct roles and states, keyboard reach and a visible focus indicator. Icons that only decorate MUST be hidden from assistive technology. *(US1–US5)*
- **FR-006**: A component that draws a button MUST do so through `<c-button>` (Article XV). *(US3, US5)*
- **FR-007**: Every removed or renamed attribute or slot on the button, dropdown and modal MUST be listed in the CHANGELOG with its replacement, and the README MUST describe the components as they now are. *(US1–US3)*

**Button**

- **FR-008**: `<c-button>` MUST accept `variant` (neutral, primary, secondary, accent, info, success, warning, error), `size` (xs–xl), the style booleans `outline`, `dash`, `soft`, `ghost` and `link`, the behaviour booleans `active` and `disabled`, and the modifier booleans `wide`, `block`, `square` and `circle`, each mapping to its daisyUI class. *(US1)*
- **FR-009**: `<c-button>` MUST render an `<a>` when `href` is given and a `<button>` otherwise. It MUST keep `text`, `icon` (drawn by `<c-icon>`, before the text) and the default slot (after the text). *(US1)*
- **FR-010**: A disabled `<button>` MUST carry the native `disabled` attribute. A disabled link MUST carry `btn-disabled`, `aria-disabled="true"`, `role="button"` and `tabindex="-1"`. *(US1)*
- **FR-011**: `block` MUST replace `full`, and `align`, `reverse` and `condition` MUST be removed. *(US1)*

**Modal**

- **FR-012**: `<c-modal>` MUST render a `<dialog>` with daisyUI's modal box, the default slot as the box's body, and an `actions` slot rendered in daisyUI's actions row. *(US2)*
- **FR-013**: `title` MUST render a heading inside the box that names the dialog for assistive technology. *(US2)*
- **FR-014**: `placement` MUST map top, middle, bottom, start and end to daisyUI's modal placement classes, replacing `position`. `open` MUST render the modal already shown. *(US2)*
- **FR-015**: The modal MUST close on Escape and on a click on the backdrop without script. `closable` MUST add a close button whose accessible name is the translatable string "Close". *(US2)*
- **FR-016**: The inner card, `size`, `icon`, `footer` and `footer_end` MUST be removed. The box MUST accept extra classes through `content_class`. *(US2)*

**Dropdown**

- **FR-017**: `<c-dropdown>` MUST use daisyUI's popover method: a trigger button opens a popover panel holding the default slot. It MUST open by pointer and keyboard, close on Escape and on an outside click, and expose its expanded state, all without script. *(US3)*
- **FR-018**: The default trigger MUST be a `<c-button>` receiving the dropdown's button attributes. A `button` slot MUST replace the default trigger. *(US3)*
- **FR-019**: Each dropdown MUST link its trigger to its own panel, generating a unique identifier when the caller gives none. *(US3)*
- **FR-020**: `placement` MUST accept one side (top, bottom, left, right) and one alignment (start, center, end), each mapped to daisyUI's dropdown placement class, replacing `valign` and `halign`. `full` and `hover` MUST be removed. The panel MUST accept extra classes through `content_class`. *(US3)*

**Swap**

- **FR-021**: `<c-swap>` MUST render daisyUI's checkbox-driven swap: a wrapper with `swap`, a visually hidden checkbox, and `on`, `off` and optional `indeterminate` slots in `swap-on`, `swap-off` and `swap-indeterminate`. *(US4)*
- **FR-022**: `rotate`, `flip` and `active` MUST map to `swap-rotate`, `swap-flip` and `swap-active`. *(US4)*
- **FR-023**: `label` MUST give the checkbox its accessible name, and `checked`, `disabled`, `name` and `value` MUST land on the checkbox, not the wrapper. *(US4)*
- **FR-024**: The checkbox MUST accept extra classes. The swap's documentation MUST show a theme toggle built by adding daisyUI's theme-controller class to it, and state that the theme controller has no component of its own, and why. *(US4)*

**FAB**

- **FR-025**: `<c-fab>` MUST render daisyUI's FAB markup: a wrapper with `fab`, a trigger, and the default slot as the speed-dial actions. *(US5)*
- **FR-026**: The default trigger MUST be a large circular `<c-button>` receiving the FAB's button attributes, explicitly focusable so a click opens the FAB in every browser. A `button` slot MUST replace it. *(US5)*
- **FR-027**: `flower` MUST map to `fab-flower`. `close` and `main_action` slots MUST render in `fab-close` and `fab-main-action`. *(US5)*

### Key Entities

- **Trigger**: the button that opens a dropdown, FAB or modal. The dropdown and FAB draw theirs with `<c-button>`. The modal's trigger sits outside the component and the project wires it.
- **Panel**: what a trigger reveals: the dropdown's popover, the modal's box, the FAB's actions.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every class daisyUI lists for button, dropdown, FAB, modal and swap is reachable through a documented attribute or slot, except the classes that belong only to methods this spec does not use: the dropdown's `dropdown-content`, `dropdown-hover`, `dropdown-open` and `dropdown-close`, and the modal's `modal-toggle`, which daisyUI marks as legacy.
- **SC-002**: `cotton_lint --warnings-as-errors` reports zero errors and zero warnings for all five components.
- **SC-003**: All five components can be opened, used and closed with the keyboard alone, and none of them ships a script. The only script a project writes is the modal's trigger, and the gallery shows it.
- **SC-004**: Every gallery example of an icon-only control has an accessible name, and every component's gallery entry shows each of its variants and states.
- **SC-005**: A developer upgrading from the previous button, dropdown or modal finds every removed or renamed attribute and its replacement in the CHANGELOG.

## Assumptions

- #11 lands first, so the gallery annotations, the lint check in CI and the documentation on running the gallery already exist.
- The host project runs daisyUI 5, the version whose class reference this spec follows.
- The package is below 0.1.0, so breaking attribute changes to existing components are acceptable when the CHANGELOG lists them.
- `<c-icon>` remains the way every component draws an icon. Its own attributes do not change here.
