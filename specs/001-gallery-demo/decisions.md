# Decisions for 001-gallery-demo

Ambiguities resolved while writing the specification. Each one is also recorded under Clarifications in `spec.md`.

## The folder-component 404 is a gallery defect, and gets no local workaround

Reproduced on main with the demo's own settings: every sidebar link returns 200 except `avatar`, `breadcrumbs`, `card`, `dock`, `dropdown` and `mockup/code`, which return 404. The gallery's catalog scanner treats `<dir>/index.html` as a component named `<dir>`. Its path resolver (`core/catalog/resolver.py` in django-cotton-gallery 1.0.0, unchanged on its main branch) builds only `<dir>.html` and raises "not found" when that file is missing. `/django-cotton-gallery/card/index/` works because the resolver then finds `card/index.html` directly. No setting in this repository touches either code path.

Two local fixes were available and both were rejected:

- Flattening `card/index.html` to `card.html`, and likewise for the others, reshapes the package's template layout around a bug in a development tool. `dock` and `breadcrumbs` would end up split across a file and a folder.
- Overriding the gallery's sidebar or detail view in the demo forks the gallery's code for a defect that is a few lines from being fixed at its source.

Instead the test covers every link, skips the folder cases with a reason naming the tracking issue filed in this repository, and the dev dependency's minimum is raised once a fixed release exists. Skipped rather than expected-failure, so a later reader can see why without decoding pytest's xfail semantics.

## Alpine in the demo

The issue asks for a "bare Cotton and daisyUI page" and also for the docs to say `alert`'s dismiss button needs Alpine. A demo without Alpine would show a dismiss button that does nothing, in a gallery whose job is showing how components behave. Alpine isn't a host package, and loading it is what any project using `dismissible` must do anyway. The package still ships no JavaScript.

## What counts as naming a host or consumer

`django-mvp/shared` and its `mvp-shared` bundle provide CI workflows, pre-commit configuration and the dev toolchain. They are tooling sources, not hosts or consumers, and replacing them is a separate concern. References to them stay. Everything else naming django-mvp or daisy-cotton-blocks goes, including CHANGELOG provenance ("migrated from django-mvp"), since nothing has been released and the Unreleased section describes what the package ships.

django-easy-icons stays in ADR 0001 as an example of an override a project might install. It illustrates the extension point and doesn't claim to host or consume the package.

## Demo and tests are in scope too

The issue lists six documents. Article XII names the demo, the tests and the dependency list as well, and the test settings currently import django-mvp's configuration from the demo settings, so dropping the dependency forces the change anyway.

## Themes

The switcher keeps the demo's current ten themes. That list was chosen to cover light, dark and heavily tinted palettes, and nothing in the issue asks for a different set.

## D1 Preview assets come from the gallery's head partial, scoped to previews

The gallery's URL-list settings load assets into its own interface page as well as the previews, and daisyUI's base styles would restyle the gallery's chrome. The demo supplies `django_cotton_gallery/_extra_head.html`, whose script loads daisyUI, Tailwind's browser build and Alpine only into preview documents.

**ADR:** none — a demo configuration detail, nothing in the package inherits it

## D2 FR-009 tracks the gallery defect in this repository

The merged specification's FR-009 still said the defect would be reported to django-cotton-gallery. The maintainer's rule is that implementation files issues here and he decides what goes upstream, and the rest of the spec was already corrected to say so. FR-009 is amended to match in this branch.

**ADR:** none — a process rule, recorded in the workspace, not an architectural decision

## D3 Design review outcome

One verified high finding and three lower ones, all applied as plan edits: the theme switcher's partial is copied into every preview frame, so it holds only a script that builds the control in the interface page (T006, research). T002 asserts only what the server renders and leaves the browser behaviours to the walkthrough. T009 fails on an empty link collection. The two new test modules are declared as non-mirror tests (T007).

**ADR:** none — plan-level corrections local to this feature

## D4 daisyUI loads as stylesheets, and the theme switcher is pinned in place

At story acceptance the head partial loaded daisyUI's CDN files through `<script>` tags. jsDelivr serves them as `text/css` with `nosniff`, so browsers refused them and previews rendered without daisyUI, and `themes.js` does not exist. The test only checked that the URLs appeared, so it passed. Fixed directly as a two-line change: `<link rel="stylesheet">` for `daisyui@5` and `daisyui@5/themes.css`, with a test that fails on the script form. The theme `<select>` also carried daisyUI classes on a page without daisyUI and was appended to the end of the body, so it is now placed with inline styles in the top-right corner. Fixed directly rather than dispatched because both are single-line corrections with no design content.

**ADR:** none — a demo configuration correction
