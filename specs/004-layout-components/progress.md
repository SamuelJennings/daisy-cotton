# Progress: Layout components

## 2026-09-27T02:40Z · Plan

Did: branch cut from origin/main 73a4826. Verify green on the base (lint, typecheck, 5s test run, build, conformance, docs). Wrote plan.md, research.md, tasks.md, decisions D1–D8 and the ledger.
Next: design review, then batch 1 (US3 divider, US8 mockups).
Watch: README and CHANGELOG lines overlap with the open navigation components pull request (D1).

## 2026-09-27T01:10Z · Implementer US3+US8 · T001

Did: `divider.html` emits `divider-horizontal` / `divider-vertical` (bare or with a breakpoint), validates `variant` and `placement` through `variation`, declares `text`, drops the `label` slot and `position`. `responsive` returns `""` for any string outside `sm,md,lg,xl,2xl`. Annotations rewritten to match the new declarations. New `tests/test_divider.py`; two new `responsive` tests.
Verified: `uv run pytest tests/test_divider.py tests/test_templatetags` 37 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings; gallery and class-merge suites green (203 passed).
Next: T002 separator role.
Watch: none.

## 2026-09-27T01:14Z · Implementer US3+US8 · T002

Did: `role` declared; an unlabelled divider (no `text`, blank slot) gets `role="separator"`, plus `aria-orientation="vertical"` when `horizontal` is bare. A caller's `role` replaces it and is written once. Empty defaults keep page context out.
Verified: `uv run pytest tests/test_divider.py` 35 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T003 annotations and changelog.
Watch: a caller `role` on an unlabelled horizontal divider gets no `aria-orientation`; the caller owns the role's semantics.
