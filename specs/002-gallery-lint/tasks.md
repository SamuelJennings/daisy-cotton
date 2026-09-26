# Tasks: Annotate every component and enforce the gallery lint in CI

**Input**: `specs/002-gallery-lint/` — spec.md, plan.md, research.md, decisions.md

**Organization**: by user story, in build order (plan.md "Story order"). Annotation stories come first so each check lands against a catalog that already passes it.

**Proof for annotation tasks**: `uv run python manage.py cotton_lint` output for the task's templates shows findings before and none (no errors, no warnings) after, each touched template has exactly one `{# @description`, a default `{# @slot` (no colon) where it renders `{{ slot }}`, and no line with a `{#` lacking a later `#}`, and every touched component's render is identical before and after with whitespace collapsed and both ends stripped (for `mockup.code.line`, the rendered `<pre …>…</pre>` byte-identical). For US4, the `undeclared-template-var` hints main reports for its named slots are gone. Record all of it in the task's evidence.

## Phase 1: US3 — The form field is annotated and its lint error is gone (P1)

- [x] T001 [US3] Reword the `{% comment %}` in `daisy_cotton/templates/cotton/form/field.html` so it names no component outside this package (FR-008), and add its annotations: `@description`, a `@prop` for each of the nine `<c-vars>` names with `label`, `help-text` and `errors` saying a named slot of the same name also works, and a default `@slot` saying what it fills per control type (FR-007).

## Phase 2: US2 — Buttons, links, badges, alerts and icons are fully annotated (P1)

- [x] T002 [P] [US2] Annotate `button.html`, `link.html` and `badge.html` (FR-006, FR-013).
- [x] T003 [P] [US2] Annotate `alert.html` and `icon.html`. `icon` renders no default slot, so it gets no `@slot` (FR-006, FR-013).

## Phase 3: US4 — Cards, modals, dropdowns and dividers are fully annotated (P2)

- [x] T004 [P] [US4] Annotate `card/index.html` and `divider.html`, including a `@slot:name` for every named slot each renders (`card`: `badges`, `actions`, `footer`, `footer_end` and any other; `divider`: `label`) (FR-009).
- [x] T005 [P] [US4] Annotate `dropdown/index.html`, including `@slot:button` and any other named slot it renders (FR-009).
- [x] T006 [US4] Annotate `modal.html`: its props, default slot, the named slots it forwards to its inner card (`actions`, `footer`, `footer_end`; not `badges`). `title` and `icon` are neither props nor slots on `modal`: they reach the inner card through `attrs`, and its `@description` says so, and a `@trigger` saying how another element opens it (FR-009, FR-010). Trim the `{# … #}` banner where annotations now say the same thing.

## Phase 4: US5 — Navigation and avatar components are fully annotated (P2)

- [x] T007 [P] [US5] Annotate `breadcrumbs/index.html` and `breadcrumbs/item.html`, each `@description` saying how it relates to the other (FR-011).
- [x] T008 [P] [US5] Annotate `dock/index.html` and `dock/item.html`, same relationship rule (FR-011).
- [x] T009 [P] [US5] Annotate `avatar/index.html` and `avatar/group.html`. `size_options` and `space_options` are documented as they behave today and are not renamed or removed (FR-011, FR-014).

## Phase 5: US6 — Mockup components are fully annotated (P3)

- [x] T010 [P] [US6] Annotate `mockup/browser.html`, `mockup/window.html` and `mockup/phone.html` (FR-012).
- [x] T011 [P] [US6] Annotate `mockup/code/index.html` and `mockup/code/line.html` (FR-012).

**Checkpoint**: `uv run python manage.py cotton_lint --warnings-as-errors` exits 0 with `21/21` components free of errors and warnings (SC-001).

## Phase 6: US7 — The suite catches the documentation the linter does not check (P2)

- [x] T012 [US7] Write `tests/test_gallery_annotations.py` rule tests against scratch sources first (red): no `@description`, two `@description`s, `{{ slot }}` rendered with no default `@slot`, a `@slot:name` alone not satisfying the default slot, no `{{ slot }}` needing no `@slot`, a `{#` that does not close on its line (failure names the line). Then implement the three rule helpers to green.
- [x] T013 [US7] Add the catalog-wide tests, parametrised by template path, applying the three rules to every template under the package's `cotton/` directory; add both new modules, `tests/test_gallery_annotations.py` and `tests/test_gallery_lint.py`, to `[tool.forge.conformance] non-mirror-paths` in `pyproject.toml` (FR-015, FR-016, FR-017, SC-004).

## Phase 7: US1 — The test suite fails when a component breaks the gallery lint (P1)

- [x] T014 [US1] Write `tests/test_gallery_lint.py` tests against scratch sources first (red): an undocumented `<c-vars>` name fails with component, line, rule and message; a call to a component that does not exist fails; a hints-only template passes; a template added to a scratch `cotton/` directory is discovered. Scratch sources are linted through `lint_catalog`. Then implement discovery (`scan` + `CatalogConfig`) and the blocking-findings filter to green (FR-001–FR-004).
- [x] T015 [US1] Add the catalog-wide test parametrised by component path, asserting no errors or warnings, with every blocking finding listed in the failure message. Every case reads its report from one module-level `lint_catalog` call over the whole catalog, never `lint_component` per path. Confirm the suite prints no gallery start-up notice (FR-001, FR-003, FR-005, SC-002, SC-003).

## Phase 8: US8 — Contributors can find how to run the gallery and the linter (P2)

- [x] T016 [US8] Write `CONTRIBUTING.md`: install (`uv sync`), start the gallery and its address, run the linter directly, run the suite, which findings fail and which do not, a link to the gallery's annotation reference, and the rule that a component is not done until it carries its annotations and the suite passes (FR-018).
- [x] T017 [US8] Link `CONTRIBUTING.md` from the README and add the CHANGELOG `[Unreleased]` entry: every component is documented in the gallery, and the test suite enforces it (FR-019, FR-020).

## Dependencies

- Phases 1–5 touch disjoint templates and may run in any order; they are built as two batches (US3+US2, then US4+US5+US6).
- Phases 6 and 7 require Phases 1–5: their catalog-wide tests are green only once every template is annotated.
- Phase 7 starts after Phase 6 has landed; both are built in one batch, in order.
- Phase 8 describes the checks from Phases 6 and 7.
