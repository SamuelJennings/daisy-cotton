# Feature Specification: Annotate every component and enforce the gallery lint in CI

**Feature Branch**: `002-gallery-lint`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G2 · Roadmap R1

**Input**: Issue #11: "Every existing component should carry the gallery annotations the constitution asks for, and the gallery's linter should pass with no errors or warnings as part of the test suite. A component that breaks the documentation contract then fails CI instead of quietly drifting. Contributors should be able to find in the docs how to run the gallery and the linter."

## Overview

Constitution Article XVI says every component documents itself for the component gallery, and that `cotton_lint --warnings-as-errors` passes. Today neither is true. On main the linter reports 1 error and 88 warnings across the 21 component templates, and only 3 of them are clean. The one error is prose, not markup: a comment in `form/field.html` mentions `<c-form.render>`, which the linter reads as a call to a component that does not exist. Nothing runs the linter automatically, so the gap has grown without anyone noticing.

This feature closes the gap and keeps it closed. Every existing component gets its annotations, the linter runs inside the test suite so CI fails on any error or warning, and the contributor docs explain how to run the gallery and the linter.

It also fixes what "passes the gallery lint" means for every later component group. A group's components pass when the check this feature adds to the test suite is green for them.

## Clarifications

### Session 2026-09-26

- Q: Which linter findings fail the build? → A: Errors and warnings fail. Hints do not. That is the constitution's rule (Article XVI), and it matches the linter's own `--warnings-as-errors` switch. Hints are heuristics by the tool's own description, and some are unavoidable. For example, `form.field` reads `{{ help_text }}`, which Cotton derives from its declared `help-text` attribute, and the linter flags that as undeclared.
- Q: The linter checks `@prop` annotations against `<c-vars>`. It does not check that a component has a `@description`, that a rendered default slot has a `@slot`, or that each annotation stays on one line. How are those enforced? → A: The test suite gets a second, small check for exactly those three things: one `@description` per component, a `@slot` annotation wherever the template renders the default slot, and no `{#` comment that runs past the end of its line. Without it, a component could pass the linter and still miss half of what Article XVI asks for, which is the drift the issue wants CI to catch. Named slots and `@trigger` are left to review. Detecting a named slot from the template reliably is guesswork, and today `modal` is the only component another element opens.
- Q: Does annotating a component change its attributes? → A: No. Annotations describe what each component declares on main today, including names that look internal, such as `avatar`'s `size_options` and `avatar.group`'s `space_options`. Renaming, removing or re-typing an attribute belongs to the feature for that component's group, and that feature updates the annotations as part of its own change.
- Q: How is the `form.field` error fixed? → A: The comment is reworded so it no longer names a component this package does not ship. The sentence pointed readers at a form-rendering component from another package, which Article XII also rules out. No lint rule is suppressed and no configuration is added to hide the finding.
- Q: Where do the contributor docs live? → A: In a `CONTRIBUTING.md` at the repository root, linked from the README. It covers installing the development environment, running the gallery, running the linter directly, and how the same check runs in the test suite.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The test suite fails when a component breaks the gallery lint (Priority: P1)

A contributor changes a component, for example by adding an attribute to `<c-vars>`, and forgets to annotate it. They run the test suite, or CI runs it on their pull request, and it fails. The failure names the component, the line and the linter's finding, so they can fix it without running anything else.

**Why this priority**: This is the guard the issue asks for. Without it the annotations drift again as soon as they are written, and none of the component groups that follow has a definition of "lint-clean" to meet.

**Independent Test**: Add an undocumented attribute to a component in a scratch copy of the catalog and run the suite. It fails with the finding. Remove the attribute and it passes. Also confirm that a component whose only finding is a hint does not fail.

**Acceptance Scenarios**:

1. **Given** every component is lint-clean, **When** the test suite runs, **Then** the gallery-lint check passes.
2. **Given** a component declares an attribute in `<c-vars>` with no `@prop` annotation, **When** the test suite runs, **Then** the check fails and its message names the component, the line and the missing annotation.
3. **Given** a component calls a Cotton component that does not exist, **When** the test suite runs, **Then** the check fails on that error.
4. **Given** a component's only findings are hints, **When** the test suite runs, **Then** the check passes.
5. **Given** a new component template is added under the package's `cotton/` directory, **When** the test suite runs, **Then** that template is linted with no change to the test.
6. **Given** a pull request, **When** CI runs the test jobs on every supported Python and Django combination, **Then** the gallery-lint check runs in each of them.

---

### User Story 2 - Buttons, links, badges, alerts and icons are fully annotated (Priority: P1)

A host project developer opens the gallery page for `button`, `link`, `badge`, `alert` or `icon` and learns every attribute, its type, its default and what it does, plus what the default slot holds, without opening the template.

**Why this priority**: These are the components nearly every page uses. They are also where adopters look first to learn the attribute vocabulary.

**Independent Test**: Run the linter and confirm these five templates report no errors or warnings. Open each one's gallery page and confirm every declared attribute appears with a description.

**Acceptance Scenarios**:

1. **Given** `button`, `link`, `badge`, `alert` and `icon`, **When** the linter runs, **Then** none of them reports an error or warning.
2. **Given** any attribute these components declare in `<c-vars>`, **When** its annotation is read, **Then** it has a type, a default equal to the `<c-vars>` value (or `required`), and a description.
3. **Given** one of these components renders its default slot, **When** its annotations are read, **Then** a `@slot` annotation describes what goes there.
4. **Given** any of these templates, **When** it is rendered, **Then** no annotation text appears in the page.

---

### User Story 3 - The form field is annotated and its lint error is gone (Priority: P1)

A host project developer opens the gallery page for `form.field` and sees every attribute documented, including the hyphenated ones (`hide-label`, `help-text`, `wrapper-class`), and learns that `label`, `help-text` and `errors` can also be filled as named slots. The linter no longer reports an error for this template.

**Why this priority**: `form.field` carries the only lint error on main, so the gate in User Story 1 cannot pass without it. It also has the widest attribute surface of any existing component, and forms are on nearly every page.

**Independent Test**: Run the linter against `form.field` and confirm no errors or warnings. Confirm the explanatory comment still says what the component does, with no mention of a component this package does not ship.

**Acceptance Scenarios**:

1. **Given** `form/field.html`, **When** the linter runs, **Then** it reports no `unknown-component` error and no warnings.
2. **Given** each of the nine names in its `<c-vars>`, **When** the annotations are read, **Then** each has a type, a matching default and a description.
3. **Given** `label`, `help-text` and `errors`, which accept either an attribute or a named slot of the same name, **When** their `@prop` annotations are read, **Then** each description says a named slot also works.
4. **Given** the template renders the default slot, **When** its annotations are read, **Then** a `@slot` annotation says what the default slot fills for each control type.
5. **Given** the template's explanatory comment, **When** it is read, **Then** it describes the component without naming any component outside this package.

---

### User Story 4 - Cards, modals, dropdowns and dividers are fully annotated (Priority: P2)

A host project developer opens the gallery page for `card`, `modal`, `dropdown` or `divider` and sees every attribute and every named slot documented. For `modal`, the page also says how the modal is opened.

**Why this priority**: These are common containers, but most pages use them less than the components in User Story 2. They carry most of the named slots in the package (`actions`, `footer`, `footer_end`, `badges`, `button`, and `divider`'s `label`), so they are where slot annotations matter most.

**Independent Test**: Run the linter and confirm these four templates report no errors or warnings. Read their annotations and confirm every named slot the template renders has a `@slot:name`, and `modal` has a `@trigger`.

**Acceptance Scenarios**:

1. **Given** `card`, `modal`, `dropdown` and `divider`, **When** the linter runs, **Then** none of them reports an error or warning.
2. **Given** a named slot one of these templates renders (for example `card`'s `actions` or `dropdown`'s `button`), **When** the annotations are read, **Then** a `@slot:name` annotation describes it.
3. **Given** `modal`, **When** its annotations are read, **Then** a `@trigger` annotation says how another element opens it.
4. **Given** the linter's undeclared-variable hints for these named slots on main, **When** the slots are annotated, **Then** those hints no longer appear.

---

### User Story 5 - Navigation and avatar components are fully annotated (Priority: P2)

A host project developer opens the gallery pages for `breadcrumbs`, `breadcrumbs.item`, `dock`, `dock.item`, `avatar` and `avatar.group` and sees every attribute and slot documented.

**Why this priority**: These appear on many pages, but mostly once per page, in the frame around the content. Their attributes will be revisited by their groups' features, so what matters here is that they are documented as they stand.

**Independent Test**: Run the linter and confirm these six templates report no errors or warnings.

**Acceptance Scenarios**:

1. **Given** the six templates, **When** the linter runs, **Then** none of them reports an error or warning.
2. **Given** a parent and child pair such as `dock` and `dock.item`, **When** their annotations are read, **Then** each has its own `@description` saying what it is for and how it relates to the other.
3. **Given** attributes that look internal, such as `size_options` and `space_options`, **When** they are annotated, **Then** the annotation describes what the attribute does today, and the attribute itself is not renamed or removed.

---

### User Story 6 - Mockup components are fully annotated (Priority: P3)

A host project developer opens the gallery pages for `mockup.browser`, `mockup.window`, `mockup.phone`, `mockup.code` and `mockup.code.line` and sees every attribute and slot documented.

**Why this priority**: Mockups are for marketing and documentation pages, not application screens, so fewer adopters need them.

**Independent Test**: Run the linter and confirm these five templates report no errors or warnings.

**Acceptance Scenarios**:

1. **Given** the five mockup templates, **When** the linter runs, **Then** none of them reports an error or warning.
2. **Given** each mockup renders its default slot, **When** its annotations are read, **Then** a `@slot` annotation says what goes there.

---

### User Story 7 - The suite catches the documentation the linter does not check (Priority: P2)

A contributor adds a component with every `@prop` in place but forgets its `@description`, or writes an annotation that wraps onto a second line. The linter accepts both. The test suite does not.

**Why this priority**: Article XVI asks for more than the linter checks. Without this, the "documentation contract" in the issue would be only partly enforced. It is P2 because the linter gate in User Story 1 already catches the most common drift, an undocumented attribute.

**Independent Test**: In a scratch template, remove the `@description`, then separately wrap a `{# … #}` annotation onto two lines, then separately render the default slot with no `@slot`. Each time the suite fails and names the template. Restore the template and it passes.

**Acceptance Scenarios**:

1. **Given** a component with no `@description`, or with more than one, **When** the test suite runs, **Then** it fails and names the component.
2. **Given** a component that renders its default slot with no `@slot` annotation, **When** the test suite runs, **Then** it fails and names the component.
3. **Given** a `{#` comment that does not close on the same line, **When** the test suite runs, **Then** it fails and names the component and the line.
4. **Given** a component that renders no default slot, **When** the test suite runs, **Then** no `@slot` annotation is required.

---

### User Story 8 - Contributors can find how to run the gallery and the linter (Priority: P2)

A new contributor reads the repository's contributing guide and, from it alone, installs the development environment, opens the gallery in a browser, runs the linter, and understands that the test suite runs the same check.

**Why this priority**: The issue asks for it explicitly, and every later group feature depends on contributors running this loop. It is P2 because the gate protects the contract even when nobody reads the guide.

**Independent Test**: Follow `CONTRIBUTING.md` from a fresh clone and confirm each command works as written and the gallery opens at the address it gives.

**Acceptance Scenarios**:

1. **Given** the README, **When** a contributor looks for how to contribute, **Then** it links to `CONTRIBUTING.md`.
2. **Given** `CONTRIBUTING.md`, **When** a contributor follows it, **Then** it gives the commands to install the environment, start the gallery, run the linter and run the test suite, and the address where the gallery opens.
3. **Given** `CONTRIBUTING.md`, **When** a contributor reads about the linter, **Then** it says which findings fail (errors and warnings) and which do not (hints), and links to the gallery's annotation reference.
4. **Given** `CONTRIBUTING.md`, **When** a contributor reads about adding a component, **Then** it says a component is not done until it carries the annotations and the suite passes.

---

### Edge Cases

- A template's only findings are hints. The check passes. Hints are never promoted to failures, and none is suppressed by configuration.
- An attribute name is hyphenated in `<c-vars>` (`hide-label`), and the template reads its underscore form (`help_text`). The `@prop` uses the declared, hyphenated name, which is the name a caller writes.
- A component forwards named slots to another component (`modal` passes `actions` and `footer` to its inner `card`). Each component annotates the slots a caller can fill on it, even when it only forwards them.
- A component is added later by a group feature. It is picked up by both checks automatically, with no list of templates to maintain.
- The gallery prints a notice when its app loads. Running the lint inside the suite must not add that notice to the output of every test run.
- An existing `{# … #}` banner block, such as the header at the top of `modal.html`, is a run of single-line comments. It passes the single-line check. Its prose may be kept, moved into a `{% comment %}` block, or trimmed where annotations now say the same thing.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The test suite MUST run the gallery linter over every component template the package ships and fail when the linter reports any error or warning. (US1)
- **FR-002**: The linter check MUST pass when the only findings are hints. (US1)
- **FR-003**: A failure MUST report each finding with its component, line, rule and message, so it can be fixed without running the linter separately. (US1)
- **FR-004**: The linter check MUST discover component templates from the package's `cotton/` directory, so a newly added component is covered with no change to the test. (US1)
- **FR-005**: The linter check MUST run in every CI test job that runs the suite, across all supported Python and Django versions. (US1)
- **FR-006**: `button`, `link`, `badge`, `alert` and `icon` MUST each carry one `@description`, one `@prop` per `<c-vars>` name (type, default matching `<c-vars>` or `required`, description), and a `@slot` for the default slot if they render one. (US2)
- **FR-007**: `form.field` MUST carry the annotations in FR-006. The `@prop` descriptions for `label`, `help-text` and `errors` MUST say that a named slot of the same name also works. (US3)
- **FR-008**: The comment in `form/field.html` that names `<c-form.render>` MUST be reworded so the linter reports no `unknown-component` error, and so it names no component outside this package. (US3)
- **FR-009**: `card`, `modal`, `dropdown` and `divider` MUST carry the annotations in FR-006, plus a `@slot:name` for each named slot a caller can fill. (US4)
- **FR-010**: `modal` MUST carry a `@trigger` annotation describing how another element opens it. (US4)
- **FR-011**: `breadcrumbs`, `breadcrumbs.item`, `dock`, `dock.item`, `avatar` and `avatar.group` MUST carry the annotations in FR-006, plus a `@slot:name` for each named slot a caller can fill. (US5)
- **FR-012**: `mockup.browser`, `mockup.window`, `mockup.phone`, `mockup.code` and `mockup.code.line` MUST carry the annotations in FR-006. (US6)
- **FR-013**: Every annotation MUST be a single Django comment on a single line. Explanations too long for an annotation go in a `{% comment %}` block. (US2–US6)
- **FR-014**: No component's `<c-vars>` names, defaults or rendered output MAY change as part of annotating it. The only template change besides annotations is the comment rewording in FR-008 and moving or trimming existing explanatory comments. (US2–US6)
- **FR-015**: The test suite MUST fail, naming the component, when a component has no `@description` or more than one. (US7)
- **FR-016**: The test suite MUST fail, naming the component, when a component renders its default slot and carries no `@slot` annotation. (US7)
- **FR-017**: The test suite MUST fail, naming the component and line, when a `{#` comment in a component template does not close on the same line. (US7)
- **FR-018**: A `CONTRIBUTING.md` at the repository root MUST explain how to install the development environment, run the gallery (with the address it opens at), run the linter directly, and run the test suite. It MUST say which linter findings fail and link to the gallery's annotation reference. (US8)
- **FR-019**: The README MUST link to `CONTRIBUTING.md`. (US8)
- **FR-020**: The CHANGELOG MUST record that every component is now documented in the gallery and that the test suite enforces it. (US8)

### Key Entities

- **Annotation**: A one-line Django comment in a component template that the gallery reads: `@description`, `@prop`, `@slot`, `@slot:name` or `@trigger`, in the format the gallery's annotation reference defines.
- **Lint finding**: One result from the gallery's linter, with a severity (error, warning or hint), a rule, a component, a line and a message.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `uv run python manage.py cotton_lint --warnings-as-errors` exits successfully on main, with 21 of 21 components reporting no errors or warnings (from 3 of 21, with 1 error and 88 warnings, before this feature).
- **SC-002**: Adding an unannotated attribute to any component makes the test suite fail. Removing it makes the suite pass again.
- **SC-003**: Every CI test job on a pull request runs the gallery-lint check and the annotation check.
- **SC-004**: Each of the 21 components has one `@description`, and every one that renders its default slot has a `@slot`.
- **SC-005**: Following `CONTRIBUTING.md` from a fresh clone, a contributor reaches the running gallery and a passing lint run using only the commands it gives.
- **SC-006**: The rendered output of every existing component is unchanged. The existing tests pass without modification.

## Assumptions

- The component set is the 21 templates on main at the time of writing. Components added by later group features are covered by the checks automatically, and those features annotate them.
- Making the demo the gallery alone, and fixing gallery links that return 404 for folder components, belongs to issue #10. This feature adds nothing to the demo. It depends only on the linter being able to read the package's templates.
- The gallery stays a development dependency. Running the linter in the suite does not make it a runtime dependency of the package (Article VII, Article XII).
- Annotation types and defaults follow the gallery's annotation reference. Where a `<c-vars>` value is an expression or a translated string, the annotation's default is written the way the reference says to write such a value.
- The linter's rule set and severities are the ones in the pinned major version of the gallery (`>=1.0.0,<2`). A future gallery release that changes them is handled when the dependency is bumped.
- Attribute changes to bring existing components in line with Article XIV (the shared `variant`/`size` vocabulary) are out of scope. Each group's feature makes those changes and updates the annotations with them.
