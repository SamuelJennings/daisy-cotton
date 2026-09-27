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

## 2026-09-27T01:40Z · Implementer US3+US8 · T005

Did: `mockup/code/index.html` declares `class`, merges it, spreads attributes and sets `tabindex="0"`. `mockup/code/line.html` declares `prefix`, `text` and `class` with empty defaults, writes `data-prefix` only when a prefix is given, and puts `class` and attributes on the `<pre>`. The two prefix tests and the module docstring in `tests/test_mockup_code.py` are rewritten as decisions.md D2 describes (the first is renamed `test_a_line_has_no_prefix_by_default`, since its old name states the retired behaviour); new tests cover the root behaviour.
Verified: `uv run pytest tests/test_mockup_code.py` 12 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T006 slot examples and changelog.
Watch: the renamed test may show up in a tamper check as a removed test name; D2 authorises it.

## 2026-09-27T01:50Z · Implementer US3+US8 · T006

Did: each mockup template's default `@slot` carries an example (`mockup.code`'s is a `$` line and an unprefixed output line); `class` is annotated on all five. CHANGELOG Changed entries for the code line prefix, phone display, window wrapper, `class`/attribute support and keyboard focus. Tests read the annotations through the gallery's parser.
Verified: `uv run pytest tests/test_mockup.py tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_gallery_links.py tests/test_render_all.py` 203 passed, 6 skipped (folder-component gallery links, issue #96).
Next: full verify.
Watch: no page under docs/ or the README describes the divider or the mockups, so no documentation page changed.

## 2026-09-27T01:10Z · Implementer US4+US2+US1 · T007

Did: `join.html` with `join`, `vertical` and `horizontal` through `responsive`, `role` written once (the caller's, else `group`), `class` merged, attributes spread, children rendered with no wrapper; empty defaults on every declared name but `class`. Annotations were written with the template, since the gallery suites require them. New `tests/test_join.py`, registered in `non-mirror-paths`.
Verified: `uv run pytest tests/test_join.py` 19 passed; gallery annotation, lint, render-all, declared-attribute and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T008 README and CHANGELOG.
Watch: none.

## 2026-09-27T01:12Z · Implementer US4+US2+US1 · T008

Did: README component count and list gain `join`; CHANGELOG Added entry for `join`. The annotation tests were written in T007 with the template.
Verified: `git diff` reviewed; no code change, so the join suites from T007 stand.
Next: T009 footer.
Watch: the README says "Twenty-two", counting `join` as one component.

## 2026-09-27T01:20Z · Implementer US4+US2+US1 · T009, T010

Did: `footer/index.html` (a `<footer>` with `footer`, `horizontal` and `vertical` through `responsive`, `placement` validated against `center`, `class` merged, attributes spread) and `footer/nav.html` (a `<nav>` named by `aria-label` from `title`, with the title in `<span class="footer-title">` before the slot; neither when no title). Empty defaults throughout. New `tests/test_footer.py` covers both templates, registered in `non-mirror-paths`. Annotations were written with the templates, since the gallery suites require them. The two tasks share one commit because their tests share one module.
Verified: `uv run pytest tests/test_footer.py` 25 passed; gallery, render-all, declared-attribute and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T011 README and CHANGELOG.
Watch: the footer templates and tests were written together, so the tests were not observed failing before the templates existed.

## 2026-09-27T01:22Z · Implementer US4+US2+US1 · T011

Did: README component count and list gain `footer` + `footer.nav`; CHANGELOG Added entry. Annotations were written and tested in T009/T010.
Verified: documentation-only change; footer suites from T009/T010 stand.
Next: T012 drawer.
Watch: none.
