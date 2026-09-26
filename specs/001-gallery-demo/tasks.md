# Tasks: Make the component gallery the whole demo

**Input**: `specs/001-gallery-demo/` (spec.md, plan.md, research.md)

**Tests**: included. Each story's test task comes first and must fail before its implementation.

## Phase 1: Setup

- [ ] T001 Confirm the baseline: full suite green on the branch base, and record the six folder-component 404s against the running demo.

## Phase 2: User Story 1 — The demo is the gallery on a bare Cotton and daisyUI page (P1)

**Goal**: the demo serves the gallery alone, previews carry daisyUI, a theme switcher works, and django-mvp is gone.

**Independent Test**: start the demo, open `/`, land in the gallery, switch theme, dismiss an alert. `uv tree` shows no django-mvp.

- [ ] T002 [US1] Write `tests/test_demo.py`: `/` redirects to the gallery index. The preview document of a component carries the daisyUI, Tailwind browser and Alpine assets and a `data-theme` bootstrap. The interface page does not load daisyUI. Neither `mvp`, `flex_menu`, `easy_icons` nor `crispy_forms` is importable from the test environment's installed apps.
- [ ] T003 [US1] Rewrite `tests/settings.py` to stand alone: the demo's app list including the gallery, no django-mvp settings or context processor, no crispy settings.
- [ ] T004 [US1] Rewrite `demo/settings.py`: drop the host-package apps, their settings and the context processor. Keep `daisy_cotton`, `demo`, `django_cotton`, `django_cotton_gallery` and `django_browser_reload`.
- [ ] T005 [US1] Rewrite `demo/urls.py`: `/` redirects to the gallery index, the gallery mounts under `DEBUG`, custom error handlers go. Delete `demo/views.py`, `demo/templates/base.html` and `demo/templates/demo/home.html`.
- [ ] T006 [US1] Add `demo/templates/django_cotton_gallery/_extra_head.html` (preview-only daisyUI, themes, Tailwind browser build, Alpine, saved theme applied before paint) and `_extra_body.html` (theme `<select>` of the ten themes, interface page only, applies to every preview frame and persists).
- [ ] T007 [US1] Remove `django-mvp` from the dev dependency group in `pyproject.toml`, reword its comments, and regenerate `uv.lock`. Confirm `uv tree` has none of django-mvp, django-flex-menus, django-easy-icons, django-crispy-forms or crispy-tailwind.

## Phase 3: User Story 2 — Every sidebar link opens its component (P2)

**Goal**: a test walks every sidebar link. Folder components are skipped, naming the tracking issue.

- [ ] T008 [US2] File an issue in this repository describing the gallery's index-file defect, its reproduction and the six affected links. Do not file anything with the gallery project.
- [ ] T009 [US2] Write `tests/test_gallery_links.py`: collect the component links from the rendered gallery index, parametrise one case per link, assert 200 with the component on the page. A case for a folder component (`<name>/index.html` exists and `<name>.html` does not) is skipped with a reason naming the issue from T008 while the installed gallery still 404s it. A case that starts passing is not skipped.

## Phase 4: User Story 3 — The repository describes the package on its own terms (P2)

- [ ] T010 [US3] README.md: intro, status, scope and prior-art text name no other project as host, source or consumer.
- [ ] T011 [US3] CONTEXT.md: the Component, Block, Demo and "Component library" entries stand alone. The Demo entry describes the gallery-only demo.
- [ ] T012 [US3] AGENTS.md, `docs/brainstorm.md` and ADR 0001: remove host and consumer references. ADR 0001 keeps django-easy-icons only as an example override.
- [ ] T013 [US3] CHANGELOG.md: drop "migrated from" provenance and comparisons, and add an Unreleased line saying the demo is the component gallery alone.
- [ ] T014 [US3] `tests/` and `pyproject.toml` comments: remove remaining django-mvp mentions (the `pip install django-mvp` sample line becomes a neutral command, the regression-test docstrings drop the other project's issue numbers).
- [ ] T015 [US3] Run the SC-004 search and confirm only `django-mvp/shared` and `mvp-shared` remain.

## Phase 5: User Story 4 — The docs say `alert`'s dismiss button needs Alpine (P3)

- [ ] T016 [US4] README.md: next to `alert`, state that `dismissible` and `delay` need Alpine.js on the page, the package doesn't ship it, and without it the alert renders but can't be dismissed.

## Phase 6: Polish

- [ ] T017 Amend FR-009 in `spec.md` to track the defect in this repository's issue, matching the maintainer's rule that nothing is filed upstream by the implementation.
- [ ] T018 Full verify green.

## Dependencies

- US1 before US2 (the link test needs the gallery in the test settings).
- US3 and US4 are independent of US1 and US2 but share README.md, so they run after US1 in one sequence.
