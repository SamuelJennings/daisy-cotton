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

from daisy_cotton.templatetags.daisy_cotton import responsive, unique_id, variation


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
    """FR-019: a caller with no `id` still gets a unique panel identifier."""

    def test_the_id_is_the_prefix_and_eight_lowercase_hex_characters(self):
        result = unique_id("dropdown")
        assert re.fullmatch(r"dropdown-[0-9a-f]{8}", result)

    def test_two_calls_differ(self):
        assert unique_id("dropdown") != unique_id("dropdown")
