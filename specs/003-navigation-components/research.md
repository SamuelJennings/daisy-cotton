# Research: Navigation components

Evidence behind the plan. Third-party behaviour is cited from the packages this repository resolves (`.venv/lib/python3.13/site-packages/`), not from their documentation.

## R1. A Cotton child cannot read its parent's attributes

`django_cotton/templatetags/_component.py:86` renders a component's children (`default_slot = self.nodelist.render(context)`) in the caller's context, before the parent's own `<c-vars>` are extracted (line 92 onwards). An item inside `<c-tabs>` or `<c-megamenu>` therefore never sees an attribute given to the parent.

The parent's attributes are reachable during that render through `cotton_data["stack"]` (same file, lines 31–38), but that is Cotton's internal bookkeeping, not an interface, and nothing in this package reads it.

**Consequence.** Anything an item needs from its parent is given to the item. This decides two designs:

- a radio tab is given its group's `name`, the way every native radio input is;
- a megamenu item is given the megamenu's id, so it can build its panel id from it (FR-026).

## R2. Hyphenated attribute names are declared as written and read with underscores

`django_cotton/templatetags/__init__.py:225` exposes every attribute with `-` replaced by `_`. `form/field.html` already declares `help-text` and reads `{{ help_text }}`. A landmark component can therefore declare `aria-label` in `<c-vars>`, which removes it from `{{ attrs }}`, and read `{{ aria_label }}` to fall back to its translated default. Without the declaration a caller's `aria-label` would reach the element a second time through `{{ attrs }}`, after the component's own default, and the browser would keep the first one. That is the case for `breadcrumbs` today, so FR-006's "the caller can override" does not yet hold there.

## R3. Folder components have no gallery page at their own address

Issue #96 (open): django-cotton-gallery 1.0.0 lists `menu/index.html` as `menu`, but `core/catalog/resolver.py:17` (`resolve`) builds only `menu.html`, so `/django-cotton-gallery/menu/` returns 404 and `/django-cotton-gallery/menu/index/` renders. 1.0.0 is the latest release on PyPI. `tests/test_gallery_links.py` skips these cases with a reason naming #96.

**Consequence.** New components keep the repository's folder layout (`<name>/index.html` plus part templates), per the issue's ruling and the instruction not to reshape templates around the defect. Their gallery pages are reached at `/django-cotton-gallery/<name>/index/` until a gallery release fixes the resolver. `navbar` has no parts and is a single file, so its page works at its own address.

## R4. The gallery's variants matrix is driven by `select` props

`django_cotton_gallery/core/schemas.py:13` defines the prop types `text`, `number`, `boolean` and `select`, and the detail page offers a variants matrix (`templates/django_cotton_gallery/detail.html:176`) over a prop's listed options. A gallery entry shows every variant and size (FR-008) when those props are typed `select['…']` with the full list, and every state when the default `@slot` content (which the preview renders) includes an item in each state. Open pull request #100 makes `select` typing a written rule for fixed-value props. This feature follows it, so both land consistently whichever merges first.

## R5. daisyUI 5 markup and class names

From daisyUI's component reference (`llms.txt`, daisyUI 5):

| Component | Classes | Documented markup |
|---|---|---|
| breadcrumbs | `breadcrumbs` | `<div class="breadcrumbs"><ul><li><a>` |
| dock | `dock`, `dock-label`, `dock-active`, `dock-xs`…`dock-xl` | `<div class="dock">` of `<button>`s |
| link | `link`, `link-hover`, `link-neutral`, `link-primary`, `link-secondary`, `link-accent`, `link-success`, `link-info`, `link-warning`, `link-error` | `<a class="link">` |
| megamenu | `megamenu`, `megamenu-active`, `megamenu-wide`, `megamenu-full`, `megamenu-vertical`, `megamenu-xs`…`megamenu-xl` | toggle `<button class="btn sm:hidden" popovertarget="ID">`, then `<div class="megamenu max-sm:megamenu-vertical" id="ID" popover>` holding `<span class="megamenu-active">` and pairs of `<button popovertarget="P">` + `<div id="P" popover>`; at most 10 popovers |
| menu | `menu`, `menu-title`, `menu-disabled`, `menu-active`, `menu-paged`, `menu-xs`…`menu-xl`, `menu-horizontal`, `menu-vertical` (script-only: `menu-dropdown`, `menu-dropdown-toggle`, `menu-dropdown-show`, `menu-focus`) | `<ul class="menu"><li><button>`; `<details>` for collapsible submenus; `lg:menu-horizontal` for responsive |
| navbar | `navbar`, `navbar-start`, `navbar-center`, `navbar-end` | `<div class="navbar">` |
| steps | `steps`, `step`, `step-icon`, `step-neutral`…`step-error`, `steps-vertical`, `steps-horizontal` | `<ul class="steps"><li class="step step-primary">`; `data-content` for custom content |
| tabs | `tabs`, `tab`, `tab-content`, `tabs-box`, `tabs-border`, `tabs-lift`, `tabs-xs`…`tabs-xl`, `tab-active`, `tab-disabled`, `tabs-top`, `tabs-bottom` | `<div role="tablist" class="tabs"><button role="tab" class="tab">`, or radio inputs `<input type="radio" name="G" class="tab" aria-label="…">` each followed by `<div class="tab-content">` |

daisyUI styles these by class, so the element carrying the class can be the semantic one: `<nav>` for the landmark components and `<ol>` for steps.

## R6. A popover invoker exposes its expanded state without a script

A `<button popovertarget="P">` is mapped to an expanded/collapsed state that follows `P`'s popover state by the browser (HTML-AAM, "button element" mapping with the `popovertarget` attribute; shipped in current Chromium, Firefox and Safari). FR-005's "exposes whether its panel is open" is met by the native attribute. A static `aria-expanded` written by the template would go stale the moment the panel opened, so the template writes none.

## R7. The accessibility check (SC-004) runs against the running gallery, not in CI

Playwright 1.63 is installed through the shared test bundle and its Chromium build is present locally. The shared test workflow can install browsers (`install-playwright` input), but switching that on means editing `.github/workflows/tests.yml`, which automation does not do in this repository without the maintainer's say-so, and axe-core would arrive as a new dependency.

SC-004 names no CI requirement. The check runs once, against every gallery entry in the group on the running demo, with axe-core loaded into the page and the keyboard walk scripted: Tab reaches every enabled item and skips the disabled ones, Enter or Space opens a submenu and a megamenu panel, and the arrow keys move between radio tabs. The result goes in the pull request's test evidence. The suite covers what can be asserted from rendered markup: roles, names, states, native elements, and no `tabindex="-1"` on an enabled item.
