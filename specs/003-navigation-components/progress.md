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

## 2026-09-26T21:10Z · Implementer US3+US5 · T002

Did: breadcrumbs root drops `text-sm` and takes an overridable translated `aria-label`; item puts class and attributes on the `<li>`, renders the hrefless step as `<span aria-current="page">`, and loses the text span's class. Changed `TestTheItemTextSpan` under D4 and added landmark, current-item and items-versus-slot tests.
Verified: `tests/test_breadcrumbs_href_attribute.py` 17 passed; class-merge, declared-attributes and gallery tests green; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T003.
Watch: none.

## 2026-09-26T21:15Z · Implementer US3+US5 · T003

Did: CHANGELOG `Changed` entries for the link and breadcrumbs breaking changes, each with what a project writes to keep the old result. No page under `docs/` or the README describes their attributes, so no other page changed.
Verified: read back the diff; documentation only.
Next: T004.
Watch: none.

## 2026-09-26T21:20Z · Implementer US3+US5 · T004

Did: dock root is a `<nav class="dock …">` with `size`, merged `class`, pass-through attributes and an overridable translated `aria-label`; `bg-transparent backdrop-blur` removed. New `tests/test_dock.py`, listed in `non-mirror-paths`.
Verified: `tests/test_dock.py` and `tests/test_class_attribute_merge.py` 12 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T005.
Watch: none.

## 2026-09-26T21:30Z · Implementer US3+US5 · T005

Did: dock item marks the active link with `dock-active` and `aria-current="page"`, the active button or toggle with `dock-active` only; icons go through `<c-icon … aria-hidden="true" only>`; the button branch is `type="button"`; the toggle drops `role="button" tabindex="0"` (D9) and writes `aria-label` only when `label` is given.
Verified: `tests/test_dock.py` and `tests/test_class_attribute_merge.py` 29 passed; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T006.
Watch: none.

## 2026-09-26T21:35Z · Implementer US3+US5 · T006

Did: CHANGELOG `Changed` entry for the dock's `<nav>` root, removed classes, button type and toggle. No page under `docs/` or the README describes the dock's markup.
Verified: read back the diff; documentation only.
Next: full verify.
Watch: none.

## 2026-09-26T21:50Z · Implementer US1 · T007

Did: `menu/index.html`, a `<ul class="menu …">` with `size`, `horizontal` (boolean or breakpoint), `paged`, merged `class` and pass-through attributes; no direction class by default. New `tests/test_menu.py`, listed in `non-mirror-paths`.
Verified: `tests/test_menu.py` 11 passed (11 failed before the template existed); `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T008.
Watch: none.

## 2026-09-26T22:05Z · Implementer US1 · T008

Did: `menu/item.html`. A link when `href` is given, else a `<button type="button">`; `active` adds `menu-active` on the inner element and `aria-current="page"` on a link; `disabled` adds `menu-disabled` on the `<li>` and either `role="link" aria-disabled="true"` with no `href` or `tabindex` (link) or native `disabled` (button); icon through `<c-icon … aria-hidden="true" only>`; `class` and attributes on the `<li>`; `aria-label` on the inner control.
Verified: `tests/test_menu.py` 26 passed (15 failed before the template existed); `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T009.
Watch: none.

## 2026-09-26T22:15Z · Implementer US1 · T009

Did: `menu/title.html` (a `<li class="menu-title">` with no interactive element) and `menu/submenu.html` (`<li><details><summary>` plus a nested `<ul>`, `open` adds the attribute, icon in the summary, nests two levels).
Verified: `tests/test_menu.py` 36 passed (10 failed before the templates existed); `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T010.
Watch: none.

## 2026-09-26T22:25Z · Implementer US1 · T010

Did: `menu/index.html` default `@slot` carries a one-line example (title, active link, disabled item, open two-level submenu); README lists `menu`, fixes the count to twenty-five, and says pagination has no component and why; CHANGELOG `Added` entry for the four menu templates. No page under `docs/` describes the menu.
Verified: `cotton_lint --warnings-as-errors` 0 errors 0 warnings; `tests/test_gallery_annotations.py`, `test_gallery_lint.py`, `test_render_all.py`, `test_gallery_links.py` 173 passed, 7 skipped (the menu joins the folder-index skips for #96); gallery page `/django-cotton-gallery/menu/index/` returns 200.
Next: T011.
Watch: the README component count assumes navbar (T012) brings it to twenty-six.

## 2026-09-26T22:35Z · Implementer US2 · T011

Did: `navbar.html`, a `<nav class="navbar …">` named `Main` by default (a caller's `aria-label` replaces it once), merged `class`, pass-through attributes, `start`/`center`/`end` sections each written only when given, default slot directly inside the root. `start`, `center` and `end` are declared in `<c-vars>` with empty defaults so a page variable of the same name emits no section, and a real slot still wins. New `tests/test_navbar.py`, listed in `non-mirror-paths`. The template's annotations landed in this commit because the gallery lint gate fails on an unannotated template.
Verified: `tests/test_navbar.py` 12 passed (12 failed before the template existed); `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T012.
Watch: none.
