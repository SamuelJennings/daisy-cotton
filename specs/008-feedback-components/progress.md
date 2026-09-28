# Progress: Feedback components

## 2026-09-28T20:40Z · Plan

Did: branch cut from origin/main fe694a4; verify green on that commit. Re-read the spec against FS-001 to FS-007, which landed after it: no contradiction (D1). Read daisyUI 5.7.46's CSS and class reference for the seven components, and checked that Alpine attributes and a translated name reach `<c-button>` through django-cotton 2.7.2. Wrote plan.md, research.md, tasks.md, decisions D1–D4 and the ledger.
Next: design review, then batch 1 (US1 alert, US2 loading, US3 tooltip).
Watch: a progress bound to `0` must not turn indeterminate (research R5).

## 2026-09-28T21:10Z · Design review

Did: one reviewer, three lenses: approve, 0 critical, 0 high, 2 medium, 4 low. All six applied to plan.md and tasks.md (D5).
Next: US1 alert, US2 loading, US3 tooltip.
Watch: the toast is `position: fixed` inside a gallery preview frame; check it at the browser check.

## 2026-09-28T20:26:02Z · Implementer US1 · T001

Did: rewrote `alert.html` on the attribute vocabulary — `variant` validated through `variation`, `horizontal`/`vertical` through `responsive`, a caller `role` replacing the `alert` default, the icon and dismiss control drawn by `<c-icon>`/`<c-button>`, the dismiss control's "Dismiss" name translatable and its glyph hidden, `delay` passed through `add:0`. Wrote `tests/test_alert.py` (scenarios 1–7 in markup, unknown-value and page-context-leak cases) and started `tests/test_feedback_no_script.py` with a dismissible alert.
Verified: `uv run pytest tests/test_alert.py tests/test_feedback_no_script.py tests/test_declared_attributes.py tests/test_render_all.py tests/test_gallery_annotations.py tests/test_class_attribute_merge.py tests/test_gallery_lint.py -q` — 526 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 0 errors, 0 warnings. `uv run ruff check`/`ruff format` clean on the new test files.
Next: T002 (gallery annotations already written in this task; README/CHANGELOG remain).
Watch: none.
