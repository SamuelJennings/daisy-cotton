# Implementation Plan: Action components

**Branch**: `005-action-components` | **Date**: 2026-09-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-action-components/spec.md`

## Summary

Two new Cotton components (`fab`, `swap`) and three existing ones rebuilt to the constitution's attribute vocabulary and accessibility bar (`button`, `dropdown`, `modal`). Each renders daisyUI 5's documented markup, ships no script and carries its gallery annotations. The dropdown moves to daisyUI's popover method, the modal to daisyUI's own box-and-actions structure, and the button loses the attributes daisyUI has no name for. The only new Python is one template tag that makes a unique id for a dropdown panel.

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added.

**Storage**: none

**Testing**: pytest + pytest-django. Components are rendered through the Cotton compiler as a caller's template would be (the `cotton_render_string` and `cotton_render_string_soup` fixtures in `tests/conftest.py`), never by rendering the component file directly, which skips `<c-vars>` extraction.

**Target Platform**: any host project running daisyUI 5

**Project Type**: Django package (templates plus one template tag) with a demo project

**Constraints**: no JavaScript, no stylesheet, no literal colours, no class daisyUI does not define for the component except layout utilities the existing templates already use

**Scale/Scope**: 5 components, 5 templates (2 new, 3 rewritten), 1 new template tag

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Test-First | Every acceptance scenario gets a test written before the template that satisfies it. The pre-existing button, dropdown and modal tests the approved spec invalidates are rewritten under D2, not silently. | Pass |
| II Simplicity | Templates, plus one `unique_id` tag for FR-019 (research R6). `variation` covers every modifier. | Pass |
| III Anti-Abstraction | No base template, no shared include. | Pass |
| V Security | Every value reaches the page through `{{ }}` autoescaping. Ids and anchor names are built from the caller's `id` or a generated hex string, as attribute values. | Pass |
| VI Documentation | README component list and CHANGELOG entries land in the story that introduces or changes each name. | Pass |
| VII Dependency discipline | No new runtime or dev dependency. `uuid` is standard library. | Pass |
| VIII i18n | The modal's "Close" (close button and backdrop) is `{% trans %}`. No other string is written by the package. | Pass |
| X Test structure | One test module per component, `Test<Subject>` classes, new modules in `non-mirror-paths` like the existing component tests. The tag's tests go in `tests/test_templatetags/test_daisy_cotton.py`. | Pass |
| XI Cohesion | `unique_id` is a decorator-registered tag beside `responsive` and `variation`. | Pass |
| XII Agnostic | Gallery examples use neutral copy. | Pass |
| XIII Semantic palette | Colours only through validated `variant` and `base-*` classes. | Pass |
| XIV Attribute vocabulary | `variant`, `size`, daisyUI's modifier names as booleans, `placement`, merged `class`, `content_class` and `input_class` for inner surfaces, the rest through `{{ attrs }}`. | Pass |
| XV Composition | The dropdown's and FAB's triggers and the modal's close button are `<c-button>`. The button's icon is `<c-icon>`. | Pass |
| XVI Gallery annotations | Every template annotated, fixed-value props typed `select[…]`, `@trigger` on the modal, `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below:

- **Modifiers.** `variant`, `size` and `placement` go through `{% variation … %}` against daisyUI's list for that component (research R1), so an unknown value adds nothing and nothing raises (Edge Cases). A `placement` that takes two words is split and each word validated on its own, as FS-004's indicator does.
- **Root.** Every component declares `class`, merges it into the root's class list, and spreads `{{ attrs }}` on the root (FR-002), except where FR-018 and FR-026 send extra attributes to a trigger.
- **Empty defaults.** Every declared name except `class` is declared with an empty default (`text=""`, `placement=""`), the `card/index.html` pattern, so a page variable of the same name never leaks in (research R5). Annotations give no `default:` for these, which the linter accepts.
- **No script.** No `<script>`, no `on*=` attribute in any template (SC-003). Each test module asserts it for its own component.
- **Triggers are `type="button"`.** The dropdown's and FAB's default triggers pass `type="button"` to `<c-button>`. Inside a form, a button with no type is a submit button, which would submit the form and, for the dropdown, never open the popover (research R2). A caller's `type` still wins (research R4).

### Button (US1)

`button.html` — `{% load daisy_cotton %}`, `<c-vars href text icon variant size outline dash soft ghost link active disabled wide block square circle class />`, each `=""` except `class`.

```
{% if href %}<a href="{{ href }}" class="{classes}{% if disabled %} btn-disabled{% endif %}"{% if disabled %} aria-disabled="true" role="button" tabindex="-1"{% endif %} {{ attrs }}>
{% else %}<button class="{classes}"{% if disabled %} disabled{% endif %} {{ attrs }}>{% endif %}
  {% if icon %}<c-icon name="{{ icon }}" aria-hidden="true" />{% endif %}{% if text %}<span>{{ text }}</span>{% endif %}{{ slot }}
</a or button>
```

`{classes}` is `btn`, then `{% variation variant "btn" "neutral,primary,secondary,accent,info,success,warning,error" %}`, `{% variation size "btn" "xs,sm,md,lg,xl" %}`, then one `btn-<name>` for each of `outline`, `dash`, `soft`, `ghost`, `link`, `active`, `wide`, `block`, `square`, `circle` that is set, then `{{ class }}`. Every style boolean given is emitted (Edge Cases: the component does not pick between `outline` and `ghost`).

- `href` is declared now, so a page variable called `href` cannot turn a button into a link (research R5). It is written onto the `<a>` explicitly.
- `disabled` is declared, so it is written exactly once: native on a `<button>`, and on a link as the four attributes FR-010 lists, never as a bare `disabled` on an `<a>`.
- The icon is hidden from assistive technology. An icon-only button is named by the caller's `aria-label`, which reaches the element through `{{ attrs }}` (scenario 5).
- `inline-flex items-center justify-{align} gap-2` goes: `.btn` is already `display:inline-flex`, centred, with a gap (research R1). `align`, `reverse`, `condition` and `full` go (FR-011). The `{% spaceless %}` and `{% with element=… %}` wrappers go with them.

### Modal (US2)

`modal.html` — `{% load i18n daisy_cotton %}`, `<c-vars id title placement closable open content_class actions class />`, `id` annotated `required`.

```
<dialog{% if id %} id="{{ id }}"{% endif %} class="modal {% variation placement "modal" "top,middle,bottom,start,end" %} {{ class }}"
        {% if id and title %}aria-labelledby="{{ id }}-title"{% endif %}{% if open %} open{% endif %} {{ attrs }}>
  <div class="modal-box {{ content_class }}">
    {% if closable %}<form method="dialog"><c-button size="sm" circle ghost class="absolute end-2 top-2" aria-label="{% trans "Close" %}"><span aria-hidden="true">✕</span></c-button></form>{% endif %}
    {% if title %}<h2{% if id %} id="{{ id }}-title"{% endif %} class="text-lg font-bold">{{ title }}</h2>{% endif %}
    {{ slot }}
    {% if actions %}<div class="modal-action">{{ actions }}</div>{% endif %}
  </div>
  <form method="dialog" class="modal-backdrop"><button>{% trans "Close" %}</button></form>
</dialog>
```

- The heading names the dialog through `aria-labelledby`, built from the modal's own required `id`, so two modals on a page never share a heading id. A caller's `aria-label` reaches the dialog through `{{ attrs }}` for a modal with no title (Edge Cases).
- The close button is a `<c-button>` inside `<form method="dialog">`, where a button with no type submits the form and closes the dialog without script (FR-015, Article XV). The backdrop is daisyUI's own `<form method="dialog" class="modal-backdrop">`, whose button covers the backdrop and is not a styled button, so it stays a plain `<button>` with translatable text.
- Escape, the focus trap and focus return are the browser's, for a dialog opened with `showModal()`. `open` renders `<dialog open>`, which daisyUI shows (`.modal[open]`, research R1). A dialog shown this way is not modal: Escape does not close it and focus is not trapped, though the backdrop and close button still close it. That is the only way to show a dialog without script, and the `open` description says so (D4).
- `actions` is a named slot declared with an empty default, so a page variable called `actions` does not fill it (FS-004 D12).
- The inner card, `size`, `position`, `icon`, `footer` and `footer_end` go (FR-016). Width goes through `content_class`.
- `@trigger <c-button onclick="demo_modal.showModal()">Open</c-button>`. The gallery prepends it inside the dialog, where it cannot be reached while the dialog is closed (research R3, D3). The annotation still shows the trigger's markup, and the description tells the viewer to set `id` to `demo_modal` and switch `open` on to see each placement, the close button and the actions row.

### Dropdown (US3)

`dropdown/index.html` — `{% load daisy_cotton %}`, `<c-vars id placement content_class button class />`.

```
{% unique_id "dropdown" as generated_id %}{% firstof id generated_id as panel_id %}
<div class="inline-block {{ class }}" {% if button %}{{ attrs }}{% endif %}>
  {% if button %}{{ button }}{% else %}<c-button type="button" popovertarget="{{ panel_id }}" style="anchor-name: --{{ panel_id }}" :attrs="attrs" />{% endif %}
  <div id="{{ panel_id }}" popover
       class="dropdown {% for word in placement.split %}{% variation word "dropdown" "top,bottom,left,right,start,center,end" %} {% endfor %}bg-base-100 rounded-box min-w-52 shadow-sm {{ content_class }}"
       style="position-anchor: --{{ panel_id }}">{{ slot }}</div>
</div>
```

- The root is a wrapper `<div class="inline-block">`, the display `.dropdown` gave the old wrapper, so `class` has a root to land on (Article XIV). The `dropdown` class and its placement classes sit on the panel, which is where daisyUI's popover method puts them (research R2).
- The panel id is the caller's `id`, or `dropdown-` plus eight hex characters from the new `unique_id` tag (FR-019, research R6). The trigger's `popovertarget` and both anchor names are built from it.
- Extra attributes configure the default trigger (`text`, `icon`, `variant`, `aria-label`…), and fall through to the wrapper when a `button` slot replaces it, as today. A custom trigger must carry `popovertarget` set to the dropdown's `id` and `type="button"`, plus `style="anchor-name: --<id>"` for placement, so a dropdown with a custom trigger needs an `id`. The `@slot:button` description and a `{% comment %}` block say so (scenario 6).
- `button` is declared with an empty default, so a page variable called `button` does not replace the trigger (FS-004 D12).
- `valign`, `halign`, `full` and `hover` go (FR-020). The panel loses `dropdown-content`, `tabindex`, `z-50` and `border border-base-300`: the popover is in the top layer, and daisyUI's popover panel carries none of them (SC-001).
- The CSS-anchor limitation (Edge Cases) goes in the `{% comment %}` block that replaces the current one about positioning.

`daisy_cotton/templatetags/daisy_cotton.py` — `unique_id(prefix)`: returns `f"{prefix}-{uuid.uuid4().hex[:8]}"`, a `simple_tag` used with `as`.

### Swap (US4)

`swap.html` — `<c-vars label rotate flip active checked disabled name value input_class on off indeterminate class />`.

```
<label class="swap{% if rotate %} swap-rotate{% endif %}{% if flip %} swap-flip{% endif %}{% if active %} swap-active{% endif %} {{ class }}" {{ attrs }}>
  <input type="checkbox"{% if label %} aria-label="{{ label }}"{% endif %}{% if name %} name="{{ name }}"{% endif %}{% if value %} value="{{ value }}"{% endif %}{% if checked %} checked{% endif %}{% if disabled %} disabled{% endif %}{% if input_class %} class="{{ input_class }}"{% endif %} />
  <div class="swap-on">{{ on }}</div>
  <div class="swap-off">{{ off }}</div>
  {% if indeterminate %}<div class="swap-indeterminate">{{ indeterminate }}</div>{% endif %}
</label>
```

- The control's state, form attributes and accessible name are declared so they reach the checkbox. Everything else reaches the `<label>` (FR-023, clarification).
- `input_class` is the checkbox's extra classes, the name FS-010 gives the OTP's inner input for the same idea (Article XIV). The theme toggle is `input_class="theme-controller" value="dark"` (FR-024).
- The named slots `on`, `off` and `indeterminate` are declared with empty defaults so a page variable called `on` or `off` does not fill them (FS-004 D12). Only `indeterminate` is conditional: `swap-on` and `swap-off` are always emitted, because daisyUI's CSS keys on them.
- The checkbox stays in the tab order with the browser's focus ring (research R8), so the swap needs no focus class.
- A `{% comment %}` block says the theme controller has no component of its own and why, and shows the theme toggle.

### FAB (US5)

`fab.html` — `<c-vars flower close main_action button class />`.

```
<div class="fab{% if flower %} fab-flower{% endif %} {{ class }}" {% if button %}{{ attrs }}{% endif %}>
  {% if button %}{{ button }}{% else %}<c-button type="button" size="lg" circle tabindex="0" :attrs="attrs" />{% endif %}
  {% if close %}<div class="fab-close">{{ close }}</div>{% endif %}
  {% if main_action %}<div class="fab-main-action">{{ main_action }}</div>{% endif %}
  {{ slot }}
</div>
```

- The trigger is the first child and carries `tabindex="0"`, which daisyUI's rules key on and which makes a click focus it in Safari (research R7, FR-026). A caller's `size`, `variant`, `icon` and `aria-label` reach it and override the defaults (research R4).
- A custom `button` slot must be focusable and carry `tabindex`, and its description says so.
- `close`, `main_action` and `button` are named slots declared with empty defaults. Each action in the default slot is a direct child of the FAB, as daisyUI's rules require: a `<c-button>`, a `<div>` holding a label and a button, or a daisyUI tooltip wrapping a button.
- A FAB with no actions is a single floating button (scenario 3): the trigger alone.

### Gallery entries (FR-003, FR-004)

Every template carries `@description`, a `@prop` per `<c-vars>` name and `@slot` / `@slot:name` per slot, in the order FS-002 set: description, props in declaration order, default slot, named slots in render order, trigger. A named slot declared in `<c-vars>` gets both a `@prop` and a `@slot:name`, as FS-004's `drawer` does for `side`. Fixed-value props are `select[…]` with daisyUI's full list, which gives the gallery's variants matrix every colour, size and placement. Booleans are toggles. One-line examples must not contain `#}` or a spaced em dash (FS-004 plan).

- `button`: `@slot Save`. The variants matrix shows each `variant` and `size`. The style and modifier booleans are toggles. The description says an icon-only button needs an `aria-label`.
- `modal`: `@slot` a sentence of body copy, `@slot:actions` a `<form method="dialog">` holding a `<c-button>`. `@trigger` as above.
- `dropdown`: `@slot` a plain daisyUI menu, `<ul class="menu"><li><a href="#">…</a></li>…</ul>`. The description tells the viewer to type `text="Options"` in the attributes field, since the gallery cannot prefill forwarded attributes (D5). `@slot:button` has no example, so the preview uses the default trigger.
- `swap`: `@slot:on` and `@slot:off` short words (`ON`, `OFF`), `@slot:indeterminate` with no example. The description says to give `label`.
- `fab`: `@slot` three `<c-button circle>` actions, each with an icon and an `aria-label`, and one labelled action (`<div>Label <c-button …/></div>`). `@slot:close` and `@slot:main_action` have no example, and their descriptions give the markup. The description tells the viewer to type `icon="bi bi-plus-lg" aria-label="Actions"` in the attributes field for the trigger (D5).

### Documentation

- `README.md`: component count and list gain `fab` and `swap` in their stories.
- `CHANGELOG.md` `[Unreleased]`: `Added` for `fab`, `swap` and `unique_id`. `Changed` for every removed or renamed attribute or slot on `button`, `dropdown` and `modal`, each with what a project writes instead (FR-007, SC-005).

## Project Structure

### Documentation (this feature)

```text
specs/005-action-components/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templates/cotton/
├── button.html               # rewritten (US1)
├── modal.html                # rewritten (US2)
├── dropdown/index.html       # rewritten (US3)
├── swap.html                 # new (US4)
└── fab.html                  # new (US5)
daisy_cotton/templatetags/daisy_cotton.py   # unique_id (US3)
tests/
├── test_button.py, test_modal.py, test_dropdown.py   # rewritten under D2
├── test_swap.py, test_fab.py                         # new
└── test_templatetags/test_daisy_cotton.py            # unique_id tests
pyproject.toml                # new test modules in non-mirror-paths
README.md, CHANGELOG.md
```

**Structure Decision**: templates and their tests, plus one tag. The dropdown keeps its folder layout. `swap` and `fab` have no parts, so each is a single template.

## Story order

One worktree, two dispatch batches on the same branch. Each story touches its own template and test module, and appends to `README.md`, `CHANGELOG.md` and `pyproject.toml`, so batches run one after another rather than in parallel.

1. US1 (button), then US2 (modal) and US3 (dropdown): the modal's close button and the dropdown's trigger are drawn with the new button.
2. US4 (swap), US5 (FAB). The FAB's trigger and actions use the new button.

## Complexity Tracking

| Addition | Why | Simpler alternative rejected because |
|---|---|---|
| `unique_id` template tag | FR-019: two dropdowns with no `id` must never share a panel | A template has nothing unique to build an id from. A counter repeats across includes, a slot hash repeats for identical menus (research R6). |
