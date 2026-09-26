# Brainstorm

Working notes from framing this package. Not ratified decisions — see `docs/adr/` for those, and `README.md` for the settled scope.

## Why this package exists

A project that wants daisyUI-styled Cotton components (buttons, inputs, cards, alerts, and similar) without adopting a full application shell — settings, menus, icons, views — has nowhere to get just those.

`daisy-cotton` is that base layer: a dependency-free set of Cotton primitives styled with daisyUI, installable on its own. A page-level layout package (heroes, sections, calls to action) can compose on top of it without depending on anything heavier.

This repository started as an empty scaffold with a passing test suite and green CI, then filled in with its first components.

## Prior-art research (2026-09-23)

Searched for existing standalone django-cotton + daisyUI component libraries before scaffolding.

**labbhq/labb** — the real overlap. Actively maintained (140 stars, commits through the week of research, alpha release v0.5.0), MIT-licensed, org-owned. It is a full framework rather than a bare component layer: a bundled reactivity layer (Datastar, ships JS), its own icon subsystem, a CLI (`labb dev`, `labb init`, component inspection), and a project scaffolder (`labbstart`). It markets itself as an opinionated batteries-included stack, not a dependency-free base a project drops in alongside its own choices.

**snopoke/cotton-daisyui ("Astral UI")** — dead. No commits in ~22 months, 3 stars, no tagged releases, README marked "a work in progress" with unfinished setup steps. Not a real obstacle.

**cotton-daisy (PyPI/Qwizi)** and **django-cotton-components (PyPI)** — different tools, not competitors. The former is a CLI code-generator that scaffolds component files into a consuming project rather than shipping an installable library; the latter is an Alpine.js-based form component pack with no daisyUI styling.

**Why proceeding despite labb's overlap is justified:** this isn't a search for a generic solution to "daisyUI components for django-cotton" — it's building components that need to work exactly one specific way and keep working that way. Depending on labb instead would mean building every component against a different framework (different reactivity model, different icon system, different CLI) for no functional gain. The honest motivation, in Sam's words: control over a piece this central, rather than waiting on someone else's release cadence for it.
