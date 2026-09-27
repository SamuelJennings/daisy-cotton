# Progress: Animated and decorative display components

## 2026-09-27T20:30Z · Plan

Did: branch cut from origin/main b2146a4. Re-read the spec against FS-001 to FS-006, which landed after it: no contradiction. Read daisyUI 5.7.46's CSS and class reference for the seven components and the gallery's preview builder. Wrote plan.md, research.md, tasks.md, decisions D1–D5 and the ledger.
Next: design review, then batch 1 (US1 carousel, US2 chat bubble, US3 countdown).
Watch: daisyUI's countdown CSS hides the element carrying `aria-live` (research R3). Checked in the browser at the walkthrough.

## 2026-09-27T22:50Z · Implementer US1 · T001

Did: added `carousel/index.html` and `carousel/item.html` — a focusable, named `role="region"` carousel with translatable roledescriptions "carousel" and "slide", `snap`/`horizontal`/`vertical` through `variation`/`responsive`, `aria-label` with no default (D5), and no controls of its own (FR-008–FR-010). Wrote `tests/test_carousel.py` and started `tests/test_animated_display_no_script.py` with the carousel's caller string.
Verified: `uv run pytest tests/test_carousel.py tests/test_animated_display_no_script.py -q` — 24 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 0 errors, 0 warnings (the carousel's `aria_label` undeclared-var hint matches the same pre-existing heuristic false positive already carried by `breadcrumbs`, `dock`, `navbar` and `megamenu`). The translation test was verified by mutation: hard-coding `aria-roledescription="carousel"` makes it fail for the right reason, confirmed then reverted.
Next: T002 — gallery annotations for `carousel`/`carousel.item`, the `mockup.browser` product-page composition, README and CHANGELOG.
Watch: nothing new.

## 2026-09-27T23:05Z · Implementer US1 · T002

Did: expanded the carousel's own `@slot` to daisyUI's previous/next pattern — four full-width `gallery-slide-N` slides, each with a `<c-button href circle aria-label>` pair overlaid — and left `carousel.item`'s own entry at one `<img alt>`, matching plan.md's Gallery entries table. Rewrote `mockup.browser`'s default `@slot` into a product page: a named `<c-carousel aria-label="Product photos">` of three full-width slides (daisyUI's hat stock images) and daisyUI's indicator row of three `<c-button href size=xs aria-label>` links below it. README: count 55 → 57, `carousel` added to the alphabetical list, and the aura sentence added beside the pagination one. CHANGELOG: an `Added` entry for `<c-carousel>` + `<c-carousel.item>`.
Verified: `uv run pytest tests/test_carousel.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py tests/test_mockup.py tests/test_gallery_links.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 601 passed, 17 skipped (skips are the pre-existing folder-component gallery defect, issue #96, which also covers `carousel`'s own detail page, so I additionally built and rendered the carousel, carousel.item and mockup.browser preview tags by hand through `AnnotationParser` + `build_default_tag` + the Cotton compiler to prove the annotated slot markup itself renders with no error). `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 0 errors, 0 warnings.
Next: US1 done; US2 chat bubble (T003–T004) is a separate story.
Watch: the carousel's own gallery entry preview is unnamed and its indicator/previous-next links are untestable through the sidebar route until issue #96 is fixed upstream — the named, linked version lives in the `mockup.browser` entry instead (D7), and T015's browser walkthrough is where the click-through and keyboard/focus scenarios (US1-4, US1-6) get checked.
