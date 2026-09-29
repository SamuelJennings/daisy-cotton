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

# Every attribute the component offers, filled in.
CALLER_STRINGS = {
    "filter": (
        '<c-form.filter name="status" value="Open" label="Status" '
        'reset_label="Clear" variant="primary" size="sm" required disabled '
        'form="search" id="status-filter" class="mb-4" data-testid="f" '
        ":options=\"['Open', 'Closed']\" />"
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
