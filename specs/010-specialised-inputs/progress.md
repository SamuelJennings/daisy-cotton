# Progress: Specialised inputs

## 2026-09-29T10:24Z · Plan

Did: branch cut from origin/main cdce18f; verify green on that commit. Re-read the spec against FS-001 to FS-009, which landed after it: FS-009's `form.` namespace ruling applies, the rest changes nothing (D1). Read daisyUI 5.7.46's CSS for the filter, OTP, rating and calendar, which decides where each hidden name can sit (research R2, D3). Wrote plan.md, research.md, tasks.md, decisions D1–D4 and the ledger.
Next: design review, then batch 1 (US1 filter, US2 calendar).
Watch: the OTP's hidden name must not be a `<span>`, and nothing but items may sit inside the rating.

## 2026-09-29T10:34Z · Implementer US1 · T001

Did: `filter_options(options, value)` in `daisy_cotton/templatetags/daisy_cotton.py`, tests first in `TestFilterOptions` (import failed first, the right reason). Plain values are their own label, two-entry lists and tuples split, `checked` compares `str()` of both sides, `None` and `""` check nothing, empty, `None` and non-iterable options give `[]`.
Verified: `uv run pytest tests/test_templatetags/test_daisy_cotton.py -q` 32 passed; pre-commit on the two files passed.
Next: T002, `form/filter.html` and its tests.
Watch: a bare string passed as `options` iterates by character, as any iterable would.

## 2026-09-29T10:37Z · Implementer US1 · T002

Did: `form/filter.html` and `tests/test_filter.py` (38 tests, tests first: red on the missing component), plus `tests/test_specialised_inputs.py` started with the filter's no-script and page-context rows; both modules added to `[tool.forge.conformance] non-mirror-paths`. Wrote the template's annotations here rather than in T003, because the existing gallery annotation and lint tests fail on an unannotated template.
Verified: `uv run pytest tests/test_filter.py tests/test_specialised_inputs.py -q` 41 passed; twelve mutations of the template each failed a new test; `cotton_lint --warnings-as-errors` 0 errors 0 warnings; the gallery, render-all, declared-attribute, palette, link and demo tests 755 passed, 17 skipped (pre-existing skips).
Next: T003, fieldset composition row, README and CHANGELOG.
Watch: the rendered reset's `aria-labelledby` target is a hidden span, so the reset's name does not depend on its position in the wrapper.

## 2026-09-29T10:38Z · Implementer US1 · T003

Did: the fieldset composition gains the filter row (a nested fieldset with a legend holding four filters: one named by the legend with nothing chosen, a labelled one with three value and label options and one chosen, a primary small and an accent large one) and its `@slot` description names it. README count is now Seventy-nine with `form.filter` in the list, and the scope section says the validator has no component. CHANGELOG `Added` bullet. Tests first in `tests/test_specialised_inputs.py::TestFieldsetCompositionFilters`: they rendered the composition and failed on it holding no filter. The filter's own annotations were written in T002.
Verified: the composition, fieldset, filter, gallery annotation and lint tests 498 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: full verify, then the completion report.
Watch: `docs/ROADMAP.md` line 110 lists which data-input components exist and is outside this story's files.

## 2026-09-29T10:41Z · Implementer US2 · T004

Did: `count_range(value, default)` in `daisy_cotton/templatetags/daisy_cotton.py`, tests first in `TestCountRange` (import failed first, the right reason). An integer or numeric string above zero gives that many entries; zero, a negative, a float, a bool, a non-number and an empty value give `default`.
Verified: `uv run pytest tests/test_templatetags/test_daisy_cotton.py -q` 47 passed; changing `> 0` to `>= 0` failed nine of the new tests; pre-commit on the two files passed.
Next: T005, `form/calendar.html` and its tests.
Watch: the tag is shared with the OTP (US3), which passes `length` and 6.

## 2026-09-29T10:42Z · Implementer US2 · T005

Did: `form/calendar.html` and `tests/test_calendar.py` (28 tests, tests first: red on the missing component), plus the calendar's rows in `tests/test_specialised_inputs.py` (no script or handler, page context); `tests/test_calendar.py` added to `[tool.forge.conformance] non-mirror-paths`. Wrote the template's annotations here rather than in T006, because the existing gallery annotation and lint tests fail on an unannotated template, as in US1. The root is `<calendar-date>` or `<calendar-range>` with `cally`, `months` written on it above one, one `<calendar-month>` per month with `offset` from the second, and `previous` and `next` span slots each holding an `aria-hidden` icon and a `sr-only` name.
Verified: `uv run pytest tests/test_calendar.py tests/test_specialised_inputs.py -q` 40 passed; fourteen mutations of the template each failed a new test; `cotton_lint --warnings-as-errors` 0 errors 0 warnings; the gallery, render-all, declared-attribute, palette, link, demo and class-merge tests 768 passed, 17 skipped (pre-existing skips).
Next: T006, the demo loads Cally, the fieldset composition row, README and CHANGELOG.
Watch: the page-context rule cannot catch a leak into `range` or `months`, since neither value is ever written into the output as text; the icon and class names are covered.

## 2026-09-29T10:44Z · Implementer US2 · T006

Did: the demo's preview-document head loads `cally@0.9.2` as a module from unpkg, inside the preview-document branch, with the split closing tag the other scripts use. The fieldset composition gains a nested "Delivery date" fieldset holding a single date calendar with a value, min and max and a two-month range calendar, both passing bootstrap-icons classes for the paging icons, and its `@slot` description names it. README: count is Eighty, `form.calendar` is in the list, the scope section says the calendar needs Cally, and a Calendar section shows the script tag, an example and the change-event script copying the date into a hidden input. CHANGELOG `Added` bullet. The calendar's annotations were written in T005. Tests first in `tests/test_specialised_inputs.py` (`TestFieldsetCompositionCalendars`, `TestDemoHeadLoadsCally`): red on the composition holding no calendar and the head loading no Cally.
Verified: the composition, calendar, fieldset, gallery annotation, lint, render-all, demo, link and palette tests 745 passed, 17 skipped (pre-existing skips); five mutations of the row and head each failed a new test; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: full verify, then the completion report.
Watch: the README's range example (`start/end` joined by a slash) and the `change` event target are from Cally's documented behaviour, unchecked in a browser; the walkthrough's browser check covers them (research R8).

## 2026-09-29T10:47Z · Implementer US3 · T007

Did: `form/otp.html` and `tests/test_otp.py` (29 tests, tests first: red on the missing component), plus the OTP's rows in `tests/test_specialised_inputs.py` (no script or handler, page context); `tests/test_otp.py` added to `[tool.forge.conformance] non-mirror-paths`. Wrote the template's annotations here rather than in T008, because the existing gallery annotation and lint tests fail on an unannotated template, as in US1 and US2. The label carries `otp`, `otp-{variant}`, `otp-{size}`, `otp-joined` and `class`; the boxes come first, then the input (`maxlength`, `pattern`, `inputmode`, `autocomplete`, `input_class`, everything else through `attrs`), then a `<small class="sr-only">` name. Boxes come from `count_range`.
Verified: `uv run pytest tests/test_otp.py tests/test_specialised_inputs.py -q` 52 passed; fourteen mutations of the template each failed a new test; `cotton_lint --warnings-as-errors` 0 errors 0 warnings; the gallery, render-all, declared-attribute, palette, link, demo and class-merge tests 777 passed, 17 skipped (pre-existing skips).
Next: T008, the fieldset composition row, README and CHANGELOG.
Watch: the hidden name is a `<small>`, never a `<span>`, since daisyUI counts span children as boxes.

## 2026-09-29T10:48Z · Implementer US3 · T008

Did: the fieldset composition gains a nested "Two-step verification" fieldset holding a labelled six-digit OTP, a joined four-digit OTP and a disabled OTP, each with its own `name` and hidden name, and its `@slot` description names it. README count is Eighty-one with `form.otp` in the list. CHANGELOG `Added` bullet. The OTP's annotations were written in T007. Tests first in `tests/test_specialised_inputs.py::TestFieldsetCompositionOtps`: red on the composition holding no OTP. No page under `docs/` describes the OTP or the fieldset composition, so none changed.
Verified: the composition, OTP, fieldset, gallery annotation, lint and render-all tests 605 passed; five mutations of the row each failed a new test; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: full verify, then the completion report.
Watch: the OTP's focus indicator, digit display and submission are browser behaviour (US3-6) and covered by the walkthrough's browser check, not by these tests.

## 2026-09-29T10:52Z · Implementer US4 · T009

Did: `rating_items(max, half, value)` in `daisy_cotton/templatetags/daisy_cotton.py` and `TestRatingItems` (35 cases) in `tests/test_templatetags/test_daisy_cotton.py`, tests first: red on the missing import. Whole values are ints, half values strings, `half` is 1 or 2 on a half rating and 0 otherwise, `max` reuses `count_range` with a default of five, and `value` is compared as a number so `7`, `"7"` and `"7.0"` match while empty, non-numeric, out-of-range and off-step values check nothing.
Verified: `uv run pytest tests/test_templatetags/test_daisy_cotton.py -q` 82 passed; five mutations of the tag each failed a new test; `ruff check` clean.
Next: T010, `form/rating.html` and `tests/test_rating.py`.
Watch: the tag's first parameter is named `max` to match the plan's signature, with a `noqa: A002` for the builtin shadow.

## 2026-09-29T10:54Z · Implementer US4 · T010

Did: `form/rating.html` and `tests/test_rating.py` (73 tests, tests first: red on the missing template), plus the rating's two rows (interactive and read-only caller strings, page-context leak) in `tests/test_specialised_inputs.py`; `tests/test_rating.py` added to `[tool.forge.conformance] non-mirror-paths`. Wrote the template's annotations here rather than in T011, because the gallery annotation and lint tests fail on an unannotated template, as in US1 to US3. The wrapper carries `rating`, `rating-{size}`, `rating-half`, `class` and `attrs`; interactive it is a `radiogroup` named by `label`, read-only it is `role="img"` named "value out of max". Items are radios (or `<div>`s) carrying `mask`, `mask-{shape}`, `mask-half-{1,2}` and `bg-{variant}`. Radio names bind the item (`count counter=item.value`, `with step=item.value`). The read-only total is the last item's value so a `max` that is not a number reads as five.
Verified: `uv run pytest tests/test_rating.py tests/test_specialised_inputs.py -q` 106 passed; fifteen mutations of the template each failed a new test; gallery, lint, render-all, declared-attribute and fieldset tests 749 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T011, the fieldset composition row, README and CHANGELOG.
Watch: nothing but items sits inside `.rating`, so the group name is `aria-label` on the wrapper. Focus indicator and keyboard use (US4-8) are browser behaviour, covered by the walkthrough's browser check, not by these tests.
