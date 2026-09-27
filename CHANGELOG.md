# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Every component is documented in the component gallery through `@description`, `@prop` and `@slot`
  annotations at the top of its template, and the test suite enforces it: `tests/test_gallery_lint.py`
  fails on any error or warning from the gallery's linter, and `tests/test_gallery_annotations.py`
  requires one `@description`, a default `@slot` wherever a template renders `{{ slot }}`, and
  single-line annotations. [CONTRIBUTING.md](CONTRIBUTING.md) explains how to run the checks.
- The first 21 components: `alert`, `avatar` + `avatar.group`, `badge`, `breadcrumbs` +
  `breadcrumbs.item`, `button`, `card`, `divider`, `dock` + `dock.item`, `dropdown`, `form.field`,
  `icon`, `link`, `modal`, `mockup.browser` + `mockup.window` + `mockup.phone` + `mockup.code` +
  `mockup.code.line`.
- `join`: a group of joined items such as buttons, or an input with a button. `vertical` and `horizontal` each
  take a breakpoint such as `lg`, the group has `role="group"` unless you pass `role`, and children are
  rendered with no wrapper, so give each one the `join-item` class.
- `footer` + `footer.nav`: a `<footer>` that takes `horizontal` and `vertical` (each with a breakpoint such
  as `sm`) and `placement="center"`, and link groups that are `<nav>` landmarks named by their `title`.
- `drawer` + `drawer.button`: a sidebar drawer. `id` names its toggle checkbox (never the root element),
  `open` keeps the sidebar open beside the page, from a breakpoint such as `lg` when given one, and the
  `side` slot holds the sidebar. `drawer.button` is a `<label>` for that id that opens the drawer without
  script.
- `indicator` + `indicator.item`: a badge or other item pinned to a corner of its content. Put items in the
  `items` slot and the content in the default slot; the items are always written first. `placement` takes
  one or two words from `top`, `middle`, `bottom`, `start`, `center` and `end` (`top end`, `bottom start`),
  each checked on its own, so an unknown word adds nothing.
- `hero`: the hero container. The slot lands inside `hero-content`, `overlay` adds a `hero-overlay` element
  hidden from assistive technology behind the content, and a `style` attribute such as
  `style="background-image: url(hero.jpg)"` reaches the root unchanged. Composed hero sections stay in your own markup.
- `mask`: crops an image or a block of content to one of daisyUI's fourteen shapes (`circle`, `heart`,
  `hexagon`, `squircle`, `star` and the rest), with `half="1"` or `half="2"` for one half of the shape. With
  `src` it renders an `<img>` that always carries `alt` (empty unless you set it); without `src` it wraps
  the slot in a `<div>`. An unknown `shape` or `half` adds nothing.
- `stack`: piles its children on top of each other, offset towards `placement` (`top`, `bottom`, `start`
  or `end`). Children are rendered untouched and stay visible to assistive technology.
- `<c-icon>`: a basic primitive that treats `name` as a literal CSS class string
  (`<i class="{{ name }} {{ class }}">`). This package resolves no icon pack of its own — a
  project wanting name-based resolution (an icon font, an SVG sprite, an icon-resolution package)
  provides its own `cotton/icon.html`, which shadows this one. Every other component here calls
  `<c-icon name="..." />` exactly as it would call that richer version.
- `menu`, `menu.item`, `menu.title` and `menu.submenu`. `menu` is a vertical list by default, takes `size`,
  `horizontal` (or a breakpoint such as `lg`) and `paged`. `menu.item` is a link when given `href` and a
  button otherwise, and takes `active`, `disabled`, `icon` and an `aria-label` for an icon-only entry.
  `menu.title` is a heading row, and `menu.submenu` is a collapsible group that nests and takes `open`.
- `navbar`, a top bar rendered as a `<nav>` named `Main` unless given an `aria-label`. Its `start`, `center`
  and `end` slots each become a `navbar-start`, `navbar-center` or `navbar-end` section only when given,
  and the default slot sits directly inside the bar.
- `tabs`, a row of tabs with `box`, `border` and `lift` styles, a `size` and a `placement` of `top` or
  `bottom`. The row is a `tablist` unless given `links`. `tabs.tab` is a link when given `href`, a radio
  input followed by its panel when given `name`, and a button otherwise, and takes `active` and `disabled`.
- `steps`, an ordered list showing progress, with `vertical` and `horizontal` (each a boolean or a
  breakpoint such as `lg`). `steps.step` takes a `variant` colour, `current` (written as
  `aria-current="step"`), `content` for the marker's text and an `icon` shown in the marker.
- `megamenu`, a navigation bar whose entries open panels, rendered as a `<nav popover>` named `Site`
  unless given an `aria-label`. It needs an `id`, takes `wide`, `full` and `size`, and shows a `Menu`
  button below the small breakpoint. `megamenu.item` is a button paired with the panel it opens, built
  from the megamenu's id (given as `megamenu`) and the item's `key`.
- `responsive` and `variation`, the two generic Cotton-attribute helper tags several of the
  above components use, in a small `daisy_cotton` templatetag library.
- `unique_id`, a `daisy_cotton` template tag returning a prefix plus eight lowercase hex
  characters, different on every call. `<c-dropdown>` uses it to give its panel an id when the
  caller gives none.
- `<c-swap>`: daisyUI's checkbox-driven swap. `rotate`, `flip` and `active` map to `swap-rotate`,
  `swap-flip` and `swap-active`; `label` names the checkbox for assistive technology; `checked`,
  `disabled`, `name` and `value` land on the checkbox, and everything else lands on the wrapper.
  `on` and `off` slots always render in `swap-on`/`swap-off`, and an `indeterminate` slot renders
  in `swap-indeterminate` when given. The checkbox accepts extra classes through `input_class` —
  a theme toggle is `input_class="theme-controller" value="dark"`; the theme controller has no
  component of its own, since a plain `<c-swap>` already covers it.
- `<c-fab>`: daisyUI's floating action button. The default trigger is a large circular
  `<c-button>` receiving the FAB's own extra attributes and explicitly focusable, so a click
  opens it in every browser; a `button` slot replaces it entirely. `flower` maps to `fab-flower`;
  `close` and `main_action` slots render in `fab-close`/`fab-main-action`, taking the trigger's
  place while the FAB is open. `class` lands on the wrapper only and never reaches the default
  trigger.

`avatar` takes `src`/`placeholder` with a silhouette fallback; it resolves no settings-driven user
lookup of its own. `dropdown` ships CSS-only daisyUI positioning; no JavaScript enhancement is
included. `breadcrumbs.item`'s text-wrapping hook class is `daisy-cotton-breadcrumb-text`.

Deliberately out of scope for now: anything coupled to Django's messages framework or
`Paginator`, a generic content-section wrapper, and Django form/formset rendering beyond the
single presentational `form.field`. See `docs/adr/0001-icon-is-an-extension-point.md` for the icon
decision.

### Changed

- `divider`: `vertical` now emits `divider-vertical`, as daisyUI names it. Write `horizontal` to get
  what `vertical` used to give. Both accept a breakpoint such as `md`; a value that is not a
  breakpoint emits nothing.
- `divider`: `position` is renamed `placement`, and `variant` and `placement` ignore values daisyUI
  does not define.
- `divider`: the `label` slot and the undeclared `label` attribute are removed. Use the `text`
  attribute or the default slot.
- `divider`: an unlabelled divider is a `separator` (with `aria-orientation="vertical"` when
  `horizontal` is set); a labelled one has no default role. Pass `role` to replace either.
- `mockup.code.line` has no default prefix: write `prefix="$"` for a shell prompt. A line with no
  prefix (or an empty one) renders no `data-prefix` attribute.
- `mockup.phone`'s display uses the theme's base colours instead of white text on a fixed dark
  background, and no longer centres its content. To keep the old look, wrap the content in
  `<div class="grid place-content-center">`.
- `mockup.window` no longer imposes a centred 20rem-high content area; the content sits in a plain
  `<div>` and lays itself out. To keep the old layout, wrap the content in
  `<div class="grid place-content-center h-80">`.
- `mockup.browser` puts its content in a `<div>` below the toolbar, as daisyUI's markup does.
- Every mockup (`mockup.browser`, `mockup.phone`, `mockup.window`, `mockup.code`, `mockup.code.line`)
  accepts `class` and passes further attributes to its root element, and `mockup.code` is
  keyboard-focusable so a long block can be scrolled with the arrow keys. Pass `tabindex` to change
  that.
- The project is built, locked and developed with uv instead of Poetry. Contributors run `uv sync` and `uv run ...` in place of `poetry install` and `poetry run ...`, and the lockfile is now `uv.lock`. The published package is unchanged.
- Django 6.1 is supported and tested.
- The demo project is the component gallery alone: a plain Cotton and daisyUI page with a theme
  switcher, needing no other package behind it.
- `<c-button>`: `size` accepts daisyUI's full `xs`–`xl` scale (previously `sm`–`lg`); `dash`,
  `soft`, `link`, `active`, `wide`, `square` and `circle` are new booleans (on main they reached the
  element as raw attributes and did nothing); `full` is renamed `block`, daisyUI's own
  name for the modifier. `align`, `reverse` and `condition` are removed: set layout with `class`,
  put an icon after the text in the default slot, and wrap the tag in `{% if %}` for a conditional
  button. The icon is now hidden from assistive technology (`aria-hidden="true"`); an icon-only
  button needs a caller-supplied `aria-label` for its accessible name. A disabled link (`href` and
  `disabled` together) now carries `btn-disabled`, `aria-disabled="true"`, `role="button"` and
  `tabindex="-1"` instead of a native `disabled` attribute, which links cannot carry.
- `<c-modal>`: drops the inner `<c-card>` for daisyUI's own plain box, so `class` now lands on the
  `<dialog>` instead of the card — put an inner surface's own classes in `content_class`. `size`,
  `icon`, `footer` and `footer_end` are removed: put a `<c-card>` in the default slot for a card
  inside a modal, and size the box with `content_class`. The `actions` slot now renders in
  daisyUI's actions row at the foot of the box instead of the card header. `position` is renamed `placement` and
  gains `middle` alongside `top`, `bottom`, `start` and `end`. `title` now renders as a heading
  that names the dialog (`aria-labelledby`) instead of forwarding to the card.
- `<c-dropdown>`: moves to daisyUI's popover method — the trigger is a real `<button>` with
  `popovertarget`, and the browser handles opening, closing on Escape and on an outside click,
  and reporting the open state, with no script. `valign` and `halign` are replaced by a single
  `placement` taking one side and one alignment, e.g. `placement="top end"`. `full` and `hover`
  are removed: the popover method offers neither. `class` now lands on the wrapper only and
  never reaches the default trigger. The panel no longer carries `dropdown-content`, `tabindex`,
  `z-50` or a border — put those in `content_class` if a project needs them. `id` now names the
  panel instead of passing through to the wrapper or the trigger. A custom `button` slot trigger
  opens the panel only if it is a button carrying `popovertarget` set to the dropdown's `id`,
  `type="button"` and `style="anchor-name: --<id>"`, so a dropdown with a custom trigger needs an
  `id`. A `<div tabindex="0" role="button">` trigger no longer opens anything.
- `link` no longer defaults `href` to `#`: without an `href` it renders an anchor with no `href` attribute.
  Write `href="#"` to keep the old result. Its `variant` accepts daisyUI's eight link colours
  (`neutral`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`) and adds no class for any other value.
- `breadcrumbs` no longer adds `text-sm` to its root; pass `class="text-sm"` to keep it. The root is named
  `Breadcrumbs` by default (translated), and an `aria-label` passed by the caller replaces that name.
- A `breadcrumbs.item` puts its `class` and any other attributes on its `<li>`, where they used to land on
  the inner `<a>`. To set `target`, `hx-*` or similar on the link, write your own `<a>` in the item's slot.
  An item without `href` renders `<span aria-current="page">`. Linked items render their text directly in the
  `<a>` with no span, and the current item's span has no class. A project that styled
  `.daisy-cotton-breadcrumb-text` now targets `.breadcrumbs li > a` and `.breadcrumbs li > span`, or writes its
  own span in the item's slot.
- `dock` renders as a `<nav>` named `Dock` by default (translated; an `aria-label` passed by the caller replaces
  it) instead of a `<div>`, and no longer adds `bg-transparent backdrop-blur`; pass them through `class` to keep them.
  A `dock.item` with no `href` and no `toggle` is now a `<button type="button">`, its icon is hidden from
  assistive technology, and the drawer-toggle item no longer has `role="button" tabindex="0"`, so it is no
  longer a Tab stop.
