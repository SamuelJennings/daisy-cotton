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
