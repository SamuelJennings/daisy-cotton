# Progress: Layout components

## 2026-09-27T00:42Z · Plan

Did: branch cut from origin/main 73a4826. Verify green on the base (lint, typecheck, 5s test run, build, conformance, docs). Wrote plan.md, research.md, tasks.md, decisions D1–D8 and the ledger.
Next: design review, then batch 1 (US3 divider, US8 mockups).
Watch: README and CHANGELOG lines overlap with the open navigation components pull request (D1).

## 2026-09-27T00:55Z · Implementer US3+US8 · T001

Did: `divider.html` emits `divider-horizontal` / `divider-vertical` (bare or with a breakpoint), validates `variant` and `placement` through `variation`, declares `text`, drops the `label` slot and `position`. `responsive` returns `""` for any string outside `sm,md,lg,xl,2xl`. Annotations rewritten to match the new declarations. New `tests/test_divider.py`; two new `responsive` tests.
Verified: `uv run pytest tests/test_divider.py tests/test_templatetags` 37 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings; gallery and class-merge suites green (203 passed).
Next: T002 separator role.
Watch: none.

## 2026-09-27T00:56Z · Implementer US3+US8 · T002

Did: `role` declared; an unlabelled divider (no `text`, blank slot) gets `role="separator"`, plus `aria-orientation="vertical"` when `horizontal` is bare. A caller's `role` replaces it and is written once. Empty defaults keep page context out.
Verified: `uv run pytest tests/test_divider.py` 35 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T003 annotations and changelog.
Watch: a caller `role` on an unlabelled horizontal divider gets no `aria-orientation`; the caller owns the role's semantics.

## 2026-09-27T00:56Z · Implementer US3+US8 · T003

Did: divider annotations (`placement` and `variant` as selects, direction toggles naming the breakpoint form, `text`, `role`, `class`, one `@slot`) were written with the template in T001/T002; this task adds tests that read them through the gallery's parser, and the CHANGELOG entries under Changed.
Verified: `uv run pytest tests/test_divider.py` 42 passed.
Next: T004 mockups.
Watch: none.

## 2026-09-27T00:57Z · Implementer US3+US8 · T004

Did: `mockup/browser.html`, `phone.html` and `window.html` declare `class`, merge it and spread attributes on the root. The phone display takes `bg-base-100 text-base-content`, loses `text-white`, `bg-neutral-900`, `grid`, `place-content-center`, and its camera is `aria-hidden`. The window keeps a bare `<div>` around the slot without `grid place-content-center h-80`. The browser wraps its slot in a bare `<div>` after the toolbar and declares `url=""`. New `tests/test_mockup.py`, registered in `non-mirror-paths`. Annotations updated with the templates.
Verified: `uv run pytest tests/test_mockup.py` 22 passed; gallery, render-all and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T005 code mockup.
Watch: none.

## 2026-09-27T00:57Z · Implementer US3+US8 · T005

Did: `mockup/code/index.html` declares `class`, merges it, spreads attributes and sets `tabindex="0"`. `mockup/code/line.html` declares `prefix`, `text` and `class` with empty defaults, writes `data-prefix` only when a prefix is given, and puts `class` and attributes on the `<pre>`. The two prefix tests and the module docstring in `tests/test_mockup_code.py` are rewritten as decisions.md D2 describes (the first is renamed `test_a_line_has_no_prefix_by_default`, since its old name states the retired behaviour); new tests cover the root behaviour.
Verified: `uv run pytest tests/test_mockup_code.py` 12 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T006 slot examples and changelog.
Watch: the renamed test may show up in a tamper check as a removed test name; D2 authorises it.

## 2026-09-27T00:58Z · Implementer US3+US8 · T006

Did: each mockup template's default `@slot` carries an example (`mockup.code`'s is a `$` line and an unprefixed output line); `class` is annotated on all five. CHANGELOG Changed entries for the code line prefix, phone display, window wrapper, `class`/attribute support and keyboard focus. Tests read the annotations through the gallery's parser.
Verified: `uv run pytest tests/test_mockup.py tests/test_gallery_annotations.py tests/test_gallery_lint.py tests/test_gallery_links.py tests/test_render_all.py` 203 passed, 6 skipped (folder-component gallery links, issue #96).
Next: full verify.
Watch: no page under docs/ or the README describes the divider or the mockups, so no documentation page changed.

## 2026-09-27T01:01Z · Implementer US4+US2+US1 · T007

Did: `join.html` with `join`, `vertical` and `horizontal` through `responsive`, `role` written once (the caller's, else `group`), `class` merged, attributes spread, children rendered with no wrapper; empty defaults on every declared name but `class`. Annotations were written with the template, since the gallery suites require them. New `tests/test_join.py`, registered in `non-mirror-paths`.
Verified: `uv run pytest tests/test_join.py` 19 passed; gallery annotation, lint, render-all, declared-attribute and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T008 README and CHANGELOG.
Watch: none.

## 2026-09-27T01:01Z · Implementer US4+US2+US1 · T008

Did: README component count and list gain `join`; CHANGELOG Added entry for `join`. The annotation tests were written in T007 with the template.
Verified: `git diff` reviewed; no code change, so the join suites from T007 stand.
Next: T009 footer.
Watch: the README says "Twenty-two", counting `join` as one component.

## 2026-09-27T01:02Z · Implementer US4+US2+US1 · T009, T010

Did: `footer/index.html` (a `<footer>` with `footer`, `horizontal` and `vertical` through `responsive`, `placement` validated against `center`, `class` merged, attributes spread) and `footer/nav.html` (a `<nav>` named by `aria-label` from `title`, with the title in `<span class="footer-title">` before the slot; neither when no title). Empty defaults throughout. New `tests/test_footer.py` covers both templates, registered in `non-mirror-paths`. Annotations were written with the templates, since the gallery suites require them. The two tasks share one commit because their tests share one module.
Verified: `uv run pytest tests/test_footer.py` 25 passed; gallery, render-all, declared-attribute and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T011 README and CHANGELOG.
Watch: the footer templates and tests were written together, so the tests were not observed failing before the templates existed.

## 2026-09-27T01:02Z · Implementer US4+US2+US1 · T011

Did: README component count and list gain `footer` + `footer.nav`; CHANGELOG Added entry. Annotations were written and tested in T009/T010.
Verified: documentation-only change; footer suites from T009/T010 stand.
Next: T012 drawer.
Watch: none.

## 2026-09-27T01:03Z · Implementer US4+US2+US1 · T012

Did: `drawer/index.html`: root `drawer`, a `drawer-toggle` checkbox carrying the drawer's `id` (never the root), the page in `drawer-content`, and `drawer-side` holding the `drawer-overlay` label for the same id before the `side` slot; `open` through `responsive`, `placement` validated against `end`. New `tests/test_drawer.py` (registered in `non-mirror-paths`) covers structure, modifiers, two drawers on one page and page-context isolation. The prop annotations the gallery linter needs went in with the template; the accessible names are T013.
Verified: `uv run pytest tests/test_drawer.py` 13 passed; gallery annotation, lint and render-all suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T013 accessible names.
Watch: none.

## 2026-09-27T01:03Z · Implementer US4+US2+US1 · T013

Did: the toggle's and the overlay's `aria-label` are written through `{% trans %}` ("Toggle sidebar", "Close sidebar"). Tests assert each is non-empty in the rendered drawer and that both strings sit inside `{% trans %}` with `i18n` loaded. Observed the three new tests fail before the change.
Verified: `uv run pytest tests/test_drawer.py` 16 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T014 drawer.button.
Watch: no locale catalogue exists in the package, so the strings render in English.

## 2026-09-27T01:03Z · Implementer US4+US2+US1 · T014

Did: `drawer/button.html`: `<label for="{drawer}" class="btn drawer-button {class}">` with the slot, no `role` and no `tabindex`, `drawer` declared with an empty default. Tests cover the label's `for`, classes, absent role and tabindex, attribute pass-through, the button inside a drawer's page wired to the checkbox id, and the page-context case. The minimum annotations the gallery suites require went in with the template; T015 finishes the drawer's.
Verified: `uv run pytest tests/test_drawer.py` 22 passed (six new tests observed failing first); gallery, render-all, declared-attribute and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T015 gallery annotations.
Watch: none.

## 2026-09-27T01:04Z · Implementer US4+US2+US1 · T015

Did: drawer annotations completed: `id` required with no default, `open` toggle naming the `lg` breakpoint form, `placement` select `end`, `class`; `@trigger` the `demo-drawer` opener; default `@slot` the page (responsive divider pattern, `<c-join vertical horizontal="sm">` of three buttons, `<c-footer vertical horizontal="sm">` with two groups); `@slot:side` a menu list; the description tells the viewer to set `id` to `demo-drawer`. `drawer.button` annotations name `drawer` as required and the focus-ring condition. README lists `drawer` + `drawer.button` (count now twenty-six); CHANGELOG Added. Tests read the annotations through the gallery's parser. I also rendered the trigger, page and side example inside `<c-drawer id="demo-drawer">` through the Cotton compiler and read the output: the opener sits in `drawer-content`, its `for` matches the checkbox, divider, join and footer carry their `sm` modifiers.
Verified: `uv run pytest tests/test_drawer.py` 32 passed; gallery annotation, lint, link and render-all suites 211 passed, 8 skipped; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: full verify and report.
Watch: the skip count rises from 6 to 8 because `footer` and `drawer` are folder components, which `tests/test_gallery_links.py` already skips with a reason (issue #96).

## 2026-09-27T01:07Z · Implementer US5 · T016

Did: `indicator/index.html` (`<div class="indicator">` with `{{ items }}` before `{{ slot }}`) and `indicator/item.html` (`<span class="indicator-item">`, each space-separated `placement` word validated on its own, `placement` defaulting to empty). Tests in `tests/test_indicator.py` cover the items slot ahead of the content whichever order the caller writes them, the span and its classes, several items with their own classes, an indicator with no items, the nine corners' words, an unknown word (alone and beside a known one), single class attribute and the page-context case. The minimum annotations the gallery suites require went in with the templates; T017 finishes them.
Verified: the new module failed 20 of 20 before the templates existed, then `uv run pytest tests/test_indicator.py` 20 passed.
Next: T017 annotations, README, CHANGELOG.
Watch: none.

## 2026-09-27T01:08Z · Implementer US5 · T017

Did: indicator annotations finished: the default `@slot` is a button, `@slot:items` an `indicator.item` badge whose visible count is `aria-hidden` and followed by a `sr-only` phrase ("12 unread messages"); `placement` is a `select` of the nine two-word corners with no default; `class` documented. README lists `indicator` + `indicator.item` (count now twenty-eight); CHANGELOG Added. The `placement` select and the required gallery annotations had already gone in with T016 because the gallery suites fail without them.
Verified: the new annotation test on the items slot failed first (no `aria-hidden` count, no `sr-only` phrase), then `uv run pytest tests/test_indicator.py` 27 passed. The test reads the slot through the gallery's parser and renders it inside `<c-indicator>`.
Next: T018 hero.
Watch: none.

## 2026-09-27T01:08Z · Implementer US6 · T018

Did: `hero.html`: `hero` root with the caller's class and attributes, the slot inside `hero-content`, `overlay` adding `<div class="hero-overlay" aria-hidden="true">` before it, `style` reaching the root through `{{ attrs }}`. Annotations: `overlay` toggle, `class`, default `@slot` a heading, a paragraph and a button. README lists `hero` (count now twenty-nine) and its scope line now says the hero container ships while composed hero sections stay with the project; CHANGELOG Added.
Verified: `tests/test_hero.py` failed (8 failed, 3 errors) before the template, then `uv run pytest tests/test_hero.py` 11 passed; gallery annotation, lint, render-all, declared-attribute and class-merge suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T019 mask and stack.
Watch: none.

## 2026-09-27T01:09Z · Implementer US7 · T019

Did: `mask.html` (an `<img>` with `mask`, the shape class, `mask-half-1/2` and an always-present `alt` when `src` is given, a `<div>` around the slot when it is not; `shape` checked against daisyUI's fourteen shapes, `half` against `1,2`) and `stack.html` (`stack`, `placement` checked against `top,bottom,start,end`, children untouched). All declared names default to empty except `class`. Tests in `tests/test_mask_stack.py` cover the image, each of the fourteen shapes, both halves, empty alt, the div form, no shape, unknown shape and half, the four stack placements, an unknown placement, three unhidden children, single class attribute and page-context cases. The gallery suites need minimal annotations on any new template, so the props and a plain slot went in with the templates; T020 finishes them.
Verified: the new module failed 35 of 35 before the templates existed, then `uv run pytest tests/test_mask_stack.py` 35 passed; gallery annotation, lint, render-all, declared-attribute, class-merge and link suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T020 annotations, README, CHANGELOG.
Watch: none.

## 2026-09-27T01:09Z · Implementer US7 · T020

Did: mask annotations finished: `shape` is `required` with no default and lists the fourteen shapes, `half` is `select['1','2']`, `src`, `alt` and `class` documented, and the default `@slot` is an inline `data:` SVG image with alt text. Stack: `placement` select of the four sides, `class`, and the default `@slot` three cards. README lists `mask` and `stack` (count now thirty-one); CHANGELOG Added for both.
Verified: three annotation tests failed first (shape not required, slot not an image with alt text, slot not three cards), then `uv run pytest tests/test_mask_stack.py` 42 passed; gallery annotation, lint and render-all suites green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: full verify and report.
Watch: the mask gallery example is a data: SVG, so it needs no static file or network.

## 2026-09-27T01:13Z · Converge

Did: all eight stories accepted, each re-verified independently. Declared the drawer's `side` and the indicator's `items` slots with empty defaults, added the literal-colour check across every template, and computed the mask's classes once (D12). Progress stamps corrected to the task commit times in UTC.
Verified: uv run pytest 667 passed, 9 skipped. pre-commit, cotton_lint --warnings-as-errors, build, conformance green. No ADR graduated.
Next: code review.
