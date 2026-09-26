# Feature Specification: Layout components

**Feature Branch**: `004-layout-components`

**Created**: 2026-09-26

**Status**: Draft

**Input**: Issue #13, "Layout components": divider, drawer, footer, hero, indicator, join, mask and stack as Cotton components, with the four existing mockups brought to the same bar.

**Serves**: G1, G2, G3 · **Roadmap**: R3 · **Depends on**: #11 (every component annotated for the gallery, and the gallery linter enforced in the test suite)

## Summary

daisyUI's layout components arrange other content. A drawer puts a sidebar beside a page, a footer
closes it, a join fuses buttons and inputs into one control, an indicator pins a badge to a corner,
a stack piles cards on top of each other, and a mask crops an image to a shape. This feature gives
each of them a Cotton component. The package already ships `divider` and four mockups
(`mockup.browser`, `mockup.code` with `mockup.code.line`, `mockup.phone`, `mockup.window`). They
come out of this feature with the same attribute vocabulary, accessibility defaults and gallery
coverage as the new components.

Every component emits the markup and classes daisyUI documents, takes its colours from the
semantic palette, names its attributes as `CONSTITUTION.md` Article XIV requires, and ships no
JavaScript. The drawer opens and closes through daisyUI's own checkbox toggle, so it needs no
script.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Page with a sidebar drawer (Priority: P1)

A project developer builds an application page with a navigation sidebar. On small screens the
sidebar is hidden and opens over the page from a button. On large screens it stays open beside the
content. They write `<c-drawer>` with the page in the default slot and the sidebar in a `side`
slot, put a `<c-drawer.button>` wherever the opener belongs, and get daisyUI's drawer without
writing its markup by hand.

**Why this priority**: Almost every application built on daisyUI has a sidebar, and the drawer's
markup (a hidden checkbox, matching ids, an overlay label) is the easiest to get wrong by hand.

**Independent Test**: Render a drawer with page content, a sidebar and an opener. Check the
markup against daisyUI's documented structure, then open and close it in the demo using only the
keyboard.

**Acceptance Scenarios**:

1. **Given** a drawer with `id="nav"`, page content and a `side` slot, **When** it renders, **Then** the output is daisyUI's drawer: the `drawer` root, a `drawer-toggle` checkbox with id `nav`, the page inside `drawer-content`, and the sidebar inside `drawer-side` after a `drawer-overlay` label pointing at `nav`.
2. **Given** a `<c-drawer.button drawer="nav">` anywhere on the page, **When** it is activated, **Then** the drawer with id `nav` opens, and activating it again or activating the overlay closes it.
3. **Given** `open="lg"`, **When** the drawer renders, **Then** its root carries `lg:drawer-open` and the sidebar stays visible from the large breakpoint up. **Given** `open` with no value, **Then** it carries `drawer-open` at every width.
4. **Given** `position="end"`, **When** the drawer renders, **Then** its root carries `drawer-end` and the sidebar opens from the other side.
5. **Given** a keyboard user, **When** they tab to the drawer's toggle, **Then** focus is visible on the opener, Space opens and closes the drawer, and the toggle and the overlay each have an accessible name in the active language.

---

### User Story 2 - Page footer (Priority: P1)

A developer ends every page with a footer holding a logo, a copyright line and a few groups of
links. They write `<c-footer>` with `<c-footer.nav title="Company">` groups inside it and get
daisyUI's footer, stacked on phones and laid out in a row from a breakpoint they choose.

**Why this priority**: Nearly every site has a footer, and it appears on every page.

**Independent Test**: Render a footer with two link groups and some free-form content, in each
direction and alignment, and check the markup and landmarks.

**Acceptance Scenarios**:

1. **Given** a footer with content, **When** it renders, **Then** the root is a `<footer>` element carrying `footer` and the caller's classes.
2. **Given** `horizontal="sm"`, **When** it renders, **Then** the root carries `sm:footer-horizontal`. **Given** `vertical`, it carries `footer-vertical`. **Given** `position="center"`, it carries `footer-center`.
3. **Given** two `<c-footer.nav>` groups titled "Company" and "Legal", **When** they render, **Then** each is a `<nav>` whose accessible name is its title, and each title carries `footer-title`, so the two navigation landmarks can be told apart by name.
4. **Given** free-form content such as a logo and a copyright line, **When** the footer renders, **Then** that content passes through unchanged beside the link groups.

---

### User Story 3 - Divider brought to the bar (Priority: P1)

A developer separates two sections of a page, or two columns side by side, with a divider that may
carry a short label such as "OR". The existing `divider` keeps doing this, now with daisyUI's own
names for its direction modifiers and with separator semantics for assistive technology.

**Why this priority**: The divider already ships and is used often. Its current `vertical`
attribute emits daisyUI's `divider-horizontal`, the opposite of what the name says, and that is
worth fixing before anyone depends on it.

**Independent Test**: Render the divider in every direction, colour and alignment, with and
without a label, and check its classes and role.

**Acceptance Scenarios**:

1. **Given** `horizontal`, **When** the divider renders, **Then** it carries `divider-horizontal` (a vertical line between side-by-side content). **Given** `vertical`, it carries `divider-vertical`. **Given** `horizontal="md"`, it carries `md:divider-horizontal`.
2. **Given** `variant="primary"`, **When** it renders, **Then** it carries `divider-primary`, and each of daisyUI's other divider colours works the same way.
3. **Given** `position="start"` or `position="end"`, **When** it renders, **Then** it carries `divider-start` or `divider-end`.
4. **Given** no label, **When** it renders, **Then** assistive technology sees a separator, with a vertical orientation when it separates side-by-side content.
5. **Given** a label such as "OR" in the default slot or the `text` attribute, **When** it renders, **Then** assistive technology can read the label.

---

### User Story 4 - Joined controls (Priority: P2)

A developer builds a search box fused to its button, a segmented set of buttons, or a pager. They
wrap the pieces in `<c-join>` and give each one `class="join-item"`, and daisyUI rounds only the
outer corners.

**Why this priority**: Common in forms and toolbars, but a page works without it.

**Independent Test**: Render a join of three buttons, and a join of an input and a button, in
both directions, and check the markup and the group's accessible name.

**Acceptance Scenarios**:

1. **Given** a join with children, **When** it renders, **Then** the root carries `join` and is exposed to assistive technology as a group, named by an `aria-label` the caller passes.
2. **Given** `vertical horizontal="lg"`, **When** it renders, **Then** the root carries both `join-vertical` and `lg:join-horizontal`, stacking the items on small screens and lining them up from the large breakpoint.
3. **Given** children that are this package's own components with `class="join-item"`, **When** the join renders, **Then** each child carries `join-item` on its own root element, with no wrapper element between the join and the child.

---

### User Story 5 - Indicator on a corner (Priority: P2)

A developer puts an unread count on the corner of an inbox button or a status dot on an avatar.
They wrap the target in `<c-indicator>` and put one or more `<c-indicator.item>` elements in its
`items` slot, each at the corner it names.

**Why this priority**: Notification counts and status dots are frequent in application chrome,
but not needed on every page.

**Independent Test**: Render an indicator with items at several positions around a button and
check the classes, the element order and what a screen reader hears.

**Acceptance Scenarios**:

1. **Given** an indicator with main content and one item, **When** it renders, **Then** the root carries `indicator`, and the item carries `indicator-item` and sits before the main content, as daisyUI requires, whatever order the caller wrote them in.
2. **Given** an item with `position="bottom start"`, **When** it renders, **Then** it carries `indicator-bottom` and `indicator-start`. **Given** no position, it carries neither and takes daisyUI's default top-end corner.
3. **Given** several items, **When** the indicator renders, **Then** each item keeps its own position.
4. **Given** the gallery example of a count on a button, **When** a screen reader reads it, **Then** the count's meaning is announced in words, not as a bare number.

---

### User Story 6 - Hero (Priority: P2)

A developer opens a landing page with a large banner: a heading, a line of copy and a call to
action, optionally over a background image with a tinted overlay. They write `<c-hero>` with that
content in the default slot and get daisyUI's hero container. The heading, copy and buttons are
theirs. The component is the container, not a finished page section.

**Why this priority**: Used on landing and marketing pages, less often inside applications.

**Independent Test**: Render a hero with and without an overlay and a background image, and
check the markup.

**Acceptance Scenarios**:

1. **Given** a hero with content, **When** it renders, **Then** the root carries `hero` and the caller's classes and attributes, and the content sits inside `hero-content`.
2. **Given** `overlay`, **When** it renders, **Then** a `hero-overlay` layer sits between the background and the content and is hidden from assistive technology.
3. **Given** a background image passed in the root's `style` attribute, **When** it renders, **Then** the style reaches the root unchanged.

---

### User Story 7 - Mask and stack (Priority: P3)

A developer crops an avatar to a squircle or a product image to a hexagon with `<c-mask>`, and piles
notification cards or photos on top of each other with `<c-stack>`.

**Why this priority**: Visual treatments. A page without them looks plainer but loses nothing.

**Independent Test**: Render a mask in each shape and each half, with an image and with slotted
content, and a stack at each position, then check the classes and the image's text alternative.

**Acceptance Scenarios**:

1. **Given** `<c-mask shape="squircle" src="…" alt="Profile photo">`, **When** it renders, **Then** it emits an `<img>` carrying `mask` and `mask-squircle` with that `src` and `alt`.
2. **Given** `half="1"` or `half="2"`, **When** it renders, **Then** it also carries `mask-half-1` or `mask-half-2`.
3. **Given** a mask with no `src` and slotted content, **When** it renders, **Then** it emits a container carrying the mask classes around that content.
4. **Given** a mask with `src` but no `alt`, **When** it renders, **Then** the image carries an empty `alt`, marking it decorative, and never omits the attribute.
5. **Given** a stack with three children and `position="top"`, **When** it renders, **Then** the root carries `stack` and `stack-top`, and every child stays available to assistive technology.

---

### User Story 8 - Mockups brought to the bar (Priority: P3)

A developer shows a screenshot inside a browser frame, a terminal session in a code mockup, or a
mobile screen in a phone frame, usually on a documentation or marketing page. The four existing
mockups keep working, and now every one takes `class` and extra attributes, uses only the
semantic palette, and forces no size or layout on the caller's content.

**Why this priority**: The mockups already ship and appear mostly on marketing pages. The work is
consistency, not new capability.

**Independent Test**: Render each mockup with content, extra classes and an extra attribute, and
check the markup, colours and accessibility.

**Acceptance Scenarios**:

1. **Given** `mockup.browser`, `mockup.code`, `mockup.phone` or `mockup.window` with `class` and another attribute, **When** it renders, **Then** the class is merged into the root's class list and the attribute reaches the root.
2. **Given** `mockup.phone`, **When** it renders, **Then** its display area uses semantic palette colours, never a literal Tailwind colour.
3. **Given** `mockup.window` with content, **When** it renders, **Then** no fixed height or centring is imposed on that content.
4. **Given** `mockup.browser` with `url`, **When** it renders, **Then** the URL shows in the toolbar and assistive technology can read it, while decorative parts of every mockup (the phone's camera, the window and browser chrome) are hidden from assistive technology.
5. **Given** `mockup.code` whose lines are wider than the box, **When** a keyboard user tabs to it, **Then** it shows visible focus and scrolls with the arrow keys.
6. **Given** `mockup.code.line` with no `prefix`, **When** it renders, **Then** the line has no prefix. **Given** `prefix="$"`, it shows `$` before the line.

---

### Edge Cases

- **Drawer without an id**: the drawer cannot be wired to its opener without one. `id` is declared
  required in the drawer's annotations, so the gallery shows it as required.
- **Two drawers on one page**: each opener and overlay targets its own drawer by id, and opening
  one leaves the other alone.
- **Both directions on one component** (`vertical horizontal="lg"`): both classes are emitted as
  asked. This is daisyUI's own responsive pattern, not a conflict.
- **An enumerated attribute given a value daisyUI does not define** (`variant="pink"`,
  `shape="blob"`, `position="left"`): no modifier class is emitted for it, the component renders
  with daisyUI's default, and nothing raises.
- **A mask with no `shape`**: `shape` is declared required. Without it the element carries only
  `mask`, which crops nothing and does no harm.
- **An indicator with no items**: the main content renders unchanged inside the `indicator` root.
- **A footer with no `footer.nav` groups**: free-form content renders unchanged.
- **A caller-supplied `role`**: where a component sets a role by default (the join's group, the
  divider's separator), the caller's `role` replaces it. The element never ends up with two `role`
  attributes.

## Requirements *(mandatory)*

### Functional Requirements

**Shared**

- **FR-001**: The package MUST ship Cotton components `drawer`, `drawer.button`, `footer`, `footer.nav`, `hero`, `indicator`, `indicator.item`, `join`, `mask` and `stack`, alongside the existing `divider`, `mockup.browser`, `mockup.code`, `mockup.code.line`, `mockup.phone` and `mockup.window`. (All stories)
- **FR-002**: Every component in FR-001 MUST emit the element structure and class names daisyUI documents for it, and MUST take every colour from the semantic palette, never a literal Tailwind colour or hard-coded value. (All stories)
- **FR-003**: Every component in FR-001 MUST declare `class` and merge it into its root element's class list, and MUST pass every attribute it does not declare through to its root element. (All stories)
- **FR-004**: Modifiers MUST use daisyUI's names: `variant` for colour, `position` for placement (taking daisyUI's placement suffixes such as `start`, `end`, `top`, `bottom`, `center`), and the boolean direction modifiers `horizontal` and `vertical`. A direction modifier or `open` given with no value MUST emit daisyUI's class. Given a breakpoint name (`sm`, `md`, `lg`, `xl`, `2xl`), it MUST emit that class behind the breakpoint prefix. A value daisyUI does not define MUST emit no modifier class and MUST NOT raise. (All stories)
- **FR-005**: Components in this feature MUST NOT ship or require JavaScript. (All stories)
- **FR-006**: Any accessible name the package writes itself (the drawer's toggle and overlay) MUST be translatable. (US1)
- **FR-007**: Every component in FR-001 MUST carry the gallery annotations Article XVI requires, and `cotton_lint --warnings-as-errors` MUST pass. (All stories)
- **FR-008**: The component gallery MUST show each component in FR-001 in each of its variants and states: every colour, direction, position, shape and open state it supports, plus a responsive example wherever it accepts a breakpoint. (All stories)
- **FR-009**: The README MUST list the new components, and the CHANGELOG MUST record the new components and every changed attribute on `divider` and the mockups. The README's scope note that heroes are not shipped MUST be reworded to match what ships: the `hero` container ships, and composed hero sections built from it stay with the project. (All stories)

**Drawer**

- **FR-010**: `drawer` MUST require an `id`, render the page from its default slot inside `drawer-content` and the sidebar from a `side` slot inside `drawer-side`, and emit a `drawer-overlay` label for the same id before the sidebar. (US1)
- **FR-011**: `drawer` MUST accept `open` (daisyUI's `drawer-open`, per FR-004) and `position="end"` (`drawer-end`). (US1)
- **FR-012**: `drawer.button` MUST toggle the drawer whose id it names, carry `drawer-button`, and show visible focus when reached by keyboard. The drawer's toggle and overlay MUST each have an accessible name. (US1)

**Footer**

- **FR-013**: `footer` MUST render a `<footer>` element carrying `footer`, and accept `horizontal` and `vertical` (per FR-004) and `position="center"`. (US2)
- **FR-014**: `footer.nav` MUST render a `<nav>` whose accessible name is its `title`, with the title carrying `footer-title`, followed by its default slot. (US2)

**Divider**

- **FR-015**: `divider` MUST map `horizontal` to `divider-horizontal` and `vertical` to `divider-vertical` (per FR-004), `variant` to daisyUI's divider colours, and `position` to `divider-start` or `divider-end`. Its label MUST come from the default slot or a `text` attribute. (US3)
- **FR-016**: An unlabelled `divider` MUST be exposed as a separator, with a vertical orientation when `horizontal` applies at every width. A labelled `divider` MUST leave its label readable. (US3)

**Join**

- **FR-017**: `join` MUST carry `join`, accept `horizontal` and `vertical` (per FR-004), be exposed as a group to assistive technology, and add no wrapper around its children. (US4)

**Indicator**

- **FR-018**: `indicator` MUST render its `items` slot before its default slot inside the `indicator` root. (US5)
- **FR-019**: `indicator.item` MUST carry `indicator-item` and accept `position` with up to one horizontal placement (`start`, `center`, `end`) and one vertical placement (`top`, `middle`, `bottom`). (US5)

**Hero**

- **FR-020**: `hero` MUST render its default slot inside `hero-content`, and with `overlay` MUST add a `hero-overlay` layer hidden from assistive technology. (US6)

**Mask and stack**

- **FR-021**: `mask` MUST accept a required `shape` (one of daisyUI's mask styles) and an optional `half` (`1` or `2`). With `src` it MUST emit an `<img>` that always carries an `alt` attribute, empty when none is given. Without `src` it MUST emit a container around its default slot. (US7)
- **FR-022**: `stack` MUST carry `stack` and accept `position` (`top`, `bottom`, `start`, `end`). (US7)

**Mockups**

- **FR-023**: Each mockup MUST emit daisyUI's structure for it with no fixed size, centring or literal colour imposed on the caller's content, and MUST hide its decorative parts from assistive technology. `mockup.browser` MUST keep its `url` readable. (US8)
- **FR-024**: `mockup.code` MUST be reachable by keyboard with visible focus, so overflowing lines can be scrolled. `mockup.code.line` MUST emit a prefix only when `prefix` is given. (US8)

### Key Entities

- **Layout component**: a component whose job is to arrange or frame other content (a sidebar, a footer, a group of controls, a corner badge, a pile, a shape) rather than show a value of its own.
- **Part component**: a component that only makes sense inside its parent, or pointed at it (`drawer.button`, `footer.nav`, `indicator.item`, `mockup.code.line`), named the way the package already names `dock.item` and `breadcrumbs.item`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 16 components in FR-001 render, and each one's output matches the element structure and class names daisyUI documents, checked by a test per component.
- **SC-002**: `cotton_lint --warnings-as-errors` passes with every component in FR-001 annotated.
- **SC-003**: Every variant, direction, position, shape and open state listed in FR-008 appears in the component gallery, with none missing.
- **SC-004**: An automated accessibility check of each component's gallery page reports no violations, and the drawer opens, closes and shows focus using only the keyboard.
- **SC-005**: No template in this feature contains a literal Tailwind colour or a hard-coded colour value.
- **SC-006**: A developer can build a page with a responsive sidebar drawer and a footer from the gallery's documentation alone, without opening either template.

## Clarifications

### Session 2026-09-26

- Q: The divider's `vertical` attribute currently emits `divider-horizontal`. Keep it, or follow daisyUI's names? → A: Follow daisyUI. `horizontal` emits `divider-horizontal` and `vertical` emits `divider-vertical`. This reverses the meaning of `vertical` for existing callers, which is acceptable before 0.1.0 and goes in the CHANGELOG.
- Q: How are direction, placement and open state named across components? → A: Direction is two boolean attributes named as daisyUI names the modifiers (`horizontal`, `vertical`), each also taking a breakpoint name for the responsive form, because daisyUI's own responsive pattern puts both on one element. Placement is `position`, which `divider` and `modal` already use for the same idea. The drawer's `drawer-open` is a boolean `open` that also takes a breakpoint.
- Q: A mask has fourteen mutually exclusive shapes. Fourteen booleans, or one attribute? → A: One attribute, `shape`, the word daisyUI uses for what a mask does. The shapes exclude each other the way colours do, and several names (`hexagon-2`, `triangle-3`) would make awkward attribute names.
- Q: The README says heroes are not shipped, yet the issue asks for a hero. → A: `hero` ships as daisyUI's container (`hero`, `hero-content`, `hero-overlay`), which is a daisyUI component under G1. Composed hero sections, with a heading, copy and calls to action, stay with the project. The README line is reworded to say so.
- Q: Does `join` need a `join.item` part? → A: No. daisyUI needs `join-item` on the control itself, and a wrapper element would break the styling. Callers pass `class="join-item"` to each child, which every component here accepts.

## Assumptions

- The gallery annotations and the linter gate arrive with #11. This feature adds annotations for its own components and updates those on `divider` and the mockups where their attributes change.
- The project supplies daisyUI 5 and its themes. The drawer's toggle, its focus style and the `is-drawer-open`/`is-drawer-close` variants come from daisyUI's CSS. A caller uses those variants in its own classes, and the package emits nothing for them.
- The sidebar's contents, usually a menu, are the caller's. The menu component belongs to the navigation components feature, not this one.
- Accessibility is judged on what these components emit. Slotted content is the caller's responsibility, and the gallery demonstrates accessible usage, such as a count with a text alternative.
