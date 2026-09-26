# Decisions: Core form controls

Ambiguities in issue #18 that were resolved while writing the spec, with the reasoning behind each. The short form of every one is in `spec.md` under *Clarifications*.

## `form.field` is removed rather than kept alongside

`form.field` renders daisyUI's fieldset, label and one of seven controls from a single tag, switching markup on `type`. The README's first scope rule gives each base daisyUI component one Cotton component and nothing else, so a component that combines three of them has no place here. Keeping it as a convenience beside the new components would also go against tie-break 3 (fewer attributes) and tie-break 2 (leave composition to the project). The package is below 0.1.0, so the removal is acceptable with a CHANGELOG entry that shows the replacement for every case.

## Labels come from `<c-label>`, in daisyUI's three shapes

daisyUI uses the `label` class in three places: a `<label>` above a control inside a fieldset, a `<label>` wrapping a checkbox and its text, and a `<span>` inside an input's box. It uses `floating-label` for the floating form. The first two and the floating form are all a `<label>` element, which is what ties text to a control for assistive technology (G3), so `<c-label>` covers them.

The inline form is a `<span>`, not a `<label>`, and it sits inside the element that carries the `input` class. A `<label>` there would nest one label inside another, which is invalid. So the inline form is content in the input's `start` or `end` slot, and the documentation shows it written as daisyUI writes it.

## The legend does not stand in for a label

daisyUI's simplest fieldset example puts a single input under a legend with no label. A legend names the group, not the control inside it, so a screen reader announces that input with no name. The documentation keeps the legend for groups (a radio set, an address) and gives every control its own `<c-label>`. This costs one more tag per field and is what G3 asks for.

## Help text and errors belong to the fieldset

daisyUI describes a fieldset as a legend, content and a description line, which is where `form.field` put its help text and errors. Putting `description` and `errors` on the fieldset keeps them in daisyUI's structure. `description` is daisyUI's own word for the line. `errors` keeps `form.field`'s name and its acceptance of a string or a list, so upgrading code changes as little as possible.

Linking the messages to the control needs an id on each message. The fieldset cannot know which control it holds, so it derives the ids from its own `id` and the caller names them in the control's `aria-describedby`. That keeps every component to plain values and one job each.

## The invalid state is set on the control by the caller

`form.field` switched the control to its error colour and set `aria-invalid` whenever it had errors. Once the fieldset and the control are separate components, the fieldset cannot reach into its slot to change the control. Inferring it any other way would need shared state between components. The caller already knows when a field is invalid, so it sets `variant="error"` and `aria-invalid="true"` on the control. Both are ordinary attributes with their usual meaning.

## Attributes that do not carry over

- `hide-label`: a visually hidden label is `class="sr-only"` on `<c-label>`, a Tailwind class the project already has.
- `wrapper-class`: the fieldset is now its own component, so its `class` does this.
- `prelabel` and `postlabel`: the `start` and `end` slots, which also take icons and keyboard hints.
- The required asterisk: dropped. daisyUI has no such marker, and the control's `required` attribute is what assistive technology reads. A visible marker is text the project writes.

## `class` and the other attributes split on a wrapped input

Article XIV sends `class` to the root element and everything else through `attrs`. When the text input or select is wrapped, the root is the `<label>` that carries daisyUI's `input` or `select` class, which is where layout classes such as `w-full` must go. Form attributes (`name`, `value`, `required`, `id`) do nothing on a label, so they go to the control. FS-005 made the same split for the swap's wrapper and checkbox.

## `start` and `end` for the slots

daisyUI has no name for the content inside an input's box. Article XIV says to reuse an existing name for the same idea before coining one. The navbar already uses `start` and `end` for content at either side of it.

## The toggle is a switch

A toggle looks like an on-off switch, and assistive technology has a role for that. `role="switch"` on the checkbox makes screen readers say "on" and "off" rather than "checked", which matches what sighted users see. It is valid on a checkbox and needs no script.

## The range defaults `min` and `max`

daisyUI's rules say a range must have both. The browser's own defaults are 0 and 100, so emitting them when the caller gives none changes nothing a user sees and keeps the markup within daisyUI's rules.

## No `form.` prefix

Every other component is named after its daisyUI component alone (`button`, `modal`). `form.field` was the only grouped name, and it is going. The new tags are `<c-input>`, `<c-select>` and so on. `<c-input>` takes daisyUI's own name for the text input.

## Priorities

Priorities reflect how many adopters need each component, and what must ship together. The text input, the label and the fieldset replace `form.field` and are needed in nearly every form, so they are P1 along with the removal itself. The textarea, select, checkbox, radio and toggle appear in most forms beyond the simplest (P2). The file input and range appear in fewer (P3).
