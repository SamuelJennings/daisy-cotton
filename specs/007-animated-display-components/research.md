# Research: Animated and decorative display components

Evidence behind the plan. Third-party behaviour is cited from what this repository resolves: django-cotton 2.6.1 and django-cotton-gallery 1.0.0 in `.venv/lib/python3.13/site-packages/`, and daisyUI 5.7.46, the build `https://cdn.jsdelivr.net/npm/daisyui@5` serves to the demo (`demo/templates/django_cotton_gallery/_extra_head.html`).

## R1. daisyUI 5 class names for this feature

Read from the served `daisyui.css` (5.7.46):

| Component | Classes |
|---|---|
| carousel | `carousel`, `carousel-item`, `carousel-start`, `carousel-center`, `carousel-end`, `carousel-horizontal`, `carousel-vertical` |
| chat | `chat`, `chat-start`, `chat-end`, `chat-image`, `chat-header`, `chat-footer`, `chat-bubble`, `chat-bubble-neutral`, `chat-bubble-primary`, `chat-bubble-secondary`, `chat-bubble-accent`, `chat-bubble-info`, `chat-bubble-success`, `chat-bubble-warning`, `chat-bubble-error` |
| countdown | `countdown` |
| diff | `diff`, `diff-item-1`, `diff-item-2`, `diff-resizer` |
| hover 3D | `hover-3d` |
| hover gallery | `hover-gallery` |
| text rotate | `text-rotate` |
| aura (no component) | `aura`, `aura-dual`, `aura-glow`, `aura-gold`, `aura-holo`, `aura-rainbow`, `aura-silver`, `aura-xs`–`aura-xl` |

daisyUI's class reference files `carousel-start`, `carousel-center` and `carousel-end` under "modifier" and `carousel-horizontal`/`carousel-vertical` under "direction", while `chat-start`/`chat-end` are filed under "placement". The build ships every one of these behind the `sm:`–`2xl:` prefixes too (`\:carousel-vertical` and the rest are in the CSS), so a breakpoint value on the carousel's direction emits a class that exists.

## R2. daisyUI's markup for each component

From daisyUI's class reference (`runs/daisy-cotton/daisyui-llms.txt`) and its component pages:

- **Carousel**: `<div class="carousel {MODIFIER}">` holding `carousel-item` divs. `w-full` on each item makes a full-width carousel. The previous/next and indicator examples are links (`<a href="#slide2" class="btn …">`) to each item's `id`. Previous/next links sit inside each item, positioned over it (`carousel-item relative` holding an `absolute` row); indicator links sit in a row after the carousel.
- **Chat**: `<div class="chat chat-start">` with optional `chat-image`, `chat-header`, then `chat-bubble`, then optional `chat-footer`. A placement class is required.
- **Countdown**: `<span class="countdown"><span style="--value:{n};" aria-live="polite" aria-label="{n}">{n}</span></span>`. daisyUI also documents a `--digits` variable (2 or 3) for zero-padding, set in the same `style`.
- **Diff**: `<figure class="diff aspect-16/9" tabindex="0">` holding `<div class="diff-item-1" role="img" tabindex="0">`, `<div class="diff-item-2" role="img">` and an empty `<div class="diff-resizer">`.
- **Hover 3D**: a `<div>` or `<a>` with `hover-3d` and exactly nine children: the content, then eight empty `<div>`s.
- **Hover gallery**: `<figure class="hover-gallery max-w-60">` holding up to ten same-size `<img>`s.
- **Text rotate**: `<span class="text-rotate">` wrapping one `<span>` that holds up to six line elements. Centring is `justify-items-center` on the inner span.

## R3. What daisyUI's CSS does to the accessibility tree

Read from the 5.7.46 CSS, since the spec requires that no slot content is hidden from assistive technology (FR-005, FR-020):

| Component | CSS | Effect |
|---|---|---|
| hover gallery | `.hover-gallery>*{opacity:0}`, first child `opacity:1` | Every image stays in the accessibility tree. Opacity does not remove content. |
| text rotate | `.text-rotate{overflow:hidden;height:1lh}`, the inner span animated with `translate` | Every line stays in the tree. The lines are grid items of the inner span. Whether a screen reader reads them as separate lines or one run is checked in the browser (R7). |
| diff | `.diff{overflow:hidden}`, the items clipped by the resizer's width | Both items stay in the tree whatever the resizer's position. |
| diff, keyboard | `.diff:focus-visible .diff-resizer{min-width:95cqi}`, `.diff:has(.diff-item-1:focus-visible) .diff-resizer{min-width:5cqi}` | daisyUI 5.7 gives the diff a keyboard behaviour: focusing the figure shows the first item almost fully, focusing the first item shows the second. That is what the two `tabindex="0"`s in its markup are for. |
| hover 3D | eight zones positioned over the content, `z-index:1` | The zones are empty `<div>`s. They carry nothing to announce, and `aria-hidden="true"` keeps them out of the tree (FR-023). |
| countdown | `.countdown>*{visibility:hidden}`, its `::before`/`::after` `visibility:visible` with `content` holding the strings `00` to `99` | **Risk.** The element carrying `aria-live` and `aria-label` is `visibility:hidden`, and the digits are drawn by generated content listing every number. Browsers drop `visibility:hidden` elements from the accessibility tree, so the label may never be read, and generated content can be. US3-2 is checked in the browser (R7). The markup is daisyUI's documented markup, which is what the spec requires, so a failure is daisyUI's to own and is reported, not worked around in the package. |

## R4. daisyUI's diff markup carries `role="img"`

daisyUI's diff example puts `role="img"` on both items. An element with role `img` exposes no children: the `<img alt>` or the text inside is replaced by the element's own name, and these divs have none. That would hide both items' content from assistive technology, which FR-005 and FR-020 forbid. FR-019 takes "any further attributes daisyUI's documented diff markup carries", and the stricter requirements rule this one out. The diff emits both `tabindex="0"`s and no `role`.

## R5. A declared name falls through to the page's context

As FS-006 research R3: a name declared in `<c-vars>` with no default resolves from the caller's template context when the caller leaves it out. `value`, `image`, `header`, `footer` and `href` are all names a page is likely to have in its context. Every name this feature declares gets a default (`=""`, or `placement="start"` and `value="0"`), and each component has one test rendering it inside a context that carries its declared names.

## R6. The gallery shows one preview per component

Gallery 1.0.0 builds each entry's preview as one tag of that component, with the annotated props and slots inside it (`core/preview/tag_builder.py:27-72`). A prop's `example:` is parsed and never used (`core/annotations.py:227`), so a preview carries only declared defaults: a carousel preview cannot carry an `aria-label` unless the carousel declares one with a default. `@trigger` content is placed inside the tag, before the slots, so it cannot put markup beside the component either. FS-001 FR-001 rules out a demo page of the project's own.

So a scenario that needs more than one instance, or markup beside the component, is shown the way FS-006 showed its accordion groups: inside the slot example of a component that holds free markup, where an application would write it, with the component's own `@description` naming that entry.

## R7. The browser checks

As FS-006 research R8: Playwright and Chromium are available locally, and CI has no browser step. The check runs once at the walkthrough against the running gallery: axe-core on each touched entry, plus scripted checks.

- **Carousel**: Tab reaches the carousel, a focus indicator is visible, ArrowRight scrolls it (`scrollLeft` grows). If no indicator shows, the remedy is a `focus-visible` outline utility on the root, as FS-006's collapse needed.
- **Countdown**: the accessibility snapshot of a countdown exposes its number, and after a script sets `--value`, the text and `aria-label`, the live region's content changes (R3 risk).
- **Diff**: the accessibility snapshot contains both items' alt text and text. Tab to the figure, then to the first item, changes the resizer's width.
- **Hover gallery**: the snapshot contains every image's alt text.
- **Hover 3D**: the snapshot contains the content and nothing from the eight zones.
- **Text rotate**: the snapshot contains every line, in order.

The suite asserts what rendered markup can show: elements, classes, roles, names, `aria-*`, `tabindex`, `style`, element order.

## R8. Gallery images

The existing slot examples use `src="..."`, which draws a broken image. The carousel, hover gallery, hover 3D card and diff exist to show images, and the hover gallery needs images of one size to work at all. Their examples use daisyUI's own stock images from `https://img.daisyui.com/images/stock/`, the images daisyUI's documentation uses for these components. The demo already loads daisyUI itself from a CDN, so this adds no new kind of dependency, and the package ships nothing that references them outside annotations.
