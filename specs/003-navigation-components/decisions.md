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

## D1 — Tab shape follows the attributes given, and link tabs say so on the root

A tab given `href` is a link, a tab given `name` is a radio input with its panel, and any other tab is a `<button role="tab">`. A Cotton item cannot read its parent's attributes (research R1), so the radio group's `name` is given to each tab, exactly as it is given to each native radio input. The root has to know one thing the items decide: whether it is a tab widget. A `role="tablist"` holding plain links is an accessibility error, and the spec's decision is that link tabs drop that role. `<c-tabs links>` does that. daisyUI has no name for it and no other component in this package has the idea, so the attribute is named for what the caller is building.

**Revisit if:** Cotton gains a supported way for a child to read its parent's attributes.

**ADR:** none — local to the tabs component, nothing else inherits it.

## D2 — A megamenu item is given its megamenu's id

FR-026 builds every panel id from the megamenu's id. The item cannot read that id (research R1), so it takes it as `megamenu`, plus a `key` unique within the megamenu, and its panel id is `<megamenu>-<key>`. Both are required.

**Revisit if:** as D1.

**ADR:** none — local to the megamenu component.

## D3 — The breadcrumb text span's class goes

`breadcrumbs/item.html` wraps its text in `<span class="daisy-cotton-breadcrumb-text">`, which came across from django-mvp for a stylesheet this package does not ship. FR-002 forbids emitting a class daisyUI does not define for the component, so the class goes. The hrefless item keeps a span, because that is where `aria-current="page"` goes.

**ADR:** none — follows directly from FR-002.

## D4 — Pre-existing tests the approved breaking changes invalidate

Article I forbids changing a pre-existing test without a recorded decision. These change, because the spec Sam approved changes the behaviour they pin, and nothing else about them does:

- `tests/test_link.py::TestLinkDefaults::test_default_href_falls_back_to_hash` pins the `href="#"` default that "Link loses its `href=\"#\"` default" removes. It becomes a test that no `href` is emitted.
- `tests/test_breadcrumbs_href_attribute.py::TestTheItemTextSpan` pins the class D3 removes. Its three cases become the same assertions about the text and slot order without the class.
- `tests/test_breadcrumbs_href_attribute.py::TestTheItemTextSpan::test_href_class_and_attrs_still_land_where_they_did` pins pass-through attributes on the `<a>`, which "Attributes on list items go to the item's root" moves to the `<li>`.

**ADR:** none — test maintenance under approved spec changes.

## D5 — The accessibility check runs against the running gallery

SC-004 is checked by axe-core and a scripted keyboard walk over each gallery entry, run once at the walkthrough, with the result in the pull request (research R7). Running it in CI needs a workflow edit and a new dependency, and SC-004 does not ask for CI. The suite asserts what the markup can show: roles, names, states and native elements.

**Revisit if:** browser tests are switched on in this repository's CI.

**ADR:** none — how this feature verifies one criterion.

## D6 — Built on main while pull request #100 is open

Open pull request #100 retypes fixed-value props as `select[…]` and edits `link.html`. This branch starts from main and types every fixed-value prop it touches as `select[…]` already, so the two agree whichever merges first. The second to merge resolves the conflict in `link.html`.

**ADR:** none — sequencing between two open branches.

## D7 — Design review applied

One design review round, verdict "request changes", no critical or high findings. Applied as plan and task edits:

- Nested `<c-icon>` and `<c-button>` calls end in `only` and receive what they need explicitly, and the megamenu toggle is `type="button"` (ARCH-001).
- A disabled link carries `role="link" aria-disabled="true"` with no `href`, so it is announced as disabled (SPEC-001).
- `start`, `center` and `end` on the navbar and `name` on a tab default to `""`, so a page-context variable of the same name cannot change the markup (ARCH-002).
- The megamenu's description tells the viewer to set `id` in the gallery playground (SPEC-004).
- `menu.item` writes a given `aria-label` on its inner link or button, where an icon-only item needs its name (review note).

**ADR:** none — plan corrections inside this feature.

## D8 — Radio tabs keep the tablist role until the accessibility run says otherwise

The review expects axe-core to flag radio inputs inside `role="tablist"` (a tablist must own tabs), which would put US4 scenario 6 against SC-004. Scenario 6 is approved and daisyUI documents that markup, so the tabs are built as specified. If the walkthrough's run reports the violation, it goes to Sam as a one-line change to scenario 6: radio tabs get no container role, since native radios sharing a name already give arrow-key selection.

**ADR:** none — a question for the spec's owner, not an architectural decision.

## D9 — The dock's drawer toggle is not a Tab stop

FR-022 keeps the drawer-toggle branch, and FR-005 requires every interactive element to be operable from the keyboard. A `<label role="button" tabindex="0">` can be focused but not activated by Enter or Space without a script, which FR-004 rules out. The toggle drops `role` and `tabindex`, so it is a click target only, and keyboard users open the drawer through its own `drawer-toggle` checkbox, which daisyUI leaves focusable.

**ADR:** none — local to the dock item.
