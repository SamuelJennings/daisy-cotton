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
    count_range,
    filter_options,
    checked_value,
    rating_items,
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

    @pytest.mark.parametrize("options", [[], (), None, "", "Open,Closed", 5, object()])
    def test_empty_none_and_non_iterable_options_give_no_options(self, options):
        assert filter_options(options, "x") == []

    def test_a_django_choices_list_works(self):
        choices = [("draft", "Draft"), ("live", "Live")]

        result = filter_options(choices, "live")

        assert result == [
            {"value": "draft", "label": "Draft", "checked": False},
            {"value": "live", "label": "Live", "checked": True},
        ]


class TestCountRange:
    def test_an_integer_gives_that_many_entries(self):
        assert list(count_range(4, 6)) == [0, 1, 2, 3]

    def test_a_numeric_string_gives_that_many_entries(self):
        assert len(count_range("3", 6)) == 3

    def test_a_string_with_surrounding_whitespace_counts(self):
        assert len(count_range(" 2 ", 6)) == 2

    def test_zero_gives_the_default(self):
        assert len(count_range(0, 6)) == 6

    def test_a_negative_number_gives_the_default(self):
        assert len(count_range(-3, 6)) == 6

    def test_a_negative_numeric_string_gives_the_default(self):
        assert len(count_range("-3", 6)) == 6

    @pytest.mark.parametrize("value", ["abc", "2.5", 2.5, True, [], object()])
    def test_a_non_number_gives_the_default(self, value):
        assert len(count_range(value, 6)) == 6

    @pytest.mark.parametrize("value", ["", None])
    def test_an_empty_value_gives_the_default(self, value):
        assert len(count_range(value, 1)) == 1

    def test_the_result_indexes_from_zero(self):
        assert list(count_range(3, 1)) == [0, 1, 2]


class TestRatingItems:
    def test_five_whole_items_by_default(self):
        result = rating_items(5, False, "")

        assert [item["value"] for item in result] == [1, 2, 3, 4, 5]
        assert all(item["whole"] for item in result)
        assert all(not item["half"] for item in result)

    def test_max_sets_the_number_of_items(self):
        assert [item["value"] for item in rating_items(10, False, "")] == list(
            range(1, 11)
        )

    def test_a_numeric_string_max_counts(self):
        assert len(rating_items("3", False, "")) == 3

    @pytest.mark.parametrize("max_value", ["many", 0, "0", -2, "2.5", "", None])
    def test_a_max_that_is_not_a_positive_whole_number_gives_five(self, max_value):
        assert len(rating_items(max_value, False, "")) == 5

    def test_whole_values_are_ints(self):
        assert all(type(item["value"]) is int for item in rating_items(5, False, ""))

    def test_half_ratings_run_from_a_half_to_max_in_steps_of_a_half(self):
        result = rating_items(3, True, "")

        assert [item["value"] for item in result] == [
            "0.5",
            1,
            "1.5",
            2,
            "2.5",
            3,
        ]

    def test_half_ratings_alternate_the_half_and_mark_whole_values(self):
        result = rating_items(2, True, "")

        assert [item["half"] for item in result] == [1, 2, 1, 2]
        assert [item["whole"] for item in result] == [False, True, False, True]

    def test_half_ratings_give_whole_values_as_ints_and_half_values_as_strings(self):
        for item in rating_items(5, True, ""):
            expected = int if item["whole"] else str
            assert type(item["value"]) is expected

    @pytest.mark.parametrize("value", [7, "7", "7.0", " 7 ", 7.0])
    def test_value_matches_as_a_number(self, value):
        result = rating_items(10, False, value)

        assert [item["value"] for item in result if item["checked"]] == [7]

    def test_value_checks_one_half_item(self):
        result = rating_items(5, True, "2.5")

        assert [item["value"] for item in result if item["checked"]] == ["2.5"]

    def test_a_whole_value_checks_the_whole_item_on_a_half_rating(self):
        result = rating_items(5, True, 2)

        assert [item["value"] for item in result if item["checked"]] == [2]

    @pytest.mark.parametrize(
        "value", ["", None, "abc", "nan", "inf", 6, "6", 0, -1, "0.5", True]
    )
    def test_a_value_that_is_empty_not_a_number_out_of_range_or_off_step_checks_nothing(
        self, value
    ):
        assert not any(item["checked"] for item in rating_items(5, False, value))

    def test_a_value_off_the_half_step_checks_nothing(self):
        assert not any(item["checked"] for item in rating_items(5, True, "2.3"))

    def test_a_whole_rating_has_no_item_at_a_half_value(self):
        assert not any(item["checked"] for item in rating_items(5, False, "2.5"))

    def test_every_item_carries_the_documented_keys(self):
        for item in rating_items(2, True, 1):
            assert set(item) == {"value", "half", "whole", "checked"}


class TestCheckedValue:
    def test_gives_the_value_of_the_checked_item(self):
        assert checked_value(rating_items(5, False, "3")) == 3

    def test_gives_a_half_value(self):
        assert checked_value(rating_items(5, True, "1.5")) == "1.5"

    @pytest.mark.parametrize("value", ["", "9", "0", 0, "abc"])
    def test_gives_an_empty_string_when_nothing_is_checked(self, value):
        assert checked_value(rating_items(5, False, value)) == ""
