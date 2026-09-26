# Implementation Plan: Make the component gallery the whole demo

**Branch**: `001-gallery-demo` | **Date**: 2026-09-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-gallery-demo/spec.md`

## Summary

The demo project stops being a django-mvp site with a gallery mounted beside it and becomes the gallery alone. The root URL redirects to the gallery's index. daisyUI, Tailwind's browser build and Alpine reach the component previews through the gallery's own extension point, a `django_cotton_gallery/_extra_head.html` partial supplied by the demo app, and are scoped to preview documents so the gallery's own interface is left alone. A theme switcher sits in the gallery page and sets `data-theme` on every preview frame, remembered in the browser's local storage. django-mvp and its dependency chain leave the dev dependencies, the lockfile, the demo, the test settings and the documents. A new test walks every sidebar link and skips the folder components that the gallery's index-file defect breaks, naming this repository's tracking issue.

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton (runtime), django-cotton-gallery 1.x (dev), shared toolchain bundle (dev)

**Storage**: SQLite for the demo, in-memory for tests. No models.

**Testing**: pytest + pytest-django, run through the shared verify flow

**Target Platform**: the development server (demo) and CI (tests). Nothing here is deployed.

**Project Type**: Django package with a demo project

**Performance Goals**: none beyond the demo loading promptly

**Constraints**: the package ships no JavaScript and no stylesheet. The demo may load daisyUI, Tailwind's browser build and Alpine from a public CDN, since it is never deployed (spec Assumptions).

**Scale/Scope**: 21 component templates, 6 of them folder components

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Test-First | The sidebar-link test and the settings-without-django-mvp checks are written before the demo changes they cover. | Pass |
| II Simplicity | Configuration and two template partials. No new Python module in the package. | Pass |
| III Anti-Abstraction | The gallery's documented partials are used as they are. Nothing wraps or subclasses gallery code. | Pass |
| V Security | The gallery stays mounted under `DEBUG` only. CDN assets are pinned to a major version in a dev-only template. | Pass |
| VI Documentation | README, CONTEXT, AGENTS, brainstorm, ADR 0001 and CHANGELOG are edited in this feature. | Pass |
| VII Dependency discipline | Removes one dev dependency and its chain. Adds none. | Pass |
| XII Agnostic of every adopter | The purpose of the feature. | Pass |
| XIII–XVI | No component template changes. | N/A |

## Project Structure

### Documentation (this feature)

```text
specs/001-gallery-demo/
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
demo/
├── settings.py              # host-package apps, settings and context processor removed
├── urls.py                  # "/" redirects to the gallery; custom error handlers removed
├── views.py                 # removed
└── templates/
    ├── base.html            # removed
    ├── demo/home.html       # removed
    └── django_cotton_gallery/
        ├── _extra_head.html # new: daisyUI, Tailwind browser build, Alpine and the saved theme, previews only
        └── _extra_body.html # new: the theme switcher, gallery page only
tests/
├── settings.py              # standalone; gallery installed so its sidebar can be tested
├── test_demo.py             # new: root redirect, dependency absence, preview assets
└── test_gallery_links.py    # new: every sidebar link, folder components skipped
pyproject.toml               # django-mvp removed from the dev group, comments reworded
uv.lock                      # regenerated
README.md, CONTEXT.md, AGENTS.md, CHANGELOG.md, docs/brainstorm.md, docs/adr/0001-*.md
```

**Structure Decision**: Everything lives in the demo project, the tests and the documents. The package directory `daisy_cotton/` is untouched.

## Complexity Tracking

None.
