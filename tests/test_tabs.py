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


class TestTabLink:
    """A tab given an ``href`` is a link."""

    def test_link_tab_carries_href_and_the_tab_class(self, cotton_render_string):
        a = parse(cotton_render_string('<c-tabs.tab href="/a" text="A" />')).a
        assert a["href"] == "/a"
        assert a["class"] == ["tab"]
        assert a.get_text(strip=True) == "A"

    def test_active_link_is_marked_current(self, cotton_render_string):
        a = parse(cotton_render_string('<c-tabs.tab href="/a" text="A" active />')).a
        assert "tab-active" in a["class"]
        assert a["aria-current"] == "page"

    def test_inactive_link_has_neither_marker(self, cotton_render_string):
        a = parse(cotton_render_string('<c-tabs.tab href="/a" text="A" />')).a
        assert "tab-active" not in a["class"]
        assert not a.has_attr("aria-current")

    def test_disabled_link_is_an_announced_disabled_link_without_href(
        self, cotton_render_string
    ):
        a = parse(cotton_render_string('<c-tabs.tab href="/a" text="A" disabled />')).a
        assert "tab-disabled" in a["class"]
        assert a["role"] == "link"
        assert a["aria-disabled"] == "true"
        assert not a.has_attr("href")
        assert not a.has_attr("tabindex")

    def test_enabled_link_has_no_role_or_aria_disabled(self, cotton_render_string):
        a = parse(cotton_render_string('<c-tabs.tab href="/a" text="A" />')).a
        assert not a.has_attr("role")
        assert not a.has_attr("aria-disabled")

    def test_class_and_attributes_reach_the_link(self, cotton_render_string):
        a = parse(
            cotton_render_string(
                '<c-tabs.tab href="/a" text="A" class="mine" data-x="1" />'
            )
        ).a
        assert a["class"] == ["tab", "mine"]
        assert a["data-x"] == "1"

    def test_the_slot_follows_the_text(self, cotton_render_string):
        a = parse(
            cotton_render_string('<c-tabs.tab href="/a" text="A"><b>m</b></c-tabs.tab>')
        ).a
        assert a.b.get_text() == "m"


class TestTabButton:
    """A tab with neither ``href`` nor ``name`` is a button with the tab role."""

    def test_button_tab_shape(self, cotton_render_string):
        b = parse(cotton_render_string('<c-tabs.tab text="A" />')).button
        assert b["type"] == "button"
        assert b["role"] == "tab"
        assert b["class"] == ["tab"]
        assert b.get_text(strip=True) == "A"

    def test_selected_state_follows_active(self, cotton_render_string):
        on = parse(cotton_render_string('<c-tabs.tab text="A" active />')).button
        off = parse(cotton_render_string('<c-tabs.tab text="A" />')).button
        assert on["aria-selected"] == "true"
        assert "tab-active" in on["class"]
        assert off["aria-selected"] == "false"
        assert "tab-active" not in off["class"]

    def test_disabled_button_is_natively_disabled(self, cotton_render_string):
        b = parse(cotton_render_string('<c-tabs.tab text="A" disabled />')).button
        assert b.has_attr("disabled")
        assert "tab-disabled" in b["class"]

    def test_enabled_button_is_not_disabled(self, cotton_render_string):
        b = parse(cotton_render_string('<c-tabs.tab text="A" />')).button
        assert not b.has_attr("disabled")
        assert "tab-disabled" not in b["class"]

    def test_class_and_attributes_reach_the_button(self, cotton_render_string):
        b = parse(
            cotton_render_string('<c-tabs.tab text="A" class="mine" data-x="1" />')
        ).button
        assert b["class"] == ["tab", "mine"]
        assert b["data-x"] == "1"


class TestTabRadio:
    """A tab given a ``name`` is a radio input followed by its panel."""

    SET = (
        '<c-tabs><c-tabs.tab name="g" text="One" active>panel one</c-tabs.tab>'
        '<c-tabs.tab name="g" text="Two">panel two</c-tabs.tab>'
        '<c-tabs.tab name="g" text="Three" disabled>panel three</c-tabs.tab></c-tabs>'
    )

    def test_each_tab_is_a_radio_sharing_the_name_with_its_label(
        self, cotton_render_string
    ):
        root = parse(cotton_render_string(self.SET)).div
        inputs = root.find_all("input")
        assert [i["type"] for i in inputs] == ["radio"] * 3
        assert {i["name"] for i in inputs} == {"g"}
        assert all("tab" in i["class"] for i in inputs)
        assert [i["aria-label"] for i in inputs] == ["One", "Two", "Three"]

    def test_each_input_is_immediately_followed_by_its_panel(
        self, cotton_render_string
    ):
        inputs = parse(cotton_render_string(self.SET)).find_all("input")
        panels = []
        for i in inputs:
            panel = i.find_next_sibling()
            assert panel.name == "div"
            assert panel["class"] == ["tab-content"]
            panels.append(panel.get_text(strip=True))
        assert panels == ["panel one", "panel two", "panel three"]

    def test_active_checks_exactly_that_input(self, cotton_render_string):
        inputs = parse(cotton_render_string(self.SET)).find_all("input")
        assert [i.has_attr("checked") for i in inputs] == [True, False, False]

    def test_disabled_input_is_natively_disabled(self, cotton_render_string):
        inputs = parse(cotton_render_string(self.SET)).find_all("input")
        assert [i.has_attr("disabled") for i in inputs] == [False, False, True]

    def test_root_keeps_the_tablist_role(self, cotton_render_string):
        assert parse(cotton_render_string(self.SET)).div["role"] == "tablist"

    def test_class_and_attributes_reach_the_input(self, cotton_render_string):
        i = parse(
            cotton_render_string(
                '<c-tabs.tab name="g" text="A" class="mine" data-x="1" />'
            )
        ).input
        assert i["class"] == ["tab", "mine"]
        assert i["data-x"] == "1"

    def test_a_name_in_the_page_context_does_not_make_a_button_tab_a_radio(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-tabs.tab text="A" />', context={"name": "leaked"}
        )
        soup = parse(html)
        assert soup.find("input") is None
        assert soup.button["role"] == "tab"


class TestTabsPageContext:
    """Page variables named like props never reach a plain tabs row or tab."""

    def test_page_links_does_not_drop_the_tablist_role(self, cotton_render_string):
        root = parse(cotton_render_string("<c-tabs>x</c-tabs>", {"links": True})).div
        assert root["role"] == "tablist"

    def test_page_active_does_not_mark_a_tab_current(self, cotton_render_string):
        button = parse(
            cotton_render_string('<c-tabs.tab text="A" />', {"active": "x"})
        ).button
        assert "tab-active" not in button["class"]
        assert button["aria-selected"] == "false"

    def test_page_disabled_does_not_disable_a_tab(self, cotton_render_string):
        button = parse(
            cotton_render_string('<c-tabs.tab text="A" />', {"disabled": True})
        ).button
        assert "tab-disabled" not in button["class"]
        assert button.get("disabled") is None

    def test_page_href_does_not_turn_a_tab_into_a_link(self, cotton_render_string):
        soup = parse(cotton_render_string('<c-tabs.tab text="A" />', {"href": "/leak"}))
        assert soup.a is None
        assert soup.button is not None
