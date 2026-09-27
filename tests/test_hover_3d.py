"""Tests for the <c-hover-3d> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


SLOT = '<figure><img src="/a.jpg" alt="A"></figure>'


class TestHover3dStructure:
    """Scenarios 1-2: the slot content first, then exactly eight empty
    hidden zones, nine element children in all.
    """

    def test_root_has_nine_element_children(self, cotton_render_string):
        html = cotton_render_string(f"<c-hover-3d>{SLOT}</c-hover-3d>")
        root = parse(html).find(class_="hover-3d")
        assert len(root.find_all(recursive=False)) == 9

    def test_slot_content_is_the_first_child(self, cotton_render_string):
        html = cotton_render_string(f"<c-hover-3d>{SLOT}</c-hover-3d>")
        root = parse(html).find(class_="hover-3d")
        first = root.find_all(recursive=False)[0]
        assert first.name == "figure"
        assert first.img["alt"] == "A"

    def test_next_eight_children_are_empty_divs_hidden_from_assistive_technology(
        self, cotton_render_string
    ):
        html = cotton_render_string(f"<c-hover-3d>{SLOT}</c-hover-3d>")
        root = parse(html).find(class_="hover-3d")
        zones = root.find_all(recursive=False)[1:]
        assert len(zones) == 8
        for zone in zones:
            assert zone.name == "div"
            assert zone["aria-hidden"] == "true"
            assert len(zone.find_all(recursive=False)) == 0
            assert zone.get_text(strip=True) == ""

    def test_whitespace_around_the_slot_does_not_change_the_child_count(
        self, cotton_render_string
    ):
        html = cotton_render_string(f"<c-hover-3d>\n  {SLOT}\n</c-hover-3d>")
        root = parse(html).find(class_="hover-3d")
        assert len(root.find_all(recursive=False)) == 9
        assert root.find_all(recursive=False)[0].name == "figure"


class TestHover3dElement:
    """Scenario 3: href switches the root element and carries the href."""

    def test_href_renders_an_a_carrying_the_href_and_hover_3d_class(
        self, cotton_render_string
    ):
        html = cotton_render_string(f'<c-hover-3d href="/cards/1">{SLOT}</c-hover-3d>')
        root = parse(html).find(class_="hover-3d")
        assert root.name == "a"
        assert root["href"] == "/cards/1"

    def test_no_href_renders_a_div_with_no_href_attribute(self, cotton_render_string):
        html = cotton_render_string(f"<c-hover-3d>{SLOT}</c-hover-3d>")
        root = parse(html).find(class_="hover-3d")
        assert root.name == "div"
        assert not root.has_attr("href")


class TestHover3dClassAndAttrs:
    """`class` merges into the root and further attributes spread onto it."""

    def test_root_carries_hover_3d_class_and_the_callers_class(
        self, cotton_render_string
    ):
        html = cotton_render_string(f'<c-hover-3d class="max-w-60">{SLOT}</c-hover-3d>')
        root = parse(html).find(class_="hover-3d")
        assert root["class"] == ["hover-3d", "max-w-60"]

    def test_undeclared_attributes_spread_onto_the_root(self, cotton_render_string):
        html = cotton_render_string(f'<c-hover-3d data-id="7">{SLOT}</c-hover-3d>')
        root = parse(html).find(class_="hover-3d")
        assert root["data-id"] == "7"


class TestHover3dPageContext:
    """A page variable named href never leaks into the component (research R5)."""

    def test_page_href_does_not_leak(self, cotton_render_string):
        html = cotton_render_string(
            f"<c-hover-3d>{SLOT}</c-hover-3d>", {"href": "/leaked"}
        )
        root = parse(html).find(class_="hover-3d")
        assert root.name == "div"
        assert not root.has_attr("href")
