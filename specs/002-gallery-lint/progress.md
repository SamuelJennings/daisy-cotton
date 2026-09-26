# Progress: FS-002

## 2026-09-26T16:39:16Z · Forge · S3 PLAN
Did: branch `002-gallery-lint` cut from origin/main `cc7473f`. plan.md, research.md, tasks.md written; D1–D3 appended to decisions.md.
Verified: `cotton_lint --warnings-as-errors` on base: 3/21 clean, 1 error, 88 warnings (matches spec). `uv run pytest`: 149 passed.
Next: design review, then US3 + US2 dispatch.

## 2026-09-26T16:49:25Z · Implementer US3 · T001
Did: Reworded the field.html comment so it names no component outside this package, and added @description, nine @prop lines and a default @slot.
Verified: `uv run python manage.py cotton_lint`: form/field had 1 error (unknown-component form.render) and 9 missing-annotation warnings before; after, 0 errors, 0 warnings, 3 hints. One `{# @description`, one default `{# @slot`, no unterminated `{#` line. Render of 8 attribute combinations (text input, bare, textarea, select, checkbox, toggle with list errors, file, radio) at base d04b053 and after: identical with whitespace collapsed. `uv run pytest tests/test_form_field.py -q`: 25 passed.
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:50:03Z · Implementer US2 · T002
Did: Added @description, one @prop per <c-vars> name (including badge's :size_opts) and a default @slot to button.html, link.html and badge.html.
Verified: `uv run python manage.py cotton_lint`: button, link, badge each had missing-annotation warnings before (see base run); after, none listed with any error or warning. Each has one `{# @description`, one default `{# @slot`, no unterminated `{#` line. Renders at base d04b053 vs after (button with all attributes, plain, condition false; link full and bare; badge full and size lg) identical with whitespace collapsed. `uv run pytest tests -q -k 'button or link or badge or alert or icon'`: 32 passed.
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:50:03Z · Implementer US2 · T003
Did: Added @description and @prop lines to alert.html and icon.html, plus a default @slot on alert. The icon description says a project may shadow it with its own cotton/icon.html.
Verified: `uv run python manage.py cotton_lint`: alert and icon each had missing-annotation warnings before; after, none. Each has one `{# @description`; alert has one default `{# @slot`, icon has none. Renders at base d04b053 vs after (alert with all attributes, variant only, bare; icon with name, class, attrs) identical with whitespace collapsed. `uv run pytest tests -q -k 'button or link or badge or alert or icon'`: 32 passed.
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:53:49Z · Implementer US4 · T004
Did: card 5 warnings + 4 undeclared-var hints, divider 4 warnings + 1 hint
Verified: `uv run python manage.py cotton_lint` at base 85a252e: Annotated card and divider: one @description, one @prop per <c-vars> name, a default @slot and a @slot:name for each named slot (card badges, actions, footer, footer_end; divider label). Trimmed card's banner, which the annotations now repeat.; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'card or divider'`: ====================== 10 passed, 139 deselected in 0.28s ======================
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:53:50Z · Implementer US4 · T005
Did: 6 warnings + 1 hint (button)
Verified: `uv run python manage.py cotton_lint` at base 85a252e: Annotated dropdown: description, six props, default slot and @slot:button. The banner's trigger and positioning prose moved into a {% comment %} block.; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'dropdown'`: ====================== 26 passed, 123 deselected in 0.31s ======================
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:53:51Z · Implementer US4 · T006
Did: 5 warnings + 3 hints (actions, footer, footer_end)
Verified: `uv run python manage.py cotton_lint` at base 85a252e: Annotated modal: description saying title, icon and other attributes reach the inner card, five props, default slot, @slot:actions/footer/footer_end and a @trigger for showModal(). Removed the banner, now covered by the annotations.; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'modal'`: ====================== 7 passed, 142 deselected in 0.27s =======================
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:01Z · Implementer US5 · T007
Did: breadcrumbs 2 warnings, breadcrumbs/item 3 warnings
Verified: `uv run python manage.py cotton_lint` at base 85a252e: Annotated breadcrumbs and its item; each description names the other. Left the existing comment about `only` in place.; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'breadcrumbs or breadcrumb'`: ====================== 12 passed, 137 deselected in 0.27s ======================
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:02Z · Implementer US5 · T008
Did: dock 1 warning, dock/item 6 warnings
Verified: `uv run python manage.py cotton_lint` at base 85a252e: Annotated dock and its item; each description names the other. dock.item has no default slot. Removed the item banner now covered by the annotations.; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'dock'`: ====================== 7 passed, 142 deselected in 0.26s =======================
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.

## 2026-09-26T16:54:04Z · Implementer US5 · T009
Did: avatar 9 warnings, avatar/group 2 warnings
Verified: `uv run python manage.py cotton_lint` at base 85a252e: Annotated avatar and avatar.group, keeping the dynamic ':size_options' and ':space_options' names as declared and describing what they do today. avatar has no default slot. Removed the avatar banner now covered by the annotations.; `uv run python manage.py cotton_lint` after: no errors, no warnings for these templates; the named-slot hints (where any) are gone; rules check (one `{# @description`, default `{# @slot` iff `{{ slot }}` rendered, no unterminated `{#` line) on each touched template: all OK; render comparison at base 85a252e vs after, 22 cases across the touched components with attributes, slots and named slots, whitespace collapsed and ends stripped (plus `<pre>` blocks byte-compared): identical; `uv run pytest tests -q -k 'avatar'`: ====================== 4 passed, 145 deselected in 0.22s =======================
Next: continue with the next task in the brief.
Watch: rendered output compared with whitespace collapsed and ends stripped, using a throwaway script outside the repo.
