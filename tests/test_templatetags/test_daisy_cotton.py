"""Unit tests for the ``responsive`` and ``variation`` template tags.

Both are exercised indirectly through component templates elsewhere (e.g.
``<c-divider vertical="md">``, ``<c-button size="sm">``), but only for the
attribute values those components' own tests happen to pass — a bare
``<c-divider>`` never calls ``responsive`` at all, since its template only
invokes the tag inside an ``{% if vertical %}`` guard. These tests cover the
tags' own branches directly.
"""

from daisy_cotton.templatetags.daisy_cotton import responsive, variation


class TestResponsive:
    def test_true_returns_the_bare_class(self):
        assert responsive(True, "divider-horizontal") == "divider-horizontal"

    def test_a_breakpoint_name_returns_the_prefixed_class(self):
        assert responsive("md", "divider-horizontal") == "md:divider-horizontal"

    def test_falsy_returns_empty_string(self):
        assert responsive(False, "divider-horizontal") == ""
        assert responsive("", "divider-horizontal") == ""
        assert responsive(None, "divider-horizontal") == ""


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
