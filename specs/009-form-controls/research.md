# Research: Core form controls

Evidence behind the plan. Third-party behaviour is cited from what this repository resolves: django-cotton 2.7.2 and django-cotton-gallery 1.0.0 in `.venv/lib/python3.13/site-packages/`, and daisyUI 5.7.46, the build `https://cdn.jsdelivr.net/npm/daisyui@5` serves to the demo.

## R1. daisyUI 5 class names for this feature

Read from the served `daisyui.css` (5.7.46):

| Component | Classes |
|---|---|
| input | `input`, `input-ghost`, `input-{neutral,primary,secondary,accent,info,success,warning,error}`, `input-{xs,sm,md,lg,xl}` |
| textarea | `textarea`, `textarea-ghost`, `textarea-{…eight colours…}`, `textarea-{xs…xl}` |
| select | `select`, `select-ghost`, `select-{…eight colours…}`, `select-{xs…xl}` |
| checkbox | `checkbox`, `checkbox-{…eight colours…}`, `checkbox-{xs…xl}` |
| radio | `radio`, `radio-{…eight colours…}`, `radio-{xs…xl}` |
| toggle | `toggle`, `toggle-{…eight colours…}`, `toggle-{xs…xl}` |
| range | `range`, `range-{…eight colours…}`, `range-{xs…xl}`, `range-vertical` |
| file input | `file-input`, `file-input-ghost`, `file-input-{…eight colours…}`, `file-input-{xs…xl}` |
| label | `label`, `floating-label` |
| fieldset | `fieldset`, `fieldset-legend` (and a legacy `fieldset-label` that daisyUI's class reference no longer lists) |

The eight colours are the same for every control: neutral, primary, secondary, accent, info, success, warning, error. Every class the spec names exists, including `range-vertical`. Only input, textarea, select and file input have a ghost style. `fieldset-label` is left out: daisyUI's own reference names `label` for the description line, so SC-001 does not reach it.

## R2. daisyUI's markup

From daisyUI's class reference (`runs/daisy-cotton/daisyui-llms.txt`):

- **Input**: `<input type="{type}" class="input {MODIFIER}">`. "If the input contains more than one element, use the `input` class on the parent element": `<label class="input"><span class="label">…</span><input type="text"></label>`. The inner `<input>` carries no class.
- **Select**: `<select class="select {MODIFIER}">` around its options. The wrapped form is the same as the input's, with `select` on the parent.
- **Textarea, file input, checkbox, radio, toggle, range**: the native element carrying the class. The range "must specify `min` and `max`".
- **Label**: a `<span class="label">` inside an input's box, or a `<label class="label">`. The floating form is `<label class="floating-label"><input … class="input"><span>{text}</span></label>`, the field first and the span after it. "Do not add the `input` class to the label."
- **Fieldset**: `<fieldset class="fieldset"><legend class="fieldset-legend">{title}</legend>{CONTENT}<p class="label">{description}</p></fieldset>`, and "the fieldset can have all types of elements as direct children".
- **Checkbox wrapped in a label**, from daisyUI's fieldset examples: `<label class="label"><input type="checkbox" class="checkbox">Remember me</label>`, the control before its text.

## R3. What daisyUI's label CSS does

- `.label` is `display:inline-flex; white-space:nowrap`. A long description or error line does not wrap. That is daisyUI's styling of its own markup; the fieldset's description says a project adds `whitespace-normal` through the named slot when it needs long lines to wrap.
- `.label:is(.input>*, .select>*)` draws the divider between inline content and the field, so start and end content written as `<span class="label">` gets daisyUI's inline-label look with no extra class.
- `.floating-label>span` is positioned over the field and floats while `:focus-within`, or while the wrapper has no `input:placeholder-shown`/`textarea:placeholder-shown`. A `<select>` never matches `:placeholder-shown`, so a floating label around a select always sits in its floated position. Only the span has to be a direct child.
- A floating label around an input that uses `start` or `end` would put the input's own `<label>` wrapper inside the floating `<label>`, and a label inside a label is invalid HTML. The label's description says to float a label only around an unwrapped control.

## R4. Cotton behaviour this plan relies on

Checked by rendering through the compiler (probe templates, removed afterwards):

- A bare boolean attribute (`checked`, `disabled`, `required`) given to a component and not declared reaches `{{ attrs }}` as a bare attribute: `<c-x name="q" checked disabled required aria-invalid="true">` renders `name="q" checked disabled required aria-invalid="true"`. So the native states pass through with nothing declared (FR-005, FR-009).
- A named slot declared in `<c-vars>` with an empty default (`start=""`) is empty unless the caller fills it, and `{% if start or end %}` chooses the wrapped form (the navbar's pattern).
- `:errors="['a', 'b']"` arrives as a list (probe; Django's `ErrorList` is a `list` subclass whose `__str__` renders HTML, `django/forms/utils.py`, so it never equals its own `stringformat:"s"`). `errors="one"` arrives as a string. `{% if errors == errors|stringformat:"s" %}` tells the two apart, as `form.field` did, and a Django `ErrorList` takes the list branch, iterates its messages and autoescapes each one. An empty list renders nothing.
- A declared name with a default does not fall through to a page variable of the same name: a context carrying `type`, `start` and `errors` leaves the component's own defaults in place (FS-006 research R3).
- Slot content keeps the whitespace the caller wrote, so `<c-textarea>  Hello  </c-textarea>` gives the value `  Hello  `. The textarea writes `{{ slot }}` with nothing around it, and the description says the slot is the value exactly as written.
- `<c-file-input>` resolves to `file_input.html`, the rule FS-007 recorded for `hover_gallery.html`.

## R5. The gallery shows one preview per component

As FS-008 research R7: gallery 1.0.0 builds each preview as one tag of that component with only declared defaults, `select[…]` props get the variants matrix and boolean props a toggle. A control's bare preview therefore has no accessible name (nothing declared carries one) and no disabled or invalid state (those are pass-through attributes). FS-008 D5 settled that reading: SC-003's "every gallery example" is the composed examples, and a bare preview's description tells the developer what to type.

The composed examples go where an application writes them: inside the fieldset's own `@slot` example. A fieldset's `@slot:legend` example fills its legend, and a fieldset nested inside the slot can carry an `id`, a description and errors, which the preview's own fieldset cannot (an `id` default would give every fieldset the same id). The fieldset entry has no `select` prop, so it has no variants matrix and its ids are rendered once.

## R6. `size` on the input and the select

HTML has a native `size` on `<input>` (visible width in characters) and `<select>` (visible rows, turning it into a list box). Article XIII gives `size` to daisyUI's size modifier, so the component declares it and a native value such as `size="4"` emits no class and never reaches the element. daisyUI's select does not style the list-box form, and width is a Tailwind class. The descriptions say `size` is daisyUI's scale.

## R7. Accessible names

- A `<label for>` names the control whose `id` matches. A `<label>` wrapping a control names it with the label's text content, including text outside any span. The floating label's `<span>` is inside the `<label>`, so it names the input.
- A wrapped input (`<label class="input">`) is itself a label of its input. Its text (the start and end content, such as "https://") joins the name given by a separate `<label for>`. That is daisyUI's documented markup for inline labels and the spec's (FR-008), so it is recorded rather than worked around.
- `role="switch"` on `<input type="checkbox">` is allowed by ARIA in HTML, and the checked state maps to on and off.
- A `<legend>` names its `<fieldset>` group, and radio buttons in the group are announced within it (US5-4).

## R8. The browser checks

As FS-008 research R9: Playwright and Chromium are available locally, CI has no browser step, and the check runs once at the walkthrough against the running gallery: axe-core on each touched entry, plus scripted checks.

- Every control in the fieldset composition has an accessible name, and the described ones expose the description and error text as their description.
- Tab reaches each control and shows a focus indicator. Space toggles the checkbox and the toggle, the arrow keys move within the radio group, and the toggle is exposed with role `switch` and its checked state.
- The group of radio buttons is exposed inside a group named by its legend.
- The floating label's text is the input's name.

The bare control previews are unnamed by construction (R5) and are recorded as expected, not as failures. The suite asserts what rendered markup can show: elements, classes, attributes, element order, ids and `for`/`aria-describedby` links.
