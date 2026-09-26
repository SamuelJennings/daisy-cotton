# daisy-cotton

Domain model for daisy-cotton — base daisyUI-styled components for django-cotton.

The terms below are the ones to use in issues, commits, tests and component names.

## Core concepts

**Component**:
The unit this package ships: a single Cotton component (`<c-name>`), styled with daisyUI classes —
a button, an input, a card, an alert, a badge, a modal. A component has no page-level layout of its
own; it composes into whatever a project builds around it.
_Avoid_: element, widget, control, block (see below).

**Block**:
Not used in this package. It names a page-level layout — a hero, a section, a call-to-action —
built from components. Named here only to draw the line: this package's job stops at the
component; a project's own blocks compose components together.

**Host project**:
The Django project that installs daisy-cotton. It owns daisyUI, the active theme and the base
template. This package never reaches into any of them.
_Avoid_: consumer, client, downstream, user.

**Theme**:
A daisyUI theme, supplied and selected by the host project. Components are built from the semantic
palette so they follow whatever theme is active.
_Avoid_: skin, style.

**Semantic palette**:
daisyUI's named colour roles: `primary`, `secondary`, `accent`, `neutral`, `base-100`, `base-200`,
`base-300` and their `-content` pairs. Components use these, never a literal Tailwind colour or a
hard-coded value.

**Demo**:
The `demo/` Django project in this repository: a development target, never deployed, that serves
the component gallery and nothing else — a plain Cotton and daisyUI page with a theme switcher,
with every component browsable as it lands.

## Terms deliberately not used

**Component library**: accurate but too broad — it names this package's shape without saying what
makes it a base layer rather than a framework, which is the distinction that matters. Say
*component* when talking about a single unit, or name the package.
