"""``<c-drawer>`` and ``<c-drawer.button>``: the sidebar and its opener."""

from html.parser import HTMLParser
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

DRAWER_DIR = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "drawer"
)


class _Attrs(HTMLParser):
    """Attributes of every start tag, duplicates included, in document order."""

    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, [name for name, _ in attrs], dict(attrs)))


def parse_tags(html):
    parser = _Attrs()
    parser.feed(html)
    return parser.tags


def root(soup):
    return soup.find(class_="drawer")


DRAWER = (
    '<c-drawer id="nav">'
    "<p>Page</p>"
    '<c-slot name="side"><ul><li>Item</li></ul></c-slot>'
    "</c-drawer>"
)


class TestDrawerStructure:
    def test_root_holds_toggle_content_and_side_in_order(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(DRAWER)

        children = root(soup).find_all(recursive=False)
        assert [c.name for c in children] == ["input", "div", "div"]
        assert children[0]["type"] == "checkbox"
        assert children[0]["class"] == ["drawer-toggle"]
        assert children[1]["class"] == ["drawer-content"]
        assert children[2]["class"] == ["drawer-side"]

    def test_the_toggle_carries_the_id_and_the_root_does_not(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(DRAWER)

        assert root(soup).find("input")["id"] == "nav"
        assert not root(soup).has_attr("id")

    def test_the_default_slot_is_the_page(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(DRAWER)

        assert root(soup).find(class_="drawer-content").find("p").get_text() == "Page"

    def test_the_overlay_comes_first_in_the_side_and_points_at_the_toggle(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(DRAWER)

        side = root(soup).find(class_="drawer-side")
        first = side.find_all(recursive=False)[0]
        assert first.name == "label"
        assert first["for"] == "nav"
        assert first["class"] == ["drawer-overlay"]
        assert side.find("ul") is not None

    def test_class_is_merged_and_attributes_reach_the_root_once(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-drawer id="nav" class="my-2" data-x="1" />')

        tag, names, attrs = parse_tags(html)[0]
        assert names.count("class") == 1
        assert "my-2" in attrs["class"]
        assert attrs["data-x"] == "1"

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string(DRAWER)

        assert "<script" not in html
        assert all(
            not name.startswith("on")
            for _, names, _ in parse_tags(html)
            for name in names
        )


class TestDrawerModifiers:
    def test_open_takes_a_breakpoint(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-drawer id="nav" open="lg" />')

        assert "lg:drawer-open" in root(soup)["class"]
        assert "drawer-open" not in root(soup)["class"]

    def test_bare_open_emits_drawer_open(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-drawer id="nav" open />')

        assert "drawer-open" in root(soup)["class"]

    def test_an_unknown_open_value_adds_nothing(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-drawer id="nav" open="huge" />')

        assert root(soup)["class"] == ["drawer"]

    def test_placement_end_emits_drawer_end(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-drawer id="nav" placement="end" />')

        assert "drawer-end" in root(soup)["class"]

    def test_an_unknown_placement_adds_nothing(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-drawer id="nav" placement="start" />')

        assert root(soup)["class"] == ["drawer"]


class TestTwoDrawersOnOnePage:
    def test_each_overlay_matches_its_own_checkbox_and_ids_are_unique(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-drawer id="a">One</c-drawer><c-drawer id="b">Two</c-drawer>'
        )

        drawers = soup.find_all(class_="drawer")
        pairs = [
            (d.find("input")["id"], d.find(class_="drawer-overlay")["for"])
            for d in drawers
        ]
        assert pairs == [("a", "a"), ("b", "b")]
        ids = [tag["id"] for tag in soup.find_all(id=True)]
        assert len(ids) == len(set(ids))


class TestDrawerIgnoresPageContext:
    """Declared names default to empty, so a page's own variables of the same
    name do not rewrite the drawer (D9)."""

    def test_page_context_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-drawer id="nav" />',
            {"open": True, "placement": "end"},
        )

        assert root(soup)["class"] == ["drawer"]
