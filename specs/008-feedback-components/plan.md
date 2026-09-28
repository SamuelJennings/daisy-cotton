# Implementation Plan: Feedback components

**Branch**: `008-feedback-components` | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/008-feedback-components/spec.md`

## Summary

One rewritten Cotton template and six new ones for daisyUI's Feedback group: `alert` is rebuilt on the attribute vocabulary and the accessibility bar, and `loading`, `progress`, `radial-progress`, `skeleton`, `toast` and `tooltip` are added. Each renders daisyUI 5's documented markup, ships no script and carries its gallery annotations. The alert keeps its Alpine.js attributes and now draws its dismiss control with `<c-button>`. No Python changes: the existing `variation` and `responsive` tags cover every modifier. Scenarios that need several instances or markup beside the component are shown inside the slot examples of `toast`, `mockup.browser` and `mockup.phone` (research R7).

## Technical Context

**Language/Version**: Python 3.12–3.13, Django 5.2–6.1

**Primary Dependencies**: django-cotton 2.6+ (runtime). django-cotton-gallery 1.x and the shared test bundle (dev). Nothing added.

**Storage**: none

**Testing**: pytest + pytest-django. Components are rendered through the Cotton compiler as a caller's template would be (the `cotton_render_string` and `cotton_render_string_soup` fixtures in `tests/conftest.py`), never by rendering the component file directly, which skips `<c-vars>` extraction.

**Target Platform**: any host project running daisyUI 5

**Project Type**: Django package (templates) with a demo project

**Constraints**: no JavaScript shipped, no stylesheet, no literal colours, no class daisyUI does not define for the component

**Scale/Scope**: 1 rewritten and 6 new templates, 7 new test modules plus one no-script module, annotation changes on 2 existing templates (`mockup.browser`, `mockup.phone`)

## Constitution Check

| Article | Check | Result |
|---|---|---|
| I Testing | Every acceptance scenario markup can show gets a test written before the template. Fixed wording is not asserted: a translatable name is tested by patching gettext, not by its English text. In-browser scenarios run at the walkthrough (research R9). | Pass |
| II Simplicity | Templates only. `variation` and `responsive` cover every modifier. | Pass |
| III Anti-Abstraction | No base template, no shared include. | Pass |
| V Security | Every value reaches the page through `{{ }}` autoescaping. The radial progress writes `value` into `style` as the countdown does: escaping keeps it inside the attribute, not inside the declaration, so its description says the value is a number and never unvalidated user input (research R8). | Pass |
| VI Documentation | README and CHANGELOG lines land in the story that introduces each name. The alert's breaking changes are listed under CHANGELOG `Changed` (FR-009, SC-005). | Pass |
| VII Dependency discipline | No new dependency. | Pass |
| VIII i18n | "Dismiss" and "Loading" are `{% trans %}` strings. No other component writes a string of its own. | Pass |
| X Test structure | One test module per component, `Test<Subject>` classes, new modules in `non-mirror-paths` like the existing component tests. | Pass |
| XI Agnostic | Gallery examples use neutral copy. | Pass |
| XII Semantic palette | Colour only through validated `variant` and semantic utilities (`text-primary`) in gallery examples. | Pass |
| XIII Attribute vocabulary | `variant`, `size`, daisyUI's modifier names as booleans, `placement`, `horizontal`/`vertical` with breakpoints, `label` for an accessible name (the swap's name), merged `class`, the rest through `{{ attrs }}`. The tooltip sends `id` to its content element, a spec-stated exception (FR-018). | Pass |
| XIV Composition | The alert's icon is `<c-icon>` and its dismiss control `<c-button>` (FR-007). Gallery examples compose `<c-alert>`, `<c-button>` and `<c-avatar>`. | Pass |
| XV Gallery annotations | Every template annotated, fixed-value props typed `select[…]`, `cotton_lint --warnings-as-errors` clean. | Pass |

## Design

Shared rules, applied everywhere below (FS-006's and FS-007's, unchanged):

- **Modifiers.** `variant`, `size` and each word of `placement` go through `{% variation … %}` against daisyUI's list (research R1), so an unknown value adds nothing and nothing raises (Edge Cases). A two-word `placement` is split and each word validated, as the dropdown does. The alert's `horizontal` and `vertical` go through `{% responsive … %}`: bare gives the class, a breakpoint gives `<bp>:<class>`, anything else nothing.
- **Root.** Every component declares `class`, merges it into the root's class list, and spreads `{{ attrs }}` on the root (FR-002).
- **Defaults.** Every declared name gets a default, so a page variable of the same name never leaks in (research R6). `=""` everywhere except the alert's `role="alert"` and the progress's `max="100"`. Annotations give no `default:` for empty defaults, and a `select` must not get `default:""`.
- **Named slots.** Declared once in `<c-vars>` and rendered only when non-empty. Each gets a `@prop` and a `@slot:name`.
- **No script.** No `<script>` and no `on*=` attribute in any component's rendered output (SC-003), asserted on the component rendered from a caller string, in one module, `tests/test_feedback_no_script.py`, that each story extends. Alpine's `x-*` and `@click` attributes are not event-handler attributes and pass the check.
- **Translatable names.** Tested as FS-007 tested the carousel's roledescriptions: patch the gettext `{% trans %}` resolves to with a function returning a marked string, assert the marked string, and confirm the test fails against a hard-coded string. No .po/.mo catalog.

### Alert (US1)

`alert.html` — `{% load i18n daisy_cotton %}`, `<c-vars variant="" icon="" soft="" outline="" dash="" horizontal="" vertical="" dismissible="" delay="" role="alert" class="" />`.

```
<div role="{{ role }}" class="alert {% variation variant "alert" "info,success,warning,error" %}{% if soft %} alert-soft{% endif %}{% if outline %} alert-outline{% endif %}{% if dash %} alert-dash{% endif %} {% responsive horizontal "alert-horizontal" %} {% responsive vertical "alert-vertical" %} {{ class }}"{% if dismissible %} x-data="{ show: true }" x-show="show" x-transition{% if delay %} x-init="setTimeout(() => show = false, {{ delay }})"{% endif %}{% endif %} {{ attrs }}>
  {% if icon %}<c-icon name="{{ icon }}" aria-hidden="true" />{% elif variant %}<c-icon name="{{ variant }}" aria-hidden="true" />{% endif %}
  {{ slot }}
  {% if dismissible %}<c-button type="button" ghost size="xs" circle x-on:click="show = false" aria-label="{{ dismiss_label }}"><span aria-hidden="true">✕</span></c-button>{% endif %}
</div>
```

- `role` is declared with the default `alert`, so a caller's `role` replaces it and is never spread a second time through `{{ attrs }}` (FR-010, US1-4).
- `{% trans "Dismiss" as dismiss_label %}` precedes the markup (research R4). The ✕ sits in an `aria-hidden` span inside the button, so the name is the label alone (FR-013).
- `x-on:click` rather than `@click`: both reach the button (research R4), and the long form reads unambiguously as an attribute to anyone reading the template.
- The old template gave `variant` no validation; it now goes through `variation`, so an unknown value emits nothing. The icon fallback still uses `variant` as given, which is the icon extension point working as ADR 0001 describes (Edge Cases).
- The old `class` annotation said the icon gets the classes too. It never did; the new annotation says `class` goes on the alert.
- CHANGELOG `Changed`: `horizontal` and `vertical` added; `role` can be replaced; the dismiss button is now `<c-button>` with a translatable name and a hidden glyph; the icon is hidden from assistive technology; an unknown `variant` emits no class.
- The description warns against `delay` on errors or anything the reader must act on (FR-013, Edge Cases), says `dismissible` and `delay` need Alpine.js, and names the `toast` entry as where an alert with an icon and a dismissible alert are shown.

### Loading (US2)

`loading.html` — `{% load i18n daisy_cotton %}`, `<c-vars spinner="" dots="" ring="" ball="" bars="" infinity="" size="" label="" class="" />`.

```
<span class="loading{% if spinner %} loading-spinner{% endif %}…six in all… {% variation size "loading" "xs,sm,md,lg,xl" %} {{ class }}" role="status" aria-label="{% if label %}{{ label }}{% else %}{% trans "Loading" %}{% endif %}" {{ attrs }}></span>
```

- With no animation given, no style class is emitted and daisyUI draws the spinner (spec Clarifications).
- More than one animation given emits every class, as the alert's styles do; the component does not pick.
- The description names the `mockup.browser` entry as where a loading indicator inside a button is shown.

### Tooltip (US3)

`tooltip.html` — `{% load daisy_cotton %}`, `<c-vars tip="" content="" placement="" variant="" open="" id="" class="" />`.

```
<div class="tooltip {% for word in placement.split %}{% variation word "tooltip" "top,bottom,left,right,start,center,end" %} {% endfor %}{% variation variant "tooltip" "primary,secondary,accent,info,success,warning,error" %}{% if open %} tooltip-open{% endif %} {{ class }}" {{ attrs }}>
  {{ slot }}
  <div class="tooltip-content" role="tooltip"{% if id %} id="{{ id }}"{% endif %}>{% if content %}{{ content }}{% else %}{{ tip }}{% endif %}</div>
</div>
```

- The trigger comes first and the hint after it, so reading order is the control, then its description. daisyUI's CSS needs `tooltip-content` only as a direct child, in any position (research R3).
- No `data-tip` anywhere (FR-016).
- `id` is declared so it never reaches the wrapper through `{{ attrs }}` (FR-018).
- The description and a `{% comment %}` block carry: wrap a focusable trigger or the hint shows on hover only; the tooltip is a description, not a name, so an icon-only trigger still needs `aria-label`; give `id` and put `aria-describedby` with that id on the trigger; Escape does not dismiss it without a project script. It names the `mockup.browser` entry for the linked example.

### Progress and radial progress (US4)

`progress.html` — `{% load daisy_cotton %}`, `<c-vars value="" max="100" variant="" label="" class="" />`.

```
<progress class="progress {% variation variant "progress" "neutral,primary,secondary,accent,info,success,warning,error" %} {{ class }}"{% if value != "" %} value="{{ value }}"{% endif %} max="{{ max }}"{% if label %} aria-label="{{ label }}"{% endif %} {{ attrs }}></progress>
```

- The value test is for emptiness, not truthiness, so `:value="0"` renders `value="0"` rather than an indeterminate bar (research R5). The implementer confirms the comparison against a `None` value too.

`radial_progress.html` — `{% load daisy_cotton %}`, `<c-vars value="" label="" style="" class="" />`.

```
<div class="radial-progress {{ class }}" role="progressbar" style="--value:{{ value }};{% if style %} {{ style }}{% endif %}" aria-valuenow="{{ value }}" aria-valuemin="0" aria-valuemax="100"{% if label %} aria-label="{{ label }}"{% endif %} {{ attrs }}>{% if slot %}{{ slot }}{% elif value != "" %}{{ value }}%{% endif %}</div>
```

- `value` is annotated `required` with `=""` in `<c-vars>`, as the modal's `id` is. The gallery preview therefore shows an empty ring, and the values live in the `mockup.phone` composition (research R7).
- Cotton resolves `<c-radial-progress>` to `radial_progress.html`, the rule FS-007 recorded for `hover_gallery.html`.
- The description states the 0–100 range, that `value` must be a number (research R8), that size and thickness are set with `[--size:…]` and `[--thickness:…]` classes, and that a label should always be given. It names the `mockup.phone` entry.

### Toast (US5)

`toast.html` — `{% load daisy_cotton %}`, `<c-vars placement="" class="" />`.

```
<div class="toast {% for word in placement.split %}{% variation word "toast" "top,middle,bottom,start,center,end" %} {% endfor %}{{ class }}" {{ attrs }}>{{ slot }}</div>
```

- No `role` and no `aria-live` (FR-022). With no placement, daisyUI's default is bottom end.
- `@slot` holds three `<c-alert>`s: an info alert with an icon, a success alert with `role="status"`, and a dismissible warning.
- The `{% comment %}` block and the README show a project rendering its messages: `{% for message in messages %}<c-alert variant="{{ message.level_tag }}" dismissible>{{ message }}</c-alert>{% endfor %}` inside `<c-toast>`, noting that Django's `debug` level tag has no alert colour and falls back to the plain alert.

### Skeleton (US6)

`skeleton.html` — `<c-vars text="" class="" />`.

```
<div class="skeleton{% if text %} skeleton-text{% endif %} {{ class }}"{% if not text %} aria-hidden="true"{% endif %} {{ attrs }}>{% if text and text is not True %}{{ text }}{% else %}{{ slot }}{% endif %}</div>
```

- Bare `text` arrives as `True` and leaves the slot as content. A string is the content (FR-025).
- The description names the `mockup.phone` entry for the composed card placeholder.

### Gallery entries (FR-004, FR-005)

Every template carries `@description`, a `@prop` per `<c-vars>` name and `@slot` / `@slot:name` per slot, in FS-002's order. Fixed-value props are `select[…]` with daisyUI's full list. `placement` lists every single word and every two-word combination, as the dropdown's annotation does. `horizontal`/`vertical` are `select['sm','md','lg','xl','2xl']` with the bare-attribute description, as FS-006's stat group. One-line examples must not contain `#}` or a spaced em dash before the description separator.

| Entry | Default slot / named slots |
|---|---|
| alert | A one-line message. |
| loading | No slot. |
| tooltip | `@slot` an icon-only `<c-button circle icon aria-label>`; `@slot:content` a short hint with a `<kbd>` shortcut, the rich-content case (US3-6). `tip` is typed by the developer in the props panel. |
| progress | No slot. |
| radial-progress | `@slot` custom centre content, such as an icon or a short word (US4-6). |
| toast | Three alerts (see Toast above). |
| skeleton | `@slot` a line of text, shown when `text` is set. |

**Compositions (research R7).** Each goes where an application would write it, and the component's `@description` names the entry that shows it:

| Host entry | Composition | Scenarios |
|---|---|---|
| `mockup.browser` default slot | Added to the product page: a toolbar with an icon-only share `<c-button aria-label aria-describedby="product-share-hint">` inside `<c-tooltip id="product-share-hint" tip>` (US3-8), and an "Add to cart" `<c-button>` holding `<c-loading size="sm" />` (US2-6). | US2-6, US3-8 |
| `mockup.phone` default slot | A mobile upload screen: `<c-progress label>` bars at several values and colours plus one indeterminate (US4-8); three `<c-radial-progress label>`s at different values, one with `[--size:…] [--thickness:…]`, one `text-primary`, one with custom centre content (US4-8); and a card placeholder of `<c-skeleton>` shapes for an image and an avatar and two text-line skeletons (US6-4). | US4-8, US6-4 |

Every icon-only control has an `aria-label`, every loading, progress and radial progress a name, and colours come from the semantic palette only (SC-004).

### Documentation

- `README.md`: the component count goes from Sixty-three to Sixty-nine and the list gains each new component in its story. The Alpine paragraph is rewritten in US1 to describe the alert as it now is. US5 adds the toast-with-messages example.
- `CHANGELOG.md` `[Unreleased]`: `Added` per new component, each naming its attributes and slots; `Changed` for the alert (US1).

## Project Structure

### Documentation (this feature)

```text
specs/008-feedback-components/
├── spec.md, decisions.md      # on main
├── plan.md, research.md, tasks.md, progress.md, feature-state.json
```

### Source Code

```text
daisy_cotton/templates/cotton/
├── alert.html                                # rewritten (US1)
├── loading.html                              # new (US2)
├── tooltip.html                              # new (US3)
├── progress.html, radial_progress.html       # new (US4)
├── toast.html                                # new (US5)
├── skeleton.html                             # new (US6)
├── mockup/browser.html, mockup/phone.html    # annotations only
tests/
├── test_alert.py, test_loading.py, test_tooltip.py, test_progress.py,
│   test_radial_progress.py, test_toast.py, test_skeleton.py            # new
└── test_feedback_no_script.py                                         # new, extended per story
pyproject.toml                # new test modules in non-mirror-paths
README.md, CHANGELOG.md
```

**Structure Decision**: single-file components throughout. None has a part that a caller places separately: the tooltip's content and the alert's dismiss button are emitted by the component itself.

## Story order

One worktree, stories one after another: they share `README.md`, `CHANGELOG.md`, `pyproject.toml`, the no-script module and the host entries' annotations.

1. Batch 1: US1 alert, US2 loading, US3 tooltip.
2. Batch 2: US4 progress and radial progress, US5 toast (after US1, whose alert it holds), US6 skeleton.

## Complexity Tracking

| Addition | Why | Simpler alternative rejected because |
|---|---|---|
| Compositions in two host entries | US2-6, US3-8, US4-8 and US6-4 need several instances or markup beside the component, and the gallery shows one preview per entry (research R7) | A demo page of its own is ruled out by FS-001 FR-001. |
