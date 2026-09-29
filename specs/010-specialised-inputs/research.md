# Research: Specialised inputs

Evidence behind the plan. Third-party behaviour is cited from what this repository resolves: django-cotton 2.7.2 and django-cotton-gallery 1.0.0 in `.venv/lib/python3.13/site-packages/`, and daisyUI 5.7.46, the build `https://cdn.jsdelivr.net/npm/daisyui@5` serves to the demo.

## R1. daisyUI 5 class names for this feature

Read from the served `daisyui.css` (5.7.46) and daisyUI's class reference:

| Component | Classes |
|---|---|
| filter | `filter`, `filter-reset` (the options are radio inputs carrying `btn`, so `btn-{neutral,primary,secondary,accent,info,success,warning,error}` and `btn-{xs,sm,md,lg,xl}` apply to them) |
| OTP | `otp`, `otp-joined`, `otp-{neutral,primary,secondary,accent,info,success,warning,error}`, `otp-{xs,sm,md,lg,xl}` |
| rating | `rating`, `rating-half`, `rating-hidden`, `rating-{xs,sm,md,lg,xl}`; items carry `mask` and `mask-star`, `mask-star-2` or `mask-heart`, and on a half rating `mask-half-1` or `mask-half-2` |
| calendar | `cally` (the `react-day-picker` and `vc` classes belong to libraries the spec leaves out) |

Colour on a rating item is a background class. `bg-{variant}` for the eight semantic roles keeps it on the palette (Article XII).

## R2. What daisyUI's CSS does with the markup

- **Filter reset glyph.** `.filter input.filter-reset::after` sets `content: "×"`. `.btn:is([type=checkbox],[type=radio])[aria-label]::after` sets `content: attr(aria-label)` and is more specific (three classes/attributes against two and an element). So a reset with an `aria-label` shows that label, and one without shows "×". Keeping `aria-label="×"` shows the glyph under either rule, and the accessible name comes from `aria-labelledby`, which takes precedence (spec Clarifications). The option radios show their label the same way: each option carries its label as `aria-label`.
- **Filter hiding.** daisyUI hides the unchecked options once one is checked and shows the reset only then. It selects `input` elements, so a visually hidden `<span>` inside the wrapper is untouched. `.filter>input:not(:last-child)` adds a gap after each input, so the span goes first, not last.
- **OTP box count.** `.otp:has(>span:nth-child(n))` sets the width from the position of the last `<span>` child, for n up to 8, and `.otp>span` draws each box. Any extra `<span>` child is counted and drawn as a box. The visually hidden name therefore cannot be a `<span>`, and must come after the input so the boxes stay children 1 to `length`. A `<small class="sr-only">` after the input is not counted, is phrasing content (valid inside `<label>`), and is out of flow.
- **OTP focus and disabled.** `.otp:focus-within` and `.otp:has(>input:disabled)` style the boxes from the input's state, so `disabled` has to be on the input for the disabled look.
- **Rating descendants.** `.rating *` gives every descendant the item's background, size and 20% opacity. Nothing but items can sit inside the wrapper, so the group's name goes on the wrapper as `aria-label`, not as hidden text.
- **Rating state.** `.rating :checked`, `[aria-current=true]` and every item before one of them are drawn at full opacity. `.rating :focus-visible` scales the focused item to 1.1. `.rating .rating-hidden` is transparent and narrow.
- **Calendar.** `.cally` styles Cally's shadow parts (`::part(button)`, `::part(day)`, `::part(selected)`), so daisyUI's styling applies once Cally has upgraded the elements.

## R3. Cally

Cally is a set of web components (`calendar-date`, `calendar-range`, `calendar-month`), loaded as an ES module from its npm package. From its documentation and the markup daisyUI's calendar page uses:

- The root reads `value`, `min`, `max`, `locale`, `months`, `first-day-of-week`, `page-by` and `today` as attributes. `months` sets how many months one "next" or "previous" step moves by and how many a range spans. Each `<calendar-month>` shows one month, and `offset="n"` shows the month n after the first.
- The root has `previous` and `next` slots for the paging buttons' content. Cally puts the slotted content inside its own `<button>`, so the slotted content's text is the button's accessible name.
- A chosen date is read from the root's `value` in a `change` event. Copying it into a form input takes a few lines of script, which the documentation shows and the package does not ship.

The demo loads Cally in the preview documents from `https://unpkg.com/cally` as a module, beside daisyUI, Tailwind and Alpine in `demo/templates/django_cotton_gallery/_extra_head.html`. The package loads nothing (spec FR-018).

## R4. Cotton and template behaviour this plan relies on

Taken from FS-009 research R4 and this package's existing templates:

- A bare boolean attribute that is not declared reaches `{{ attrs }}` as a bare attribute. A declared one arrives as `True`.
- A declared name with a default does not fall through to a page variable of the same name.
- `:options="[...]"` arrives as a Python list, and `options="..."` as a string.
- The package's `unique_id` tag already generates ids (`dropdown`, `menu`, `table`), so a generated `name` and the filter reset's hidden-label id use it.
- Django's template language cannot build a numeric range or tell a pair from a plain value. The three loops this feature needs (OTP boxes, calendar months, rating items) and the filter's option shapes need a small Python tag each, in `daisy_cotton/templatetags/daisy_cotton.py` beside `variation` and `unique_id`.

## R5. The gallery

As FS-008 research R7 and FS-009 research R5: gallery 1.0.0 previews each component once with its declared defaults. `select[…]` props get the variants matrix and boolean props a toggle. The linter reports a `@prop` default that differs from the `<c-vars>` default as an error (`default-mismatch`), so a sample list of options cannot be the filter's preview default. The filter's bare preview is therefore a reset alone. Every composed example (a filter with options, a disabled OTP, a disabled or read-only rating, a calendar with `min` and `max`) goes in the fieldset entry's composition, where FS-009 put the labelled, disabled and invalid examples.

## R6. Accessible names

- A radio group is a wrapper with `role="radiogroup"` and an `aria-label`. Each radio is named by its own `aria-label`.
- `aria-labelledby` takes precedence over `aria-label` in the accessible-name computation, so the filter reset shows "×" and is announced "Clear filter".
- `role="img"` with an `aria-label` names the whole read-only rating, and its children are presentational. ARIA 1.2 prohibits `aria-label` on a generic `<div>`, so the read-only items carry none. `aria-current` stays because daisyUI's CSS reads it.
- A `<label>` names the input it contains from its text content, including visually hidden text, so the OTP's `<small class="sr-only">` names its input.
- An `<i>` element is generic, so an `aria-label` on `<c-icon>` would be prohibited. The calendar's paging buttons are named by visually hidden text beside an `aria-hidden` icon inside the slotted element.

## R7. Pluralised and numeric strings

Python's gettext only accepts an integer plural count. Whole rating values use `{% blocktrans count %}` ("1 star", "2 stars"). Half values (0.5, 1.5, …) use one non-plural translatable string with the number in it ("1.5 stars"), because plural rules for decimals differ by language and the integer-only count cannot express them. The read-only name "`value` out of `max`" is one `{% blocktrans %}` string.

## R8. The browser checks

As FS-009 research R8: Playwright and Chromium are available locally, CI has no browser step, and the check runs once at the walkthrough against the running gallery: axe-core on each touched entry, plus scripted checks.

- Filter: tab into the group, arrow between options, the others hide once one is chosen, the reset is reachable and announced "Clear filter" while showing "×", a form submits the chosen value and an empty value after the reset.
- OTP: typing and pasting a code fills the boxes, the focus indicator shows, the form submits the code.
- Rating: the arrow keys change the value, the focused item is visibly marked through the mask (spec Edge Cases), a form submits the value, and the clearable rating submits an empty value.
- Calendar: with Cally loaded, the paging buttons are named "Previous" and "Next", a keyboard user can page, move between days and choose one, with a visible focus indicator.
