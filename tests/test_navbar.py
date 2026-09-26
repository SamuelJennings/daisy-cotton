"""Tests for the <c-navbar> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes and named slots reach the component the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestNavbarRoot:
    """The navbar is a named navigation landmark."""

    def test_root_is_a_nav_with_the_navbar_class(self, cotton_render_string):
        nav = parse(cotton_render_string("<c-navbar>x</c-navbar>")).find("nav")
        assert nav is not None
        assert nav["class"] == ["navbar"]

    def test_caller_class_is_merged(self, cotton_render_string):
        nav = parse(cotton_render_string('<c-navbar class="mine">x</c-navbar>')).nav
        assert nav["class"] == ["navbar", "mine"]

    def test_default_name_is_main(self, cotton_render_string):
        nav = parse(cotton_render_string("<c-navbar>x</c-navbar>")).nav
        assert nav["aria-label"] == "Main"

    def test_caller_aria_label_replaces_the_default_once(self, cotton_render_string):
        html = cotton_render_string('<c-navbar aria-label="Site">x</c-navbar>')
        assert html.count("aria-label=") == 1
        assert parse(html).nav["aria-label"] == "Site"

    def test_other_attributes_reach_the_root(self, cotton_render_string):
        nav = parse(
            cotton_render_string('<c-navbar id="top" data-x="1">x</c-navbar>')
        ).nav
        assert nav["id"] == "top"
        assert nav["data-x"] == "1"

    def test_default_slot_sits_directly_inside_the_root(self, cotton_render_string):
        nav = parse(cotton_render_string("<c-navbar><p>body</p></c-navbar>")).nav
        assert nav.find("p", recursive=False).text == "body"


class TestNavbarSections:
    """Each named slot lands in its own section, emitted only when given."""

    def test_each_slot_lands_in_its_section(self, cotton_render_string):
        html = cotton_render_string(
            "<c-navbar>"
            '<c-slot name="start"><b>s</b></c-slot>'
            '<c-slot name="center"><b>c</b></c-slot>'
            '<c-slot name="end"><b>e</b></c-slot>'
            "</c-navbar>"
        )
        nav = parse(html).nav
        for section, text in (("start", "s"), ("center", "c"), ("end", "e")):
            div = nav.find("div", class_=f"navbar-{section}", recursive=False)
            assert div.b.text == text

    def test_only_the_given_sections_are_emitted(self, cotton_render_string):
        html = cotton_render_string(
            '<c-navbar><c-slot name="start">s</c-slot></c-navbar>'
        )
        nav = parse(html).nav
        assert nav.find(class_="navbar-start") is not None
        assert nav.find(class_="navbar-center") is None
        assert nav.find(class_="navbar-end") is None

    def test_no_named_slots_emits_no_sections(self, cotton_render_string):
        html = cotton_render_string("<c-navbar>x</c-navbar>")
        assert "navbar-start" not in html
        assert "navbar-center" not in html
        assert "navbar-end" not in html

    def test_an_empty_slot_emits_no_section(self, cotton_render_string):
        html = cotton_render_string(
            '<c-navbar><c-slot name="start"></c-slot>x</c-navbar>'
        )
        assert "navbar-start" not in html

    def test_a_page_variable_named_start_emits_no_section(self, cotton_render_string):
        html = cotton_render_string(
            "<c-navbar>x</c-navbar>",
            {"start": "leak", "center": "leak", "end": "leak"},
        )
        assert "leak" not in html
        assert "navbar-start" not in html

    def test_a_real_slot_wins_over_a_page_variable(self, cotton_render_string):
        html = cotton_render_string(
            '<c-navbar><c-slot name="start">mine</c-slot></c-navbar>',
            {"start": "leak"},
        )
        assert "mine" in html
        assert "leak" not in html
