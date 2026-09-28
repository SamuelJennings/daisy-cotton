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

## 2026-09-28T20:41:52Z · Implementer US3 · T005

Did: wrote `tooltip.html` — a wrapper carrying `tooltip` around the trigger slot, followed by a `tooltip-content` element with `role="tooltip"` holding `tip` or, when given, the `content` slot; `placement` split on whitespace and each word validated through `variation` (top, bottom, left, right, start, center, end); `variant` validated against the seven tooltip colours daisyUI defines (no `tooltip-neutral` exists, confirmed against the authoritative CSS); `open` adds `tooltip-open`; `id` declared so it lands on the content element only, never the wrapper, and never reaches it through `{{ attrs }}`; no `data-tip` anywhere; `class` merged, attributes spread. Wrote `tests/test_tooltip.py` (scenarios 1, 3–7 in markup, `tooltip-content` a direct child of the root, no `data-tip`, no `id` on the wrapper, every placement word and the two-word `bottom end` combination, an unknown placement word, each of the seven variants, `variant="neutral"` emitting nothing, `open`/no-`open`, the `content` slot replacing `tip`, `class`/attrs merge, and a page context carrying `tip`, `content`, `placement`, `variant` and `id` that does not leak in). Extended `tests/test_feedback_no_script.py` with a tooltip caller string exercising every attribute and the slot. Added `tests/test_tooltip.py` to `[tool.forge.conformance] non-mirror-paths`.
Verified: `uv run pytest tests/test_tooltip.py tests/test_feedback_no_script.py tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 575 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 57/65 clean, 0 errors, 0 warnings.
Next: T006 (gallery annotations already written in this task; `mockup.browser` composition, README, CHANGELOG remain).
Watch: none.

## 2026-09-28T20:43:44Z · Implementer US3 · T006

Did: refined the tooltip's `@description` to also carry the "wrap a focusable trigger" edge case (a plain-text trigger shows the hint on hover only), alongside the annotations already written in T005 — the `placement` select lists every single word and two-word combination as the dropdown's does, `@slot` shows an icon-only `<c-button circle icon aria-label>`, and `@slot:content` shows a `<kbd>` shortcut. Added a toolbar to `mockup.browser`'s default `@slot` example: an icon-only share `<c-button circle icon="bi bi-share" aria-label="Share" aria-describedby="product-share-hint">` inside `<c-tooltip id="product-share-hint" tip="Share this product">`, placed before the existing carousel; sanity-rendered the added fragment through the Cotton compiler to confirm valid output. README component count Sixty-four → Sixty-five with `tooltip` listed alphabetically after `timeline`. CHANGELOG `### Added` bullet for `tooltip`.
Verified: `uv run pytest tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_mockup.py tests/test_render_all.py tests/test_tooltip.py tests/test_feedback_no_script.py -q` — 486 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 57/65 clean, 0 errors, 0 warnings.
Next: US3 complete; US4 progress and radial progress follows.
Watch: none.

## 2026-09-28T20:52:35Z · Implementer US4 · T007

Did: wrote `progress.html` — a native `<progress>` carrying `progress`, `variant` validated through `variation` against the eight colours, `value` emitted only when it is not `None` and not empty (so `:value="0"` renders `value="0"` and a bound `None` renders no attribute), `max` defaulting to `100`, `aria-label` from `label`, `class` merged, attributes spread. Wrote `radial_progress.html` — a `<div>` carrying `radial-progress`, `role="progressbar"`, `style` beginning `--value:{{ value }};` with the caller's `style` appended, `aria-valuenow`/`aria-valuemin`/`aria-valuemax` (valuenow only with a value), `aria-label` from `label`, visible `<value>%` unless the slot (tested after stripping whitespace) has content, `value` required with an empty default so a page variable never leaks in (D3). Wrote `tests/test_progress.py` and `tests/test_radial_progress.py` (scenarios from tasks.md T007: no value by default, bound zero, bound `None`, each of the eight/none variant classes, an unknown variant, default and custom `max`, `label`, no-slot/whitespace-slot/non-empty-slot visible text, `aria-valuenow` only with a value, style escaping of `"` and `<`, caller `style` appended after `--value`, `class`/attrs merge, and a page context carrying each component's declared names that does not leak in). Extended `tests/test_feedback_no_script.py` with `progress` and `radial-progress` caller strings. Added both new test modules to `[tool.forge.conformance] non-mirror-paths` in `pyproject.toml`.
Verified: `uv run pytest tests/test_progress.py tests/test_radial_progress.py tests/test_feedback_no_script.py tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 626 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 59/67 clean, 0 errors, 0 warnings.
Next: T008 (gallery annotations already written in this task; `mockup.phone` composition, README, CHANGELOG remain).
Watch: none.

## 2026-09-28T21:00:55Z · Implementer US4 · T008

Did: gallery annotations for `progress` and `radial-progress` were already complete in T007 (each `@prop`, `radial-progress`'s `value` annotated `required`); reworded both descriptions to tell the developer to type `value`/`label` in the attributes field, since the bare previews carry only declared defaults (D5, as the FAB's does for its trigger). Added a mobile upload screen to `mockup.phone`'s default `@slot` example: four progress bars at several values and colours plus one left indeterminate, and three radial progresses — one sized with `[--size:…] [--thickness:…]`, one `text-primary`, one with a checkmark icon as custom centre content; sanity-rendered the composition through the Cotton compiler to confirm valid output. README component count Sixty-five → Sixty-seven with `progress` and `radial-progress` listed alphabetically after `navbar`. CHANGELOG `### Added` bullets for both.
Verified: `uv run pytest tests/test_progress.py tests/test_radial_progress.py tests/test_feedback_no_script.py tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_mockup.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 657 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 59/67 clean, 0 errors, 0 warnings.
Next: US4 complete; US5 toast follows.
Watch: `<c-radial-progress>`'s catalog entry is registered from its file stem `radial_progress`, so any future template that references it inside gallery-scanned markup (an `@slot` example or another component's annotation) must spell it `<c-radial_progress>` to satisfy the linter's unknown-component check — the hyphen form renders fine at runtime through Cotton's own resolution but is invisible to the catalog's known-tags set. `<c-hover_gallery>` in `card/index.html` is the existing instance of the same rule.

## 2026-09-28T21:08:02Z · Implementer US5 · T009

Did: wrote `toast.html` — a `<div>` carrying `toast` around the default slot, `placement` split on whitespace and each word validated through `variation` against `top,middle,bottom,start,center,end` (a single word or a two-word combination both work), no `role` and no `aria-live` on the wrapper, `class` merged, attributes spread. Wrote `tests/test_toast.py` (scenarios 1–3 in markup: two alerts rendered in order, each keeping its own role; an empty toast rendering an empty wrapper; every placement word and the two-word combinations `top center`/`bottom start`; an unknown placement word; no `role`/`aria-live` on the root; `class`/attrs merge; a page context carrying `placement` that does not leak in). Extended `tests/test_feedback_no_script.py` with a toast caller string holding two alerts and exercising `placement`, `dismissible` and `delay`. Added `tests/test_toast.py` to `[tool.forge.conformance] non-mirror-paths`.
Verified: `uv run pytest tests/test_toast.py tests/test_feedback_no_script.py tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 626 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — 60/68 clean, 0 errors, 0 warnings.
Next: T010 (gallery annotations already written in this task; README, CHANGELOG remain).
Watch: none.
