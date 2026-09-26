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


class TestMenuItem:
    """An item is a list item holding a link or a button."""

    def test_link_item_with_active_marks_the_link_as_current(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-menu.item href="/a" text="A" active />')
        li = parse(html).li
        a = li.a
        assert a["href"] == "/a"
        assert a["class"] == ["menu-active"]
        assert a["aria-current"] == "page"
        assert a.text.strip() == "A"
        assert not li.get("class")

    def test_link_item_that_is_not_active_has_no_active_marks(
        self, cotton_render_string
    ):
        a = parse(cotton_render_string('<c-menu.item href="/a" text="A" />')).a
        assert not a.get("class")
        assert "aria-current" not in a.attrs

    def test_item_without_href_renders_a_button(self, cotton_render_string):
        soup = parse(cotton_render_string('<c-menu.item text="Go" />'))
        button = soup.li.button
        assert button["type"] == "button"
        assert button.text.strip() == "Go"
        assert soup.find("a") is None

    def test_active_button_has_the_class_but_no_aria_current(
        self, cotton_render_string
    ):
        button = parse(cotton_render_string('<c-menu.item text="Go" active />')).button
        assert button["class"] == ["menu-active"]
        assert "aria-current" not in button.attrs

    def test_disabled_link_is_a_role_link_without_href_or_tabindex(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-menu.item href="/a" text="A" disabled />')
        li = parse(html).li
        assert li["class"] == ["menu-disabled"]
        a = li.a
        assert a["role"] == "link"
        assert a["aria-disabled"] == "true"
        assert "href" not in a.attrs
        assert "tabindex" not in a.attrs

    def test_disabled_button_uses_the_native_attribute(self, cotton_render_string):
        li = parse(cotton_render_string('<c-menu.item text="Go" disabled />')).li
        assert li["class"] == ["menu-disabled"]
        assert li.button.has_attr("disabled")
        assert "aria-disabled" not in li.button.attrs

    def test_enabled_items_carry_no_disabled_marks(self, cotton_render_string):
        html = cotton_render_string(
            '<c-menu.item href="/a" text="A" /><c-menu.item text="B" />'
        )
        assert "menu-disabled" not in html
        assert "disabled" not in html
        assert "role=" not in html

    def test_several_active_items_each_render_as_given(self, cotton_render_string):
        html = cotton_render_string(
            '<c-menu><c-menu.item href="/a" text="A" active />'
            '<c-menu.item href="/b" text="B" active />'
            '<c-menu.item href="/c" text="C" /></c-menu>'
        )
        soup = parse(html)
        assert len(soup.select("a.menu-active")) == 2
        assert len(soup.select('a[aria-current="page"]')) == 2

    def test_icon_is_rendered_and_hidden_from_assistive_tech(
        self, cotton_render_string
    ):
        a = parse(
            cotton_render_string('<c-menu.item href="/a" text="A" icon="fa fa-home" />')
        ).a
        icon = a.find("i")
        assert icon["class"][:2] == ["fa", "fa-home"]
        assert icon["aria-hidden"] == "true"

    def test_item_class_reaches_the_list_item_and_not_the_icon(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-menu.item href="/a" text="A" icon="fa fa-home" class="mine" />'
        )
        li = parse(html).li
        assert li["class"] == ["mine"]
        assert "mine" not in li.find("i")["class"]

    def test_other_attributes_land_on_the_list_item(self, cotton_render_string):
        li = parse(
            cotton_render_string('<c-menu.item href="/a" text="A" data-x="1" id="i" />')
        ).li
        assert li["data-x"] == "1"
        assert li["id"] == "i"
        assert "data-x" not in li.a.attrs

    def test_aria_label_lands_on_the_inner_link(self, cotton_render_string):
        soup = parse(
            cotton_render_string(
                '<c-menu.item href="/a" icon="fa fa-home" aria-label="Home" />'
            )
        )
        assert soup.a["aria-label"] == "Home"
        assert "aria-label" not in soup.li.attrs

    def test_aria_label_lands_on_the_inner_button(self, cotton_render_string):
        soup = parse(
            cotton_render_string('<c-menu.item icon="fa fa-home" aria-label="Home" />')
        )
        assert soup.button["aria-label"] == "Home"
        assert "aria-label" not in soup.li.attrs

    def test_no_aria_label_writes_none(self, cotton_render_string):
        assert "aria-label" not in cotton_render_string('<c-menu.item text="A" />')

    def test_slot_content_follows_the_text(self, cotton_render_string):
        a = parse(
            cotton_render_string(
                '<c-menu.item href="/a" text="A"><b>2</b></c-menu.item>'
            )
        ).a
        assert a.text.strip().replace("\n", "").replace(" ", "") == "A2"
