# AGENTS.md — Agent Configuration for daisy-cotton

<!-- Thin index only — bloat here = ignored instructions. Details live in the pointed-to files. -->

daisy-cotton ships base daisyUI-styled components for django-cotton: buttons, inputs, cards,
alerts and the rest of an application's furniture, one Cotton component per unit. `CONTEXT.md`
defines these terms. Use them.

Presentation only. No models, no views, no forms, no URLs, no migrations, and no runtime
dependency on any host project — see `CONSTITUTION.md` Article XII.

## Stack & commands

- **Stack:** Python 3.12+ / Django 5.2, 6.0 and 6.1, uv-managed, built on Cotton and daisyUI
- **Install:** `uv sync`
- **Test:** `uv run pytest`
- **Lint:** `uv run pre-commit run --all-files` (ruff lint + format, mypy, deptry)
- **Type-check:** `uv run mypy`
- **Build:** `uv build`
- **Demo project:** `uv run python manage.py runserver 0.0.0.0:8000`

Lint is the pre-commit run, not a bare `ruff check .`: the hook config excludes `docs/` and
migrations, and a raw invocation reports findings in paths the gate does not cover.

## Agent skills

### Issue tracker

Issues tracked in GitHub Issues via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary mapped 1:1 to canonical roles (needs-triage, needs-info, ready-for-agent,
ready-for-human, wontfix). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — one `CONTEXT.md` at root and `docs/adr/` for architectural decisions.
See `docs/agents/domain.md`.

### CI checks

CI runs from the shared reusable workflows in `django-mvp/shared`, pinned at `v0.4.1`. Because
they are called rather than inlined, those status checks carry their caller job as a prefix.
The required checks are:

- `call-build / Code Quality`
- `call-build / Security Scan`
- `call-build / Build Package`
- `call-tests / Test Python 3.12, Django 5.2`
- `call-tests / Test Python 3.12, Django 6.0`
- `call-tests / Test Python 3.13, Django 5.2`
- `call-tests / Test Python 3.13, Django 6.0`

`tests.yml` and `build.yml` deliberately carry no `paths:` filter on `pull_request`. A required
check that is filtered out never reports, and a check that never reports blocks the merge.

## Releasing

Releases run through the shared release flow, never by hand and never by pushing a tag.

1. Dispatch **Prepare Release** with a bump level. It opens a PR carrying the version bump and
   the CHANGELOG section.
2. Merging that PR is the release decision. **Tag Release** then cuts the tag and the GitHub
   Release from the merge commit.
3. **Publish** uploads to PyPI through trusted publishing. PyPI's trusted publisher is bound to
   the `publish.yml` filename — renaming that file breaks publishing until the PyPI project
   settings are changed to match.

`pyproject.toml` holds the version and is the single source of truth for all three steps.

Nothing has been released yet. Before the first release: a PyPI trusted publisher pointed at
`publish.yml`, and a `RELEASE_TOKEN` secret that can actually write to this repository (the
default `GITHUB_TOKEN` cannot trigger `publish.yml` from a bot-created tag/release).

## Development workflow

Feature work follows a spec-driven process: spec → plan → tasks → implement → review → PR.
Project standards and the quality bar live in `CONSTITUTION.md`.

`docs/brainstorm.md` holds the working notes the package was founded on, chiefly the prior-art
survey. Those are conclusions, not ratified decisions.
