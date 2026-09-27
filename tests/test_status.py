"""Tests for <c-status>: daisyUI's status markup — a small coloured dot
that tells a screen-reader user what it means through ``label``, or is
hidden from assistive technology when beside text that already says it.
"""

from html.parser import HTMLParser

import pytest


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser — which is what a duplicate
    ``class`` attribute needs to be caught.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _attrs_on(html, tag):
    """The raw ``(name, value)`` attribute list of the first ``<tag ...>`` open tag."""
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return parser.attrs


def _attr_value(attrs, name):
    """The value of the first attribute named ``name``, or ``None`` if absent."""
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


def _class_attrs_on(html, tag):
    """Every ``class="..."`` value found on the first ``<tag ...>`` open tag."""
    return [
        name_value[1] for name_value in _attrs_on(html, tag) if name_value[0] == "class"
    ]


class TestStatusElement:
    """FR-034: the status is a ``<span>`` carrying ``status``."""

    def test_renders_a_span_carrying_status(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-status />")

        span = soup.find("span", class_="status")
        assert span is not None


class TestStatusVariant:
    """FR-034: ``variant`` maps to daisyUI's eight colours."""

    @pytest.mark.parametrize(
        "variant",
        [
            "neutral",
            "primary",
            "secondary",
            "accent",
            "info",
            "success",
            "warning",
            "error",
        ],
    )
    def test_each_variant_maps_to_its_daisyui_class(
        self, cotton_render_string, variant
    ):
        html = cotton_render_string(f'<c-status variant="{variant}" />')

        root_classes = _class_attrs_on(html, "span")
        assert f"status-{variant}" in root_classes[0]

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-status variant="rainbow" />')

        root_classes = _class_attrs_on(html, "span")
        assert "status-rainbow" not in root_classes[0]


class TestStatusSize:
    """FR-034: ``size`` maps xs-xl to daisyUI's ``status-<size>`` class."""

    @pytest.mark.parametrize("size", ["xs", "sm", "md", "lg", "xl"])
    def test_each_size_maps_to_its_daisyui_class(self, cotton_render_string, size):
        html = cotton_render_string(f'<c-status size="{size}" />')

        root_classes = _class_attrs_on(html, "span")
        assert f"status-{size}" in root_classes[0]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-status size="xxl" />')

        root_classes = _class_attrs_on(html, "span")
        assert "status-xxl" not in root_classes[0]

    def test_variant_and_size_combine_in_one_class_list(self, cotton_render_string):
        html = cotton_render_string('<c-status variant="success" size="lg" />')

        root_classes = _class_attrs_on(html, "span")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        for token in ("status", "status-success", "status-lg"):
            assert token in root_classes[0]


class TestStatusAccessibility:
    """FR-035: given ``label``, the status is exposed as an image named by
    it (US9-3); without one, it is hidden from assistive technology (US9-4).
    """

    def test_label_gives_role_img_and_aria_label(self, cotton_render_string):
        html = cotton_render_string(
            '<c-status variant="success" size="lg" label="Online" />'
        )

        attrs = _attrs_on(html, "span")
        assert _attr_value(attrs, "role") == "img"
        assert _attr_value(attrs, "aria-label") == "Online"
        assert _attr_value(attrs, "aria-hidden") is None

    def test_no_label_is_hidden_from_assistive_technology(self, cotton_render_string):
        html = cotton_render_string('<c-status variant="success" />')

        attrs = _attrs_on(html, "span")
        assert _attr_value(attrs, "aria-hidden") == "true"
        assert _attr_value(attrs, "role") is None
        assert _attr_value(attrs, "aria-label") is None


class TestStatusClassAndAttrs:
    """``class`` merges into the status's single class list, and other
    attributes reach the status (FR-002)."""

    def test_class_merges_and_extra_attributes_reach_the_status(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-status class="ms-2" data-test="x" />')

        root_classes = _class_attrs_on(html, "span")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "ms-2" in root_classes[0]
        assert "status" in root_classes[0]

        attrs = _attrs_on(html, "span")
        assert _attr_value(attrs, "data-test") == "x"


class TestStatusPageContextDoesNotLeak:
    """A page variable sharing a declared name never fills an empty status."""

    def test_page_context_label_and_variant_do_not_leak_in(self, cotton_render_string):
        html = cotton_render_string(
            "<c-status />",
            context={"label": "Leaked", "variant": "error"},
        )

        attrs = _attrs_on(html, "span")
        assert _attr_value(attrs, "aria-hidden") == "true"
        assert _attr_value(attrs, "aria-label") is None
        root_classes = _class_attrs_on(html, "span")
        assert "status-error" not in root_classes[0]
