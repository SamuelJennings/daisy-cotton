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

## 2026-09-26T22:40Z · Implementer US2 · T012

Did: the navbar's annotations (`@description`, a `@prop` per `<c-vars>` name, `@slot` and `@slot:start`, `:center`, `:end` with example content) were written with the template in T011. This task adds `navbar` to the README component list (count now twenty-six) and a CHANGELOG `Added` entry. No page under `docs/` describes the navbar.
Verified: `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: full verify.
Watch: none.

## 2026-09-26T23:10Z · Implementer US4 · T013

Did: `tabs/index.html`, a `<div class="tabs …">` with `role="tablist"` unless `links`; `box`, `border`, `lift` booleans, `size` and `placement` (`top`/`bottom`) through `variation` so an unknown value adds nothing; class and attributes on the root. Annotations landed with the template; the example slot is a plain description until `tabs.tab` exists (T016 adds the real example). New `tests/test_tabs.py`, listed in `non-mirror-paths`.
Verified: `tests/test_tabs.py` 10 passed (10 failed before the template existed); `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T014.
Watch: none.

## 2026-09-26T23:15Z · Implementer US4 · T014

Did: `tabs/tab.html` link and button shapes. A link tab with `active` gets `tab-active` and `aria-current="page"`; a disabled one drops `href` and carries `tab-disabled`, `role="link"` and `aria-disabled="true"`, with no `tabindex`. A tab with no `href` is `<button type="button" role="tab">` with `aria-selected` true or false from `active`, and native `disabled` plus `tab-disabled`. `class` and attributes land on the tab element. Annotations landed with the template.
Verified: `tests/test_tabs.py` 22 passed (12 new ones failed before the template existed); `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T015 (radio shape and the `name` c-var).
Watch: none.

## 2026-09-26T23:20Z · Implementer US4 · T015

Did: the radio shape in `tabs/tab.html`: `<input type="radio" class="tab" name aria-label>` with `checked` on `active` and native `disabled`, followed by `<div class="tab-content">` holding the slot. `name` is declared in `<c-vars>` with an empty default so a page variable called `name` cannot turn a button tab into a radio. Radio tabs sit in a root that keeps `role="tablist"`.
Verified: `tests/test_tabs.py` 29 passed (5 of the 7 new tests failed before the radio branch existed); the page-context test was probed: without `name=""` in `<c-vars>` it fails, with it it passes. `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T016.
Watch: none.

## 2026-09-26T23:25Z · Implementer US4 · T016

Did: the tabs annotations were written with the templates (T013-T015); this task adds the `tabs/index.html` default `@slot` example (a link set with one active and one disabled tab), lists `tabs` in the README (count now twenty-seven) and adds a CHANGELOG `Added` entry. No page under `docs/` describes the tabs.
Verified: `cotton_lint --warnings-as-errors` 0 errors 0 warnings; `tests/test_tabs.py`, `test_gallery_annotations.py`, `test_gallery_lint.py`, `test_render_all.py`, `test_gallery_links.py` 219 passed, 8 skipped (tabs joins the folder-index skips for #96).
Next: T017.
Watch: the README count assumes steps and megamenu bring it to twenty-eight and twenty-nine.

## 2026-09-26T23:35Z · Implementer US6 · T017

Did: `steps/index.html`, an `<ol class="steps …">` with `vertical` and `horizontal`, each a boolean or a breakpoint through `responsive` (vertical plus `horizontal="lg"` gives `steps-vertical lg:steps-horizontal`); and `steps/step.html`, an `<li class="step …">` with `variant` validated against the eight colours through `variation`, `aria-current="step"` on `current`, `data-content` only when `content` is given, and an icon in `<span class="step-icon">` through `<c-icon … aria-hidden="true" only />` so the step's class does not reach the icon. Annotations landed with the templates. New `tests/test_steps.py`, listed in `non-mirror-paths`.
Verified: `tests/test_steps.py` 19 passed (19 failed before the templates existed); `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T018.
Watch: none.

## 2026-09-26T23:40Z · Implementer US6 · T018

Did: the steps annotations were written with the templates (T017); this task adds the `steps/index.html` default `@slot` example (four steps: two primary, one current, one with custom content, one with an icon), lists `steps` in the README (count now twenty-eight) and adds a CHANGELOG `Added` entry. No page under `docs/` describes the steps.
Verified: `cotton_lint --warnings-as-errors` 0 errors 0 warnings; `tests/test_steps.py`, `test_gallery_annotations.py`, `test_gallery_lint.py`, `test_render_all.py`, `test_gallery_links.py` 220 passed, 9 skipped (steps joins the folder-index skips for #96).
Next: T019.
Watch: none.

## 2026-09-26T23:50Z · Implementer US7 · T019

Did: `megamenu/index.html`: a required `id`, a Menu toggle rendered through `<c-button class="sm:hidden" type="button" popovertarget="{{ id }}" … only />`, then `<nav id popover class="megamenu max-sm:megamenu-vertical …">` holding `<span class="megamenu-active">` and the slot. `wide`, `full` and `size` add `megamenu-wide`, `megamenu-full` and `megamenu-<size>`; the name is a translated `Site` unless the caller gives an `aria-label`, which replaces it once. Annotations landed with the template; the description gives daisyUI's ten-item limit and says to set `id` in the playground. New `tests/test_megamenu.py`, listed in `non-mirror-paths`.
Verified: `tests/test_megamenu.py` 11 passed (11 failed before the template existed); probed: dropping `only` from the toggle makes the full/size and page-context `href` tests fail; `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T020.
Watch: none.

## 2026-09-26T23:55Z · Implementer US7 · T020

Did: `megamenu/item.html`: `<button type="button" popovertarget="<megamenu>-<key>">` followed by `<div id="<megamenu>-<key>" popover>` holding the slot. `megamenu` (the megamenu's id) and `key` are required, since an item cannot read the id of the megamenu around it. `class` and attributes land on the panel, and no `aria-expanded` is written: the browser exposes the popover's state. Annotations landed with the template.
Verified: `tests/test_megamenu.py` 17 passed (6 new ones failed before the template existed); three items each target the id of their own following panel, and two megamenus with different ids on one page repeat no id. `cotton_lint --warnings-as-errors` 0 errors 0 warnings.
Next: T021.
Watch: none.

## 2026-09-26T23:58Z · Implementer US7 · T021

Did: the megamenu annotations were written with the templates (T019, T020, including the ten-item limit and setting `id` in the playground); this task adds the `megamenu/index.html` default `@slot` example (three items each holding a menu), lists `megamenu` in the README (count now twenty-nine) and adds a CHANGELOG `Added` entry. No page under `docs/` describes the megamenu.
Verified: `cotton_lint --warnings-as-errors` 0 errors 0 warnings; `tests/test_megamenu.py`, `test_gallery_annotations.py`, `test_gallery_lint.py`, `test_render_all.py`, `test_gallery_links.py` 229 passed, 10 skipped (megamenu joins the folder-index skips for #96).
Next: full verify.
Watch: none.
