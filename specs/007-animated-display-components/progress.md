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

## 2026-09-27T21:20Z · Implementer US2 · T003

Did: added `chat.html` — daisyUI's chat markup: a root with `chat` and a `placement` class (`start`/`end`, default `start`, unknown adds nothing), `image`/`header`/`footer` named slots rendered only when given in `chat-image`/`chat-header`/`chat-footer`, and the default slot in `chat-bubble` with `variant` mapped to the eight `chat-bubble-*` colours (FR-012–FR-014). No `{% trans %}`: the chat writes no string of its own (D8 does not apply). Wrote `tests/test_chat.py` for the root/placement, every colour mapping, all three named slots rendering only when given, an empty-slots chat emitting only the root and the bubble, `<c-avatar>` in `image` drawing inside `chat-image` with no `avatar` class leaking onto `chat-image` itself, `class`/`data-id` on the root, and a page context carrying `image`/`header`/`footer`/`variant` not leaking in. Extended `tests/test_animated_display_no_script.py` with the chat's caller string. Added `tests/test_chat.py` to `pyproject.toml`'s `non-mirror-paths`.
Verified: `uv run pytest tests/test_chat.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` — 343 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 51/58 clean, 0 errors, 0 warnings. `uv run ruff check`/`uv run ruff format` clean on the new/edited test files. Probed the tests that weren't obviously red-first by mutating the template twice (hard-coding `chat-start` always; always rendering `chat-image`) and confirming the placement/unknown-placement/empty-slots/page-context tests fail for the right reason each time, then reverted both mutations.
Next: T004 — gallery annotations for `chat` (the description names the speaker convention and the `mockup.window` entry), the `mockup.window` two-sided-conversation composition, README and CHANGELOG.
Watch: nothing new.

## 2026-09-27T21:35Z · Implementer US2 · T004

Did: elevated `chat.html`'s `@slot:header` example from a bare name to a name and a `<time>` (Gallery entries table, US2-7), matching its already-correct `@slot` (a message), `@slot:image` (a `<c-avatar src alt>`) and `@slot:footer` (a delivery status) examples; its `@description` already names the header-speaker convention and the `mockup.window` entry from T003. Rewrote `mockup.window`'s default `@slot` into a two-sided conversation: four `<c-chat>`s alternating `start`/`end`, each with a `<c-avatar>` in `image` (alt left empty — the header names the speaker, so per `avatar`'s own doc an alt here would be noise) and a name plus `<time>` in `header`; the two `placement="end"` bubbles carry `variant="primary"` and "Delivered"/"Seen" in `footer`. README: count 57 → 58, `chat` added to the alphabetical list. CHANGELOG: an `Added` entry for `<c-chat>`.
Verified: `uv run pytest tests/test_chat.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py tests/test_mockup.py tests/test_gallery_links.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 604 passed, 17 skipped (the same pre-existing folder-component gallery defect, issue #96, T002 already recorded — `chat` and `mockup.window` are not folder components and are not among the skips). `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 51/58 clean, 0 errors, 0 warnings. Additionally rendered `mockup.window`'s annotated default `@slot` by hand through the Cotton compiler to confirm the composition itself renders with no error and produces the intended structure.
Next: US2 done.
Watch: nothing new.

## 2026-09-27T21:22Z · Implementer US4 · T007

Did: added `diff.html` — a `<figure>` carrying `diff`, `tabindex="0"` and `aria-label` when given (no default: the component cannot invent a name, D5's precedent extended), holding `diff-item-1` (`tabindex="0"`, `item_1`), `diff-item-2` (`item_2`) and an empty `diff-resizer`, in that order, with no `role="img"` on either item (D1, research R4). Wrote `tests/test_diff.py` for the root's class/tabindex/aria-label, child order and content, the resizer's emptiness, no `role="img"`/`aria-hidden` anywhere, `class`/`data-id` on the figure, and a page context carrying `item_1`/`item_2`/`aria_label` not leaking in. Extended `tests/test_animated_display_no_script.py` with the diff's caller string. Added `tests/test_diff.py` to `pyproject.toml`'s `non-mirror-paths`.
Verified: `uv run pytest tests/test_diff.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` — 347 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 51/59 clean, 0 errors, 0 warnings (the diff's `aria_label` undeclared-var hint matches the same pre-existing heuristic false positive already carried by `carousel`, `breadcrumbs`, `dock`, `navbar` and `megamenu`, T001). `uv run ruff check`/`uv run ruff format` clean on the new/edited test files. All 11 tests observed failing on `TemplateDoesNotExist` before the template existed, then passing after.
Next: T008 — gallery annotations for `diff`, the `mockup.browser` text-comparison composition, README and CHANGELOG.
Watch: nothing new.

## 2026-09-27T21:25Z · Implementer US4 · T008

Did: confirmed the diff's own gallery entry (`@description`, `@prop`s and `@slot:item_1`/`@slot:item_2` two daisyUI stock images — `photo-1560717789-0ac7c58ac90a.webp` and its `-blur.webp` — with alt text) already carries the pointer/Tab/aria-label description and the aspect-ratio class note (written with the template in T007, matching plan.md's Gallery entries table for `diff`). Extended `mockup.browser`'s default `@slot` with a text comparison: a named `<c-diff aria-label class="aspect-16/9">` whose `item_1`/`item_2` slots each wrap one line of text in a single `<div>` (D6: daisyUI positions each item's child absolutely) coloured from the semantic palette (`bg-primary`/`bg-secondary` with their `-content` pair), alongside the existing carousel product-page composition. README: count 58 → 59, `diff` added to the alphabetical list. CHANGELOG: an `Added` entry for `<c-diff>`.
Verified: `uv run pytest tests/test_diff.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py tests/test_mockup.py tests/test_gallery_links.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 612 passed, 17 skipped (the same pre-existing folder-component gallery defect, issue #96, T002 already recorded — `diff` and `mockup.browser` are not folder components and are not among the skips). `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 51/59 clean, 0 errors, 0 warnings. Additionally rendered `mockup.browser`'s annotated default `@slot` by hand through `AnnotationParser().parse()` + `build_default_tag` + the Cotton compiler: no error, the diff figure renders with the given `aria-label`, `item_1` text "BEFORE", `item_2` text "AFTER", and no `role="img"`/`aria-hidden` anywhere.
Next: US4 done.
Watch: nothing new.

## 2026-09-27T23:35Z · Implementer US5 · T009

Did: added `hover_gallery.html` (D10: the tag `<c-hover-gallery>` resolves via django-cotton's snake-cased
lookup to `cotton/hover_gallery.html`, so the file is named with an underscore rather than the hyphen the
plan illustrates) — a `<figure>` carrying `hover-gallery` and the caller's `class` with no width class of
its own, holding the default slot, attributes spread (FR-021). Wrote `tests/test_hover_gallery.py` for the
root's class (with and without a caller class), the slotted images rendering in order, `class`/`data-id` on
the figure, no `aria-hidden` on the figure or any image, and a page context carrying `class` not leaking in.
Extended `tests/test_animated_display_no_script.py` with the hover gallery's caller string. Added
`tests/test_hover_gallery.py` to `pyproject.toml`'s `non-mirror-paths`.
Verified: `uv run pytest tests/test_hover_gallery.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` — 350 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 52/60 clean, 0 errors, 0 warnings (the pre-existing `aria_label` heuristic hint on `breadcrumbs`/`carousel`/`diff`/`dock`/`megamenu`/`navbar`, T001/T007). `uv run ruff check`/`uv run ruff format` clean on the new/edited test files. All 7 tests observed failing on `TemplateDoesNotExist` before the template existed (first against the hyphenated filename, again against the underscore one before it was created), then passing after.
Next: T010 — gallery annotations for `hover-gallery`, the card's `@slot:figure` composition, README and CHANGELOG.
Watch: nothing new.

## 2026-09-27T23:50Z · Implementer US5 · T010

Did: `hover_gallery.html`'s `@description` (written with the template in T009) already carries daisyUI's
three rules, that every image stays available to screen readers and only the hover effect needs a pointer,
and names the card entry for a gallery inside a card; added the missing "a decorative image takes alt=\"\""
sentence (Edge Cases), and its `@slot` already holds four same-size daisyUI hat images with alt (D10). The
`card` entry's `@slot:figure` is now a gallery of the same four hat images with alt, inside a `<c-vars>`
`<figure>` before the body — its example calls `<c-hover_gallery>` rather than `<c-hover-gallery>` (D11: the
gallery lint's unknown-component check compares literally against the catalog's filename-derived tag,
`hover_gallery`, with no hyphen/underscore folding; both forms render identically). README: count 59 → 60,
`hover-gallery` added to the alphabetical list between `hero` and `icon`. CHANGELOG: an `Added` entry for
`<c-hover-gallery>`.
Verified: `uv run pytest tests/test_hover_gallery.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py tests/test_card.py tests/test_gallery_links.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 615 passed, 17 skipped (the same pre-existing folder-component gallery defect, issue #96, T002 already recorded — `hover_gallery` and `card` are not folder components and are not among the skips). `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 52/60 clean, 0 errors, 0 warnings. `uv run ruff check`/`uv run ruff format --check` clean on the touched test files. Additionally rendered the card's annotated `@slot:figure` by hand through `AnnotationParser().parse()` + the Cotton compiler: no error, the card's figure holds a `hover-gallery` figure with the four hat images and their alt text, in order.
Next: US5 done.
Watch: the same `<c-hover-3d>`/`<c-text-rotate>` vs gallery-lint filename mismatch (D10/D11's cause) will
recur the first time US6 or US7 writes either tag into a scanned `.html` composition, not just its own
component's tests.

## 2026-09-27T21:45:15Z · Implementer US6 · T011

Did: added `hover_3d.html` (D10's underscore-filename rule applies here too: `<c-hover-3d>` resolves via
django-cotton's snake-cased lookup to `cotton/hover_3d.html`) — the same `href|yesno:"a,div"` element switch
`button.html` uses, inside `djlint:off`/`on` as there; the root carries `hover-3d`, the caller's `class`
merged, `{{ attrs }}` spread; the default slot renders first, followed by exactly eight empty
`<div aria-hidden="true">` zones (FR-023); the root is an `<a>` with `href` when given, a `<div>` otherwise,
with no `href` attribute when it is absent (FR-024). Wrote `tests/test_hover_3d.py` for nine element
children with the slot content first (also with whitespace around the slot), the eight hidden zones being
empty and carrying `aria-hidden="true"`, the `<a>`/`<div>` switch, `class`/attribute passthrough, and a page
context carrying `href` not leaking in. Extended `tests/test_animated_display_no_script.py` with the hover
3D card's caller string (linked, so its `<a>` branch is covered too). Added `tests/test_hover_3d.py` to
`pyproject.toml`'s `non-mirror-paths`.
Verified: all 9 new tests observed failing on `TemplateDoesNotExist: cotton/hover_3d/index.html` with the
template moved aside, then passing once it was restored. `uv run pytest tests/test_hover_3d.py
tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` —
359 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 53/61 clean, 0 errors, 0
warnings (the same pre-existing `aria_label` heuristic hints as before, T001/T007/T010). `uv run ruff
check`/`uv run ruff format --check` clean on the touched test files.
Next: T012 — gallery annotations for `hover-3d`, the `mockup.browser` linked-card composition, README and
CHANGELOG.
Watch: D11's gallery-lint filename mismatch will hit T012's `mockup.browser` composition the moment it
writes the tag into that scanned file — call it `<c-hover_3d>` there, as the brief already notes.

## 2026-09-27T21:47:28Z · Implementer US6 · T012

Did: expanded `hover_3d.html`'s `@description` with FR-025's wording — the content must be one element
with no buttons, links or inputs of its own, a linked card's accessible name comes from the content's text
or image alt or from `aria-label`, the tilt needs a pointer, and whether it respects reduced motion is up
to daisyUI's CSS. `mockup.browser`'s default `@slot` example gains a linked `<c-hover_3d href="/cards/1">`
wrapping a `<c-card>` with an image figure (the daisyUI `creditcard.webp` stock image, D4) and a title, no
`actions` slot (D6: no interactive content inside); it uses `<c-hover_3d>` rather than `<c-hover-3d>`
because `mockup/browser.html` is a scanned `.html` file and the gallery lint's unknown-component check
compares literally against the catalog's filename-derived tag, `hover_3d` (D10/D11's cause, watched for in
T011). README: "Sixty" -> "Sixty-one", `hover-3d` added alphabetically before `hover-gallery`. CHANGELOG:
an `Added` entry for `<c-hover-3d>`.
Verified: `uv run pytest tests/test_mockup.py tests/test_gallery_lint.py tests/test_gallery_annotations.py
tests/test_hover_3d.py tests/test_animated_display_no_script.py tests/test_card.py tests/test_render_all.py
tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` —
608 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 53/61 clean, 0 errors, 0
warnings (same pre-existing `aria_label` heuristic hints). Additionally rendered `mockup.browser`'s
annotated default `@slot` by hand through `AnnotationParser().parse()` + the Cotton compiler: no error, the
`<c-hover_3d>` root is an `<a href="/cards/1">` wrapping a `<c-card>` whose figure holds the credit-card
image and alt, a `card-title` of "Rewards card", and no `card-actions` element. No new test file this task
(T012's work is documentation content the generic gallery lint/annotation suites already discover
dynamically, the same pattern T010 followed for the hover gallery).
Next: US6 done.
Watch: nothing new.

## 2026-09-27T21:53Z · Implementer US7 · T013

Did: added `text_rotate.html` — a `<span class="text-rotate">` (`class` merged, `attrs` spread) wrapping one inner `<span>` that holds the default slot's lines in order and carries `content_class` only when given (D10: the file is `text_rotate.html` because Cotton folds `-` to `_`; callers write `<c-text-rotate>`). Wrote `tests/test_text_rotate.py` for the root's class merge, the inner span's line order, `content_class` landing on the inner span, no `class` attribute on the inner span when `content_class` is empty, `class`/`data-id` on the root, no `aria-hidden` anywhere, and a page context carrying `content_class`/`class` not leaking in. Extended `tests/test_animated_display_no_script.py` with the text rotate's caller string. Added `tests/test_text_rotate.py` to `pyproject.toml`'s `non-mirror-paths`.
Verified: `uv run pytest tests/test_text_rotate.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py -q` — 365 passed. `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 54/62 clean, 0 errors, 0 warnings (`text_rotate` is not among the pre-existing `aria_label` heuristic hints). All 8 tests observed failing on `TemplateDoesNotExist: cotton/text_rotate/index.html` before the template existed, then passing after.
Next: T014 — gallery annotations for `text-rotate`, the `hero` composition's rotating heading and inline word, README and CHANGELOG.
Watch: US6 (`hover_3d`) already hit the gallery-linter's underscore-only `known_tags` mismatch D11 names; T014 will need `<c-text_rotate>` (not `<c-text-rotate>`) inside the `hero` template's scanned `@slot` annotation for the same reason.

## 2026-09-27T22:05Z · Implementer US7 · T014

Did: `text_rotate.html`'s own `@description` and three-line `@slot` example (`text-primary`/`text-secondary`/`text-accent`) already carried the full gallery-entry content from T013 (the six-line limit, the `duration-*` class, the pointer-only pause, the reduced-motion note and the `hero` pointer), so this task made no further change to that file. Rewrote `hero.html`'s default `@slot` (its only permitted edit) into a launch banner: the `<h1>` now wraps `<c-text_rotate class="text-5xl" content_class="justify-items-center">` around three heading lines, the paragraph gains an inline `<c-text_rotate>` of three words mid-sentence, and the existing "Get started" button is unchanged — written as `<c-text_rotate>` per D10/D11 (the gallery linter's `known_tags` is underscore-only, matching how `hover_3d` was written into `mockup.browser`'s annotation). No countdown clock added yet — US3 lands it later per plan.md's "Compositions" and the brief's instruction to leave room. README: Sixty-one → Sixty-two, `text-rotate` added to the alphabetical list. CHANGELOG: an `Added` entry for `<c-text-rotate>`.
Verified: `uv run pytest tests/test_text_rotate.py tests/test_animated_display_no_script.py tests/test_gallery_lint.py tests/test_gallery_annotations.py tests/test_hero.py tests/test_render_all.py tests/test_declared_attributes.py tests/test_class_attribute_merge.py tests/test_semantic_palette.py -q` — 582 passed (`tests/test_hero.py`'s pre-existing, unedited `test_the_default_slot_holds_a_heading_copy_and_a_button` still finds `<h1`, `<p` and `btn` in the rewritten slot). `uv run python manage.py cotton_lint --warnings-as-errors` — exit 0, 54/62 clean, 0 errors, 0 warnings. Additionally parsed `hero.html`'s annotation by hand through `AnnotationParser().parse()`, compiled the extracted `@slot` content through `CottonCompiler` + `Template.render()`: no error, the rendered output holds a `text-rotate` span with the three heading lines under `justify-items-center` in the `<h1>`, a second `text-rotate` span with the three inline words in the paragraph, and the button, in that order.
Next: US7 done.
Watch: nothing new.

## 2026-09-27T22:05Z · Browser check, six stories

Did: ran axe-core and the scripted checks (research R7) on the running gallery's raw preview pages for the carousel, chat bubble, diff, hover gallery, hover 3D card and text rotate, and the four host entries.
Verified: no component-level axe violation. The only findings are page-level ones the bare preview page raises for any component (no `main` landmark, no `h1`, content outside a landmark). The carousel is the first Tab stop with the browser's focus ring, ArrowRight scrolls it (0 → 1280), and a next link and an indicator link both scroll it in the raw view. The diff exposes the figure's name and both images' alt text, and Tab moves the resizer (16px min → 1216px on the figure → 64px on the first item). All four hover gallery images are in the accessibility tree, and the pointer at the right shows the fourth. The hover 3D card exposes only its image and tilts under the pointer. The text rotate exposes every line in order, runs `rotator` for 10s, and pauses under the pointer.
Next: the countdown (US3) after the maintainer's ruling on FR-016 (decisions D6), then converge.
Watch: the carousel's own gallery page returns 404, like the gallery's other folder components (#96). The raw view and the browser mockup's entry work.
