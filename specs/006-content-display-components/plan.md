# Implementation Plan: Content display components

**Branch**: `006-content-display-components` | **Date**: 2026-09-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-content-display-components/spec.md`

## Summary

Twelve new Cotton components (`table`, `collapse`, `accordion`, `list`, `list.row`, `stat`, `stat.group`, `timeline`, `timeline.item`, `kbd`, `status`) and four existing ones rebuilt to the constitution's attribute vocabulary and accessibility bar (`card`, `badge`, `avatar`, `avatar.group`). Each renders daisyUI 5's documented markup, ships no script and carries its gallery annotations. The card moves to daisyUI's figure, body, title and actions structure, and the modal that draws its box with the card is adjusted so it keeps rendering what it rendered before. The only new Python is the `unique_id` tag that names a table's scrolling region by its caption.

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added.

**Storage**: none

**Testing**: pytest + pytest-django. Components are rendered through the Cotton compiler as a caller's template would be (the `cotton_render_string` and `cotton_render_string_soup` fixtures in `tests/conftest.py`), never by rendering the component file directly, which skips `<c-vars>` extraction.

**Target Platform**: any host project running daisyUI 5

**Project Type**: Django package (templates plus one template tag) with a demo project

**Constraints**: no JavaScript, no stylesheet, no literal colours, no class daisyUI does not define for the component except the layout utilities this plan names (the table's `overflow-x-auto`, the avatar frame's defaults, the timeline connector's `group` utilities)

**Scale/Scope**: 15 components, 15 templates (11 new, 4 rewritten), `modal.html` adjusted, 1 new template tag

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Test-First | Every acceptance scenario gets a test written before the template that satisfies it. The pre-existing card, badge, avatar and modal tests the approved spec invalidates are rewritten, not silently (D2). | Pass |
| II Simplicity | Templates, plus one `unique_id` tag (research R6) and FS-004's breakpoint check in `responsive`. `variation` and `responsive` cover every modifier. | Pass |
| III Anti-Abstraction | No base template, no shared include. | Pass |
| V Security | Every value reaches the page through `{{ }}` autoescaping. The caption id is a generated hex string written as an attribute value. | Pass |
| VI Documentation | README component list and CHANGELOG entries land in the story that introduces or changes each name. | Pass |
| VII Dependency discipline | No new runtime or dev dependency. `uuid` is standard library. | Pass |
| VIII i18n | No component writes a user-facing string of its own. The avatar's old "User avatar" default goes. | Pass |
| X Test structure | One test module per component family, `Test<Subject>` classes, new modules in `non-mirror-paths` like the existing component tests. The tag's tests go in `tests/test_templatetags/test_daisy_cotton.py`. | Pass |
| XI Cohesion | `unique_id` is a decorator-registered tag beside `responsive` and `variation`. | Pass |
| XII Agnostic | Gallery examples use neutral copy. | Pass |
| XIII Semantic palette | Colours only through validated `variant` and the avatar placeholder's `bg-neutral text-neutral-content`, daisyUI's own example colours. | Pass |
| XIV Attribute vocabulary | `variant`, `size`, daisyUI's modifier names as booleans, breakpoint values for `side`, `vertical` and `horizontal`, merged `class`, `content_class` for inner surfaces, the rest through `{{ attrs }}`. | Pass |
| XV Composition | The accordion is drawn by `<c-collapse>`. The card and stat take icons through their slots, drawn by the caller's `<c-icon>`. | Pass |
| XVI Gallery annotations | Every template annotated, fixed-value props typed `select[…]`, `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below:

- **Modifiers.** `variant` and `size` go through `{% variation … %}` against daisyUI's list for that component (research R1), so an unknown value adds nothing and nothing raises (Edge Cases). `side`, `vertical` and `horizontal` go through `{% responsive … %}`, the menu's convention from FS-003: `True` gives the class, a breakpoint gives `<bp>:<class>`. On main `responsive` passes any string through, so a value outside Tailwind's breakpoints would emit a class (Edge Cases). FS-004 (open as #102) restricts it to `sm,md,lg,xl,2xl` with a `BREAKPOINTS` tuple and two tests. This feature makes the identical change, same code, docstring and tests, so whichever lands second reconciles identical code (research R6 does the same for `unique_id`).
- **Root.** Every component declares `class`, merges it into the root's class list, and spreads `{{ attrs }}` on the root (FR-002).
- **Empty defaults.** Every declared name, `class` included, is declared with an empty default (`title=""`, `class=""`), so a page variable of the same name never leaks in (research R3). Annotations give no `default:` for these. A `select` must not get `default:""`, which the linter rejects.
- **Hyphenated booleans** (`image-full`, `pin-rows`, `pin-cols`, `snap-icon`) are declared hyphenated and read underscored (research R2).
- **Parts.** A part filled by an attribute or a named slot of the same name is declared once in `<c-vars>` and rendered only when non-empty (FR-007). A named slot declared in `<c-vars>` gets both a `@prop` and a `@slot:name`, as FS-004's `drawer` does.
- **No script.** No `<script>` and no `on*=` attribute in any component's rendered output (SC-003), asserted on the component rendered from a caller string.

### Card (US1)

`card/index.html` — `{% load daisy_cotton %}`, `<c-vars title="" figure="" actions="" size="" border="" dash="" side="" image-full="" content_class="" class="" />`.

```
<div class="card {% variation size "card" "xs,sm,md,lg,xl" %}{% if border %} card-border{% endif %}{% if dash %} card-dash{% endif %} {% responsive side "card-side" %}{% if image_full %} image-full{% endif %} {{ class }}" {{ attrs }}>
  {% if figure %}<figure>{{ figure }}</figure>{% endif %}
  <div class="card-body {{ content_class }}">
    {% if title %}<h2 class="card-title">{{ title }}</h2>{% endif %}
    {{ slot }}
    {% if actions %}<div class="card-actions">{{ actions }}</div>{% endif %}
  </div>
</div>
```

- `icon`, `tight`, `badges`, `footer`, `footer_end`, `body_class` and `bg-base-100 shadow-sm` go (FR-012).

**The modal (research R7).** `modal.html` keeps its public contract on this branch. It declares `title=""` and `icon=""` so they no longer reach the card as raw attributes, and hands the card a `title` slot holding `<c-icon name="{{ icon }}" />` and `<span>{{ title }}</span>` when either is given. `actions` is forwarded as today and now renders in `card-actions` at the foot of the body. `footer` and `footer_end` are rendered by the modal itself, after its body inside the card's default slot, in the same flex row the card used to draw. `class="w-full h-full {{ class }}"` stays, so the existing modal tests stand, and the modal gains a surface class the card no longer adds: `bg-base-100 shadow-sm`, on the `<c-card>` call. The modal's annotations are updated to match. FS-005 replaces this modal wholesale, and whichever lands second reconciles.

### Table (US2)

`table.html` — `{% load daisy_cotton %}`, `<c-vars caption="" size="" zebra="" pin-rows="" pin-cols="" content_class="" class="" />`.

```
{% unique_id "table" as caption_id %}
<div class="overflow-x-auto {{ class }}" tabindex="0" role="region"{% if caption %} aria-labelledby="{{ caption_id }}"{% endif %} {{ attrs }}>
  <table class="table {% variation size "table" "xs,sm,md,lg,xl" %}{% if zebra %} table-zebra{% endif %}{% if pin_rows %} table-pin-rows{% endif %}{% if pin_cols %} table-pin-cols{% endif %} {{ content_class }}">
    {% if caption %}<caption id="{{ caption_id }}">{{ caption }}</caption>{% endif %}
    {{ slot }}
  </table>
</div>
```

- A caller's `aria-label` reaches the wrapper through `{{ attrs }}` (scenario 3).
- `unique_id` is FS-005's tag, added here identically (research R6).
- The `{% comment %}` block names the three caller duties the edge cases list: give a caption or `aria-label`; `pin-rows` needs a `<thead>` and `pin-cols` row header cells; the wrapper is a keyboard stop even when the table fits.

### Badge (US3)

`badge.html` — `{% load daisy_cotton %}`, `<c-vars text="" variant="" size="" outline="" dash="" soft="" ghost="" class="" />`.

```
<span class="badge {% variation variant "badge" "neutral,primary,secondary,accent,info,success,warning,error" %} {% variation size "badge" "xs,sm,md,lg,xl" %}{% if outline %} badge-outline{% endif %}{% if dash %} badge-dash{% endif %}{% if soft %} badge-soft{% endif %}{% if ghost %} badge-ghost{% endif %} {{ class }}" {{ attrs }}>{{ text }}{{ slot }}</span>
```

- `<div>` becomes `<span>`, so a badge inside a button is valid HTML (scenario 4). `size_opts` and the `get_item` lookup go. The badge now spreads `{{ attrs }}`, which it did not (scenario 5).

### Collapse and accordion (US4)

`collapse.html` — `<c-vars title="" arrow="" plus="" open="" class="" />`.

```
<details class="collapse{% if arrow %} collapse-arrow{% endif %}{% if plus %} collapse-plus{% endif %} {{ class }}"{% if open %} open{% endif %} {{ attrs }}>
  <summary class="collapse-title">{{ title }}</summary>
  <div class="collapse-content">{{ slot }}</div>
</details>
```

- `name` is not declared on the collapse. It passes through `{{ attrs }}` to `<details>`, which is how the accordion's group name arrives.
- The summary is always emitted: a `<details>` with no summary gets the browser's own "Details" label.

`accordion.html` — `<c-vars name="" title="" />`, `name` annotated `required`.

```
<c-collapse name="{{ name }}" :attrs="attrs">{% if title %}<c-slot name="title">{{ title }}</c-slot>{% endif %}{{ slot }}</c-collapse>
```

- Every other collapse attribute (`arrow`, `plus`, `open`, `class`) reaches the collapse through `:attrs` (FR-020, scenario 8). `title`, as attribute or slot, is re-passed as the collapse's `title` slot.
- The `{% comment %}` block says items sharing a `name` form one group, that an older browser lets more than one open, and to open at most one item per group.

### Avatar and avatar group (US5)

`avatar/index.html` — `<c-vars src="" alt="" placeholder="" online="" offline="" content_class="" class="" />`.

```
<div class="avatar{% if not src %} avatar-placeholder{% endif %}{% if online %} avatar-online{% endif %}{% if offline %} avatar-offline{% endif %} {{ class }}" {{ attrs }}>
  <div class="{% if content_class %}{{ content_class }}{% else %}w-12 rounded-full{% if not src %} bg-neutral text-neutral-content{% endif %}{% endif %}">
    {% if src %}<img src="{{ src }}" alt="{{ alt }}" />
    {% elif placeholder %}<span>{{ placeholder }}</span>
    {% else %}<svg … aria-hidden="true" focusable="false">…</svg>{% endif %}
  </div>
</div>
```

- The silhouette is a placeholder too: it takes `avatar-placeholder`, which centres the frame's content, and the placeholder colours (D4).
- `alt` defaults to empty (FR-022). `size`, `size_options`, `shape`, `variant` and `status` go.

`avatar/group.html` — `<c-vars class="" />`, `<div class="avatar-group {{ class }}" {{ attrs }}>{{ slot }}</div>`. `size` and `space_options` go.

### Stat (US6)

`stat/index.html` — `<c-vars title="" value="" desc="" figure="" actions="" class="" />`.

```
<div class="stat {{ class }}" {{ attrs }}>
  {% if figure %}<div class="stat-figure">{{ figure }}</div>{% endif %}
  {% if title %}<div class="stat-title">{{ title }}</div>{% endif %}
  {% if value %}<div class="stat-value">{{ value }}</div>{% endif %}
  {% if desc %}<div class="stat-desc">{{ desc }}</div>{% endif %}
  {% if actions %}<div class="stat-actions">{{ actions }}</div>{% endif %}
</div>
```

- The figure comes first in source order as in daisyUI's examples. daisyUI's grid places it at the end of the row. A value of `0` is falsy in a template, so `value` is tested with `{% if value or value == 0 %}` (Edge Cases: a number renders as text).

`stat/group.html` — `{% load daisy_cotton %}`, `<c-vars vertical="" horizontal="" class="" />`, `<div class="stats {% responsive vertical "stats-vertical" %} {% responsive horizontal "stats-horizontal" %} {{ class }}" {{ attrs }}>{{ slot }}</div>`.

### List (US7)

`list/index.html` — `<c-vars class="" />`, `<ul class="list {{ class }}" {{ attrs }}>{{ slot }}</ul>`.
`list/row.html` — `<c-vars class="" />`, `<li class="list-row {{ class }}" {{ attrs }}>{{ slot }}</li>`.

- The `@description` of `list.row` names `list-col-grow` and `list-col-wrap`, and the gallery's `@slot` examples use them (FR-028).

### Timeline (US8)

`timeline/index.html` — `{% load daisy_cotton %}`, `<c-vars vertical="" horizontal="" compact="" snap-icon="" class="" />`, `<ul class="timeline {% responsive vertical "timeline-vertical" %} {% responsive horizontal "timeline-horizontal" %}{% if compact %} timeline-compact{% endif %}{% if snap_icon %} timeline-snap-icon{% endif %} {{ class }}" {{ attrs }}>{{ slot }}</ul>`.

`timeline/item.html` — `<c-vars start="" middle="" end="" box="" class="" />`.

```
<li class="group {{ class }}" {{ attrs }}>
  <hr class="group-first:hidden" aria-hidden="true" />
  {% if start %}<div class="timeline-start{% if box == "start" %} timeline-box{% endif %}">{{ start }}</div>{% endif %}
  {% if middle %}<div class="timeline-middle">{{ middle }}</div>{% endif %}
  {% if end %}<div class="timeline-end{% if box and box != "start" %} timeline-box{% endif %}">{{ end }}</div>{% endif %}
  <hr class="group-last:hidden" aria-hidden="true" />
</li>
```

- Connectors per research R4. Consecutive items each draw their half of the line between them, which is daisyUI's own markup.

### Kbd and status (US9)

`kbd.html` — `{% load daisy_cotton %}`, `<c-vars text="" size="" class="" />`, `<kbd class="kbd {% variation size "kbd" "xs,sm,md,lg,xl" %} {{ class }}" {{ attrs }}>{{ text }}{{ slot }}</kbd>`.

`status.html` — `{% load daisy_cotton %}`, `<c-vars label="" variant="" size="" class="" />`.

```
<span class="status {% variation variant "status" "neutral,primary,secondary,accent,info,success,warning,error" %} {% variation size "status" "xs,sm,md,lg,xl" %} {{ class }}"{% if label %} role="img" aria-label="{{ label }}"{% else %} aria-hidden="true"{% endif %} {{ attrs }}></span>
```

### Gallery entries (FR-004, FR-005)

Every template carries `@description`, a `@prop` per `<c-vars>` name and `@slot` / `@slot:name` per slot, in the order FS-002 set: description, props in declaration order, default slot, named slots in render order. Fixed-value props are `select[…]` with daisyUI's full list, which gives the gallery's variants matrix every colour and size. Booleans are toggles. Breakpoint-valued props are `select['sm','md','lg','xl','2xl']` with a description saying the bare attribute applies it at every width. One-line examples must not contain `#}` or a spaced em dash (FS-004 plan). Every image example has `alt`, every icon-only control an `aria-label`, and every icon `aria-hidden="true"` (SC-004).

### Documentation

- `README.md`: the component count and list gain each new component in its story.
- `CHANGELOG.md` `[Unreleased]`: `Added` for each new component and `unique_id`. `Changed` for every removed or renamed attribute or slot on `card`, `badge`, `avatar` and `avatar.group`, each with what a project writes instead (FR-008, SC-005).

## Project Structure

### Documentation (this feature)

```text
specs/006-content-display-components/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templates/cotton/
├── card/index.html           # rewritten (US1)
├── modal.html                # adjusted to the new card (US1)
├── table.html                # new (US2)
├── badge.html                # rewritten (US3)
├── collapse.html             # new (US4)
├── accordion.html            # new (US4)
├── avatar/index.html         # rewritten (US5)
├── avatar/group.html         # rewritten (US5)
├── stat/index.html, stat/group.html          # new (US6)
├── list/index.html, list/row.html            # new (US7)
├── timeline/index.html, timeline/item.html   # new (US8)
├── kbd.html, status.html                     # new (US9)
daisy_cotton/templatetags/daisy_cotton.py     # responsive breakpoint check (US1), unique_id (US2)
tests/
├── test_card.py, test_modal.py                # rewritten / adjusted (US1)
├── test_table.py, test_badge.py, test_collapse.py, test_avatar.py,
│   test_stat.py, test_list.py, test_timeline.py, test_kbd.py, test_status.py   # new
└── test_templatetags/test_daisy_cotton.py     # responsive and unique_id tests
pyproject.toml                # new test modules in non-mirror-paths
README.md, CHANGELOG.md
```

**Structure Decision**: templates and their tests, plus one tag. A component with sub-parts is a folder (`stat/index.html` + `stat/group.html`), matching `avatar/`. Components with no parts are single files.

## Story order

One worktree, three dispatch batches on the same branch. Stories touch their own templates and test modules and append to `README.md`, `CHANGELOG.md` and `pyproject.toml`, so they run one after another.

1. US1 (card and modal), US2 (table), US3 (badge): the P1 stories.
2. US4 (collapse and accordion), US5 (avatar), US6 (stat), US7 (list).
3. US8 (timeline), US9 (kbd and status).

## Complexity Tracking

| Addition | Why | Simpler alternative rejected because |
|---|---|---|
| `unique_id` template tag | FR-014: the table's region is named by its caption, which needs an id | `aria-label` copied from the caption breaks on a slot holding markup and doubles up with a caller's own `aria-label` (research R6). |
| Timeline `group` utilities | FR-032: no connector past the first or last item | A component cannot know its position, and daisyUI's CSS does not hide the end connectors (research R4). |
