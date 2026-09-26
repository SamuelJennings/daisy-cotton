# ADR 0001 — `<c-icon>` is a bare primitive, overridden by projects that need resolution

**Status:** accepted

## Decision

`daisy_cotton`'s `<c-icon>` component does no icon-name resolution. Its entire body is:

```html
<c-vars name class />
<i class="{{ name }} {{ class }}" {{ attrs }}></i>
```

`name` is a literal CSS class string, not a semantic name looked up against an icon pack. A
project that wants name-to-glyph resolution — an icon font, an SVG sprite system, a component
library such as django-easy-icons — installs its own `templates/cotton/icon.html` above
`daisy_cotton` in `INSTALLED_APPS`, which Cotton resolves as a straight template-path shadow: the
project's own component replaces this one everywhere, with no further wiring.

Every other component in this package that renders an icon (`button`, `alert`, `card`, `dock.item`,
`form.field`'s pre/post-label slots) calls `<c-icon name="..." />` exactly as
it would call a richer, resolving version. A project's override is a drop-in replacement, not a
fork of every caller.

## Why

The alternative was taking on django-easy-icons (or an equivalent) as a runtime dependency, since
it is what django-mvp's own icon-bearing components use today. Rejected: it would make every
consumer of `daisy_cotton` pull in an icon-resolution package whether or not it wants one, and it
would tie this package's release cadence to that dependency's for a concern this package does not
actually need to solve. The components that use `icon=` do not care how a name becomes markup —
they only need something to render into that slot.

## Revisit if

A second package in this family needs the same resolution logic and starts duplicating it, at
which point a shared (but still optional) icon-resolution package is worth extracting — daisy-cotton
itself should stay dependency-free either way.
