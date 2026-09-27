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
- `<c-button>`: `size` accepts daisyUI's full `xs`–`xl` scale (previously `sm`–`lg`); `dash`,
  `link` and `active` are new style/behaviour booleans; `full` is renamed `block`, daisyUI's own
  name for the modifier. `align`, `reverse` and `condition` are removed: set layout with `class`,
  put an icon after the text in the default slot, and wrap the tag in `{% if %}` for a conditional
  button. The icon is now hidden from assistive technology (`aria-hidden="true"`); an icon-only
  button needs a caller-supplied `aria-label` for its accessible name. A disabled link (`href` and
  `disabled` together) now carries `btn-disabled`, `aria-disabled="true"`, `role="button"` and
  `tabindex="-1"` instead of a native `disabled` attribute, which links cannot carry.
- `<c-modal>`: drops the inner `<c-card>` for daisyUI's own plain box, so `class` now lands on the
  `<dialog>` instead of the card — put an inner surface's own classes in `content_class`. `size`,
  `icon`, `footer` and `footer_end` are removed: put a `<c-card>` in the default slot for a card
  inside a modal, and size the box with `content_class`. `position` is renamed `placement` and
  gains `middle` alongside `top`, `bottom`, `start` and `end`. `title` now renders as a heading
  that names the dialog (`aria-labelledby`) instead of forwarding to the card.
- `<c-dropdown>`: moves to daisyUI's popover method — the trigger is a real `<button>` with
  `popovertarget`, and the browser handles opening, closing on Escape and on an outside click,
  and reporting the open state, with no script. `valign` and `halign` are replaced by a single
  `placement` taking one side and one alignment, e.g. `placement="top end"`. `full` and `hover`
  are removed: the popover method offers neither. `class` now lands on the wrapper only and
  never reaches the default trigger. The panel no longer carries `dropdown-content`, `tabindex`,
  `z-50` or a border — put those in `content_class` if a project needs them.
