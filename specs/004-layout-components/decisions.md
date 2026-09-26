# Decisions: Layout components

Ambiguities in issue #13 resolved while writing the specification, with the reasoning behind each.

## `position` for placement, not a new name

daisyUI groups `divider-start`, `drawer-end`, `footer-center`, `indicator-*` and `stack-*` as
placement modifiers. The package already uses `position` for exactly this idea on `divider` and
`modal`, and Article XIV says a name another component already uses for the same idea is reused
before a new one is coined. Renaming it on those components would be churn with no gain for the
caller. Values are daisyUI's own suffixes, so `position="end"` gives `drawer-end`.

The indicator is the one place with two placement axes. Its `position` takes up to two values
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
