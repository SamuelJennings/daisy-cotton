# Decisions: Content display components

Ambiguities in issue #15 that were resolved while writing the spec, with the reasoning behind each. The short form of every one is in `spec.md` under *Clarifications*.

## The accordion is included, as a thin layer over the collapse

The README's *Scope & philosophy* gives no component to anything daisyUI builds from other components, and daisyUI's accordion is the `collapse` classes used in a group. The maintainer ruled it in anyway, because adopters expect an accordion in any component library. To keep the cost of that exception low, `<c-accordion>` is drawn by `<c-collapse>` (Article XV) and adds only the required group `name`.

## Collapse and accordion use `<details>`, not radio inputs or focus

daisyUI documents three ways to build a collapse:

- **Focus (`tabindex="0"`).** The content shows while the element has focus. Nothing reports whether it is open, and it closes as soon as focus moves, so a user cannot tab into the content they just expanded.
- **Checkbox or radio input.** A checkbox is announced as a checkbox, not as a disclosure. daisyUI's accordion uses radios, which are announced as radio buttons, and an open radio item cannot be closed again.
- **`<details>` and `<summary>`.** The browser handles Enter and Space, announces the item as expanded or collapsed, and keeps it open while the user moves through its content.

Only `<details>` meets G3 without script. Browsers that support the `name` attribute on `<details>` treat items with the same name as an exclusive group, which gives the accordion its one-open-at-a-time behaviour natively. In an older browser the items still work, but more than one can be open. Nothing breaks, and the documentation says so.

## The accordion is one item, not a group wrapper

A Cotton component renders its slot content before it renders itself, in the caller's context, so a wrapper cannot pass a group name down to the items inside it. A `<c-accordion>` wrapper would therefore still need the name repeated on every item and would contribute nothing but a `<div>`. daisyUI's own accordion markup has no wrapper either: the group is the shared name. Stacking or joining the items is ordinary layout, which the caller writes (the gallery shows it).

## `open` sets the initial state, it does not lock it

`collapse-open` and `collapse-close` force a collapse's state regardless of the user. Offering them as attributes would produce something that looks like a control and does not respond. `open` maps to the native `open` attribute on `<details>`, so the item starts expanded and still closes when the user asks. A project that really wants a locked item can pass the class through `class`.

## The card follows daisyUI's structure

The current card is a header row (icon, title, badges, actions) over a body and a two-part footer. None of that layout is daisyUI's. daisyUI's card is a figure, a body, a title and an actions row. Tie-break 1 (follow daisyUI) and tie-break 3 (fewer attributes) both point to the plain structure:

- `title` stays, as an attribute or a named slot, so an icon or badges can go in the heading without dedicated attributes.
- `actions` stays but moves from the header to `card-actions` at the foot of the body, where daisyUI puts it.
- `figure` is new, because daisyUI's card has a `<figure>` part and `image-full` and `card-side` only make sense with one.
- `icon`, `badges`, `footer`, `footer_end` and `tight` go. `tight` set `p-0` on the body, which `content_class` now does.

The modal still wraps its content in a card until issue #14 replaces that with daisyUI's own modal box. Whichever of the two features lands second reconciles the modal's call.

## The card and avatar group drop their built-in utility classes

The card always emitted `bg-base-100 shadow-sm`, and the avatar group computed a `-space-x-*` class from `size`. A component cannot take away a class it always adds, and Tailwind gives no reliable winner between two conflicting utilities on one element. Built-in utilities therefore block the caller from choosing their own. daisyUI's `card` and `avatar-group` classes stand alone, and its examples add the surface and the overlap as utilities, which is what callers now do through `class`.

The avatar group's computed class was also built by joining strings, which Tailwind cannot detect when it scans templates.

## The avatar keeps a default frame, replaced by `content_class`

The avatar is the one exception to the rule above. Without a width on its image frame, a photo renders at its natural size, which is never what a caller wants. So the frame defaults to `w-12 rounded-full` (plus `bg-neutral text-neutral-content` for a placeholder, daisyUI's own placeholder example colours), and `content_class` replaces the defaults rather than adding to them. That avoids the conflicting-utility problem while keeping a sensible default.

`size`, `shape` and `variant` go because daisyUI has no avatar size or colour modifier, and Article XIV reserves those names for daisyUI's modifiers. The modal lost `size` in #14 for the same reason. `status="online"` becomes the boolean `online` because daisyUI's modifiers are `avatar-online` and `avatar-offline`.

## The avatar's `alt` defaults to empty

The old default, "User avatar", is read aloud for every avatar, usually right beside the person's name. An empty `alt` marks the image as decorative, which is correct in the common case. When the avatar is the only thing identifying someone, the caller gives `alt`, and the documentation says so.

## `content_class` names every inner surface

Article XIV sends `class` to the root. The card body, the avatar frame and the table are inner elements callers regularly need to style. The dropdown and modal already call this attribute `content_class`, and Article XIV says to reuse an existing name for the same idea before coining one. The card's `body_class` is renamed to match.

## The table's wrapper is the root

daisyUI wraps its table in an `overflow-x-auto` element so it scrolls on narrow screens. Under Article XIV that wrapper is the root, so `class` and pass-through attributes land there, and the `<table>` takes `content_class`. A scrollable region must be reachable by keyboard (WCAG 2.1.1), so the wrapper is focusable. A focusable region needs a name, and the natural one is the table's caption, which also names the table. A caller who does not want a visible caption gives `aria-label`, which passes through to the wrapper.

## The table takes caller-written rows

daisyUI has no row or cell classes, so row and cell components would only wrap `<tr>` and `<td>` with nothing added. Building rows from a list of values would couple the component to a data shape, which the README rules out. The caller writes the rows, and the gallery shows correct header cells.

## The status dot is named with `label`, or hidden

A coloured dot conveys meaning by colour alone, which fails WCAG 1.4.1 when nothing else says the same thing. With `label`, the dot becomes an image named by that text. Without it, the dot is hidden, because the usual case is a dot beside a word that already says "Online". A dot with neither label nor text is a caller error the documentation warns about.

## `stat.group` names the container

daisyUI calls the container `stats` and each item `stat`. The package already has a pattern for one item plus its container: `avatar` and `avatar.group`. Following it keeps the item's name short, since the item is what callers configure, and reuses a name the package already has, as Article XIV asks.

## Responsive modifiers take a breakpoint value

daisyUI shows `sm:card-side`, `lg:stats-horizontal` and `md:timeline-horizontal` as the usual responsive patterns. The navigation components already let `horizontal` take either a boolean or a breakpoint for the menu. Reusing that convention means one pattern to learn across the package.

## Timeline box placement

daisyUI's examples put `timeline-box` on the event text, usually at the end, with the date at the start. `box` alone follows that. Alternating timelines put the box on the start for some items, so `box="start"` covers that case without a second attribute.

## Priorities

Priorities reflect how many adopters need each component: cards, tables and badges on nearly every page (P1); collapse and accordion, avatar, stat and list in most applications (P2); timeline, kbd and status in some (P3).

## D1 — Built on main while three other component pull requests are open

Pull requests #101 (navigation components), #102 (layout components) and #103 (action components) are open and unmerged. This feature depends only on #11, which is delivered, so it is built alongside them rather than after them. This feature branches from main and builds on none of them. All four change the README's component count and list and append to the CHANGELOG, so whichever merges later resolves those lines by hand. #103 rewrites the modal this feature adjusts (research R7). The `responsive` breakpoint check is copied from #102 and `unique_id` from #103 byte for byte, so those two reconcile as identical code.

**ADR:** none — a sequencing note for concurrent branches, nothing downstream inherits it.

## D2 — The pre-existing card test is rewritten

`tests/test_card.py` asserts the `bg-base-100 shadow-sm` surface, which FR-012 removes. It is rewritten to the new contract in T002. The behaviours it guarded that survive (the root is the card, `class` merges into its one class list, extra attributes reach it, the body sits directly inside) are asserted again. `tests/test_modal.py` is not changed: the modal keeps its output on this branch (T004), and its new tests are additions.

**Why:** Article I forbids changing a pre-existing test without a recorded decision. This is it.

**ADR:** none — local to this feature's approved breaking changes, recorded in the CHANGELOG.

## D3 — The modal keeps its contract until the action components land

The spec's edge case says the modal keeps rendering its title, body and actions if this feature lands first. The modal on main also forwards `icon`, `footer` and `footer_end` to the card, all of which the card loses. Rather than drop three documented modal attributes in a feature about content display, the modal declares `title` and `icon` and renders them into the card's `title` slot, and renders `footer` and `footer_end` itself. Its actions now sit at the foot of the card body, where daisyUI puts them. It also adds the `bg-base-100 shadow-sm` surface the card no longer draws, or the dialog would be transparent. #103 replaces all of this with daisyUI's own modal box.

**ADR:** none — a stopgap that the next feature to touch the modal removes.

## D4 — The silhouette avatar is a placeholder too

The spec gives the frame `bg-neutral text-neutral-content` "when showing a placeholder" and puts `avatar-placeholder` on the root for placeholder text. The silhouette is shown in the same situation, when there is no photo, and needs the same centring, which `avatar-placeholder` provides (`.avatar-placeholder>div{display:flex;align-items:center;justify-content:center}`). So any avatar without `src` takes `avatar-placeholder` and the placeholder colours. The old muted `bg-base-300 text-base-content/40` silhouette goes, which also removes an opacity-modified colour class.

**ADR:** none — local to the avatar template.


## D5 — Design review applied

One design reviewer, three lenses. Findings and what was done:

- **SPEC-001, high.** Gallery 1.0.0 renders an entry as one component tag, so an accordion group, a second group, a key combination, a status dot beside text, a badge inside a button and several avatar widths cannot be shown in those components' own entries. Each is shown inside the slot example of a component that holds free markup, where an application would write it: two accordion groups and a badge in a button in the card's entry, a key combination and a status beside text in the table's entry, three avatar widths and shapes in the avatar group's entry (plan "Compositions"). Each item's description names the entry that shows it. The markup-level tests for these scenarios are unchanged.
- **SPEC-002, medium.** The modal's title slot drew an empty icon for a title-only modal. Each piece is now guarded on its own, with a test.
- **ARCH-001, medium.** An unnamed Tailwind `group` on the timeline item would let any enclosing `.group` hide its connectors. The group is named `group/item`.
- **SPEC-003, low.** The stat's `0` guard only matters for a dynamic `:value`, so its test uses `:value="0"`.
- **SPEC-004, low.** The accessibility run checks the table wrapper's focus indicator.

Editorial notes applied in the same pass: the component count, the accordion's deliberate lack of a `class` declaration, the modal's footer row now sitting above its actions, and the gallery select not offering the bare breakpoint form.

**ADR:** none — plan corrections local to this feature.

## D6 — Convergence changes made directly

Four changes, each small enough that a dispatch would have cost more than the edit.

- One test module, `tests/test_content_display_no_script.py`, renders every component in this group from a caller's string with its slots and modifiers filled and asserts there is no `<script>` and no `on*=` attribute (SC-003). The stories had each left this check out. It fails when an `onclick` is added to one template.
- `collapse.html`, `accordion.html` and `timeline/item.html` no longer load the `daisy_cotton` tag library, which none of them uses.
- The README's component count is 32 (21 before this feature, 11 added). It had read 29.
- The roadmap's data display item names the components that now exist.

Every acceptance scenario that rendered markup can show has a test. The scenarios that need a browser (keyboard operation, the accordion's one-open-at-a-time behaviour, the table's scrolling, the timeline's connector, the gallery entries) are checked in the accessibility run.

**ADR:** none — local edits inside this feature.
