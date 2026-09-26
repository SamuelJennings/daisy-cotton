# Feature Specification: Content display components

**Feature Branch**: `006-content-display-components`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2, G3 · **Roadmap**: R5 · **Depends on**: #11 (gallery annotations and the lint check in CI)

**Input**: Issue #15, "Content display components": accordion and collapse, avatar, badge, card, kbd, list, stat, status, table and timeline. Avatar, badge and card already exist. Each should be accessible and shown in the gallery with its variants and states.

## Scope

These are the components for showing ordinary content. Roadmap item R5 also lists aura, carousel, chat bubble, countdown, diff, hover 3D card, hover gallery and text rotate. Those belong to issue #16 and are not part of this feature.

| Component | State today | This feature |
|---|---|---|
| Card | exists | brought to the attribute vocabulary and the accessibility bar |
| Badge | exists | brought to the attribute vocabulary and the accessibility bar |
| Avatar, avatar group | exist | brought to the attribute vocabulary and the accessibility bar |
| Table | missing | new |
| Collapse | missing | new |
| Accordion | missing | new, built on the collapse |
| List, list row | missing | new |
| Stat, stat group | missing | new |
| Timeline, timeline item | missing | new |
| Kbd | missing | new |
| Status | missing | new |

daisyUI builds its accordion from the `collapse` classes, so under the README's *Scope & philosophy* it would normally get no component of its own. It is included by the maintainer's decision, because adopters expect an accordion in any component library. It is a thin component over `<c-collapse>`, and it adds only what makes a group of collapses behave as an accordion.

Out of scope: any JavaScript, and rendering querysets, model instances or other Django objects. The table takes the rows and cells the caller writes. It does not build them from data.

## Clarifications

### Session 2026-09-26

- Q: How do the collapse and the accordion open and close with no script, and how do they report their state? → A: Both use `<details>` and `<summary>`, which daisyUI supports for the collapse. The browser handles the keyboard and reports whether each item is expanded. An accordion is a set of collapses sharing a `name`, which the browser treats as one group where opening one item closes the others. daisyUI's radio-input method is not used: it announces each item as a radio button, and an open item cannot be closed again.
- Q: Does `<c-accordion>` wrap the whole group, or one item? → A: One item, the same as daisyUI's own accordion markup, where the group is formed by a shared name. A Cotton parent cannot hand a value down to the components in its slot, so a group wrapper would still need the name on every item and would add nothing. `name` is required on `<c-accordion>`.
- Q: Does `open` on a collapse force it open? → A: No. It renders the item already expanded, and the user can still close it. daisyUI's `collapse-open` and `collapse-close` classes, which lock the state, are not offered as attributes. They would turn the control into something that looks interactive and is not.
- Q: Does the card keep its header layout with `icon`, `badges`, `footer` and `footer_end`? → A: No. It renders daisyUI's card structure: an optional figure, a body, a title, and an actions row. `title` stays as an attribute or a named slot. `actions` stays and moves into daisyUI's actions row at the foot of the body. `icon`, `badges`, `footer`, `footer_end` and `tight` go. A caller who wants an icon or badges in the title fills the `title` slot.
- Q: Does the card keep its `bg-base-100 shadow-sm` surface? → A: No. It emits `card` and the modifiers the caller asks for. Surface colour and shadow go through `class`, as in daisyUI's examples. The component cannot remove a class it always adds, so a built-in surface would stop callers from choosing their own.
- Q: What is the extra-classes attribute for an inner element called? → A: `content_class`, the name the dropdown and modal use for their inner surface. It applies to the card's body, the avatar's image frame and the table's `<table>`. The card's `body_class` becomes `content_class`.
- Q: Which avatar attributes survive? → A: `src`, `alt`, `placeholder` and `class`. `online` and `offline` replace `status`, as daisyUI names those modifiers. `size`, `size_options`, `shape` and `variant` go: daisyUI has no avatar size or colour modifier, and Article XIV reserves `size` and `variant` for those. Width, shape and placeholder colour go through `content_class` on the image frame.
- Q: With no `size`, how big is an avatar by default? → A: The image frame gets a default of `w-12 rounded-full`, plus `bg-neutral text-neutral-content` when showing a placeholder. Giving `content_class` replaces those defaults rather than adding to them. Without a default width an avatar image renders at its natural size, which is never what a caller wants.
- Q: What does the avatar's `alt` default to? → A: Empty. An avatar almost always sits next to the person's name, where "User avatar" read aloud is noise. The documentation says to give `alt` when the avatar is the only thing identifying the person.
- Q: Which avatar group attributes survive? → A: Only `class`. `size` and `space_options` go. The group emits `avatar-group`, and the overlap (for example `-space-x-6`, as daisyUI's examples use) goes through `class`.
- Q: What are the stat's container and item called? → A: `<c-stat>` for one stat and `<c-stat.group>` for daisyUI's `stats` container, following the package's `avatar` and `avatar.group` pair. A stat is always placed in a group, even when it is alone, because daisyUI styles it inside one.
- Q: How does a status dot tell a screen-reader user what it means? → A: With `label`. Given a label, the dot is exposed as an image with that name. Without one, it is hidden from assistive technology, on the assumption that text beside it says the same thing. Colour alone never carries the meaning.
- Q: Which element of the table receives `class` and pass-through attributes? → A: The scrolling wrapper, which is the root element under Article XIV. The `<table>` takes extra classes through `content_class`. The wrapper is keyboard-focusable so a keyboard user can scroll a wide table, and it is named by the table's caption or by an `aria-label` the caller gives.
- Q: Does the table build rows and cells? → A: No. daisyUI has no row or cell classes, and components take plain values rather than data structures. The caller writes `<thead>`, `<tbody>`, rows and cells in the default slot. The gallery shows header cells with `scope`.
- Q: Where does `timeline-box` go on a timeline item? → A: On the `end` part when `box` is given, matching daisyUI's examples where the date sits at the start and the event in a box at the end. `box="start"` puts it on the start part instead, for alternating layouts.
- Q: How are responsive direction changes written, such as a stat group that stacks on small screens? → A: The way the menu does it in the navigation components: `vertical` or `horizontal` as a boolean applies the class, and a breakpoint value such as `horizontal="lg"` applies it from that breakpoint. The card's `side` works the same way.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Card (Priority: P1)

A developer groups content into cards on dashboards, list pages and detail pages: a title, some content, perhaps an image, and buttons at the foot, in any of daisyUI's sizes and styles.

**Why this priority**: The card is the most used container in an application. Its attribute and slot changes are breaking, and other components and projects compose into it, so it lands first.

**Independent Test**: Render `<c-card>` with each attribute and slot and check the emitted classes and structure. Open the card's gallery entry and see every size, style and layout.

**Acceptance Scenarios**:

1. **Given** `<c-card title="Plan">Body</c-card>`, **When** it renders, **Then** the root carries `card`, the body sits in `card-body`, and "Plan" is a heading carrying `card-title`.
2. **Given** a `title` slot holding an icon and a badge, **When** it renders, **Then** the slot content fills the `card-title` heading.
3. **Given** an `actions` slot, **When** it renders, **Then** its content sits in `card-actions` at the foot of the body.
4. **Given** a `figure` slot, **When** it renders, **Then** its content sits in a `<figure>` before the body.
5. **Given** `size="sm"`, **When** it renders, **Then** the root carries `card-sm`, and each of `xs`–`xl` maps to its daisyUI class.
6. **Given** `border`, `dash`, `side` or `image-full`, **When** it renders, **Then** the root carries `card-border`, `card-dash`, `card-side` or `image-full`. Given `side="sm"`, it carries `sm:card-side` instead.
7. **Given** `class="bg-base-100 shadow-sm w-96"` and `content_class="gap-4"`, **When** it renders, **Then** the root's single class list holds `card` and the caller's classes, and the body's holds `card-body` and `gap-4`.
8. **Given** a card with no title, figure or actions, **When** it renders, **Then** it emits only the root and the body, with no empty heading or actions row.
9. **Given** the card's gallery entry, **When** a developer opens it, **Then** every size, both styles, the side and image-full layouts, a card with a figure and a card with actions are shown.

---

### User Story 2 - Table (Priority: P1)

A developer shows tabular data in daisyUI's table styles. The table is named for assistive technology, scrolls sideways on narrow screens, and a keyboard user can scroll it.

**Why this priority**: Tables carry the list pages and reports that most applications are built around.

**Independent Test**: Render `<c-table>` with a caption and a few rows, check the classes and structure, then narrow the browser and scroll the table with the keyboard.

**Acceptance Scenarios**:

1. **Given** `<c-table caption="Invoices">` with a header row and body rows in its slot, **When** it renders, **Then** a wrapper carrying `overflow-x-auto` holds a `<table>` carrying `table`, the caption renders as the table's `<caption>`, and the slot content follows it inside the table.
2. **Given** a caption, **When** the table renders, **Then** the wrapper is focusable by keyboard, is exposed as a region, and takes its name from the caption.
3. **Given** no caption and `aria-label="Invoices"`, **When** it renders, **Then** the wrapper carries that label.
4. **Given** `zebra`, `pin-rows` or `pin-cols`, **When** it renders, **Then** the table carries `table-zebra`, `table-pin-rows` or `table-pin-cols`.
5. **Given** `size="xs"`, **When** it renders, **Then** the table carries `table-xs`, and each of `xs`–`xl` maps to its daisyUI class.
6. **Given** `class="mt-4"` and `content_class="w-full"`, **When** it renders, **Then** `mt-4` joins the wrapper's class list and `w-full` joins the table's.
7. **Given** a `caption` slot instead of the attribute, **When** it renders, **Then** the slot content fills the `<caption>`.
8. **Given** the table's gallery entry, **When** a developer opens it, **Then** every size, zebra rows, pinned rows and pinned columns are shown, and every example uses header cells with `scope`.

---

### User Story 3 - Badge (Priority: P1)

A developer marks an item with a short label, such as a status, a count or a tag, in any colour, size and style daisyUI offers, inside text or inside a button.

**Why this priority**: Badges appear across nearly every list and detail page, and the existing badge's attributes change.

**Independent Test**: Render `<c-badge>` with each attribute, check the emitted element and classes, and open its gallery entry.

**Acceptance Scenarios**:

1. **Given** `<c-badge variant="success" size="sm" soft>Paid</c-badge>`, **When** it renders, **Then** it is a `<span>` carrying `badge`, `badge-success`, `badge-sm` and `badge-soft`, with "Paid" as its content.
2. **Given** `text="New"`, **When** it renders, **Then** "New" is the badge's content.
3. **Given** `outline`, `dash`, `soft` or `ghost`, **When** it renders, **Then** the badge carries `badge-outline`, `badge-dash`, `badge-soft` or `badge-ghost`.
4. **Given** a badge inside a `<c-button>`, **When** it renders, **Then** the result is valid HTML, with no block element inside the button.
5. **Given** `class="ms-2"` and `data-test="x"`, **When** it renders, **Then** `ms-2` is in the badge's single class list and `data-test="x"` is on the badge.
6. **Given** the badge's gallery entry, **When** a developer opens it, **Then** every colour, size and style is shown, as well as an empty badge and a badge inside a button.

---

### User Story 4 - Collapse and accordion (Priority: P2)

A developer hides detail behind a heading the user can expand, either alone (a collapse) or in a group where opening one item closes the others (an accordion), such as an FAQ. Keyboard and screen-reader users can expand and collapse every item, with no script.

**Why this priority**: Common on settings, help and detail pages, and expected in any component library, but fewer pages need it than the components above.

**Independent Test**: Render a collapse and a three-item accordion, operate both by keyboard and pointer in a browser, and check the expanded state is reported and only one accordion item is open at a time.

**Acceptance Scenarios**:

1. **Given** `<c-collapse title="Details">Content</c-collapse>`, **When** it renders, **Then** it is daisyUI's collapse built on `<details>`: a root carrying `collapse`, a `<summary>` carrying `collapse-title` holding "Details", and the content in `collapse-content`.
2. **Given** a rendered collapse, **When** a keyboard user tabs to its title and presses Enter or Space, **Then** it expands, a visible focus indicator shows, and it is announced as expanded. Pressing again collapses it.
3. **Given** `open`, **When** the page loads, **Then** the collapse is expanded, and the user can still collapse it.
4. **Given** `arrow` or `plus`, **When** it renders, **Then** the root carries `collapse-arrow` or `collapse-plus`.
5. **Given** a `title` slot, **When** it renders, **Then** the slot content fills the summary.
6. **Given** three `<c-accordion name="faq">` items, **When** the user opens one and then another, **Then** the first closes, so at most one is open.
7. **Given** two accordion groups with different names on one page, **When** the user opens an item in one, **Then** the other group is unaffected.
8. **Given** `<c-accordion>`, **When** it renders, **Then** it is drawn by `<c-collapse>` and accepts every collapse attribute and slot.
9. **Given** the gallery entries, **When** a developer opens them, **Then** the collapse shows the plain, arrow and plus styles and an item open by default, and the accordion shows a working group of items, with and without a bordered surface.

---

### User Story 5 - Avatar and avatar group (Priority: P2)

A developer shows a person's photo, their initials when there is no photo, or a neutral silhouette when there is neither, with an online or offline indicator, alone or overlapped in a group.

**Why this priority**: Avatars appear on most application pages, but usually once, in the frame around the content. The existing attributes change and adopters need the new shape.

**Independent Test**: Render `<c-avatar>` with a photo, with initials and with nothing, and a group of three. Check the classes and the accessible output.

**Acceptance Scenarios**:

1. **Given** `<c-avatar src="/p.jpg" alt="Ada Lovelace">`, **When** it renders, **Then** it is daisyUI's avatar markup: a root carrying `avatar`, an image frame, and an `<img>` with that source and alt text.
2. **Given** `src` and no `alt`, **When** it renders, **Then** the image has an empty `alt`.
3. **Given** `placeholder="AL"` and no `src`, **When** it renders, **Then** the root carries `avatar-placeholder` and the frame shows "AL".
4. **Given** neither `src` nor `placeholder`, **When** it renders, **Then** the frame shows a silhouette that is hidden from assistive technology.
5. **Given** `online` or `offline`, **When** it renders, **Then** the root carries `avatar-online` or `avatar-offline`.
6. **Given** no `content_class`, **When** it renders, **Then** the frame carries `w-12 rounded-full`, plus `bg-neutral text-neutral-content` when showing a placeholder. **Given** `content_class="w-24 rounded-xl"`, **Then** the frame carries those classes instead of the defaults.
7. **Given** `<c-avatar.group class="-space-x-6">` holding three avatars, **When** it renders, **Then** the root carries `avatar-group` and `-space-x-6` in one class list, with the avatars inside.
8. **Given** the gallery entries, **When** a developer opens them, **Then** photo, placeholder and silhouette avatars, both indicators, several widths and shapes, and an overlapping group are shown.

---

### User Story 6 - Stat (Priority: P2)

A developer shows key figures on a dashboard, each with a title, a value, a description, an optional figure such as an icon, and optional actions, laid out in a row that stacks on small screens.

**Why this priority**: Most dashboards open with a row of figures, but fewer pages need them than cards or tables.

**Independent Test**: Render a `<c-stat.group>` holding three `<c-stat>` items and check the classes, the order the text is read in, and the responsive layout.

**Acceptance Scenarios**:

1. **Given** `<c-stat title="Downloads" value="31K" desc="Jan 1st – Feb 1st">`, **When** it renders, **Then** it carries `stat`, and the three texts sit in `stat-title`, `stat-value` and `stat-desc`, read in that order.
2. **Given** `title`, `value` or `desc` slots, **When** it renders, **Then** the slot content fills the matching part.
3. **Given** a `figure` slot, **When** it renders, **Then** the content sits in `stat-figure`.
4. **Given** an `actions` slot, **When** it renders, **Then** the content sits in `stat-actions`.
5. **Given** a stat with no description, figure or actions, **When** it renders, **Then** no empty part is emitted.
6. **Given** `<c-stat.group>` holding stats, **When** it renders, **Then** the root carries `stats` with the stats inside.
7. **Given** `vertical` or `horizontal`, **When** the group renders, **Then** it carries `stats-vertical` or `stats-horizontal`. **Given** `vertical horizontal="lg"`, it carries `stats-vertical` and `lg:stats-horizontal`.
8. **Given** the gallery entries, **When** a developer opens them, **Then** stats with figures, with actions and with descriptions are shown in horizontal, vertical and responsive groups.

---

### User Story 7 - List (Priority: P2)

A developer shows a vertical list of rows, such as people, files or songs, each row holding an image, the main text and actions, with the main text filling the remaining width.

**Why this priority**: Lists of this shape carry many mobile and settings pages. They are simple and have no attributes to learn beyond the rows.

**Independent Test**: Render `<c-list>` with three `<c-list.row>` items and check the list semantics and classes.

**Acceptance Scenarios**:

1. **Given** `<c-list>` holding `<c-list.row>` items, **When** it renders, **Then** it is a `<ul>` carrying `list`, and each row is an `<li>` carrying `list-row`.
2. **Given** `class` and other attributes on the list or a row, **When** it renders, **Then** the classes join that element's single class list and the attributes land on it.
3. **Given** the list's documentation, **When** a developer wants a column other than the second to fill the row, or a column to wrap onto its own line, **Then** it shows `list-col-grow` and `list-col-wrap` on the row's children.
4. **Given** the gallery entries, **When** a developer opens them, **Then** a list with images, text and icon-only actions (each with an accessible name) is shown, along with the grow and wrap examples.

---

### User Story 8 - Timeline (Priority: P3)

A developer shows events in order, vertically or horizontally, each with a date or label, an icon on the line, and a description, optionally in a box.

**Why this priority**: Used for history, audit and progress pages, which fewer applications have.

**Independent Test**: Render a `<c-timeline>` with three `<c-timeline.item>` entries, check the structure and classes, and confirm the connector line runs only between events.

**Acceptance Scenarios**:

1. **Given** `<c-timeline>` holding items, **When** it renders, **Then** it is a `<ul>` carrying `timeline`, and each item is an `<li>`.
2. **Given** `<c-timeline.item start="1984" end="First Macintosh">` with a `middle` slot, **When** it renders, **Then** the texts sit in `timeline-start` and `timeline-end` and the slot content in `timeline-middle`.
3. **Given** `start`, `end` or `middle` left out, **When** the item renders, **Then** that part is not emitted.
4. **Given** `box`, **When** the item renders, **Then** the end part carries `timeline-box`. **Given** `box="start"`, the start part carries it instead.
5. **Given** `vertical`, `horizontal`, `compact` or `snap-icon`, **When** the timeline renders, **Then** it carries `timeline-vertical`, `timeline-horizontal`, `timeline-compact` or `timeline-snap-icon`, and `horizontal="md"` gives `md:timeline-horizontal`.
6. **Given** three items, **When** they render, **Then** a connector line joins consecutive events and does not extend past the first or the last, and the connectors are hidden from assistive technology.
7. **Given** the gallery entries, **When** a developer opens them, **Then** vertical, horizontal, responsive, compact, snap-icon and boxed timelines are shown.

---

### User Story 9 - Kbd and status (Priority: P3)

A developer shows a keyboard shortcut, such as Ctrl + K, in key-cap style, and marks something as online, busy or failing with a small coloured dot that screen-reader users can also understand.

**Why this priority**: Small, occasional elements. Few pages need either, and both are simple.

**Independent Test**: Render `<c-kbd>` and `<c-status>` with each attribute and check the element, classes and accessible output.

**Acceptance Scenarios**:

1. **Given** `<c-kbd size="sm">K</c-kbd>`, **When** it renders, **Then** it is a `<kbd>` carrying `kbd` and `kbd-sm`, and each of `xs`–`xl` maps to its daisyUI class.
2. **Given** `<c-kbd text="Ctrl">`, **When** it renders, **Then** "Ctrl" is its content.
3. **Given** `<c-status variant="success" size="lg" label="Online">`, **When** it renders, **Then** it is a `<span>` carrying `status`, `status-success` and `status-lg`, exposed to assistive technology as an image named "Online".
4. **Given** a status with no `label`, **When** it renders, **Then** it is hidden from assistive technology.
5. **Given** the gallery entries, **When** a developer opens them, **Then** every kbd size and a key combination are shown, and every status colour and size is shown, both labelled and beside visible text.

---

### Edge Cases

- A `variant` or `size` value daisyUI does not define emits no class for that attribute and raises no error. A breakpoint value outside Tailwind's breakpoints emits no class.
- A card whose title is only an icon has no text heading. The documentation says to give the icon an accessible name or add visible text.
- A card with a figure but no image alt text is the caller's omission. Every gallery example gives alt text.
- An accordion item given no `name` is not part of a group. `name` is marked required, and the documentation says why.
- In a browser that does not support grouped `<details>`, accordion items still open and close, but more than one can be open at a time. The documentation says so.
- If two items in one accordion group are both given `open`, the browser decides which stays open. The documentation says to open at most one.
- A collapse's content is still in the page while collapsed. It is hidden from view and from assistive technology until expanded.
- A table with neither a caption nor an `aria-label` has an unnamed scrolling region. The documentation says to give one or the other.
- A table's wrapper is a keyboard stop even when the table fits. That is the cost of letting keyboard users scroll a table that does not fit.
- `pin-rows` has no effect without a `<thead>`, and `pin-cols` without row header cells. The documentation says so.
- An avatar group's overlap class is Tailwind's, so it needs the project's Tailwind build to see it, like any class a caller writes.
- A status given `label` next to visible text saying the same thing is read twice. The documentation says to leave `label` off when text is beside it.
- A stat value given as a number reaches the template as a number and renders as text. Formatting it is the caller's job.
- An icon-only action in a card, stat or list row has no accessible name unless the caller gives one. Every gallery example does.
- The modal draws its box with `<c-card>` until issue #14 lands. If this feature lands first, the modal keeps rendering its title, body and actions as before.

## Requirements *(mandatory)*

### Functional Requirements

**Every component in the group**

- **FR-001**: Accordion, avatar, avatar group, badge, card, collapse, kbd, list, list row, stat, stat group, status, table, timeline and timeline item MUST each exist as a Cotton component (`<c-accordion>`, `<c-avatar>`, `<c-avatar.group>`, `<c-badge>`, `<c-card>`, `<c-collapse>`, `<c-kbd>`, `<c-list>`, `<c-list.row>`, `<c-stat>`, `<c-stat.group>`, `<c-status>`, `<c-table>`, `<c-timeline>`, `<c-timeline.item>`) emitting the markup and classes daisyUI documents. *(US1–US9)*
- **FR-002**: Each MUST follow Article XIV: `variant` for colour where daisyUI has a colour modifier, `size` on daisyUI's `xs`–`xl` scale where daisyUI has a size modifier, daisyUI's modifier names as boolean attributes, `class` merged into the root element's class list, and every other attribute passed through to the root element unless this spec names another element for it. *(US1–US9)*
- **FR-003**: A direction or layout modifier that daisyUI shows with a responsive prefix (`side`, `vertical`, `horizontal`) MUST accept either a boolean, which applies the class, or a breakpoint (`sm`, `md`, `lg`, `xl`, `2xl`), which applies it from that breakpoint. *(US1, US6, US8)*
- **FR-004**: Each MUST carry the gallery annotations Article XVI requires, and `cotton_lint --warnings-as-errors` MUST pass. *(US1–US9)*
- **FR-005**: Each MUST have a gallery entry that renders its variants and states, so a developer can choose attributes without reading the template. *(US1–US9)*
- **FR-006**: Each MUST emit accessible markup by default: correct elements, roles and states, keyboard reach for anything interactive, and a visible focus indicator. Icons and decorations that carry no meaning MUST be hidden from assistive technology. *(US1–US9)*
- **FR-007**: A part that the caller leaves empty (an attribute not given and its slot not filled) MUST NOT be emitted. *(US1, US6, US8)*
- **FR-008**: Every removed or renamed attribute or slot on the card, badge, avatar and avatar group MUST be listed in the CHANGELOG with its replacement, and the README MUST list the components as they now are. *(US1, US3, US5)*

**Card**

- **FR-009**: `<c-card>` MUST render daisyUI's card: a root with `card`, an optional `<figure>` from a `figure` slot before the body, and a body with `card-body` holding the default slot. *(US1)*
- **FR-010**: `title`, as an attribute or a named slot, MUST render a heading with `card-title` at the top of the body. An `actions` slot MUST render in `card-actions` at the foot of the body. *(US1)*
- **FR-011**: `<c-card>` MUST accept `size` (xs–xl) and the booleans `border`, `dash`, `side` and `image-full`, each mapping to its daisyUI class, with `side` also accepting a breakpoint. *(US1)*
- **FR-012**: The body MUST accept extra classes through `content_class`, replacing `body_class`. `icon`, `tight`, `badges`, `footer`, `footer_end` and the built-in `bg-base-100 shadow-sm` surface MUST be removed. *(US1)*

**Table**

- **FR-013**: `<c-table>` MUST render a root wrapper with `overflow-x-auto` holding a `<table>` with `table`, the default slot as the table's content, and a `<caption>` from `caption`, given as an attribute or a named slot. *(US2)*
- **FR-014**: The wrapper MUST be keyboard-focusable and exposed as a region, named by the caption when there is one. It MUST receive `class` and pass-through attributes. The `<table>` MUST accept extra classes through `content_class`. *(US2)*
- **FR-015**: `<c-table>` MUST accept `size` (xs–xl) and the booleans `zebra`, `pin-rows` and `pin-cols`, each mapping to its daisyUI class on the `<table>`. *(US2)*

**Badge**

- **FR-016**: `<c-badge>` MUST render a `<span>` with `badge`, holding `text` followed by the default slot. *(US3)*
- **FR-017**: `<c-badge>` MUST accept `variant` (neutral, primary, secondary, accent, info, success, warning, error), `size` (xs–xl, replacing the previous `sm` and `lg` only) and the style booleans `outline`, `dash`, `soft` and `ghost`, each mapping to its daisyUI class. *(US3)*

**Collapse and accordion**

- **FR-018**: `<c-collapse>` MUST render daisyUI's collapse on `<details>`: a root with `collapse`, a `<summary>` with `collapse-title` holding `title` (attribute or named slot), and the default slot in `collapse-content`. It MUST open and close by pointer and keyboard and report its expanded state, without script. *(US4)*
- **FR-019**: `arrow` and `plus` MUST map to `collapse-arrow` and `collapse-plus`. `open` MUST render the collapse initially expanded without preventing the user from collapsing it. *(US4)*
- **FR-020**: `<c-accordion>` MUST be drawn by `<c-collapse>` (Article XV), accept every attribute and slot the collapse does, and require `name`. Items sharing a `name` MUST form one group in which opening an item closes the others, without script. *(US4)*

**Avatar and avatar group**

- **FR-021**: `<c-avatar>` MUST render daisyUI's avatar: a root with `avatar` and an image frame holding an `<img>` when `src` is given, the `placeholder` text with `avatar-placeholder` on the root when it is not, or a silhouette hidden from assistive technology when neither is given. *(US5)*
- **FR-022**: `alt` MUST default to empty. `online` and `offline` MUST map to `avatar-online` and `avatar-offline`, replacing `status`. *(US5)*
- **FR-023**: The image frame MUST default to `w-12 rounded-full`, plus `bg-neutral text-neutral-content` when showing a placeholder. `content_class` MUST replace those defaults. `size`, `size_options`, `shape` and `variant` MUST be removed. *(US5)*
- **FR-024**: `<c-avatar.group>` MUST render a root with `avatar-group` holding the default slot. `size` and `space_options` MUST be removed. *(US5)*

**Stat**

- **FR-025**: `<c-stat>` MUST render an element with `stat`, holding `title`, `value` and `desc` (each an attribute or a named slot) in `stat-title`, `stat-value` and `stat-desc`, in that order, a `figure` slot in `stat-figure`, and an `actions` slot in `stat-actions`. *(US6)*
- **FR-026**: `<c-stat.group>` MUST render a root with `stats` holding the default slot, and accept `vertical` and `horizontal` mapping to `stats-vertical` and `stats-horizontal`, each also accepting a breakpoint. *(US6)*

**List**

- **FR-027**: `<c-list>` MUST render a `<ul>` with `list` holding the default slot. `<c-list.row>` MUST render an `<li>` with `list-row` holding the default slot. *(US7)*
- **FR-028**: The list's documentation MUST show `list-col-grow` and `list-col-wrap` applied to a row's children. *(US7)*

**Timeline**

- **FR-029**: `<c-timeline>` MUST render a `<ul>` with `timeline` holding the default slot, and accept `vertical`, `horizontal` (each also accepting a breakpoint), `compact` and `snap-icon`, each mapping to its daisyUI class. *(US8)*
- **FR-030**: `<c-timeline.item>` MUST render an `<li>` holding `start` and `end` (each an attribute or a named slot) in `timeline-start` and `timeline-end`, and a `middle` slot in `timeline-middle`. *(US8)*
- **FR-031**: `box` MUST put `timeline-box` on the end part, and `box="start"` on the start part. *(US8)*
- **FR-032**: A connector line MUST join consecutive items without extending past the first or last item, and MUST be hidden from assistive technology. *(US8)*

**Kbd and status**

- **FR-033**: `<c-kbd>` MUST render a `<kbd>` with `kbd`, holding `text` followed by the default slot, and accept `size` (xs–xl). *(US9)*
- **FR-034**: `<c-status>` MUST render a `<span>` with `status` and accept `variant` (the eight daisyUI colours) and `size` (xs–xl). *(US9)*
- **FR-035**: Given `label`, the status MUST be exposed to assistive technology as an image named by the label. Without it, the status MUST be hidden from assistive technology. *(US9)*

### Key Entities

- **Part**: a named piece of a component's markup that daisyUI gives its own class, such as `card-title`, `stat-value` or `timeline-end`. Most parts can be filled by an attribute or a named slot of the same name.
- **Group**: a container that gives several items a shared layout or behaviour: the avatar group, the stat group, and the set of accordion items sharing a name.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every class daisyUI lists for accordion, avatar, badge, card, collapse, kbd, list, stat, status, table and timeline is reachable through a documented attribute, slot or documented example, except `collapse-open` and `collapse-close`, which lock a collapse's state.
- **SC-002**: `cotton_lint --warnings-as-errors` reports zero errors and zero warnings for all fifteen component templates in this group.
- **SC-003**: The collapse and accordion can be expanded and collapsed with the keyboard alone, and the table can be scrolled with the keyboard alone. None of the components ships a script.
- **SC-004**: Every component's gallery entry shows each of its variants and states, and every gallery example of an image, icon-only control or status dot has an accessible name or is shown beside text that gives one.
- **SC-005**: A developer upgrading from the previous card, badge, avatar or avatar group finds every removed or renamed attribute and slot, with its replacement, in the CHANGELOG.

## Assumptions

- #11 lands first, so the gallery annotations, the lint check in CI and the documentation on running the gallery already exist.
- The host project runs daisyUI 5, the version whose class reference this spec follows, and its Tailwind build scans the package's templates.
- The package is below 0.1.0, so breaking attribute changes to existing components are acceptable when the CHANGELOG lists them.
- `<c-icon>` remains the way a caller draws an icon inside these components. None of them takes an `icon` attribute of its own.
- The responsive-value convention matches the one the navigation components (issue #12) use for the menu. If that feature settles on a different form first, this group follows it.
