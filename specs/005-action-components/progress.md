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
