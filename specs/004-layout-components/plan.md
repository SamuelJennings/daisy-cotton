# Implementation Plan: Layout components

**Branch**: `004-layout-components` | **Date**: 2026-09-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-layout-components/spec.md`

## Summary

Ten new Cotton components (`drawer`, `drawer.button`, `footer`, `footer.nav`, `hero`, `indicator`, `indicator.item`, `join`, `mask`, `stack`) and six existing ones brought to the same bar (`divider`, `mockup.browser`, `mockup.code`, `mockup.code.line`, `mockup.phone`, `mockup.window`). Each renders daisyUI 5's documented markup with the constitution's attribute vocabulary, semantic colours only, no script, and gallery annotations. Every template is markup plus `<c-vars>`. The only Python the feature uses is the two helper tags that already exist (`responsive`, `variation`).

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added.

**Storage**: none

**Testing**: pytest + pytest-django. Components are rendered through the Cotton compiler as a caller's template would be (the `cotton_render_string_soup` fixture in `tests/conftest.py`), never by rendering the component file directly, which skips `<c-vars>` extraction.

**Target Platform**: any host project running daisyUI 5

**Project Type**: Django package (templates only) with a demo project

**Constraints**: no JavaScript, no stylesheet, no literal colours, no class daisyUI does not define for the component (FR-002, FR-004, FR-005)

**Scale/Scope**: 16 components, 16 templates (10 new, 6 changed)

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Test-First | Every acceptance scenario gets a test written before the template that satisfies it. The two pre-existing `mockup.code.line` tests the approved spec invalidates change under D2, not silently. | Pass |
| II Simplicity | Templates only. `responsive` and `variation` cover every modifier. No new tag, no new module. | Pass |
| III Anti-Abstraction | No base template, no shared include. | Pass |
| V Security | Every value reaches the page through `{{ }}` autoescaping. `src`, `alt`, `url`, `title` and ids are attribute values or text, never markup. | Pass |
| VI Documentation | README component list and CHANGELOG entries land in the story that introduces or changes each name. | Pass |
| VII Dependency discipline | No new runtime or dev dependency. | Pass |
| VIII i18n | The drawer toggle's and overlay's names are `{% trans %}`. No other string is written by the package. | Pass |
| X Test structure | One test module per component group, `Test<Subject>` classes, registered in `non-mirror-paths` like the existing component tests. | Pass |
| XII Agnostic | Gallery examples use neutral copy. | Pass |
| XIII Semantic palette | `mockup.phone` loses `text-white` and `bg-neutral-900`. Colours only through validated `variant` and `base-*` classes. | Pass |
| XIV Attribute vocabulary | `variant`, `placement`, `horizontal`, `vertical`, `open`, `shape`, merged `class`, the rest through `{{ attrs }}`. `role` declared where the component sets one (D5). | Pass |
| XV Composition | No template copies another component's markup. | Pass |
| XVI Gallery annotations | Every template annotated, fixed-value props typed `select[…]` (`placement`, `variant`, `shape`, `half`), `@trigger` on the drawer, `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below:

- **Modifiers.** `variant` and `placement` go through `{% variation … %}` against daisyUI's list for that component (research R1), so an unknown value adds nothing and nothing raises (Edge Cases, FR-004). `horizontal`, `vertical` and `open` go through `{% responsive … %}`: bare gives the class, a breakpoint gives `<bp>:<class>`. `responsive` is narrowed so a string that is not one of `sm`, `md`, `lg`, `xl`, `2xl` gives nothing (FR-004, D10).
- **Root.** Every component declares `class`, merges it into the root's class list, and spreads `{{ attrs }}` on the root (FR-003).
- **Empty defaults.** Every declared name except `class` is declared with an empty default (`role=""`, `placement=""`), the `card/index.html` pattern. A name declared with no default falls through to the page's template context when the caller leaves it out, so a view with `role` or `title` in its context would otherwise rewrite the component's semantics (D9). The `<c-vars>` lines below show the names; each carries `=""`. Annotations give no `default:` for these, which the linter accepts.
- **Caller `role`.** Where a component sets a role by default, `role` is declared in `<c-vars>` and written once: the caller's if given, else the default (research R6, D5).
- **No script.** No `<script>`, no `on*=` attribute (FR-005). Each test module asserts it for its own components.

### Divider (US3)

`divider.html` — `<c-vars horizontal vertical variant placement text role class />`.

```
<div class="divider {variant: divider-X} {horizontal: responsive divider-horizontal} {vertical: responsive divider-vertical} {placement: divider-start|end} {{ class }}"
     {role} {aria-orientation} {{ attrs }}>{{ text }}{{ slot }}</div>
```

- Unlabelled (`not text and not slot.strip`, research R7): `role="separator"` (or the caller's `role`), and `aria-orientation="vertical"` when `horizontal` is bare `True`. A responsive `horizontal="md"` gets no orientation, since it is horizontal below the breakpoint (FR-016).
- Labelled: no default role, so the label stays readable (decisions.md "Unlabelled divider is a separator"). A caller's `role` is still written.
- `position` becomes `placement`, `vertical` now emits `divider-vertical`, the undeclared `label` named slot is gone and `text` replaces it (FR-015, clarification 1, decisions.md "Divider's vertical is reversed").

### Mockups (US8)

- `mockup/browser.html` — `<div class="mockup-browser border border-base-300 bg-base-100 w-full {{ class }}" {{ attrs }}>`, toolbar `<div class="mockup-browser-toolbar"><div class="input">{{ url }}</div></div>`, then `<div>{{ slot }}</div>`, daisyUI's documented content wrapper. The URL is plain text in the toolbar, never hidden. The toolbar's dots are CSS pseudo-elements with nothing for assistive technology to read.
- `mockup/code/index.html` — `<c-vars class />`, `<div class="mockup-code w-full {{ class }}" tabindex="0" {{ attrs }}>{{ slot }}</div>`. `tabindex="0"` makes the overflowing box a Tab stop that scrolls with the arrow keys (FR-024). Visible focus is the browser's default outline, measured at the walkthrough (research R8).
- `mockup/code/line.html` — `<c-vars prefix text class />`, `<pre{% if prefix %} data-prefix="{{ prefix }}"{% endif %} class="{{ class }}" {{ attrs }}><code>{{ text }}{{ slot }}</code></pre>`. No default prefix (decisions.md "Code mockup lines have no default prefix", D2).
- `mockup/phone.html` — `<c-vars class />`, `<div class="mockup-phone {{ class }}" {{ attrs }}><div class="mockup-phone-camera" aria-hidden="true"></div><div class="mockup-phone-display bg-base-100 text-base-content">{{ slot }}</div></div>`. `grid place-content-center` and the literal colours go (FR-023, D3).
- `mockup/window.html` — `<c-vars class />`, `<div class="mockup-window border border-base-300 bg-base-100 {{ class }}" {{ attrs }}><div>{{ slot }}</div></div>`. The wrapper stays, daisyUI's documented structure, and loses `grid place-content-center h-80`. Without it every child of the slot would become a stretched item of the window's column flexbox. The window's dots are pseudo-elements.

### Join (US4)

`join.html` — `<c-vars horizontal vertical role class />`. `<div class="join {vertical: responsive join-vertical} {horizontal: responsive join-horizontal} {{ class }}" role="{caller's role, else group}" {{ attrs }}>{{ slot }}</div>`. The group's name is the caller's `aria-label`, through `{{ attrs }}`. No wrapper around children (FR-017).

### Footer (US2)

`footer/index.html` — `<c-vars horizontal vertical placement class />`. `<footer class="footer {horizontal: responsive footer-horizontal} {vertical: responsive footer-vertical} {placement: footer-center} {{ class }}" {{ attrs }}>{{ slot }}</footer>`.

`footer/nav.html` — `<c-vars title class />`. `<nav{% if title %} aria-label="{{ title }}"{% endif %} class="{{ class }}" {{ attrs }}>{% if title %}<span class="footer-title">{{ title }}</span>{% endif %}{{ slot }}</nav>`. The title names the landmark through `aria-label` rather than `aria-labelledby`, which would need an id the template cannot make unique (D6). A `<span>`, not a heading (decisions.md "Footer titles are not headings").

### Drawer (US1)

`drawer/index.html` — `{% load i18n daisy_cotton %}`, `<c-vars id open placement class />`, `id` annotated `required`.

```
<div class="drawer {open: responsive drawer-open} {placement: drawer-end} {{ class }}" {{ attrs }}>
  <input id="{{ id }}" type="checkbox" class="drawer-toggle" aria-label="{% trans "Toggle sidebar" %}" />
  <div class="drawer-content">{{ slot }}</div>
  <div class="drawer-side">
    <label for="{{ id }}" class="drawer-overlay"><span class="sr-only">{% trans "Close sidebar" %}</span></label>
    {{ side }}
  </div>
</div>
```

`id` is declared, so it reaches the checkbox and never the root: two elements with one id would break every `for`. `placement` validated against `end` only (FR-011). Named slot `side`. `@trigger` is the opener's markup, `<c-drawer.button drawer="demo-drawer">…</c-drawer.button>`, as `modal.html`'s trigger is. The gallery prepends it to the default slot, so it lands inside `drawer-content` where the focus ring applies (Article XVI, research R2).

`drawer/button.html` — `<c-vars drawer class />`, `drawer` annotated `required`. `<label for="{{ drawer }}" class="btn drawer-button {{ class }}" {{ attrs }}>{{ slot }}</label>`. A `<label>`, because daisyUI's focus ring targets `label.drawer-button` inside `.drawer-content` (research R2). `btn` is daisyUI's documented opener class (D4). No `role`, no `tabindex`: the Tab stop is the checkbox (research R2).

### Indicator (US5)

`indicator/index.html` — `<c-vars class />`. `<div class="indicator {{ class }}" {{ attrs }}>{{ items }}{{ slot }}</div>`. Named slot `items`, always emitted before the default slot (FR-018).

`indicator/item.html` — `<c-vars placement class />`. `<span class="indicator-item {% for p in placement.split %}{% variation p "indicator" "start,center,end,top,middle,bottom" %} {% endfor %}{{ class }}" {{ attrs }}>{{ slot }}</span>`. Each space-separated value is validated on its own (FR-019). `placement` is typed `select[…]` listing the combinations the gallery should offer (D7).

### Hero (US6)

`hero.html` — `<c-vars overlay class />`. `<div class="hero {{ class }}" {{ attrs }}>{% if overlay %}<div class="hero-overlay" aria-hidden="true"></div>{% endif %}<div class="hero-content">{{ slot }}</div></div>`. A background image is the caller's `style`, which reaches the root through `{{ attrs }}` (FR-020, decisions.md "Hero is the container only").

### Mask and stack (US7)

`mask.html` — `<c-vars shape half src alt class />` (each `=""` per the shared rule), `shape` annotated `required` and `select[…]` with daisyUI's fourteen shapes. With `src`: `<img src="{{ src }}" alt="{{ alt }}" class="mask {shape} {half} {{ class }}" {{ attrs }} />`. Without: `<div class="mask {shape} {half} {{ class }}" {{ attrs }}>{{ slot }}</div>`. `half` validated against `1,2` (FR-021).

`stack.html` — `<c-vars placement class />`. `<div class="stack {placement: stack-top|bottom|start|end} {{ class }}" {{ attrs }}>{{ slot }}</div>` (FR-022).

### Gallery entries (FR-007, FR-008)

Every template carries `@description`, a `@prop` per `<c-vars>` name and `@slot` / `@slot:name` per slot. Fixed-value props are `select[…]` with daisyUI's full list, which gives the gallery's variants matrix every colour, placement and shape (FS-003 research R4). Booleans (`horizontal`, `vertical`, `open`, `overlay`) are toggles. Each default `@slot` is a one-line example that shows the component's states:

- `drawer`: `@trigger` the opener for `demo-drawer`. The default `@slot` a page holding daisyUI's responsive divider pattern (`<div class="flex flex-col sm:flex-row">…<c-divider horizontal="sm">OR</c-divider>…</div>`), a `<c-join vertical horizontal="sm">` of three buttons, and a `<c-footer vertical horizontal="sm">` with two `footer.nav` groups. `@slot:side` is a sidebar list. The description tells the viewer to set `id` to `demo-drawer` (research R4). This page is the responsive example for `divider`, `join` and `footer` (research R3, D8).
- `divider`: `OR`. `join`: three buttons with `join-item`. `indicator`: a button with an item whose count carries a visually hidden text alternative (scenario 4). `hero`: a heading, copy and a button. `mask`: an inline image. `stack`: three cards. Each mockup: content that exercises it (`mockup.code` with a prompt line and an output line).

Two traps in a one-line example: it must not contain `#}`, and must not contain a spaced em dash, which the gallery takes as the start of the slot's description (`core/annotations.py:241`). The indicator example's count carries a visually hidden text alternative, and a test reads the example through the gallery's own parser to hold it there (T017).

Descriptions of `horizontal`, `vertical` and `open` say that a breakpoint such as `lg` applies the modifier from that width up, as FS-003's do.

Folder components' pages are at `/django-cotton-gallery/<name>/index/` until #96 is fixed (FS-003 research R3). `tests/test_gallery_links.py` already skips those cases with a reason.

### Documentation

- `README.md`: component count and list gain each new component in its story. The scope note "Heroes, sections and other compositions are built from these components, not shipped with them" is reworded: the `hero` container ships, composed hero sections stay with the project (FR-009).
- `CHANGELOG.md` `[Unreleased]`: `Added` per new component. `Changed` per breaking change on `divider` and the mockups, each with what a host project writes to keep the old result.

## Project Structure

### Documentation (this feature)

```text
specs/004-layout-components/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templates/cotton/
├── divider.html                                  # changed (US3)
├── mockup/browser.html, phone.html, window.html  # changed (US8)
├── mockup/code/index.html, line.html             # changed (US8)
├── join.html                                     # new (US4)
├── footer/index.html, nav.html                   # new (US2)
├── drawer/index.html, button.html                # new (US1)
├── indicator/index.html, item.html               # new (US5)
├── hero.html                                     # new (US6)
└── mask.html, stack.html                         # new (US7)
tests/
├── test_divider.py, test_mockup.py               # new (US3, US8)
├── test_mockup_code.py                           # changed under D2
├── test_join.py, test_footer.py, test_drawer.py  # new (US4, US2, US1)
├── test_indicator.py, test_hero.py, test_mask_stack.py   # new (US5–US7)
pyproject.toml                                    # new test modules in non-mirror-paths
README.md, CHANGELOG.md
```

**Structure Decision**: templates and their tests only. Components with parts use the package's folder layout (`<name>/index.html` plus part templates).

## Story order

One worktree, three dispatch batches on the same branch. Each story touches its own templates and test module, and appends to `README.md`, `CHANGELOG.md` and `pyproject.toml`'s `non-mirror-paths`, so batches run one after another rather than in parallel.

1. US3 (divider) and US8 (mockups): the breaking changes to shipped components.
2. US4 (join), US2 (footer), US1 (drawer), in that order: the drawer's gallery example composes the other three.
3. US5 (indicator), US6 (hero), US7 (mask and stack).

## Complexity Tracking

None.
