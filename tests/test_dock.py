"""Tests for the <c-dock> and <c-dock.item> components.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestDockRoot:
    """The dock is a named navigation landmark carrying daisyUI's classes only."""

    def test_root_is_a_nav_with_the_dock_class(self, cotton_render_string):
        nav = parse(cotton_render_string("<c-dock>x</c-dock>")).find("nav")
        assert nav is not None
        assert nav["class"] == ["dock"]

    def test_size_and_caller_class_are_the_only_extra_classes(self, cotton_render_string):
        nav = parse(
            cotton_render_string('<c-dock size="sm" class="mine">x</c-dock>')
        ).nav
        assert nav["class"] == ["dock", "dock-sm", "mine"]

    def test_unknown_size_adds_no_class(self, cotton_render_string):
        nav = parse(cotton_render_string('<c-dock size="huge">x</c-dock>')).nav
        assert nav["class"] == ["dock"]

    def test_the_removed_backdrop_classes_are_not_emitted(self, cotton_render_string):
        html = cotton_render_string("<c-dock>x</c-dock>")
        assert "bg-transparent" not in html
        assert "backdrop-blur" not in html

    def test_other_attributes_reach_the_root(self, cotton_render_string):
        nav = parse(cotton_render_string('<c-dock id="bar" data-x="1">x</c-dock>')).nav
        assert nav["id"] == "bar"
        assert nav["data-x"] == "1"

    def test_the_slot_is_rendered_inside(self, cotton_render_string):
        nav = parse(cotton_render_string("<c-dock><b>marker</b></c-dock>")).nav
        assert nav.b.get_text() == "marker"

    def test_default_name_is_dock(self, cotton_render_string):
        nav = parse(cotton_render_string("<c-dock>x</c-dock>")).nav
        assert nav["aria-label"] == "Dock"

    def test_caller_aria_label_replaces_the_default_once(self, cotton_render_string):
        html = cotton_render_string('<c-dock aria-label="Tabs bar">x</c-dock>')
        assert html.count("aria-label=") == 1
        assert parse(html).nav["aria-label"] == "Tabs bar"
