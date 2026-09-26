# Research: FS-002

What the plan rests on, read from django-cotton-gallery 1.0.0 as installed and from the repository on main (`cc7473f`).

## Linter entry points

- `python manage.py cotton_lint` builds the catalog through the gallery's settings, calls `lint_catalog(catalog.sources())`, prints each finding and exits 1 on any error, or on any warning with `--warnings-as-errors`.
- `django_cotton_gallery.core.linter.lint_catalog(pairs)` is the pure function underneath. It takes `(component_path, source)` pairs, builds the set of known component tags from those paths (so `unknown-component` is judged against the catalog it is given), and returns a `LintReport` whose `ComponentReport`s expose `errors`, `warnings` and `hints`. Its module docstring calls it the public API and says it has no I/O and no Django imports.
- `django_cotton_gallery.core.catalog.scanner.scan(CatalogConfig(cotton_dir=...))` is the gallery's discovery walk. It maps `<dir>/index.html` to the component `<dir>`, skips `_`-prefixed files, and fills each `Component` with its `path` and `source`.

**Conclusion:** the suite can lint exactly what `cotton_lint` lints by calling `scan` and `lint_catalog` directly, with no gallery settings and no installed app.

## The start-up notice

`DjangoCottonGalleryConfig.ready()` warns when the gallery's URLs are mounted. It runs only when `django_cotton_gallery` is in `INSTALLED_APPS`. `tests/settings.py` already removes it for that reason, and importing `core.linter` or `core.catalog.scanner` does not load the app.

## Named slots and hints

`scan_undeclared_template_vars` adds every `{# @slot:name #}` in the source to the allowed names, so annotating `card`'s `actions` removes the `undeclared-template-var` hint for it (spec US4, scenario 4).

## CI

The shared test workflow runs `uv sync --locked` and then `uv run pytest` for every Python and Django pair in the matrix. `uv sync` installs the default `dev` group, which carries the gallery, so a pytest check runs in every test job with no workflow change (FR-005).

## Baseline

`uv run python manage.py cotton_lint --warnings-as-errors` on main: `3/21 clean · 1 errors · 88 warnings`, exit 1. The error is `unknown-component` for `<c-form.render>` inside `form/field.html`'s `{% comment %}` block. No template has a `{#` that runs past its line.

18 of the 21 templates render `{{ slot }}`. The three that do not are `icon`, `avatar` and `dock.item`, so they need no default `@slot`. The annotation check derives this from each template, not from a list.
