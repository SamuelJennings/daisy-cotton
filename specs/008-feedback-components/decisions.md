# Decisions: Feedback components

Ambiguities in issue #17 that were resolved while writing the spec, with the reasoning behind each. The short form of every one is in `spec.md` under *Clarifications*.

## The alert keeps its Alpine dismiss and `delay`

The package ships no JavaScript, and the alert's dismiss button and `delay` both run on Alpine.js attributes that the host project's own Alpine picks up. Removing them would break every existing caller for no gain, and the README already documents the requirement. Two things change. The button is drawn by `<c-button>`, as Article XV requires, and it gets a translatable accessible name with its ✕ glyph hidden, because a bare "✕" is announced as "multiplication x".

`delay` stays because toasts that clear themselves are common and the attribute already exists. An alert that disappears on a timer can fail people who read slowly or use a screen reader, so the documentation warns against it for errors and for anything the reader has to act on, rather than the component refusing it.

## `role` stays `alert`, and callers can change it

daisyUI's markup uses `role="alert"`, which interrupts a screen reader. That suits errors and not much else. A caller-given `role` replaces the default rather than being written as a second attribute, so `role="status"` gives a polite announcement for success messages. The default stays daisyUI's, per tie-break 1.

## No `variant` on loading, radial progress or skeleton

daisyUI defines no colour classes for these three and colours them with text or background utilities instead. Article XIV defines `variant` as the selector for daisyUI's colour modifier, so a `variant` here would have to invent classes, which FR-003 forbids, or map to utilities, which is a parallel vocabulary tie-break 1 rules out. Callers pass `text-primary` and similar through `class`.

## Loading animations are booleans

Article XIV makes style modifiers boolean attributes named as daisyUI names them. The layout group used a single `shape` attribute for the mask, but that was for fourteen shapes with names like `hexagon-2`. The six loading animations are plain words (`spinner`, `dots`, `ring`, `ball`, `bars`, `infinity`), so the general rule applies.

## Radial progress sizing through CSS variables

daisyUI sizes the radial progress with `--size` and `--thickness` and has no size classes for it. Article XIV reserves `size` for the `xs`–`xl` scale, so a `size` attribute taking a length would break that promise. Callers set the variables with arbitrary-property classes (`[--size:8rem]`), which pass through `class` with no attribute at all. The component writes `--value` into `style` itself, so a caller's `style` is combined with it rather than overwriting it.

## `label` is the accessible-name attribute

Loading, progress and radial progress convey state only visually, so each needs a name. The swap in the action group already calls its accessible-name attribute `label`, and Article XIV says to reuse an existing name for the same idea. Loading can default to "Loading" because that is always true. A progress bar's meaning depends on the task, so it has no default and the documentation asks for one.

## The skeleton's `text` does both jobs

daisyUI's modifier is `skeleton-text`, so Article XIV points to a `text` attribute. Elsewhere in the package `text` is the content string (button, dropdown). The two readings don't collide here: a text skeleton always has text content, so `text="Loading data…"` both applies the modifier and supplies the content, and bare `text` applies the modifier to slot content. Each call reads naturally under either expectation.

A shape skeleton is hidden from assistive technology because an empty grey box says nothing. A text skeleton stays readable because its text is the only signal that content is on its way.

## The toast has no live region

A toast only positions its children. The alerts inside already carry `role="alert"` or `role="status"`, which are live regions themselves. Adding `aria-live` to the wrapper would announce each message twice in some screen readers. Messages rendered with the page on first load are not announced by any live region, which is a limit of the platform rather than something the wrapper could fix.

## The tooltip renders its text as an element

daisyUI offers two ways to give a tooltip its text: a `data-tip` attribute, drawn by CSS, and a `tooltip-content` element. CSS-generated text is not reliably exposed to assistive technology, so G3 rules out `data-tip`. The component always renders `tooltip-content` with `role="tooltip"`, filled from `tip` or the `content` slot.

Linking the tooltip to its trigger takes `aria-describedby` on the trigger, and the trigger arrives in the slot, where the component cannot touch it. The component therefore puts the caller's `id` on the content element, and the documentation shows the trigger referencing it. That is an exception to Article XIV's "everything else goes to the root", made for the same reason the swap sends control attributes to its checkbox: on the wrapper, the id would be useless.

Escape-to-dismiss, which WCAG 1.4.13 asks of content shown on hover or focus, needs a script. The package ships none, so it is listed as a known limit and left to the project.

## Placement values

daisyUI calls both the tooltip's and the toast's class groups "placement". Following the dropdown in the action group, each takes one value combining a side or position with an alignment, such as `placement="bottom end"`.

## Priorities

Priorities reflect how many adopters need each component. The alert and loading indicator appear in nearly every application (P1). Tooltips, progress bars and toasts appear in most (P2). Skeletons are polish (P3). Progress and radial progress share a story because they show the same thing in two shapes.
