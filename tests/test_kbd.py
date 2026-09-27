"""Tests for <c-kbd>: daisyUI's kbd markup — a key-cap-styled ``<kbd>``
holding ``text`` then the default slot, with a ``size`` modifier.
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


class TestKbdElement:
    """FR-033: the kbd is a ``<kbd>`` carrying ``kbd``."""

    def test_renders_a_kbd_element_carrying_kbd(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-kbd>K</c-kbd>")

        kbd = soup.find("kbd", class_="kbd")
        assert kbd is not None


class TestKbdContent:
    """FR-033: ``text`` renders, then the default slot (US9-2)."""

    def test_text_attribute_is_the_kbds_content(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-kbd text="Ctrl" />')

        kbd = soup.find("kbd", class_="kbd")
        assert kbd.get_text(strip=True) == "Ctrl"

    def test_text_renders_before_the_default_slot(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-kbd text="Ctrl">+K</c-kbd>')

        kbd = soup.find("kbd", class_="kbd")
        assert kbd.get_text(strip=True) == "Ctrl+K"


class TestKbdSize:
    """FR-033: ``size`` maps xs-xl to daisyUI's ``kbd-<size>`` class (US9-1)."""

    @pytest.mark.parametrize("size", ["xs", "sm", "md", "lg", "xl"])
    def test_each_size_maps_to_its_daisyui_class(self, cotton_render_string, size):
        html = cotton_render_string(f'<c-kbd size="{size}">K</c-kbd>')

        root_classes = _class_attrs_on(html, "kbd")
        assert f"kbd-{size}" in root_classes[0]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-kbd size="xxl">K</c-kbd>')

        root_classes = _class_attrs_on(html, "kbd")
        assert "kbd-xxl" not in root_classes[0]


class TestKbdClassAndAttrs:
    """``class`` merges into the kbd's single class list, and other
    attributes reach the kbd (FR-002)."""

    def test_class_merges_and_extra_attributes_reach_the_kbd(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-kbd class="ms-1" data-test="x">K</c-kbd>')

        root_classes = _class_attrs_on(html, "kbd")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "ms-1" in root_classes[0]
        assert "kbd" in root_classes[0]

        attrs = _attrs_on(html, "kbd")
        assert _attr_value(attrs, "data-test") == "x"


class TestKbdPageContextDoesNotLeak:
    """A page variable sharing a declared name never fills an empty kbd."""

    def test_page_context_text_and_size_do_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-kbd />",
            context={"text": "Leaked", "size": "lg"},
        )

        kbd = soup.find("kbd", class_="kbd")
        assert kbd.get_text(strip=True) == ""
        assert "kbd-lg" not in (kbd.get("class") or [])
