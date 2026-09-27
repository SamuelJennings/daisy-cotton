"""``<c-join>``: grouped, directional children with a group role."""

from html.parser import HTMLParser
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

JOIN = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "join.html"
)


class _RootAttrs(HTMLParser):
    """Every attribute name on the first start tag, duplicates included."""

    def __init__(self):
        super().__init__()
        self.names = None

    def handle_starttag(self, tag, attrs):
        if self.names is None:
            self.names = [name for name, _ in attrs]


def root_attribute_names(html):
    parser = _RootAttrs()
    parser.feed(html)
    return parser.names


def root(soup):
    return soup.find("div")


class TestJoinRoot:
    def test_the_root_is_a_join_group(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-join>Body</c-join>")

        assert "join" in root(soup)["class"]
        assert root(soup)["role"] == "group"

    def test_a_bare_join_has_no_direction_modifier(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-join />")

        assert root(soup)["class"] == ["join"]

    def test_the_callers_aria_label_reaches_the_root(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-join aria-label="Pages" />')

        assert root(soup)["aria-label"] == "Pages"

    def test_class_is_merged_into_one_class_attribute(self, cotton_render_string):
        html = cotton_render_string('<c-join class="my-4" data-x="1" />')

        assert root_attribute_names(html).count("class") == 1
        assert "my-4" in html
        assert 'data-x="1"' in html

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string("<c-join><c-button>A</c-button></c-join>")

        assert "<script" not in html
        assert " on" not in html.replace("\n", " ").split(">")[0]


class TestJoinDirection:
    def test_vertical_emits_join_vertical(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-join vertical />")

        assert "join-vertical" in root(soup)["class"]
        assert "join-horizontal" not in root(soup)["class"]

    def test_horizontal_emits_join_horizontal(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-join horizontal />")

        assert "join-horizontal" in root(soup)["class"]
        assert "join-vertical" not in root(soup)["class"]

    def test_vertical_with_a_horizontal_breakpoint(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-join vertical horizontal="lg" />')

        assert "join-vertical" in root(soup)["class"]
        assert "lg:join-horizontal" in root(soup)["class"]
        assert "join-horizontal" not in root(soup)["class"]

    def test_vertical_takes_a_breakpoint(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-join vertical="md" />')

        assert "md:join-vertical" in root(soup)["class"]

    def test_an_unknown_breakpoint_adds_no_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-join horizontal="huge" vertical="left" />')

        assert root(soup)["class"] == ["join"]


class TestJoinChildren:
    def test_buttons_are_direct_children_carrying_join_item(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-join>"
            '<c-button class="join-item">One</c-button>'
            '<c-button class="join-item">Two</c-button>'
            '<c-button class="join-item">Three</c-button>'
            "</c-join>"
        )

        children = root(soup).find_all(recursive=False)
        assert len(children) == 3
        assert all("join-item" in child["class"] for child in children)

    def test_an_input_and_a_button_are_direct_children(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-join>"
            '<input class="join-item input" placeholder="Email">'
            '<c-button class="join-item">Subscribe</c-button>'
            "</c-join>"
        )

        children = root(soup).find_all(recursive=False)
        assert [child.name for child in children] == ["input", "button"]
        assert all("join-item" in child["class"] for child in children)


class TestJoinRole:
    def test_a_caller_role_replaces_group_once(self, cotton_render_string):
        html = cotton_render_string('<c-join role="toolbar" />')

        assert root_attribute_names(html).count("role") == 1
        assert 'role="toolbar"' in html
        assert 'role="group"' not in html

    def test_the_default_role_is_written_once(self, cotton_render_string):
        html = cotton_render_string("<c-join />")

        assert root_attribute_names(html).count("role") == 1


class TestJoinIgnoresPageContext:
    """Declared names default to empty, so a page's own variables of the same
    name do not rewrite the join (D9)."""

    def test_page_context_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-join />",
            {"role": "banner", "horizontal": True, "vertical": True},
        )

        assert root(soup)["role"] == "group"
        assert root(soup)["class"] == ["join"]


class TestJoinAnnotations:
    @pytest.fixture
    def parsed(self):
        return AnnotationParser().parse(JOIN.read_text())

    @pytest.mark.parametrize("name", ["horizontal", "vertical"])
    def test_direction_props_are_toggles_that_name_the_breakpoint_form(
        self, parsed, name
    ):
        prop = next(p for p in parsed.props if p.clean_name == name)

        assert prop.type == "boolean"
        assert "breakpoint" in prop.description

    def test_role_and_class_are_documented(self, parsed):
        props = {p.clean_name: p for p in parsed.props}

        assert {"role", "class"} <= set(props)
        assert "group" in props["role"].description

    def test_the_default_slot_holds_three_join_item_buttons(self, parsed):
        assert len(parsed.slots) == 1
        assert parsed.slots[0].content.count("join-item") == 3
