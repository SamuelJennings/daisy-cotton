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
- `<c-icon>`: a basic primitive that treats `name` as a literal CSS class string
  (`<i class="{{ name }} {{ class }}">`). This package resolves no icon pack of its own — a
  project wanting name-based resolution (an icon font, an SVG sprite, an icon-resolution package)
  provides its own `cotton/icon.html`, which shadows this one. Every other component here calls
  `<c-icon name="..." />` exactly as it would call that richer version.
- `responsive` and `variation`, the two generic Cotton-attribute helper tags several of the
  above components use, in a small `daisy_cotton` templatetag library.
- `<c-table>`: daisyUI's table, wrapped in a keyboard-focusable, horizontally scrolling region
  named by its `caption` (attribute or slot) or an `aria-label`. Accepts `size` (`xs`–`xl`) and
  the booleans `zebra`, `pin-rows` and `pin-cols`; extra classes reach the `<table>` through
  `content_class` and the wrapper through `class`. The caller writes `<thead>`, `<tbody>`, rows
  and cells directly in the default slot.
- `unique_id`, a `daisy_cotton` template tag returning a prefix plus eight random lowercase hex
  characters, different on every call, for elements — such as the table's caption — that need a
  unique id without the caller supplying one.
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

`avatar` takes `src`/`placeholder` with a silhouette fallback; it resolves no settings-driven user
lookup of its own. `dropdown` ships CSS-only daisyUI positioning; no JavaScript enhancement is
included. `breadcrumbs.item`'s text-wrapping hook class is `daisy-cotton-breadcrumb-text`.

Deliberately out of scope for now: anything coupled to Django's messages framework or
`Paginator`, a generic content-section wrapper, and Django form/formset rendering beyond the
single presentational `form.field`. See `docs/adr/0001-icon-is-an-extension-point.md` for the icon
decision.

### Changed

- The project is built, locked and developed with uv instead of Poetry. Contributors run `uv sync` and `uv run ...` in place of `poetry install` and `poetry run ...`, and the lockfile is now `uv.lock`. The published package is unchanged.
- Django 6.1 is supported and tested.
- The demo project is the component gallery alone: a plain Cotton and daisyUI page with a theme
  switcher, needing no other package behind it.
- `<c-card>` is rebuilt around daisyUI's own card structure. `icon`, `badges`, `footer`, `footer_end`
  and `tight` are removed: put an icon or a badge in the `title` slot instead, put footer content in
  the body or the `actions` slot, and use `content_class="p-0"` in place of `tight`. `body_class` is
  renamed `content_class`. `actions` now renders in a `card-actions` row at the foot of the body
  instead of the header. The built-in `bg-base-100 shadow-sm` surface is gone; add it through `class`
  where it is still wanted. Adds `size` (`xs`–`xl`), the booleans `border`, `dash` and `image-full`,
  `side` (a boolean or a breakpoint, as `card-side` or `<bp>:card-side`), and a `figure` slot rendered
  in a `<figure>` before the body.
- `responsive`, the `daisy_cotton` template tag `<c-card>`'s `side` and `<c-divider>`'s `vertical` use,
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
- `<c-modal>`'s actions now render in a `card-actions` row at the foot of the dialog body, after
  the `footer`/`footer_end` row.
