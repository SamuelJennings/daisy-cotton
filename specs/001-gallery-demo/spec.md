# Feature Specification: Make the component gallery the whole demo

**Feature Branch**: `001-gallery-demo`

**Created**: 2026-09-26

**Status**: Draft

**Serves**: G1, G2 (see [GOALS.md](../../GOALS.md)) · Roadmap: R1

**Input**: Issue #10: "The demo project should be the component gallery and nothing else: a bare Cotton and daisyUI page with a theme switcher, with no other host package behind it. Every link in the gallery sidebar should open its component. Today the ones whose template is a folder, like `card` and `dock`, return 404. The README, CONTEXT, contributor notes, ADR 0001 and changelog should describe this package without naming another project as its host or consumer, and the docs should say that `alert`'s dismiss button needs Alpine on the page."

## Scope

The demo project becomes the component gallery and nothing else, running on a plain Cotton and daisyUI page with a theme switcher and no other package behind it. The repository's own documents describe the package on its own terms.

Issue #11 owns the gallery annotations on each component, the linter in the test suite, and the contributor docs on running the gallery and the linter. New components are out of scope, as are gallery features the gallery package doesn't already provide.

## Clarifications

### Session 2026-09-26

- Q: Why do the sidebar links for `card`, `dock` and the other folder components return 404: this repository's configuration, or the gallery? → A: The gallery. django-cotton-gallery 1.0.0, the latest release, lists `card/index.html` under the name `card` and links to `/django-cotton-gallery/card/`, but the page behind that link looks only for `card.html` and never falls back to `card/index.html` the way Cotton does. The defect is still on the gallery's main branch, and no setting here changes either side. Six links are affected today: `avatar`, `breadcrumbs`, `card`, `dock`, `dropdown` and `mockup/code`.
- Q: What does this repository do about those six links? → A: It doesn't work around the defect. Moving templates out of their folders would reshape the package to suit a development tool. A test checks that every sidebar link opens its component, and for folder components that test is skipped with a reason naming the upstream issue. The implementation files that issue with django-cotton-gallery. When a gallery release carries the fix, the dev dependency's minimum goes up and the skip comes out.
- Q: Does "a bare Cotton and daisyUI page" rule out Alpine in the demo? → A: No. Alpine is a script, not a host package. The demo loads it so `alert`'s dismiss button works in the gallery, which is exactly what a project using the component does. The package itself still ships no JavaScript.
- Q: Which themes does the switcher offer? → A: The ten the demo offers today: light, dark, cupcake, emerald, corporate, synthwave, dracula, business, night and winter. Between them they cover light, dark and heavily tinted palettes.
- Q: Does "name no other project as its host or consumer" cover the shared CI and toolchain repository, `django-mvp/shared`? → A: No. It supplies the CI workflows, the pre-commit configuration and the development toolchain. It neither hosts nor consumes this package, so references to it stay.
- Q: Does the CHANGELOG keep "migrated from django-mvp" as provenance for the first components? → A: No. Nothing has been released, so the Unreleased section describes what the package ships. Where a component came from tells a reader of this package nothing. Comparisons with another package's version of a component are restated as plain facts about this one.
- Q: The issue lists six documents. Do the demo and the tests also stop naming django-mvp? → A: Yes. Constitution Article XII covers the demo, the tests and the dependency list, and the test settings can't import django-mvp's configuration once it isn't installed. Sample text in a test (a `pip install django-mvp` code line) becomes a neutral command.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The demo is the gallery on a bare Cotton and daisyUI page (Priority: P1)

A contributor starts the demo and lands in the component gallery. There is no home page and no application shell. Components render with daisyUI styling, and a theme switcher changes the theme of every component preview. The demo installs Django, Cotton, the gallery and the development toolchain and nothing more, so what's on the page is this package's components alone.

**Why this priority**: Every later roadmap item adds components and has to look at them. Today the demo leans on another package's shell to supply daisyUI, which Article XII rules out. The other stories assume this one.

**Independent Test**: Install the dev dependencies, start the demo, open its root URL, browse to a component and switch the theme. Confirm django-mvp isn't in the installed dependency tree and the test suite passes.

**Acceptance Scenarios**:

1. **Given** a fresh checkout with its dev dependencies installed, **When** a contributor opens the demo's root URL, **Then** they reach the component gallery, and no separate home page exists.
2. **Given** the gallery is open on any component, **When** the contributor picks a different theme from the switcher, **Then** the preview re-renders in that theme's semantic palette.
3. **Given** a theme was picked on one gallery page, **When** the contributor opens another component, **Then** the preview uses the same theme.
4. **Given** the dev dependencies are installed, **When** the dependency tree is listed, **Then** it contains no django-mvp and nothing that arrived only as a dependency of it.
5. **Given** django-mvp isn't installed, **When** the test suite runs, **Then** it passes.
6. **Given** the gallery is open on `alert` with `dismissible` set, **When** the contributor clicks the dismiss button, **Then** the alert disappears.

---

### User Story 2 - Every sidebar link opens its component (Priority: P2)

Every link in the gallery sidebar opens its component's page, including components whose template is a folder (`avatar`, `breadcrumbs`, `card`, `dock`, `dropdown`, `mockup.code`). The cause is a defect in the gallery package, so this repository reports it upstream and records exactly which links wait on the fix, rather than reshaping its templates around it.

**Why this priority**: A broken link hides a component from the gallery, which works against G2. Stories 1 and 3 still deliver their value before the upstream fix ships.

**Independent Test**: Run the sidebar-link test. It opens every link the sidebar renders: flat components pass, and each folder component either passes (once a fixed gallery release is installed) or is skipped with a reason naming the upstream issue.

**Acceptance Scenarios**:

1. **Given** the gallery sidebar, **When** the test opens every component link in it, **Then** each link to a single-file component returns that component's page.
2. **Given** the installed gallery release still has the index-file defect, **When** the test reaches a folder component, **Then** that case is skipped and the skip reason names the upstream issue.
3. **Given** a gallery release that fixes the defect, **When** the dev dependency's minimum is raised to it and the skip removed, **Then** every sidebar link returns its component's page.
4. **Given** a folder component added later, **When** the test runs, **Then** its link is covered without editing the test.

---

### User Story 3 - The repository describes the package on its own terms (Priority: P2)

Someone reading the README, CONTEXT.md, AGENTS.md, `docs/brainstorm.md`, ADR 0001 or the CHANGELOG learns what daisy-cotton is and does without being told another project hosts it or depends on it. The demo, the tests and the dependency list don't name one either.

**Why this priority**: Article XII requires it, and the README, the first thing an adopter reads, currently presents the package as a piece moving out of another project.

**Independent Test**: Search the six documents, `demo/`, `tests/` and `pyproject.toml` for `django-mvp`, `mvp` and `daisy-cotton-blocks`. The only matches left point at the shared CI and toolchain repository and its `mvp-shared` bundle.

**Acceptance Scenarios**:

1. **Given** the README, **When** an adopter reads it, **Then** it states what the package provides and requires (Django, Cotton, and daisyUI loaded by the project) and names no other project as a host, a source or a consumer.
2. **Given** CONTEXT.md, **When** a contributor reads the Component, Block, Demo and "Component library" entries, **Then** each defines its term without naming another package, and the Demo entry describes the gallery-only demo.
3. **Given** ADR 0001, **When** it is read, **Then** its decision and reasoning stand without comparison to another package's icon handling, and django-easy-icons appears only as an example of an override a project might install.
4. **Given** the CHANGELOG's Unreleased section, **When** it is read, **Then** it lists what the package ships, with no "migrated from" provenance and no comparison to another package's version of a component.
5. **Given** `docs/brainstorm.md`, **When** it is read, **Then** the prior-art survey and the case for building the package survive, restated without naming another project as host or consumer.

---

### User Story 4 - The docs say `alert`'s dismiss button needs Alpine (Priority: P3)

An adopter setting `dismissible` on `alert` learns from the README that the dismiss button, and the `delay` auto-dismiss, only work with Alpine.js on the page, and that daisy-cotton doesn't load it.

**Why this priority**: Without Alpine the alert still renders and reads fine. Only the button does nothing, so the gap costs confusion rather than breakage.

**Independent Test**: Read the README's component notes and find the Alpine requirement next to `alert`.

**Acceptance Scenarios**:

1. **Given** the README, **When** an adopter looks up `alert`, **Then** it says `dismissible` and `delay` need Alpine.js on the page, the package doesn't ship it, and without it the alert renders but can't be dismissed.

### Edge Cases

- A component has both `name.html` and `name/index.html`: the gallery lists `name.html`, following Cotton's resolution order, and the link works. No such component exists today.
- A folder component nested in a category (`mockup/code/index.html`) has the same defect and falls under the same test and skip.
- A URL the demo doesn't serve returns Django's default error page. The demo supplies no custom error pages.
- No theme has been picked yet: the preview uses the default theme, light.
- JavaScript is off in the browser: the gallery's interactive panels, the theme switcher and alert dismissal stop working. Acceptable for a development tool.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The demo project MUST serve the component gallery at its root URL and MUST serve no other page of its own. *(US1)*
- **FR-002**: The demo MUST render component previews with Cotton and daisyUI styles, with no other host package installed or configured. *(US1)*
- **FR-003**: The demo MUST offer a theme switcher covering light, dark, cupcake, emerald, corporate, synthwave, dracula, business, night and winter. The chosen theme MUST apply to every component preview and persist across gallery pages in the same browser. *(US1)*
- **FR-004**: django-mvp MUST be removed from the development dependencies and the lockfile, together with every package present only because django-mvp required it. *(US1)*
- **FR-005**: The test suite and its settings MUST run and pass without django-mvp installed. *(US1)*
- **FR-006**: The demo MUST load Alpine.js on the preview page so `alert`'s dismiss button works in the gallery. The package itself MUST NOT ship or load JavaScript. *(US1)*
- **FR-007**: A test MUST open every component link the gallery sidebar renders and assert each returns its component's page. The cases come from the sidebar itself, so new components are covered automatically. *(US2)*
- **FR-008**: While the installed gallery release has the index-file defect, folder-component cases MUST be skipped, not marked as expected failures, with a reason naming the upstream issue. No component template may be moved, renamed or duplicated to get around the defect. *(US2)*
- **FR-009**: The defect MUST be reported to django-cotton-gallery with its reproduction during implementation, and this repository's dependency on the fix MUST be recorded. *(US2)*
- **FR-010**: README.md, CONTEXT.md, AGENTS.md, `docs/brainstorm.md`, `docs/adr/0001-icon-is-an-extension-point.md` and CHANGELOG.md MUST NOT name django-mvp or daisy-cotton-blocks as a host, source or consumer of this package. References to the shared CI and toolchain repository (`django-mvp/shared`, `mvp-shared`) MAY remain. *(US3)*
- **FR-011**: `demo/`, `tests/` and the comments in `pyproject.toml` MUST NOT name django-mvp or daisy-cotton-blocks. *(US3)*
- **FR-012**: CONTEXT.md's Demo entry MUST describe the demo as the component gallery alone, on a plain Cotton and daisyUI page with a theme switcher. *(US3)*
- **FR-013**: The CHANGELOG's Unreleased section MUST tell contributors the demo is now the component gallery alone and no longer needs another package. *(US3)*
- **FR-014**: The README MUST state that `alert`'s `dismissible` and `delay` attributes need Alpine.js on the page, that the package doesn't ship it, and what happens without it. *(US4)*

### Key Entities

- **Demo**: the `demo/` Django project, a development target that is never deployed. After this feature it is the component gallery alone.
- **Folder component**: a component whose template is `name/index.html` rather than `name.html`. Cotton resolves both the same way.
- **Index-file defect**: django-cotton-gallery lists a folder component under its folder name but can't open the page it links to.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: With the dev dependencies installed, the resolved dependency tree contains none of django-mvp, django-flex-menus, django-easy-icons, django-crispy-forms or crispy-tailwind.
- **SC-002**: The full test suite passes in CI on every supported Python and Django combination with django-mvp absent.
- **SC-003**: The sidebar-link test runs one case per sidebar link, and every case either passes or is one of the six folder-component skips naming the upstream issue.
- **SC-004**: A case-insensitive search for `mvp` and `daisy-cotton-blocks` across the six documents, `demo/`, `tests/` and `pyproject.toml` finds nothing except references to `django-mvp/shared` or `mvp-shared`.
- **SC-005**: The demo's root URL reaches the gallery in one request or one redirect, and choosing any of the ten themes applies that theme to the preview.

## Assumptions

- Loading daisyUI and Alpine into the demo from a public CDN is acceptable for a development target that is never deployed. The package's requirement that the project supplies daisyUI doesn't change. How the demo loads them is a planning decision.
- The gallery's existing extension points (its extra CSS and JavaScript settings, and its head and body partials) can host the theme switcher. If they can't, the gap goes upstream like the index-file defect.
- The demo's live browser reload comes from the shared development toolchain, not a host package, and stays.
- Issue #11 adds the gallery annotations and the linter gate. Neither feature depends on the other.
