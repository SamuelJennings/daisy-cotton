# Research: Action components

Evidence behind the plan. Third-party behaviour is cited from what this repository resolves: django-cotton 2.6.1 and django-cotton-gallery 1.0.0 in `.venv/lib/python3.13/site-packages/`, and daisyUI 5.7.46, the build `https://cdn.jsdelivr.net/npm/daisyui@5` serves to the demo (`demo/templates/django_cotton_gallery/_extra_head.html`).

## R1. daisyUI 5 class names for this feature

Read from the served `daisyui.css` (5.7.46):

| Component | Classes |
|---|---|
| button | `btn`, `btn-neutral`, `btn-primary`, `btn-secondary`, `btn-accent`, `btn-info`, `btn-success`, `btn-warning`, `btn-error`, `btn-xs`, `btn-sm`, `btn-md`, `btn-lg`, `btn-xl`, `btn-outline`, `btn-dash`, `btn-soft`, `btn-ghost`, `btn-link`, `btn-active`, `btn-disabled`, `btn-wide`, `btn-block`, `btn-square`, `btn-circle` |
| dropdown | `dropdown`, `dropdown-top`, `dropdown-bottom`, `dropdown-left`, `dropdown-right`, `dropdown-start`, `dropdown-center`, `dropdown-end`, plus `dropdown-content`, `dropdown-hover`, `dropdown-open`, `dropdown-close`, which belong to the methods this feature does not use (SC-001) |
| fab | `fab`, `fab-flower`, `fab-close`, `fab-main-action` |
| modal | `modal`, `modal-box`, `modal-action`, `modal-backdrop`, `modal-top`, `modal-middle`, `modal-bottom`, `modal-start`, `modal-end`, plus `modal-open` and the legacy `modal-toggle` |
| swap | `swap`, `swap-on`, `swap-off`, `swap-indeterminate`, `swap-rotate`, `swap-flip`, `swap-active` |
| theme controller | `theme-controller` |

`modal-open` is a state class daisyUI treats the same as `[open]` (`.modal.modal-open,.modal[open],.modal:popover-open,…`). The `open` attribute on `<dialog>` covers it, so `modal-open` needs no attribute of its own.

## R2. The popover dropdown's CSS

```
.dropdown{position-area:var(--anchor-v,block-end) var(--anchor-h,span-inline-end);display:inline-block;position:relative}
.dropdown[popover],.dropdown .dropdown-content{z-index:999; …}
&.dropdown-close,&:not(.dropdown-open,:popover-open){opacity:0;display:none; …}
.dropdown-top{--anchor-v:block-start}
.dropdown-end{--anchor-h:span-inline-start}
```

In the popover method the `dropdown` class and its placement classes sit **on the popover panel itself**, not on a wrapper, and placement is `position-area` driven by custom properties the placement classes set. `position-area` positions against the panel's anchor, which daisyUI's documented markup names explicitly: `style="anchor-name:--x"` on the button and `style="position-anchor:--x"` on the panel. The panel's placement classes therefore go on the element carrying `popover`.

The popover is in the top layer while open, so it paints above an open modal, which is also in the top layer but was opened earlier (Edge Cases).

`popovertarget` on a `<button>` gives, with no script: open and close on click, Enter and Space; close on Escape and on a click outside (light dismiss); focus returned to the trigger when the popover closes with focus inside it; and the trigger's expanded state exposed to assistive technology (HTML-AAM maps a popover invoker's state to `aria-expanded`). This is what FR-017 asks for.

Probed in Chromium 153 with the served CSS and exactly that markup (`anchor-name` on the button, `position-anchor` on a `<div popover class="dropdown …">`): Tab then Enter opened the panel, the accessibility tree reported the button `expanded: false` before and `expanded: true` after, and Escape closed it with focus left on the button. With no placement class the panel sat directly below the button, start-aligned. `dropdown-top dropdown-end` put it above, end edges aligned. `dropdown-right dropdown-center` put it to the right, vertically centred.

A `<button>` with no `type` inside a `<form>` is a submit button, and HTML ignores `popovertarget` on a submit button in a form. The trigger therefore carries `type="button"`. The FAB's trigger does too, or clicking it inside a form would submit the form.

## R3. The gallery puts a `@trigger` inside the component

`django_cotton_gallery/core/preview/tag_builder.py:62-71`: `_compose` builds `inner = trigger + named slots + default slot` and renders `<c-name …>{inner}</c-name>`. A trigger annotation is prepended to the component's default slot.

For the drawer that works, because the default slot is the visible page. For the modal it does not: the trigger lands inside the `<dialog>`, which is closed and hidden, so nothing in the preview can open it. This is what main does today. The modal's raw preview (`/django-cotton-gallery/modal/raw/`) renders `<button onclick="myModal.showModal()">Open</button>` inside the closed dialog's card, and the dialog has no id, because `example:` values are never rendered (FS-004 research R3).

No annotation places content outside the component tag. So the modal's gallery entry cannot open the dialog from a trigger button in gallery 1.0.0. What it can do is show the trigger's markup in the `@trigger` annotation, and let the viewer switch `open` on to see each placement, the close button and the actions row rendered. See D3.

## R4. Cotton's `:attrs` wins over literal attributes on the same tag

Probed with a throwaway component holding `<c-button size="lg" circle tabindex="0" :attrs="attrs" />`: a caller's `size="sm"` rendered `btn-sm`, and with no caller `size` it rendered `btn-lg`. Attributes spread through `:attrs` replace literal ones of the same name. So the FAB can give its trigger `size="lg"` and `circle` as defaults, and a caller's own `size` still reaches the button.

The same probe showed `circle` reaching the button as a raw HTML attribute. It is not declared on the button today; this feature declares it.

## R5. A declared name falls through to the page's context

As FS-004 research R5 and its D9: a name declared in `<c-vars>` with no default resolves from the caller's template context when the caller leaves it out, and a quoted default shadows it. `card/index.html` declares `title=""` for this reason. The button reads `href` without declaring it, so a page with an `href` variable in its context turns every `<c-button>` on it into a link with no `href` attribute. Every name this feature declares, except `class`, gets `=""`.

## R6. A unique panel id needs a template tag

Django templates have no way to make an id unique per render. FR-019 needs one for every dropdown whose caller gives no `id`, and the id is used twice (the panel's `id` and the trigger's `popovertarget`) plus once more for the anchor name. A `simple_tag` in the existing `daisy_cotton` library, `{% unique_id "dropdown" as panel_id %}`, returns `dropdown-` plus eight hex characters of a `uuid4`. It is the feature's only new Python. `forloop.counter`-style counters would repeat across two includes on one page, and a hash of the slot would repeat for two dropdowns with the same menu.

## R7. The FAB opens on focus, so the trigger must be the first child and carry `tabindex`

```
.fab>[tabindex]:first-child{ … display:grid;position:relative}
.fab:focus-within>:nth-child(n+2){visibility:visible; … opacity:1}
:is(.fab:focus-within:has(.fab-close),.fab:focus-within:has(.fab-main-action))>[tabindex]{opacity:0;rotate:90deg}
.fab .fab-close,.fab .fab-main-action{inset-inline-end:0;position:absolute;bottom:0}
.fab-flower>:nth-child(n+7){display:none}
```

The trigger must be the FAB's first child and carry a `tabindex` attribute, or daisyUI's rules neither style it nor hide it when `fab-close` or `fab-main-action` takes its place. Every other child is hidden until focus is inside the FAB. `fab-close` and `fab-main-action` are placed over the trigger. The flower arrangement shows at most four actions beside the trigger and the close or main action, and hides the rest.

Safari does not focus a `<button>` on click unless it carries an explicit `tabindex` (why daisyUI's examples use `<div tabindex="0" role="button">`). A `<c-button tabindex="0">` is a real button that Safari will focus. Probed in Chromium with the served CSS: Tab to the trigger made the actions visible once the 0.2 s transition ran, and two more Tabs reached each action in order. A scripted walk has to wait out the transition, or its next Tab lands on an action that is still hidden. Chromium is the only browser this checkout has (`~/.cache/ms-playwright/`), so the Safari half is checked by reading the markup, not by running it.

## R8. The swap's checkbox is not hidden, only unstyled

```
.swap{cursor:pointer; … display:inline-grid;position:relative}
.swap input{appearance:none;border:none}
.swap>*{grid-row-start:1;grid-column-start:1; …}
```

daisyUI does not hide the checkbox. It removes its appearance and stacks it under the two faces, so it stays in the tab order and Space toggles it. daisyUI draws no focus style for a swap, but the browser's own ring shows: probed in Chromium with the served CSS, Tab focused the checkbox, which the grid stretches to the swap's size (31×24 px for a text swap), with the default `outline-style: auto`, and Space checked it. The swap needs no focus class of its own. The accessibility run (R9) re-checks it on the real gallery entry.

## R9. The accessibility check runs against the running gallery

Same setting as FS-004 research R8: Playwright and Chromium are available locally, CI has no browser step, and adding one means editing `.github/workflows/tests.yml`, which automation does not do here. The check runs once, against every gallery entry this feature touches, with axe-core loaded into each preview, plus a scripted keyboard walk of the dropdown (Tab to the trigger, Enter opens, `aria-expanded` reads true, Escape closes and focus is back on the trigger), the swap (Tab reaches the checkbox, Space flips it, the focus ring is visible) and the FAB (Tab to the trigger opens it, Tab reaches each action). The modal is opened through `showModal()` from the test script and checked for its name, Escape and focus return. The result goes in the pull request's test evidence. The suite asserts what rendered markup can show: classes, roles, names, `aria-*`, `tabindex`, `popovertarget`, ids.
