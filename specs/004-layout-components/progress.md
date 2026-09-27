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

## 2026-09-27T01:20Z · Implementer US3+US8 · T003

Did: divider annotations (`placement` and `variant` as selects, direction toggles naming the breakpoint form, `text`, `role`, `class`, one `@slot`) were written with the template in T001/T002; this task adds tests that read them through the gallery's parser, and the CHANGELOG entries under Changed.
Verified: `uv run pytest tests/test_divider.py` 42 passed.
Next: T004 mockups.
Watch: none.

## 2026-09-27T01:30Z · Implementer US3+US8 · T004

Did: `mockup/browser.html`, `phone.html` and `window.html` declare `class`, merge it and spread attributes on the root. The phone display takes `bg-base-100 text-base-content`, loses `text-white`, `bg-neutral-900`, `grid`, `place-content-center`, and its camera is `aria-hidden`. The window keeps a bare `<div>` around the slot without `grid place-content-center h-80`. The browser wraps its slot in a bare `<div>` after the toolbar and declares `url=""`. New `tests/test_mockup.py`, registered in `non-mirror-paths`. Annotations updated with the templates.
Verified: `uv run pytest tests/test_mockup.py` 22 passed; gallery, render-all and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T005 code mockup.
Watch: none.
