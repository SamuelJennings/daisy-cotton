"""Shared rules across the specialised inputs, tested once per rule.

Parametrised once per rule rather than duplicated per component: no <script>
or on*= handler in the rendered output, and a page context carrying the
component's own declared names leaves its declared defaults in place (model:
tests/test_form_controls.py). Each story extends this module with its own
component's row rather than repeating the rule.
"""

import re
from collections import Counter
from pathlib import Path

import pytest

EVENT_HANDLER = re.compile(r"\son[a-z]+\s*=", re.IGNORECASE)
FIELDSET_TEMPLATE = (
    Path(__file__).parent.parent
    / "daisy_cotton"
    / "templates"
    / "cotton"
    / "form"
    / "fieldset.html"
)
DEMO_HEAD = (
    Path(__file__).parent.parent
    / "demo"
    / "templates"
    / "django_cotton_gallery"
    / "_extra_head.html"
)

# Every attribute the component offers, filled in.
CALLER_STRINGS = {
    "filter": (
        '<c-form.filter name="status" value="Open" label="Status" '
        'reset_label="Clear" variant="primary" size="sm" required disabled '
        'form="search" id="status-filter" class="mb-4" data-testid="f" '
        ":options=\"['Open', 'Closed']\" />"
    ),
    "calendar": (
        '<c-form.calendar range months="2" previous_icon="bi bi-arrow-left" '
        'next_icon="bi bi-arrow-right" class="mb-4" id="delivery" '
        'value="2026-09-01/2026-09-07" min="2026-09-01" max="2026-09-30" '
        'locale="en-GB" first-day-of-week="1" data-testid="c" />'
    ),
    "otp": (
        '<c-form.otp name="code" id="otp-code" length="4" label="Code" '
        'variant="primary" size="sm" joined required disabled autofocus '
        'form="verify" value="1234" pattern="[0-9]{4}" inputmode="numeric" '
        'input_class="validator" class="mb-4" data-testid="o" />'
    ),
    "rating": (
        '<c-form.rating name="score" value="3" label="Your rating" max="10" '
        'shape="heart" variant="warning" size="lg" half clearable required '
        'disabled form="review" id="score-rating" class="mb-4" '
        'data-testid="r" />'
    ),
    "rating-readonly": (
        '<c-form.rating readonly value="3" label="Your rating" max="10" '
        'shape="heart" variant="warning" size="lg" half clearable '
        'id="score-rating" class="mb-4" data-testid="r" />'
    ),
}

# The bare component, and a page context naming every declared attribute with
# a value that must not leak into the rendered output.
PAGE_CONTEXT_LEAK = {
    "filter": (
        "<c-form.filter />",
        {
            "options": "leaked-options",
            "value": "leaked-value",
            "name": "leaked-name",
            "label": "leaked-label",
            "reset_label": "leaked-reset-label",
            "variant": "leaked-variant",
            "size": "leaked-size",
            "required": "leaked-required",
            "disabled": "leaked-disabled",
            "form": "leaked-form",
            "class": "leaked-class",
        },
    ),
    "calendar": (
        "<c-form.calendar />",
        {
            "range": "leaked-range",
            "months": "leaked-months",
            "previous_icon": "leaked-previous-icon",
            "next_icon": "leaked-next-icon",
            "class": "leaked-class",
        },
    ),
    "otp": (
        "<c-form.otp />",
        {
            "length": "leaked-length",
            "label": "leaked-label",
            "variant": "leaked-variant",
            "size": "leaked-size",
            "joined": "leaked-joined",
            "pattern": "leaked-pattern",
            "inputmode": "leaked-inputmode",
            "input_class": "leaked-input-class",
            "class": "leaked-class",
        },
    ),
    "rating": (
        "<c-form.rating />",
        {
            "max": "leaked-max",
            "value": "leaked-value",
            "name": "leaked-name",
            "label": "leaked-label",
            "shape": "leaked-shape",
            "variant": "leaked-variant",
            "size": "leaked-size",
            "half": "leaked-half",
            "clearable": "leaked-clearable",
            "readonly": "leaked-readonly",
            "required": "leaked-required",
            "disabled": "leaked-disabled",
            "form": "leaked-form",
            "class": "leaked-class",
        },
    ),
}


class TestSpecialisedInputsNoScript:
    @pytest.mark.parametrize(
        "source", CALLER_STRINGS.values(), ids=CALLER_STRINGS.keys()
    )
    def test_rendered_output_has_no_script_element(self, cotton_render_string, source):
        assert "<script" not in cotton_render_string(source).lower()

    @pytest.mark.parametrize(
        "source", CALLER_STRINGS.values(), ids=CALLER_STRINGS.keys()
    )
    def test_rendered_output_has_no_event_handler_attribute(
        self, cotton_render_string, source
    ):
        assert not EVENT_HANDLER.search(cotton_render_string(source))


class TestSpecialisedInputsPageContextDoesNotLeak:
    @pytest.mark.parametrize(
        "source_and_context", PAGE_CONTEXT_LEAK.values(), ids=PAGE_CONTEXT_LEAK.keys()
    )
    def test_declared_names_do_not_leak_from_the_page_context(
        self, cotton_render_string, source_and_context
    ):
        source, context = source_and_context
        html = cotton_render_string(source, dict(context))

        for leaked_value in context.values():
            assert leaked_value not in html


def _fieldset_composition():
    """The source of the fieldset's ``@slot`` example, the composed gallery form."""
    for line in FIELDSET_TEMPLATE.read_text(encoding="utf-8").splitlines():
        if line.startswith("{# @slot <"):
            return line.removeprefix("{# @slot ").split(" \u2014 ")[0]
    raise AssertionError("the fieldset template carries no @slot example")


class TestFieldsetCompositionFilters:
    @pytest.fixture
    def composition(self, cotton_render_string_soup):
        return cotton_render_string_soup(_fieldset_composition())

    @pytest.fixture
    def filter_fieldset(self, composition):
        fieldsets = [
            fieldset
            for fieldset in composition.find_all("fieldset")
            if fieldset.find("div", class_="filter")
        ]
        assert fieldsets, "the composition holds no filter"
        return fieldsets[0]

    def test_the_composition_holds_a_filter_row_in_its_own_fieldset(
        self, filter_fieldset
    ):
        assert filter_fieldset.find("legend") is not None
        assert len(filter_fieldset.find_all("div", class_="filter")) >= 3

    def test_every_filter_has_an_accessible_name(self, filter_fieldset):
        for group in filter_fieldset.find_all("div", class_="filter"):
            assert group["role"] == "radiogroup"
            assert group.get("aria-label") or group.find_parent("fieldset").find(
                "legend"
            )
            for radio in group.find_all("input", type="radio"):
                assert radio.get("aria-label")
            reset = group.find("input", class_="filter-reset")
            assert group.find(id=reset["aria-labelledby"]) is not None

    def test_ids_are_unique_within_the_composition(self, composition):
        ids = [element["id"] for element in composition.find_all(id=True)]

        assert [id_ for id_, count in Counter(ids).items() if count > 1] == []

    def test_each_filter_has_its_own_name(self, filter_fieldset):
        names = []
        for group in filter_fieldset.find_all("div", class_="filter"):
            group_names = {radio["name"] for radio in group.find_all("input")}
            assert len(group_names) == 1
            names.extend(group_names)

        assert len(names) == len(set(names))

    def test_the_row_shows_nothing_chosen_and_one_chosen(self, filter_fieldset):
        chosen = [
            len(group.find_all("input", checked=True))
            for group in filter_fieldset.find_all("div", class_="filter")
        ]

        assert 0 in chosen
        assert 1 in chosen

    def test_the_row_shows_a_colour_and_a_size(self, filter_fieldset):
        classes = {
            name
            for radio in filter_fieldset.find_all("input", type="radio")
            for name in radio["class"]
        }

        assert {"btn-primary", "btn-sm", "btn-accent", "btn-lg"} <= classes


class TestFieldsetCompositionCalendars:
    @pytest.fixture
    def composition(self, cotton_render_string_soup):
        return cotton_render_string_soup(_fieldset_composition())

    @pytest.fixture
    def calendar_fieldset(self, composition):
        fieldsets = [
            fieldset
            for fieldset in composition.find_all("fieldset")
            if fieldset.find(["calendar-date", "calendar-range"])
        ]
        assert fieldsets, "the composition holds no calendar"
        return fieldsets[0]

    def test_the_composition_holds_a_calendar_row_in_its_own_fieldset(
        self, calendar_fieldset
    ):
        assert calendar_fieldset.find("legend") is not None
        assert calendar_fieldset.find("calendar-date") is not None
        assert calendar_fieldset.find("calendar-range") is not None

    def test_the_single_date_calendar_has_a_minimum_and_a_maximum(
        self, calendar_fieldset
    ):
        calendar = calendar_fieldset.find("calendar-date")

        assert calendar.get("min")
        assert calendar.get("max")

    def test_the_range_calendar_shows_two_months(self, calendar_fieldset):
        calendar = calendar_fieldset.find("calendar-range")

        assert len(calendar.find_all("calendar-month")) == 2

    def test_every_calendar_draws_its_paging_icons_from_an_icon_font(
        self, calendar_fieldset
    ):
        calendars = calendar_fieldset.find_all(["calendar-date", "calendar-range"])
        assert len(calendars) >= 2
        for calendar in calendars:
            previous = calendar.find(attrs={"slot": "previous"}).find("i")
            following = calendar.find(attrs={"slot": "next"}).find("i")
            assert {"bi", "bi-chevron-left"} <= set(previous["class"])
            assert {"bi", "bi-chevron-right"} <= set(following["class"])

    def test_every_calendar_paging_button_has_a_name(self, calendar_fieldset):
        for calendar in calendar_fieldset.find_all(["calendar-date", "calendar-range"]):
            for slot in ("previous", "next"):
                name = calendar.find(attrs={"slot": slot}).find(class_="sr-only")
                assert name.get_text(strip=True)


class TestFieldsetCompositionOtps:
    @pytest.fixture
    def composition(self, cotton_render_string_soup):
        return cotton_render_string_soup(_fieldset_composition())

    @pytest.fixture
    def otp_fieldset(self, composition):
        fieldsets = [
            fieldset
            for fieldset in composition.find_all("fieldset")
            if fieldset.find("label", class_="otp")
        ]
        assert fieldsets, "the composition holds no OTP"
        return fieldsets[0]

    def test_the_composition_holds_an_otp_row_in_its_own_fieldset(self, otp_fieldset):
        assert otp_fieldset.find("legend") is not None
        assert len(otp_fieldset.find_all("label", class_="otp")) >= 3

    def test_every_otp_has_an_accessible_name(self, otp_fieldset):
        for label in otp_fieldset.find_all("label", class_="otp"):
            name = label.find("small", class_="sr-only")
            assert name.get_text(strip=True)
            assert name.find_previous_sibling("input") is not None

    def test_the_row_shows_a_labelled_a_joined_four_digit_and_a_disabled_otp(
        self, otp_fieldset
    ):
        labels = otp_fieldset.find_all("label", class_="otp")
        inputs = [label.find("input") for label in labels]

        assert any("otp-joined" in label["class"] for label in labels)
        assert any(field["maxlength"] == "4" for field in inputs)
        assert any(field.has_attr("disabled") for field in inputs)
        assert len({label.find("small").get_text(strip=True) for label in labels}) >= 2

    def test_each_otp_has_its_own_name(self, otp_fieldset):
        names = [
            field["name"]
            for field in otp_fieldset.find_all("input")
            if field.find_parent("label", class_="otp")
        ]

        assert all(names)
        assert len(names) == len(set(names))

    def test_ids_are_unique_within_the_composition(self, composition):
        ids = [element["id"] for element in composition.find_all(id=True)]

        assert [id_ for id_, count in Counter(ids).items() if count > 1] == []


class TestFieldsetCompositionRatings:
    @pytest.fixture
    def composition(self, cotton_render_string_soup):
        return cotton_render_string_soup(_fieldset_composition())

    @pytest.fixture
    def rating_fieldset(self, composition):
        fieldsets = [
            fieldset
            for fieldset in composition.find_all("fieldset")
            if fieldset.find("div", class_="rating")
        ]
        assert fieldsets, "the composition holds no rating"
        return fieldsets[0]

    def _interactive(self, rating_fieldset):
        return [
            group
            for group in rating_fieldset.find_all("div", class_="rating")
            if group.get("role") == "radiogroup"
        ]

    def _read_only(self, rating_fieldset):
        return [
            group
            for group in rating_fieldset.find_all("div", class_="rating")
            if group.get("role") == "img"
        ]

    def test_the_composition_holds_a_rating_row_in_its_own_fieldset(
        self, rating_fieldset
    ):
        assert rating_fieldset.find("legend") is not None
        assert len(rating_fieldset.find_all("div", class_="rating")) >= 4

    def test_every_rating_has_an_accessible_name(self, rating_fieldset):
        for group in rating_fieldset.find_all("div", class_="rating"):
            assert group.get("aria-label")
        for group in self._interactive(rating_fieldset):
            for radio in group.find_all("input", type="radio"):
                assert radio.get("aria-label")

    def test_the_row_shows_a_clearable_rating(self, rating_fieldset):
        assert any(
            group.find("input", class_="rating-hidden")
            for group in self._interactive(rating_fieldset)
        )

    def test_the_row_shows_a_half_star_rating_with_a_value(self, rating_fieldset):
        halves = [
            group
            for group in self._interactive(rating_fieldset)
            if "rating-half" in group["class"]
        ]

        assert halves
        assert any(group.find("input", checked=True) for group in halves)

    def test_the_row_shows_a_disabled_rating(self, rating_fieldset):
        assert any(
            all(radio.has_attr("disabled") for radio in group.find_all("input"))
            for group in self._interactive(rating_fieldset)
        )

    def test_the_row_shows_a_read_only_rating_with_a_value(self, rating_fieldset):
        read_only = self._read_only(rating_fieldset)

        assert read_only
        assert any(group.find(attrs={"aria-current": "true"}) for group in read_only)

    def test_each_interactive_rating_has_its_own_name(self, rating_fieldset):
        names = []
        for group in self._interactive(rating_fieldset):
            group_names = {radio["name"] for radio in group.find_all("input")}
            assert len(group_names) == 1
            names.extend(group_names)

        assert len(names) >= 3
        assert len(names) == len(set(names))

    def test_ids_are_unique_within_the_composition(self, composition):
        ids = [element["id"] for element in composition.find_all(id=True)]

        assert [id_ for id_, count in Counter(ids).items() if count > 1] == []


class TestDemoHeadLoadsCally:
    @pytest.fixture
    def head(self):
        return DEMO_HEAD.read_text(encoding="utf-8")

    def test_cally_loads_as_a_module_from_unpkg_at_a_pinned_version(self, head):
        assert re.search(
            r"<script\s+type=\"module\"\s+src=\"https://unpkg\.com/cally@\d+\.\d+\.\d+\"",
            head,
        )

    def test_cally_loads_only_after_the_preview_document_check(self, head):
        guard = head.index("if (!isPreviewDocument) return;")

        assert head.index("cally@") > guard

    def test_the_closing_script_tag_is_split_inside_the_inline_script(self, head):
        line = next(line for line in head.splitlines() if "cally@" in line)

        assert "</script>" not in line
        assert "</' + 'script>" in line
