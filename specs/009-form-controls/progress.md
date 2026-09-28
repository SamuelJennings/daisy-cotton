# Progress: Core form controls

## 2026-09-28T23:14Z · Plan

Did: branch cut from origin/main 6c8464a; verify green on that commit. Re-read the spec against FS-001 to FS-008, which landed after it: no contradiction (D1). Read daisyUI 5.7.46's CSS and class reference for the ten components, and checked through django-cotton 2.7.2 that bare boolean attributes, named slots, list-valued errors and declared defaults behave as the plan needs (research R4). Wrote plan.md, research.md, tasks.md, decisions D1–D4 and the ledger.
Next: design review, then batch 1 (US1 text input, US2 label and fieldset).
Watch: the wrapped input and select send `class` to the wrapper and everything else to the control.

## 2026-09-28T23:22Z · Design review

Did: one reviewer, three lenses: approve, 0 critical, 0 high, 3 medium, 3 low. All six applied to plan.md and tasks.md, with the review's notes (D5).
Next: US1 text input, US2 label and fieldset.

## 2026-09-28T23:30Z · Implementer US1 · T001

Did: added `daisy_cotton/templates/cotton/input.html` per plan "Text input": one `<input>` unwrapped, a wrapping `<label>` when `start` or `end` is filled, `variant`, `size` and `ghost` on whichever element carries the `input` class, every other attribute on the inner `<input>`. Wrote `tests/test_input.py` (13 tests, scenarios 1-6 plus the bare boolean, only-start, only-end, id/aria-describedby and unknown-variant/size cases) and started `tests/test_form_controls.py` with input's rows for the three shared rules. Added both new modules to `pyproject.toml`'s `non-mirror-paths`.
Verified: `uv run pytest tests/test_input.py -q` failed first with `TemplateDoesNotExist: cotton/input/index.html` before the template existed, then 13 passed once it did; `uv run pytest tests/test_form_controls.py -q` 4 passed, and a manual mutation (injecting `aria-invalid` into the unwrapped branch) turned the no-own-invalid-state row red before being reverted, confirming it is not a tautology; `uv run pytest tests/test_declared_attributes.py tests/test_gallery_annotations.py tests/test_semantic_palette.py tests/test_render_all.py -q` 535 passed with the new template included; `uv run python manage.py cotton_lint --warnings-as-errors` exit 0, 0 errors, 0 warnings, no findings for `input`; `uv run djlint daisy_cotton/templates/cotton/input.html --check` 0 files would be updated; `uv run ruff check tests/test_input.py tests/test_form_controls.py` clean after an unused import was auto-fixed.
Next: T002, gallery annotations, README and CHANGELOG for `input`.
Watch: the wrapped form never spreads `attrs` on the `<label>` — only the literal `class` string — so `id`, `aria-describedby` and the rest only ever reach the inner `<input>` by construction.

## 2026-09-28T23:31Z · Implementer US1 · T002

Did: `input`'s gallery annotations were already lint-clean from T001 (verified there: `cotton_lint --warnings-as-errors` exit 0, 0 errors, 0 warnings). Updated `README.md`'s component count Sixty-nine → Seventy and added `input` to the alphabetical list. Added a CHANGELOG `### Added` bullet for `input` naming its attributes (`variant`, `size`, `ghost`, `type` and its default), its `start`/`end` slots and the wrapped-form split.
Verified: documentation-only change, no test covers wording per `docs/contributing/standards/testing.md` §1; re-ran `uv run python manage.py cotton_lint --warnings-as-errors` (exit 0, 0 errors, 0 warnings, unaffected by doc edits) as a sanity check.
Next: US1 complete. US2 (label and fieldset) picks up the composition with `input`.
