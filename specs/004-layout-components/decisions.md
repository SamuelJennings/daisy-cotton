# Decisions: Layout components

Ambiguities in issue #13 resolved while writing the specification, with the reasoning behind each.

## `placement` for placement

daisyUI groups `divider-start`, `drawer-end`, `footer-center`, `indicator-*` and `stack-*` as
placement modifiers, and Article XIV takes attribute names from daisyUI's own vocabulary, so the
attribute is `placement`. The same name is used by every component that has placement modifiers,
including `modal` and `dropdown` in the action components, which replaces the `position` attribute
`divider` and `modal` carry today. Values are daisyUI's own suffixes, so `placement="end"` gives
`drawer-end`.

The indicator is the one place with two placement axes. Its `placement` takes up to two values
separated by a space (`"bottom start"`), one per axis, which keeps one attribute name for one idea.

## Direction as two booleans that also take a breakpoint

daisyUI's documented responsive pattern is `join-vertical lg:join-horizontal`, both modifiers on
one element. A single `direction` attribute could not express that without a second attribute for
the breakpoint. Two booleans named as daisyUI names the modifiers can: `vertical horizontal="lg"`.
The existing `divider` already accepts a breakpoint name on a boolean through the package's
`responsive` helper, so this extends an established pattern rather than inventing one.

## Divider's `vertical` is reversed

The current `vertical` emits `divider-horizontal`. It named the layout the divider sits in rather
than the modifier it emits. Keeping it would leave `divider` as the one component whose direction
attributes mean the opposite of daisyUI's classes. The package is unreleased, so the break costs
nothing now and a lot later. The divider's `label` variable, which was read but never declared,
becomes a declared `text` attribute, the name `button` already uses for its text.

## Unlabelled divider is a separator, labelled divider is not

The ARIA `separator` role makes its children presentational, so a labelled divider with that role
would hide its label from screen readers. An unlabelled divider takes the role, and a labelled one
keeps its text readable instead.

## Footer titles are not headings

daisyUI's examples use `<h6 class="footer-title">`. An `h6` on a page without `h2` to `h5` breaks
the heading outline, and the component cannot know the page's heading levels. Each group's title
names its `<nav>` landmark instead, which is what makes several footer navs distinguishable to a
screen reader.

## Mask renders an image or a container

daisyUI applies the mask class straight to the `<img>`, which is the common case, so `src` gives an
`<img>`. Without `src` the mask wraps slotted content, which covers video, SVG or a styled block.
`alt` is always emitted, empty when not given, because an image without the attribute makes a
screen reader read out its filename.

## Hero is the container only

The README's scope section says heroes are not shipped, meaning composed page sections. daisyUI's
`hero` is a component in its own right (G1) and the issue asks for it, so the container ships and
the README is reworded to draw the line where it actually lies. No `image` attribute is added. A
background image goes in the caller's `style`, as in daisyUI's own examples, so the component
gains no attribute it does not need.

## Drawer opener is a part component

daisyUI opens a drawer with a `<label for="…" class="drawer-button">`. Callers would otherwise
hand-write that label and keep its `for` in step with the drawer's id, so `drawer.button` emits it.
It can sit anywhere on the page, because `for` works across the document.

## Code mockup lines have no default prefix

The current `mockup.code.line` defaults `prefix` to `$`, so every output line in a terminal
transcript needs `prefix=""`. daisyUI's markup has no prefix unless one is given, and a line number
or `>` is as common as `$`. No default follows daisyUI and removes the per-line override.

## Mockups lose their imposed layout and literal colours

`mockup.phone` hard-codes `text-white` and `bg-neutral-900`, which breaks Article XIII and ignores
the active theme. `mockup.window` forces a 20rem centred grid on whatever it frames. Both come out.
The frames keep the semantic-palette border and background daisyUI's own examples use.

## D1 — Built on main while the navigation components pull request is open

Pull request #101 (navigation components) is open and unmerged. This feature branches from main
and does not build on it. Both change the README's component count and list and append to the
CHANGELOG, so whichever merges second resolves those lines by hand. Neither touches the other's
templates.

**ADR:** none — a sequencing note for two branches, nothing downstream inherits it.

## D2 — The two pre-existing prefix tests change

`tests/test_mockup_code.py` asserts that a line defaults to `data-prefix="$"` and that
`prefix=""` gives an empty `data-prefix`. The approved spec removes the default and emits no
`data-prefix` without a prefix (scenario 6, decisions "Code mockup lines have no default prefix"),
so both tests describe behaviour the spec retires. They are rewritten to the new contract in T005,
not deleted: no prefix gives no `data-prefix`, and an empty prefix gives none either.

**Why:** Article I forbids changing a pre-existing test without a recorded decision. This is it.

**ADR:** none — local to this feature's approved breaking change, recorded in the CHANGELOG.

## D3 — The phone's display takes base colours

Dropping `text-white bg-neutral-900` leaves the display transparent over daisyUI's black phone
body, where the theme's default text colour is unreadable on light themes. The display carries
`bg-base-100 text-base-content`, the pair `mockup.browser` and `mockup.window` already use, so
content on the screen follows the active theme (scenario 2, Article XIII).

**ADR:** none — a styling choice inside one template.

## D4 — The drawer opener is a `<label class="btn drawer-button">`

daisyUI draws the keyboard focus ring on `label.drawer-button` inside `.drawer-content` while the
hidden toggle has focus (research R2), so the opener must be a `<label>`, and a `<button>` would
never show focus. daisyUI's documented opener is `btn drawer-button`, so `btn` is emitted too and
a caller restyles it through `class` (`btn-primary`, `btn-ghost btn-square`). The opener gets no
`role` or `tabindex`: the toggle is the Tab stop, as FS-003 ruled for the dock's drawer toggle.

**ADR:** none — follows daisyUI's documented markup, nothing cross-cutting.

## D5 — `role` is declared where a component sets one

`divider` and `join` set a role by default. An undeclared caller `role` would reach the element
a second time through `{{ attrs }}`, and the browser keeps the first, so the caller could never
override it. Declaring `role` in `<c-vars>` removes it from `{{ attrs }}` and the template writes
exactly one (research R6, Edge Cases).

**ADR:** none — the same mechanism the package already uses for `class`.

## D6 — A footer group is named by `aria-label`, not `aria-labelledby`

`aria-labelledby` needs an id on the title, and the template has nothing unique to build one from:
two footers on a page, or two groups with the same title, would collide. `aria-label="{{ title }}"`
names the landmark with the same text the title shows (scenario 3).

**ADR:** none — local to one template.

## D7 — The indicator's `placement` is a select of the nine corners

`placement` takes up to two words, one per axis. Article XVI types a fixed-value prop as
`select[…]`, and the variants matrix then shows every option. The list is the nine combinations of
`top`/`middle`/`bottom` with `start`/`center`/`end`, which is every position daisyUI can place an
item. Single words still work when written by hand, since each word is validated on its own.

**ADR:** none — an annotation choice for one prop.

## D8 — Responsive examples live in the drawer's page example

The gallery 1.0.0 cannot set a boolean attribute to a breakpoint from its controls, and it renders
no sample values (research R3). The only place it shows a caller's markup verbatim is a slot's
default content. The drawer's page slot is a whole page, which is where a responsive layout
naturally sits and is SC-006's page. It holds daisyUI's responsive divider pattern
(`<c-divider horizontal="sm">` between two columns that stack below `sm`), a
`<c-join vertical horizontal="sm">` and a `<c-footer vertical horizontal="sm">`. The drawer's own
`open` takes its breakpoint the same way, and is documented in its description. Each prop that
accepts a breakpoint says so in its description.

**Revisit if:** a gallery release lets a boolean control take a value, or renders `example:`.

**ADR:** none — a workaround for one tool version, recorded here and in research R3.
