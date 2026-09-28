# Implementation Plan: Animated and decorative display components

**Branch**: `007-animated-display-components` | **Date**: 2026-09-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/007-animated-display-components/spec.md`

## Summary

Eight new Cotton templates for seven daisyUI components: `carousel` with `carousel.item`, `chat`, `countdown`, `diff`, `hover-3d`, `hover-gallery` and `text-rotate`. Each renders daisyUI 5's documented markup, ships no script and carries its gallery annotations. Aura gets no component, and the README says why and how to apply it. No Python changes: the existing `variation` and `responsive` tags cover every modifier. Scenarios that need several instances, or markup beside the component, are shown inside the slot examples of the hero, the card and the two window mockups (research R6).

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added.

**Storage**: none

**Testing**: pytest + pytest-django. Components are rendered through the Cotton compiler as a caller's template would be (the `cotton_render_string` and `cotton_render_string_soup` fixtures in `tests/conftest.py`), never by rendering the component file directly, which skips `<c-vars>` extraction.

**Target Platform**: any host project running daisyUI 5

**Project Type**: Django package (templates) with a demo project

**Constraints**: no JavaScript, no stylesheet, no literal colours, no class daisyUI does not define for the component

**Scale/Scope**: 8 new templates, 7 new test modules plus one no-script module, annotation changes on 4 existing templates (`hero`, `card`, `mockup.browser`, `mockup.window`)

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Test-First | Every acceptance scenario that markup can show gets a test written before the template. In-browser scenarios run at the walkthrough (research R7). | Pass |
| II Simplicity | Templates only. `variation` and `responsive` cover every modifier. | Pass |
| III Anti-Abstraction | No base template, no shared include. | Pass |
| V Security | Every value reaches the page through `{{ }}` autoescaping. The countdown's `value` is written into a `style` attribute unvalidated, by the spec's decision (FR-017): escaping keeps it inside the attribute, but not inside the `--value` declaration, so a string holding `;` adds CSS declarations. The countdown's description says the value must be a number and never unvalidated user input. | Pass |
| VI Documentation | README and CHANGELOG lines land in the story that introduces each name. Each component's caller duties and pointer limits live in its annotations and a `{% comment %}` block, as FS-006's did. | Pass |
| VII Dependency discipline | No new dependency. | Pass |
| VIII i18n | The carousel's two roledescriptions, "carousel" and "slide", are `{% trans %}` strings. No other component writes a string of its own. | Pass |
| X Test structure | One test module per component, `Test<Subject>` classes, new modules in `non-mirror-paths` like the existing component tests. | Pass |
| XII Agnostic | Gallery examples use neutral copy. | Pass |
| XIII Semantic palette | Colours only through validated `variant` and semantic utilities (`text-primary`, `bg-base-200`) in gallery examples. | Pass |
| XIV Attribute vocabulary | `variant`, `placement` and `snap`, direction booleans with breakpoints, merged `class`, `content_class` for the text rotate's inner element, the rest through `{{ attrs }}`. | Pass |
| XV Composition | The chat's avatar is the caller's `<c-avatar>`. Carousel controls in gallery examples are `<c-button href>`. | Pass |
| XVI Gallery annotations | Every template annotated, fixed-value props typed `select[…]`, `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below (FS-006's, unchanged):

- **Modifiers.** `variant`, `placement` and `snap` go through `{% variation … %}` against daisyUI's list (research R1), so an unknown value adds nothing and nothing raises (Edge Cases). The carousel's `horizontal` and `vertical` go through `{% responsive … %}`, the direction ruling FS-004 made and FS-007 follows: bare gives the class, a breakpoint gives `<bp>:<class>`, anything else nothing.
- **Root.** Every component declares `class`, merges it into the root's class list, and spreads `{{ attrs }}` on the root (FR-002).
- **Defaults.** Every declared name gets a default, so a page variable of the same name never leaks in (research R5). `=""` everywhere except the chat's `placement="start"` and the countdown's `value="0"`. Annotations give no `default:` for empty defaults, and a `select` must not get `default:""`.
- **Named slots.** A named slot is declared once in `<c-vars>` and rendered only when non-empty (FR-014). It gets a `@prop` and a `@slot:name`, as FS-006's card does.
- **No script.** No `<script>` and no `on*=` attribute in any component's rendered output (SC-003), asserted on the component rendered from a caller string, in one module, `tests/test_animated_display_no_script.py`, that each story extends.
- **Images in examples** use daisyUI's stock images (research R8), each with `alt` describing it.

### Carousel (US1)

`carousel/index.html` — `{% load i18n daisy_cotton %}`, `<c-vars snap="" horizontal="" vertical="" aria-label="" class="" />`.

```
<div class="carousel {% variation snap "carousel" "start,center,end" %} {% responsive horizontal "carousel-horizontal" %} {% responsive vertical "carousel-vertical" %} {{ class }}" role="region" tabindex="0" aria-roledescription="{% trans "carousel" %}"{% if aria_label %} aria-label="{{ aria_label }}"{% endif %} {{ attrs }}>{{ slot }}</div>
```

- `aria-label` is declared, as the navbar, dock and megamenu declare theirs, so the gallery shows it as a field of its own rather than leaving it to the extra-attributes box. It has no default: the component cannot invent a name (Edge Cases).
- `carousel/item.html` — `{% load i18n %}`, `<c-vars class="" />`, `<div class="carousel-item {{ class }}" role="group" aria-roledescription="{% trans "slide" %}" {{ attrs }}>{{ slot }}</div>`. `id` reaches the slide through `{{ attrs }}` (scenario 5).
- The `{% comment %}` block and description: give an `aria-label`; controls are links to slide ids that the project writes, and following one also scrolls the page to the carousel; the gallery's inline preview cannot follow those links, so try them in the entry's raw view; a keyboard user tabs to the carousel and scrolls it with the arrow keys, and screen readers announce it as a carousel of slides (FR-007).
- The carousel's own gallery preview is unnamed: gallery 1.0.0 previews carry only declared defaults, and `aria-label` has none (decisions D7). The named carousel is the `mockup.browser` composition.
- Focus indicator: the browser's own ring on a `tabindex="0"` element, checked in the browser (research R7). If none shows, a `focus-visible` outline utility on the root is a fix task.

### Chat bubble (US2)

`chat.html` — `{% load daisy_cotton %}`, `<c-vars placement="start" variant="" image="" header="" footer="" class="" />`.

```
<div class="chat {% variation placement "chat" "start,end" %} {{ class }}" {{ attrs }}>
  {% if image %}<div class="chat-image">{{ image }}</div>{% endif %}
  {% if header %}<div class="chat-header">{{ header }}</div>{% endif %}
  <div class="chat-bubble {% variation variant "chat-bubble" "neutral,primary,secondary,accent,info,success,warning,error" %}">{{ slot }}</div>
  {% if footer %}<div class="chat-footer">{{ footer }}</div>{% endif %}
</div>
```

- `chat-image` does not also carry `avatar`, as daisyUI's rule for hand-written avatar markup suggests: the caller's `<c-avatar>` brings its own `avatar` root, and doubling it would nest one avatar frame inside another (scenario 5).
- The description says to name the speaker in `header`, because the side is visual only (Edge Cases).

### Countdown (US3)

`countdown.html` — `<c-vars value="0" class="" />`.

```
<span class="countdown {{ class }}" {{ attrs }}><span style="--value:{{ value }};" aria-hidden="true">{{ value }}</span></span><span class="sr-only">{{ value }}</span>
```

- `value` defaults to `0` rather than empty, so the gallery preview draws a number and a bare `<c-countdown />` is valid markup (decisions.md D2).
- `--digits` is not offered. It is a CSS variable, not a class (SC-001 counts classes), and no FR asks for it. The description says a project wanting zero-padding overrides the component.
- The hidden copy sits after the `countdown` span, not inside it: daisyUI makes every direct child of `.countdown` `visibility:hidden` and fills it with the 00–99 lists, and `visibility` is inherited, so anything inside is hidden too (research R3, decisions D12). `sr-only` is Tailwind's, written literally in the template like the other utilities the templates use. `class` and pass-through attributes stay on the `countdown` span.
- The `{% comment %}` block and description carry FR-018: 0–999, a screen reader reads the number as rendered rather than each change, and a script animating it updates `--value`, the visible text and the hidden copy together.

### Diff (US4)

`diff.html` — `<c-vars item_1="" item_2="" aria-label="" class="" />`.

```
<figure class="diff {{ class }}" tabindex="0"{% if aria_label %} aria-label="{{ aria_label }}"{% endif %} {{ attrs }}>
  <div class="diff-item-1" tabindex="0">{{ item_1 }}</div>
  <div class="diff-item-2">{{ item_2 }}</div>
  <div class="diff-resizer"></div>
</figure>
```

- The two `tabindex="0"`s are daisyUI's, and give keyboard users a way to see each item (research R3). daisyUI's `role="img"` on the items is left out (research R4).
- The description says dragging the resizer needs a pointer, and that Tab to the comparison shows the first item and Tab again the second (FR-007, US4-4).

### Hover gallery (US5)

`hover_gallery.html` — `<c-vars class="" />`, `<figure class="hover-gallery {{ class }}" {{ attrs }}>{{ slot }}</figure>`. No width of its own (FR-021). The description carries FR-022's three rules and that every image stays available to screen readers.

### Hover 3D card (US6)

`hover_3d.html` — `<c-vars href="" class="" />`.

```
{% with element=href|yesno:"a,div" %}
<{{ element }}{% if href %} href="{{ href }}"{% endif %} class="hover-3d {{ class }}" {{ attrs }}>{{ slot }}<div aria-hidden="true"></div>…eight in all…</{{ element }}>
{% endwith %}
```

- The same `yesno` element switch the button uses, inside `djlint:off`/`on` as there.
- The description carries FR-025: the content must be one element and hold no buttons, links or inputs, and a linked card takes its name from the content's text or image alt, or from `aria-label`.

### Text rotate (US7)

`text_rotate.html` — `<c-vars content_class="" class="" />`.

```
<span class="text-rotate {{ class }}" {{ attrs }}><span{% if content_class %} class="{{ content_class }}"{% endif %}>{{ slot }}</span></span>
```

- The description carries FR-027: at most six lines, a `duration-*` class on the root changes the ten-second loop, the loop pauses only under a pointer, so rotating text is never the only place information appears.

### Gallery entries (FR-004)

Every template carries `@description`, a `@prop` per `<c-vars>` name and `@slot` / `@slot:name` per slot, in FS-002's order. Fixed-value props are `select[…]` with daisyUI's full list, so the gallery's variants matrix shows every snap, placement and colour. `horizontal`/`vertical` are `select['sm','md','lg','xl','2xl']` with the bare-attribute description, as FS-006's stat group. One-line examples must not contain `#}` or a spaced em dash before the description separator.

Each component's own entry:

| Entry | Default slot / named slots |
|---|---|
| carousel | Four `<c-carousel.item id="gallery-slide-N" class="relative w-full">` slides, each an `<img class="w-full" alt>` and a row of previous/next `<c-button href="#…" circle aria-label>` links over it, daisyUI's previous/next pattern with full-width slides (US1-6). |
| carousel.item | One `<img alt>`. |
| chat | `@slot` a message. `@slot:image` a `<c-avatar src alt>`, `@slot:header` a name and a `<time>`, `@slot:footer` a delivery status (US2-7 per bubble). |
| countdown | No slot. `value` defaults to 0. |
| diff | `@slot:item_1` and `@slot:item_2` two `<img alt>`s, the image comparison (US4-5). |
| hover-gallery | Four same-size `<img alt>`s. |
| hover-3d | A `<figure>` holding an `<img alt>`, the image case. `href` shows the linked case (US6-6). |
| text-rotate | Three lines coloured `text-primary`, `text-secondary`, `text-accent` (US7-6). |

**Compositions (research R6).** Each goes where an application would write it, and the component's `@description` names the entry that shows it:

| Host entry | Composition | Scenarios |
|---|---|---|
| `mockup.browser` default slot | A product page: a carousel named by `aria-label`, three full-width slides with ids, and daisyUI's indicator row of `<c-button href="#…" size="xs">` links below it (US1). A text comparison `<c-diff aria-label>` with text in both items (US4). A linked `<c-hover-3d href>` wrapping a `<c-card>` (US6). | US1-6, US4-5, US6-6 |
| `mockup.window` default slot | A two-sided conversation: four `<c-chat>`s, both placements, `<c-avatar>`s in `image`, names and times in `header`, "Delivered"/"Seen" in `footer`. | US2-7 |
| `hero` default slot | A launch banner: a large centred `<c-text-rotate class="text-5xl" content_class="justify-items-center">` heading, a sentence with an inline rotating word (US7), and a days, hours, minutes and seconds clock of four labelled `<c-countdown>`s (US3), plus the existing call to action. | US3-6, US7-6 |
| `card` `figure` slot | A `<c-hover-gallery>` of four same-size images, a gallery inside a card. | US5-5 |

Every image has `alt`, every icon-only control an `aria-label`, every named region and linked card a name (SC-004).

### Documentation

- `README.md`: the component count goes from 55 to 63 and the list gains each new component in its story. US1 adds the aura sentence beside the pagination one: aura modifies another component, so it has none; wrap the component in `<div class="aura">` with daisyUI's style and size classes (FR-006, SC-005).
- `CHANGELOG.md` `[Unreleased]` `Added`: one entry per new component, each naming its attributes and slots.

## Project Structure

### Documentation (this feature)

```text
specs/007-animated-display-components/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templates/cotton/
├── carousel/index.html, carousel/item.html   # new (US1)
├── chat.html                                 # new (US2)
├── countdown.html                            # new (US3)
├── diff.html                                 # new (US4)
├── hover_gallery.html                        # new (US5)
├── hover_3d.html                             # new (US6)
├── text_rotate.html                          # new (US7)
├── mockup/browser.html, mockup/window.html, hero.html, card/index.html   # annotations only
tests/
├── test_carousel.py, test_chat.py, test_countdown.py, test_diff.py,
│   test_hover_gallery.py, test_hover_3d.py, test_text_rotate.py        # new
└── test_animated_display_no_script.py                                 # new, extended per story
pyproject.toml                # new test modules in non-mirror-paths
README.md, CHANGELOG.md
```

**Structure Decision**: Cotton resolves a hyphenated tag to an underscored file name, so `<c-hover-gallery>`, `<c-hover-3d>` and `<c-text-rotate>` live in `hover_gallery.html`, `hover_3d.html` and `text_rotate.html` (decisions D10). A component with a part is a folder (`carousel/index.html` + `carousel/item.html`), matching `stat/`. The others are single files. The carousel is a folder component, so its sidebar link is one of the skipped cases in `tests/test_gallery_links.py` until the gallery's index-file fix ships, which that test handles with no edit.

## Story order

One worktree, stories in priority order, one after another: they share `README.md`, `CHANGELOG.md`, `pyproject.toml` and, for the compositions, the host templates' annotations.

1. US1 carousel, US2 chat bubble, US4 diff.
2. US5 hover gallery, US6 hover 3D card, US7 text rotate.
3. US3 countdown, last: its markup waits on the maintainer's ruling on FR-016 (decisions D6).

## Complexity Tracking

| Addition | Why | Simpler alternative rejected because |
|---|---|---|
| Compositions in four host entries | US1-6, US2-7, US3-6, US4-5, US5-5, US6-6 and US7-6 need several instances or markup beside the component, and the gallery shows one preview per entry (research R6) | A demo page of its own is ruled out by FS-001 FR-001. |
