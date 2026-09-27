# Research: Content display components

Evidence behind the plan. Third-party behaviour is cited from what this repository resolves: django-cotton 2.6.1 and django-cotton-gallery 1.0.0 in `.venv/lib/python3.13/site-packages/`, and daisyUI 5.7.46, the build `https://cdn.jsdelivr.net/npm/daisyui@5` serves to the demo (`demo/templates/django_cotton_gallery/_extra_head.html`).

## R1. daisyUI 5 class names for this feature

Read from the served `daisyui.css` (5.7.46):

| Component | Classes |
|---|---|
| card | `card`, `card-body`, `card-title`, `card-actions`, `card-border`, `card-dash`, `card-side`, `card-xs`, `card-sm`, `card-md`, `card-lg`, `card-xl`, `image-full` |
| table | `table`, `table-zebra`, `table-pin-rows`, `table-pin-cols`, `table-xs`, `table-sm`, `table-md`, `table-lg`, `table-xl` |
| badge | `badge`, `badge-neutral`, `badge-primary`, `badge-secondary`, `badge-accent`, `badge-info`, `badge-success`, `badge-warning`, `badge-error`, `badge-outline`, `badge-dash`, `badge-soft`, `badge-ghost`, `badge-xs`, `badge-sm`, `badge-md`, `badge-lg`, `badge-xl` |
| collapse | `collapse`, `collapse-title`, `collapse-content`, `collapse-arrow`, `collapse-plus`, `collapse-open`, `collapse-close` |
| avatar | `avatar`, `avatar-group`, `avatar-online`, `avatar-offline`, `avatar-placeholder` |
| stat | `stats`, `stats-horizontal`, `stats-vertical`, `stat`, `stat-title`, `stat-value`, `stat-desc`, `stat-figure`, `stat-actions` |
| list | `list`, `list-row`, `list-col-grow`, `list-col-wrap` |
| timeline | `timeline`, `timeline-start`, `timeline-middle`, `timeline-end`, `timeline-box`, `timeline-vertical`, `timeline-horizontal`, `timeline-compact`, `timeline-snap-icon` |
| kbd | `kbd`, `kbd-xs`, `kbd-sm`, `kbd-md`, `kbd-lg`, `kbd-xl` |
| status | `status`, `status-neutral`, `status-primary`, `status-secondary`, `status-accent`, `status-info`, `status-success`, `status-warning`, `status-error`, `status-xs`, `status-sm`, `status-md`, `status-lg`, `status-xl` |

`collapse-open` and `collapse-close` are the two classes SC-001 excludes. `list-col-grow` and `list-col-wrap` go on a row's children, so they are reached through the documented example, not an attribute (FR-028).

## R2. A hyphenated attribute must be declared hyphenated

Probed with a throwaway component under Cotton 2.6.1:

| Declared in `<c-vars>` | Caller writes | Variable | Left in `{{ attrs }}` |
|---|---|---|---|
| `pin_rows=""` | `pin-rows` | `pin_rows` = True | `pin-rows` (leaks onto the element) |
| `pin-rows=""` | `pin-rows` | `pin_rows` = True | nothing |
| `pin-rows=""` | `pin-rows="lg"` | `pin_rows` = "lg" | nothing |

Cotton exposes a hyphenated attribute under its underscored name either way, but strips it from the pass-through only when the declaration is spelled the way the caller writes it. `image-full`, `pin-rows`, `pin-cols` and `snap-icon` are therefore declared hyphenated and read underscored. `tests/test_declared_attributes.py` already accepts both spellings (`spellings = {name, name.replace("-", "_")}`).

## R3. A declared name falls through to the page's context

As FS-004 research R5 and FS-005 research R5: a name declared in `<c-vars>` with no default resolves from the caller's template context when the caller leaves it out. `title`, `caption`, `value`, `src` and `start` are all names a page is likely to have in its context. Every name this feature declares, `class` included, gets `=""`, and each component has one test rendering it inside a context that carries its declared names.

## R4. The timeline connector

daisyUI's CSS styles `<hr>` inside a timeline item (`.timeline :where(hr){background-color:var(--color-base-300);height:.25rem}`) and places the first and last `hr` of an item at the start and end of the grid. It does nothing to hide a connector before the first item or after the last one: its own examples leave the `<hr>` out of those two items by hand.

A Cotton component cannot know its position among its siblings. So every `<c-timeline.item>` emits both connectors, and each connector hides itself at the ends of the list with a named Tailwind group, `group/item` on the item and `group-first/item:hidden` / `group-last/item:hidden` on its two `hr`s. An unnamed `group` would match any enclosing `.group` on the page. Hidden `hr`s still count for daisyUI's `hr:first-child` / `hr:last-child` placement. Both connectors carry `aria-hidden="true"`, since an `<hr>` is otherwise announced as a separator (FR-032). These are Tailwind utilities written literally in the template, so a host whose Tailwind build scans the package templates generates them, like every other utility the templates already use (spec Assumptions).

## R5. The collapse on `<details>`

daisyUI 5 supports the collapse on `<details>` directly: its open-state selectors include `.collapse[open]`, and `summary::-webkit-details-marker` is hidden. The browser gives `<summary>` its keyboard behaviour (Enter and Space toggle) and exposes the disclosure's expanded state. The `name` attribute on `<details>` makes items sharing a name an exclusive group in browsers that support it (Chromium 120+, Safari 17.2+, Firefox 130+).

daisyUI removes `outline` on menu summaries only (`.menu … summary`), not on `.collapse-title`, so the browser's own focus ring should show on a collapse's summary. The accessibility run (R8) confirms it on the real gallery entry. If it does not show, the fix is a `focus-visible` outline utility on the summary.

## R6. A table caption needs an id to name its region

A focusable scrolling wrapper named by the table's caption needs `aria-labelledby` pointing at the caption's id, and a table with no `id` of its own has nothing unique to build one from. `aria-label="{{ caption }}"` is not a substitute: the caption can be a slot holding markup, and a caller's own `aria-label` would then be a second attribute of the same name on the wrapper.

FS-005 (open as #103) adds a `unique_id` simple tag to `daisy_cotton/templatetags/daisy_cotton.py` for the same reason (its research R6). This feature adds the identical function, same name, signature, body and docstring, with the same two tests, so whichever of the two lands second reconciles identical code.

## R7. The card inside the modal

`modal.html` on main wraps its content in `<c-card>` and forwards `actions`, `footer` and `footer_end` as card slots, with `title`, `icon` and everything else reaching the card through `:attrs`. After US1 the card has no `icon`, `footer` or `footer_end`, and an undeclared `icon` would land on the card root as a raw HTML attribute. The spec's edge case keeps the modal rendering its title, body and actions as before. FS-005 replaces the modal's card entirely, and whichever lands second reconciles the modal (decisions.md, "The card follows daisyUI's structure").

## R8. The accessibility check runs against the running gallery

As FS-004 research R8 and FS-005 research R9: Playwright and Chromium are available locally, and CI has no browser step. The check runs once at the walkthrough, with axe-core loaded into each touched gallery preview, plus a scripted keyboard walk: the collapse (Tab to the summary, focus ring visible, Enter expands and `expanded` reads true, Enter collapses), the accordion (opening a second item closes the first; a second group is unaffected), and the table (Tab reaches the wrapper, its focus indicator is visible, ArrowRight scrolls it; if no indicator shows, the same `focus-visible` outline remedy as R5). The accordion walks run against the card entry, which holds the two groups (plan "Compositions"). The suite asserts what rendered markup can show: elements, classes, roles, names, `aria-*`, `tabindex`, `open`, `name`.
