# Implementation Plan: Core form controls

**Branch**: `009-form-controls` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/009-form-controls/spec.md`

## Summary

Ten new Cotton templates for daisyUI's data input group: `input`, `textarea`, `select`, `checkbox`, `radio`, `toggle`, `range`, `file_input`, `label` and `fieldset`, and `form/field.html` removed with its tests. Each control emits its native element with daisyUI's classes, ships no script and carries its gallery annotations. The label names a control from above (`for`), by wrapping it, or as daisyUI's floating label. The fieldset carries a legend, a description and errors, with ids derived from its own `id`. No Python changes: the existing `variation` tag covers every modifier. The labelled, disabled and invalid examples live in one composition inside the fieldset's gallery entry (research R5).

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added.

**Storage**: none

**Testing**: pytest + pytest-django. Components are rendered through the Cotton compiler as a caller's template would be (the `cotton_render_string` and `cotton_render_string_soup` fixtures in `tests/conftest.py`), never by rendering the component file directly, which skips `<c-vars>` extraction.

**Target Platform**: any host project running daisyUI 5

**Project Type**: Django package (templates) with a demo project

**Constraints**: no JavaScript shipped, no stylesheet, no colour outside the semantic palette, and every daisyUI class a component emits exists in daisyUI 5 for that component

**Scale/Scope**: 10 new templates, 1 removed; 10 new test modules plus one shared module and one removal module, 1 test module removed

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Testing | Every acceptance scenario markup can show gets a test written before the template. Keyboard and screen-reader scenarios run at the walkthrough (research R8). No wording is asserted. | Pass |
| II Simplicity | Templates only. `variation` covers every modifier. | Pass |
| III Anti-Abstraction | No base template and no shared include. The text input and the select each write the same short wrapped form rather than share one. | Pass |
| V Security | Every value reaches the page through `{{ }}` autoescaping, including each error message (research R4). No value is written into `style` or a script. | Pass |
| VI Documentation | README and CHANGELOG lines land in the story that introduces each name. The removal and its migration notes land together in US3 (FR-023). | Pass |
| VII Dependency discipline | No new dependency. | Pass |
| VIII i18n | No component writes a string of its own. | Pass |
| X Test structure | One test module per component, `Test<Subject>` classes, new modules in `non-mirror-paths` like the existing component tests. | Pass |
| XI Agnostic | Gallery examples use neutral copy. | Pass |
| XII Semantic palette | Colour only through validated `variant`, and `text-error` on the fieldset's error lines. The errors' wrapper carries the layout utility `grid`, as other packaged templates carry `flex` and `w-full`. | Pass |
| XIII Attribute vocabulary | `variant`, `size`, `ghost` and `vertical` as daisyUI names them, merged `class`, the rest through `{{ attrs }}`. The wrapped input and select send `class` to the wrapper and every other attribute to the control (FR-009, spec Clarifications). `start` and `end` reuse the navbar's names. | Pass |
| XIV Composition | Gallery examples compose `<c-label>`, `<c-fieldset>`, the controls, `<c-icon>` and `<c-kbd>`. The components themselves call no other component. | Pass |
| XV Gallery annotations | Every template annotated, fixed-value props typed `select[…]`, `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below:

- **Modifiers.** `variant` and `size` go through `{% variation … %}` against daisyUI's lists (research R1): the eight colours `neutral,primary,secondary,accent,info,success,warning,error` and the sizes `xs,sm,md,lg,xl`. An unknown value adds nothing and nothing raises (Edge Cases). `ghost` and `vertical` are booleans.
- **Root.** Every component declares `class`, merges it into the root's class list, and spreads `{{ attrs }}` on the element the spec names (FR-002). For the controls that is the native form element. The wrapped input and select are the one split (below).
- **Native states pass through.** `name`, `value`, `id`, `checked`, `disabled`, `required`, `placeholder`, `aria-invalid`, `aria-describedby` and the rest are not declared: they reach the element through `{{ attrs }}` (research R4, FR-005, FR-009). The error colour and `aria-invalid` are never set by a component (FR-006).
- **Defaults.** Every declared name gets a default, so a page variable of the same name never leaks in (research R4). `=""` everywhere except the input's `type="text"` and the range's `min="0"` and `max="100"`. Annotations give no `default:` for empty defaults, and a `select` must not get `default:""`.
- **Named slots.** Declared once in `<c-vars>` with an empty default and rendered only when non-empty. Each gets a `@prop` and a `@slot:name`, as the navbar's `start` and `end` do.
- **Shared rules, tested once.** Three rules hold for every component and are each one parametrised test in one module, `tests/test_form_controls.py`, that each story extends by adding its components' rows: no `<script>` and no `on*=` attribute in the rendered output (FR-005, SC-003; FS-008's `tests/test_feedback_no_script.py` is the model); no `aria-invalid` and no `*-error` class when the caller gives neither (FR-006, controls only); and a page context carrying the component's declared names leaves its own defaults in place (research R4). The testing standard asks for one parametrised test over a rule, not one copy per subject (`docs/contributing/standards/testing.md` §5).
- **One line of markup.** The controls are single elements, so each template is its annotations, `<c-vars>` and one line of markup inside `{# djlint:off #}`, as `progress.html` is.

### Text input (US1)

`input.html` — `{% load daisy_cotton %}`, `<c-vars type="text" variant="" size="" ghost="" start="" end="" class="" />`.

```
{% if start or end %}<label class="input {% variation variant "input" "…eight…" %} {% variation size "input" "xs,sm,md,lg,xl" %}{% if ghost %} input-ghost{% endif %} {{ class }}">{{ start }}<input type="{{ type }}" {{ attrs }}>{{ end }}</label>{% else %}<input type="{{ type }}" class="input …same modifiers… {{ class }}" {{ attrs }}>{% endif %}
```

- Unwrapped, it is one `<input>` and composes inside a join (US1-5).
- Wrapped, the `<label>` carries `input`, the modifiers and `class`. The inner `<input>` carries no class, as daisyUI writes it (research R2), and every other attribute (FR-008, FR-009).
- `type` is typed `select[…]` with the text-like types `form.field` offered (`text`, `email`, `password`, `number`, `tel`, `url`, `search`, `date`, `time`, `datetime-local`, `month`, `week`, `color`), default `text`. The description says checkbox, radio, range and file have their own components and the input does not refuse those types (Edge Cases).
- The description says: `size` is daisyUI's scale, not the native `size` attribute (research R6); a control needs `<c-label>`, `aria-label` or `aria-labelledby` for a name, and the component cannot invent one; start and end content goes inside the box, written as `<span class="label">` for daisyUI's inline label; it names the fieldset entry for labelled, wrapped, disabled and invalid examples.

### Label (US2)

`label.html` — `<c-vars text="" floating="" class="" />`.

```
{% if floating %}<label class="floating-label {{ class }}" {{ attrs }}>{{ slot }}<span>{{ text }}</span></label>{% else %}<label class="label {{ class }}" {{ attrs }}>{{ slot }}{{ text }}</label>{% endif %}
```

- Above a control: `<c-label for="id_email" text="Email" />` renders `<label class="label" for="id_email">Email</label>` (US2-1). `for` passes through.
- Around a control: the slot comes first, then the text, as daisyUI writes a checkbox and its text (research R2, US2-2).
- Floating: the field first, then the `<span>` as a direct child (research R2, R3, US2-3).
- The description says: the `for` id must match the control's `id` or it names nothing (Edge Cases); float a label only around an unwrapped input, textarea or select, and give the field a placeholder, since daisyUI floats the label while the field shows its placeholder (research R3, Edge Cases); `class="sr-only"` hides it visually and keeps the name; it names the fieldset entry for all three forms.

### Fieldset (US2)

`fieldset.html` — `<c-vars legend="" description="" errors="" id="" class="" />`.

```
<fieldset class="fieldset {{ class }}"{% if id %} id="{{ id }}"{% endif %} {{ attrs }}>{% if legend %}<legend class="fieldset-legend">{{ legend }}</legend>{% endif %}{{ slot }}{% if description %}<p class="label"{% if id %} id="{{ id }}-description"{% endif %}>{{ description }}</p>{% endif %}{% if errors %}<div class="grid"{% if id %} id="{{ id }}-errors"{% endif %}>{% if errors == errors|stringformat:"s" %}<p class="label text-error">{{ errors }}</p>{% else %}{% for error in errors %}<p class="label text-error">{{ error }}</p>{% endfor %}{% endif %}</div>{% endif %}</fieldset>
```

- `legend`, `description` and `errors` are attributes and named slots under the same names (FR-019, FR-020). A slot's content is a string and renders as one line.
- `id` is declared so the template can derive from it. It is emitted on the fieldset only when given, and never twice.
- The derived ids are `<id>-description` and `<id>-errors`. The errors sit in one `<div class="grid">` carrying `<id>-errors`, so a control names every message with one id however many there are (FR-021). `grid` stacks the lines: daisyUI's `.label` is `inline-flex`, and only the fieldset's direct children are grid items, so without it the messages run together on one line. The div renders only when there are errors.
- An empty string, an empty list and an absent value all render nothing (US2-7, Edge Cases).
- The description states both derived ids, shows `aria-describedby="<id>-description <id>-errors"` on a control, says the legend names the group and not a control inside it (a fieldset holding one control still gives it a `<c-label>`), says a description or message containing HTML is escaped and the named slot takes markup, notes that daisyUI's description line does not wrap (research R3), says a named slot filled with whitespace only still renders its element, and names its own composition for every control.

### Textarea and select (US4)

`textarea.html` — `{% load daisy_cotton %}`, `<c-vars variant="" size="" ghost="" class="" />`.

```
<textarea class="textarea …modifiers… {{ class }}" {{ attrs }}>{{ slot }}</textarea>
```

`select.html` — `{% load daisy_cotton %}`, `<c-vars variant="" size="" ghost="" start="" end="" class="" />`. The input's two forms with `select` in place of `input`, and `<select {{ attrs }}>{{ slot }}</select>` in place of the `<input>` (FR-011).

- The textarea's value is the slot exactly as the caller wrote it (research R4), and its description says so.
- The select's description says the slot holds its `<option>` elements, `size` is daisyUI's scale and not the native row count (research R6), and a floating label always sits in its floated position around a select (research R3).

### Checkbox, radio and toggle (US5)

`checkbox.html`, `radio.html`, `toggle.html` — `{% load daisy_cotton %}`, `<c-vars variant="" size="" class="" />`.

```
<input type="checkbox" class="checkbox …modifiers… {{ class }}" {{ attrs }}>
<input type="radio" class="radio …modifiers… {{ class }}" {{ attrs }}>
<input type="checkbox" role="switch" class="toggle …modifiers… {{ class }}" {{ attrs }}>
```

- `type`, and the toggle's `role="switch"`, are written by the template (FR-014, research R7). A caller passes neither: a second `type` or `role` would reach the element as a duplicate attribute, which the browser resolves to the first. Each description says so. Neither is declared, because a declared name the template does not read fails `tests/test_declared_attributes.py`.
- The checkbox's description says its indeterminate state can only be set from the project's own script. The radio's says to give every radio in a group the same `name`, and to group them in a `<c-fieldset>` whose legend names the group. Each names the fieldset entry.

### File input and range (US6)

`file_input.html` — `{% load daisy_cotton %}`, `<c-vars variant="" size="" ghost="" class="" />`.

```
<input type="file" class="file-input …modifiers…{% if ghost %} file-input-ghost{% endif %} {{ class }}" {{ attrs }}>
```

`range.html` — `{% load daisy_cotton %}`, `<c-vars variant="" size="" vertical="" min="0" max="100" class="" />`.

```
<input type="range" min="{{ min }}" max="{{ max }}" class="range …modifiers…{% if vertical %} range-vertical{% endif %} {{ class }}" {{ attrs }}>
```

- `min` and `max` are declared with the browser's own defaults, so they are always emitted and never twice (FR-016). `value` and `step` pass through.
- Cotton resolves `<c-file-input>` to `file_input.html` (research R4).

### Removing `form.field` (US3)

- `daisy_cotton/templates/cotton/form/field.html` and `tests/test_form_field.py` are deleted, and the empty `form/` directory with them. No alias, no stub (FR-022).
- A new `tests/test_form_field_removed.py` asserts that rendering `<c-form.field />` raises `TemplateDoesNotExist` with `form/field` in its message (US3-1), under pytest-django's default `DEBUG=False`: with `DEBUG=True`, Django's debug-info step fails first on the compiled node and hides the real error.
- `docs/adr/0001-icon-is-an-extension-point.md` lists `form.field`'s pre/post-label slots among the components that call `<c-icon>`. `form.field` never called `<c-icon>` itself, so that entry is deleted from the parenthesised list and nothing is added, and the record keeps describing the package as it is.
- `CHANGELOG.md` gains `### Removed` under `[Unreleased]` (see Documentation). The existing `Added` line listing the first 21 components stays as it is. The sentence at the end of `Added` that excludes form rendering "beyond the single presentational `form.field`" is reworded to describe the package without it, and `docs/ROADMAP.md`'s "`form.field` covers part of fieldset today" is brought up to date the same way.

### Gallery entries (FR-003, FR-004)

Every template carries `@description`, a `@prop` per `<c-vars>` name and `@slot` / `@slot:name` per slot, in FS-002's order. `variant` and `size` are `select[…]` with daisyUI's full lists. One-line examples must not contain `#}`, `{{`, `{%` or a spaced em dash before the description separator.

| Entry | Default slot / named slots |
|---|---|
| input | No default slot. `@slot:start` and `@slot:end` with no sample, so the bare preview is one `<input>`. |
| label | `@slot` `Email`. |
| fieldset | `@slot:legend` `Account`. `@slot` the composition below. `@slot:description` with a one-line sample. `@slot:errors` with no sample. |
| textarea | `@slot` a one-line sample value. |
| select | `@slot` three `<option>` elements. `@slot:start` and `@slot:end` with no sample. |
| checkbox, radio, toggle, file input, range | No slot. |

**The composition (research R5).** The fieldset entry's `@slot` holds nested fieldsets, one per section, and every story adds its controls to it. Every control in it has an accessible name, and every control appears at least once disabled and once invalid (`variant="error" aria-invalid="true"`). Ids are unique within the composition.

| Story | Adds to the composition |
|---|---|
| US2 | A `<c-fieldset id="account-email">` with a description and an error: `<c-label for>` above a required `<c-input type="email">` that is invalid and names both derived ids in `aria-describedby` (US2-8, US1-7). A floating `<c-label>` around a `<c-input placeholder>`. A labelled `<c-input type="url">` with `start` `<span class="label">https://</span>`. A `<c-input type="search" aria-label>` with a `<c-icon aria-hidden="true">` in `start` and a `<c-kbd>` in `end`. A labelled disabled `<c-input>`. |
| US4 | A labelled `<c-textarea>`, an invalid one and a disabled one. A labelled `<c-select>`, a `<c-select>` whose `start` holds `<span class="label">` text that names it, a floating `<c-label>` around a `<c-select>`, an invalid select and a disabled one (US4-5). |
| US5 | A `<c-fieldset legend>` holding three `<c-label>`-wrapped `<c-radio>`s sharing a `name`, one checked and one disabled, and one invalid radio (US2-8, US5-4). A `<c-label>`-wrapped checked `<c-checkbox>`, an invalid one and a disabled one. A `<c-label>`-wrapped checked `<c-toggle>`, an invalid one and a disabled one (US5-6). |
| US6 | A labelled `<c-file-input>`, an invalid one and a disabled one. A labelled `<c-range>` with a value, a labelled vertical range, an invalid one and a disabled one (US6-5). |

Each control's `@description` names the fieldset entry as where its labelled, disabled and invalid examples are. The bare control previews carry only declared defaults and are unnamed by construction, as FS-008 D5 recorded for the progress: their descriptions tell the developer to type `aria-label` in the attributes field.

### Documentation

- `README.md`: the component count goes from Sixty-nine to Seventy-eight in words, one step per story, and the alphabetical list gains each new component in its story (`checkbox`, `fieldset`, `file-input`, `input`, `label`, `radio`, `range`, `select`, `textarea`, `toggle`). US3 removes `form.field` from the list (FR-024).
- `CHANGELOG.md` `[Unreleased]`: `Added` per new component in its story, each naming its attributes and slots. US3 adds `### Removed` for `form.field`: before-and-after examples for a labelled text input, a textarea, a select, a file input, a checkbox, a radio button, a toggle, a field with help text, a field with errors, and an input with `prelabel` and `postlabel`, then `hide-label`, `wrapper-class`, `prelabel`, `postlabel` and the required asterisk each with its replacement or the reason it was dropped (FR-023, spec Clarifications). Before `tests/test_form_field.py` is deleted, each of its tests is mapped to the example or table row that rebuilds it, and any case left unmapped gets one more before-and-after line (SC-004).

## Project Structure

### Documentation (this feature)

```text
specs/009-form-controls/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templates/cotton/
├── input.html                                  # new (US1)
├── label.html, fieldset.html                   # new (US2)
├── textarea.html, select.html                  # new (US4)
├── checkbox.html, radio.html, toggle.html      # new (US5)
├── file_input.html, range.html                 # new (US6)
└── form/field.html                             # removed (US3)
tests/
├── test_input.py, test_label.py, test_fieldset.py, test_textarea.py, test_select.py,
│   test_checkbox.py, test_radio.py, test_toggle.py, test_file_input.py, test_range.py   # new
├── test_form_controls.py                        # new, extended per story
├── test_form_field_removed.py                  # new (US3)
└── test_form_field.py                          # removed (US3)
docs/adr/0001-icon-is-an-extension-point.md     # one sentence (US3)
pyproject.toml                # new test modules in non-mirror-paths, the removed one dropped
README.md, CHANGELOG.md
```

**Structure Decision**: one flat template per daisyUI component, named after it, as every other component is (spec Clarifications, "No `form.` prefix").

## Story order

One worktree, stories one after another: they share `README.md`, `CHANGELOG.md`, `pyproject.toml`, the shared module and the fieldset's composition.

1. US1 text input, US2 label and fieldset (the composition starts here, with the input), then a checkpoint.
2. US4 textarea and select, US5 checkbox, radio and toggle, US6 file input and range, each adding to the composition, then a checkpoint.
3. US3 removes `form.field` last, because its CHANGELOG examples use every control. It is P1 and still ships in this pull request, with the components that replace it.

## Complexity Tracking

| Addition | Why | Simpler alternative rejected because |
|---|---|---|
| One composition inside the fieldset's gallery entry | FR-004 asks for labelled, disabled and invalid examples of every control, and the gallery shows one preview per entry with declared defaults only (research R5) | A demo page of its own is ruled out by FS-001 FR-001. Declaring `disabled` on every control to get a gallery toggle would add eight declared names that do nothing `{{ attrs }}` does not already do. |
