"""Tests for <c-table>'s daisyUI structure: a keyboard-focusable scrolling
wrapper named by the caption or an ``aria-label``, holding a ``<table>`` with
the zebra/pin-rows/pin-cols/size modifiers, a ``<caption>`` (attribute or
slot) as the table's first child, and the caller's content in the default
slot.
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


ROWS = "<thead><tr><th scope='col'>Name</th></tr></thead><tbody><tr><td>Ada</td></tr></tbody>"


class TestTableStructure:
    """AS1: a wrapper carrying ``overflow-x-auto`` holds a ``<table>``
    carrying ``table``, the caption renders as the table's ``<caption>``, and
    the slot content follows it inside the table."""

    def test_wrapper_holds_a_table_with_caption_then_slot_content(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            f'<c-table caption="Invoices">{ROWS}</c-table>'
        )

        wrapper = soup.find("div", class_="overflow-x-auto")
        assert wrapper is not None
        table = wrapper.find("table", class_="table", recursive=False)
        assert table is not None

        children = table.find_all(recursive=False)
        assert children[0].name == "caption"
        assert children[0].get_text(strip=True) == "Invoices"
        assert children[1].name == "thead"


class TestTableWrapperAccessibility:
    """AS2: given a caption, the wrapper is focusable by keyboard, exposed as
    a region, and named by the caption."""

    def test_wrapper_is_focusable_and_named_by_the_caption(self, cotton_render_string):
        html = cotton_render_string(f'<c-table caption="Invoices">{ROWS}</c-table>')

        wrapper_attrs = _attrs_on(html, "div")
        assert _attr_value(wrapper_attrs, "tabindex") == "0"
        assert _attr_value(wrapper_attrs, "role") == "region"

        labelledby = _attr_value(wrapper_attrs, "aria-labelledby")
        assert labelledby

        caption_attrs = _attrs_on(html, "caption")
        assert _attr_value(caption_attrs, "id") == labelledby


class TestTableAriaLabel:
    """AS3: given no caption and a caller ``aria-label``, the wrapper carries
    that label, with no ``aria-labelledby``."""

    def test_caller_aria_label_reaches_the_wrapper(self, cotton_render_string):
        html = cotton_render_string(f'<c-table aria-label="Invoices">{ROWS}</c-table>')

        wrapper_attrs = _attrs_on(html, "div")
        assert _attr_value(wrapper_attrs, "aria-label") == "Invoices"
        assert _attr_value(wrapper_attrs, "aria-labelledby") is None


class TestTableModifiers:
    """AS4: ``zebra``, ``pin-rows`` and ``pin-cols`` map to their daisyUI classes."""

    def test_zebra_adds_table_zebra(self, cotton_render_string):
        html = cotton_render_string(f"<c-table zebra>{ROWS}</c-table>")
        assert "table-zebra" in _class_attrs_on(html, "table")[0]

    def test_pin_rows_adds_table_pin_rows(self, cotton_render_string):
        html = cotton_render_string(f"<c-table pin-rows>{ROWS}</c-table>")
        assert "table-pin-rows" in _class_attrs_on(html, "table")[0]

    def test_pin_cols_adds_table_pin_cols(self, cotton_render_string):
        html = cotton_render_string(f"<c-table pin-cols>{ROWS}</c-table>")
        assert "table-pin-cols" in _class_attrs_on(html, "table")[0]


class TestTableSize:
    """AS5: ``size`` maps xs-xl to daisyUI's ``table-<size>`` class."""

    @pytest.mark.parametrize("size", ["xs", "sm", "md", "lg", "xl"])
    def test_each_size_maps_to_its_daisyui_class(self, cotton_render_string, size):
        html = cotton_render_string(f'<c-table size="{size}">{ROWS}</c-table>')
        assert f"table-{size}" in _class_attrs_on(html, "table")[0]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string
    ):
        html = cotton_render_string(f'<c-table size="xxl">{ROWS}</c-table>')
        assert "table-xxl" not in _class_attrs_on(html, "table")[0]


class TestTableClasses:
    """AS6: ``class`` merges into the wrapper's class list, ``content_class``
    into the table's."""

    def test_class_and_content_class_reach_their_own_elements(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            f'<c-table class="mt-4" content_class="w-full">{ROWS}</c-table>'
        )

        wrapper_classes = _class_attrs_on(html, "div")
        assert len(wrapper_classes) == 1
        assert "overflow-x-auto" in wrapper_classes[0]
        assert "mt-4" in wrapper_classes[0]

        table_classes = _class_attrs_on(html, "table")
        assert len(table_classes) == 1
        assert "table" in table_classes[0]
        assert "w-full" in table_classes[0]
        assert "mt-4" not in table_classes[0]


class TestTableCaptionSlot:
    """AS7: a ``caption`` slot fills the ``<caption>`` in place of the attribute."""

    def test_caption_slot_fills_the_caption(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-table><c-slot name="caption">Invoices <em>2026</em></c-slot>'
            f"{ROWS}</c-table>"
        )

        caption = soup.find("caption")
        assert caption is not None
        assert caption.find("em") is not None
        assert "Invoices" in caption.get_text()


class TestTableUniqueIds:
    """Two tables on one page get different caption ids."""

    def test_two_tables_get_different_caption_ids(self, cotton_render_string):
        html = cotton_render_string(
            f'<c-table caption="One">{ROWS}</c-table>'
            f'<c-table caption="Two">{ROWS}</c-table>'
        )

        wrappers = html.split("<div")[1:]
        assert len(wrappers) == 2
        first_id = _attr_value(
            _attrs_on("<div" + wrappers[0], "div"), "aria-labelledby"
        )
        second_id = _attr_value(
            _attrs_on("<div" + wrappers[1], "div"), "aria-labelledby"
        )

        assert first_id
        assert second_id
        assert first_id != second_id


class TestTablePageContextDoesNotLeak:
    """A page variable named ``caption`` never fills a table given no caption."""

    def test_page_context_caption_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            f"<c-table>{ROWS}</c-table>",
            context={"caption": "Leaked"},
        )

        assert soup.find("caption") is None

        wrapper = soup.find("div", class_="overflow-x-auto")
        assert wrapper.get("aria-labelledby") is None
