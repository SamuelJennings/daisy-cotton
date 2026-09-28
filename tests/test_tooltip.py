"""Tests for <c-tooltip>: daisyUI's tooltip, rendering its hint as an
element so it reaches assistive technology instead of living in CSS.
"""

from html.parser import HTMLParser

import pytest


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _attrs_on(html, tag):
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return parser.attrs


def _attr_value(attrs, name):
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


class TestTooltipRoot:
    def test_renders_a_wrapper_carrying_tooltip_around_the_trigger(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-tooltip tip="Copy link"><c-button>Copy</c-button></c-tooltip>'
        )

        div = soup.find("div", class_="tooltip")
        assert div is not None
        assert div.find("button") is not None

    def test_tooltip_content_holds_role_tooltip_and_the_tip_text(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-tooltip tip="Copy link"><c-button>Copy</c-button></c-tooltip>'
        )

        content = soup.div.find("div", class_="tooltip-content")
        assert content is not None
        assert content["role"] == "tooltip"
        assert content.get_text(strip=True) == "Copy link"

    def test_tooltip_content_is_a_direct_child_of_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-tooltip tip="Copy link">x</c-tooltip>')

        content = soup.div.find("div", class_="tooltip-content", recursive=False)
        assert content is not None

    def test_no_data_tip_attribute_anywhere(self, cotton_render_string):
        html = cotton_render_string('<c-tooltip tip="Copy link">x</c-tooltip>')

        assert "data-tip" not in html

    def test_no_id_on_the_wrapper(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-tooltip tip="Copy link" id="copy-hint">x</c-tooltip>'
        )

        assert soup.div.get("id") is None


class TestTooltipPlacement:
    @pytest.mark.parametrize(
        "placement,classes",
        [
            ("top", ["tooltip-top"]),
            ("bottom", ["tooltip-bottom"]),
            ("left", ["tooltip-left"]),
            ("right", ["tooltip-right"]),
            ("start", ["tooltip-start"]),
            ("center", ["tooltip-center"]),
            ("end", ["tooltip-end"]),
            ("bottom end", ["tooltip-bottom", "tooltip-end"]),
        ],
    )
    def test_each_placement_word_maps_to_its_daisyui_class(
        self, cotton_render_string_soup, placement, classes
    ):
        soup = cotton_render_string_soup(
            f'<c-tooltip placement="{placement}">x</c-tooltip>'
        )

        for css_class in classes:
            assert css_class in soup.div["class"]

    def test_unknown_placement_word_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-tooltip placement="diagonal">x</c-tooltip>'
        )

        assert not any("diagonal" in cls for cls in soup.div["class"])


class TestTooltipVariant:
    @pytest.mark.parametrize(
        "variant",
        ["primary", "secondary", "accent", "info", "success", "warning", "error"],
    )
    def test_each_variant_maps_to_its_daisyui_class(
        self, cotton_render_string_soup, variant
    ):
        soup = cotton_render_string_soup(
            f'<c-tooltip variant="{variant}">x</c-tooltip>'
        )

        assert f"tooltip-{variant}" in soup.div["class"]

    def test_neutral_emits_no_class_and_does_not_raise(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-tooltip variant="neutral">x</c-tooltip>')

        assert not any("neutral" in cls for cls in soup.div["class"])


class TestTooltipOpen:
    def test_open_emits_tooltip_open(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-tooltip open>x</c-tooltip>")

        assert "tooltip-open" in soup.div["class"]

    def test_no_open_emits_no_tooltip_open(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-tooltip>x</c-tooltip>")

        assert "tooltip-open" not in soup.div["class"]


class TestTooltipContentSlot:
    def test_content_slot_replaces_tip_in_the_tooltip_content_element(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-tooltip tip="Copy link">'
            '<c-slot name="content"><kbd>Ctrl</kbd>+C</c-slot>'
            "x</c-tooltip>"
        )

        content = soup.div.find("div", class_="tooltip-content")
        assert content.find("kbd") is not None
        assert "Copy link" not in content.get_text()


class TestTooltipId:
    def test_id_lands_on_the_content_element_only(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-tooltip tip="Copy link" id="copy-hint">x</c-tooltip>'
        )

        content = soup.div.find("div", class_="tooltip-content")
        assert content["id"] == "copy-hint"
        assert soup.div.get("id") is None


class TestTooltipClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-tooltip tip="x" class="mt-4" data-test="x">x</c-tooltip>'
        )

        div = soup.div
        assert "mt-4" in div["class"]
        assert "tooltip" in div["class"]
        assert div["data-test"] == "x"


class TestTooltipPageContextDoesNotLeak:
    def test_page_context_does_not_leak_into_the_tooltip(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-tooltip>x</c-tooltip>",
            context={
                "tip": "Leaked",
                "content": "Leaked",
                "placement": "top",
                "variant": "error",
                "id": "leaked-id",
            },
        )

        div = soup.div
        assert not any("top" in cls for cls in div["class"])
        assert not any("error" in cls for cls in div["class"])
        assert div.get("id") is None
        content = div.find("div", class_="tooltip-content")
        assert content.get_text(strip=True) == ""
        assert content.get("id") is None


class TestTooltipBlankContentSlot:
    def test_whitespace_only_content_slot_falls_back_to_tip(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-tooltip tip="Copy link"><c-slot name="content">  </c-slot>'
            "<button>Copy</button></c-tooltip>"
        )

        content = soup.div.find("div", class_="tooltip-content")
        assert content.get_text(strip=True) == "Copy link"
