# Decisions: Action components

Ambiguities in issue #14 that were resolved while writing the spec, with the reasoning behind each. The short form of every one is in `spec.md` under *Clarifications*.

## The dropdown uses the popover method

daisyUI documents three ways to build a dropdown:

- **Popover.** A button targets a popover panel. The browser handles opening, closing on Escape and on an outside click, and tells assistive technology whether the panel is open. The trigger is a real `<button>`, so `<c-button>` can draw it.
- **`<details>` and `<summary>`.** The browser reports the open state, but the trigger must be the `<summary>` element itself. A button inside a summary is invalid HTML, so the trigger would have to copy the button's classes inline, which Article XV forbids. It also does not close on an outside click without script.
- **CSS focus.** This is what the current component does. The panel shows while focus is inside it. Nothing reports whether it is open, and Escape does not close it without script. It is the only method that supports `dropdown-hover`.

Popover is the only method that meets G3 and Article XV together with no script, and it is the one daisyUI lists first. The cost is `hover`, `dropdown-open` and `dropdown-close`, which daisyUI's rules tie to the other methods, and placement depends on CSS anchor positioning. A project that wants hover-to-open overrides the component, which is what the README's tie-break 2 prescribes.

## `placement` replaces `valign`, `halign` and `position`

daisyUI calls both class groups "placement". Article XIV asks for daisyUI's name where it has one. Two attributes for one daisyUI concept would also go against tie-break 3. The dropdown takes a side and an alignment in one value, for example `placement="top end"`, because daisyUI's examples combine one of each.

## The modal drops its inner card

The current modal puts a `<c-card>` inside a transparent modal box, so its attributes are the card's: `title`, `icon`, `footer`, `footer_end`. daisyUI's modal is a box with an actions row. Tie-break 1 (follow daisyUI) and tie-break 3 (fewer attributes) both point to the plain structure. `title` stays because it gives the dialog its accessible name, which G3 needs. `actions` stays because it maps to daisyUI's `modal-action`. A project that wants a card puts one in the slot.

## The modal drops `size`

daisyUI has no modal size modifier. Article XIV reserves `size` for daisyUI's `xs`–`xl` scale, and the current `size` maps to arbitrary maximum widths instead. Width goes through `content_class` on the box.

## `content_class` for inner surfaces

Article XIV sends `class` to the root element. The modal box and the dropdown panel are inner elements that callers regularly need to size or style. The dropdown already calls this attribute `content_class`. Article XIV says to reuse an existing name for the same idea before coining one, so the modal uses it too.

## The button's non-daisyUI attributes go

- `full` becomes `block`, daisyUI's name for the same modifier.
- `align` sets a flex justification. That is a layout class, so it passes through `class`.
- `reverse` puts the icon after the text. Putting the icon in the default slot does the same with no attribute.
- `condition` wraps the button in an `if`. The caller's template can do that itself.

All four removals follow tie-break 3. They break existing callers, which is acceptable below 0.1.0 as long as the CHANGELOG lists them.

## The swap's control attributes reach the checkbox

The swap's wrapper is a `<label>` and its control is a hidden checkbox. `checked`, `disabled`, `name` and `value` are meaningless on the label and would silently do nothing there, so they go to the checkbox. `label` gives the checkbox its accessible name. Both slots stay in the accessibility tree (daisyUI hides the inactive one visually only), so the label text cannot name the control reliably.

## The swap documents the theme toggle

The theme controller is excluded because it is a class on an input. The most common place adopters use it is on a swap's checkbox, a sun and moon toggle. The swap therefore accepts extra classes on its checkbox, and its documentation shows the toggle. The exclusion and its reason are recorded where adopters will look for the component.

## The FAB trigger is explicitly focusable

daisyUI's FAB opens while its trigger has focus, and its examples use `<div tabindex="0" role="button">` because some browsers do not focus a clicked `<button>`. Article XV requires the trigger to come from `<c-button>`, so the trigger is a `<c-button>` with `tabindex="0"`, the same approach the current dropdown takes. The implementation should confirm in a real browser that a click opens the FAB.

## Priorities

Priorities reflect how many adopters need each component: the button everywhere (P1), the modal and dropdown in most applications (P2), the swap and FAB in some (P3).

## D1 — Built on main while two other component pull requests are open

Pull requests #101 (navigation components) and #102 (layout components) are open and unmerged.
This feature branches from main and builds on neither. All three change the README's component
count and list and append to the CHANGELOG, so whichever merges later resolves those lines by
hand. None touches another's templates. #102 narrows the `responsive` tag in the same template tag
module this feature adds `unique_id` to, which is a line-level merge.

**ADR:** none — a sequencing note for concurrent branches, nothing downstream inherits it.

## D2 — The pre-existing button, dropdown and modal tests are rewritten

`tests/test_button.py` asserts `condition`, which the approved spec removes (FR-011).
`tests/test_dropdown.py` asserts `valign`, `halign`, `full`, `hover`, the `dropdown-content` panel
and the focus-method trigger, all of which FR-017 and FR-020 replace. `tests/test_modal.py`
asserts `position`, `size` and the inner card, which FR-014 and FR-016 remove. Each module is
rewritten to the new contract in its story (T001, T004, T008). T001 also updates the one
expected-markup string in `tests/test_dropdown.py` that asserts the old button classes on the
dropdown's trigger, so the suite is green at the end of US1 and not only at the end of the batch. The behaviours they guarded that
survive (`size` sets the button's size, an undeclared attribute passes through, `class` and
`content_class` land where they should) are asserted again in the new modules.

**Why:** Article I forbids changing a pre-existing test without a recorded decision. This is it.

**ADR:** none — local to this feature's approved breaking changes, recorded in the CHANGELOG.

## D3 — The modal's gallery entry cannot open the dialog from its trigger

The gallery 1.0.0 puts a `@trigger` inside the component's default slot (research R3), so the
modal's trigger sits inside the closed dialog where nothing can reach it. This is already true on
main. Scenario US2-7 asks for each placement, the closable variant and a modal with actions to be
opened from a trigger button in the gallery. The entry does the closest the tool allows: the
`@trigger` annotation shows the trigger's markup, and the `open` toggle shows each placement, the
close button and the actions row rendered. The in-browser check of opening from a trigger,
Escape and focus return runs in the accessibility run instead (T013), against the same template.

**Falls short of US2-7** as written. This goes to Sam at the walkthrough.

**Revisit if:** a gallery release renders a trigger outside the component tag.

**ADR:** none — a workaround for one tool version, recorded here and in research R3.

## D4 — `open` shows the dialog without making it modal

`<dialog open>` is the only way to show a dialog from markup alone. The browser then treats it as
non-modal: Escape does not close it and focus is not trapped. The backdrop and the close button
still close it, because both are `method="dialog"` forms. Scenario US2-6 asks only that the
modal is already shown, which this does. A project that needs the re-rendered dialog to be modal
calls `showModal()` on load, which is the project's script, not the package's. The `open`
description says so.

**ADR:** none — a property of the HTML element, documented on the prop.

## D5 — Forwarded trigger attributes are typed into the gallery by hand

The dropdown's and FAB's default triggers are drawn from the attributes the caller gives the
component (FR-018, FR-026). The gallery lists only declared props and has no way to prefill the
extra-attributes field, so their previews open with an unlabelled trigger. Declaring `text`,
`icon`, `variant` and the rest on each component to fill the gallery would duplicate half the
button's vocabulary and still leave the other half forwarded. The descriptions tell the viewer
which attributes to type (`text="Options"`, or `icon="bi bi-plus-lg" aria-label="Actions"`).

**ADR:** none — an annotation choice for two components.

## D6 — `class` gets an empty default too

Design review SPEC-001. Cotton pushes an enclosing component's attributes, its declared `class`
included, into the context its inner components render in. A name declared with no default then
reads that value. On main, `<c-dropdown class="mt-4">` puts `mt-4` on the wrapper and on the
trigger button. For the FAB this would move the trigger away from its actions whenever a project
positions the FAB with a class. Every template this feature touches declares `class=""`, and the
dropdown and FAB tests assert the component's `class` is absent from the default trigger.

**ADR:** none — the empty-default pattern already used for every other declared name.

## D7 — Design review applied

One design reviewer, three lenses, verdict request changes with one high finding.

- SPEC-001 (high) → D6, plan "Empty defaults", T008 and T012 assertions.
- SPEC-002 → D2 and T001 update the dropdown test's expected trigger markup.
- SPEC-003 → the dropdown writes `popovertarget` and `style` after `:attrs`, so a caller's `style`
  cannot remove the anchor. T008 tests it.
- SPEC-004 → the `title` description says it names the dialog when `id` is set.
- SPEC-005 → T013 names the dropdown's gallery URL.
- SPEC-006 → the no-script check asserts on rendered output, not the template source.
- SPEC-007 → dropped the test that a caller's `type` replaces the trigger's.
- Notes folded into T006, T011 and T013: the modal description asks for `title` or `aria-label`
  and says the trigger cannot open an already-shown dialog; the `indeterminate` slot says only a
  project's script sets that state; T013 opens a dropdown inside an open modal. `modal-open` is
  reachable through `class` (SC-001), and `open` covers the same state.

**ADR:** none — a record of review dispositions.
