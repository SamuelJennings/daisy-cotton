# Implementation Plan: Annotate every component and enforce the gallery lint in CI

**Branch**: `002-gallery-lint` | **Date**: 2026-09-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-gallery-lint/spec.md`

## Summary

Annotate all 21 component templates for the gallery, then add two checks to the test suite so the annotations stay true: one runs the gallery's linter over the package's own `cotton/` directory and fails on errors and warnings, the other checks the three things the linter does not (one `@description`, a `@slot` wherever `{{ slot }}` is rendered, and no `{#` comment that runs past its line). A `CONTRIBUTING.md` explains how to run the gallery, the linter and the suite.

The annotations come first and the checks second, so every story leaves the suite green: the checks arrive against a catalog that already passes them, and each proves it can fail with its own tests against scratch templates.

## Technical Context

**Language/Version**: Python 3.12 and 3.13, Django 5.2 / 6.0 / 6.1, Django templates with Cotton

**Primary Dependencies**: django-cotton (runtime). django-cotton-gallery `>=1.0.0,<2` (development group only, already declared)

**Storage**: N/A

**Testing**: pytest + pytest-django, run by CI as `uv run pytest` after `uv sync --locked`, which installs the development group, so the gallery is importable in every CI test job

**Target Platform**: A reusable Django app

**Project Type**: Library (template-only components)

**Constraints**: No change to any component's `<c-vars>` or rendered markup (FR-014). The gallery stays a development dependency and stays out of the test settings' `INSTALLED_APPS`.

**Scale/Scope**: 21 templates, 2 new test modules, 1 new doc, README and CHANGELOG edits

## Constitution Check

| Article | How the plan meets it |
|---|---|
| XVI (components document themselves) | This feature is the article's enforcement: every template annotated, `cotton_lint --warnings-as-errors` green, and the suite checks both. |
| VII / XII (no runtime dependency beyond Cotton) | The checks import the gallery only from `tests/`. `deptry` already excludes `tests/`. No change to `[project].dependencies`. |
| X / XIV (test structure) | Two test modules grouped in `Test<Subject>` classes. Both check templates, not Python modules, so both go on the `non-mirror-paths` list in `pyproject.toml` beside the other template tests. |
| Quality bar | README and CHANGELOG change in the same PR. Coverage is unaffected (no package Python changes). |

No violations.

## Design

### Annotation format (US2–US6)

The gallery's [annotation reference](https://velezanthony.github.io/django-cotton-gallery/users/annotations/) is the format. In each template:

- The annotations sit at the top of the file, above `<c-vars>` and above any `{% load %}`: `@description` first, then one `@prop` per `<c-vars>` name in declaration order, then `@slot`, then `@slot:name` in the order the template renders them, then `@trigger`.
- The `@prop` name is the name as declared, hyphens and a leading `:` included (`hide-label`, `:size_options`).
- `default:` repeats the `<c-vars>` value. A name declared with no value gets no `default:` and no `required`, since Cotton gives it an empty value rather than refusing the call. The linter is the judge of whether each default and type agree, so every template is run through it until it reports no errors or warnings.
- Types: `text`, `boolean` or `number` from what the template does with the value. `select[...]` only where the template maps a closed set of values to classes (for example `modal`'s `size`) and the default is one of them or empty.
- Annotation text never contains a literal `<c-vars` (the existing declared-attributes test reads the first one in the file) or a `<c-…>` tag for a component this package does not ship (the linter reads comments too).
- Existing `{# … #}` banners whose content is now said by annotations are trimmed. Prose worth keeping moves into the component's existing `{% comment %}` block, or a new one below the annotations.

### The lint check (US1) — `tests/test_gallery_lint.py`

- Discovery reuses the gallery's own scanner, `django_cotton_gallery.core.catalog.scanner.scan`, pointed at the package's `cotton/` directory through a `django_cotton_gallery.core.schemas.CatalogConfig`. That keeps "what is a component and what is it called" identical to the gallery's, including the `<dir>/index.html` convention, and a new template is picked up with no change to the test (FR-004).
- `django_cotton_gallery.core.linter.lint_catalog` lints the `(path, source)` pairs. Only the pure modules are imported. The gallery app is never installed in the test settings, so its "mounted and serving" notice never fires.
- A finding blocks when its severity is `error` or `warning`. Hints never block (FR-002).
- The catalog test is parametrised by component path, so a failure names the component in the test id. Each case reads its `ComponentReport` from one `lint_catalog` call over the whole scanned catalog, made once per module, and never from `lint_component` per path: `lint_component` skips the `unknown-component` rule unless it is given the catalog's known tags. Its assertion message lists every blocking finding as `<component> L<line> <rule>: <message>` (FR-003).
- The gallery is imported directly, never through `pytest.importorskip`: a skip would pass silently in a job without the development group.
- Tests against scratch sources, linted through `lint_catalog`, prove the check can fail: an undeclared `@prop`, an unknown component, a hints-only template that passes, and a template added to a scratch `cotton/` directory that is discovered.

### The annotation check (US7) — `tests/test_gallery_annotations.py`

Reads every template under the package's `cotton/` directory (every template file by `rglob("*.html")`, which today is the same set the scanner yields) and checks:

- exactly one `{# @description … #}` (FR-015)
- when the template renders the default slot — a `{{ slot }}` expression, filters allowed and the name word-bounded so `{{ slots }}` does not count, outside `{# … #}` (blanked per line, as Django's lexer reads them) and `{% comment %}` blocks (with or without a note argument) — at least one default `{# @slot … #}`, meaning `@slot` not followed by `:` (FR-016)
- every `{#` on a line closes with `#}` later on the same line; a failure names the template and the line number (FR-017)

Each rule gets its own tests against scratch sources, pass and fail.

### Contributor docs (US8)

`CONTRIBUTING.md` at the root: `uv sync`, `uv run python manage.py runserver`, the gallery at `http://127.0.0.1:8000/django-cotton-gallery/`, `uv run python manage.py cotton_lint --warnings-as-errors`, `uv run pytest`, which findings fail, a link to the annotation reference, and the rule that a component is not done until it is annotated and the suite passes. The README's Status section links to it. CHANGELOG `[Unreleased]` records the annotations and the new checks.

## Project Structure

### Documentation (this feature)

```text
specs/002-gallery-lint/
├── spec.md
├── decisions.md
├── plan.md
├── research.md
├── tasks.md
├── progress.md
└── feature-state.json
```

### Source Code (repository root)

```text
daisy_cotton/templates/cotton/**/*.html   # 21 templates, annotations only (+ form/field.html comment)
tests/test_gallery_lint.py                # US1
tests/test_gallery_annotations.py         # US7
pyproject.toml                            # non-mirror-paths gains the two modules
CONTRIBUTING.md                           # US8
README.md                                 # link to CONTRIBUTING.md
CHANGELOG.md                              # Unreleased entry
```

## Story order

1. US3 then US2 — `form.field` (the one error) and the five everyday components.
2. US4, US5, US6 — the remaining fifteen templates.
3. US7, US1, US8 — the two checks, then the contributor guide that describes them.

Each annotation story is proven by the linter's own output for its templates (red on main, clean after), by the same three rules the annotation check will enforce, applied by hand to each touched template (one `@description`, a default `@slot` where `{{ slot }}` is rendered, no `{#` left open at the end of its line) and, for US4, the named-slot hints gone, plus a render comparison of every touched component before and after with whitespace collapsed and both ends stripped (FR-014). For `mockup.code.line` the rendered `<pre …>…</pre>` must also be byte-identical. Those comparisons are run, recorded as evidence and not committed: once the checks land, the lint and annotation rules are guarded by the suite, and the existing render tests guard the markup.

## Complexity Tracking

None.
