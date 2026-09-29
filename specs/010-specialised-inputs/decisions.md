# Decisions: Specialised inputs

Ambiguities in issue #19 that were resolved while writing the spec, with the reasoning behind each. The short form of every one is in `spec.md` under *Clarifications*.

## Validator has no component

daisyUI's validator is a class added to an input, select or textarea, plus a hint element beside it. It changes how another control looks, so under the README's scope rule it gets no component. A project adds the class through the control's own class attribute, and the OTP exposes `input_class` so its inner input can take it.

## The calendar supports Cally only

daisyUI styles three calendar libraries:

- **Cally** is a set of web components. The calendar is written as markup (`<calendar-date>`, `<calendar-month>`, slotted month icons), so there is real markup for a component to own.
- **React Day Picker** is a React component and cannot be written in a Django template.
- **Vanilla Calendar Pro** is an empty `<div class="vc">` that its script builds. A component would emit one div with one class, which a project can write faster than it can look up the component.

Cally is therefore the only library the component serves. A project using Vanilla Calendar Pro writes its div directly.

The package ships no JavaScript, so the project loads Cally. The demo loads it so the gallery can show a working calendar. That is the demo showing the component in use, not the package depending on Cally, so Article XI's runtime rule still holds.

## The filter uses daisyUI's structure without a form

daisyUI documents the filter as a `<form>` with a reset input, or as a `<div>` whose reset is a radio carrying `filter-reset`. A filter usually sits inside a larger form: a search box, a list's other filters, a submit button. HTML forbids nested forms, and a reset input inside a form clears every field in it, not just the filter. The `<div>` structure works in every place a filter goes, including a form of its own that the project writes around it.

## The filter reset shows "×" and is named "Clear filter"

daisyUI draws a radio-input button's text from its `aria-label`, so the glyph "×" has to live in `aria-label`. On its own that makes the accessible name "×", which screen readers read as "times" or "multiplication sign". `aria-labelledby` takes precedence over `aria-label` when the browser computes an accessible name, so pointing it at a visually hidden "Clear filter" gives a proper name without changing what is drawn. The implementation should confirm in a browser that the glyph still shows and the name is read.

## Filter options arrive as a list

The README says components take plain values and leave wiring to Django to the project. A list of values, or of (value, label) pairs, is plain data, and it is the same shape as a Django `choices` list, so a caller can pass `form.fields["status"].choices` without the component importing anything from forms. Child components per option were rejected: Cotton does not pass a parent's attributes to its slot content, so every option would have to repeat the group's `name`.

## The filter passes only `variant` and `size` to its buttons

The filter's options are radio inputs carrying daisyUI's `btn` class, not buttons, so `<c-button>` cannot draw them and Article XIV does not apply. Colour and size are the two things most filters change, and they already have names under Article XIII. The other button styles would add five attributes for rare uses, and tie-break 3 sends those to a project override.

## The rating takes colour through `variant`

daisyUI has no rating colour modifier. Its examples colour each item with a background class, usually a literal Tailwind colour such as `bg-orange-400`, which Article XII forbids. Article XIII says that where daisyUI has no name, the attribute reuses the name the package already gives the same idea. Colour is `variant` everywhere else, so `variant="warning"` gives each item `bg-warning`. That keeps the rating on the theme's palette.

## The rating's shape is `shape`

The rating's items are daisyUI masks. FS-004's `<c-mask>` names the mask class `shape`, so the rating does too. The rating offers the three shapes daisyUI's rating examples use (`star`, `star-2`, `heart`). The items are radio inputs, which `<c-mask>` does not emit, so the rating writes the mask classes itself, as daisyUI's rating markup does.

## The read-only rating is announced as an image

daisyUI's read-only markup is a row of `<div>` elements with `aria-current="true"` on the selected one. A screen reader reading that row hears a list of unlabelled shapes, or "1 star, 2 star, 3 star" with no sign of which is current. Naming the whole rating as an image, "3 out of 5", gives the value in one phrase. The per-item markup stays because daisyUI's CSS uses `aria-current` to shade the items.

## Clearing a rating submits an empty value

`clearable` follows daisyUI: a first radio carrying `rating-hidden`, which is invisible and lets the user unset the rating. It carries an empty value, so a cleared rating submits the field with nothing in it, the same thing a blank text input submits. It is checked when no value is given, so an untouched rating submits an empty value instead of leaving the field out of the form.

## The OTP defaults to six digits

daisyUI supports four to six boxes. Six is the length TOTP authenticator apps and most text-message codes use, so it is the default. The `pattern` accepts digits only, matching daisyUI's syntax and the numeric keypad `inputmode` brings up. A project with letter codes overrides `pattern` and `inputmode` on the input, or overrides the component.

## The OTP names itself with visually hidden text

daisyUI puts the OTP inside a `<label>`, whose text would normally name the input. Here the label holds only empty boxes, so the input has no name. Nesting a visible label inside it is invalid HTML, so `label` renders as visually hidden text inside the existing label, with "Verification code" as the default. A visible heading comes from the fieldset legend, and `label` can repeat it for the input.

## Control attributes reach the input

The OTP's root is a `<label>` and the rating's and filter's roots are `<div>` elements. `name`, `value`, `required`, `disabled` and the rest do nothing there and would be silently dropped, so they go to the input or radios. This is the same split FS-005 made for the swap. Where #18 settles a different list for the core controls, these components follow #18, so all form controls in the package behave the same way.

## Priorities

Priorities reflect how many adopters need each component. The filter appears on list and search pages across most data applications (P1). The calendar and OTP are each needed by many applications, but on few pages, and the calendar also needs a third-party script (P2). The rating belongs to reviews and feedback, which fewer applications have (P3).

## D1 — The spec read against FS-001 to FS-009, and the `form.` namespace

Nine features were delivered after this spec landed. Read against their specs, one changes what this spec says. At FS-009's walkthrough the maintainer asked for every form component to sit under a `form.` namespace, so a project's form markup reads as one family, and FS-009's decisions record it ("The `form.` namespace", D11). This spec was written before that ruling and names `<c-filter>`, `<c-calendar>`, `<c-otp>` and `<c-rating>`. All four belong to the same daisyUI data-input group as FS-009's controls, and the spec itself describes them as building on those controls. So they are `<c-form.filter>`, `<c-form.calendar>`, `<c-form.otp>` and `<c-form.rating>`, with their templates in `templates/cotton/form/`. Only the names change. The calendar goes with the others because daisyUI files it in the same group and a project would look for it there.

The other features change nothing here. FS-004's `<c-mask>` still names the mask classes `shape`. FS-005's swap still splits its wrapper and checkbox and takes `input_class`. FS-008's loading and FS-006's components still name themselves with `label`. FS-009 delivered the fieldset and legend this spec's filter, OTP and rating sit in, and settled the attribute rule D2 applies.

**ADR:** none — the namespace ruling is already recorded in FS-009's decisions and applied here as written.

## D2 — Which attributes reach the control

The spec's clarification lists `id`, `name`, `value`, `required`, `disabled`, `autofocus` and `form` for the control and sends everything else to the wrapper, "where #18 settles a different list for the core controls, these components follow #18". FS-009 (#18) settled that for a single control `class` goes to the element carrying daisyUI's class and every other attribute goes to the control. The OTP is a single control, so it follows FS-009: `class` on the `<label class="otp">`, everything else on the `<input>`. Acceptance scenario US3-5's "any other attribute lands on the label" reads accordingly.

FS-009 has no group component, so it settles nothing for the filter and the rating. For them the spec's own list stands, adjusted for a group of radios: `name`, `value`, `required`, `disabled` and `form` are declared and written on every radio (`value` checks the matching one), and everything else, `id` included, goes to the wrapper through `attrs`. An `id` cannot be repeated on every radio, and `aria-describedby` from a fieldset's description belongs on the group. `autofocus` is left to pass through to the wrapper rather than picking a radio for it, since which radio should take focus depends on the page.

**ADR:** none — follows FS-009's rule and the spec's own clarification.

## D3 — Where the hidden names go

daisyUI's CSS constrains where visually hidden text can sit. The OTP counts its `<span>` children to size itself and draws each one as a box, so its name is a `<small class="sr-only">` after the input. The rating styles every descendant as an item, so its group name is an `aria-label` on the wrapper. The filter's reset keeps `aria-label="×"` because daisyUI draws a radio button's text from its `aria-label`, and takes its announced name from a `hidden` span through `aria-labelledby`, as the spec describes. The calendar's paging buttons are named by hidden text beside an `aria-hidden` icon, because an `aria-label` on the icon's `<i>` element is not allowed by ARIA. Research R2 and R6 give the CSS and the rule for each.

**ADR:** none — local to these four templates.

## D4 — The calendar's paging icons

The spec says `<c-icon>` draws the previous and next icons. `<c-icon>` takes a CSS class string and does no lookup (ADR 0001), and the calendar has to pass it something. `previous_icon` and `next_icon` default to `chevron-left` and `chevron-right`, the names a project's own `<c-icon>` override resolves, as the alert passes its variant name. With the bare `<c-icon>` a caller passes its icon classes, and the gallery example passes Bootstrap Icons classes, which the demo already loads. `icon` is the name the button, alert and menu already use for an icon's classes, so the two attributes follow it.

**ADR:** none — follows ADR 0001 and the alert's precedent.

## D5 — Design review applied

The review approved the plan with no critical or high findings, four medium and six low. All were applied as plan, research and task edits:

- The rating binds each item's value explicitly inside `blocktrans`, and whole values reach the plural count as numbers, because Django's `blocktrans count` rejects a string. The rating test asserts that every radio's name differs rather than that one exists.
- The calendar's description says the paging icons need icon classes or a resolving `<c-icon>`, and the calendar's bare gallery preview is recorded as having empty paging buttons.
- Cally is pinned to 0.9.2 in the demo and the README, and research R3 is checked against that version's source: its paging button has no name of its own, so the slotted text names it.
- The filter's reset name is a `hidden` span, which drops the ordering rule and its test. The filter's bare preview is empty, since daisyUI hides the reset until an option is chosen, so its colours and sizes are shown in the composition.
- The filter and rating descriptions say that `autofocus` on the group does nothing and that `required` cannot stop an empty submission once there is a reset or a clearable item. D2's choice to leave `autofocus` on the wrapper stands.
- The OTP pattern's braces use `templatetag`, the read-only rating's name defaults the value to 0, and the browser check submits the filter, OTP and rating in one form.

One finding asks that the spec's tag names match what ships. The `form.` names (D1) are raised with the maintainer at the walkthrough, where a rename is still cheap either way.

**ADR:** none — plan and documentation edits local to this feature.

## D6 — The roadmap records every delivered group

With the specialised inputs in, R7 is delivered. The roadmap status step found R1 to R6 delivered as well, by the features before this one, with their status lines never updated. All seven now read as delivered, each brief rewritten to say what is true now, in the same change that completes the last of them. The cleanup pass renamed `rating_items`' first parameter from `max`, which shadowed a builtin behind a lint suppression, to `highest`.

**ADR:** none — roadmap housekeeping and a parameter name.
