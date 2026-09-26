# Feature Specification: Navigation components

**Feature Branch**: `003-navigation-components`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2, G3 · **Roadmap**: R2 · **Source**: issue #12

**Depends on**: issue #11 (annotation coverage and the gallery linter running in CI)

**Input**: Projects need daisyUI's navigation pieces as Cotton components: breadcrumbs, dock, link, megamenu, menu, navbar, steps and tabs. Breadcrumbs, dock and link already exist and should follow the same attribute conventions as the new ones. Each should render accessible markup and be shown in the gallery with its variants and states.

## Summary

Eight navigation components, one for each daisyUI navigation component that qualifies under G1:

- **New:** `menu`, `navbar`, `tabs`, `steps` and `megamenu`.
- **Brought in line:** `breadcrumbs`, `dock` and `link`, which already ship.

daisyUI lists pagination under navigation too. It gets no component. daisyUI builds it from `join` and `btn` and gives it no class of its own, so under G1 it is a composition rather than a base component. The README says so.

Menu and navbar are the frame most pages sit in. The attribute choices made here set the pattern the later component groups follow.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Menu (Priority: P1)

A developer builds a sidebar or a top-level list of links with `<c-menu>`. Items can be links or buttons, can be grouped under titles, and can nest into submenus that open and close without any script. The current page's item is marked active, and an item can be disabled.

**Why this priority**: The menu is the most common navigation surface in an application. Navbar, dropdown and megamenu content is usually built from it.

**Independent Test**: Render a menu with a title, three links (one active, one disabled) and a collapsible submenu. Check the classes, the active and disabled states, and that the submenu opens with the keyboard alone.

**Acceptance Scenarios**:

1. **Given** a menu with no attributes, **When** it renders, **Then** the root carries `menu` and lays out vertically.
2. **Given** `size="sm"`, **When** it renders, **Then** the root carries `menu-sm`, and a size outside `xs`–`xl` adds no size class.
3. **Given** `horizontal`, **When** it renders, **Then** the root carries `menu-horizontal`. Given `horizontal="lg"`, it carries `lg:menu-horizontal` instead.
4. **Given** an item with a link and `active`, **When** it renders, **Then** the link carries `menu-active` and `aria-current="page"`.
5. **Given** a disabled item, **When** it renders, **Then** it carries `menu-disabled`, is announced as disabled, and cannot be reached with Tab.
6. **Given** a titled group, **When** it renders, **Then** the title carries `menu-title` and is not an interactive element.
7. **Given** a collapsible submenu, **When** it renders, **Then** it uses a native disclosure (`<details>` and `<summary>`), opens and closes with Enter or Space, and can be rendered open.
8. **Given** `paged`, **When** the menu renders, **Then** the root carries `menu-paged`.

---

### User Story 2 - Navbar (Priority: P1)

A developer puts a bar across the top of a page with `<c-navbar>`: a brand at the start, links in the centre, account controls at the end, each through its own slot.

**Why this priority**: Nearly every page has one, and it hosts the menu from story 1.

**Independent Test**: Render a navbar with content in all three positions. Check each lands in its `navbar-start`, `navbar-center` or `navbar-end` section, and that the bar is exposed as a named navigation landmark.

**Acceptance Scenarios**:

1. **Given** content in the start, center and end slots, **When** the navbar renders, **Then** each lands inside the matching `navbar-start`, `navbar-center` or `navbar-end` element.
2. **Given** a slot left empty, **When** it renders, **Then** that section's element is not emitted.
3. **Given** content in the default slot only, **When** it renders, **Then** it lands directly inside the `navbar` root.
4. **Given** a navbar, **When** it renders, **Then** it is a navigation landmark with an accessible name the caller can override.
5. **Given** `class="bg-base-200"`, **When** it renders, **Then** that class is merged into the root's class list.

---

### User Story 3 - Link and breadcrumbs (Priority: P1)

A developer uses `<c-link>` for inline links and `<c-breadcrumbs>` for the trail to the current page, with the same attribute names every other component uses.

**Why this priority**: Both already ship and are in use. Aligning them is small, and doing it now keeps the breaking changes before 0.1.0.

**Independent Test**: Render a link in each colour and with `hover`, and a three-item breadcrumb trail built both from a list and from slotted items. Check the classes, the landmark and the current-page marker.

**Acceptance Scenarios**:

1. **Given** `<c-link href="/x" variant="primary">`, **When** it renders, **Then** it is an `<a href="/x">` with `link link-primary`.
2. **Given** `hover`, **When** the link renders, **Then** it carries `link-hover`.
3. **Given** a link with no `href`, **When** it renders, **Then** it emits no `href` attribute, rather than a placeholder `#`.
4. **Given** a breadcrumb trail, **When** it renders, **Then** it is a navigation landmark named "Breadcrumbs" (translatable), and its root carries only `breadcrumbs` plus the caller's classes.
5. **Given** a trail whose last item has no `href`, **When** it renders, **Then** that item is marked `aria-current="page"`.
6. **Given** a trail built from `items`, **When** it renders, **Then** it matches the same trail built from slotted items.

---

### User Story 4 - Tabs (Priority: P2)

A developer shows a row of tabs with `<c-tabs>`, in one of two shapes. Link tabs move between pages and mark the current one. Radio tabs switch between content panels on the same page using daisyUI's CSS alone.

**Why this priority**: Common on detail and settings pages, but fewer pages need tabs than need a menu.

**Independent Test**: Render link tabs with one active and one disabled, and radio tabs with three panels. Check the classes, the current-page marker, and that the radio tabs switch panels with the arrow keys and no script.

**Acceptance Scenarios**:

1. **Given** tabs with `box`, `border` or `lift`, **When** they render, **Then** the root carries `tabs-box`, `tabs-border` or `tabs-lift`.
2. **Given** `size="lg"`, **When** they render, **Then** the root carries `tabs-lg`.
3. **Given** `placement="bottom"`, **When** they render, **Then** the root carries `tabs-bottom`.
4. **Given** a tab with an `href` and `active`, **When** it renders, **Then** it is a link carrying `tab tab-active` and `aria-current="page"`.
5. **Given** a disabled tab, **When** it renders, **Then** it carries `tab-disabled`, is announced as disabled and cannot be reached with Tab.
6. **Given** radio tabs, **When** they render, **Then** the root has `role="tablist"`, each tab is a radio input with `tab` and an accessible name, the tabs share one group name, each panel carries `tab-content` and follows its tab, and one tab can be rendered selected.
7. **Given** a tab with no `href` outside radio shape, **When** it renders, **Then** it is a `<button type="button">` with `role="tab"`, for a project that adds its own switching script.

---

### User Story 5 - Dock (Priority: P2)

A developer adds a bottom navigation bar for small screens with `<c-dock>` and `<c-dock.item>`. Each item is an icon with a label, and one is marked active.

**Why this priority**: Already shipped and useful on mobile, but only projects with a mobile layout need it.

**Independent Test**: Render a dock with three items (a link, a drawer toggle and a button), one active and one icon-only. Check the classes, the landmark, the active marker and each item's accessible name.

**Acceptance Scenarios**:

1. **Given** `size="sm"`, **When** the dock renders, **Then** the root carries `dock dock-sm` and no classes daisyUI does not define for the dock.
2. **Given** `class` or any other attribute on the dock, **When** it renders, **Then** the class is merged into the root and the rest reach the root element.
3. **Given** a dock, **When** it renders, **Then** it is a navigation landmark with an accessible name the caller can override.
4. **Given** an active link item, **When** it renders, **Then** it carries `dock-active` and `aria-current="page"`.
5. **Given** an item with an icon and `label`, **When** it renders, **Then** the icon comes from `<c-icon>`, the label sits inside `dock-label`, and the item's accessible name is the label.
6. **Given** an item with neither `href` nor `toggle`, **When** it renders, **Then** it is a `<button type="button">`.

---

### User Story 6 - Steps (Priority: P3)

A developer shows progress through a multi-step process with `<c-steps>`, colouring the completed steps and marking the current one.

**Why this priority**: Wizards and checkouts use it, a narrower need than the stories above.

**Independent Test**: Render four steps, the first two coloured primary and the second marked current, one with custom content and one with an icon, first horizontal and then vertical.

**Acceptance Scenarios**:

1. **Given** steps with no attributes, **When** they render, **Then** the root carries `steps` and is announced as an ordered list.
2. **Given** `vertical`, **When** they render, **Then** the root carries `steps-vertical`. Given `vertical` with a `horizontal` breakpoint such as `lg`, it carries `steps-vertical lg:steps-horizontal`.
3. **Given** a step with `variant="primary"`, **When** it renders, **Then** it carries `step step-primary`.
4. **Given** a step marked `current`, **When** it renders, **Then** it carries `aria-current="step"`.
5. **Given** a step with custom content, **When** it renders, **Then** the value is written to `data-content`.
6. **Given** a step with an icon, **When** it renders, **Then** the icon comes from `<c-icon>` inside a `step-icon` element.

---

### User Story 7 - Megamenu (Priority: P3)

A developer puts a large horizontal menu at the top of a marketing or documentation site with `<c-megamenu>`. Each item is a button that opens a panel of links through the browser's native popover, with no script. On small screens the megamenu hides behind a toggle button and lays out vertically, as daisyUI documents.

**Why this priority**: A newer component that only larger sites need.

**Independent Test**: Render a megamenu with three items whose panels hold a menu. Check the classes, that every button targets its own panel, that no id repeats, and that the whole thing opens and closes with the keyboard.

**Acceptance Scenarios**:

1. **Given** a megamenu, **When** it renders, **Then** its root carries `megamenu max-sm:megamenu-vertical` and contains the `megamenu-active` indicator.
2. **Given** `wide` or `full`, **When** it renders, **Then** the root carries `megamenu-wide` or `megamenu-full`, and `size="md"` adds `megamenu-md`.
3. **Given** three items, **When** the megamenu renders, **Then** each item's button has a `popovertarget` equal to its own panel's `id`, and no id repeats on the page.
4. **Given** a megamenu, **When** it renders, **Then** a small-screen toggle button, rendered through `<c-button>`, opens the megamenu, and the toggle is hidden from `sm` up.
5. **Given** a megamenu, **When** it renders, **Then** it is a navigation landmark with an accessible name, and each item button exposes whether its panel is open.

---

### Edge Cases

- An out-of-range `size` or an unknown `variant` adds no modifier class, rather than a class daisyUI does not define.
- An icon-only item (dock, menu) with no `label` still needs an accessible name. The caller supplies it through `aria-label`, and the gallery example shows how.
- A menu or tabs with several items marked `active` renders each as given. The component does not pick one.
- Breadcrumbs with a single item render that item as the current page.
- Two megamenus on one page stay valid only if they have different ids, which is why the megamenu requires one.
- daisyUI supports at most ten megamenu items. The component does not enforce the limit, and the gallery entry mentions it.

## Requirements *(mandatory)*

### Functional Requirements

**Shared across the group**

- **FR-001**: Every component in the group MUST name its attributes per the constitution's attribute vocabulary: `variant` for colour, `size` on daisyUI's `xs`–`xl` scale, daisyUI's own modifier names as boolean attributes, `class` merged into the root's class list, and everything else passed through to the root element.
- **FR-002**: Every component MUST take its colours from daisyUI's semantic roles only, and MUST NOT emit a literal colour or a class daisyUI does not define for that component.
- **FR-003**: A component that renders another component's output (an icon, a button, a menu item) MUST call it as that Cotton component.
- **FR-004**: The package MUST ship no JavaScript for this group. Submenus, radio tabs and megamenu panels MUST work through native HTML (`<details>`, radio inputs, the `popover` attribute) and daisyUI's CSS.
- **FR-005**: Every interactive element MUST be reachable and operable with the keyboard, MUST keep daisyUI's visible focus style, and MUST expose its role, name and state (current, active, disabled, expanded, selected) to assistive technology.
- **FR-006**: Every component that is a navigation region (breadcrumbs, dock, megamenu, navbar) MUST render as a navigation landmark with a translatable default accessible name the caller can override.
- **FR-007**: Every component template MUST carry the gallery annotations the constitution requires, and the gallery linter MUST pass with warnings treated as errors.
- **FR-008**: Every component MUST have a gallery entry that renders each of its variants, sizes, style modifiers and states (active, disabled, current, open), so a developer can pick attributes without opening the template.
- **FR-009**: The README MUST list the new components, and MUST record that pagination has no component of its own and why.
- **FR-010**: Every breaking change to `breadcrumbs`, `dock` or `link` MUST be recorded in the CHANGELOG with what a project changes to keep working.

**Menu**

- **FR-011**: The menu MUST support `size`, a `horizontal` direction that is either always on or on from a named breakpoint, and the `paged` modifier.
- **FR-012**: Menu items MUST support links and buttons, `active` (adding `menu-active` and, on a link, `aria-current="page"`) and `disabled` (adding `menu-disabled`).
- **FR-013**: The menu MUST support titled groups (`menu-title`) and collapsible submenus through `<details>` and `<summary>`, which can be rendered open and nest at least two levels deep.

**Navbar**

- **FR-014**: The navbar MUST provide `start`, `center` and `end` slots, each rendering its `navbar-*` section only when given content, plus a default slot rendered directly inside the root.

**Link and breadcrumbs**

- **FR-015**: The link MUST support every colour daisyUI defines for it through `variant`, plus `hover`. It MUST NOT emit an `href` the caller did not give.
- **FR-016**: Breadcrumbs MUST keep building a trail from either an `items` list or slotted items with identical output, and MUST mark a final item that has no `href` as the current page.
- **FR-017**: The breadcrumbs root MUST carry only `breadcrumbs` and the caller's classes, dropping the text-size class it ships with today.

**Tabs**

- **FR-018**: Tabs MUST support the `box`, `border` and `lift` styles, `size`, and `placement` (`top` or `bottom`).
- **FR-019**: A tab MUST render as a link when given an `href`, as a native radio input followed by its `tab-content` panel when the tabs are in radio shape, and as a `<button type="button" role="tab">` otherwise. Tabs MUST support `active` and `disabled`.
- **FR-020**: Radio-shaped tabs MUST share one group name per set, give each radio an accessible name, and let the caller choose which tab starts selected.

**Dock**

- **FR-021**: The dock root MUST carry only `dock`, its size class and the caller's classes, and MUST pass other attributes through. It drops the transparent background and blur it adds today.
- **FR-022**: A dock item MUST render as a link, a drawer toggle or a `<button type="button">` as it does today, with `active` adding `dock-active` (and `aria-current="page"` on a link) and the label serving as its accessible name.

**Steps**

- **FR-023**: Steps MUST render as an ordered list and support a `vertical` direction that can turn horizontal again from a named breakpoint.
- **FR-024**: A step MUST support `variant`, `current` (adding `aria-current="step"`), custom content written to `data-content`, and an icon inside `step-icon`.

**Megamenu**

- **FR-025**: The megamenu MUST require an id, emit the `megamenu-active` indicator, lay out vertically below `sm`, and render a small-screen toggle through `<c-button>` that opens it.
- **FR-026**: The megamenu MUST support `wide`, `full` and `size`. Each item MUST pair a button with its own popover panel, and the panel ids MUST be built from the megamenu's id so they are unique on the page.

### Key Entities

- **Navigation component**: one of the eight Cotton components above, with its item or section parts.
- **Item**: a single entry in a menu, tabs, steps, breadcrumbs, dock or megamenu, carrying its own state (active, disabled, current).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All eight components render without error in the test suite, and each acceptance scenario above has a test that fails if the behaviour is removed.
- **SC-002**: The gallery linter reports zero errors and zero warnings across the group.
- **SC-003**: Every component has a gallery entry showing every variant, size, modifier and state listed in its requirements.
- **SC-004**: An automated accessibility check of each gallery entry finds no violations, and every interactive element in the group can be reached and operated with the keyboard alone.
- **SC-005**: No template in the group emits a `<script>` element or an inline event handler.
- **SC-006**: Coverage stays at or above the constitution's floors (project 90%, patch 85%).

## Clarifications

### Session 2026-09-26

- Q: Which navigation components are in scope? → A: Breadcrumbs, dock, link, megamenu, menu, navbar, steps and tabs. Pagination is out: daisyUI builds it from `join` and `btn` and gives it no class of its own. The README records why.
- Q: How are direction modifiers named? → A: With daisyUI's direction word as the attribute (`horizontal` on menu, `vertical` on steps). Each takes either a boolean or a breakpoint name, the way `divider` already takes `vertical`.
- Q: Which menu modifiers become attributes? → A: `size`, `horizontal` and `paged` on the menu, `active` and `disabled` on items. `menu-dropdown`, `menu-dropdown-toggle`, `menu-dropdown-show` and `menu-focus` exist for a script to toggle, so a project that wants them passes them through `class`.
- Q: What does a tab with no `href` render outside radio shape? → A: A `<button type="button" role="tab">`, the markup daisyUI documents. The package ships no switching script, so a project adds one if it wants it.
- Q: Where do extra attributes go on list items such as menu and breadcrumb items? → A: To the item's root element, as the constitution requires. A caller who needs full control of the link inside writes it in the item's slot.
- Q: Does the megamenu include its small-screen toggle? → A: Yes. daisyUI's documented megamenu includes it, and without it the megamenu cannot be opened below `sm`.
- Q: Are the extra classes breadcrumbs and dock carry today kept? → A: No. `text-sm` on breadcrumbs and `bg-transparent backdrop-blur` on the dock are not part of daisyUI's markup for either. A project that wants them passes them through `class`. Both are breaking changes and go in the CHANGELOG.

## Assumptions

- Annotation coverage and the gallery linter from issue #11 land first, so this feature adds its components to a gate that already runs.
- The megamenu targets browsers that support the `popover` attribute, as daisyUI's own megamenu does.
- Breaking attribute changes to `breadcrumbs`, `dock` and `link` are acceptable before 0.1.0.
- Driving any of these components from Django objects (a URL resolver, a paginator, a menu registry) is out of scope and stays with the project.
