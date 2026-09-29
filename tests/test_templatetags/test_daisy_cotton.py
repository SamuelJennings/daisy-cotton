"""Unit tests for the ``responsive``, ``variation`` and ``unique_id`` template tags.

``responsive`` and ``variation`` are exercised indirectly through component
templates elsewhere (e.g. ``<c-divider vertical="md">``, ``<c-button
size="sm">``), but only for the attribute values those components' own tests
happen to pass — a bare ``<c-divider>`` never calls ``responsive`` at all,
since its template only invokes the tag inside an ``{% if vertical %}``
guard. These tests cover the tags' own branches directly.
"""

import re

import pytest

from daisy_cotton.templatetags.daisy_cotton import (
    filter_options,
    responsive,
    unique_id,
    variation,
)


class TestResponsive:
    def test_true_returns_the_bare_class(self):
        assert responsive(True, "divider-horizontal") == "divider-horizontal"

    def test_a_breakpoint_name_returns_the_prefixed_class(self):
        assert responsive("md", "divider-horizontal") == "md:divider-horizontal"

    def test_falsy_returns_empty_string(self):
        assert responsive(False, "divider-horizontal") == ""
        assert responsive("", "divider-horizontal") == ""
        assert responsive(None, "divider-horizontal") == ""

    def test_a_string_that_is_not_a_breakpoint_returns_empty_string(self):
        assert responsive("true", "divider-horizontal") == ""
        assert responsive("left", "divider-horizontal") == ""

    @pytest.mark.parametrize("bp", ["sm", "md", "lg", "xl", "2xl"])
    def test_every_daisyui_breakpoint_is_accepted(self, bp):
        assert responsive(bp, "divider-horizontal") == f"{bp}:divider-horizontal"


class TestVariation:
    def test_an_allowed_value_returns_the_suffixed_class(self):
        assert variation("sm", "btn", "sm,md,lg") == "btn-sm"

    def test_an_unallowed_value_returns_empty_string(self):
        assert variation("xl", "btn", "sm,md,lg") == ""

    def test_falsy_returns_empty_string(self):
        assert variation("", "btn", "sm,md,lg") == ""
        assert variation(None, "btn", "sm,md,lg") == ""

    def test_allowed_accepts_a_list_as_well_as_a_comma_string(self):
        assert variation("sm", "btn", ["sm", "md", "lg"]) == "btn-sm"


class TestUniqueId:
    def test_the_id_is_the_prefix_and_eight_lowercase_hex_characters(self):
        result = unique_id("dropdown")
        assert re.fullmatch(r"dropdown-[0-9a-f]{8}", result)

    def test_two_calls_differ(self):
        assert unique_id("dropdown") != unique_id("dropdown")


class TestFilterOptions:
    def test_a_plain_value_is_its_own_label(self):
        assert filter_options(["Open"], "") == [
            {"value": "Open", "label": "Open", "checked": False}
        ]

    def test_a_tuple_splits_into_value_and_label(self):
        assert filter_options([("o", "Open")], "") == [
            {"value": "o", "label": "Open", "checked": False}
        ]

    def test_a_list_pair_splits_into_value_and_label(self):
        assert filter_options([["o", "Open"]], "") == [
            {"value": "o", "label": "Open", "checked": False}
        ]

    def test_entries_keep_their_order(self):
        result = filter_options(["a", ("b", "B"), "c"], "")

        assert [entry["value"] for entry in result] == ["a", "b", "c"]

    def test_the_entry_matching_value_is_checked_and_no_other(self):
        result = filter_options(["Open", "Closed"], "Closed")

        assert [entry["checked"] for entry in result] == [False, True]

    def test_an_integer_value_matches_a_string_value(self):
        result = filter_options([1, 2, 3], "2")

        assert [entry["checked"] for entry in result] == [False, True, False]

    def test_a_string_entry_value_matches_an_integer_value(self):
        result = filter_options([("2", "Two")], 2)

        assert result[0]["checked"] is True

    @pytest.mark.parametrize("value", ["", None])
    def test_an_empty_value_checks_nothing(self, value):
        result = filter_options(["Open", "Closed", ""], value)

        assert not any(entry["checked"] for entry in result)

    def test_a_value_matching_no_entry_checks_nothing(self):
        result = filter_options(["Open", "Closed"], "Archived")

        assert not any(entry["checked"] for entry in result)

    @pytest.mark.parametrize("options", [[], (), None, "", 5, object()])
    def test_empty_none_and_non_iterable_options_give_no_options(self, options):
        assert filter_options(options, "x") == []

    def test_a_django_choices_list_works(self):
        choices = [("draft", "Draft"), ("live", "Live")]

        result = filter_options(choices, "live")

        assert result == [
            {"value": "draft", "label": "Draft", "checked": False},
            {"value": "live", "label": "Live", "checked": True},
        ]
