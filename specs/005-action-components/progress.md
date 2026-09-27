# Progress: Action components

## 2026-09-27T08:46Z · Plan

Did: branch cut from origin/main 73a4826. Verify green on the base (conformance, docs, lint, typecheck, 4s test run, build). Probed daisyUI 5.7.46 in Chromium for the popover dropdown, the FAB and the swap. Wrote plan.md, research.md, tasks.md, decisions D1–D5 and the ledger.
Next: design review, then batch 1 (US1 button, US2 modal, US3 dropdown).
Watch: README, CHANGELOG and the template tag module overlap with the open navigation and layout pull requests (D1). The modal's gallery entry cannot open from its trigger in gallery 1.0.0 (D3).

## 2026-09-27T08:55Z · Design review

Did: one design reviewer, three lenses. One high finding (a component's `class` leaking onto the trigger it draws) and six low or medium, all verified and applied as plan and task edits (D6, D7). Receipts green.
Next: batch 1 (US1 button, US2 modal, US3 dropdown).
Watch: SPEC-002: T001 must update the dropdown test's expected trigger markup in the same task.

## 2026-09-27T09:03Z · Implementer US1 · T001

Did: rewrote `button.html`'s class list — `variant` and `size` (now `xs`–`xl`) validated
through `{% variation %}`, one class per style boolean (`outline`, `dash`, `soft`, `ghost`,
`link`), behaviour boolean (`active`) and modifier boolean (`wide`, `block`, `square`,
`circle`), `class` merged last. Removed `inline-flex items-center justify-*`, `align`,
`reverse`, `full` and `condition`. Every declared name (including the still-present `href`,
`text`, `icon`) now has an empty default (D6). Rewrote `tests/test_button.py` to the new
contract (D2) and updated the one expected-markup string in
`tests/test_dropdown.py::TestDropdownTrigger::test_extra_attributes_configure_the_default_inner_button`
to the button's new classes.
Verified: `uv run pytest tests/test_button.py tests/test_dropdown.py -q` → 30 passed.
`uv run python manage.py cotton_lint --warnings-as-errors` → button 0 errors/0 warnings (exit 0).
`uv run pytest tests/test_gallery_lint.py -k button -q` → 1 passed. `uv run pytest
tests/test_declared_attributes.py -q` → 26 passed.
Next: T002 (element and states: href/button toggle, disabled, icon `aria-hidden`).
Watch: `href`, `disabled` element/state logic still to land in T002 per the task split.

## 2026-09-27T09:05Z · Implementer US1 · T002

Did: split `button.html` into an explicit `{% if href %}<a>{% else %}<button>{% endif %}`
pair (FR-009). A link carries `href`, `btn-disabled`, `aria-disabled="true"`, `role="button"`
and `tabindex="-1"` when `disabled`, with no native `disabled` attribute; a button carries the
native `disabled` attribute. The icon is now `<c-icon aria-hidden="true">`, decorative by
default; an icon-only button's accessible name comes from the caller's `aria-label` (FR-010).
Added `TestButtonElement` to `tests/test_button.py` for scenarios 2-5.
Verified: `uv run pytest tests/test_button.py tests/test_dropdown.py
tests/test_declared_attributes.py -q` → 61 passed. `uv run python manage.py cotton_lint
--warnings-as-errors` → button 0 errors/0 warnings (exit 0). `uv run pytest
tests/test_gallery_lint.py -k button -q` → 1 passed.
Next: T003 (gallery annotations for button, CHANGELOG).
Watch: the two branches duplicate the class-list construction — Django has no built-in
capture-to-variable tag and the codebase has no existing pattern for it, so this mirrors
plan.md's own two-branch design rather than introducing a new abstraction for two callers.

## 2026-09-27T09:07Z · Implementer US1 · T003

Did: reordered `button.html`'s `@prop` annotations to match `<c-vars>` declaration order,
added an example (`Save`) to the default `@slot`, and extended `@description` to name the
`aria-label` an icon-only button needs. Added `TestButtonGalleryAnnotations` to
`tests/test_button.py`, reading the template's annotations through the gallery's own
`AnnotationParser`: `variant` and `size` are `select` with the full daisyUI list, every style/
behaviour/modifier boolean has its own `@prop`, the default slot's example is `Save`, and the
description mentions `aria-label`. Added the button's `CHANGELOG.md` `Changed` entry (every
removed/renamed attribute and its replacement) — no README change needed, since `button` was
already listed.
Verified: `uv run pytest tests/test_button.py tests/test_dropdown.py
tests/test_declared_attributes.py tests/test_gallery_lint.py tests/test_gallery_annotations.py
-q` → 216 passed. `uv run python manage.py cotton_lint --warnings-as-errors` → button 0
errors/0 warnings (exit 0).
Next: T004 (US2, modal structure).
Watch: US1 (button) done-check satisfied — every acceptance scenario the tests can cover (1-6)
has a test that fails when the behaviour is removed; scenario 7 (gallery, in-browser) is T013's.

## 2026-09-27T09:08Z · Implementer US2 · T004

Did: rewrote `modal.html`'s structure (FR-012, FR-014, FR-016): a `<dialog>` with the
caller's `id`, `placement` (top/middle/bottom/start/end) validated through `{% variation %}`,
`class` merged and attributes spread on the dialog; a plain `modal-box` (no inner `<c-card>`)
holding the default slot and `content_class`; an `actions` slot rendered in a trailing
`modal-action` only when given; `open` rendering `<dialog open>`. Removed the inner card,
`size`, `position`, `icon`, `footer` and `footer_end`; kept the existing translatable
backdrop-close form unchanged. Every declared name has an empty default. `title` and
`closable` are deliberately not yet declared — T005 adds and reads them, so nothing here is
declared without being used (`tests/test_declared_attributes.py`). Rewrote `tests/test_modal.py`
under D2 for scenarios 1 (structure half), 2, 3, 6, an unknown placement, and a page context
carrying `title`, `actions` and `open` that does not leak in.
Verified: `uv run pytest tests/test_modal.py tests/test_declared_attributes.py
tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` → 181 passed. `uv run python
manage.py cotton_lint --warnings-as-errors` → 20/21 clean, 0 errors/0 warnings (exit 0).
Next: T005 (modal naming and closing: title heading, aria-labelledby, closable).

## 2026-09-27T09:10Z · Implementer US2 · T005

Did: `title` renders as an `<h2 id="<id>-title">` and the dialog gets `aria-labelledby`
pointing at it, only when both `id` and `title` are set — no `aria-labelledby` without a
title, and a caller's `aria-label` reaches the dialog through `{{ attrs }}` for a modal with
no title (FR-013). `closable` adds `<form method="dialog">` holding a `<c-button size="sm"
circle ghost>` whose `aria-label` is `{% trans "Close" %}` and whose glyph is `aria-hidden`
(FR-015) — a button with no type inside a form submits it, which closes the dialog with no
script (Article XV). Added `TestModalNaming`, `TestModalClosable` and
`TestModalTranslatableStrings` to `tests/test_modal.py` for scenarios 1 (naming) and 4, that
both "Close" strings sit inside `{% trans %}` in the template source, and that two modals with
different ids get different heading ids.
Verified: `uv run pytest tests/test_modal.py tests/test_declared_attributes.py
tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` → 166 passed. `uv run python
manage.py cotton_lint --warnings-as-errors` → 20/21 clean, 0 errors/0 warnings (exit 0).
`uv run pytest tests/test_render_all.py -k modal -q` → 1 passed.
Next: T006 (gallery annotations for modal, CHANGELOG).

## 2026-09-27T09:11Z · Implementer US2 · T006

Did: `id` is `required` with no `default:`; `placement` lists all five values; `open`'s
description says the dialog shown this way is not modal and a trigger cannot reopen it (D4);
the component `@description` says to give `title` or `aria-label` and how to preview it open
(set `id` to `demo_modal`, switch `open` on, per D3); the default `@slot` and `@slot:actions`
now carry examples (body copy, and a `<form method="dialog"><c-button>` pair); added
`@trigger <c-button onclick="demo_modal.showModal()">Open</c-button>` with D3's description.
Added `TestModalGalleryAnnotations` to `tests/test_modal.py`, reading the template through the
gallery's `AnnotationParser`. Added the modal's `CHANGELOG.md` `Changed` entry — no README
change needed, `modal` was already listed.
Verified: `uv run pytest tests/test_modal.py tests/test_declared_attributes.py
tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` → 166 passed. `uv run python
manage.py cotton_lint --warnings-as-errors` → 20/21 clean, 0 errors/0 warnings (exit 0).
Next: T007 (US3, `unique_id` template tag).
Watch: US2 (modal) done-check satisfied for scenarios 1-4 and 6; scenarios 5 and 7 (in-browser
close/focus-return, gallery trigger) are T013's per D3.

## 2026-09-27T09:12Z · Implementer US3 · T007

Did: added `unique_id(prefix)` to `daisy_cotton/templatetags/daisy_cotton.py` — a
`simple_tag`, usable with `as`, returning `f"{prefix}-{uuid.uuid4().hex[:8]}"` (FR-019,
research R6). Added `TestUniqueId` to `tests/test_templatetags/test_daisy_cotton.py` for the
id's shape and that two calls differ. This test module already mirrors its source module, so
no `pyproject.toml` change was needed.
Verified: `uv run pytest tests/test_templatetags/test_daisy_cotton.py -q` → 9 passed.
Next: T008 (dropdown/index.html, popover method).

## 2026-09-27T09:16Z · Implementer US3 · T008

Did: rebuilt `dropdown/index.html` on daisyUI's popover method (FR-017-FR-020). A wrapper
`<div class="inline-block">` holds either the caller's `button` slot or a default
`<c-button type="button" :attrs="attrs" popovertarget="<panel id>" style="anchor-name:
--<panel id>">`, written after `:attrs` so a caller's forwarded `popovertarget`/`style` cannot
override the anchor (SPEC-003 — confirmed empirically: Cotton's `:attrs` spread does a
`dict.update()` in tag-source order, so a literal attribute written after it wins). The panel
is `<div id="<panel id>" popover class="dropdown ... bg-base-100 rounded-box min-w-52
shadow-sm <content_class>" style="position-anchor: --<panel id>">`, with `<panel id>` the
caller's `id` or a `unique_id "dropdown"` (T007). `placement` splits on whitespace and each
word is validated independently through `{% variation %}`. Removed `valign`, `halign`, `full`,
`hover`, the panel's `dropdown-content`/`tabindex`/`z-50`/border classes. Rewrote
`tests/test_dropdown.py` under D2 for scenarios 1, 2, 5, 6, every side/alignment pair, an
unknown placement word, a caller `id`, a caller `style` that leaves the anchor, `class` on the
wrapper and absent from the default trigger, and a context-leak test. One pre-existing
assertion (`id="sort"` reaching the wrapper) no longer applies: `id` is now a declared prop
naming the panel, not a generic passthrough attribute, so that test now demonstrates
fall-through with `x-data` instead — the underlying "extra attributes fall through" behaviour
is unchanged, only the specific attribute example.
Verified: `uv run pytest tests/test_button.py tests/test_modal.py tests/test_dropdown.py
tests/test_templatetags/ tests/test_declared_attributes.py tests/test_gallery_lint.py
tests/test_gallery_annotations.py tests/test_render_all.py -q` → 277 passed. `uv run python
manage.py cotton_lint --warnings-as-errors` → 20/21 clean, 0 errors/0 warnings (exit 0).
Next: T009 (gallery annotations for dropdown, CHANGELOG). Checkpoint after T009: batch 1 full
suite, cotton_lint, pre-commit.

## 2026-09-27T09:17Z · Implementer US3 · T009

Did: `placement`'s `select` now lists all seven single words and all twelve side-and-alignment
pairs; `@slot:button` has no example and its description names the custom-trigger contract
(`popovertarget`, `type="button"`, the anchor `style`); the default `@slot` example is a plain
daisyUI menu; the component `@description` tells the viewer to type `text="Options"` in the
attributes field to see the default trigger labelled (D5). The `{% comment %}` block on the
custom-trigger contract and the anchor-positioning limitation was already written in T008.
Added `TestDropdownGalleryAnnotations` to `tests/test_dropdown.py`, reading the template
through the gallery's `AnnotationParser`. Added the dropdown's `CHANGELOG.md` `Changed` entry
(popover method, `placement` replacing `valign`/`halign`, `full`/`hover` removed, `class` no
longer reaching the trigger, the panel's dropped classes) and `unique_id`'s `Added` entry — no
README change needed, `dropdown` was already listed and README does not enumerate template tags
individually.
Verified: `uv run pytest tests/test_dropdown.py tests/test_declared_attributes.py
tests/test_gallery_lint.py tests/test_gallery_annotations.py tests/test_render_all.py -q` → 188
passed. `uv run python manage.py cotton_lint --warnings-as-errors` → 20/21 clean, 0 errors/0
warnings (exit 0).
Next: batch 1 checkpoint — full suite, cotton_lint, pre-commit.
Watch: US3 (dropdown) done-check satisfied for scenarios 1, 2, 5 and 6; scenarios 3, 4 and 7
(in-browser keyboard/outside-click, gallery) are T013's.

## 2026-09-27T09:27Z · Implementer US4 · T010

Did: `swap.html`: a `<label class="swap">` wrapper carrying `class` and attributes, `rotate`,
`flip` and `active` mapping to `swap-rotate`/`swap-flip`/`swap-active`; a checkbox carrying
`aria-label` from `label`, and `checked`, `disabled`, `name`, `value` and `input_class` only
when given; `on` and `off` slots always rendered in `swap-on`/`swap-off`; `indeterminate`
rendered in `swap-indeterminate` only when given. Every declared name has an empty default.
Added `tests/test_swap.py` for scenarios 1, 3-6, that `name` and `value` never reach the
wrapper, and that a page context carrying `on`, `off` and `label` does not leak in
(FR-021-FR-023). Added `tests/test_swap.py` to `pyproject.toml`'s
`[tool.forge.conformance] non-mirror-paths`.
Verified: confirmed RED first (moved `swap.html` aside, `uv run pytest tests/test_swap.py -q`
→ 15 failed on `TemplateDoesNotExist`, restored the template) then GREEN — `uv run pytest
tests/test_swap.py -q` → 15 passed. `uv run djlint daisy_cotton/templates/cotton/swap.html
--check` → 0 files would be updated.
Next: T011 (swap gallery annotations, theme-toggle comment, README/CHANGELOG).
Watch: US4 done-check for scenarios 1, 3-6 satisfied; scenarios 2, 7 and 8 (in-browser
keyboard, documentation, gallery) are T011's and T013's.

## 2026-09-27T09:28Z · Implementer US4 · T011

Did: `@slot:on ON` and `@slot:off OFF` gained short-word examples; `@slot:indeterminate` keeps
no example and its description says only a project's own script sets the indeterminate state;
the component `@description` now tells the viewer to give `label` (D5-style). Added a
`{% comment %}` block showing the theme toggle (`input_class="theme-controller" value="dark"`)
and that the theme controller has no component of its own, since a plain `<c-swap>` already
covers it. README's component count and list gain `swap`. CHANGELOG `Added` records `<c-swap>`'s
attributes and the theme-toggle pattern (FR-003, FR-007, FR-024).
Added `TestSwapThemeToggleComment` and extended `TestSwapGalleryAnnotations` in
`tests/test_swap.py`, reading the template through the gallery's `AnnotationParser` and the raw
source for the comment block.
Verified: `uv run pytest tests/test_swap.py tests/test_gallery_lint.py
tests/test_gallery_annotations.py tests/test_declared_attributes.py -q` → 191 passed. `uv run
python manage.py cotton_lint --warnings-as-errors` → 21/22 clean, 0 errors/0 warnings (exit 0).
Next: T012 (FAB).
Watch: US4 done-check satisfied for scenarios 1, 3-6; scenario 2 (in-browser keyboard) and
scenario 7's gallery walk are T013's. Scenario 8 (gallery entry showing the styles/states) is
covered by the annotations above plus T013's browser walk.

## 2026-09-27T09:31Z · Implementer US5 · T012

Did: `fab.html`: a `<div class="fab">` wrapper carrying `class` and pass-through attributes
only when a custom trigger replaces the default; `flower` maps to `fab-flower`; the default
trigger is `<c-button type="button" size="lg" circle tabindex="0" :attrs="attrs" />`, written
before `:attrs` so a caller's `size`, `variant`, `icon` and `aria-label` override the defaults
(research R4); `close` and `main_action` slots render in `fab-close`/`fab-main-action` only when
given; the default slot's actions render as direct children after them; a `button` slot
replaces the default trigger entirely. Every declared name has an empty default, and the FAB's
own `class` never reaches the default trigger (D6).
Gallery annotations: `@description` tells the viewer to type `icon="bi bi-plus-lg"
aria-label="Actions"` in the attributes field (D5); the default `@slot` shows three actions
(two icon-only, one labelled); `@slot:close` and `@slot:main_action` have no example and give
the markup; `@slot:button` names the focusability/tabindex contract.
Added `tests/test_fab.py` for scenarios 1 and 3-6, and a page context carrying `close`,
`main_action` and `button` that does not leak in (FR-025-FR-027). Added the module to
`pyproject.toml`'s `non-mirror-paths`. README lists `fab` in the component count and list.
CHANGELOG `Added` records the FAB's trigger, `flower`, `close`/`main_action` and `class`
behaviour.
Verified: confirmed RED first (moved `fab.html` aside, `uv run pytest tests/test_fab.py -q` →
17 failed on `TemplateDoesNotExist`, restored the template) then GREEN — `uv run pytest
tests/test_fab.py tests/test_gallery_lint.py tests/test_gallery_annotations.py
tests/test_declared_attributes.py -q` → 195 passed. `uv run python manage.py cotton_lint
--warnings-as-errors` → 22/23 clean, 0 errors/0 warnings (exit 0). `uv run djlint
daisy_cotton/templates/cotton/fab.html --check` → 0 files would be updated.
Next: batch 2 checkpoint — full suite, cotton_lint, pre-commit.
Watch: US5 done-check satisfied for scenarios 1, 3-6; scenario 2 (in-browser keyboard) and
scenario 7's gallery walk are T013's.

## 2026-09-27T09:35Z · Converge

Did: all five stories accepted after independent verify and tamper-check. The button now builds one element instead of two branches, and a modal with no id writes no empty `id` (D8). Every decision carries an ADR verdict, none graduated.
Verified: `uv run pytest` 418 passed, 6 skipped; `cotton_lint --warnings-as-errors` 0 errors 0 warnings; pre-commit clean.
Next: code review, then the accessibility run and the walkthrough.
Watch: none.

## 2026-09-27T09:46Z · Review and walkthrough

Did: code review applied (D9): changelog breaks documented, test gaps closed, each surviving mutation now killed. Accessibility run in Chromium clean for the components, every keyboard walk passing. Pull request ready; dev server on port 8023 from this worktree.
Verified: `uv run pytest` 457 passed, 6 skipped; `cotton_lint --warnings-as-errors` 0 errors 0 warnings; pre-commit clean.
Next: the maintainer's walkthrough, then the merge gate.
Watch: port 8023 served the layout components branch before; it now serves this one.
