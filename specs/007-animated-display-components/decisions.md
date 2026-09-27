# Decisions: Animated and decorative display components

Ambiguities in issue #16 that were resolved while writing the spec, with the reasoning behind each. The short form of every one is in `spec.md` under *Clarifications*.

## Aura has no component

daisyUI describes aura as a light effect around the border of an important button, card or div. Its markup is a wrapper with exactly one child, the element it highlights, and it has no parts or content of its own. The README's scope gives no Cotton component to something that only modifies another component, the same reason the theme controller and pagination have none. A project writes `<div class="aura">` around the component it wants to highlight, with daisyUI's style and size classes. The README records the exclusion so an adopter looking for it learns why and how.

## The carousel does not emit controls

daisyUI's carousel is one container and its items. The indicator buttons and previous/next arrows in its examples are links to each item's `id`, written beside the carousel rather than inside it. Emitting them would add attributes for button style, placement and labels (tie-break 3), and would tie every adopter to link-based controls that also scroll the page (tie-break 2). A slide accepts an `id`, and the gallery entry shows both patterns built with `<c-button href>`, which satisfies Article XV and shows adopters the markup to copy.

## The carousel is a focusable, named region

With no controls, keyboard users need another way to move through the slides. A scrollable element that can take focus scrolls with the arrow keys in every current browser, so the carousel carries `tabindex="0"`. A focusable element needs a role and a name, so it is a `region` named by `aria-label`, with the roledescriptions "carousel" and "slide" from the WAI-ARIA carousel pattern. The roledescriptions are translatable strings because screen readers speak them.

## `snap` for the carousel's alignment

daisyUI lists `carousel-start`, `carousel-center` and `carousel-end` under the generic heading "modifier" and describes them in its examples as where the items snap to. Article XIV asks for daisyUI's own word, and "snap" is the only one it uses for the concept. `placement` would suggest the carousel's position on the page, which is not what the class does.

## Direction follows the layout components

The layout components spec rules that direction is two booleans named as daisyUI names the modifiers. The carousel uses `horizontal` and `vertical` the same way, so direction reads the same across the package.

## The chat bubble's avatar is a slot

daisyUI puts avatar content inside `chat-image`. Accepting `src`, `alt` and `size` on the chat bubble would copy `<c-avatar>`'s attributes, which then drift when the avatar changes. An `image` slot holding `<c-avatar>` keeps one definition of an avatar (Article XV) and lets a project put an icon or initials there instead.

## The chat bubble defaults to `start`

daisyUI requires a placement class. Defaulting to `start` means `<c-chat>` with no attributes renders valid markup, and `start` is the side daisyUI's examples show first.

## The countdown does not validate its value

A countdown's value almost always comes from the server's clock or a script. Refusing a value outside 0–999 would turn a presentation limit into a page error. The component renders what it is given, Django's autoescaping keeps the value inside the `style` attribute, and the documentation states daisyUI's range.

## `item_1` and `item_2` for the diff

These are daisyUI's part names. `before` and `after` would read better in the common case but invent a parallel vocabulary (tie-break 1), and a diff does not always compare a before with an after. The underscore follows the FAB's `main_action` for `fab-main-action`.

## Slots, not list attributes, for images and lines

A hover gallery's images need `alt`, and sometimes `width`, `height` and `loading`. A text rotate's lines often carry their own colours. A list attribute would have to reinvent each of those, and slots already carry them.

## `content_class` on the text rotate

daisyUI centres the lines with a class on the inner element, which the caller cannot reach through `class` (Article XIV sends that to the root). Every other component with one inner element a caller styles names that attribute `content_class`, so the text rotate uses the same name rather than a second one for the same idea.

## Pointer-only effects

The hover gallery, the hover 3D card, the diff resizer and the text rotate's pause all respond to a pointer only, and daisyUI's CSS drives each one. The package ships no CSS or script, so it cannot add keyboard equivalents without breaking README scope. What it controls is the markup: every piece of slot content stays in the accessibility tree, the effect-only elements are hidden from it, and each component's documentation says what non-pointer users get.

## Priorities

Priorities reflect how many adopters need each component: the carousel in most kinds of project (P1), the chat bubble and countdown in many (P2), and the diff, hover gallery, hover 3D card and text rotate in some (P3).

## D1 — The diff leaves out daisyUI's `role="img"`

daisyUI's diff example puts `role="img"` on both items. An element with that role exposes none of its children, and these carry no name of their own, so a screen reader would get neither item's image alt nor its text. FR-005 and FR-020 require both items' content to stay available. FR-019's "any further attributes daisyUI's documented diff markup carries" is read as the two `tabindex="0"`s, which give keyboard users a way to see each item, and not the role (research R3, R4).

**ADR:** none — local to the diff template.

## D2 — The countdown's value defaults to 0

The spec gives `value` no default. With an empty one, `<c-countdown />` and the gallery preview would render `--value:;` and draw nothing. A counter's natural starting point is 0, a non-empty default still keeps a page variable named `value` from leaking in, and FR-017 is unaffected: whatever the caller gives is rendered as given.

**ADR:** none — local to the countdown template.

## D3 — Multi-instance gallery scenarios are shown in host entries

The gallery renders one preview per component (research R6), and FS-001 rules out a demo page of the project's own. Scenarios that need several instances or markup beside the component (the carousel's indicator row, a conversation, a countdown clock, a gallery inside a card, a linked 3D card, a text comparison, an inline and a centred text rotate) are written into the slot examples of `mockup.browser`, `mockup.window`, `hero` and `card`, and each component's description names where. This is how FS-006 showed its accordion groups.

**ADR:** none — follows the approach FS-006 already set for the gallery.

## D4 — Gallery examples use daisyUI's stock images

The components in this group exist to show images, and the hover gallery only works with images of one size. The existing `src="..."` placeholders draw broken images. Examples use the stock images daisyUI's own documentation uses for these components (research R8). They appear only in annotations, which the gallery reads, so the package ships no reference to them in rendered output.

**ADR:** none — a choice of example content.

## D5 — The carousel and the diff declare `aria-label`

Both take their name from `aria-label`, which would reach them through `{{ attrs }}` anyway. Declaring it puts a named field in the gallery's props panel, as the navbar, dock and megamenu do, so the one attribute every example needs is visible rather than left to the extra-attributes box. Neither gets a default: a component cannot invent a name.

**ADR:** none — local to two templates.

## D6 — Design review applied

One reviewer, three lenses. Verified findings and what was done:

- **SPEC-001 (high), the countdown is not readable by screen readers.** With daisyUI 5.7.46's CSS, the element FR-016 puts `aria-live` and `aria-label` on is `visibility:hidden`, so it leaves the accessibility tree, and the digits are drawn by generated content that lists every number from 00 to 99. Chromium's accessibility tree for `<c-countdown value="42">` holds the two lists and no 42. US3-2 and FR-005 cannot be met with FR-016's markup. This is a spec fault, not a plan fault, so it goes to the maintainer and US3 is built last, after his ruling.
- **SPEC-002 (medium).** The gallery's inline preview is a `srcdoc` frame where a link to `#slide2` navigates the frame to the parent page. The carousel's description says to try the controls in the entry's raw view, and the browser check does so.
- **SPEC-003 (medium).** Recorded as D7.
- **SPEC-004 (medium).** FR-007 for the carousel added to T002 and the plan.
- **SEC-001 (low).** A countdown `value` holding `;` adds CSS declarations inside the `style` attribute. No validation (FR-017). The plan's security row is corrected and the description says the value must be a number.
- **SPEC-005 (low).** D1 confirmed in the browser: without `role="img"` both items' content is exposed, and the two `tabindex="0"`s move the resizer as research R3 says. The pull request names the reading.
- **ARCH-001 (low).** T001 names how the translation test works.
- Review notes carried into tasks: the diff's text example wraps each item's text in one element, the linked 3D card example has no actions, and the text rotate's reduced-motion wording defers to daisyUI's CSS.

**ADR:** none — plan corrections local to this feature.

## D7 — The carousel's own gallery preview is unnamed

Gallery 1.0.0 builds a preview from declared defaults only, and the linter rejects an annotation default that differs from `<c-vars>`. `aria-label` has no default, because the component cannot invent a name. So the carousel entry's own preview is an unnamed region. SC-004's named carousel is the `mockup.browser` composition, which the carousel's description names. The pull request lists this as a known gap against SC-004.

**ADR:** none — a limit of the gallery version in use.

## D8 — How the carousel's translation test works

`{% trans "carousel" %}` does not call `django.utils.translation.gettext` directly: `TranslateNode.render` marks the filter expression for translation and resolves it, and `FilterExpression.resolve` (`django/template/base.py`) calls `gettext_lazy`, imported by name into that module at import time. Patching `django.utils.translation.gettext` therefore does nothing — the lazy wrapper already closed over the real function. `tests/test_carousel.py::TestCarouselTranslation` patches `django.template.base.gettext_lazy` itself, which is the name `FilterExpression.resolve` actually looks up at call time, with a function returning a marked string (`"[t]carousel[/t]"`), no `.po`/`.mo` catalog involved. Verified by mutation: hard-coding `aria-roledescription="carousel"` in the template makes the test fail on the unmarked string, then the template was reverted.

**ADR:** none — a testing technique, not a design choice; recorded so later stories' no-script/translation tests don't rediscover it.

## D9 — The two-sided conversation's avatars carry no alt text of their own

`mockup.window`'s composition names each speaker in the chat's `header` slot (FR-015), so the `<c-avatar>` in each bubble's `image` slot sits beside that name. `avatar`'s own `alt` prop documents "leave empty unless the avatar is the only thing identifying the person — beside a name it is usually noise", so the composition's four avatars carry `alt=""`. `chat.html`'s own isolated `@slot:image` example has no header alongside it, so it keeps a descriptive `alt` there.

**ADR:** none — applies `avatar`'s own documented rule; local to one gallery example.

## D10 — The hover gallery's template file is `hover_gallery.html`, not `hover-gallery.html`

`COTTON_SNAKE_CASED_NAMES` is unset (default `True`), so django-cotton resolves `<c-hover-gallery>` by
replacing `-` with `_` in the tag name before looking up the template: `cotton/hover_gallery.html`, falling
back to `cotton/hover_gallery/index.html`. A file named `hover-gallery.html` never resolves. Verified: the
new tests failed with `TemplateDoesNotExist: cotton/hover_gallery/index.html` against the hyphenated
filename, and passed once renamed to the underscore form.

**ADR:** none — a fixed behaviour of the templating library already in use, not a design choice.

## D11 — The card's `@slot:figure` example calls `<c-hover_gallery>`, not `<c-hover-gallery>`

The gallery's own unknown-component lint (`django_cotton_gallery.core.linter._scanners.scan_unknown_components`)
compares a template's `<c-X>` references against `known_tags` built verbatim from each catalog component's
file name (`Component.path`, from `scanner.py`'s `file.stem`) — it does not apply django-cotton's own
hyphen-to-underscore normalization. D10 already named the component's file `hover_gallery.html`, so the
catalog's only known tag for it is `hover_gallery`; a `<c-hover-gallery>` reference anywhere the lint scans
(a `.html` file under `cotton/`) is flagged `unknown-component`, even though it renders correctly. `card`'s
`@slot:figure` annotation is one such scanned file, so its example calls `<c-hover_gallery>`. Both forms
render identically — Cotton's own resolver folds `-` to `_` before ever comparing to the gallery's
underscore-only view — so this changes nothing about what the gallery entry shows. Verified by rendering the
annotation's parsed `content` by hand through `AnnotationParser` + the Cotton compiler: the card's figure
holds a `hover-gallery` figure with the four hat images and their alt text, in order.

**ADR:** none — a workaround for the same underlying gallery-linter limitation D10 names, not a design
choice. Flagged in `concerns`: US6 (`hover-3d`) and US7 (`text-rotate`) will hit the identical mismatch the
first time either tag is written into a scanned `.html` file (a gallery composition), not just their own
component's tests.
