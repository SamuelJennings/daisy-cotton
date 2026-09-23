# daisy-cotton

Base [daisyUI](https://daisyui.com/)-styled components for [django-cotton](https://django-cotton.com/) — buttons, inputs, cards, alerts, badges, modals and the rest of an application's furniture.

These components currently live inside [django-mvp](https://github.com/django-mvp/django-mvp), bundled with its application shell. This package is where they are moving to, so a project that only wants daisyUI-styled Cotton components can depend on them directly, without adopting django-mvp's settings, menus, icons or views. [daisy-cotton-blocks](https://github.com/django-mvp/daisy-cotton-blocks), which builds page-level layouts such as heroes and sections, composes on top of this package rather than on django-mvp for the same reason.

## Status

Version 0.0.1. This is the scaffold: build pipeline, demo project and test harness, no components migrated in yet. The [CHANGELOG](CHANGELOG.md) is how a project finds out what has landed.

## Requirements

- Python 3.12+
- Django 5.2 or 6.0
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

**What this is.** A presentation-only component library. Templates and the small amount of JavaScript a component needs. Components are configured through attributes and themed by whatever daisyUI theme the project runs, so they never pin a literal colour into the markup.

**What this deliberately is not.**

- **Not an application shell.** No settings-driven configuration, no menu system, no icon registry, no class-based views. Those stay in django-mvp.
- **Not page-level layout.** Heroes, sections and other block-level compositions are [daisy-cotton-blocks](https://github.com/django-mvp/daisy-cotton-blocks)' job. This package owns the primitives those blocks are built from.
- **Not a CSS framework.** No daisyUI plugin, no theme layer, no preflight. Those come from the project.
- **Not tied to django-mvp.** django-mvp is a demo/development dependency of this repository, never a runtime dependency of the package. Any django-cotton + daisyUI project can use these components standalone.

**Tie-breaks.** When two of these pull against each other: theme-driven beats hard-coded, and a component that composes existing daisyUI markup beats one that invents its own.

## Prior art

[labbhq/labb](https://github.com/labbhq/labb) is an actively maintained django-cotton + daisyUI 5 component library covering similar ground. It is a batteries-included framework — its own CLI, reactivity layer, icon system and project scaffolder — rather than a thin base layer, and daisy-cotton's purpose here is narrower: extracting components already written and shipped inside django-mvp so other packages in this family can depend on them directly. See [docs/brainstorm.md](docs/brainstorm.md) for the fuller reasoning.

## License

MIT
