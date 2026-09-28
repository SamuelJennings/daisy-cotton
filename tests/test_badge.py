"""Tests for <c-badge>'s daisyUI structure: a ``<span>`` carrying ``badge``,
the variant/size/style modifiers, ``text`` then the default slot, and
pass-through ``class``/attributes.
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


def _class_attrs_on(html, tag):
    """Every ``class="..."`` value found on the first ``<tag ...>`` open tag."""
    return [
        name_value[1] for name_value in _attrs_on(html, tag) if name_value[0] == "class"
    ]


def _attr_value(attrs, name):
    """The value of the first attribute named ``name``, or ``None``."""
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


class TestBadgeElement:
    def test_renders_a_span_carrying_badge(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-badge>New</c-badge>")

        span = soup.find("span", class_="badge")
        assert span is not None
        assert soup.find("div", class_="badge") is None


class TestBadgeContent:
    def test_text_attribute_is_the_badges_content(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-badge text="New" />')

        span = soup.find("span", class_="badge")
        assert span.get_text(strip=True) == "New"

    def test_text_renders_before_the_default_slot(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-badge text="Status: ">Paid</c-badge>')

        span = soup.find("span", class_="badge")
        assert span.get_text(strip=True) == "Status: Paid"


class TestBadgeVariant:
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
        html = cotton_render_string(f'<c-badge variant="{variant}">Paid</c-badge>')

        root_classes = _class_attrs_on(html, "span")
        assert f"badge-{variant}" in root_classes[0]

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-badge variant="rainbow">Paid</c-badge>')

        root_classes = _class_attrs_on(html, "span")
        assert "badge-rainbow" not in root_classes[0]


class TestBadgeSize:
    @pytest.mark.parametrize("size", ["xs", "sm", "md", "lg", "xl"])
    def test_each_size_maps_to_its_daisyui_class(self, cotton_render_string, size):
        html = cotton_render_string(f'<c-badge size="{size}">Paid</c-badge>')

        root_classes = _class_attrs_on(html, "span")
        assert f"badge-{size}" in root_classes[0]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-badge size="xxl">Paid</c-badge>')

        root_classes = _class_attrs_on(html, "span")
        assert "badge-xxl" not in root_classes[0]


class TestBadgeStyleBooleans:
    def test_outline_adds_badge_outline(self, cotton_render_string):
        html = cotton_render_string("<c-badge outline>Paid</c-badge>")
        assert "badge-outline" in _class_attrs_on(html, "span")[0]

    def test_dash_adds_badge_dash(self, cotton_render_string):
        html = cotton_render_string("<c-badge dash>Paid</c-badge>")
        assert "badge-dash" in _class_attrs_on(html, "span")[0]

    def test_soft_adds_badge_soft(self, cotton_render_string):
        html = cotton_render_string("<c-badge soft>Paid</c-badge>")
        assert "badge-soft" in _class_attrs_on(html, "span")[0]

    def test_ghost_adds_badge_ghost(self, cotton_render_string):
        html = cotton_render_string("<c-badge ghost>Paid</c-badge>")
        assert "badge-ghost" in _class_attrs_on(html, "span")[0]

    def test_variant_size_and_a_style_boolean_combine_in_one_class_list(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-badge variant="success" size="sm" soft>Paid</c-badge>'
        )

        root_classes = _class_attrs_on(html, "span")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        for token in ("badge", "badge-success", "badge-sm", "badge-soft"):
            assert token in root_classes[0]


class TestBadgeInsideButton:
    def test_badge_inside_a_button_is_a_span_with_no_block_element(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-button text="Cart"><c-badge variant="secondary">3</c-badge></c-button>'
        )

        button = soup.find("button")
        assert button is not None

        badge = button.find("span", class_="badge")
        assert badge is not None
        assert badge.get_text(strip=True) == "3"

        block_tags = {"div", "p", "section", "article", "ul", "ol", "table", "form"}
        for descendant in button.find_all(recursive=True):
            assert descendant.name not in block_tags


class TestBadgeClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_badge(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-badge class="ms-2" data-test="x">Paid</c-badge>'
        )

        root_classes = _class_attrs_on(html, "span")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "ms-2" in root_classes[0]
        assert "badge" in root_classes[0]

        attrs = _attrs_on(html, "span")
        assert _attr_value(attrs, "data-test") == "x"


class TestBadgePageContextDoesNotLeak:
    def test_page_context_text_and_variant_do_not_leak_in(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-badge />",
            context={"text": "Leaked", "variant": "error"},
        )

        span = soup.find("span", class_="badge")
        assert span.get_text(strip=True) == ""
        assert "badge-error" not in (span.get("class") or [])
