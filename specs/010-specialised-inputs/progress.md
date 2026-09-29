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
