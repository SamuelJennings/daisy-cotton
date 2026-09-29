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
