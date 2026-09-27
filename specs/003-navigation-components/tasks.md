# Tasks: Navigation components

**Input**: `specs/003-navigation-components/` — spec.md, plan.md, research.md, decisions.md

**Organization**: by user story, in build order (plan.md "Story order").

**Every story's done-check**: its acceptance scenarios each have a test that fails when the behaviour is removed (SC-001). Its templates pass `uv run python manage.py cotton_lint --warnings-as-errors` (SC-002). Its templates emit no `<script>` and no `on*=` attribute (SC-005). Its new test module is in `[tool.forge.conformance] non-mirror-paths`. Its README and CHANGELOG lines are written.

Tests render through the Cotton compiler as a caller's template would (`tests/test_link.py`'s `render` helper, or the `cotton_render_string` fixture in `tests/conftest.py`), never by rendering the component file directly, which skips `<c-vars>` extraction.

## Phase 1: US3 — Link and breadcrumbs (P1)

- [ ] T001 [US3] `link.html`: no `href` default (no `href` attribute emitted without one), `variant` validated through `variation` against daisyUI's eight link colours and typed `select[…]`, `hover`. Tests for scenarios 1–3 and an unknown variant adding no class, in `tests/test_link.py`. Change `test_default_href_falls_back_to_hash` under D4 (FR-001, FR-002, FR-015).
- [ ] T002 [US3] `breadcrumbs/index.html` and `breadcrumbs/item.html`: `text-sm` gone from the root, `aria-label` declared and overridable with the translated default `Breadcrumbs`, attributes and class on the item's `<li>`, a hrefless item rendered as `<span aria-current="page">`, the `daisy-cotton-breadcrumb-text` span removed. Tests for scenarios 4–6 (the `items` and slotted trails compared after whitespace normalisation) and a single-item trail, in `tests/test_breadcrumbs_href_attribute.py`. Change `TestTheItemTextSpan` and `test_href_class_and_attrs_still_land_where_they_did` under D4 (FR-006, FR-016, FR-017).
- [ ] T003 [US3] CHANGELOG `Changed` entries for the `link` and `breadcrumbs` breaking changes, each with what a host project writes to keep the old result (FR-010).

## Phase 2: US5 — Dock (P2)

- [ ] T004 [US5] `dock/index.html`: root is `<nav class="dock …">` with `size`, merged `class`, pass-through attributes, `aria-label` overridable with the translated default `Dock`, and no `bg-transparent backdrop-blur`. Tests for scenarios 1–3 in a new `tests/test_dock.py` (FR-006, FR-021).
- [ ] T005 [US5] `dock/item.html`: `dock-active`, `aria-current="page"` on the link only, `type="button"` on the button branch, `<c-icon … aria-hidden="true">`, label in `dock-label`, the toggle's `aria-label` only when `label` is given, the toggle's `role="button" tabindex="0"` removed (D9). Tests for scenarios 4–6, an icon-only item named by the caller's `aria-label`, and the toggle carrying no `tabindex` (FR-003, FR-005, FR-022).
- [ ] T006 [US5] CHANGELOG `Changed` entry for the dock's removed classes and new `<nav>` root (FR-010).

**Checkpoint**: batch 1 green. Full suite, `cotton_lint --warnings-as-errors`, pre-commit.

## Phase 3: US1 — Menu (P1)

- [ ] T007 [US1] `menu/index.html`: `menu`, `size`, `horizontal` (boolean or breakpoint), `paged`. Tests for scenarios 1–3 and 8 in a new `tests/test_menu.py` (FR-001, FR-011).
- [ ] T008 [US1] `menu/item.html`: link or `<button type="button">`, `active` (`menu-active`, and `aria-current="page"` on a link), `disabled` (`menu-disabled` on the `<li>`, `role="link" aria-disabled="true"` and no `href` or `tabindex` on a link, native `disabled` on a button), icon through `<c-icon … only>`, attributes on the `<li>`, `aria-label` on the inner control. Tests for scenarios 4–5, several active items each rendered as given, an icon-only item named by `aria-label` on its link, and an item `class` not reaching its icon (FR-003, FR-005, FR-012).
- [ ] T009 [US1] `menu/title.html` and `menu/submenu.html`: `menu-title` on a non-interactive `<li>`, submenus as `<details>`/`<summary>` that render open on `open` and nest two levels. Tests for scenarios 6–7 (FR-013).
- [ ] T010 [US1] Gallery: annotations for the four templates, the menu's default `@slot` example showing a title, an active link, a disabled item and an open two-level submenu. README lists `menu` and says pagination has no component and why. CHANGELOG `Added` (FR-007, FR-008, FR-009).

## Phase 4: US2 — Navbar (P1)

- [ ] T011 [US2] `navbar.html`: `<nav class="navbar …">` with `start`, `center`, `end` named slots each emitted only when given, default slot directly inside the root, merged `class`, `aria-label` overridable with the translated default `Main`. Tests for scenarios 1–5 in a new `tests/test_navbar.py`, and a `start` in the page context emitting no section (FR-006, FR-014).
- [ ] T012 [US2] Gallery annotations including `@slot:start`, `@slot:center`, `@slot:end` with example content, README and CHANGELOG `Added` (FR-007, FR-008, FR-009).

**Checkpoint**: batch 2 green.

## Phase 5: US4 — Tabs (P2)

- [ ] T013 [US4] `tabs/index.html`: `tabs-box`, `tabs-border`, `tabs-lift`, `size`, `placement` (`top`/`bottom`, typed `select`), `role="tablist"` unless `links`. Tests for scenarios 1–3 in a new `tests/test_tabs.py` (FR-018, D1).
- [ ] T014 [US4] `tabs/tab.html` link and button shapes: link with `tab tab-active` and `aria-current="page"`, disabled with `tab-disabled`, `role="link" aria-disabled="true"` and no `href`, button shape `<button type="button" role="tab">` with `aria-selected` and native `disabled`. Tests for scenarios 4, 5 and 7 (FR-005, FR-019).
- [ ] T015 [US4] `tabs/tab.html` radio shape: `<input type="radio" class="tab" name aria-label>` followed by its `tab-content` panel, `checked` on `active`, `disabled`. Tests for scenario 6, rendering a three-tab set, and a `name` in the page context not turning a button tab into a radio input (FR-019, FR-020).
- [ ] T016 [US4] Gallery annotations, the default `@slot` example a link set with one active and one disabled tab, README and CHANGELOG `Added` (FR-007, FR-008, FR-009).

## Phase 6: US6 — Steps (P3)

- [ ] T017 [US6] `steps/index.html` as `<ol class="steps …">` with `vertical` and `horizontal` (each a boolean or breakpoint), and `steps/step.html` with validated `variant`, `current` (`aria-current="step"`), `content` → `data-content`, icon in `step-icon` through `<c-icon>`. Tests for scenarios 1–6 in a new `tests/test_steps.py` (FR-003, FR-023, FR-024).
- [ ] T018 [US6] Gallery annotations, the default `@slot` example four steps (two primary, one current, one with custom content, one with an icon), README and CHANGELOG `Added` (FR-007, FR-008, FR-009).

## Phase 7: US7 — Megamenu (P3)

- [ ] T019 [US7] `megamenu/index.html`: required `id`, the small-screen toggle through `<c-button class="sm:hidden" type="button" popovertarget … only>` (a `<button>` even with `size`, `full` or a page-context `href` about), `<nav id popover class="megamenu max-sm:megamenu-vertical …">` with the `megamenu-active` span, `wide`, `full`, `size`, `aria-label` overridable with the translated default `Site`. Tests for scenarios 1, 2, 4 and 5 in a new `tests/test_megamenu.py` (FR-003, FR-006, FR-025, FR-026).
- [ ] T020 [US7] `megamenu/item.html`: `<button type="button" popovertarget="{megamenu}-{key}">` and its `<div id="{megamenu}-{key}" popover>` panel. Tests for scenario 3 with three items (each `popovertarget` equals its panel's `id`, and no id repeats in the rendered page) and for two megamenus with different ids on one page (FR-026).
- [ ] T021 [US7] Gallery annotations (description mentions daisyUI's ten-item limit and that `id` is set in the playground), the default `@slot` example three items holding menus, README and CHANGELOG `Added` (FR-007, FR-008, FR-009).

**Checkpoint**: batch 3 green.

## Phase 8: Verification at the walkthrough (orchestrator)

- [ ] T022 Run axe-core and the scripted keyboard walk against every gallery entry in the group on the running demo (research R7) and record the result in the pull request's test evidence (SC-004). Set the megamenu's `id` in the playground first. A radio-tab `aria-required-children` finding goes to Sam as D8 describes.

## Dependencies

- Phases 1–7 touch disjoint templates and test modules. They share `README.md`, `CHANGELOG.md` and `pyproject.toml`'s `non-mirror-paths`, so batches run one after another on one branch.
- Phase 3 before Phase 7: the megamenu's gallery example holds a `<c-menu>`.
- Phase 8 needs every story done and the demo running.

## Review fixes

- [ ] T023 Default to `""` in `<c-vars>` every name that decides which markup or state is emitted and that a page variable could supply: `active`, `disabled`, `href` on `menu.item`, `tabs.tab` and `dock.item`, `toggle` on `dock.item`, `links` on `tabs`, `current` and `content` on `steps.step`, `open` on `menu.submenu`, `href` on `link`. One page-context test per component (RVW-001).
- [ ] T024 Tests that fail when `only` is dropped from `menu.submenu`'s icon, and when the dock toggle's icon loses `aria-hidden="true" only` (RVW-002).
- [ ] T025 README count to thirty-two. CHANGELOG `breadcrumbs.item` bullet: linked items render their text directly in the `<a>` with no span, the current item's span has no class, and a project that styled `.daisy-cotton-breadcrumb-text` targets `.breadcrumbs li > a` and `.breadcrumbs li > span` or writes its own span in the item's slot. `tabs.tab`'s `text` annotation says a radio tab needs it for its name (RVW-003, RVW-004, review note).
