# daisy-cotton

Base [daisyUI](https://daisyui.com/)-styled components for [django-cotton](https://django-cotton.com/) — buttons, inputs, cards, alerts, badges, modals and the rest of an application's furniture.

These components currently live inside [django-mvp](https://github.com/django-mvp/django-mvp), bundled with its application shell. This package is where they are moving to, so a project that only wants daisyUI-styled Cotton components can depend on them directly, without adopting django-mvp's settings, menus, icons or views. [daisy-cotton-blocks](https://github.com/django-mvp/daisy-cotton-blocks), which builds page-level layouts such as heroes and sections, composes on top of this package rather than on django-mvp for the same reason.

## Status

Version 0.0.1, pre-1.0: names, attributes and the set of classes a component emits can change between minor versions. The [CHANGELOG](CHANGELOG.md) is how a project finds out what has landed.

Thirty components are built so far — the base primitives most projects reach for first: `alert`, `avatar`, `badge`, `breadcrumbs`, `button`, `card`, `container`, `divider`, `dock`, `dropdown`, `form.field`, `grid`, `group`, `icon`, `link`, `modal`, `mockup.*`, `placeholder.card`, `rule`, `text` and `toolbar`. Each one is documented live in the component gallery (`python manage.py runserver` from a checkout). More migrate in from django-mvp as the need arises.

`<c-icon>` renders `name` as a literal CSS class string and resolves nothing itself — a project wanting name-based icon resolution provides its own override (see [docs/adr/0001](docs/adr/0001-icon-is-an-extension-point.md)).

## Requirements

- Python 3.12+
- Django 5.2, 6.0 or 6.1
- django-cotton 2.6+
- daisyUI 5, loaded by the project

daisyUI is a hard requirement and this package does not ship it. Any project already running daisyUI satisfies it, whether through its own Tailwind build or through a package that provides one, such as django-mvp.

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

## Scope & philosophy

**What this is.** One Cotton component for each base daisyUI component, and nothing else. A component that daisyUI builds out of other components, or a class that only modifies another component, gets no Cotton component of its own. Everything here is presentation: templates configured through attributes and themed by whatever daisyUI theme the project runs.

**What this deliberately is not.**

- **Not an application shell.** No settings, no menu system, no icon registry, no views.
- **Not page-level layout.** Heroes, sections and other compositions are built from these components, not shipped with them.
- **Not a CSS framework.** daisyUI, its themes and Tailwind's preflight come from the project.
- **Not a JavaScript layer.** The package ships no scripts. A project that wants behaviour daisyUI's CSS doesn't give, such as smarter dropdown placement, adds it by overriding the component.
- **Not coupled to Django objects.** Components take plain values. Wiring one up to a form, a paginator or the messages framework is the project's job.
- **Not shaped for any particular project.** Nothing here exists because one adopter needed it.

**Tie-breaks.** When two of these pull against each other:

1. Following daisyUI beats convenience. A component's attributes use daisyUI's own names for its modifiers rather than a friendlier parallel vocabulary.
2. Leaving it to the project beats doing it here. If only some adopters need it, they get it by overriding the component.
3. Fewer attributes beat more. Anything a component doesn't need to decide passes straight through to the markup.

## Prior art

[labbhq/labb](https://github.com/labbhq/labb) is an actively maintained django-cotton + daisyUI 5 component library covering similar ground. It is a batteries-included framework — its own CLI, reactivity layer, icon system and project scaffolder — rather than a thin base layer, and daisy-cotton's purpose here is narrower: extracting components already written and shipped inside django-mvp so other packages in this family can depend on them directly. See [docs/brainstorm.md](docs/brainstorm.md) for the fuller reasoning.

## License

MIT
