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

The package ships no JavaScript, so the project loads Cally. The demo loads it so the gallery can show a working calendar. That is the demo showing the component in use, not the package depending on Cally, so Article XII's runtime rule still holds.

## The filter uses daisyUI's structure without a form

daisyUI documents the filter as a `<form>` with a reset input, or as a `<div>` whose reset is a radio carrying `filter-reset`. A filter usually sits inside a larger form: a search box, a list's other filters, a submit button. HTML forbids nested forms, and a reset input inside a form clears every field in it, not just the filter. The `<div>` structure works in every place a filter goes, including a form of its own that the project writes around it.

## The filter reset shows "×" and is named "Clear filter"

daisyUI draws a radio-input button's text from its `aria-label`, so the glyph "×" has to live in `aria-label`. On its own that makes the accessible name "×", which screen readers read as "times" or "multiplication sign". `aria-labelledby` takes precedence over `aria-label` when the browser computes an accessible name, so pointing it at a visually hidden "Clear filter" gives a proper name without changing what is drawn. The implementation should confirm in a browser that the glyph still shows and the name is read.

## Filter options arrive as a list

The README says components take plain values and leave wiring to Django to the project. A list of values, or of (value, label) pairs, is plain data, and it is the same shape as a Django `choices` list, so a caller can pass `form.fields["status"].choices` without the component importing anything from forms. Child components per option were rejected: Cotton does not pass a parent's attributes to its slot content, so every option would have to repeat the group's `name`.

## The filter passes only `variant` and `size` to its buttons

The filter's options are radio inputs carrying daisyUI's `btn` class, not buttons, so `<c-button>` cannot draw them and Article XV does not apply. Colour and size are the two things most filters change, and they already have names under Article XIV. The other button styles would add five attributes for rare uses, and tie-break 3 sends those to a project override.

## The rating takes colour through `variant`

daisyUI has no rating colour modifier. Its examples colour each item with a background class, usually a literal Tailwind colour such as `bg-orange-400`, which Article XIII forbids. Article XIV says that where daisyUI has no name, the attribute reuses the name the package already gives the same idea. Colour is `variant` everywhere else, so `variant="warning"` gives each item `bg-warning`. That keeps the rating on the theme's palette.

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
