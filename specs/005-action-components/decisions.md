# Decisions: Action components

Ambiguities in issue #14 that were resolved while writing the spec, with the reasoning behind each. The short form of every one is in `spec.md` under *Clarifications*.

## The dropdown uses the popover method

daisyUI documents three ways to build a dropdown:

- **Popover.** A button targets a popover panel. The browser handles opening, closing on Escape and on an outside click, and tells assistive technology whether the panel is open. The trigger is a real `<button>`, so `<c-button>` can draw it.
- **`<details>` and `<summary>`.** The browser reports the open state, but the trigger must be the `<summary>` element itself. A button inside a summary is invalid HTML, so the trigger would have to copy the button's classes inline, which Article XV forbids. It also does not close on an outside click without script.
- **CSS focus.** This is what the current component does. The panel shows while focus is inside it. Nothing reports whether it is open, and Escape does not close it without script. It is the only method that supports `dropdown-hover`.

Popover is the only method that meets G3 and Article XV together with no script, and it is the one daisyUI lists first. The cost is `hover`, `dropdown-open` and `dropdown-close`, which daisyUI's rules tie to the other methods, and placement depends on CSS anchor positioning. A project that wants hover-to-open overrides the component, which is what the README's tie-break 2 prescribes.

## `placement` replaces `valign`, `halign` and `position`

daisyUI calls both class groups "placement". Article XIV asks for daisyUI's name where it has one. Two attributes for one daisyUI concept would also go against tie-break 3. The dropdown takes a side and an alignment in one value, for example `placement="top end"`, because daisyUI's examples combine one of each.

## The modal drops its inner card

The current modal puts a `<c-card>` inside a transparent modal box, so its attributes are the card's: `title`, `icon`, `footer`, `footer_end`. daisyUI's modal is a box with an actions row. Tie-break 1 (follow daisyUI) and tie-break 3 (fewer attributes) both point to the plain structure. `title` stays because it gives the dialog its accessible name, which G3 needs. `actions` stays because it maps to daisyUI's `modal-action`. A project that wants a card puts one in the slot.

## The modal drops `size`

daisyUI has no modal size modifier. Article XIV reserves `size` for daisyUI's `xs`–`xl` scale, and the current `size` maps to arbitrary maximum widths instead. Width goes through `content_class` on the box.

## `content_class` for inner surfaces

Article XIV sends `class` to the root element. The modal box and the dropdown panel are inner elements that callers regularly need to size or style. The dropdown already calls this attribute `content_class`. Article XIV says to reuse an existing name for the same idea before coining one, so the modal uses it too.

## The button's non-daisyUI attributes go

- `full` becomes `block`, daisyUI's name for the same modifier.
- `align` sets a flex justification. That is a layout class, so it passes through `class`.
- `reverse` puts the icon after the text. Putting the icon in the default slot does the same with no attribute.
- `condition` wraps the button in an `if`. The caller's template can do that itself.

All four removals follow tie-break 3. They break existing callers, which is acceptable below 0.1.0 as long as the CHANGELOG lists them.

## The swap's control attributes reach the checkbox

The swap's wrapper is a `<label>` and its control is a hidden checkbox. `checked`, `disabled`, `name` and `value` are meaningless on the label and would silently do nothing there, so they go to the checkbox. `label` gives the checkbox its accessible name. Both slots stay in the accessibility tree (daisyUI hides the inactive one visually only), so the label text cannot name the control reliably.

## The swap documents the theme toggle

The theme controller is excluded because it is a class on an input. The most common place adopters use it is on a swap's checkbox, a sun and moon toggle. The swap therefore accepts extra classes on its checkbox, and its documentation shows the toggle. The exclusion and its reason are recorded where adopters will look for the component.

## The FAB trigger is explicitly focusable

daisyUI's FAB opens while its trigger has focus, and its examples use `<div tabindex="0" role="button">` because some browsers do not focus a clicked `<button>`. Article XV requires the trigger to come from `<c-button>`, so the trigger is a `<c-button>` with `tabindex="0"`, the same approach the current dropdown takes. The implementation should confirm in a real browser that a click opens the FAB.

## Priorities

Priorities reflect how many adopters need each component: the button everywhere (P1), the modal and dropdown in most applications (P2), the swap and FAB in some (P3).
