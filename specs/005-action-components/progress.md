# Progress: Action components

## 2026-09-27T08:30Z · Plan

Did: branch cut from origin/main 73a4826. Verify green on the base (conformance, docs, lint, typecheck, 4s test run, build). Probed daisyUI 5.7.46 in Chromium for the popover dropdown, the FAB and the swap. Wrote plan.md, research.md, tasks.md, decisions D1–D5 and the ledger.
Next: design review, then batch 1 (US1 button, US2 modal, US3 dropdown).
Watch: README, CHANGELOG and the template tag module overlap with the open navigation and layout pull requests (D1). The modal's gallery entry cannot open from its trigger in gallery 1.0.0 (D3).

## 2026-09-27T09:00Z · Design review

Did: one design reviewer, three lenses. One high finding (a component's `class` leaking onto the trigger it draws) and six low or medium, all verified and applied as plan and task edits (D6, D7). Receipts green.
Next: batch 1 (US1 button, US2 modal, US3 dropdown).
Watch: SPEC-002: T001 must update the dropdown test's expected trigger markup in the same task.

## 2026-09-27T09:10Z · Implementer US1 · T001

Did: rewrote `button.html`'s class list — `variant` and `size` (now `xs`–`xl`) validated
through `{% variation %}`, one class per style boolean (`outline`, `dash`, `soft`, `ghost`,
`link`), behaviour boolean (`active`) and modifier boolean (`wide`, `block`, `square`,
`circle`), `class` merged last. Removed `inline-flex items-center justify-*`, `align`,
`reverse`, `full` and `condition`. Every declared name (including the still-present `href`,
`text`, `icon`) now has an empty default (D6). Rewrote `tests/test_button.py` to the new
contract (D2) and updated the one expected-markup string in
`tests/test_dropdown.py::TestDropdownTrigger::test_extra_attributes_configure_the_default_inner_button`
to the button's new classes.
Verified: `uv run pytest tests/test_button.py tests/test_dropdown.py -q` → 30 passed.
`uv run python manage.py cotton_lint --warnings-as-errors` → button 0 errors/0 warnings (exit 0).
`uv run pytest tests/test_gallery_lint.py -k button -q` → 1 passed. `uv run pytest
tests/test_declared_attributes.py -q` → 26 passed.
Next: T002 (element and states: href/button toggle, disabled, icon `aria-hidden`).
Watch: `href`, `disabled` element/state logic still to land in T002 per the task split.

## 2026-09-27T09:20Z · Implementer US1 · T002

Did: split `button.html` into an explicit `{% if href %}<a>{% else %}<button>{% endif %}`
pair (FR-009). A link carries `href`, `btn-disabled`, `aria-disabled="true"`, `role="button"`
and `tabindex="-1"` when `disabled`, with no native `disabled` attribute; a button carries the
native `disabled` attribute. The icon is now `<c-icon aria-hidden="true">`, decorative by
default; an icon-only button's accessible name comes from the caller's `aria-label` (FR-010).
Added `TestButtonElement` to `tests/test_button.py` for scenarios 2-5.
Verified: `uv run pytest tests/test_button.py tests/test_dropdown.py
tests/test_declared_attributes.py -q` → 61 passed. `uv run python manage.py cotton_lint
--warnings-as-errors` → button 0 errors/0 warnings (exit 0). `uv run pytest
tests/test_gallery_lint.py -k button -q` → 1 passed.
Next: T003 (gallery annotations for button, CHANGELOG).
Watch: the two branches duplicate the class-list construction — Django has no built-in
capture-to-variable tag and the codebase has no existing pattern for it, so this mirrors
plan.md's own two-branch design rather than introducing a new abstraction for two callers.

## 2026-09-27T09:30Z · Implementer US1 · T003

Did: reordered `button.html`'s `@prop` annotations to match `<c-vars>` declaration order,
added an example (`Save`) to the default `@slot`, and extended `@description` to name the
`aria-label` an icon-only button needs. Added `TestButtonGalleryAnnotations` to
`tests/test_button.py`, reading the template's annotations through the gallery's own
`AnnotationParser`: `variant` and `size` are `select` with the full daisyUI list, every style/
behaviour/modifier boolean has its own `@prop`, the default slot's example is `Save`, and the
description mentions `aria-label`. Added the button's `CHANGELOG.md` `Changed` entry (every
removed/renamed attribute and its replacement) — no README change needed, since `button` was
already listed.
Verified: `uv run pytest tests/test_button.py tests/test_dropdown.py
tests/test_declared_attributes.py tests/test_gallery_lint.py tests/test_gallery_annotations.py
-q` → 216 passed. `uv run python manage.py cotton_lint --warnings-as-errors` → button 0
errors/0 warnings (exit 0).
Next: T004 (US2, modal structure).
Watch: US1 (button) done-check satisfied — every acceptance scenario the tests can cover (1-6)
has a test that fails when the behaviour is removed; scenario 7 (gallery, in-browser) is T013's.

## 2026-09-27T09:45Z · Implementer US2 · T004

Did: rewrote `modal.html`'s structure (FR-012, FR-014, FR-016): a `<dialog>` with the
caller's `id`, `placement` (top/middle/bottom/start/end) validated through `{% variation %}`,
`class` merged and attributes spread on the dialog; a plain `modal-box` (no inner `<c-card>`)
holding the default slot and `content_class`; an `actions` slot rendered in a trailing
`modal-action` only when given; `open` rendering `<dialog open>`. Removed the inner card,
`size`, `position`, `icon`, `footer` and `footer_end`; kept the existing translatable
backdrop-close form unchanged. Every declared name has an empty default. `title` and
`closable` are deliberately not yet declared — T005 adds and reads them, so nothing here is
declared without being used (`tests/test_declared_attributes.py`). Rewrote `tests/test_modal.py`
under D2 for scenarios 1 (structure half), 2, 3, 6, an unknown placement, and a page context
carrying `title`, `actions` and `open` that does not leak in.
Verified: `uv run pytest tests/test_modal.py tests/test_declared_attributes.py
tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` → 181 passed. `uv run python
manage.py cotton_lint --warnings-as-errors` → 20/21 clean, 0 errors/0 warnings (exit 0).
Next: T005 (modal naming and closing: title heading, aria-labelledby, closable).
