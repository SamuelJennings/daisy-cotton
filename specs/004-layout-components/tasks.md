# Tasks: Layout components

**Input**: `specs/004-layout-components/` — spec.md, plan.md, research.md, decisions.md

**Organization**: by user story, in build order (plan.md "Story order").

**Every story's done-check**: its acceptance scenarios each have a test that fails when the behaviour is removed (SC-001). An unknown value for each fixed-value prop it adds emits no modifier class and does not raise (FR-004). Its templates pass `uv run python manage.py cotton_lint --warnings-as-errors` (SC-002). Its templates emit no `<script>` and no `on*=` attribute (FR-005) and no literal Tailwind colour (SC-005). Every component it touches merges `class` and passes an extra attribute to its root (FR-003). Its new test module is in `[tool.forge.conformance] non-mirror-paths`. Its README and CHANGELOG lines are written.

Tests render through the Cotton compiler as a caller's template would (the `cotton_render_string_soup` fixture in `tests/conftest.py`), never by rendering the component file directly.

## Phase 1: US3 — Divider brought to the bar (P1)

- [ ] T001 [US3] `divider.html`: `horizontal` → `divider-horizontal`, `vertical` → `divider-vertical`, each bare or with a breakpoint through `responsive`; `variant` validated through `variation` against daisyUI's eight divider colours; `placement` validated against `start,end`; `text` declared and rendered before the slot; the undeclared `label` slot removed; `position` removed. Tests for scenarios 1–3 and unknown `variant`/`placement` values in a new `tests/test_divider.py` (FR-004, FR-015).
- [ ] T002 [US3] `divider.html` roles: unlabelled (no `text`, empty or whitespace-only slot) → `role="separator"`, plus `aria-orientation="vertical"` when `horizontal` is bare; labelled → no default role; a caller's `role` replaces the default and appears once in either case (`role` declared). Tests for scenarios 4–5 and the caller-`role` edge case, asserting a single `role` attribute through `HTMLParser` as `tests/test_class_attribute_merge.py` does (FR-016, D5).
- [ ] T003 [US3] Gallery annotations for `divider` (`placement` and `variant` as `select[…]`, `horizontal`/`vertical` descriptions naming the breakpoint form, `@slot OR — …`). README unchanged in count. CHANGELOG `Changed`: `vertical` now emits `divider-vertical` (write `horizontal` for the old result), `position` renamed `placement`, the `label` slot removed in favour of `text` or the default slot, and the separator role (FR-007, FR-009).

## Phase 2: US8 — Mockups brought to the bar (P3)

- [ ] T004 [US8] `mockup/browser.html`, `mockup/phone.html`, `mockup/window.html`: `class` declared and merged, extra attributes on the root, `mockup.phone` display `bg-base-100 text-base-content` with `text-white`, `bg-neutral-900`, `grid` and `place-content-center` gone, the camera `aria-hidden="true"`, `mockup.window`'s `grid place-content-center h-80` wrapper gone, `mockup.browser`'s `url` in the toolbar and not inside anything `aria-hidden`. Tests for scenarios 1–4 in a new `tests/test_mockup.py` (FR-003, FR-023).
- [ ] T005 [US8] `mockup/code/index.html` and `mockup/code/line.html`: `class` and attributes on both roots, `tabindex="0"` on the code block, `data-prefix` only when `prefix` is given. Tests for scenarios 5–6 in `tests/test_mockup_code.py`. Change `test_the_prompt_defaults_to_a_shell_dollar` and `test_the_prompt_can_be_emptied` under D2, and update that module's docstring (FR-024).
- [ ] T006 [US8] Gallery annotations for the five mockup templates (`mockup.code`'s example a `$` line and an unprefixed output line). CHANGELOG `Changed`: `mockup.code.line` has no default prefix (write `prefix="$"`), `mockup.phone` display colours and centring, `mockup.window`'s wrapper, and `class`/attribute support on every mockup (FR-007, FR-009).

**Checkpoint**: batch 1 green. Full suite, `cotton_lint --warnings-as-errors`, pre-commit.

## Phase 3: US4 — Joined controls (P2)

- [ ] T007 [US4] `join.html`: `join`, `vertical` and `horizontal` through `responsive`, `role="group"` unless the caller gives `role`, `aria-label` passing through, children rendered with no wrapper. Tests for scenarios 1–3 (a join of three `<c-button class="join-item">`, and of an input and a button) and the caller-`role` edge case in a new `tests/test_join.py` (FR-017, D5).
- [ ] T008 [US4] Gallery annotations (`@slot` three `join-item` buttons), README lists `join`, CHANGELOG `Added` (FR-007, FR-008, FR-009).

## Phase 4: US2 — Page footer (P1)

- [ ] T009 [US2] `footer/index.html`: `<footer class="footer …">`, `horizontal` and `vertical` through `responsive`, `placement` validated against `center`. Tests for scenarios 1, 2 and 4, and a footer with no `footer.nav`, in a new `tests/test_footer.py` (FR-013).
- [ ] T010 [US2] `footer/nav.html`: `<nav aria-label="{title}">` with `<span class="footer-title">` then the slot; no `aria-label` and no title span without `title`. Tests for scenario 3, with two groups each named by its own title (FR-014, D6).
- [ ] T011 [US2] Gallery annotations for both templates (the footer's `@slot` a copyright line and two `footer.nav` groups), README lists `footer` + `footer.nav`, CHANGELOG `Added` (FR-007, FR-008, FR-009).

## Phase 5: US1 — Page with a sidebar drawer (P1)

- [ ] T012 [US1] `drawer/index.html`: root `drawer`, `drawer-toggle` checkbox with the drawer's `id`, page in `drawer-content`, `drawer-side` holding the `drawer-overlay` label for the same id before the `side` slot, `id` never on the root, `open` through `responsive` (`drawer-open`), `placement` validated against `end`. Tests for scenarios 1, 3 and 4, and two drawers on one page each wired to its own id, in a new `tests/test_drawer.py` (FR-010, FR-011).
- [ ] T013 [US1] Accessible names: the toggle's and the overlay's `aria-label` written through `{% trans %}`. Tests that each is present and non-empty in the rendered drawer, and that both strings sit inside `{% trans %}` in the template source (FR-006, FR-012).
- [ ] T014 [US1] `drawer/button.html`: `<label for="{drawer}" class="btn drawer-button …">` with the slot, no `role` or `tabindex`. Tests for scenario 2's markup (the label's `for` equals the drawer's checkbox id) and the label being a `<label>` inside `.drawer-content` in the gallery example (FR-012, D4).
- [ ] T015 [US1] Gallery annotations: `id` and `drawer` `required`, `@trigger` naming `drawer.button`, the drawer's `@slot` the page described in plan.md "Gallery entries" (opener for `demo-drawer`, the responsive divider pattern, `<c-join vertical horizontal="sm">`, `<c-footer vertical horizontal="sm">` with two groups), `@slot:side` a sidebar list, the description telling the viewer to set `id` to `demo-drawer`. README lists `drawer` + `drawer.button`, CHANGELOG `Added` (FR-007, FR-008, FR-009, D8).

**Checkpoint**: batch 2 green.

## Phase 6: US5 — Indicator on a corner (P2)

- [ ] T016 [US5] `indicator/index.html` and `indicator/item.html`: `items` slot before the default slot whatever order the caller wrote them, `indicator-item` with each space-separated `placement` value validated on its own, an indicator with no items. Tests for scenarios 1–3 and an unknown placement word in a new `tests/test_indicator.py` (FR-018, FR-019, D7).
- [ ] T017 [US5] Gallery annotations (`placement` `select[…]` per D7; the indicator's `@slot` a button and `@slot:items` an item whose count has a visually hidden text alternative, scenario 4), README lists `indicator` + `indicator.item`, CHANGELOG `Added` (FR-007, FR-008, FR-009).

## Phase 7: US6 — Hero (P2)

- [ ] T018 [US6] `hero.html`: `hero` root, slot inside `hero-content`, `overlay` adding an `aria-hidden="true"` `hero-overlay` before the content, `style` reaching the root unchanged. Tests for scenarios 1–3 in a new `tests/test_hero.py`. Gallery annotations, README lists `hero` and rewords the scope note per FR-009, CHANGELOG `Added` (FR-007, FR-009, FR-020).

## Phase 8: US7 — Mask and stack (P3)

- [ ] T019 [US7] `mask.html`: `shape` validated against daisyUI's fourteen shapes, `half` against `1,2`, `<img>` with `src` and an always-present `alt` (empty by default), a `<div>` around the slot without `src`, a mask with no `shape` carrying only `mask`. `stack.html`: `stack` and `placement` validated against `top,bottom,start,end`, children untouched. Tests for scenarios 1–5 and the unknown-value and no-shape edge cases in a new `tests/test_mask_stack.py` (FR-021, FR-022).
- [ ] T020 [US7] Gallery annotations (`shape` `select[…]` and `required`), README lists `mask` and `stack`, CHANGELOG `Added` (FR-007, FR-008, FR-009).

**Checkpoint**: batch 3 green.

## Phase 9: Verification at the walkthrough (orchestrator)

- [ ] T021 Run axe-core and the scripted keyboard walk against every gallery entry this feature touches on the running demo (research R8) and record the result in the pull request's test evidence (SC-004). Set the drawer's `id` to `demo-drawer` first.

## Dependencies

- Phases 1–8 touch disjoint templates and test modules. They share `README.md`, `CHANGELOG.md` and `pyproject.toml`'s `non-mirror-paths`, so batches run one after another on one branch.
- Phase 5 after Phases 1, 3 and 4: the drawer's gallery example composes `divider`, `join` and `footer`.
- Phase 9 needs every story done and the demo running.
