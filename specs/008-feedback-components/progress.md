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

## 2026-09-28T20:27:31Z · Implementer US1 · T002

Did: gallery annotations for the alert (written together with the T001 rewrite: `horizontal`/`vertical` as breakpoint selects, `role` typed text with default `alert`, the description naming the Alpine.js requirement, the warning against `delay` on errors and anything the reader must act on, and the toast entry). Rewrote the README's Alpine paragraph to describe the alert's full current attribute set. Added a CHANGELOG `### Changed` bullet for the alert listing each change from plan "Alert".
Verified: `uv run python manage.py cotton_lint --warnings-as-errors` — 55/63 clean, 0 errors, 0 warnings. `uv run pytest tests/test_gallery_annotations.py tests/test_gallery_lint.py -q` — 350 passed.
Next: US1 complete; US2 loading follows.
Watch: none.

## 2026-09-28T20:34:10Z · Implementer US2 · T003

Did: wrote `loading.html` — a `<span>` carrying `loading`, `role="status"`, the six animation booleans each mapped to their `loading-*` class with none emitted when none given, `size` validated through `variation`, `class` merged, `aria-label` from `label` or the translatable "Loading". Wrote `tests/test_loading.py` (scenarios 1–5, each animation's class, two animations together, an unknown `size`, the translation test, a loading indicator inside a `<c-button>` slot, and a page context carrying `label`, `size` and `dots` that does not leak in). Extended `tests/test_feedback_no_script.py` with a loading caller string. Added `tests/test_loading.py` to `[tool.forge.conformance] non-mirror-paths`.
Verified: `uv run pytest tests/test_loading.py tests/test_feedback_no_script.py tests/test_declared_attributes.py tests/test_render_all.py tests/test_gallery_annotations.py tests/test_class_attribute_merge.py tests/test_gallery_lint.py -q` — 527 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 56/64 clean, 0 errors, 0 warnings.
Next: T004 (mockup.browser composition, README, CHANGELOG).
Watch: none.

## 2026-09-28T20:36:46Z · Implementer US2 · T004

Did: gallery annotations for `loading` were already complete in T003 (description naming the colour-via-class convention, the always-given name defaulting to "Loading", and the `mockup.browser` entry). Added an "Add to cart" `<c-button text="Add to cart">` holding `<c-loading size="sm" />` to the `mockup.browser` default `@slot` example, after the existing hover 3D card, without removing anything; sanity-rendered the slot's example markup through the Cotton compiler to confirm it produces valid output. README component count Sixty-three → Sixty-four with `loading` listed alphabetically between `list` and `mask`. CHANGELOG `### Added` bullet for `loading`.
Verified: `uv run pytest tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_render_all.py tests/test_loading.py tests/test_feedback_no_script.py -q` — 451 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 56/64 clean, 0 errors, 0 warnings.
Next: US2 complete; US3 tooltip follows.
Watch: none.
