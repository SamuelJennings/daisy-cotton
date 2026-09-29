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
  caller gives none, and `<c-table>` to give its caption the id that names the scrolling region.
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
- `<c-table>`: daisyUI's table, wrapped in a keyboard-focusable, horizontally scrolling region
  named by its `caption` (attribute or slot) or an `aria-label`. Accepts `size` (`xs`–`xl`) and
  the booleans `zebra`, `pin-rows` and `pin-cols`; extra classes reach the `<table>` through
  `content_class` and the wrapper through `class`. The caller writes `<thead>`, `<tbody>`, rows
  and cells directly in the default slot.
- `<c-collapse>` and `<c-accordion>`: daisyUI's collapse, built on `<details>`/`<summary>` with no
  script. `<c-collapse>` accepts `title` (attribute or slot), the booleans `arrow` and `plus`, and
  `open`, which renders it already expanded without preventing the user from collapsing it again —
  daisyUI's state-locking `collapse-open`/`collapse-close` classes are not offered. `name` is not
  declared, so it passes straight through to `<details>`. `<c-accordion>` is a `<c-collapse>` that
  requires `name`: items sharing one form an exclusive group, in which opening an item closes the
  others; in a browser without grouped `<details>` support, more than one can stay open.
- `<c-stat>` and `<c-stat.group>`: daisyUI's stat, always placed inside a group even when it is
  alone. `<c-stat>` accepts `title`, `value` and `desc` (each an attribute or a named slot),
  rendered in that order, a `figure` slot and an `actions` slot; a value of `0` still renders.
  `<c-stat.group>` accepts `vertical` and `horizontal`, each a boolean or a breakpoint, as
  `stats-vertical`/`stats-horizontal` or their responsive form.
- `<c-list>` and `<c-list.row>`: daisyUI's list, a `<ul>` carrying `list` holding `<c-list.row>`
  items, each an `<li>` carrying `list-row`. A row's own children reach `list-col-grow` and
  `list-col-wrap` through their own `class`, as the row's documentation shows.
- `<c-timeline>` and `<c-timeline.item>`: daisyUI's timeline. `<c-timeline>` accepts `vertical` and
  `horizontal` (each a boolean or a breakpoint), and the booleans `compact` and `snap-icon`.
  `<c-timeline.item>` accepts `start`, `middle` and `end` (each an attribute or a named slot, only
  emitted when given) and `box`, which puts `timeline-box` on the end part, or the start part when
  given as `box="start"`. Every item carries a leading and a trailing connector line, hidden from
  assistive technology, so consecutive items join and the line stops at the first and last item.
- `<c-kbd>`: daisyUI's kbd, a `<kbd>` carrying `kbd`, holding `text` then the default slot, with
  `size` (`xs`–`xl`).
- `<c-status>`: daisyUI's status, a `<span>` carrying `status`, with `variant` (the eight daisyUI
  colours) and `size` (`xs`–`xl`). Given `label`, it is exposed to assistive technology as an image
  named by it; without one, it is hidden from assistive technology.
- `<c-carousel>` and `<c-carousel.item>`: daisyUI's carousel, a scrollable, snapping row or column of
  `<c-carousel.item>` slides. With no controls of its own it is a focusable, named `role="region"`
  carrying the translatable roledescription "carousel", scrolled by keyboard with the arrow keys once
  focused; each slide carries `role="group"` and the roledescription "slide". `snap` maps to
  `carousel-start`/`carousel-center`/`carousel-end`, and `horizontal`/`vertical` (each a boolean or a
  breakpoint) to `carousel-horizontal`/`carousel-vertical`. `aria-label` has no default: the component
  cannot invent a name. A slide accepts `id`, `class` and other attributes, so a project builds its own
  previous/next or indicator links to it with `<c-button href="#…">`.
- `<c-chat>`: daisyUI's chat, a `<div>` carrying `chat` and a `placement` class (`start`/`end`, default
  `start`), holding the default slot in a `chat-bubble` coloured by `variant` (the eight daisyUI
  colours), plus optional `image`, `header` and `footer` named slots rendered in `chat-image`,
  `chat-header` and `chat-footer`, each emitted only when given. An avatar goes in the `image` slot as
  `<c-avatar>`; the chat's side is visual only, so name the speaker in `header`.
- `<c-diff>`: daisyUI's diff, a `<figure>` carrying `diff` and `tabindex="0"`, holding `diff-item-1`
  (also focusable) and `diff-item-2` in the `item_1` and `item_2` named slots, and an empty
  `diff-resizer`, in that order. Both items stay available to assistive technology whatever the
  resizer's position; dragging it needs a pointer. `aria-label` has no default: the component cannot
  invent a name.
- `<c-hover-gallery>`: daisyUI's hover gallery, a `<figure>` carrying `hover-gallery` holding the
  default slot of images, with no width class of its own. Every image stays available to assistive
  technology; only the hover effect needs a pointer.
- `<c-hover-3d>`: daisyUI's hover 3D card, an `<a>` with `href` or a `<div>` without one, carrying
  `hover-3d`, holding the default slot followed by eight empty `<div aria-hidden="true">` zones that
  track the pointer. The content must be one element with no buttons, links or inputs of its own; a
  linked card takes its accessible name from the content's text or image alt, or from `aria-label`.
- `<c-text-rotate>`: daisyUI's text rotate, a `<span>` carrying `text-rotate` wrapping one inner
  `<span>` that holds up to six slotted lines shown one at a time in a ten-second loop, `content_class`
  reaching that inner span. A `duration-*` class on the root changes the loop's length; the loop pauses
  only while the pointer is over it, and every line stays readable to a screen reader.
- `<c-countdown>`: daisyUI's countdown, a `<span>` carrying `countdown` wrapping one inner `<span>` that
  sets `--value` and shows the number, hidden from assistive technology, followed by a visually hidden
  copy of the number so a screen reader reads it as rendered. `value` defaults to `0`; daisyUI animates
  0 through 999 and any other value is rendered as given, so it must be a number, never unvalidated user
  input. A script that animates it updates `--value`, the visible text and the hidden copy together.
  `hero`'s example shows a days, hours, minutes and seconds clock of four labelled countdowns.
- `<c-loading>`: daisyUI's loading indicator, a `<span>` carrying `loading` and `role="status"`, named
  by `label` or the translatable "Loading". Each of `spinner`, `dots`, `ring`, `ball`, `bars` and
  `infinity` adds its own class; with none given daisyUI draws the spinner, and giving more than one
  emits every class named. `size` takes the five daisyUI sizes; colour it with a text utility such as
  `text-primary` in `class`.
- `<c-tooltip>`: a wrapper carrying `tooltip` around the default slot (the trigger), followed by a
  `tooltip-content` element with `role="tooltip"` holding `tip` or, when given, the `content` slot —
  never `data-tip`, which CSS-generated text does not reliably expose to assistive technology.
  `placement` takes one side (`top`, `bottom`, `left`, `right`) and one alignment (`start`, `center`,
  `end`), `variant` takes daisyUI's seven tooltip colours, and `open` forces the hint to show. `id`
  lands on the `tooltip-content` element rather than the wrapper, so a trigger can reference it with
  `aria-describedby`.
- `<c-progress>`: a native `<progress>` carrying `progress`, `variant` taking daisyUI's eight colours,
  `max` defaulting to `100`, `value` emitted for emptiness rather than truthiness so a bound `0` still
  renders `value="0"` and a bound `None` renders no attribute at all, and `aria-label` from `label`.
- `<c-radial-progress>`: a `<div>` carrying `radial-progress` and `role="progressbar"`, with
  `aria-valuenow`/`aria-valuemin`/`aria-valuemax` and a `style` beginning `--value:<value>;` (a
  caller's `style` appended after it). `value` is required, with an empty default so a page variable
  named `value` can never leak in; the visible `<value>%` is replaced by the default slot when given.
  Size and thickness are set with `[--size:…]`/`[--thickness:…]` classes in `class`.
- `<c-toast>`: a `<div>` carrying `toast` around one or more alerts, with no `role` or live-region
  attribute of its own — the alerts inside keep their own roles, and a live region on the wrapper
  too would announce each message twice. `placement` takes one vertical position (`top`, `middle`,
  `bottom`) and one horizontal position (`start`, `center`, `end`), each word validated on its own.
  Placing the toast on the page and keeping two toasts from sharing a placement is the project's
  job; the README shows a project rendering Django's messages framework into one.
- `<c-skeleton>`: a `<div>` carrying `skeleton`, hidden from assistive technology unless `text` is
  given. Size it with `h-*`/`w-*` utility classes in `class`. `text` given as a bare attribute adds
  `skeleton-text` and leaves the default slot as the content; given a string it adds `skeleton-text`
  and renders that string as the content instead.
- `<c-input>`: daisyUI's text input, an `<input>` carrying `input`, `variant` (the eight daisyUI
  colours), `size` (`xs`–`xl`) and `ghost`, with `type` defaulting to `text` and accepting every
  text-like native type; checkbox, radio, range and file have their own components, and `input`
  does not refuse those types. With `start` or `end` filled it renders daisyUI's wrapped form
  instead: a `<label>` carrying `input` and the modifiers, holding the start content, the `<input>`
  and the end content, in that order; `class` lands on whichever element carries `input`, and every
  other attribute lands on the `<input>` itself. Neither slot has a default sample, so the bare
  gallery preview stays one plain `<input>`. Needs a `<c-label>`, an `aria-label` or an
  `aria-labelledby` for a name; `input` cannot invent one.
- `<c-label>`: daisyUI's label in its three forms. Above a control, `<c-label for="id_email"
  text="Email" />` renders `<label class="label" for="id_email">Email</label>`. Wrapping a
  checkbox, radio or toggle, the default slot holds the control and `text` follows it inside the
  same `<label>`. With `floating`, it renders daisyUI's floating label instead: a
  `<label class="floating-label">` holding the slot's control, then a `<span>` with `text`, and no
  `label` class. `class` merges into the `<label>` and every other attribute, including `for`,
  passes through.
- `<c-fieldset>`: daisyUI's fieldset. `legend` (attribute or named slot) renders a
  `<legend class="fieldset-legend">` as the first child, then the default slot, then `description`
  as a `<p class="label">` and `errors` as one `<div class="grid">` holding a
  `<p class="label text-error">` per message — `errors` takes a string for one line or a list (a
  Django `ErrorList` works) for one line per item. With `id`, the fieldset carries it once and the
  description and errors carry `<id>-description` and `<id>-errors`, so a control can name both in
  `aria-describedby`; without `id`, neither derived id is emitted. An empty `description` or
  `errors` renders nothing.
- `<c-textarea>`: daisyUI's multi-line text box, a `<textarea>` carrying `textarea`, `variant`
  (the eight daisyUI colours), `size` (`xs`–`xl`) and `ghost`. The default slot becomes its value,
  exactly as written, with nothing added around it. Needs a `<c-label>`, an `aria-label` or an
  `aria-labelledby` for a name; `textarea` cannot invent one.
- `<c-select>`: daisyUI's select, following the text input's own split. Unwrapped, it is one
  `<select>` carrying `select`, `variant`, `size` and `ghost`, with the default slot as its
  `<option>` elements. With `start` or `end` filled it renders the wrapped form instead: a
  `<label>` carrying `select` and the modifiers, holding the start content, the `<select>` and the
  end content, in that order; `class` lands on whichever element carries `select`, and every other
  attribute lands on the `<select>` itself.
- `<c-checkbox>`: daisyUI's checkbox, a native `<input type="checkbox">` carrying `checkbox`,
  `variant` (the eight daisyUI colours) and `size` (`xs`–`xl`). `type` is written by the template
  and not accepted as an attribute. Needs a `<c-label>`, an `aria-label` or an `aria-labelledby`
  for a name; `checkbox` cannot invent one. Its indeterminate state can only be set from your own
  script.
- `<c-radio>`: daisyUI's radio, a native `<input type="radio">` carrying `radio`, `variant` and
  `size` the same way `checkbox` does. Give every radio in a group the same `name` and group them
  in a `<c-fieldset>` whose `legend` names the group.
- `<c-toggle>`: daisyUI's switch, a native `<input type="checkbox" role="switch">` carrying
  `toggle`, `variant` and `size` the same way `checkbox` does. Both `type` and `role` are written
  by the template and not accepted as attributes.
- `<c-file-input>`: daisyUI's file input, a native `<input type="file">` carrying `file-input`,
  `variant`, `size` and, when `ghost` is given, `file-input-ghost`.
- `<c-range>`: daisyUI's range, a native `<input type="range">` carrying `range`, `variant`,
  `size` and, when `vertical` is given, `range-vertical`. `min` and `max` are always emitted,
  defaulting to the browser's own `0` and `100`.

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
- `<c-alert>`: adds `horizontal` and `vertical`, each taking a breakpoint such as `sm`. `variant`
  now ignores a value daisyUI does not define, instead of emitting an invalid class. A caller-given
  `role` now replaces the default `role="alert"` instead of being written a second time, so
  `role="status"` gives a polite announcement. The dismiss button is now drawn by `<c-button>`,
  with the translatable accessible name "Dismiss" and its `✕` glyph hidden from assistive
  technology; it was a plain `<button>` named only by that glyph. The icon is now hidden from
  assistive technology. `delay` now accepts only a whole number of milliseconds: any other value is
  ignored and the alert stays until dismissed. A page variable named after one of the alert's attributes no longer leaks into it.
- `dock` renders as a `<nav>` named `Dock` by default (translated; an `aria-label` passed by the caller replaces
  it) instead of a `<div>`, and no longer adds `bg-transparent backdrop-blur`; pass them through `class` to keep them.
  A `dock.item` with no `href` and no `toggle` is now a `<button type="button">`, its icon is hidden from
  assistive technology, and the drawer-toggle item no longer has `role="button" tabindex="0"`, so it is no
  longer a Tab stop.
- `<c-card>` is rebuilt around daisyUI's own card structure. `icon`, `badges`, `footer`, `footer_end`
  and `tight` are removed: put an icon or a badge in the `title` slot instead, put footer content in
  the body or the `actions` slot, and use `content_class="p-0"` in place of `tight`. `body_class` is
  renamed `content_class`. `actions` now renders in a `card-actions` row at the foot of the body
  instead of the header. The built-in `bg-base-100 shadow-sm` surface is gone; add it through `class`
  where it is still wanted. Adds `size` (`xs`–`xl`), the booleans `border`, `dash` and `image-full`,
  `side` (a boolean or a breakpoint, as `card-side` or `<bp>:card-side`), and a `figure` slot rendered
  in a `<figure>` before the body.
- `responsive`, the `daisy_cotton` template tag behind every attribute that takes a breakpoint,
  now ignores a string that is not one of `sm`, `md`, `lg`, `xl`, `2xl` and emits no class for it —
  it previously emitted a class for any non-empty string.
- `<c-badge>` renders a `<span>` instead of a `<div>`, so it is valid inside a button. `size` gains
  `xs`, `md` and `xl` alongside the existing `sm` and `lg`; the booleans `dash`, `soft` and `ghost`
  are added alongside `outline`. Extra attributes, including data attributes, now reach the badge
  through `{{ attrs }}`, which they previously did not. The internal `size_opts` map and its
  `get_item` lookup are removed.
- `<c-avatar>`'s `status` is renamed `online`/`offline` (`avatar-online`/`avatar-offline`), a
  boolean each instead of one `select`. `size`, `size_options`, `shape` and `variant` are removed:
  the image frame's width and shape now go through `content_class`, which replaces the
  `w-12 rounded-full` default (plus `bg-neutral text-neutral-content` whenever there is no `src`,
  including the silhouette) entirely rather than adding to it. `alt` now defaults to empty instead
  of `"User avatar"`. The silhouette's muted `bg-base-300 text-base-content/40` colours are gone;
  it now takes the same neutral placeholder colours as initials text. `<c-avatar.group>`'s `size`
  and `space_options` (and its `get_item` lookup) are removed; the overlap between avatars, such as
  `-space-x-6`, now goes entirely through `class`, and the group spreads extra attributes through
  `{{ attrs }}`, which it previously did not.
