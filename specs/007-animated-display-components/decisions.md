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
