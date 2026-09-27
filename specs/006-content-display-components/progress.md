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
