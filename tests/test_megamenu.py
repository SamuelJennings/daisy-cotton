"""Tests for the <c-megamenu> and <c-megamenu.item> components.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestMegamenuRoot:
    """The root is a popover navigation landmark with a small-screen toggle."""

    def test_root_is_a_popover_nav_with_the_id(self, cotton_render_string):
        nav = parse(cotton_render_string('<c-megamenu id="mm">x</c-megamenu>')).nav
        assert nav["id"] == "mm"
        assert nav.has_attr("popover")
        assert nav["class"][:2] == ["megamenu", "max-sm:megamenu-vertical"]

    def test_root_holds_the_active_indicator_and_the_slot(self, cotton_render_string):
        nav = parse(
            cotton_render_string('<c-megamenu id="mm"><b>marker</b></c-megamenu>')
        ).nav
        assert nav.find("span", class_="megamenu-active") is not None
        assert nav.b.get_text() == "marker"

    def test_wide_and_full_add_their_classes(self, cotton_render_string):
        wide = parse(cotton_render_string('<c-megamenu id="mm" wide>x</c-megamenu>')).nav
        full = parse(cotton_render_string('<c-megamenu id="mm" full>x</c-megamenu>')).nav
        assert "megamenu-wide" in wide["class"]
        assert "megamenu-full" in full["class"]

    def test_wide_and_full_are_absent_by_default(self, cotton_render_string):
        html = cotton_render_string('<c-megamenu id="mm">x</c-megamenu>')
        assert "megamenu-wide" not in html
        assert "megamenu-full" not in html

    def test_size_adds_the_size_class_and_unknown_size_none(self, cotton_render_string):
        md = parse(cotton_render_string('<c-megamenu id="mm" size="md">x</c-megamenu>')).nav
        odd = parse(cotton_render_string('<c-megamenu id="mm" size="huge">x</c-megamenu>')).nav
        assert "megamenu-md" in md["class"]
        assert not any(c.startswith("megamenu-h") for c in odd["class"])

    def test_class_and_attributes_reach_the_root(self, cotton_render_string):
        nav = parse(
            cotton_render_string('<c-megamenu id="mm" class="mine" data-x="1">x</c-megamenu>')
        ).nav
        assert "mine" in nav["class"]
        assert nav["data-x"] == "1"

    def test_default_name_is_site(self, cotton_render_string):
        nav = parse(cotton_render_string('<c-megamenu id="mm">x</c-megamenu>')).nav
        assert nav["aria-label"] == "Site"

    def test_caller_aria_label_replaces_the_default_once(self, cotton_render_string):
        html = cotton_render_string('<c-megamenu id="mm" aria-label="Shop">x</c-megamenu>')
        assert html.count("aria-label=") == 1
        assert parse(html).nav["aria-label"] == "Shop"


class TestMegamenuToggle:
    """The toggle is a button, rendered through the button component."""

    def test_toggle_is_a_button_hidden_from_small_up_and_pointing_at_the_id(
        self, cotton_render_string
    ):
        button = parse(cotton_render_string('<c-megamenu id="mm">x</c-megamenu>')).button
        assert button is not None
        assert button["type"] == "button"
        assert button["popovertarget"] == "mm"
        assert "sm:hidden" in button["class"]
        assert "btn" in button["class"]
        assert button.get_text(strip=True) == "Menu"

    def test_toggle_stays_a_plain_button_when_the_megamenu_is_full_or_sized(
        self, cotton_render_string
    ):
        for attrs in ("full", 'size="md"', "full size='md'"):
            html = cotton_render_string(f'<c-megamenu id="mm" {attrs}>x</c-megamenu>')
            button = parse(html).button
            assert button.name == "button"
            assert "btn-block" not in button["class"]
            assert "btn-md" not in button["class"]

    def test_toggle_stays_a_button_when_the_page_context_has_an_href(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-megamenu id="mm">x</c-megamenu>', context={"href": "/somewhere"}
        )
        soup = parse(html)
        assert soup.button is not None
        assert soup.find("a") is None
