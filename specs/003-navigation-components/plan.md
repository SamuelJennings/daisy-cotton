# Implementation Plan: Navigation components

**Branch**: `003-navigation-components` | **Date**: 2026-09-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-navigation-components/spec.md`

## Summary

Five new Cotton components (`menu`, `navbar`, `tabs`, `steps`, `megamenu`) and three existing ones brought in line (`breadcrumbs`, `dock`, `link`). Each renders daisyUI 5's documented markup with the constitution's attribute vocabulary, accessible roles, names and states, no script, and gallery annotations that show every variant and state. Every template is markup plus `<c-vars>`. The only Python the feature uses is the two helper tags that already exist (`responsive`, `variation`).

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added.

**Storage**: none

**Testing**: pytest + pytest-django through the verify flow. Rendered markup is parsed with BeautifulSoup (in the test bundle) or `HTMLParser`, as the existing component tests do.

**Target Platform**: any host project running daisyUI 5

**Project Type**: Django package (templates only) with a demo project

**Constraints**: no JavaScript, no stylesheet, no literal colours, no class daisyUI does not define for the component (FR-002, FR-004)

**Scale/Scope**: 8 components, 16 templates (11 new, 5 changed)

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Test-First | Every acceptance scenario gets a test written before the template that satisfies it. Pre-existing tests the spec's breaking changes invalidate are changed under D4, not silently. | Pass |
| II Simplicity | Templates only. The existing `responsive` and `variation` tags cover every modifier. No new tag, no new module. | Pass |
| III Anti-Abstraction | No base template, no shared include across components. Each item repeats its own few lines of markup. | Pass |
| V Security | Every value reaches the page through `{{ }}` autoescaping. Ids built from caller input are attribute values, never markup. | Pass |
| VI Documentation | README component list, the pagination note and CHANGELOG entries land in the story that introduces each name. | Pass |
| VII Dependency discipline | No new runtime or dev dependency (research R7). | Pass |
| VIII i18n | Landmark default names and the megamenu toggle label are `{% trans %}`. | Pass |
| X Test structure | One test module per component, `Test<Subject>` classes, registered as non-mirror paths like the existing component tests. | Pass |
| XII Agnostic | Nothing names a host project. Gallery examples use neutral copy. | Pass |
| XIII Semantic palette | Colours only through `variant`, validated against daisyUI's list. | Pass |
| XIV Attribute vocabulary | `variant`, `size`, daisyUI modifier names as booleans, `class` merged, the rest through `{{ attrs }}`. The two coined names are argued in D1 and D2. | Pass |
| XV Composition | Icons through `<c-icon>`, the megamenu toggle through `<c-button>`. | Pass |
| XVI Gallery annotations | Every new template annotated. Fixed-value props typed `select[…]` (research R4). `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below:

- **Modifiers.** `size` goes through `{% variation size "<base>" "xs,sm,md,lg,xl" %}`. `variant` goes through `{% variation variant "<base>" "neutral,primary,secondary,accent,info,success,warning,error" %}`, so an unknown value adds nothing (Edge Cases). A direction attribute that takes a boolean or a breakpoint goes through `{% responsive … %}`, as `divider` does.
- **Landmarks** (`breadcrumbs`, `dock`, `megamenu`, `navbar`) render as `<nav>`, declare `aria-label` in `<c-vars>` with no default, and write `aria-label="{% if aria_label %}{{ aria_label }}{% else %}{% trans "<Default>" %}{% endif %}"` (research R2). Defaults: `Breadcrumbs`, `Dock`, `Site`, `Main`.
- **Items.** The root of a list item is its `<li>`, and `class` and `{{ attrs }}` land there (decisions.md, "Attributes on list items go to the item's root"). A component whose root is a link or button (`link`, `dock.item`, `tabs.tab`) keeps them on that element.
- **Nested components are called with `only`.** A component called inside another component's own template reads the host's `<c-vars>` from the shared context (research R1, second half), so `<c-icon>` would pick up an item's `class` and `<c-button>` the megamenu's `size`, `full` and any `href` in the page. Every nested call passes what it needs explicitly and ends in `only` (D7).
- **Icons** inside an item are `<c-icon name="{{ icon }}" aria-hidden="true" only />`, so the item's text is its name.
- **Current and disabled.** `active` on a link adds `aria-current="page"`. `disabled` on a link drops `href` and adds `role="link" aria-disabled="true"`: without `href` it leaves the Tab order with no `tabindex`, and the explicit role keeps it announced as a disabled link (D7). `disabled` on a button or input uses the native `disabled` attribute.
- **Buttons** are always `type="button"`.

### Menu (US1)

`menu/index.html` — `<ul class="menu {size} {horizontal} {paged} {class}" {{ attrs }}>{{ slot }}</ul>`. `<c-vars size horizontal paged class />`. `horizontal` goes through `responsive` (`horizontal` → `menu-horizontal`, `horizontal="lg"` → `lg:menu-horizontal`). No direction class otherwise: daisyUI's menu is vertical by default.

`menu/item.html` — `<li class="{disabled: menu-disabled} {class}" {{ attrs }}>` holding an `<a>` when `href` is given, else a `<button type="button">`. `<c-vars text href active disabled icon class aria-label />`. `aria-label`, when given, is written on the inner link or button, the element that needs the name, so an icon-only item can be named (Edge Cases, D7). `active` adds `menu-active` on the inner element (daisyUI's own placement) and `aria-current="page"` on a link. Content: icon, `text`, then `{{ slot }}`.

`menu/title.html` — `<li class="menu-title {class}" {{ attrs }}>{{ text }}{{ slot }}</li>`. `<c-vars text class />`. No interactive element.

`menu/submenu.html` — `<li class="{class}" {{ attrs }}><details{% if open %} open{% endif %}><summary>{icon}{{ text }}</summary><ul>{{ slot }}</ul></details></li>`. `<c-vars text open icon class />`. Nests inside itself.

### Navbar (US2)

`navbar.html` — a single file, no parts. `<nav class="navbar {class}" aria-label=… {{ attrs }}>`, then `<div class="navbar-start">{{ start }}</div>` only when `start` is given, likewise `center` and `end`, then `{{ slot }}`. `<c-vars class aria-label start="" center="" end="" />`: the empty defaults stop a page-context variable of the same name from emitting a section, and a real named slot still wins (D7). Named slots `start`, `center`, `end`.

### Link and breadcrumbs (US3)

`link.html` — `<c-vars href text variant hover class />` with no `href` default. `<a{% if href %} href="{{ href }}"{% endif %} class="link {variant} {hover: link-hover} {class}" {{ attrs }}>`. `variant` validated through `variation`.

`breadcrumbs/index.html` — `<nav class="breadcrumbs {class}" aria-label=… {{ attrs }}>`, `text-sm` removed (FR-017). `<c-vars items class aria-label />`. The `items` loop keeps `only`.

`breadcrumbs/item.html` — `<li class="{class}" {{ attrs }}>` holding `<a href>` with `text` then `{{ slot }}`, or, without `href`, `<span aria-current="page">` with the same content. The `daisy-cotton-breadcrumb-text` span goes (FR-002, D3). An item without `href` is the current page, which is what its annotation already says. Built from `items`, only the last item is hrefless in a well-formed trail, so FR-016's "final item" holds.

### Tabs (US4)

`tabs/index.html` — `<div{% if not links %} role="tablist"{% endif %} class="tabs {box} {border} {lift} {size} {placement} {class}" {{ attrs }}>{{ slot }}</div>`. `<c-vars size box border lift placement links class />`. `placement` is `select['top','bottom']` through `variation placement "tabs" "top,bottom"`.

`tabs/tab.html` — three shapes, chosen by the attributes given (FR-019):

- `href` → `<a href class="tab {active: tab-active} {disabled: tab-disabled} {class}" {{ attrs }}>` with `aria-current="page"` when active. Disabled drops `href` and adds `aria-disabled="true"`.
- `name` → `<input type="radio" name="{{ name }}" class="tab {class}" aria-label="{{ text }}" {checked when active} {disabled} {{ attrs }} />` followed by `<div class="tab-content">{{ slot }}</div>`. The panel is in the slot. The shared group name is the caller's, given to each tab (D1, research R1).
- otherwise → `<button type="button" role="tab" class="tab …" aria-selected="{{ active|yesno:'true,false' }}" {disabled} {{ attrs }}>`.

`<c-vars text href name="" active disabled class />`, the empty `name` default for the same reason as the navbar's slots (D7). Link tabs sit in a root given `links` (D1). Radio tabs keep daisyUI's documented `role="tablist"` root, as scenario 6 requires, and the walkthrough's accessibility run decides whether that stands (D8).

### Dock (US5)

`dock/index.html` — `<nav class="dock {size} {class}" aria-label=… {{ attrs }}>{{ slot }}</nav>`. `bg-transparent backdrop-blur` removed (FR-021). `<c-vars size class aria-label />`.

`dock/item.html` — the three existing branches kept. The toggle branch drops `role="button" tabindex="0"`: a focused `<label>` cannot be activated from the keyboard without a script, and keyboard users reach the drawer through its own focusable `drawer-toggle` checkbox (D9). Each branch adds `dock-active` when active, `aria-current="page"` only on the link, `type="button"` on the button, the icon through `<c-icon … aria-hidden="true" />`, and the label inside `dock-label`. The toggle branch's `aria-label` is written only when `label` is given. With no label, the caller's `aria-label` reaches the element through `{{ attrs }}` (Edge Cases).

### Steps (US6)

`steps/index.html` — `<ol class="steps {vertical} {horizontal} {class}" {{ attrs }}>{{ slot }}</ol>`. `<c-vars vertical horizontal class />`. `vertical` through `responsive` (`steps-vertical`), `horizontal` through `responsive` (`lg:steps-horizontal`). Given together they give scenario 2.

`steps/step.html` — `<li class="step {variant} {class}"{% if content %} data-content="{{ content }}"{% endif %}{% if current %} aria-current="step"{% endif %} {{ attrs }}>`, then `<span class="step-icon"><c-icon … aria-hidden="true" /></span>` when `icon` is given, then `text` and `{{ slot }}`. `<c-vars text variant current content icon class />`.

### Megamenu (US7)

`megamenu/index.html` — `id` is required (`@prop id:text | required`). Renders, in order:

1. `<c-button class="sm:hidden" type="button" popovertarget="{{ id }}" text="{% trans "Menu" %}" only />` — the small-screen toggle, through `<c-button>` (FR-003, FR-025). `only` keeps the megamenu's own `size` and `full`, and any `href` in the page, off the toggle (D7).
2. `<nav id="{{ id }}" popover class="megamenu max-sm:megamenu-vertical {wide} {full} {size} {class}" aria-label=… {{ attrs }}><span class="megamenu-active"></span>{{ slot }}</nav>`.

`<c-vars id wide full size class aria-label />`.

`megamenu/item.html` — `<button type="button" popovertarget="{{ megamenu }}-{{ key }}">{{ text }}</button><div id="{{ megamenu }}-{{ key }}" popover class="{class}" {{ attrs }}>{{ slot }}</div>`. `<c-vars megamenu key text class />`, both `megamenu` and `key` required. The panel id is built from the megamenu's id (FR-026), and the item is given that id because it cannot read it (research R1, D2). The expanded state is the browser's (research R6).

### Gallery entries (FR-007, FR-008)

Every template carries `@description`, a `@prop` per `<c-vars>` name (fixed-value props as `select[…]` with daisyUI's full list), and `@slot` / `@slot:name` per slot, per Article XVI. The index template's default `@slot` carries a one-line example showing every state: for `menu`, a title, an active link, a disabled item and an open two-level submenu. For `tabs`, a link set with one active and one disabled. For `steps`, four steps, two coloured, one current, one with custom content, one with an icon. For `megamenu`, three items holding a menu. Its description gives daisyUI's ten-item limit and tells the viewer to set `id` in the playground, since a required prop has no default for the preview to use. Item templates show their own states through their boolean props. Folder components' pages are at `/django-cotton-gallery/<name>/index/` until #96 is fixed (research R3).

### Documentation

- `README.md`: the component list gains `menu`, `navbar`, `tabs`, `steps` and `megamenu`, each in its story, and a line that pagination has no component because daisyUI builds it from `join` and `btn` (US1).
- `CHANGELOG.md` `[Unreleased]`: `Added` per new component. `Changed` per breaking change, with what a host project writes to keep the old result: `link` without `href` (write `href="#"`), breadcrumbs `text-sm` and dock `bg-transparent backdrop-blur` (pass them through `class`), breadcrumb item attributes landing on the `<li>` (write the link in the item's slot), and the breadcrumb text span's class (FR-010).

## Project Structure

### Documentation (this feature)

```text
specs/003-navigation-components/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templates/cotton/
├── menu/index.html, item.html, title.html, submenu.html   # new (US1)
├── navbar.html                                            # new (US2)
├── link.html                                              # changed (US3)
├── breadcrumbs/index.html, item.html                      # changed (US3)
├── tabs/index.html, tab.html                              # new (US4)
├── dock/index.html, item.html                             # changed (US5)
├── steps/index.html, step.html                            # new (US6)
└── megamenu/index.html, item.html                         # new (US7)
tests/
├── test_menu.py, test_navbar.py, test_tabs.py, test_steps.py, test_megamenu.py, test_dock.py   # new
├── test_link.py, test_breadcrumbs_href_attribute.py       # changed under D4
pyproject.toml                                             # the new test modules in non-mirror-paths
README.md, CHANGELOG.md
```

**Structure Decision**: templates and their tests only. New components with parts use the folder layout the package already uses (research R3).

## Story order

One worktree, stories built in dispatch batches on the same branch. Each story touches its own templates and test module, and appends to `README.md`, `CHANGELOG.md` and `pyproject.toml`'s `non-mirror-paths`, which is why batches run one after another rather than in parallel worktrees.

1. US3 (link and breadcrumbs) and US5 (dock): the breaking changes to shipped components.
2. US1 (menu) and US2 (navbar).
3. US4 (tabs), US6 (steps) and US7 (megamenu).

## Complexity Tracking

None.
