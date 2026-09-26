# Contributing to daisy-cotton

Thanks for helping. This page covers setting up, running the component gallery, running the checks, and what a finished component looks like.

## Set up

The project is built and developed with [uv](https://docs.astral.sh/uv/). From a checkout:

```bash
uv sync
```

This installs the package, its development tools and the component gallery into a local `.venv`. Prefix every command below with `uv run` so it uses that environment.

## Open the component gallery

```bash
uv run python manage.py runserver
```

Then open <http://127.0.0.1:8000/django-cotton-gallery/>. Every component is listed there with its description, attributes and slots, all read from the annotations at the top of its template. The gallery is a development tool and only runs with `DEBUG` on, which the demo project sets. Previews load the Bootstrap Icons font, so any icon attribute can be tried with a class such as `bi bi-house`.

## Run the checks

Check the annotations with the gallery's linter:

```bash
uv run python manage.py cotton_lint --warnings-as-errors
```

Run the test suite:

```bash
uv run pytest
```

Run the formatter, linter and type checks:

```bash
uv run pre-commit run --all-files
```

### What fails

Errors and warnings fail. Hints do not: a hint is advice the linter cannot be sure about, such as a template variable it can't see declared. The test suite applies the same rule, so `tests/test_gallery_lint.py` fails on any error or warning in any component, and the failure lists each finding as `<component> L<line> <rule>: <message>`.

`tests/test_gallery_annotations.py` adds four checks the linter does not make. Every template must have:

- exactly one `{# @description … #}`
- a default `{# @slot … #}` if it renders `{{ slot }}`
- every `{#` closed with `#}` on the same line
- every `variant`, `align`, `position` or `placement` prop typed `select['…']` with its values listed, so the gallery offers a dropdown

The annotation format is described in the gallery's [annotation reference](https://velezanthony.github.io/django-cotton-gallery/users/annotations/).

## When a component is done

A component is not done until it carries its annotations and the suite passes. In practice, a new or changed component in `daisy_cotton/templates/cotton/` needs:

1. A `@description`, one `@prop` for each name in `<c-vars>`, and a `@slot` and `@slot:name` for each slot it renders, at the top of the template.
2. `uv run python manage.py cotton_lint --warnings-as-errors` reporting no errors or warnings.
3. `uv run pytest` and `uv run pre-commit run --all-files` passing.
4. A line in the `[Unreleased]` section of the [CHANGELOG](CHANGELOG.md).

A new template is picked up by the linter and both checks automatically. There is no list to add it to.
