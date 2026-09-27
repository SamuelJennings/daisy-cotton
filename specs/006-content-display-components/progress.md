# Progress: Content display components

## 2026-09-27T12:41Z · Plan

Did: branch cut from origin/main 73a4826. Verify green on the base (conformance, docs, lint, typecheck, test, build). Read daisyUI 5.7.46's class list and probed Cotton's handling of hyphenated attributes. Wrote plan.md, research.md, tasks.md, decisions D1–D4 and the ledger.
Next: design review, then batch 1 (US1 card, US2 table, US3 badge).
Watch: README, CHANGELOG and the template tag module overlap with #101, #102 and #103 (D1). The modal is adjusted here and replaced in #103 (D3).

## 2026-09-27T13:05Z · Implementer US1 · T001

Did: restricted `responsive()` to daisyUI's breakpoint names via a module-level `BREAKPOINTS` tuple, copied from FS-004's diff byte for byte, same code, docstring and two tests.
Verified: `uv run pytest tests/test_templatetags/test_daisy_cotton.py -q` — 13 passed. `uv run pre-commit run --files daisy_cotton/templatetags/daisy_cotton.py tests/test_templatetags/test_daisy_cotton.py` — all hooks passed.
Next: T002, the card body rewrite.
Watch: `divider.html` is the only other caller of `responsive`, and its only test value (`md`) is an accepted breakpoint, so it is unaffected.

## 2026-09-27T13:20Z · Implementer US1 · T002

Did: rewrote `card/index.html`'s structure — root `<div class="card {{ class }}">`, a `figure` slot in `<figure>` before the body, `card-body` with `content_class`, `title` (attribute or slot) as `<h2 class="card-title">` at the top, `actions` slot in `card-actions` at the foot; every declared name `=""`; `icon`, `tight`, `badges`, `footer`, `footer_end`, `body_class` and the built-in `bg-base-100 shadow-sm` removed. Rewrote `tests/test_card.py` under D2 to the new contract: scenarios 1–4, 7, 8, plus a page context carrying `title`, `figure` and `actions` that does not leak into an empty card.
Verified: `uv run pytest tests/test_card.py tests/test_modal.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py -q` — 43 passed (`test_modal.py` untouched and still green — its five tests assert only the modal-box wrapper's width/height classes, not card internals). `uv run pre-commit run --files daisy_cotton/templates/cotton/card/index.html tests/test_card.py` — all hooks passed after ruff-format's own reformat.
Next: T003, the card's size/border/dash/side/image-full modifiers.
Watch: `modal.html` still forwards `title`/`icon`/`footer`/`footer_end` to the card through its own leftover `attrs`, which the card no longer declares — those now land as raw, unused attributes on the card's root instead of rendering. No test currently exercises that path; T004 fixes it directly.

## 2026-09-27T13:35Z · Implementer US1 · T003

Did: added the card's modifiers — `size` through `{% variation %}` against `xs,sm,md,lg,xl`; `border` → `card-border`; `dash` → `card-dash`; `side` through `{% responsive %}` → `card-side` or `<bp>:card-side`; `image-full` (declared hyphenated, research R2) → `image-full`. Wrote the `@prop` annotations for all five now, including `side` as `select['sm','md','lg','xl','2xl']` with the bare-attribute note (T005's final form), since introducing it correctly the first time avoided a rework pass.
Verified: `uv run pytest tests/test_card.py tests/test_modal.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_templatetags/ -q` — 69 passed. `uv run pre-commit run --files daisy_cotton/templates/cotton/card/index.html tests/test_card.py` — all hooks passed (one en-dash lint fix, one ruff-format pass). Spot-checked `uv run python manage.py cotton_lint` — no findings for `card/index.html`.
Next: T004, the modal's adjustment to the new card contract.
Watch: unchanged from T002 — the modal still forwards `title`/`icon`/`footer`/`footer_end` through leftover `attrs`, now also joined by any `size`/`border`/`dash`/`side`/`image-full` a caller passes to `<c-modal>`, none of which the card declares from that path. T004 fixes this directly.

## 2026-09-27T13:48Z · Implementer US1 · T004

Did: `modal.html` now declares `title=""` and `icon=""` itself (research R7) so they reach the card as a `title` slot — `{% if icon %}<c-icon .../>{% endif %}{% if title %}<span>...{% endif %}`, each guarded independently (D5 SPEC-002) so a title-only modal draws no empty icon. `footer`/`footer_end` render in the modal's own flex row, after the body, inside the card's default slot; `actions` is still forwarded as a named slot and now lands in `card-actions` at the foot, below that row. `<c-card>` gains `bg-base-100 shadow-sm`, the surface the card itself no longer draws. Updated the `@description` and `@slot:actions` annotations to say actions now sit in the card body's foot. Added five tests to `tests/test_modal.py` (title+icon in the heading, icon never a raw attribute, title-only draws no `<i>`, footer/footer_end render, actions in `card-actions`); its five pre-existing tests are untouched.
Verified: `uv run pytest tests/test_modal.py tests/test_card.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py -q` — 61 passed. `uv run pre-commit run --files daisy_cotton/templates/cotton/modal.html tests/test_modal.py` — all hooks passed after one ruff-format pass. Spot-checked `uv run python manage.py cotton_lint` — no findings for `modal.html`. `git diff tests/test_modal.py` confirmed the five pre-existing tests are byte-identical; only the new class was appended.
Next: T005, the gallery annotations and CHANGELOG.
Watch: none outstanding for this story.

## 2026-09-27T14:05Z · Implementer US1 · T005

Did: finalised the card's gallery annotations — `size` as `select['xs','sm','md','lg','xl']`, `side` as `select['sm','md','lg','xl','2xl']` with the bare-attribute note, a `@prop` per boolean (`border`, `dash`, `image-full`), `content_class` and `class`; `@slot` a short paragraph of body copy (T013 replaces it with the FAQ once the accordion exists); `@slot:title` with no example, noting an icon-only title needs an accessible name; `@slot:figure` an `<img>` with `alt`; `@slot:actions` a plain `<c-button>` (context.why: the badge-in-button composition is added by the later story that builds the finalised badge, per the brief's plan_sections note — this overrides tasks.md's literal wording). Added CHANGELOG `Changed` entries: the card's new structure (every removed/renamed attribute and slot with its replacement) and `responsive` ignoring a non-breakpoint value. While verifying against the gallery's own linter, found `modal.html` (T004) declares `title`/`icon` in `<c-vars>` with no `@prop` documenting either — a `missing-annotation` warning, which `tests/test_gallery_lint.py` treats as blocking. Added the two `@prop` lines to `modal.html`.
Verified: `uv run pytest tests/test_card.py tests/test_modal.py tests/test_gallery_lint.py tests/test_gallery_annotations.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_templatetags/ -q` — 214 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 20/21 clean, 0 errors, 0 warnings (the one component with hints is `form/field`, pre-existing and out of this story's scope; hints never block). `uv run pre-commit run --files daisy_cotton/templates/cotton/card/index.html daisy_cotton/templates/cotton/modal.html CHANGELOG.md` — all hooks passed.
Next: none — US1 (T001–T005) complete pending the story's one-time full verify.
Watch: none outstanding.

## 2026-09-27T15:20Z · Implementer US2 · T006

Did: added `unique_id` to `daisy_cotton/templatetags/daisy_cotton.py` and its two tests to `tests/test_templatetags/test_daisy_cotton.py`, copied byte for byte from FS-005's diff in the sibling worktree `../005-action-components` (research R6, D1). Merged the test module's docstring and import line with FS-005's version (now names all three tags; adds `import re` and the `unique_id` import alongside the existing `import pytest`).
Verified: `uv run pytest tests/test_templatetags/test_daisy_cotton.py -q` — 15 passed (confirmed red first: `ImportError: cannot import name 'unique_id'`). `uv run pre-commit run --files daisy_cotton/templatetags/daisy_cotton.py tests/test_templatetags/test_daisy_cotton.py` — all hooks passed.
Next: T007, the table template and its tests.
Watch: none outstanding.

## 2026-09-27T15:45Z · Implementer US2 · T007

Did: built `table.html` — wrapper `<div class="overflow-x-auto ...">` with `tabindex="0" role="region"`, `aria-labelledby` pointing at the caption's `unique_id`-generated id only when there is a caption, `class` and `{{ attrs }}` (so a caller's own `aria-label` reaches the wrapper when there is no caption); `<table class="table ...">` with `size` through `{% variation %}` against `xs,sm,md,lg,xl`, `zebra`/`pin-rows`/`pin-cols` → `table-zebra`/`table-pin-rows`/`table-pin-cols`, and `content_class`; `caption` (attribute or slot) as the table's first child `<caption id="...">`, the default slot after it; every declared name `=""`. Wrote `tests/test_table.py` for scenarios 1–7 (FR-013–FR-015), an unknown `size`, two tables on one page getting different caption ids, and a page context carrying `caption` that does not leak in. Added `tests/test_table.py` to `pyproject.toml`'s `non-mirror-paths` (a template test, not a mirrored Python module). Gallery annotations are T008's task; `cotton_lint` currently reports 7 `missing-annotation` warnings on `table`, expected until then.
Verified: confirmed red first — with `table.html` moved aside, all 16 new tests failed on `TemplateDoesNotExist: cotton/table/index.html`. `uv run pytest tests/test_table.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py -q` — 47 passed. `uv run pre-commit run --files daisy_cotton/templates/cotton/table.html tests/test_table.py pyproject.toml` — all hooks passed (one ruff-format pass).
Next: T008, the gallery annotations, `{% comment %}` block, README and CHANGELOG.
Watch: none outstanding.

## 2026-09-27T16:05Z · Implementer US2 · T008

Did: finished the table's gallery annotations — `@description`, one `@prop` per declared name (`caption` described as naming the scrolling region, `size` as `select['xs','sm','md','lg','xl']`, a `@prop` per boolean noting `pin-rows` needs a `<thead>` and `pin-cols` needs row header cells, `content_class`, `class`), default `@slot` a `<thead>`/`<tbody>` snippet with `<th scope="col">` and `<th scope="row">` (T023 replaces it with the status/shortcut composition once those components exist), `@slot:caption` with no example. Added a `{% comment %}` block naming the three caller duties the markup can't enforce (give a caption or `aria-label`; `pin-rows`/`pin-cols` need a `<thead>`/row header cells; the wrapper is a keyboard stop even when the table fits), matching `dropdown/index.html`'s placement between the annotations and `{% load %}`. README: `table` added to the component list, count to twenty-two. CHANGELOG `Added`: `<c-table>` and `unique_id`.
Verified: `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 21/22 clean, 0 errors, 0 warnings (`form/field`'s three hints are pre-existing and out of scope; hints never block). `uv run pytest tests/test_table.py tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` — 161 passed. `uv run pre-commit run --files daisy_cotton/templates/cotton/table.html README.md CHANGELOG.md` — all hooks passed.
Next: none — US2 (T006–T008) complete pending the story's one-time full verify.
Watch: none outstanding.
