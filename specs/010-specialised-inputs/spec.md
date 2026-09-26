# Feature Specification: Specialised inputs

**Feature Branch**: `010-specialised-inputs`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2, G3 · **Roadmap**: R7 · **Depends on**: #18 (the core form controls: the fieldset these inputs sit in, and the rule for which attributes reach a control rather than its wrapper)

**Input**: Issue #19, "Specialised inputs": rating, filter, calendar, validator and OTP as Cotton components. They build on the core form controls. Each is accessible and shown in the gallery with its variants and states.

## Scope

daisyUI's data-input group has five members beyond the core form controls. Four get a Cotton component, all of them new:

| Component | State today | This feature |
|---|---|---|
| Filter | missing | new |
| Calendar | missing | new |
| OTP | missing | new |
| Rating | missing | new |

**Validator is excluded.** daisyUI defines it as a class added to an input, select or textarea, so it modifies other components and gets no Cotton component of its own (README, *Scope & philosophy*).

**The calendar ships no calendar.** daisyUI's calendar is a set of styles for third-party calendar libraries. `<c-calendar>` emits the markup daisyUI styles for Cally, and the project loads Cally's script itself. The package ships no JavaScript here or anywhere else.

Out of scope: wiring any of these to a Django form or form field, and any script.

## Clarifications

### Session 2026-09-26

- Q: Which calendar libraries does `<c-calendar>` support? → A: Cally only. Of daisyUI's three, it is the one library whose markup is written in the template. React Day Picker is a React component, and Vanilla Calendar Pro is an empty `<div class="vc">` that its script fills in, so a component would add nothing to it.
- Q: How does a project see or use the calendar when the package ships no script? → A: The project loads Cally. Without it the browser treats Cally's elements as unknown and shows nothing usable. The documentation says so and shows how to load it. The demo loads Cally so the gallery entry works. The package never does.
- Q: How are a filter's options given? → A: As a list through `:options`. Each entry is either a value, which is also its label, or a (value, label) pair, the same shape as a Django `choices` list. `value` selects one. Components take plain values, so a caller can pass a form field's choices without the component knowing about forms.
- Q: Which of daisyUI's two filter structures does `<c-filter>` emit? → A: The one without a `<form>`, where the reset is a radio button carrying `filter-reset`. The other structure makes the filter a `<form>` with a reset input. A form cannot sit inside another form, and a reset input clears every field in its form, so that structure breaks the most common place a filter lives: inside a larger search or list form.
- Q: What is the filter reset called, given daisyUI shows it as "×"? → A: It still shows "×", and assistive technology reads the translatable name "Clear filter". A daisyUI button built from a radio input draws its visible text from the input's `aria-label`, so the reset keeps `aria-label="×"` for the glyph and takes its accessible name from a visually hidden "Clear filter" through `aria-labelledby`, which takes precedence. `reset_label` replaces the hidden name.
- Q: How does the rating take a colour, when daisyUI has no rating colour modifier? → A: Through `variant`, which gives each item daisyUI's background for that colour role (`variant="warning"` gives `bg-warning`). daisyUI colours rating items with background classes, and Article XIV says to reuse an existing name for the same idea where daisyUI has none. The idea is colour, and its name here is `variant`. It also keeps rating colours on the semantic palette (Article XIII), where daisyUI's own examples use literal Tailwind colours.
- Q: What is the rating's item shape called? → A: `shape`, the name `<c-mask>` uses for the same mask classes. It takes `star`, `star-2` and `heart`, and defaults to `star`.
- Q: How is a read-only rating announced? → A: As an image named by its value, "3 out of 5" (translatable), because a row of shapes means nothing to a screen reader on its own. It keeps the per-item markup daisyUI documents, with `aria-current="true"` on the selected item.
- Q: How many boxes does the OTP show, and what does it accept? → A: `length` boxes, 6 by default, the length most authenticator apps use. daisyUI supports four to six. The input gets the matching `maxlength` and digit `pattern`, plus `inputmode="numeric"` and `autocomplete="one-time-code"`, so phones offer the number keypad and fill the code from a text message.
- Q: Which OTP, rating and filter attributes reach the input rather than the wrapper? → A: The control's state and form attributes (`id`, `name`, `value`, `required`, `disabled`, `autofocus`, `form`) and its accessible name. Everything else goes to the wrapper, per Article XIV. Where #18 settles a different list for the core controls, these components follow #18.
- Q: How is each input labelled? → A: `label` names the control for assistive technology. On the OTP it renders as visually hidden text inside daisyUI's `<label class="otp">`, with the translatable default "Verification code". On the rating and the filter it names the radio group. A visible label comes from the fieldset legend #18 provides, and then `label` is left out.
- Q: Which button classes does the filter pass to its options? → A: `variant` and `size` only, as `btn-{variant}` and `btn-{size}`. Other button styles go through a project override (tie-break 3).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Filter (Priority: P1)

A developer building a list page needs a row of options where choosing one hides the rest and shows a button to clear the choice. It submits like any radio group, and keyboard and screen-reader users can choose, change and clear it with no script.

**Why this priority**: List and search pages are the most common page in a data application, and they need a quick filter more often than any other input in this group.

**Independent Test**: Render `<c-filter>` with options inside a form, choose and clear an option by pointer and keyboard in a browser, and check what the form submits and what assistive technology reads.

**Acceptance Scenarios**:

1. **Given** `<c-filter name="status" :options="['Open', 'Closed']">`, **When** it renders, **Then** it is daisyUI's filter markup: a wrapper with the `filter` class, a reset radio carrying `btn` and `filter-reset`, and one radio input with the `btn` class per option, all sharing the name `status`.
2. **Given** options given as (value, label) pairs, **When** it renders, **Then** each radio carries the value and shows the label.
3. **Given** `value="Closed"`, **When** it renders, **Then** that option is checked and the others are hidden, as daisyUI's CSS does for a checked filter.
4. **Given** a filter inside a form with the option "Closed" chosen, **When** the form submits, **Then** it sends `status=Closed`. After the reset is chosen it sends `status` with an empty value.
5. **Given** a rendered filter in a browser, **When** a keyboard user tabs to it and uses the arrow keys, **Then** they move between the visible options and the reset, each shows a visible focus indicator, and the group is announced with its `label`.
6. **Given** the reset, **When** assistive technology reads it, **Then** it is named "Clear filter", while it shows "×".
7. **Given** two filters on one page with no `name` given, **When** they render, **Then** each gets its own generated name and choosing in one never changes the other.
8. **Given** `variant="primary"` and `size="sm"`, **When** it renders, **Then** every option and the reset carry `btn-primary` and `btn-sm`.
9. **Given** the filter's gallery entry, **When** a developer opens it, **Then** it shows a filter with nothing chosen, one with an option chosen, the colours and sizes, and a filter inside a fieldset with a visible legend.

---

### User Story 2 - Calendar (Priority: P2)

A developer needs a date picker that matches the daisyUI theme. They load Cally in their project, write `<c-calendar>`, and get Cally's markup with daisyUI's calendar styles: a single date or a range, one month or several.

**Why this priority**: Choosing a date is common, but a browser's native date input already covers the simplest cases, and this component only works once the project has loaded a third-party script.

**Independent Test**: Render `<c-calendar>` on a page that loads Cally, move through months and pick dates by keyboard and pointer, and check the markup and the named month controls.

**Acceptance Scenarios**:

1. **Given** `<c-calendar>`, **When** it renders, **Then** it is Cally's `<calendar-date>` element with daisyUI's `cally` class, holding one `<calendar-month>` and the previous and next month icons in Cally's `previous` and `next` slots.
2. **Given** `range`, **When** it renders, **Then** the root is Cally's `<calendar-range>` instead, with the same class and slots.
3. **Given** `months="2"`, **When** it renders, **Then** it holds two `<calendar-month>` elements, the second offset by one month, so two months show side by side.
4. **Given** `value`, `min`, `max` and `locale`, **When** it renders, **Then** they land on the root element unchanged, where Cally reads them.
5. **Given** the previous and next icons, **When** assistive technology reads them, **Then** they are named with the translatable "Previous" and "Next", and `<c-icon>` draws them.
6. **Given** a page that loads Cally, **When** a keyboard user tabs into the calendar, **Then** they can change month, move between days and choose one, with a visible focus indicator throughout.
7. **Given** the calendar's documentation, **When** a developer reads it, **Then** it states that the project loads Cally, shows how, and shows the short script that copies a chosen date into a form input.
8. **Given** the calendar's gallery entry, **When** a developer opens it, **Then** a single date, a range, two months and a calendar with a minimum and maximum date are each shown working.

---

### User Story 3 - OTP (Priority: P2)

A developer building a sign-in or two-factor step needs a one-time code field shown as separate boxes. It works with phone autofill and the number keypad, and screen-reader users hear what it asks for.

**Why this priority**: Most applications with accounts have a verification step, but it is one page in the application, where a filter appears on many.

**Independent Test**: Render `<c-otp name="code">` in a form, type and paste a code in a browser, and check the markup, the input's attributes and what the form submits.

**Acceptance Scenarios**:

1. **Given** `<c-otp name="code">`, **When** it renders, **Then** it is daisyUI's OTP markup: a `<label>` with the `otp` class holding six empty `<span>` elements and an input named `code` with `maxlength="6"`, `pattern="[0-9]{6}"`, `inputmode="numeric"` and `autocomplete="one-time-code"`.
2. **Given** `length="4"`, **When** it renders, **Then** there are four spans, and `maxlength` and `pattern` both allow four digits.
3. **Given** `variant="error"`, `size="lg"` and `joined`, **When** it renders, **Then** the label carries `otp-error`, `otp-lg` and `otp-joined`.
4. **Given** no `label`, **When** assistive technology reads the input, **Then** it is named "Verification code". Given `label="Code from your authenticator app"`, it is named that instead.
5. **Given** `required`, `disabled` or `id`, **When** it renders, **Then** they land on the input, and `class` and any other attribute land on the label.
6. **Given** a rendered OTP in a browser, **When** a user types or pastes a six-digit code, **Then** each digit shows in its own box, the input shows a visible focus indicator, and the form submits the code under the input's name.
7. **Given** the OTP's gallery entry, **When** a developer opens it, **Then** it shows the four-, five- and six-digit lengths, joined and separate boxes, the colours and sizes, and the disabled state.

---

### User Story 4 - Rating (Priority: P3)

A developer needs a star rating a user can set, and a read-only rating for showing a score. It submits like any radio group, can be cleared, and screen-reader users hear the value.

**Why this priority**: Ratings belong to reviews and feedback, which fewer applications have than lists, dates or sign-in.

**Independent Test**: Render an interactive and a read-only `<c-rating>`, set and clear the interactive one by pointer and keyboard in a browser, and check the markup, the submitted value and what assistive technology reads.

**Acceptance Scenarios**:

1. **Given** `<c-rating name="score" label="Your rating">`, **When** it renders, **Then** it is daisyUI's rating markup: a wrapper with the `rating` class, exposed as a radio group named "Your rating", holding five radio inputs named `score` with values 1 to 5, each carrying `mask` and `mask-star`.
2. **Given** `max="10"` and `value="7"`, **When** it renders, **Then** there are ten radios and the seventh is checked.
3. **Given** each radio, **When** assistive technology reads it, **Then** it is named with its value, "1 star" through "5 stars", translatable and pluralised.
4. **Given** `clearable`, **When** it renders, **Then** a first radio carrying `rating-hidden` and named "No rating" lets the user clear the rating, and it is checked when no `value` is given.
5. **Given** `half`, **When** it renders, **Then** the wrapper carries `rating-half`, each whole value becomes two radios carrying `mask-half-1` and `mask-half-2`, and the values run from 0.5 to `max` in steps of 0.5.
6. **Given** `shape="heart"`, `variant="warning"` and `size="lg"`, **When** it renders, **Then** every item carries `mask-heart` and `bg-warning`, and the wrapper carries `rating-lg`.
7. **Given** `readonly value="3"`, **When** it renders, **Then** the items are `<div>` elements, not inputs, the third carries `aria-current="true"`, and the rating is announced as an image named "3 out of 5".
8. **Given** a rendered interactive rating in a browser, **When** a keyboard user tabs to it and uses the arrow keys, **Then** the value changes and the focused item shows a visible focus indicator.
9. **Given** the rating's gallery entry, **When** a developer opens it, **Then** it shows each shape, size and colour, the half-step rating, a clearable rating, a disabled rating and a read-only rating.

---

### Edge Cases

- A `variant`, `size` or `shape` value daisyUI does not define emits no class for that attribute and raises no error.
- An OTP `length` outside four to six renders that many boxes, but daisyUI only styles four to six. The documentation states the range.
- An OTP `value` longer than `length` renders as given, and the browser's `maxlength` stops the user adding to it.
- A rating `value` above `max`, below zero, or not a multiple of 0.5 on a half rating checks no item and raises no error.
- A filter `value` that matches no option checks nothing, so every option shows.
- A filter with an empty options list renders only the reset. The documentation says to give at least one option.
- A filter or rating with no `name` gets a generated one. That keeps its radios together but means nothing to a form, so the documentation marks `name` as needed for anything submitted.
- daisyUI's mask crops everything outside the shape, which can include a focus outline. The rating must still show a visible focus indicator on the focused item, and the implementation confirms this in a browser.
- The calendar's markup does nothing until the project loads Cally, and the component cannot detect whether it has. The documentation puts that requirement first.
- Cally's own elements handle the calendar's keyboard behaviour and name its day buttons. This feature covers only the markup it emits around them.
- Validation styling comes from daisyUI's validator class, which a project adds to the OTP's input through `input_class`. No component provides it.

## Requirements *(mandatory)*

### Functional Requirements

**Every component in the group**

- **FR-001**: Calendar, filter, OTP and rating MUST each exist as a Cotton component (`<c-calendar>`, `<c-filter>`, `<c-otp>`, `<c-rating>`) emitting the markup and classes daisyUI documents. *(US1–US4)*
- **FR-002**: Each MUST follow Article XIV: `variant` for colour, `size` on daisyUI's `xs`–`xl` scale where daisyUI has a size modifier, daisyUI's modifier names as boolean attributes, `class` merged into the root element's class list, and every other attribute passed through to the root element unless this spec names another element for it. *(US1–US4)*
- **FR-003**: Each MUST carry the gallery annotations Article XVI requires, and `cotton_lint --warnings-as-errors` MUST pass. *(US1–US4)*
- **FR-004**: Each MUST have a gallery entry that renders its variants and states, so a developer can choose attributes without reading the template. *(US1–US4)*
- **FR-005**: Each MUST emit accessible markup by default: a named control or group, correct roles and states, keyboard reach and a visible focus indicator. Every accessible name the component supplies MUST be translatable. *(US1–US4)*
- **FR-006**: The filter, OTP and rating MUST work inside the fieldset from #18, with its legend as their visible label, and MUST send their control attributes to the same element #18 sends them to for the core controls. *(US1, US3, US4)*
- **FR-007**: A component that draws an icon MUST do so through `<c-icon>` (Article XV). *(US2)*
- **FR-008**: The README MUST list the four components, and its scope section MUST record that validator has no component and that the calendar needs Cally. *(US1–US4)*

**Filter**

- **FR-009**: `<c-filter>` MUST render daisyUI's filter structure without a `<form>`: a wrapper with `filter`, a reset radio carrying `btn` and `filter-reset`, then one radio input carrying `btn` per option, all sharing one `name`. *(US1)*
- **FR-010**: `:options` MUST accept a list whose entries are a value, used as its own label, or a (value, label) pair. `value` MUST check the matching option. *(US1)*
- **FR-011**: The reset MUST show "×" and MUST be named by the translatable "Clear filter" for assistive technology. `reset_label` MUST replace that name. *(US1)*
- **FR-012**: `label` MUST name the group, which MUST be exposed as a radio group. `variant` and `size` MUST reach every option and the reset as `btn-{variant}` and `btn-{size}`. *(US1)*
- **FR-013**: Each filter MUST generate a unique `name` when the caller gives none. *(US1)*

**Calendar**

- **FR-014**: `<c-calendar>` MUST render Cally's `<calendar-date>`, or `<calendar-range>` when `range` is given, carrying `cally`, with previous and next icons in Cally's `previous` and `next` slots and one `<calendar-month>` per month. *(US2)*
- **FR-015**: `months` MUST set how many months show, 1 by default, each month after the first offset by one more. *(US2)*
- **FR-016**: The previous and next icons MUST carry the translatable accessible names "Previous" and "Next". *(US2)*
- **FR-017**: Cally's own attributes (`value`, `min`, `max`, `locale`, `first-day-of-week` and the rest) MUST pass through to the root element unchanged. *(US2)*
- **FR-018**: The calendar's documentation MUST state that the project loads Cally, show how, and show the script that copies a chosen date into a form input. The demo MAY load Cally for the gallery. The package MUST NOT. *(US2)*

**OTP**

- **FR-019**: `<c-otp>` MUST render a `<label>` carrying `otp`, holding `length` empty `<span>` elements and one text input, with `length` defaulting to 6. *(US3)*
- **FR-020**: The input MUST carry `maxlength` equal to `length`, a `pattern` allowing exactly `length` digits, `inputmode="numeric"` and `autocomplete="one-time-code"`. *(US3)*
- **FR-021**: `variant`, `size` and `joined` MUST map to `otp-{variant}`, `otp-{size}` and `otp-joined` on the label. *(US3)*
- **FR-022**: `label` MUST render as visually hidden text inside the OTP's label, naming the input, with the translatable default "Verification code". *(US3)*
- **FR-023**: `id`, `name`, `value`, `required`, `disabled`, `autofocus` and `form` MUST land on the input. `input_class` MUST add classes to the input. *(US3)*

**Rating**

- **FR-024**: `<c-rating>` MUST render a wrapper carrying `rating` holding `max` radio inputs, 5 by default, sharing one `name`, with values 1 to `max`, each carrying `mask` and the class for its `shape`. `value` MUST check the matching radio. *(US4)*
- **FR-025**: `shape` MUST take `star`, `star-2` or `heart`, defaulting to `star`, and map to daisyUI's mask class. `variant` MUST give every item `bg-{variant}`. `size` MUST map to `rating-{size}` on the wrapper. *(US4)*
- **FR-026**: `label` MUST name the group, which MUST be exposed as a radio group, and each radio MUST be named by its value with a translatable, pluralised string. *(US4)*
- **FR-027**: `clearable` MUST add a first radio carrying `rating-hidden`, with an empty value and the translatable name "No rating", checked when no `value` is given. *(US4)*
- **FR-028**: `half` MUST add `rating-half` and render two radios per whole value, carrying `mask-half-1` and `mask-half-2`, with values in steps of 0.5. *(US4)*
- **FR-029**: `readonly` MUST render `<div>` items in place of inputs, with `aria-current="true"` on the item matching `value`, and expose the rating as an image named "`value` out of `max`" through a translatable string. *(US4)*
- **FR-030**: `name`, `required` and `disabled` MUST land on every radio. Each rating MUST generate a unique `name` when the caller gives none. *(US4)*

### Key Entities

- **Option**: one choice in a filter, a value with a label.
- **Item**: one shape in a rating, a radio input or, when read-only, a `<div>`.
- **Code box**: one empty `<span>` in the OTP, where daisyUI shows one digit of the input's value.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every class daisyUI lists for filter, OTP, rating and the Cally calendar is reachable through a documented attribute, except those tied to structures this spec does not use: the filter's `<form>` structure, and the `react-day-picker` and `vc` calendar classes.
- **SC-002**: `cotton_lint --warnings-as-errors` reports zero errors and zero warnings for all four components.
- **SC-003**: The filter, OTP and rating can be set, changed and cleared with the keyboard alone, and none of the four components ships a script.
- **SC-004**: Every control and group these components emit has an accessible name in every gallery example, and every component's gallery entry shows each of its variants and states.
- **SC-005**: A form containing a filter, an OTP and an interactive rating submits each value under its `name` with no script on the page.

## Assumptions

- #18 lands first, so the fieldset these components sit in, and the rule for which attributes reach a control, already exist.
- #11 has landed, so the gallery annotations, the lint check in CI and the documentation on running the gallery already exist.
- The host project runs daisyUI 5, the version whose class reference this spec follows, and a version of Cally that daisyUI styles.
- Cally's elements handle their own keyboard behaviour and name their day buttons.
- `<c-icon>` remains the way every component draws an icon. Its own attributes do not change here.
