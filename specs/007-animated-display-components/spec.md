# Feature Specification: Animated and decorative display components

**Feature Branch**: `007-animated-display-components`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2, G3 · **Roadmap**: R5 · **Depends on**: #11 (gallery annotations and the lint check in CI)

**Input**: Issue #16, "Animated and decorative display components": the rest of daisyUI's data display group, which is mostly motion or visual effect. Each component is accessible and shown in the gallery with its variants and states.

## Scope

The issue lists eight daisyUI components. Seven get a Cotton component. None exists today, so every one is new.

| Component | daisyUI class | Cotton component |
|---|---|---|
| Carousel | `carousel` | `<c-carousel>` and `<c-carousel.item>` |
| Chat bubble | `chat` | `<c-chat>` |
| Countdown | `countdown` | `<c-countdown>` |
| Diff | `diff` | `<c-diff>` |
| Hover 3D card | `hover-3d` | `<c-hover-3d>` |
| Hover gallery | `hover-gallery` | `<c-hover-gallery>` |
| Text rotate | `text-rotate` | `<c-text-rotate>` |

**Aura is excluded.** daisyUI uses it only to put a light effect around the border of one other element, such as a button or a card, placed inside it. It decorates another component rather than being one, so it gets no Cotton component of its own (README, *Scope & philosophy*). A project wraps the component it wants to highlight in a `<div class="aura">`. The README records the exclusion and its reason (FR-006).

Out of scope: any JavaScript. The countdown's number changes only when a script changes it, and the carousel's previous and next controls are links a project writes. In both cases the component emits the markup daisyUI documents, and the project supplies any script.

## Clarifications

### Session 2026-09-26

- Q: How are carousel slides written? → A: As `<c-carousel.item>` children of `<c-carousel>`, the same parent and child pattern `dock` and `breadcrumbs` use. daisyUI needs `carousel-item` on each slide, and a child component puts it there so the caller never writes the class by hand.
- Q: What are the carousel's alignment and direction attributes called? → A: Alignment is `snap`, taking `start`, `center` or `end`. daisyUI gives the class group no category name and describes it as where the items snap to. Direction follows the ruling the layout components use: two boolean attributes named as daisyUI names the modifiers, `horizontal` and `vertical`.
- Q: Does the carousel emit previous, next or indicator controls? → A: No. daisyUI builds them as ordinary links to each slide's `id`, outside the carousel's own markup. A slide accepts an `id`, and the carousel's gallery entry shows both of daisyUI's control patterns built with `<c-button href="#…">`. The component stays at daisyUI's markup, and a project that wants scripted controls is not stuck with link-based ones.
- Q: How does a keyboard user move through a carousel with no controls? → A: The carousel is a scrollable region, so it is focusable and named. Once focused, the arrow keys scroll it. It carries `role="region"`, `tabindex="0"` and a translatable `aria-roledescription` of "carousel", and takes its name from `aria-label`. Each slide is a group with the roledescription "slide".
- Q: What does the chat bubble take as attributes and what as slots? → A: `placement` (`start` or `end`, daisyUI's own name for the class group, defaulting to `start` because daisyUI requires one) and `variant` for the bubble colour. The message is the default slot. `image`, `header` and `footer` are named slots rendered in `chat-image`, `chat-header` and `chat-footer`. An avatar goes in the `image` slot as `<c-avatar>`, so the chat bubble does not copy the avatar's attributes.
- Q: Where do the countdown's accessibility attributes go? → A: On the inner number element, as daisyUI's markup shows: `aria-live="polite"` and an `aria-label` carrying the same number as the text. Other attributes land on the root element as usual.
- Q: What does the countdown do with a value outside 0–999 or a value that is not a number? → A: It renders the value as given and raises no error. daisyUI animates only 0 through 999, and the documentation says so. Autoescaping keeps any value from breaking out of the `style` attribute.
- Q: What are the diff's slots called? → A: `item_1` and `item_2`, daisyUI's part names with the underscore the other components use where daisyUI has a hyphen (`main_action` for `fab-main-action`). The component emits the resizer handle itself.
- Q: How are the hover gallery's images and the text rotate's lines passed in? → A: As the default slot. The caller writes the `<img>` elements, each with its own `alt`, or the line elements, each with its own classes. A list attribute would have to reinvent `alt`, sizes and per-line styling as attributes.
- Q: What does the hover 3D card emit around its content? → A: The default slot as its first child, followed by the eight empty hover zones daisyUI requires. The zones are hidden from assistive technology. `href` makes the root an `<a>`, which is daisyUI's way to make the whole card a link.
- Q: The hover effects, the text rotation and the diff resizer are pointer-driven. How do they meet the accessibility bar? → A: No content is hidden from assistive technology. Every hover gallery image, every text rotate line and both diff items stay in the accessibility tree, and only the visual effect needs a pointer. Reduced-motion handling and pausing belong to daisyUI's CSS, which this package does not ship. Each component's documentation states what a keyboard or screen-reader user gets, and what daisyUI's CSS does not provide.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Carousel (Priority: P1)

A developer needs a row or column of images or cards that scrolls and snaps one item at a time, and that keyboard and screen-reader users can reach and move through.

**Why this priority**: Carousels appear on product pages, landing pages and dashboards in most kinds of project. More adopters need this than any other component in the group.

**Independent Test**: Render `<c-carousel aria-label="Photos">` with three `<c-carousel.item>` children, focus it by keyboard in a browser, scroll it with the arrow keys, and check its classes and roles.

**Acceptance Scenarios**:

1. **Given** `<c-carousel aria-label="Photos">` with three `<c-carousel.item>` children, **When** it renders, **Then** the root carries `carousel`, `role="region"`, `tabindex="0"`, the translatable roledescription "carousel" and the name "Photos", and each child carries `carousel-item`, `role="group"` and the roledescription "slide".
2. **Given** `snap="center"`, **When** it renders, **Then** the root carries `carousel-center`, and `start` and `end` map to `carousel-start` and `carousel-end`.
3. **Given** `vertical`, **When** it renders, **Then** the root carries `carousel-vertical`, and `horizontal` gives `carousel-horizontal`.
4. **Given** a rendered carousel in a browser, **When** a keyboard user tabs to it, **Then** it shows a visible focus indicator and the arrow keys scroll it.
5. **Given** `<c-carousel.item id="slide2" class="w-full">`, **When** it renders, **Then** the id and the class land on the slide, so a link to `#slide2` scrolls to it.
6. **Given** the carousel's gallery entry, **When** a developer opens it, **Then** each snap alignment, the vertical direction, full-width slides, and daisyUI's indicator and previous/next link patterns built with `<c-button>` are shown, and every image carries alt text.

---

### User Story 2 - Chat bubble (Priority: P2)

A developer building a messaging, support or comment view needs a bubble for each message, placed on either side, with an optional avatar, author, time and delivery status.

**Why this priority**: Any project with messaging or an assistant view needs it, but that is a subset of projects.

**Independent Test**: Render `<c-chat>` with a message, an avatar in the `image` slot, a header and a footer, on each side and in each colour, and check the classes and structure.

**Acceptance Scenarios**:

1. **Given** `<c-chat>Hello</c-chat>`, **When** it renders, **Then** it is daisyUI's chat markup: a root with `chat` and `chat-start`, and "Hello" in an element with `chat-bubble`.
2. **Given** `placement="end"`, **When** it renders, **Then** the root carries `chat-end` in place of `chat-start`.
3. **Given** `variant="primary"`, **When** it renders, **Then** the bubble carries `chat-bubble-primary`, and each of neutral, primary, secondary, accent, info, success, warning and error maps to its daisyUI class.
4. **Given** `image`, `header` and `footer` slots, **When** it renders, **Then** their content sits in `chat-image`, `chat-header` and `chat-footer`, and a slot that is not given emits no element.
5. **Given** `<c-avatar>` in the `image` slot, **When** it renders, **Then** the avatar is drawn by `<c-avatar>` inside `chat-image`.
6. **Given** `class="mt-2" data-id="7"`, **When** it renders, **Then** both land on the root element.
7. **Given** the chat bubble's gallery entry, **When** a developer opens it, **Then** both placements, every colour, and a two-sided conversation with avatars, author names, times and a delivery status are shown.

---

### User Story 3 - Countdown (Priority: P2)

A developer needs a number that animates when it changes, for timers, clocks and counters, and that a screen reader announces when a script updates it.

**Why this priority**: Timers and countdown clocks are common on event, sale and quiz pages.

**Independent Test**: Render `<c-countdown value="42">` and check the markup, then change the value from a script in a browser and check that the number transitions and is announced.

**Acceptance Scenarios**:

1. **Given** `<c-countdown value="42">`, **When** it renders, **Then** it is a `<span>` with `countdown` wrapping an inner `<span>` whose `style` sets `--value:42;`, whose text is `42`, and which carries `aria-live="polite"` and `aria-label="42"`.
2. **Given** a rendered countdown in a browser, **When** a script sets a new number on the inner element's `--value`, text and `aria-label`, **Then** daisyUI's transition plays and a screen reader announces the new number.
3. **Given** `value="1000"` or `value="abc"`, **When** it renders, **Then** the value is rendered as given with no error, and the documentation states that daisyUI animates only 0 through 999.
4. **Given** `class="font-mono text-4xl"`, **When** it renders, **Then** those classes land on the root element.
5. **Given** the countdown's documentation, **When** a developer wants a live timer, **Then** it names the three things a script must update together: the `--value` variable, the text and the `aria-label`.
6. **Given** the countdown's gallery entry, **When** a developer opens it, **Then** single values and a days, hours, minutes and seconds clock built from several labelled countdowns are shown.

---

### User Story 4 - Diff (Priority: P3)

A developer needs to compare two images or two blocks of content side by side, with a handle the user drags to reveal more of either.

**Why this priority**: A before-and-after comparison is useful for image editing, design and product pages, but few applications need one.

**Independent Test**: Render `<c-diff>` with `item_1` and `item_2` slots and check the structure, then drag the resizer in a browser and check both items stay readable to assistive technology.

**Acceptance Scenarios**:

1. **Given** `<c-diff aria-label="Before and after">` with `item_1` and `item_2` slots, **When** it renders, **Then** it is a `<figure>` with `diff` containing `diff-item-1`, `diff-item-2` and an empty `diff-resizer`, in that order, with each slot's content in its item.
2. **Given** `class="aspect-16/9"`, **When** it renders, **Then** the class lands on the figure, which is how daisyUI keeps the aspect ratio.
3. **Given** a rendered diff, **When** a screen reader reads it, **Then** it announces the figure's name and the content of both items.
4. **Given** the diff's documentation, **When** a developer reads it, **Then** it states that dragging the resizer needs a pointer, which is a limit of daisyUI's method.
5. **Given** the diff's gallery entry, **When** a developer opens it, **Then** an image comparison with alt text on both images and a text comparison are shown.

---

### User Story 5 - Hover gallery (Priority: P3)

A developer building a product card or portfolio needs a picture that shows its other images as the pointer moves across it, with every image still available to screen-reader users.

**Why this priority**: A common pattern in shops and portfolios, rare in other applications.

**Independent Test**: Render `<c-hover-gallery>` with four `<img>` elements, move the pointer across it in a browser, and check the images change and all four are in the accessibility tree.

**Acceptance Scenarios**:

1. **Given** `<c-hover-gallery class="max-w-60">` with four `<img>` elements, **When** it renders, **Then** it is a `<figure>` with `hover-gallery` and `max-w-60` holding the four images in order.
2. **Given** a rendered hover gallery in a browser, **When** the pointer moves across it horizontally, **Then** the images appear in turn, and when the pointer leaves, the first image shows.
3. **Given** a rendered hover gallery, **When** a screen reader reads it, **Then** every image with alt text is announced.
4. **Given** the hover gallery's documentation, **When** a developer reads it, **Then** it states daisyUI's rules: at most ten images, all the same size, and a maximum width on the gallery.
5. **Given** the hover gallery's gallery entry, **When** a developer opens it, **Then** a gallery inside a card and a stand-alone gallery are shown, with alt text on every image.

---

### User Story 6 - Hover 3D card (Priority: P3)

A developer wants a card or image that tilts toward the pointer, optionally as a link, without changing how the content reads to assistive technology.

**Why this priority**: A decorative effect for landing and marketing pages. Few application screens use it.

**Independent Test**: Render `<c-hover-3d>` with an image in its slot, with and without `href`, move the pointer over it in a browser, and check the structure and the accessibility tree.

**Acceptance Scenarios**:

1. **Given** `<c-hover-3d>` with a `<figure>` in its slot, **When** it renders, **Then** it is a `<div>` with `hover-3d` whose first child is the slot content and whose next eight children are empty `<div>` elements.
2. **Given** the eight hover zones, **When** the accessibility tree is read, **Then** each zone is hidden from assistive technology and only the slot content is exposed.
3. **Given** `href="/cards/1"`, **When** it renders, **Then** the root is an `<a>` with that `href` and the `hover-3d` class, and the documentation says the link takes its name from the content's text or image alt, or from `aria-label`.
4. **Given** a rendered hover 3D card in a browser, **When** the pointer moves over it, **Then** the content tilts toward the pointer.
5. **Given** the hover 3D card's documentation, **When** a developer reads it, **Then** it states daisyUI's rule that the content holds no buttons, links or inputs.
6. **Given** the hover 3D card's gallery entry, **When** a developer opens it, **Then** an image, a `<c-card>` and a linked card are shown.

---

### User Story 7 - Text rotate (Priority: P3)

A developer writing a headline wants one word or phrase in it to cycle through up to six alternatives, while a screen reader still reads every alternative.

**Why this priority**: Used on landing pages and hero headlines, almost never on application screens.

**Independent Test**: Render `<c-text-rotate>` with three line elements, inline in a sentence and as a large centred heading, watch it cycle in a browser, and check the accessibility tree.

**Acceptance Scenarios**:

1. **Given** `<c-text-rotate>` with three `<span>` lines in its slot, **When** it renders, **Then** it is a `<span>` with `text-rotate` wrapping one inner `<span>` that holds the three lines in order.
2. **Given** a rendered text rotate in a browser, **When** it is on screen, **Then** the lines show one at a time in a loop, and the loop pauses while the pointer is over it.
3. **Given** a rendered text rotate, **When** a screen reader reads it, **Then** every line is read in order.
4. **Given** `class="text-7xl"` and `inner_class="justify-items-center"`, **When** it renders, **Then** the first lands on the root and the second on the inner element, which is how daisyUI centres the lines.
5. **Given** the text rotate's documentation, **When** a developer reads it, **Then** it states daisyUI's limit of six lines, how to change the ten-second loop with a duration class, and that the rotation cannot be paused without a pointer, so rotating text should never be the only place information appears.
6. **Given** the text rotate's gallery entry, **When** a developer opens it, **Then** a rotating word inside a sentence, lines coloured from the semantic palette, and a large centred heading are shown.

---

### Edge Cases

- A `variant`, `placement` or `snap` value daisyUI does not define emits no class for that attribute and raises no error.
- A carousel with no `aria-label` is an unnamed region. The component cannot invent a name, so the documentation and every gallery example give one.
- A carousel with a single slide still renders as a focusable, named region.
- Following a link to a slide's `id` also scrolls the page so the carousel is in view. This comes from daisyUI's link-based controls, and the gallery entry notes it.
- A chat bubble with every named slot empty renders only the root and the bubble.
- A chat bubble's side is visual only. The documentation says to name the speaker in the `header` slot, so a screen-reader user can tell who said what.
- A countdown's `aria-live` announces every change, so a seconds counter speaks once a second. That is daisyUI's documented markup, and the documentation says a project can override the component for a quieter timer.
- A hover gallery given more than ten images, or images of different sizes, renders them all. daisyUI's CSS shows only the first ten, and mixed sizes misalign. The component does not count or measure images.
- A decorative image in a hover gallery or diff takes `alt=""`. The gallery entries show meaningful alt text.
- Interactive content inside a hover 3D card, or a text rotate with more than six lines, renders as given. daisyUI's rules forbid both, and the documentation says so.
- The hover 3D card's tilt and the text rotate's loop are CSS effects. Whether they respect a user's reduced-motion setting depends on daisyUI's CSS, which the project supplies.

## Requirements *(mandatory)*

### Functional Requirements

**Every component in the group**

- **FR-001**: Carousel, chat bubble, countdown, diff, hover 3D card, hover gallery and text rotate MUST each exist as a Cotton component (`<c-carousel>` with `<c-carousel.item>`, `<c-chat>`, `<c-countdown>`, `<c-diff>`, `<c-hover-3d>`, `<c-hover-gallery>`, `<c-text-rotate>`) emitting the markup and classes daisyUI documents. *(US1–US7)*
- **FR-002**: Each MUST follow Article XIV: `variant` for colour where daisyUI has colour modifiers, daisyUI's modifier names as attributes, `class` merged into the root element's class list, and every other attribute passed through to the root element unless this spec names another element for it. *(US1–US7)*
- **FR-003**: Each MUST carry the gallery annotations Article XVI requires, and `cotton_lint --warnings-as-errors` MUST pass. *(US1–US7)*
- **FR-004**: Each MUST have a gallery entry that renders its variants and states, so a developer can choose attributes without reading the template. Every image in a gallery entry MUST carry alt text, and every colour a gallery entry uses MUST come from the semantic palette (Article XIII). *(US1–US7)*
- **FR-005**: Each MUST emit accessible markup by default: correct roles and states, keyboard reach for anything focusable, and a visible focus indicator. Elements that exist only for a visual effect MUST be hidden from assistive technology, and no slot content MAY be hidden from it. *(US1–US7)*
- **FR-006**: The README MUST list the new components and record that aura has no component, and why. The CHANGELOG MUST list the seven new components. *(US1–US7)*
- **FR-007**: Where a component's visual effect needs a pointer, or depends on a script the project supplies, its documentation MUST say what a keyboard or screen-reader user gets instead. *(US1, US3, US4, US5, US6, US7)*

**Carousel**

- **FR-008**: `<c-carousel>` MUST render a root with `carousel`, `role="region"`, `tabindex="0"` and the translatable roledescription "carousel", taking its accessible name from `aria-label`, with the default slot as its content. *(US1)*
- **FR-009**: `snap` MUST map `start`, `center` and `end` to `carousel-start`, `carousel-center` and `carousel-end`. `horizontal` and `vertical` MUST map to `carousel-horizontal` and `carousel-vertical`. *(US1)*
- **FR-010**: `<c-carousel.item>` MUST render an element with `carousel-item`, `role="group"` and the translatable roledescription "slide", holding the default slot. It MUST accept `class`, `id` and other attributes on that element. *(US1)*
- **FR-011**: The carousel's gallery entry MUST show daisyUI's indicator and previous/next patterns as links to slide ids, drawn with `<c-button>` (Article XV). The components themselves MUST NOT emit controls. *(US1)*

**Chat bubble**

- **FR-012**: `<c-chat>` MUST render daisyUI's chat markup: a root with `chat` and a placement class, and the default slot in an element with `chat-bubble`. *(US2)*
- **FR-013**: `placement` MUST map `start` and `end` to `chat-start` and `chat-end`, defaulting to `start`. `variant` MUST map neutral, primary, secondary, accent, info, success, warning and error to the bubble's `chat-bubble-*` class. *(US2)*
- **FR-014**: `image`, `header` and `footer` named slots MUST render in `chat-image`, `chat-header` and `chat-footer`, and each MUST emit nothing when not given. *(US2)*
- **FR-015**: The chat bubble's documentation and gallery entry MUST show an avatar as `<c-avatar>` in the `image` slot, and the speaker named in the `header` slot. *(US2)*

**Countdown**

- **FR-016**: `<c-countdown>` MUST render a `<span>` with `countdown` wrapping an inner `<span>` whose `style` sets `--value` to `value`, whose text is `value`, and which carries `aria-live="polite"` and `aria-label` set to `value`. *(US3)*
- **FR-017**: `value` MUST be rendered as given, escaped, with no validation and no error for values outside 0–999 or values that are not numbers. *(US3)*
- **FR-018**: The countdown's documentation MUST state daisyUI's 0–999 range and name the three things a script updates together: `--value`, the text and `aria-label`. *(US3)*

**Diff**

- **FR-019**: `<c-diff>` MUST render a `<figure>` with `diff` containing, in order, `diff-item-1` holding the `item_1` slot, `diff-item-2` holding the `item_2` slot, and an empty `diff-resizer`, plus any further attributes daisyUI's documented diff markup carries. *(US4)*
- **FR-020**: Both items' content MUST stay available to assistive technology whatever the resizer's position, and the figure MUST take its accessible name from `aria-label`. *(US4)*

**Hover gallery**

- **FR-021**: `<c-hover-gallery>` MUST render a `<figure>` with `hover-gallery` holding the default slot. It MUST NOT set a width of its own. *(US5)*
- **FR-022**: The hover gallery's documentation MUST state daisyUI's rules: at most ten images, all the same size, and a maximum width set on the gallery. *(US5)*

**Hover 3D card**

- **FR-023**: `<c-hover-3d>` MUST render a root with `hover-3d` whose first child is the default slot and whose next eight children are empty `<div>` elements hidden from assistive technology. *(US6)*
- **FR-024**: The root MUST be an `<a>` when `href` is given and a `<div>` otherwise. *(US6)*
- **FR-025**: The hover 3D card's documentation MUST state daisyUI's rule that the content holds no interactive elements, and how a linked card gets its accessible name. *(US6)*

**Text rotate**

- **FR-026**: `<c-text-rotate>` MUST render a `<span>` with `text-rotate` wrapping one inner `<span>` that holds the default slot. `inner_class` MUST add classes to the inner element. *(US7)*
- **FR-027**: The text rotate's documentation MUST state daisyUI's limit of six lines, how to change the loop's duration with a class, and that the rotation pauses only under a pointer. *(US7)*

### Key Entities

- **Slide**: one item in a carousel, drawn by `<c-carousel.item>`. It can carry an `id` so a link can scroll to it.
- **Hover zone**: one of the eight empty elements the hover 3D card places over its content to track the pointer. It exists only for the effect.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every class daisyUI lists for carousel, chat, countdown, diff, hover 3D, hover gallery and text rotate is either reachable through a documented attribute or slot, or emitted by the component itself.
- **SC-002**: `cotton_lint --warnings-as-errors` reports zero errors and zero warnings for all eight new templates.
- **SC-003**: None of the seven components ships a script, and in every one a screen-reader user can reach all of the slot content.
- **SC-004**: Every gallery example of a named region, a linked card or an image carries an accessible name or alt text, and every component's gallery entry shows each of its variants and states.
- **SC-005**: A developer looking for aura finds in the README that it has no component, why, and how to apply it to another component.

## Assumptions

- #11 lands first, so the gallery annotations, the lint check in CI and the documentation on running the gallery already exist.
- The host project runs daisyUI 5, the version whose class reference this spec follows, and supplies its CSS, including how each effect responds to a reduced-motion setting.
- `<c-avatar>`, `<c-card>` and `<c-button>` are used as they stand when this feature is built. Changes to their attributes belong to their own features, and this feature's gallery entries follow those changes.
- Accessibility is judged on what these components emit. Slot content, such as image alt text and link names, is the caller's responsibility, and the gallery demonstrates accessible usage.
