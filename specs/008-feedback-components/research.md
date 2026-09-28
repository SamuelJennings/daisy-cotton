# Research: Feedback components

Evidence behind the plan. Third-party behaviour is cited from what this repository resolves: django-cotton 2.7.2 and django-cotton-gallery 1.0.0 in `.venv/lib/python3.13/site-packages/`, and daisyUI 5.7.46, the build `https://cdn.jsdelivr.net/npm/daisyui@5` serves to the demo.

## R1. daisyUI 5 class names for this feature

Read from the served `daisyui.css` (5.7.46):

| Component | Classes |
|---|---|
| alert | `alert`, `alert-info`, `alert-success`, `alert-warning`, `alert-error`, `alert-soft`, `alert-outline`, `alert-dash`, `alert-horizontal`, `alert-vertical` |
| loading | `loading`, `loading-spinner`, `loading-dots`, `loading-ring`, `loading-ball`, `loading-bars`, `loading-infinity`, `loading-xs` to `loading-xl` |
| progress | `progress`, `progress-neutral`, `progress-primary`, `progress-secondary`, `progress-accent`, `progress-info`, `progress-success`, `progress-warning`, `progress-error` |
| radial progress | `radial-progress` |
| skeleton | `skeleton`, `skeleton-text` |
| toast | `toast`, `toast-top`, `toast-middle`, `toast-bottom`, `toast-start`, `toast-center`, `toast-end` |
| tooltip | `tooltip`, `tooltip-content`, `tooltip-open`, `tooltip-top`, `tooltip-bottom`, `tooltip-left`, `tooltip-right`, `tooltip-start`, `tooltip-center`, `tooltip-end`, `tooltip-primary`, `tooltip-secondary`, `tooltip-accent`, `tooltip-info`, `tooltip-success`, `tooltip-warning`, `tooltip-error` |

The alert's direction classes ship behind `sm:` to `xl:` in the build, so a breakpoint value emits a class that exists. The tooltip has seven colours (no `neutral`), progress has eight. Every class the spec names exists.

## R2. daisyUI's markup

From daisyUI's class reference (`runs/daisy-cotton/daisyui-llms.txt`):

- **Alert**: `<div role="alert" class="alert {MODIFIER}">`, one class from each of style, colour and direction. `sm:alert-horizontal` is daisyUI's responsive pattern.
- **Loading**: `<span class="loading {MODIFIER}">`, one style and one size. With no style class the spinner is drawn.
- **Progress**: `<progress class="progress {MODIFIER}" value="50" max="100">`. With no `value` the browser shows an indeterminate bar and daisyUI animates it.
- **Radial progress**: `<div class="radial-progress" style="--value:70;" aria-valuenow="70" role="progressbar">70%</div>`. `--size` and `--thickness` are CSS variables, not classes.
- **Skeleton**: `<div class="skeleton h-32 w-32">`, and `<div class="skeleton skeleton-text">Loading data...</div>` for text.
- **Toast**: `<div class="toast {MODIFIER}">` around its content, one placement class per axis.
- **Tooltip**: a `tooltip` wrapper around the trigger, with the hint in a `data-tip` attribute or a `tooltip-content` child.

## R3. What daisyUI's tooltip CSS needs

The rule that shows the hint is `.tooltip:is([data-tip]:not([data-tip=""]), :has(.tooltip-content:not(:empty))):is(.tooltip-open, :hover, :has(:focus-visible)) > .tooltip-content`. So:

- `tooltip-content` must be a **direct child** of the `tooltip` root. Its position among the children does not matter.
- It shows on hover, on `tooltip-open`, and when anything inside the wrapper has `:focus-visible`. Keyboard focus on a focusable trigger shows it with no script (US3-2).
- A hidden hint is `opacity: 0`, not `display: none`, so the text stays in the accessibility tree whether or not it is shown.
- An empty `tooltip-content` shows nothing, so a tooltip with neither `tip` nor `content` is inert.

## R4. Alpine attributes and translated names reach `<c-button>`

Checked against django-cotton 2.7.2 by rendering through the compiler:

- `<c-button @click="show = false">` and `<c-button x-on:click="show = false">` both arrive on the `<button>` unchanged through `{{ attrs }}`.
- `{% trans "Dismiss" as dismiss_label %}` before the tag, then `aria-label="{{ dismiss_label }}"`, puts the translated string on the button.

So the alert's dismiss control can be a `<c-button>` with no change to the button.

## R5. Values that are falsy but meaningful

A progress value of `0` is a real value. Given as a literal attribute (`value="0"`) Cotton passes the string `"0"`, which is truthy. Given dynamically (`:value="done"` with `done = 0`) it passes the integer `0`, which a bare `{% if value %}` treats as absent and would turn a 0% bar into an indeterminate one. The progress template tests for an empty value (`{% if value != "" %}` or equivalent), not truthiness, and a test covers `:value` with `0`. The radial progress always writes its value, so it is unaffected.

## R6. A declared name falls through to the page's context

As FS-006 research R3 and FS-007 research R5: a name declared in `<c-vars>` with no default resolves from the caller's template context when the caller leaves it out. `value`, `label`, `text`, `content`, `icon`, `role`, `max` and `placement` are all names a page is likely to have in its context. Every name this feature declares gets a default, and each component has one test rendering it inside a context that carries its declared names.

## R7. The gallery shows one preview per component

As FS-007 research R6: gallery 1.0.0 builds each preview as one tag of that component with only declared defaults, and `example:` is unused. Scenarios that need several instances or markup beside the component (a tooltip whose trigger references its id, loading inside a button, a composed skeleton card, progress at several values) go inside the slot example of a component that holds free markup, where an application would write them, and the component's `@description` names that entry. Fixed-value props typed `select[…]` get the gallery's variants matrix, and boolean props are toggled in the props panel.

## R8. The radial progress's `style`

The component writes `--value` into `style` itself. A caller's `style` is declared in `<c-vars>` and appended after it, so both survive (FR-021). As with the countdown in FS-007, autoescaping keeps `value` inside the attribute but not inside the `--value` declaration: a string holding `;` adds CSS declarations. The description says `value` is a number from 0 to 100 and never unvalidated user input.

## R9. The browser checks

As FS-007 research R7: Playwright and Chromium are available locally, CI has no browser step, and the check runs once at the walkthrough against the running gallery: axe-core on each touched entry, plus scripted checks.

- **Alert**: clicking the dismiss button and pressing Enter on it removes the alert (Alpine is loaded by the demo). The button shows a focus indicator.
- **Tooltip**: hovering the trigger and tabbing to it both make `tooltip-content` visible (computed opacity 1). The accessibility snapshot contains the hint text, and the linked example exposes it as the trigger's description.
- **Loading, progress, radial progress**: the accessibility snapshot gives each a name, and progress and radial progress a value.
- **Toast**: dismissing one alert in a toast leaves the others where they were.
- **Skeleton**: the snapshot contains the text skeleton's text and nothing from a shape skeleton.

The suite asserts what rendered markup can show: elements, classes, roles, names, `aria-*`, `id`, `style`, element order.
