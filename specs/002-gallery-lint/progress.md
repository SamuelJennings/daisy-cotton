# Progress: FS-002

## 2026-09-26T16:39:16Z · Plan
Did: branch `002-gallery-lint` cut from origin/main `cc7473f`. plan.md, research.md, tasks.md written; D1–D3 appended to decisions.md.
Verified: `cotton_lint --warnings-as-errors` on base: 3/21 clean, 1 error, 88 warnings (matches spec). `uv run pytest`: 149 passed.
Next: design review, then US3 and US2.

## 2026-09-26T16:49:25Z · US3 · T001
Did: Reworded the field.html comment so it names no component outside this package, and added @description, nine @prop lines and a default @slot.
Verified: `uv run python manage.py cotton_lint`: form/field had 1 error (unknown-component form.render) and 9 missing-annotation warnings before; after, 0 errors, 0 warnings, 3 hints. One `{# @description`, one default `{# @slot`, no unterminated `{#` line. Render of 8 attribute combinations (text input, bare, textarea, select, checkbox, toggle with list errors, file, radio) at base d04b053 and after: identical with whitespace collapsed. `uv run pytest tests/test_form_field.py -q`: 25 passed.
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:50:03Z · US2 · T002
Did: Added @description, one @prop per <c-vars> name (including badge's :size_opts) and a default @slot to button.html, link.html and badge.html.
Verified: `uv run python manage.py cotton_lint`: button, link, badge each had missing-annotation warnings before (see base run); after, none listed with any error or warning. Each has one `{# @description`, one default `{# @slot`, no unterminated `{#` line. Renders at base d04b053 vs after (button with all attributes, plain, condition false; link full and bare; badge full and size lg) identical with whitespace collapsed. `uv run pytest tests -q -k 'button or link or badge or alert or icon'`: 32 passed.
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:50:03Z · US2 · T003
Did: Added @description and @prop lines to alert.html and icon.html, plus a default @slot on alert. The icon description says a project may shadow it with its own cotton/icon.html.
Verified: `uv run python manage.py cotton_lint`: alert and icon each had missing-annotation warnings before; after, none. Each has one `{# @description`; alert has one default `{# @slot`, icon has none. Renders at base d04b053 vs after (alert with all attributes, variant only, bare; icon with name, class, attrs) identical with whitespace collapsed. `uv run pytest tests -q -k 'button or link or badge or alert or icon'`: 32 passed.
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:53:49Z · US4 · T004
Did: Annotated card and divider: one @description, one @prop per <c-vars> name, a default @slot and a @slot:name for each named slot (card badges, actions, footer, footer_end; divider label). Trimmed card's banner, which the annotations now repeat.
Verified: `uv run python manage.py cotton_lint` at base 85a252e: card 5 warnings + 4 undeclared-var hints, divider 4 warnings + 1 hint; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'card or divider'`: ====================== 10 passed, 139 deselected in 0.28s ======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:53:50Z · US4 · T005
Did: Annotated dropdown: description, six props, default slot and @slot:button. The banner's trigger and positioning prose moved into a {% comment %} block.
Verified: `uv run python manage.py cotton_lint` at base 85a252e: 6 warnings + 1 hint (button); `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'dropdown'`: ====================== 26 passed, 123 deselected in 0.31s ======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:53:51Z · US4 · T006
Did: Annotated modal: description saying title, icon and other attributes reach the inner card, five props, default slot, @slot:actions/footer/footer_end and a @trigger for showModal(). Removed the banner, now covered by the annotations.
Verified: `uv run python manage.py cotton_lint` at base 85a252e: 5 warnings + 3 hints (actions, footer, footer_end); `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'modal'`: ====================== 7 passed, 142 deselected in 0.27s =======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:01Z · US5 · T007
Did: Annotated breadcrumbs and its item; each description names the other. Left the existing comment about `only` in place.
Verified: `uv run python manage.py cotton_lint` at base 85a252e: breadcrumbs 2 warnings, breadcrumbs/item 3 warnings; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'breadcrumbs or breadcrumb'`: ====================== 12 passed, 137 deselected in 0.27s ======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:02Z · US5 · T008
Did: Annotated dock and its item; each description names the other. dock.item has no default slot. Removed the item banner now covered by the annotations.
Verified: `uv run python manage.py cotton_lint` at base 85a252e: dock 1 warning, dock/item 6 warnings; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'dock'`: ====================== 7 passed, 142 deselected in 0.26s =======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:04Z · US5 · T009
Did: Annotated avatar and avatar.group, keeping the dynamic ':size_options' and ':space_options' names as declared and describing what they do today. avatar has no default slot. Removed the avatar banner now covered by the annotations.
Verified: `uv run python manage.py cotton_lint` at base 85a252e: avatar 9 warnings, avatar/group 2 warnings; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'avatar'`: ====================== 4 passed, 145 deselected in 0.22s =======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:05Z · US6 · T010
Did: Annotated the three mockup frames: description, browser's props, default slot each.
Verified: `uv run python manage.py cotton_lint` at base 85a252e: browser 2 warnings; window and phone had no findings but no annotations; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'mockup or browser or window or phone'`: ====================== 11 passed, 138 deselected in 0.27s ======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:06Z · US6 · T011
Did: Annotated mockup.code and its line, annotations above line 1 only; the rendered <pre> is byte-identical. `uv run python manage.py cotton_lint --warnings-as-errors` exits 0: 0 errors, 0 warnings across all 21 components (form.field keeps 3 undeclared-variable hints, so the summary line reads 20/21 clean).
Verified: `uv run python manage.py cotton_lint` at base 85a252e: line 2 warnings; code index had no findings but no annotations; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'mockup or code'`: ====================== 11 passed, 138 deselected in 0.27s ======================
Next: continue with the next task.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:56:48Z · US7 · T012
Did: Wrote tests/test_gallery_annotations.py rule tests against scratch sources (18 cases) first, then the three rule helpers (AnnotationRules: description, default slot, single-line comments).
Verified: red first: `uv run pytest tests/test_gallery_annotations.py -q`: 18 failed (helper class not defined); after implementing: 18 passed.
Next: T013, the catalog-wide tests and the pyproject registration.
Watch: the helpers live in the test module, since only test files are in scope.

## 2026-09-26T16:57:07Z · US7 · T013
Did: Added catalog-wide tests over every template under cotton/ (parametrised by relative path, three rules each), and registered tests/test_gallery_annotations.py and tests/test_gallery_lint.py in non-mirror-paths. Also recorded T012 in the ledger.
Verified: `uv run pytest tests/test_gallery_annotations.py -q`: 82 passed (arrived green on the real templates, as expected).
Next: US1, T014.
Watch: none.

## 2026-09-26T16:57:43Z · US1 · T014
Did: Wrote tests/test_gallery_lint.py: a GalleryLint helper (scan + CatalogConfig discovery, one lint_catalog call, blocking filter, finding formatter) and 5 tests against scratch cotton directories under tmp_path.
Verified: `uv run pytest tests/test_gallery_lint.py -q`: 5 passed. The tests and helper were written together, so the red step was shown by mutating the helper: BLOCKING limited to errors: 1 failed, 4 passed; discovery pointed at the parent directory: 5 failed. Both mutations reverted.
Next: T015, the package catalog test.
Watch: none.

## 2026-09-26T16:57:54Z · US1 · T015
Did: Added the catalog-wide test, parametrised by component path, reading every report from one module-level lint_catalog call and listing each blocking finding as `<component> L<line> <rule>: <message>`.
Verified: `uv run pytest tests/test_gallery_lint.py -q`: 27 passed (arrived green on the real templates); the same run with -s piped through `grep -ci "MOUNTED AND SERVING"`: 0.
Next: US8, T016.
Watch: none.

## 2026-09-26T16:58:28Z · US8 · T016
Did: Wrote CONTRIBUTING.md: set up, open the gallery, run the linter, the suite and pre-commit, which findings fail, the annotation reference link, and what done means for a component.
Verified: `uv sync`: exit 0; `uv run python manage.py runserver 127.0.0.1:8765 --noreload` then curl of /django-cotton-gallery/: 200, server stopped; `uv run python manage.py cotton_lint --warnings-as-errors`: exit 0, 20/21 clean, 0 errors, 0 warnings. `uv run pytest` and `uv run pre-commit run --all-files` are run in the final verify.
Next: T017.
Watch: the documented address uses port 8000; I tested the same route on port 8765 because 8000 is in use on this machine.

## 2026-09-26T16:58:28Z · US8 · T017
Did: Linked CONTRIBUTING.md from the README Status section; added the [Unreleased] Added entry for the annotations and the two checks that enforce them.
Verified: read back with git diff; the final verify below covers formatting.
Next: full verify and reports.
Watch: none.
