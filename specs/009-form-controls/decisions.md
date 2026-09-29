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

Article XIII sends `class` to the root element and everything else through `attrs`. When the text input or select is wrapped, the root is the `<label>` that carries daisyUI's `input` or `select` class, which is where layout classes such as `w-full` must go. Form attributes (`name`, `value`, `required`, `id`) do nothing on a label, so they go to the control. FS-005 made the same split for the swap's wrapper and checkbox.

## `start` and `end` for the slots

daisyUI has no name for the content inside an input's box. Article XIII says to reuse an existing name for the same idea before coining one. The navbar already uses `start` and `end` for content at either side of it.

## The toggle is a switch

A toggle looks like an on-off switch, and assistive technology has a role for that. `role="switch"` on the checkbox makes screen readers say "on" and "off" rather than "checked", which matches what sighted users see. It is valid on a checkbox and needs no script.

## The range defaults `min` and `max`

daisyUI's rules say a range must have both. The browser's own defaults are 0 and 100, so emitting them when the caller gives none changes nothing a user sees and keeps the markup within daisyUI's rules.

## No `form.` prefix

Every other component is named after its daisyUI component alone (`button`, `modal`). `form.field` was the only grouped name, and it is going. The new tags are `<c-input>`, `<c-select>` and so on. `<c-input>` takes daisyUI's own name for the text input.

## Priorities

Priorities reflect how many adopters need each component, and what must ship together. The text input, the label and the fieldset replace `form.field` and are needed in nearly every form, so they are P1 along with the removal itself. The textarea, select, checkbox, radio and toggle appear in most forms beyond the simplest (P2). The file input and range appear in fewer (P3).

## D1 — The spec still holds after FS-001 to FS-008

Eight features were delivered after this spec landed. Read against their specs: FS-002 annotated `form.field`, which this feature removes, as its assumptions expected. FS-003 gave the navbar the `start` and `end` slots whose names this spec reuses, and FS-006 used the same names for the timeline. FS-004's join already describes an input joined with a button. FS-005 kept theme-controller as a class added to a checkbox, radio or toggle, which these controls take through `class`. FS-005, FS-006 and FS-008 use `label` as an accessible-name attribute on components that name themselves. The controls here take no such attribute, because the spec names them through `<c-label>`, `aria-label` or `aria-labelledby`. None of them changes a behaviour this spec describes.

**ADR:** none — a check made once for this feature.

## D2 — The labelled, disabled and invalid examples live in the fieldset's entry

The gallery previews each component once with declared defaults, so a bare control has no name and no disabled or invalid state. Every control is therefore also shown in one composition inside the fieldset's own `@slot` example, in nested fieldsets, which is where an application writes its controls. A nested fieldset can carry the `id` that the description and error ids derive from, which the preview's own fieldset cannot. Each story adds its controls to the composition. The bare previews stay unnamed by construction, as FS-008 D5 recorded for the progress bar.

**ADR:** none — follows the gallery approach FS-006 and FS-008 set.

## D3 — The errors share one element and one id

The spec gives the errors a single derived id. A list of messages renders as one line each, so the lines sit inside one `<div>` carrying `<id>-errors`, and a control names all of them with that one id in `aria-describedby`. The alternative, one id per line, would make the caller's `aria-describedby` depend on how many errors there are.

**ADR:** none — local to the fieldset template.

## D4 — `form.field` is removed last

The removal is P1, but its CHANGELOG examples use every control, and an example may only use components that exist. So US3 is built after US6, in the same pull request as the components that replace it. The `Added` line listing the first 21 components keeps `form.field`, and the new `Removed` entry says where it went. Nothing has been released yet, so both entries describe the same unreleased version. ADR 0001's list of components that call `<c-icon>` drops `form.field`, which never called it.

**ADR:** none — ordering and a documentation edit local to this feature.

## D5 — Design review applied

The review approved the plan with three medium and three low findings, all applied as plan and task edits. The errors' wrapper carries `grid`, because daisyUI's description line is `inline-flex` and only the fieldset's direct children stack. `type` and the toggle's `role` are written by the template and documented as not for the caller, since a second one would be a duplicate attribute. SC-004 is shown by mapping each removed `form.field` test to the CHANGELOG example that rebuilds it. The ADR edit only removes `form.field` from the list. The removal test asserts `TemplateDoesNotExist` naming `form/field`. The no-script, no-invalid-state-of-its-own and page-context rules are each one parametrised test in `tests/test_form_controls.py` rather than a copy per component. The review's notes also brought in the CHANGELOG's form-rendering sentence, the roadmap's fieldset line and a sentence on whitespace-only slots.

**ADR:** none — local to this feature's templates, tests and documentation.

## D6 — The described field gets its own fieldset in the gallery composition

As built, the composition's `account-email` fieldset held every control, so the email's description and error rendered below all of them. That fieldset now holds only the email field it describes, and the other examples follow it inside the outer fieldset. The outer preview's description sample changed so it no longer repeats the inner one. It was an annotation-only edit, made directly at the story's acceptance rather than dispatched again.

**ADR:** none — a gallery example.

## D7 — `<c-file_input>` inside gallery-scanned markup

The gallery's catalog registers a component under its file stem — `file_input`, not `file-input` — and its unknown-component lint check compares a source tag against that literal set with no hyphen/underscore normalization, so `<c-file-input>` inside the fieldset's `@slot` composition read as a reference to a component that does not exist (3 errors, `cotton_lint --warnings-as-errors`), even though Cotton itself resolves the hyphen form to `file_input.html` at render time and `tests/test_file_input.py`/`tests/test_form_controls.py` use `<c-file-input>` freely. This is the same rule spec 008-feedback-components D6 recorded for `<c-radial_progress>` and spec 007-animated-display-components D10/D11 recorded for `<c-hover_gallery>`/`<c-hover_3d>`/`<c-text_rotate>`. The fieldset's composition is written `<c-file_input>` for this reason; the README and CHANGELOG still name it `file-input`, the display form the gallery and daisyUI's own naming use. `<c-range>` has no hyphen in its tag, so it needed no such rewrite.

**ADR:** none — a lint tool's known-tags limitation, not a design choice; recorded so a future template composing with `file-input` in scanned markup does not rediscover it.
