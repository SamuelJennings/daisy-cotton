# Progress: Navigation components

## 2026-09-26T20:45Z · Forge · S3 PLAN

Did: branch `003-navigation-components` cut from origin/main de15a40. plan.md, research.md, tasks.md written. decisions.md D1–D6 appended.
Verified: verify gate on the base commit (see ledger).
Next: design review, then batch 1 (US3, US5).

## 2026-09-26T21:00Z · Implementer US3+US5 · T001

Did: `link.html` no longer defaults `href`; `variant` goes through `variation` and is typed `select[…]`. Changed `test_default_href_falls_back_to_hash` under D4 and added tests for scenarios 1-3, an unknown variant and all eight colours.
Verified: `uv run pytest tests/test_link.py -q` 14 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T002.
Watch: none.
