# Decisions: Navigation components

Choices made while specifying where the issue, the goals and the constitution left a gap. Each is also folded into `spec.md`.

## Pagination has no component

daisyUI's pagination is a `join` of `btn` elements with no class of its own. G1 excludes a component daisyUI builds from other components, so pagination is listed in the README with that reason instead of being built. Driving pagination from a Django paginator was already out of scope for this group.

## Link loses its `href="#"` default

A placeholder `#` makes every `<c-link>` without an `href` look like a working link that goes nowhere. Emitting no `href` is honest about it. Breaking, recorded in the CHANGELOG.

## Breadcrumbs and dock lose their extra classes

`text-sm` on breadcrumbs and `bg-transparent backdrop-blur` on the dock came across with the components from django-mvp. They are not part of daisyUI's markup for either component, and the README's first tie-break is to follow daisyUI. Projects that want them add them through `class`.

## Attributes on list items go to the item's root

The constitution sends everything a component does not declare to its root element. For menu, breadcrumb and step items that root is the `<li>`, not the link inside it. Attributes meant for the link (`target`, `hx-*`) are written on a link in the item's slot. The alternative, treating the inner link as the root, would carve an exception into the constitution for one family of components.

## Script-only menu classes are not attributes

`menu-dropdown`, `menu-dropdown-toggle`, `menu-dropdown-show` and `menu-focus` exist for a script to toggle. The package ships no script, so they get no attributes. A project passes them through `class`.

## Buttons, not links, for tabs with no destination

daisyUI documents button tabs with `role="tab"`. Without an `href` and outside radio shape, a tab renders that way, and a project that wants client-side switching adds its own script. Link tabs drop the tablist role, because a set of page links is navigation, not a tab widget, and mark the current page with `aria-current`.

## Navigation regions are landmarks

Breadcrumbs, dock, megamenu and navbar each render as a navigation landmark with a translatable default name. Menu, tabs and steps do not, because they usually sit inside one of those, or inside a page region that already names itself. A project that uses a bare menu as its main navigation wraps it or passes `role` and `aria-label` through.

## Megamenu requires an id and includes its toggle

Every item's panel needs a page-unique id for `popovertarget`, so the megamenu takes one required id and derives the panel ids from it. daisyUI's documented megamenu includes the small-screen toggle button, and without it the megamenu cannot be opened below `sm`, so it is part of the component.
