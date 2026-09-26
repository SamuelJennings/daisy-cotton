"""Tests for the <c-tabs> and <c-tabs.tab> components.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestTabsRoot:
    """The root carries daisyUI's tabs classes and a tablist role."""

    def test_bare_root_is_a_tablist_with_the_tabs_class(self, cotton_render_string):
        root = parse(cotton_render_string("<c-tabs>x</c-tabs>")).div
        assert root["class"] == ["tabs"]
        assert root["role"] == "tablist"

    def test_box_border_and_lift_add_their_classes(self, cotton_render_string):
        for attr, css in [
            ("box", "tabs-box"),
            ("border", "tabs-border"),
            ("lift", "tabs-lift"),
        ]:
            root = parse(cotton_render_string(f"<c-tabs {attr}>x</c-tabs>")).div
            assert css in root["class"]

    def test_style_classes_are_absent_by_default(self, cotton_render_string):
        html = cotton_render_string("<c-tabs>x</c-tabs>")
        for css in ("tabs-box", "tabs-border", "tabs-lift"):
            assert css not in html

    def test_size_adds_the_size_class(self, cotton_render_string):
        root = parse(cotton_render_string('<c-tabs size="lg">x</c-tabs>')).div
        assert "tabs-lg" in root["class"]

    def test_unknown_size_adds_no_class(self, cotton_render_string):
        root = parse(cotton_render_string('<c-tabs size="huge">x</c-tabs>')).div
        assert root["class"] == ["tabs"]

    def test_bottom_placement_adds_tabs_bottom(self, cotton_render_string):
        root = parse(cotton_render_string('<c-tabs placement="bottom">x</c-tabs>')).div
        assert "tabs-bottom" in root["class"]

    def test_top_placement_and_unknown_placement(self, cotton_render_string):
        top = parse(cotton_render_string('<c-tabs placement="top">x</c-tabs>')).div
        odd = parse(cotton_render_string('<c-tabs placement="left">x</c-tabs>')).div
        assert "tabs-bottom" not in top["class"]
        assert odd["class"] == ["tabs"]

    def test_links_drops_the_role(self, cotton_render_string):
        root = parse(cotton_render_string("<c-tabs links>x</c-tabs>")).div
        assert not root.has_attr("role")

    def test_class_and_attributes_reach_the_root(self, cotton_render_string):
        root = parse(
            cotton_render_string('<c-tabs class="mine" id="t" data-x="1">x</c-tabs>')
        ).div
        assert root["class"] == ["tabs", "mine"]
        assert root["id"] == "t"
        assert root["data-x"] == "1"

    def test_the_slot_is_rendered_inside(self, cotton_render_string):
        root = parse(cotton_render_string("<c-tabs><b>marker</b></c-tabs>")).div
        assert root.b.get_text() == "marker"
