# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
