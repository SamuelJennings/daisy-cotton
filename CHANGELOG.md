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
- `menu`, `menu.item`, `menu.title` and `menu.submenu`. `menu` is a vertical list by default, takes `size`,
  `horizontal` (or a breakpoint such as `lg`) and `paged`. `menu.item` is a link when given `href` and a
  button otherwise, and takes `active`, `disabled`, `icon` and an `aria-label` for an icon-only entry.
  `menu.title` is a heading row, and `menu.submenu` is a collapsible group that nests and takes `open`.
- `responsive` and `variation`, the two generic Cotton-attribute helper tags several of the
  above components use, in a small `daisy_cotton` templatetag library.

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
- `link` no longer defaults `href` to `#`: without an `href` it renders an anchor with no `href` attribute.
  Write `href="#"` to keep the old result. Its `variant` accepts daisyUI's eight link colours
  (`neutral`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`) and adds no class for any other value.
- `breadcrumbs` no longer adds `text-sm` to its root; pass `class="text-sm"` to keep it. The root is named
  `Breadcrumbs` by default (translated), and an `aria-label` passed by the caller replaces that name.
- A `breadcrumbs.item` puts its `class` and any other attributes on its `<li>`, where they used to land on
  the inner `<a>`. To set `target`, `hx-*` or similar on the link, write your own `<a>` in the item's slot.
  An item without `href` renders `<span aria-current="page">`, and the text span no longer carries the
  `daisy-cotton-breadcrumb-text` class.
- `dock` renders as a `<nav>` named `Dock` by default (translated; an `aria-label` passed by the caller replaces
  it) instead of a `<div>`, and no longer adds `bg-transparent backdrop-blur`; pass them through `class` to keep them.
  A `dock.item` with no `href` and no `toggle` is now a `<button type="button">`, its icon is hidden from
  assistive technology, and the drawer-toggle item no longer has `role="button" tabindex="0"`, so it is no
  longer a Tab stop.
