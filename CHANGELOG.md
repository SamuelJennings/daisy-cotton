# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The first 30 components, migrated from django-mvp's own Cotton component library:
  `alert`, `avatar` + `avatar.group`, `backdrop`, `badge`, `breadcrumbs` + `breadcrumbs.item`,
  `button`, `card` + `card.wrapper`, `container`, `divider`, `dock` + `dock.item`, `dropdown`,
  `form.field`, `grid`, `group`, `icon`, `link`, `modal`, `mockup.browser` + `mockup.window` +
  `mockup.phone` + `mockup.code` + `mockup.code.line`, `placeholder.card`, `rule`, `text` and
  `toolbar`.
- `<c-icon>`: a basic primitive that treats `name` as a literal CSS class string
  (`<i class="{{ name }} {{ class }}">`). This package resolves no icon pack of its own — a
  project wanting name-based resolution (an icon font, an SVG sprite, django-easy-icons) provides
  its own `cotton/icon.html`, which shadows this one. Every other component here calls
  `<c-icon name="..." />` exactly as it would call that richer version.
- `responsive` and `variation`, the two generic Cotton-attribute helper tags several of the
  above components use, in a small `daisy_cotton` templatetag library.

### Changed

- `avatar`'s automatic user-avatar lookup is dropped along with it: the component no longer
  resolves a settings-driven `avatar_url`. It keeps `src`/`placeholder`/silhouette-fallback; a
  caller passes `src` itself.
- `dropdown` ships CSS-only daisyUI positioning. The smart-placement JavaScript enhancement
  django-mvp's version layers on top (Floating UI) is not included — no JS build pipeline exists
  in this package yet.
- `breadcrumbs.item`'s text-wrapping hook class is `daisy-cotton-breadcrumb-text`, not
  `mvp-breadcrumb-text`.

Not migrated in this pass, and deliberately out of scope: anything coupled to Django's messages
framework or `Paginator` (kept out for now, not because it's app-specific), a generic
content-section wrapper, and Django form/formset rendering beyond the single presentational
`form.field`. See `docs/adr/0001-icon-is-an-extension-point.md` for the icon decision.
