# daisy-cotton

[![Tests](https://github.com/django-mvp/daisy-cotton/actions/workflows/tests.yml/badge.svg)](https://github.com/django-mvp/daisy-cotton/actions/workflows/tests.yml) [![Coverage](https://codecov.io/gh/django-mvp/daisy-cotton/branch/main/graph/badge.svg)](https://codecov.io/gh/django-mvp/daisy-cotton) ![Python 3.12 | 3.13](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue) ![Django 5.2 | 6.0 | 6.1](https://img.shields.io/badge/django-5.2%20%7C%206.0%20%7C%206.1-blue) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/django-mvp/daisy-cotton/blob/main/LICENSE)

Base daisyUI-styled django-cotton components: buttons, inputs, cards, alerts and the rest of an application's furniture

Built on [daisyUI](https://daisyui.com/) and [django-cotton](https://django-cotton.com/). A project that wants daisyUI-styled Cotton components depends on this package directly: install it, add it to `INSTALLED_APPS`, and each `<c-name>` tag is ready to use. It carries no settings, no menus, no icon registry and no views of its own — see [Scope & philosophy](https://github.com/django-mvp/daisy-cotton#scope--philosophy).

## Status

Pre-1.0: names, attributes and the set of classes a component emits can change between minor versions. The [CHANGELOG](https://github.com/django-mvp/daisy-cotton/blob/main/CHANGELOG.md) is how a project finds out what has landed.

Eighty-two components are built so far: `accordion`, `alert`, `avatar`, `badge`, `breadcrumbs`, `button`, `card`, `carousel`, `chat`, `collapse`, `countdown`, `diff`, `divider`, `dock`, `drawer`, `dropdown`, `fab`, `footer`, `form.calendar`, `form.checkbox`, `form.fieldset`, `form.file-input`, `form.filter`, `form.input`, `form.label`, `form.otp`, `form.radio`, `form.range`, `form.rating`, `form.select`, `form.textarea`, `form.toggle`, `hero`, `hover-3d`, `hover-gallery`, `icon`, `indicator`, `join`, `kbd`, `link`, `list`, `loading`, `mask`, `megamenu`, `menu`, `modal`, `navbar`, `progress`, `radial-progress`, `skeleton`, `stack`, `stat`, `status`, `steps`, `swap`, `table`, `tabs`, `text-rotate`, `timeline`, `toast`, `tooltip` and `mockup.*`. Pagination has no component: daisyUI builds it from `join` and `btn` and gives it no class of its own, so write it with those two. Aura has no component either: it only decorates another element, so wrap the component to highlight in a `<div class="aura">` with daisyUI's style and size classes. Each one is documented live in the component gallery (`python manage.py runserver` from a checkout). More land as the need arises.

`<c-icon>` renders `name` as a literal CSS class string and resolves nothing itself — a project wanting name-based icon resolution provides its own override (see [docs/adr/0001](https://github.com/django-mvp/daisy-cotton/blob/main/docs/adr/0001-icon-is-an-extension-point.md)).

`<c-alert>` takes `variant` (info, success, warning, error), `soft`/`outline`/`dash` for style, and `horizontal`/`vertical` for direction, each accepting a breakpoint such as `sm`; a caller-given `role` replaces the default `role="alert"`, so `role="status"` gives a polite announcement instead of an interruption. Its icon and dismiss button are drawn by `<c-icon>` and `<c-button>`; the dismiss button's accessible name is the translatable "Dismiss" with its glyph hidden from assistive technology. `dismissible` and `delay` need [Alpine.js](https://alpinejs.dev/) on the page — this package doesn't ship or load it. Without Alpine, the alert still renders and reads fine, but the dismiss button does nothing and `delay` never fires.

`<c-toast>` pins its content to a corner or edge of the screen and has no role or live region of its own, so put alerts inside it and each keeps its own. A project rendering Django's messages framework writes:

```django
<c-toast placement="top end">
  {% for message in messages %}
    <c-alert variant="{{ message.level_tag }}" dismissible>{{ message }}</c-alert>
  {% endfor %}
</c-toast>
```

Django's `debug` level tag has no matching alert colour, so a debug message falls back to the plain alert.

## Requirements

- Python 3.12+
- Django 5.2, 6.0 or 6.1
- django-cotton 2.6+
- daisyUI 5, loaded by the project

daisyUI is a hard requirement and this package does not ship it. Any project already running daisyUI satisfies it, through whatever Tailwind build the project already has.

## Install

```bash
pip install daisy-cotton
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "django_cotton",
    "daisy_cotton",
]
```

## Usage

Each component is a Cotton tag named after its daisyUI component, configured through attributes that use daisyUI's own modifier names:

```html
<c-card title="Storage" border>
  Almost full.
  <c-slot name="actions">
    <c-button variant="primary" size="sm" text="Upgrade" />
  </c-slot>
</c-card>
```

Classes passed with `class` are added to the component's own, and any other attribute passes through to its root element.

## Calendar

`<c-form.calendar>` writes Cally's `<calendar-date>` element, or `<calendar-range>` with `range`, carrying daisyUI's `cally` class. It shows nothing until the project loads Cally, and this package does not. Add the module script to the page's head, pinning the version you have tested or hosting the file yourself:

```html
<script type="module" src="https://unpkg.com/cally@0.9.2"></script>
```

Cally's own attributes (`value`, `min`, `max`, `locale`, `first-day-of-week`) go on the tag and reach the calendar unchanged, `months="2"` shows two months side by side, and `class` is added to the calendar's own. The previous and next buttons hold an icon drawn by `<c-icon>` and a visually hidden name, so pass icon classes through `previous_icon` and `next_icon` unless your project's `<c-icon>` resolves names:

```html
<c-form.calendar id="delivery-calendar" min="2026-09-01" previous_icon="bi bi-chevron-left" next_icon="bi bi-chevron-right" />
<input type="hidden" name="delivery_date" id="delivery-date">
```

Cally does not write to a form itself. Its `change` event carries the chosen date in the calendar's `value`, so a few lines of script copy it into the hidden input:

```html
<script>
  document.getElementById("delivery-calendar").addEventListener("change", (event) => {
    document.getElementById("delivery-date").value = event.target.value;
  });
</script>
```

For a range the same `value` is the two dates joined with a slash, such as `2026-09-01/2026-09-07`.

## Scope & philosophy

**What this is.** One Cotton component for each base daisyUI component, and nothing else. A component that daisyUI builds out of other components, or a class that only modifies another component, gets no Cotton component of its own. The validator is one such class: add it to a control through its `class`, or to the OTP's input through `input_class`. Everything here is presentation: templates configured through attributes and themed by whatever daisyUI theme the project runs.

**What this deliberately is not.**

- **Not an application shell.** No settings, no menu system, no icon registry, no views.
- **Not page-level layout.** The `hero` container ships, but composed hero sections (the heading, copy and calls to action inside it) and other page sections stay with the project, built from these components.
- **Not a CSS framework.** daisyUI, its themes and Tailwind's preflight come from the project.
- **Not a JavaScript layer.** The package ships no scripts. A project that wants behaviour daisyUI's CSS doesn't give, such as smarter dropdown placement, adds it by overriding the component. The calendar is the one component that needs a script to show anything: it is drawn by [Cally](https://github.com/WickyNilliams/cally), which the project loads itself (see [Calendar](#calendar)).
- **Not coupled to Django objects.** Components take plain values. Wiring one up to a form, a paginator or the messages framework is the project's job.
- **Not shaped for any particular project.** Nothing here exists because one adopter needed it.

**Tie-breaks.** When two of these pull against each other:

1. Following daisyUI beats convenience. A component's attributes use daisyUI's own names for its modifiers rather than a friendlier parallel vocabulary.
2. Leaving it to the project beats doing it here. If only some adopters need it, they get it by overriding the component.
3. Fewer attributes beat more. Anything a component doesn't need to decide passes straight through to the markup.

## Prior art

[labbhq/labb](https://github.com/labbhq/labb) is an actively maintained django-cotton + daisyUI 5 component library covering similar ground. It is a batteries-included framework — its own CLI, reactivity layer, icon system and project scaffolder — rather than a thin base layer, and daisy-cotton's purpose here is narrower: a dependency-free set of base primitives a project drops in alongside its own choices. See [docs/brainstorm.md](https://github.com/django-mvp/daisy-cotton/blob/main/docs/brainstorm.md) for the fuller reasoning.

## Contributing

To set up a checkout, open the component gallery, run the checks or add a component, see [CONTRIBUTING](https://github.com/django-mvp/daisy-cotton/blob/main/CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](https://github.com/django-mvp/daisy-cotton/blob/main/CHANGELOG.md).

## License

MIT. See [LICENSE](https://github.com/django-mvp/daisy-cotton/blob/main/LICENSE).
