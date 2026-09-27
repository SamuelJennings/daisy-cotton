# Research: Layout components

Evidence behind the plan. Third-party behaviour is cited from what this repository resolves: django-cotton 2.6.1 and django-cotton-gallery 1.0.0 in `.venv/lib/python3.13/site-packages/`, and daisyUI 5.7.46, the build `https://cdn.jsdelivr.net/npm/daisyui@5` serves to the demo (`demo/templates/django_cotton_gallery/_extra_head.html`).

## R1. daisyUI 5 class names for this feature

Read from the served `daisyui.css` (5.7.46):

| Component | Classes |
|---|---|
| divider | `divider`, `divider-horizontal`, `divider-vertical`, `divider-start`, `divider-end`, `divider-neutral`, `divider-primary`, `divider-secondary`, `divider-accent`, `divider-info`, `divider-success`, `divider-warning`, `divider-error` |
| drawer | `drawer`, `drawer-toggle`, `drawer-content`, `drawer-side`, `drawer-overlay`, `drawer-button`, `drawer-open`, `drawer-end` |
| footer | `footer`, `footer-title`, `footer-horizontal`, `footer-vertical`, `footer-center` |
| hero | `hero`, `hero-content`, `hero-overlay` |
| indicator | `indicator`, `indicator-item`, `indicator-start`, `indicator-center`, `indicator-end`, `indicator-top`, `indicator-middle`, `indicator-bottom` |
| join | `join`, `join-item`, `join-horizontal`, `join-vertical` |
| mask | `mask`, `mask-circle`, `mask-decagon`, `mask-diamond`, `mask-heart`, `mask-hexagon`, `mask-hexagon-2`, `mask-pentagon`, `mask-squircle`, `mask-star`, `mask-star-2`, `mask-triangle`, `mask-triangle-2`, `mask-triangle-3`, `mask-triangle-4`, `mask-half-1`, `mask-half-2` |
| stack | `stack`, `stack-top`, `stack-bottom`, `stack-start`, `stack-end` |
| mockup | `mockup-browser`, `mockup-browser-toolbar`, `mockup-code`, `mockup-phone`, `mockup-phone-camera`, `mockup-phone-display`, `mockup-window` |

Fourteen mask shapes, matching the spec's clarification. `mask-square` does not exist in daisyUI 5.

## R2. The drawer's focus ring belongs to an opener inside the page content

```
.drawer-toggle{appearance:none;opacity:0;width:0;height:0;position:fixed}
.drawer-toggle:focus-visible~.drawer-content label.drawer-button{outline-offset:2px;outline:2px solid}
.drawer-open>.drawer-toggle{display:none; …}
```

The Tab stop is the invisible `drawer-toggle` checkbox, and Space toggles it natively. daisyUI draws the focus ring on a `<label class="drawer-button">` that is a descendant of `.drawer-content`, a later sibling of the checkbox. So `drawer.button` must emit a `<label>`, not a `<button>`, and the gallery example places it inside the page content. An opener placed outside the drawer still opens it (`for` works across the document, which is what scenario 2 needs), but its focus ring does not show. The description says so.

A `<label>` is not itself focusable, and adding `role="button" tabindex="0"` would make a second Tab stop that Space and Enter cannot activate without a script. FS-003's plan reaches the same ruling for the dock's drawer toggle (its D9, in the open pull request #101). On main the dock toggle still carries `role="button" tabindex="0"`. The keyboard path is the checkbox.

`drawer-open` hides the checkbox, so a permanently open drawer has no Tab stop for the toggle. This is correct: there is nothing to toggle.

## R3. The gallery cannot set a boolean attribute to a breakpoint

`django_cotton_gallery/core/preview/tag_builder.py:81-88`: a `boolean` prop is emitted bare when its control is on and omitted otherwise. No control produces `horizontal="lg"`. The `example:` annotation key is parsed (`core/annotations.py:227`) but 1.0.0 renders it nowhere on the detail page (the only template reference is the annotation builder, `static/django_cotton_gallery/js/ui-bits.js:635`).

What the gallery does render verbatim is a slot's default content (`tag_builder.py:94-105`, `build_default_tag` line 51). A responsive example therefore has to live in slot content, written as a caller would write it. The drawer's page slot is where one naturally sits: a page with a sidebar, a join and a footer, which is SC-006's page. See D8.

## R4. A component's own `id` and required props in the preview

A required prop with no default renders empty in the default preview (`build_default_tag`, line 41: only declared defaults are used). The drawer's `id` is required, so its preview works once the viewer sets `id` in the playground. The drawer's example slot names a fixed id (`demo-drawer`) for its opener, and the description tells the viewer to set that id. FS-003's megamenu does the same.

## R5. Cotton reads a component's children in the caller's context

`django_cotton/templatetags/_component.py:86` renders the default slot before the component's own `<c-vars>` are extracted (FS-003 research R1). Nothing in this feature needs a child to read its parent: `drawer.button` is given the drawer's id, `indicator.item` is placed through the parent's named slot, and `join` needs `join-item` on the child, which the caller passes as `class`.

None of this feature's templates call another component inside their own markup. The same fall-through reaches them from the page itself, though: a declared name with no default resolves from the caller's template context when the caller leaves it out (`_vars.py:80-82`, `_component.py:111-118`), while a quoted default shadows it (`_vars.py:73-77`, the reason `card/index.html:12` declares `title=""`). Hence the empty defaults in plan.md and D9.

## R6. A caller's `role` without a duplicate attribute

A name declared in `<c-vars>` is removed from `{{ attrs }}` (`django_cotton/templatetags/_vars.py:78` and `:82`, `attrs.exclude_from_string_output`, the mechanism the existing `class` merge relies on, `tests/test_class_attribute_merge.py`). Declaring `role` on `divider` and `join` and writing `role="{% if role %}{{ role }}{% else %}…{% endif %}"` gives exactly one `role` attribute whichever wins. The same mechanism `aria-label` uses on FS-003's landmarks (its research R2).

## R7. Detecting an unlabelled divider

`{{ slot }}` is a string. `{% if not text and not slot.strip %}` treats whitespace-only slot content as no label, which is what `<c-divider>\n</c-divider>` produces. Django resolves `slot.strip` as a no-argument method call.

## R8. The accessibility check (SC-004) runs against the running gallery

Same setting as FS-003 (its research R7 and D5): Playwright and Chromium are available locally through the shared test bundle, CI has no browser step and adding one means editing `.github/workflows/tests.yml`, which automation does not do in this repository. The check runs once, against every gallery entry this feature touches, with axe-core loaded into each preview and a scripted keyboard walk of the drawer: Tab reaches the toggle, Space opens and closes it, the opener shows an outline while the toggle has focus. The result goes in the pull request's test evidence. The suite asserts what rendered markup can show: roles, names, `aria-hidden`, `tabindex`, `alt`.
