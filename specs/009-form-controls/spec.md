# Feature Specification: Core form controls

**Feature Branch**: `009-form-controls`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2, G3 · **Roadmap**: R7 · **Depends on**: #11 (gallery annotations and the lint check in CI)

**Input**: Issue #18, "Core form controls": text input, textarea, select, checkbox, radio, toggle, range, file input, label and fieldset as Cotton components. Each ties its label to its control and is shown in the gallery with its variants and states. `form.field` already covers part of the fieldset.

## Scope

daisyUI's data input group has ten base components that nearly every form uses. Each gets a Cotton component:

| Component | Tag | State today | This feature |
|---|---|---|---|
| Text input | `<c-input>` | missing | new |
| Textarea | `<c-textarea>` | missing | new |
| Select | `<c-select>` | missing | new |
| Checkbox | `<c-checkbox>` | missing | new |
| Radio | `<c-radio>` | missing | new |
| Toggle | `<c-toggle>` | missing | new |
| Range | `<c-range>` | missing | new |
| File input | `<c-file-input>` | missing | new |
| Label | `<c-label>` | missing | new, covering daisyUI's `label` and `floating-label` |
| Fieldset | `<c-fieldset>` | missing | new |

**`form.field` is removed.** It draws a fieldset, a label and a control under one tag, three daisyUI components in one, which the README's *Scope & philosophy* rules out. Everything it does today can be written with `<c-fieldset>`, `<c-label>` and a control used together, and the CHANGELOG shows how (User Story 3).

Out of scope:

- Rendering a Django form or form field. Components take plain values such as a name, a value and a list of error messages. Turning a bound field into those values is the project's job (README, *Scope & philosophy*).
- daisyUI's validator. It is a class added to an input, select or textarea, so it gets no component of its own. Issue #19 covers the specialised inputs that build on these controls.
- Any JavaScript. A checkbox's indeterminate state, for example, can only be set from script, and the project supplies it.

## Clarifications

### Session 2026-09-26

- Q: How is a control's visible label tied to it, now that no single component draws both? → A: By `<c-label>`, in one of daisyUI's documented forms. Above a control it is a `<label class="label">` pointing at the control's `id` with `for`, the pattern daisyUI's fieldset examples use. Around a checkbox, radio or toggle it wraps the control and its text. With `floating` it becomes daisyUI's floating label, wrapping a text input, select or textarea. A wrapping label needs no `id`.
- Q: What is a fieldset's legend for, and does it name a single control? → A: The legend names a group of controls, such as a set of radio buttons or an address block. It does not name a control inside it for assistive technology, so a fieldset holding one control still gives that control a `<c-label>`. The documentation and the gallery show both shapes.
- Q: Where do `form.field`'s help text and errors go? → A: To the fieldset. `description` renders daisyUI's description line, and `errors` takes a string or a list of strings and renders them as error-coloured description lines. When the fieldset has an `id`, the description and the errors get ids derived from it, so a control can point at them with `aria-describedby`. The documentation shows that link in every example with help text or errors.
- Q: How does a control show that it is invalid? → A: The caller sets `variant="error"` for daisyUI's error colour and passes `aria-invalid="true"`, which reaches the control like any other attribute. The control does not infer either from the fieldset, so each attribute keeps one predictable meaning. The gallery shows the invalid state for every control.
- Q: Which `form.field` attributes have no direct replacement? → A: `hide-label` becomes `class="sr-only"` on the label. `wrapper-class` becomes `class` on the fieldset. `prelabel` and `postlabel` become the `start` and `end` slots of the input or select. The asterisk `form.field` added after a required control's label is dropped: the control's own `required` attribute tells assistive technology, and a project that wants a visible marker writes it in the label text. The CHANGELOG lists each one.
- Q: What do the text input's and the select's `start` and `end` slots do? → A: They put content inside the control's box, before or after the field: daisyUI's inline label (`<span class="label">https://</span>`), an icon or a `<kbd>` hint. When either is filled, the component uses daisyUI's wrapped form, with the control's classes on a wrapping `<label>`. `start` and `end` already name the navbar's sections, so the names are reused rather than coined.
- Q: Which element receives `class` and which receives the other attributes when an input or select is wrapped? → A: `class` goes to the element that carries daisyUI's `input` or `select` class, which is the wrapper when there is one. Every other attribute (`name`, `value`, `id`, `required`, `aria-*` and the rest) goes to the `<input>` or `<select>`, where it has an effect.
- Q: Is the toggle announced as a checkbox or a switch? → A: As a switch. It renders a checkbox with `role="switch"`, so assistive technology reports "on" and "off", which is what a toggle looks like it does.
- Q: daisyUI says a range must have `min` and `max`. What if the caller gives neither? → A: The range defaults them to 0 and 100, the browser's own defaults, so the rendered markup always meets daisyUI's rule.
- Q: Are the new components grouped under a `form.` prefix, as `form.field` was? → A: No. Every other component is named after its daisyUI component with no group prefix, and these follow that: `<c-input>`, `<c-select>` and so on.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Text input (Priority: P1)

A developer building a form needs a text field in every colour, size and style daisyUI offers, for any text-like input type, and sometimes with an icon, a prefix or a keyboard hint inside the box.

**Why this priority**: Almost every form has a text input. It is also what most `form.field` uses turn into, so adopters need it first.

**Independent Test**: Render `<c-input>` with each attribute and check the classes and attributes on the element it emits. Render it with `start` and `end` content and check the wrapped form. Open its gallery entry and see every variant, size and state.

**Acceptance Scenarios**:

1. **Given** `<c-input name="q" placeholder="Search">`, **When** it renders, **Then** it is a single `<input type="text">` with the `input` class and those attributes.
2. **Given** `<c-input type="email" variant="primary" size="lg" ghost>`, **When** it renders, **Then** it is an `<input type="email">` carrying `input`, `input-primary`, `input-lg` and `input-ghost`.
3. **Given** a `start` slot holding `<span class="label">https://</span>` and an `end` slot holding a `<kbd>`, **When** it renders, **Then** a `<label>` carries `input` and the modifier classes, and holds the start content, the `<input>` and the end content in that order.
4. **Given** a wrapped input with `class="w-full" name="site" required`, **When** it renders, **Then** `w-full` is on the wrapper, and `name` and `required` are on the `<input>`.
5. **Given** `<c-input class="join-item">` with no slots, **When** it renders, **Then** it is a single element that composes inside a join.
6. **Given** `<c-input variant="error" aria-invalid="true">`, **When** it renders, **Then** it carries `input-error` and `aria-invalid="true"`.
7. **Given** the text input's gallery entry, **When** a developer opens it, **Then** every colour, size, the ghost style, the disabled, required and invalid states, several input types, and start and end content are shown, each with an accessible name.

---

### User Story 2 - Label and fieldset (Priority: P1)

A developer needs to name every control, group related controls under a heading, and show help text and error messages under a field. They put a `<c-label>` beside or around a control, and wrap related controls in a `<c-fieldset>` with a legend, a description and errors.

**Why this priority**: Without a label no control is accessible, and without the fieldset there is nowhere for help text and errors to go. Together they replace `form.field`, so they land with the text input.

**Independent Test**: Render a fieldset holding a label and an input, and a fieldset holding a group of radio buttons. Check that every control has an accessible name, that the legend names the group, and that the description and errors can be linked to the control.

**Acceptance Scenarios**:

1. **Given** `<c-label for="id_email" text="Email">`, **When** it renders, **Then** it is a `<label class="label" for="id_email">` reading "Email", and the control with that id takes "Email" as its accessible name.
2. **Given** `<c-label text="Remember me">` wrapping a `<c-checkbox>`, **When** it renders, **Then** the `<label>` holds the checkbox and the text, and the checkbox's accessible name is "Remember me".
3. **Given** `<c-label text="Email" floating>` wrapping a `<c-input placeholder="Email">`, **When** it renders, **Then** it is daisyUI's floating label: a `floating-label` wrapper holding the input and a `<span>` with the text, and the input's accessible name is "Email".
4. **Given** `<c-fieldset legend="Shipping">`, **When** it renders, **Then** it is a `<fieldset class="fieldset">` whose first child is a `<legend class="fieldset-legend">` reading "Shipping", followed by the default slot.
5. **Given** `<c-fieldset id="f-email" description="We never share it.">`, **When** it renders, **Then** the description is a daisyUI description line after the slot content, with an id derived from `f-email` that a control can name in `aria-describedby`.
6. **Given** `errors` as a string or as a list of strings, **When** the fieldset renders, **Then** each message appears as an error-coloured description line, and with an `id` the errors carry their own derived id.
7. **Given** a fieldset with no `legend`, `description` or `errors`, **When** it renders, **Then** it emits no empty legend or description element.
8. **Given** the label's and fieldset's gallery entries, **When** a developer opens them, **Then** each label form (above a control, around a checkbox, floating) and a fieldset with a legend, a description, errors and a radio group are shown, with the `aria-describedby` link in the example markup.

---

### User Story 3 - `form.field` is replaced (Priority: P1)

A developer whose templates use `<c-form.field>` upgrades and finds it gone. The CHANGELOG shows, for each thing `form.field` did, the fieldset, label and control that now do it, so they can rewrite each use without reading the old template.

**Why this priority**: Removing a component breaks every template that uses it. The removal and its migration notes must ship together with the components that replace it.

**Independent Test**: Take each case the current `form.field` tests cover, rewrite it from the CHANGELOG's guidance, and check the rewritten markup renders the same daisyUI structure with every control named.

**Acceptance Scenarios**:

1. **Given** the package after this feature, **When** a template calls `<c-form.field>`, **Then** Cotton reports that the component does not exist. No alias or stub remains.
2. **Given** the CHANGELOG, **When** a developer looks up `form.field`, **Then** they find a before-and-after example for a labelled text input, a textarea, a select, a file input, a checkbox, a radio button, a toggle, a field with help text, a field with errors, and an input with `prelabel` and `postlabel`.
3. **Given** the CHANGELOG, **When** a developer looks up `hide-label`, `wrapper-class`, `prelabel`, `postlabel` and the required-field asterisk, **Then** each is listed with its replacement, or as dropped with the reason.
4. **Given** the README, **When** a developer reads the component list, **Then** `form.field` is gone and the ten new components are listed.

---

### User Story 4 - Textarea and select (Priority: P2)

A developer needs a multi-line text box and a drop-down list of options, styled to match the text input and using the same attribute names.

**Why this priority**: Most forms beyond a login have one or the other, but they are less universal than the text input.

**Independent Test**: Render `<c-textarea>` and `<c-select>` with each attribute and check the emitted classes and attributes. Open their gallery entries.

**Acceptance Scenarios**:

1. **Given** `<c-textarea name="bio" rows="3" variant="secondary" size="sm">Hello</c-textarea>`, **When** it renders, **Then** it is a `<textarea>` carrying `textarea`, `textarea-secondary` and `textarea-sm`, with `name` and `rows`, and "Hello" as its value.
2. **Given** `<c-select name="plan" ghost>` with `<option>` elements in the default slot, **When** it renders, **Then** it is a `<select>` carrying `select` and `select-ghost` and holding the options.
3. **Given** a select with a `start` slot, **When** it renders, **Then** a `<label>` carries `select` and the modifier classes and holds the start content and the `<select>`, with `name` and the other attributes on the `<select>`.
4. **Given** either control with `variant="error" aria-invalid="true"`, **When** it renders, **Then** it carries its error class and `aria-invalid="true"`.
5. **Given** the textarea's and select's gallery entries, **When** a developer opens them, **Then** every colour, size, the ghost style, and the disabled and invalid states are shown, and the select also shows start content and a floating label.

---

### User Story 5 - Checkbox, radio and toggle (Priority: P2)

A developer needs on-off and one-of-many choices: a checkbox for "remember me", a set of radio buttons for a shipping option, a toggle for a setting. Each is labelled, reachable by keyboard and reports its state.

**Why this priority**: Common in settings pages and sign-up forms, but fewer forms need them than need a text field.

**Independent Test**: Render each control with each attribute inside a `<c-label>` and check the emitted markup. In a browser, tab to each, change it with Space or the arrow keys, and check what assistive technology reports.

**Acceptance Scenarios**:

1. **Given** `<c-checkbox name="remember" variant="primary" size="sm" checked>`, **When** it renders, **Then** it is a checked `<input type="checkbox">` carrying `checkbox`, `checkbox-primary` and `checkbox-sm`.
2. **Given** `<c-radio name="ship" value="std" variant="accent">`, **When** it renders, **Then** it is an `<input type="radio">` carrying `radio` and `radio-accent`, with that name and value.
3. **Given** `<c-toggle name="notify" size="lg">`, **When** it renders, **Then** it is an `<input type="checkbox" role="switch">` carrying `toggle` and `toggle-lg`, and is announced as a switch with its on or off state.
4. **Given** three radio buttons sharing a name inside a `<c-fieldset legend="Shipping">`, each in a `<c-label>`, **When** a keyboard user tabs into the group, **Then** the group is announced as "Shipping", the arrow keys move between options, and each option is announced by its label.
5. **Given** any of the three with `disabled`, **When** it renders, **Then** the input carries the native `disabled` attribute.
6. **Given** the three gallery entries, **When** a developer opens them, **Then** every colour, size, the checked, unchecked, disabled and invalid states, a labelled radio group and a labelled toggle are shown.

---

### User Story 6 - File input and range (Priority: P3)

A developer needs a file picker for uploads and a slider for picking a number in a range, styled like the other controls.

**Why this priority**: Uploads and sliders appear in fewer forms than any other control here.

**Independent Test**: Render `<c-file-input>` and `<c-range>` with each attribute and check the emitted markup. Open their gallery entries.

**Acceptance Scenarios**:

1. **Given** `<c-file-input name="avatar" accept="image/*" variant="info" ghost>`, **When** it renders, **Then** it is an `<input type="file">` carrying `file-input`, `file-input-info` and `file-input-ghost`, with `name` and `accept`.
2. **Given** `<c-range name="volume" value="40" variant="success" size="xs">`, **When** it renders, **Then** it is an `<input type="range">` carrying `range`, `range-success` and `range-xs`, with `min="0"` and `max="100"`.
3. **Given** `<c-range min="10" max="20" step="2">`, **When** it renders, **Then** those values replace the defaults.
4. **Given** `<c-range vertical>`, **When** it renders, **Then** it carries `range-vertical`.
5. **Given** the file input's and range's gallery entries, **When** a developer opens them, **Then** every colour, size, the file input's ghost style, the vertical range and the disabled state are shown, each control labelled.

---

### Edge Cases

- A `variant` or `size` value daisyUI does not define emits no class for that attribute and raises no error.
- A control with no `<c-label>`, no `aria-label` and no `aria-labelledby` has no accessible name, and the component cannot invent one. The documentation says so, and every gallery example names its control.
- A `<c-label for="...">` whose id matches no control names nothing, and the browser does not report it. The documentation says the id must match.
- A fieldset holding one control, with the legend as its only text, leaves that control unnamed. The documentation shows the label-per-control shape instead.
- `<c-input type="checkbox">`, `type="radio"`, `type="range"` or `type="file"` renders an input with the `input` class, which daisyUI does not style for those types. The documentation points to the matching component. The input does not refuse the type.
- An empty `errors` list renders no error lines.
- A description or error message containing HTML is escaped like any other template value. A caller who wants markup uses the named slot of the same name.
- A checkbox's indeterminate state can only be set from script. The project supplies it.
- A disabled fieldset disables every control inside it. That is the browser's behaviour, and the component adds nothing to it.
- A floating label only floats while the field has a placeholder or a value. The documentation says to give a placeholder, as daisyUI does.

## Requirements *(mandatory)*

### Functional Requirements

**Every component in the group**

- **FR-001**: Checkbox, fieldset, file input, label, radio, range, select, text input, textarea and toggle MUST each exist as a Cotton component (`<c-checkbox>`, `<c-fieldset>`, `<c-file-input>`, `<c-label>`, `<c-radio>`, `<c-range>`, `<c-select>`, `<c-input>`, `<c-textarea>`, `<c-toggle>`) emitting the markup and classes daisyUI documents. *(US1, US2, US4–US6)*
- **FR-002**: Each MUST follow Article XIV: `variant` for colour (neutral, primary, secondary, accent, info, success, warning, error), `size` on daisyUI's `xs`–`xl` scale, daisyUI's modifier names as boolean attributes, `class` merged into the root element's class list, and every other attribute passed through to the element this spec names. The fieldset and label have no colour or size modifier in daisyUI and take neither attribute. *(US1, US2, US4–US6)*
- **FR-003**: Each MUST carry the gallery annotations Article XVI requires, and `cotton_lint --warnings-as-errors` MUST pass. *(US1, US2, US4–US6)*
- **FR-004**: Each MUST have a gallery entry that renders its variants and states, including the disabled and invalid states for every control, so a developer can choose attributes without reading the template. Every control in every gallery example MUST have an accessible name. *(US1, US2, US4–US6)*
- **FR-005**: Each control MUST emit its native form element, so it is reachable by keyboard, shows the browser's visible focus indicator and reports its state to assistive technology with no script. *(US1, US4–US6)*
- **FR-006**: A control MUST NOT set `aria-invalid` or an error colour on its own. Both come from the caller, through `aria-invalid` and `variant="error"`. *(US1, US4, US5)*

**Text input**

- **FR-007**: `<c-input>` MUST render an `<input>` with the `input` class and `type="text"` unless `type` is given. It MUST accept `variant`, `size` and `ghost`. *(US1)*
- **FR-008**: `<c-input>` MUST accept `start` and `end` slots. When either is filled, it MUST render daisyUI's wrapped form: a `<label>` carrying `input`, the modifier classes and `class`, holding the start content, the `<input>` and the end content, in that order. When neither is filled, it MUST render the `<input>` alone. *(US1)*
- **FR-009**: Every attribute other than `class`, `variant`, `size` and `ghost` MUST reach the `<input>`, wrapped or not. *(US1)*

**Textarea and select**

- **FR-010**: `<c-textarea>` MUST render a `<textarea>` with the `textarea` class and its default slot as the value, and accept `variant`, `size` and `ghost`. *(US4)*
- **FR-011**: `<c-select>` MUST render a `<select>` with the `select` class and its default slot as the options, and accept `variant`, `size` and `ghost`. It MUST accept `start` and `end` slots with the same wrapped form and attribute split as the text input (FR-008, FR-009). *(US4)*

**Checkbox, radio and toggle**

- **FR-012**: `<c-checkbox>` MUST render an `<input type="checkbox">` with the `checkbox` class, and accept `variant` and `size`. *(US5)*
- **FR-013**: `<c-radio>` MUST render an `<input type="radio">` with the `radio` class, and accept `variant` and `size`. *(US5)*
- **FR-014**: `<c-toggle>` MUST render an `<input type="checkbox">` with the `toggle` class and `role="switch"`, and accept `variant` and `size`. *(US5)*

**File input and range**

- **FR-015**: `<c-file-input>` MUST render an `<input type="file">` with the `file-input` class, and accept `variant`, `size` and `ghost`. *(US6)*
- **FR-016**: `<c-range>` MUST render an `<input type="range">` with the `range` class, accept `variant`, `size` and `vertical` (mapping to `range-vertical`), and emit `min` and `max`, defaulting to 0 and 100 when not given. *(US6)*

**Label**

- **FR-017**: `<c-label>` MUST render a `<label>` with the `label` class, its `text` attribute and its default slot. `for` and every other attribute MUST pass through to the `<label>`. A control in the default slot MUST be named by the text. *(US2)*
- **FR-018**: `<c-label floating>` MUST render daisyUI's floating label: a `<label>` with the `floating-label` class holding the control from its default slot and a `<span>` with the text. *(US2)*

**Fieldset**

- **FR-019**: `<c-fieldset>` MUST render a `<fieldset>` with the `fieldset` class, then a `<legend class="fieldset-legend">` when `legend` is given, then its default slot. `legend` MUST also be fillable as a named slot. *(US2)*
- **FR-020**: `description` MUST render daisyUI's description line (`label` class) after the default slot. `errors` MUST accept a string or a list of strings and render each as an error-coloured description line after the description. Both MUST also be fillable as named slots. An empty value MUST render nothing. *(US2)*
- **FR-021**: When the fieldset has an `id`, its description and its errors MUST each carry an id derived from it, and the documentation MUST state both derived ids and show a control naming them in `aria-describedby`. *(US2)*

**Replacing `form.field`**

- **FR-022**: `form.field`'s template and its tests MUST be removed, with no alias left behind. *(US3)*
- **FR-023**: The CHANGELOG MUST record the removal with before-and-after examples for each control type `form.field` supported, for help text, for errors and for `prelabel`/`postlabel`, and MUST list `hide-label`, `wrapper-class`, `prelabel`, `postlabel` and the required asterisk with their replacements or the reason they were dropped. *(US3)*
- **FR-024**: The README's component list MUST drop `form.field` and list the ten new components, and the README MUST describe them as they now are. *(US3)*

### Key Entities

- **Control**: the form element a user fills in: text input, textarea, select, checkbox, radio, toggle, range or file input.
- **Label**: the text that names a control for sighted users and assistive technology, tied to it by `for` or by wrapping it.
- **Fieldset**: the container that groups controls under a legend and carries their description and error messages.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every class daisyUI lists for checkbox, fieldset, file input, input, label, radio, range, select, textarea and toggle is reachable through a documented attribute or slot.
- **SC-002**: `cotton_lint --warnings-as-errors` reports zero errors and zero warnings for all ten components.
- **SC-003**: Every control in every gallery example has an accessible name, and every control can be focused, changed and read with the keyboard and a screen reader alone, with no script shipped.
- **SC-004**: Every case the removed `form.field` tests covered can be rebuilt from the CHANGELOG's examples using the new components.
- **SC-005**: No template in the package, its tests or its demo references `form.field` after this feature.

## Assumptions

- #11 lands first, so the gallery annotations, the lint check in CI and the documentation on running the gallery already exist. #11 annotates `form.field`, and this feature then removes it.
- The host project runs daisyUI 5, the version whose class reference this spec follows.
- The package is below 0.1.0, so removing `form.field` is acceptable when the CHANGELOG lists it with its replacement.
- Issue #19's specialised inputs (rating, filter, calendar, OTP) build on these controls and are specified separately. The validator stays a class the project adds.
