# Implementation Plan: Specialised inputs

**Branch**: `010-specialised-inputs` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/010-specialised-inputs/spec.md`

## Summary

Four new Cotton templates under `templates/cotton/form/`, called `<c-form.filter>`, `<c-form.calendar>`, `<c-form.otp>` and `<c-form.rating>` (D1). The filter and rating are radio groups whose items the template builds from plain values. The OTP is daisyUI's `<label class="otp">` with one box per digit and one input. The calendar emits Cally's elements with daisyUI's `cally` class and its paging icons through `<c-icon>`, and the demo loads Cally so the gallery shows it working. Three small template tags do what Django's template language cannot: build a numeric range, normalise a filter's options, and lay out a rating's items (research R4). No component ships a script.

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added. Cally is loaded by the demo from a CDN and is not a dependency of anything.

**Storage**: none

**Testing**: pytest + pytest-django. Components render through the Cotton compiler as a caller's template would (`cotton_render_string` and `cotton_render_string_soup` in `tests/conftest.py`). The template tags are tested directly in `tests/test_templatetags/test_daisy_cotton.py`.

**Target Platform**: any host project running daisyUI 5. The calendar also needs the project to load Cally.

**Project Type**: Django package (templates and template tags) with a demo project

**Constraints**: no JavaScript shipped, no stylesheet, no colour outside the semantic palette, every daisyUI class a component emits exists in daisyUI 5 for that component, every accessible name a component writes is translatable

**Scale/Scope**: 4 new templates, 3 new template tags, 4 new test modules, 2 extended ones, the fieldset's gallery composition, the demo head, README and CHANGELOG

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Testing | Every acceptance scenario markup can show gets a test written before the template. Keyboard, focus and screen-reader scenarios run at the walkthrough (research R8). No wording is asserted: tests find elements by role, attribute and structure. | Pass |
| II Simplicity | Three template tags, each justified in Complexity Tracking. Everything else is template markup. | Pass |
| III Anti-Abstraction | No base template. The filter and rating each write their own radio loop. | Pass |
| V Security | Every value, including each option label and the generated names, reaches the page through `{{ }}` autoescaping. No value is written into `style` or a script. | Pass |
| VI Documentation | Each story writes its README and CHANGELOG lines and its gallery annotations. US2 adds the calendar's Cally instructions to the README (FR-018), and US1 adds the scope notes (FR-008). | Pass |
| VII Dependency discipline | No new dependency. | Pass |
| VIII i18n | "Clear filter", "Verification code", "Previous", "Next", "No rating", the per-item rating names and "`value` out of `max`" are `{% trans %}` / `{% blocktrans %}` strings (research R7). | Pass |
| X Cohesion | The three tags are decorator-registered template tags beside `variation` and `unique_id`, the case the article exempts. | Pass |
| XI Agnostic | Gallery examples use neutral copy. Cally is loaded only by the demo. | Pass |
| XII Semantic palette | Colour only through validated `variant`: `btn-*`, `otp-*`, and `bg-*` on rating items. | Pass |
| XIII Attribute vocabulary | `variant`, `size`, `joined`, `half` and `range` as daisyUI and Cally name them, `shape` reused from `<c-mask>`, `label` reused from the components that name themselves, `input_class` reused from the swap. `class` merged into the root. Other attributes per D2. | Pass |
| XIV Composition | The calendar draws its icons with `<c-icon>` (FR-007). The filter's options are radio inputs carrying `btn`, which `<c-button>` does not emit (spec decisions). | Pass |
| XV Gallery annotations | Every template annotated, fixed-value props typed `select[…]`, `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below:

- **Namespace.** Templates live in `templates/cotton/form/`: `filter.html`, `calendar.html`, `otp.html`, `rating.html` (D1).
- **Modifiers.** `variant` and `size` go through `{% variation … %}` against daisyUI's lists: the eight colours `neutral,primary,secondary,accent,info,success,warning,error` and `xs,sm,md,lg,xl`. An unknown value adds nothing and raises nothing. `shape` goes through `variation` against `star,star-2,heart`.
- **Attribute routing (D2).** The OTP follows FS-009's rule for a single control: `class` on the element carrying daisyUI's class (the `<label class="otp">`), every other attribute through `{{ attrs }}` to the `<input>`. The filter and rating are groups of radios: `name`, `value`, `required`, `disabled` and `form` are declared and written on every radio, and everything else, `id` included, goes through `{{ attrs }}` to the wrapper, where the group lives.
- **Generated names.** When `name` is empty, `{% unique_id "filter" as generated_name %}` (or `"rating"`) supplies one, so two groups on a page never share radios (FR-013, FR-030).
- **Defaults.** Every declared name gets a default so a page variable of the same name never leaks in. Annotations give no `default:` for empty defaults, and a `select` never gets `default:""`.
- **Numbers.** A `length`, `max` or `months` that is not a positive whole number falls back to the component's default (6, 5, 1). It never raises.
- **Shared rules, tested once.** A new `tests/test_specialised_inputs.py`, extended per story, holds one parametrised test per rule, as `tests/test_form_controls.py` does for FS-009: no `<script>` and no `on*=` attribute in the rendered output (SC-003), and a page context carrying the component's declared names leaves its own defaults in place.
- **One line of markup.** Each template's markup sits inside `{# djlint:off #}`, as the form controls do.

### Template tags

Added to `daisy_cotton/templatetags/daisy_cotton.py`, each a `@register.simple_tag` with a Google-style docstring:

- `count_range(value, default)` returns `range(n)`, where `n` is `value` as a positive integer, or `default` when it is not one. Used as `{% count_range length 6 as boxes %}` for the OTP (`boxes|length` gives the digit count) and `{% count_range months 1 as offsets %}` for the calendar.
- `filter_options(options, value)` returns one dict per entry: `{"value", "label", "checked"}`. A list or tuple of two is a (value, label) pair, anything else is its own label. `checked` compares `str(entry value)` with `str(value)` when `value` is not empty. A non-iterable or empty `options` gives an empty list.
- `rating_items(max, half, value)` returns one dict per item: `{"value", "half", "whole", "checked"}`, in order. Whole ratings give values `"1"` to `str(max)`. Half ratings give `"0.5"`, `"1"`, `"1.5"` … `str(max)`, with `half` `1` or `2` alternating, and `whole` true on whole values. `checked` is true on the item whose numeric value equals `value`, compared as numbers, so `7`, `"7"` and `"7.0"` all match. A `value` that is empty, not a number, out of range or not a multiple of the step checks nothing (Edge Cases). `max` falls back to 5 as above.

Tests in `tests/test_templatetags/test_daisy_cotton.py`, one class per tag.

### Filter (US1)

`form/filter.html` — `{% load i18n daisy_cotton %}`, `<c-vars options="" value="" name="" label="" reset_label="" variant="" size="" required="" disabled="" form="" class="" />`.

```
<div class="filter {{ class }}" role="radiogroup"{% if label %} aria-label="{{ label }}"{% endif %} {{ attrs }}>
  <span class="sr-only" id="{{ reset_id }}">{% if reset_label %}{{ reset_label }}{% else %}{% trans "Clear filter" %}{% endif %}</span>
  <input type="radio" class="btn filter-reset {{ modifiers }}" name="{{ name or generated }}" value="" aria-label="×" aria-labelledby="{{ reset_id }}" {{ shared }}>
  {% for option in items %}<input type="radio" class="btn {{ modifiers }}" name="…" value="{{ option.value }}" aria-label="{{ option.label }}"{% if option.checked %} checked{% endif %} {{ shared }}>{% endfor %}
</div>
```

- `reset_id` comes from `{% unique_id "filter-reset" as reset_id %}`. `modifiers` is `btn-{variant}` and `btn-{size}` through `variation` (FR-012). `shared` is `required`, `disabled` and `form` when given (D2).
- The hidden span comes first so daisyUI's gap rule is unaffected (research R2).
- The reset carries `value=""`, so choosing it submits the name with an empty value (US1-4). Nothing is checked unless `value` matches an option, as daisyUI's rules ask.
- The description says: `name` is needed for anything submitted; give at least one option; `label` names the group, or leave it out when a fieldset legend names it; the reset shows "×" and is announced by `reset_label`; `:options` takes values or (value, label) pairs, such as a form field's `choices`; other button styles come from overriding the component. It names the fieldset entry for filters with options.

### Calendar (US2)

`form/calendar.html` — `{% load i18n daisy_cotton %}`, `<c-vars range="" months="1" previous_icon="chevron-left" next_icon="chevron-right" class="" />`.

```
{% count_range months 1 as offsets %}
<calendar-date|calendar-range class="cally {{ class }}"{% if offsets|length > 1 %} months="{{ offsets|length }}"{% endif %} {{ attrs }}>
  <span slot="previous"><c-icon name="{{ previous_icon }}" aria-hidden="true" only /><span class="sr-only">{% trans "Previous" %}</span></span>
  <span slot="next"><c-icon name="{{ next_icon }}" aria-hidden="true" only /><span class="sr-only">{% trans "Next" %}</span></span>
  {% for offset in offsets %}<calendar-month{% if offset %} offset="{{ offset }}"{% endif %}></calendar-month>{% endfor %}
</calendar-date|calendar-range>
```

- `range` picks `<calendar-range>` (FR-014). `months` above 1 is also written on the root, where Cally reads it to page by that many months (research R3). `value`, `min`, `max`, `locale`, `first-day-of-week` and the rest reach the root through `{{ attrs }}` unchanged (FR-017).
- The paging content is a `<span>` carrying the slot, holding an `aria-hidden` `<c-icon>` and the visually hidden translatable name. Cally puts it inside its own button, so the button is named "Previous" or "Next" (FR-016, research R6). `<c-icon>` gets `only`, as the menu and dock do, so the calendar's own `class` never reaches the icon.
- `previous_icon` and `next_icon` default to the names `chevron-left` and `chevron-right`, which a project's own `<c-icon>` resolves (ADR 0001). With the bare `<c-icon>` the caller passes icon classes, as the gallery composition does (D4).
- `months` is typed `select['1','2','3']` with `default:"1"`, `range` a boolean.
- The description puts first that the project loads Cally and nothing shows until it does, then how to load it, then the input-copying script's location (the README), then the fieldset entry for more examples.
- `README.md` gets a "Calendar" usage section: the one-line module script tag, a `<c-form.calendar>` example, and a short script that copies the chosen date from the `change` event into a hidden input (FR-018, US2-7). The package ships none of it.

### OTP (US3)

`form/otp.html` — `{% load i18n daisy_cotton %}`, `<c-vars length="6" label="" variant="" size="" joined="" pattern="" inputmode="numeric" input_class="" class="" />`.

```
{% count_range length 6 as boxes %}
<label class="otp {{ modifiers }}{% if joined %} otp-joined{% endif %} {{ class }}">{% for _ in boxes %}<span></span>{% endfor %}<input type="text" maxlength="{{ boxes|length }}" pattern="{% if pattern %}{{ pattern }}{% else %}[0-9]{{ '{' }}{{ boxes|length }}{{ '}' }}{% endif %}" inputmode="{{ inputmode }}" autocomplete="one-time-code"{% if input_class %} class="{{ input_class }}"{% endif %} {{ attrs }}><small class="sr-only">{% if label %}{{ label }}{% else %}{% trans "Verification code" %}{% endif %}</small></label>
```

- `modifiers` are `otp-{variant}` and `otp-{size}` (FR-021).
- The boxes are the label's first children, the input follows, and the hidden name is a `<small>` after the input, so daisyUI counts only the boxes (research R2, FR-022). The implementer confirms how the pattern's braces render and picks whichever template form outputs `[0-9]{6}` literally.
- `pattern` and `inputmode` are declared so a project with letter codes can replace them without a duplicate attribute (spec decisions "The OTP defaults to six digits"). Empty `pattern` means digits only, exactly `length` of them.
- `id`, `name`, `value`, `required`, `disabled`, `autofocus`, `form` and every other attribute reach the input through `{{ attrs }}` (FR-023, D2).
- `length` is typed `select['4','5','6']` with `default:"6"`. The description says daisyUI styles four to six boxes (Edge Cases), that validation styling comes from adding `validator` through `input_class`, and names the fieldset entry for the disabled and labelled examples.

### Rating (US4)

`form/rating.html` — `{% load i18n daisy_cotton %}`, `<c-vars max="5" value="" name="" label="" shape="star" variant="" size="" half="" clearable="" readonly="" required="" disabled="" form="" class="" />`.

Interactive:

```
<div class="rating {{ size_class }}{% if half %} rating-half{% endif %} {{ class }}" role="radiogroup"{% if label %} aria-label="{{ label }}"{% endif %} {{ attrs }}>
  {% if clearable %}<input type="radio" class="rating-hidden" name="…" value="" aria-label="{% trans "No rating" %}"{% if not value %} checked{% endif %} {{ shared }}>{% endif %}
  {% for item in items %}<input type="radio" class="mask {{ shape_class }}{% if item.half %} mask-half-{{ item.half }}{% endif %} {{ bg_class }}" name="…" value="{{ item.value }}" aria-label="…" {% if item.checked %} checked{% endif %} {{ shared }}>{% endfor %}
</div>
```

Read-only:

```
<div class="rating …same classes…" role="img" aria-label="{% blocktrans %}{{ value }} out of {{ max }}{% endblocktrans %}" {{ attrs }}>
  {% for item in items %}<div class="mask …"{% if item.checked %} aria-current="true"{% endif %}></div>{% endfor %}
</div>
```

- Each radio's `aria-label` is `{% blocktrans count counter=… %}{{ counter }} star{% plural %}{{ counter }} stars{% endblocktrans %}` on whole values and `{% blocktrans %}{{ value }} stars{% endblocktrans %}` on half values (research R7, FR-026).
- `bg_class` is `bg-{variant}` through `variation`, `size_class` is `rating-{size}`, `shape_class` is `mask-{shape}` (FR-025).
- `clearable` adds the hidden first radio, checked when no `value` is given (FR-027). It is not rendered when read-only.
- The read-only items carry no `aria-label` (research R6). With no `value` the read-only name reads "0 out of `max`" and no item is current.
- `shape` is typed `select['star','star-2','heart']` with `default:"star"`. The description says `name` is needed for anything submitted, `label` names the group unless a fieldset legend does, `readonly` shows a score and submits nothing, and names the fieldset entry for disabled and read-only examples.

### Gallery entries (FR-003, FR-004)

Every template carries `@description`, a `@prop` per `<c-vars>` name, and no `@slot` (none of the four renders a slot). `variant`, `size`, `shape`, `length` and `months` are `select[…]`, the booleans `boolean`.

The composed examples go in the fieldset entry's `@slot` composition (research R5), each story appending one nested `<c-form.fieldset legend="…">` section. Ids and generated names stay unique within the composition. Every control in it has an accessible name.

| Story | Adds to the composition |
|---|---|
| US1 | A fieldset "Status" holding a filter named `status` with nothing chosen, its legend as the visible label (US1-9). A filter with `label`, three (value, label) options and one chosen. Filters in `primary` and `sm`, and `accent` and `lg`. |
| US2 | A fieldset "Delivery date" holding a calendar with `min` and `max` and bootstrap-icons classes for the paging icons, and a two-month range calendar (US2-8). |
| US3 | A fieldset "Two-step verification" holding a labelled OTP, a four-digit joined OTP and a disabled OTP (US3-7). |
| US4 | A fieldset "Your rating" holding a clearable rating, a half-star rating with a value, a disabled rating and a read-only rating with a value (US4-9). |

The bare previews cover what the declared props reach through the gallery's controls: filter colours and sizes with only the reset showing, OTP lengths, colours, sizes and joined, rating shapes, sizes, colours, half, clearable and read-only, the calendar's range and month count.

### Demo

`demo/templates/django_cotton_gallery/_extra_head.html` adds `<script type="module" src="https://unpkg.com/cally"></script>` to the preview documents beside daisyUI and Alpine, with a comment saying the demo loads Cally so the calendar's entry works and the package does not (FR-018, research R3). US2.

### Documentation

- `README.md`: the component count goes up by one in words per story, and the alphabetical list gains `form.filter`, `form.calendar`, `form.otp` and `form.rating` in their stories. US1 adds to the *Scope & philosophy* section that validator has no component (a class added to an input through `class` or the OTP's `input_class`) and US2 that the calendar needs Cally (FR-008). US2 adds the calendar usage section.
- `CHANGELOG.md` `[Unreleased]` `Added`: one line per component in its story, naming its attributes and the elements they reach.

## Project Structure

### Documentation (this feature)

```text
specs/010-specialised-inputs/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templatetags/daisy_cotton.py      # count_range, filter_options, rating_items
daisy_cotton/templates/cotton/form/
├── filter.html     # new (US1)
├── calendar.html   # new (US2)
├── otp.html        # new (US3)
├── rating.html     # new (US4)
└── fieldset.html   # gallery composition extended per story
demo/templates/django_cotton_gallery/_extra_head.html   # loads Cally (US2)
tests/
├── test_filter.py, test_calendar.py, test_otp.py, test_rating.py   # new
├── test_specialised_inputs.py                                     # new, extended per story
└── test_templatetags/test_daisy_cotton.py                         # extended
pyproject.toml     # new test modules in non-mirror-paths
README.md, CHANGELOG.md
```

**Structure Decision**: one template per daisyUI component under `templates/cotton/form/`, beside the core form controls (D1).

## Story order

One worktree, stories one after another: they share the template tag module and its tests, `README.md`, `CHANGELOG.md`, `pyproject.toml`, the shared test module and the fieldset composition.

1. US1 filter (brings `filter_options`), then US2 calendar (brings `count_range` and the demo's Cally), then a checkpoint.
2. US3 OTP (uses `count_range`), then US4 rating (brings `rating_items`), then a checkpoint.

## Complexity Tracking

| Addition | Why | Simpler alternative rejected because |
|---|---|---|
| `count_range` tag | The OTP needs `length` boxes and the calendar `months` month elements, and the template language has no numeric range | A `"x"|rjust:length` string loop hides intent and breaks on a non-number |
| `filter_options` tag | Options arrive as plain values or pairs (spec Clarifications), and the template language cannot tell a pair from a string or compare an int value with a string one | Child components per option were rejected in the spec's decisions. `stringformat` comparisons fail for integer values. |
| `rating_items` tag | Half steps, alternating half classes and a checked item compared as numbers | Doing it in the template needs arithmetic Django templates do not have |
| Composed examples in the fieldset entry | The filter's bare preview has no options, and disabled and read-only states are not reachable from props (research R5) | A sample default for `options` is a lint error, and a demo page of its own is ruled out by FS-001 FR-001 |
