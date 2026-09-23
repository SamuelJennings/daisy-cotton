# Brainstorm

Working notes from framing this package. Not ratified decisions — see `docs/adr/` for those, and `README.md` for the settled scope.

## Why this package exists

django-mvp's component library currently bundles its daisyUI-styled Cotton components (buttons, inputs, cards, alerts, and similar) together with the rest of its application shell — settings, menus, icons, views. Anything that wants only the components has to adopt the whole shell to get them.

`daisy-cotton` is where those components move to, decoupled from django-mvp. `daisy-cotton-blocks` (page-level layouts: heroes, sections, calls to action) already exists as a sibling package built the same way — pulled out so it works on any django-cotton + daisyUI project rather than depending on django-mvp. `daisy-cotton` is the base layer underneath it: block-level layouts compose the primitives this package will ship.

Migrating the actual components out of django-mvp happens later, as its own piece of work once the first one is needed. This repository starts as an empty scaffold with a passing test suite and green CI, nothing more.

## Prior-art research (2026-09-23)

Searched for existing standalone django-cotton + daisyUI component libraries before scaffolding.

**labbhq/labb** — the real overlap. Actively maintained (140 stars, commits through the week of research, alpha release v0.5.0), MIT-licensed, org-owned. It is a full framework rather than a bare component layer: a bundled reactivity layer (Datastar, ships JS), its own icon subsystem, a CLI (`labb dev`, `labb init`, component inspection), and a project scaffolder (`labbstart`). It markets itself as an opinionated batteries-included stack, not a dependency-free base a project drops in alongside its own choices.

**snopoke/cotton-daisyui ("Astral UI")** — dead. No commits in ~22 months, 3 stars, no tagged releases, README marked "a work in progress" with unfinished setup steps. Not a real obstacle.

**cotton-daisy (PyPI/Qwizi)** and **django-cotton-components (PyPI)** — different tools, not competitors. The former is a CLI code-generator that scaffolds component files into a consuming project rather than shipping an installable library; the latter is an Alpine.js-based form component pack with no daisyUI styling.

**Why proceeding despite labb's overlap is justified:** this isn't a search for a generic solution to "daisyUI components for django-cotton" — it's extracting code that already exists, is already proven inside django-mvp and its downstream packages, and needs to keep working exactly as it does today. Depending on labb instead would mean rewriting every consuming component against a different framework (different reactivity model, different icon system, different CLI) for no functional gain, and would still leave django-mvp's own components needing a home. The honest motivation, in Sam's words: control over packages this family depends on, rather than waiting on someone else's release cadence for a piece this central.
