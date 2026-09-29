# Tasks: Specialised inputs

**Input**: `specs/010-specialised-inputs/` — spec.md, plan.md, research.md, decisions.md

**Organization**: by user story, in build order (plan.md "Story order").

**Every story's done-check**: its acceptance scenarios each have a test that fails when the behaviour is removed, except the gallery and in-browser scenarios the browser check covers (T012). An unknown `variant`, `size` or `shape` emits no class for it and does not raise. Its templates pass `uv run python manage.py cotton_lint --warnings-as-errors` (SC-002). Its component, rendered from a caller string, emits no `<script>` and no `on*=` attribute, and keeps its own defaults inside a page context carrying its declared names: each is one parametrised test in `tests/test_specialised_inputs.py`, which the story extends with its component's rows. It emits no daisyUI class that does not exist for the component (research R1). `class` merges into the root and an extra attribute reaches the element plan.md "Attribute routing" names. No wording is asserted: tests find elements by role, attribute and structure. New test modules are in `[tool.forge.conformance] non-mirror-paths`. Its README and CHANGELOG lines are written in the story. Every control it adds to the fieldset composition has an accessible name, and colours come from the semantic palette only.

Tests render through the Cotton compiler as a caller's template would (the `cotton_render_string` and `cotton_render_string_soup` fixtures in `tests/conftest.py`), never by rendering the component file directly. Template tags are tested by calling them.

## Phase 1: US1 — Filter (P1)

- [ ] T001 [US1] `filter_options(options, value)` in `daisy_cotton/templatetags/daisy_cotton.py` per plan "Template tags", with a Google-style docstring. Tests first in `tests/test_templatetags/test_daisy_cotton.py` (`TestFilterOptions`): plain values are their own label, (value, label) tuples and lists split, integer values compare with a string `value`, an empty or unmatched `value` checks nothing, an empty list, `None` and a non-iterable give no options, a Django `choices`-shaped list works.
- [ ] T002 [US1] `form/filter.html` per plan "Filter". Tests first in a new `tests/test_filter.py` for scenarios 1–4, 6 (the reset carries `aria-label="×"` and `aria-labelledby` pointing at an element that exists in the output, with `reset_label` changing that element's text and nothing else), 7 (two filters without `name` get different names, each shared by all its radios) and 8, plus: `label` giving `role="radiogroup"` and `aria-label` on the wrapper, no `aria-label` on the wrapper without it, `required`, `disabled` and `form` on every radio and not on the wrapper, `id` and an extra attribute on the wrapper, `class` merged into the wrapper, the reset's empty `value`, no radio checked when `value` matches nothing (Edge Cases), an empty options list rendering only the reset, unknown `variant` and `size` emitting no `btn-` modifier (FR-009–FR-013). Start `tests/test_specialised_inputs.py` with the filter's rows (plan "Shared rules, tested once"; model: `tests/test_form_controls.py`).
- [ ] T003 [US1] Gallery annotations for `filter` (plan "Filter" and "Gallery entries"). The fieldset composition gains US1's row. README: count up by one and `form.filter` in the list, and the *Scope & philosophy* note that validator has no component (FR-008). CHANGELOG `Added`.

## Phase 2: US2 — Calendar (P2)

- [ ] T004 [US2] `count_range(value, default)` per plan "Template tags". Tests first (`TestCountRange`): an integer, a numeric string, zero, a negative, a non-number and an empty value, each giving the expected length.
- [ ] T005 [US2] `form/calendar.html` per plan "Calendar". Tests first in a new `tests/test_calendar.py` for scenarios 1–5 as markup: the `<calendar-date>` root with `cally` and one `<calendar-month>`; `range` giving `<calendar-range>`; `months="2"` giving two months, the second with `offset="1"`, and `months="2"` on the root; `value`, `min`, `max`, `locale` and `first-day-of-week` on the root unchanged; the `previous` and `next` slot elements each holding an `aria-hidden` `<i>` with the icon class and a visually hidden text element; `previous_icon` and `next_icon` reaching the icons; the calendar's own `class` on the root and not on either icon; a non-number `months` giving one month (FR-014–FR-017). Extend `tests/test_specialised_inputs.py`.
- [ ] T006 [US2] Gallery annotations for `calendar`. The demo head loads Cally (plan "Demo"). The fieldset composition gains US2's row. README: count, `form.calendar` in the list, the scope note that the calendar needs Cally, and the calendar usage section with the script tag and the date-copying script (FR-018, US2-7). CHANGELOG `Added`.

**Checkpoint**: batch 1 green. Full suite, `cotton_lint --warnings-as-errors`, pre-commit.

## Phase 3: US3 — OTP (P2)

- [ ] T007 [US3] `form/otp.html` per plan "OTP". Tests first in a new `tests/test_otp.py` for scenarios 1–5: the `<label>` with `otp`, six empty `<span>` children first, the input with `maxlength="6"`, `pattern="[0-9]{6}"`, `inputmode="numeric"`, `autocomplete="one-time-code"` and `type="text"`; `length="4"` giving four spans and four-digit `maxlength` and `pattern`; `variant`, `size` and `joined` on the label; the hidden name element after the input, not a `<span>`, and `label` changing its text; `required`, `disabled`, `id`, `name` and an extra attribute on the input and not on the label, `class` on the label; `input_class` on the input; `pattern` and `inputmode` replacing the defaults with exactly one of each attribute; a non-number `length` giving six boxes; unknown `variant` and `size` emitting nothing (FR-019–FR-023). Extend `tests/test_specialised_inputs.py`.
- [ ] T008 [US3] Gallery annotations for `otp`. The fieldset composition gains US3's row. README: count and `form.otp` in the list. CHANGELOG `Added`.

## Phase 4: US4 — Rating (P3)

- [ ] T009 [US4] `rating_items(max, half, value)` per plan "Template tags". Tests first (`TestRatingItems`): five whole items by default, `max=10`, half items from 0.5 to `max` with alternating halves and `whole` set on whole values, whole values returned as ints and half values as strings, `value` matching as an int, a string and `"7.0"`, and an empty, non-number, too-high, negative or off-step `value` checking nothing, a non-number `max` giving five.
- [ ] T010 [US4] `form/rating.html` per plan "Rating". Tests first in a new `tests/test_rating.py` for scenarios 1–7: the wrapper with `rating`, `role="radiogroup"` and the `label` as `aria-label`; five radios sharing a name with values 1–5, each with `mask` and `mask-star`; `max="10" value="7"` checking the seventh; each radio's `aria-label` differing from every other radio's, on whole and half ratings; `clearable` adding a first radio with `rating-hidden` and an empty value, checked with no `value` and unchecked with one; `half` giving `rating-half`, ten radios with alternating `mask-half-1`/`mask-half-2` and values 0.5 to 5; `shape="heart"`, `variant="warning"` and `size="lg"` giving `mask-heart` and `bg-warning` on every item and `rating-lg` on the wrapper; `readonly value="3"` giving `<div>` items, no inputs, `aria-current="true"` on the third only and `role="img"` with an `aria-label` on the wrapper. Plus: two ratings without `name` getting different names; `required`, `disabled` and `form` on every radio; `id` and an extra attribute on the wrapper; unknown `shape`, `variant` and `size` emitting nothing; a `value` above `max` checking nothing (FR-024–FR-030). Extend `tests/test_specialised_inputs.py`.
- [ ] T011 [US4] Gallery annotations for `rating`. The fieldset composition gains US4's row. README: count and `form.rating` in the list. CHANGELOG `Added`.

**Checkpoint**: batch 2 green.

## Phase 5: Browser check at the walkthrough (orchestrator)

- [ ] T012 Run axe-core and the scripted checks (research R8) against the four gallery entries and the fieldset composition on the running demo, and record the result in the pull request's test evidence (SC-003, SC-005, US1-5, US1-6, US2-6, US3-6, US4-8, the rating focus edge case). The filter's bare preview is empty and the calendar's bare preview has empty paging buttons, both by construction (plan "Gallery entries"), and are recorded as expected. A failure the markup can fix becomes a fix task. A failure that is daisyUI's or Cally's is reported in the pull request, not worked around.

## Dependencies

- Each story adds its own template, test module and tag. They share `daisy_cotton/templatetags/daisy_cotton.py`, its test module, `README.md`, `CHANGELOG.md`, `pyproject.toml`, `tests/test_specialised_inputs.py` and the fieldset composition, so they run one after another on one branch.
- US3 uses US2's `count_range`. A composition example may only use components that already exist.
- T012 needs every story done and the demo running.
