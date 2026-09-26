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

    def test_size_and_caller_class_are_the_only_extra_classes(
        self, cotton_render_string
    ):
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


class TestDockItemLink:
    """An item with an ``href`` is a link."""

    def test_active_link_has_dock_active_and_aria_current(self, cotton_render_string):
        a = parse(
            cotton_render_string('<c-dock.item href="/" label="Home" active />')
        ).a
        assert "dock-active" in a["class"]
        assert a["aria-current"] == "page"
        assert a["href"] == "/"

    def test_inactive_link_has_neither(self, cotton_render_string):
        a = parse(cotton_render_string('<c-dock.item href="/" label="Home" />')).a
        assert "dock-active" not in a["class"]
        assert not a.has_attr("aria-current")

    def test_label_sits_in_dock_label(self, cotton_render_string):
        a = parse(cotton_render_string('<c-dock.item href="/" label="Home" />')).a
        assert a.find("span", class_="dock-label").get_text() == "Home"

    def test_no_label_emits_no_dock_label(self, cotton_render_string):
        a = parse(
            cotton_render_string(
                '<c-dock.item href="/" icon="i-home" aria-label="Home" />'
            )
        ).a
        assert a.find(class_="dock-label") is None

    def test_icon_is_hidden_from_assistive_technology(self, cotton_render_string):
        i = parse(
            cotton_render_string('<c-dock.item href="/" icon="i-home" label="Home" />')
        ).i
        assert i["aria-hidden"] == "true"
        assert "i-home" in i["class"]

    def test_item_class_does_not_reach_the_icon(self, cotton_render_string):
        i = parse(
            cotton_render_string(
                '<c-dock.item href="/" icon="i-home" class="mine" label="Home" />'
            )
        ).i
        assert "mine" not in i["class"]

    def test_icon_only_item_is_named_by_the_callers_aria_label(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-dock.item href="/" icon="i-home" aria-label="Home" />'
        )
        assert html.count("aria-label=") == 1
        assert parse(html).a["aria-label"] == "Home"


class TestDockItemButton:
    """An item with neither ``href`` nor ``toggle`` is a button."""

    def test_renders_a_button_of_type_button(self, cotton_render_string):
        button = parse(cotton_render_string('<c-dock.item label="Add" />')).button
        assert button["type"] == "button"

    def test_active_button_has_dock_active_and_no_aria_current(
        self, cotton_render_string
    ):
        button = parse(
            cotton_render_string('<c-dock.item label="Add" active />')
        ).button
        assert "dock-active" in button["class"]
        assert not button.has_attr("aria-current")

    def test_label_sits_in_dock_label(self, cotton_render_string):
        button = parse(cotton_render_string('<c-dock.item label="Add" />')).button
        assert button.find("span", class_="dock-label").get_text() == "Add"

    def test_icon_is_hidden_from_assistive_technology(self, cotton_render_string):
        i = parse(cotton_render_string('<c-dock.item icon="i-add" label="Add" />')).i
        assert i["aria-hidden"] == "true"


class TestDockItemToggle:
    """An item with ``toggle`` is a label that flips a drawer checkbox."""

    def test_renders_a_label_for_the_drawer(self, cotton_render_string):
        label = parse(
            cotton_render_string('<c-dock.item toggle="drawer" label="Menu" />')
        ).label
        assert label["for"] == "drawer"

    def test_it_is_not_a_tab_stop_and_claims_no_role(self, cotton_render_string):
        label = parse(
            cotton_render_string('<c-dock.item toggle="drawer" label="Menu" />')
        ).label
        assert not label.has_attr("tabindex")
        assert not label.has_attr("role")

    def test_aria_label_is_written_when_a_label_is_given(self, cotton_render_string):
        label = parse(
            cotton_render_string('<c-dock.item toggle="drawer" label="Menu" />')
        ).label
        assert label["aria-label"] == "Menu"

    def test_no_label_means_no_aria_label_of_its_own(self, cotton_render_string):
        html = cotton_render_string('<c-dock.item toggle="drawer" icon="i-menu" />')
        assert not parse(html).label.has_attr("aria-label")

    def test_icon_only_toggle_takes_the_callers_aria_label(self, cotton_render_string):
        html = cotton_render_string(
            '<c-dock.item toggle="drawer" icon="i-menu" aria-label="Open menu" />'
        )
        assert html.count("aria-label=") == 1
        assert parse(html).label["aria-label"] == "Open menu"

    def test_active_toggle_has_dock_active_and_no_aria_current(
        self, cotton_render_string
    ):
        label = parse(
            cotton_render_string('<c-dock.item toggle="drawer" label="Menu" active />')
        ).label
        assert "dock-active" in label["class"]
        assert not label.has_attr("aria-current")


class TestDockItemPageContext:
    """Page variables named like props never reach a plain dock item."""

    def test_page_active_does_not_mark_an_item_current(self, cotton_render_string):
        button = parse(
            cotton_render_string('<c-dock.item label="A" />', {"active": "x"})
        ).button
        assert "dock-active" not in button["class"]

    def test_page_href_does_not_turn_an_item_into_a_link(self, cotton_render_string):
        soup = parse(cotton_render_string('<c-dock.item label="A" />', {"href": "/leak"}))
        assert soup.a is None
        assert soup.button is not None

    def test_page_toggle_does_not_turn_an_item_into_a_label(self, cotton_render_string):
        soup = parse(
            cotton_render_string('<c-dock.item label="A" />', {"toggle": "drawer"})
        )
        assert soup.label is None
        assert soup.button is not None


class TestDockItemToggleIcon:
    """The toggle's icon is decorative and does not inherit the item's class."""

    def test_icon_is_hidden_from_assistive_technology(self, cotton_render_string):
        html = cotton_render_string(
            '<c-dock.item toggle="drawer" icon="i-menu" aria-label="Open menu" />'
        )
        assert parse(html).label.find("i")["aria-hidden"] == "true"

    def test_the_items_class_does_not_reach_the_icon(self, cotton_render_string):
        html = cotton_render_string(
            '<c-dock.item toggle="drawer" icon="i-menu" class="mine" label="Menu" />'
        )
        label = parse(html).label
        assert "mine" in label["class"]
        assert "mine" not in label.find("i")["class"]
