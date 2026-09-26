"""Tests for the <c-menu> family: menu, menu.item, menu.title and menu.submenu.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestMenuRoot:
    """The menu is a bare list carrying daisyUI's menu classes only."""

    def test_bare_menu_is_a_ul_with_only_the_menu_class(self, cotton_render_string):
        ul = parse(cotton_render_string("<c-menu>x</c-menu>")).find("ul")
        assert ul is not None
        assert ul["class"] == ["menu"]

    def test_size_adds_the_size_class(self, cotton_render_string):
        ul = parse(cotton_render_string('<c-menu size="sm">x</c-menu>')).ul
        assert ul["class"] == ["menu", "menu-sm"]

    def test_size_outside_the_scale_adds_no_class(self, cotton_render_string):
        ul = parse(cotton_render_string('<c-menu size="huge">x</c-menu>')).ul
        assert ul["class"] == ["menu"]

    def test_horizontal_adds_the_direction_class(self, cotton_render_string):
        ul = parse(cotton_render_string("<c-menu horizontal>x</c-menu>")).ul
        assert ul["class"] == ["menu", "menu-horizontal"]

    def test_horizontal_with_a_breakpoint_is_responsive(self, cotton_render_string):
        ul = parse(cotton_render_string('<c-menu horizontal="lg">x</c-menu>')).ul
        assert ul["class"] == ["menu", "lg:menu-horizontal"]

    def test_no_horizontal_adds_no_direction_class(self, cotton_render_string):
        html = cotton_render_string("<c-menu>x</c-menu>")
        assert "horizontal" not in html
        assert "menu-vertical" not in html

    def test_paged_adds_menu_paged(self, cotton_render_string):
        ul = parse(cotton_render_string("<c-menu paged>x</c-menu>")).ul
        assert ul["class"] == ["menu", "menu-paged"]

    def test_not_paged_adds_no_paged_class(self, cotton_render_string):
        assert "menu-paged" not in cotton_render_string("<c-menu>x</c-menu>")

    def test_caller_class_is_merged(self, cotton_render_string):
        ul = parse(cotton_render_string('<c-menu class="mine">x</c-menu>')).ul
        assert ul["class"] == ["menu", "mine"]

    def test_other_attributes_reach_the_root(self, cotton_render_string):
        ul = parse(cotton_render_string('<c-menu id="m" data-x="1">x</c-menu>')).ul
        assert ul["id"] == "m"
        assert ul["data-x"] == "1"

    def test_slot_content_is_inside_the_list(self, cotton_render_string):
        ul = parse(cotton_render_string("<c-menu><li>one</li></c-menu>")).ul
        assert ul.find("li").text == "one"
