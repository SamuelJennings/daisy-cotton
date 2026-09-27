"""``<c-divider>``: direction, colour, label placement, label and role."""

from html.parser import HTMLParser

from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

DIVIDER = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "divider.html"
)

COLOURS = [
    "neutral",
    "primary",
    "secondary",
    "accent",
    "info",
    "success",
    "warning",
    "error",
]


def classes(soup):
    return soup.find("div")["class"]


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


class TestDividerDirection:
    def test_a_bare_divider_has_no_direction_modifier(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-divider />")

        assert "divider" in classes(soup)
        assert "divider-horizontal" not in classes(soup)
        assert "divider-vertical" not in classes(soup)

    def test_horizontal_emits_divider_horizontal(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-divider horizontal />")

        assert "divider-horizontal" in classes(soup)
        assert "divider-vertical" not in classes(soup)

    def test_vertical_emits_divider_vertical(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-divider vertical />")

        assert "divider-vertical" in classes(soup)
        assert "divider-horizontal" not in classes(soup)

    def test_horizontal_takes_a_breakpoint(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-divider horizontal="md" />')

        assert "md:divider-horizontal" in classes(soup)
        assert "divider-horizontal" not in classes(soup)

    def test_vertical_takes_a_breakpoint(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-divider vertical="lg" />')

        assert "lg:divider-vertical" in classes(soup)

    def test_a_value_that_is_not_a_breakpoint_adds_no_modifier(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-divider horizontal="true" vertical="left" />'
        )

        assert not any(
            c.startswith(("divider-", "true:", "left:")) for c in classes(soup)
        )


class TestDividerVariant:
    @pytest.mark.parametrize("colour", COLOURS)
    def test_each_colour_emits_its_modifier(self, cotton_render_string_soup, colour):
        soup = cotton_render_string_soup(f'<c-divider variant="{colour}" />')

        assert f"divider-{colour}" in classes(soup)

    def test_an_unknown_variant_adds_no_modifier(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-divider variant="magenta" />')

        assert classes(soup) == ["divider"]


class TestDividerPlacement:
    @pytest.mark.parametrize("placement", ["start", "end"])
    def test_a_placement_emits_its_modifier(self, cotton_render_string_soup, placement):
        soup = cotton_render_string_soup(
            f'<c-divider placement="{placement}">OR</c-divider>'
        )

        assert f"divider-{placement}" in classes(soup)

    def test_an_unknown_placement_adds_no_modifier(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-divider placement="middle">OR</c-divider>')

        assert classes(soup) == ["divider"]

    def test_position_is_no_longer_a_placement(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-divider position="start">OR</c-divider>')

        assert "divider-start" not in classes(soup)


class TestDividerLabel:
    def test_text_renders_before_the_slot(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-divider text="OR">and more</c-divider>')

        assert soup.find("div").get_text().strip() == "ORand more"

    def test_the_default_slot_is_the_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-divider>OR</c-divider>")

        assert soup.find("div").get_text() == "OR"

    def test_a_label_slot_is_not_rendered(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-divider><c-slot name='label'>Gone</c-slot></c-divider>"
        )

        assert "Gone" not in soup.get_text()


class TestDividerRootAttributes:
    def test_class_is_merged_into_one_class_attribute(self, cotton_render_string):
        html = cotton_render_string('<c-divider class="my-8" data-x="1" />')

        names = root_attribute_names(html)
        assert names.count("class") == 1
        assert "my-8" in html
        assert 'data-x="1"' in html

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string("<c-divider>OR</c-divider>")

        assert "<script" not in html
        assert " on" not in html.replace("\n", " ").split(">")[0]


class TestDividerRole:
    def test_an_unlabelled_divider_is_a_separator(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-divider />")

        assert soup.find("div")["role"] == "separator"

    def test_a_whitespace_only_slot_counts_as_unlabelled(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-divider>   \n  </c-divider>")

        assert soup.find("div")["role"] == "separator"

    def test_a_bare_horizontal_divider_says_it_is_vertical(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-divider horizontal />")

        assert soup.find("div")["aria-orientation"] == "vertical"

    def test_a_responsive_horizontal_divider_has_no_orientation(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-divider horizontal="md" />')

        assert soup.find("div")["role"] == "separator"
        assert not soup.find("div").has_attr("aria-orientation")

    def test_a_plain_unlabelled_divider_has_no_orientation(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-divider />")

        assert not soup.find("div").has_attr("aria-orientation")

    def test_text_removes_the_role(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-divider text="OR" />')

        assert not soup.find("div").has_attr("role")
        assert "OR" in soup.get_text()

    def test_a_slot_label_removes_the_role(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-divider>OR</c-divider>")

        assert not soup.find("div").has_attr("role")

    def test_a_labelled_horizontal_divider_has_no_orientation(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-divider horizontal>OR</c-divider>")

        assert not soup.find("div").has_attr("aria-orientation")

    def test_a_caller_role_replaces_the_default_once(self, cotton_render_string):
        html = cotton_render_string('<c-divider role="none" />')

        assert root_attribute_names(html).count("role") == 1
        assert 'role="none"' in html
        assert 'role="separator"' not in html

    def test_a_caller_role_on_a_labelled_divider_is_written_once(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-divider role="heading">OR</c-divider>')

        assert root_attribute_names(html).count("role") == 1
        assert 'role="heading"' in html


class TestDividerIgnoresPageContext:
    """Declared names default to empty, so a page's own variables of the same
    name do not rewrite the divider (D9)."""

    def test_page_context_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-divider />",
            {
                "role": "banner",
                "text": "Leaked",
                "variant": "error",
                "placement": "end",
            },
        )

        div = soup.find("div")
        assert div["role"] == "separator"
        assert classes(soup) == ["divider"]
        assert "Leaked" not in soup.get_text()


class TestDividerAnnotations:
    @pytest.fixture
    def parsed(self):
        return AnnotationParser().parse(DIVIDER.read_text())

    def test_variant_offers_the_eight_colours(self, parsed):
        prop = next(p for p in parsed.props if p.clean_name == "variant")

        assert prop.type == "select"
        assert list(prop.options) == COLOURS

    def test_placement_offers_start_and_end(self, parsed):
        prop = next(p for p in parsed.props if p.clean_name == "placement")

        assert prop.type == "select"
        assert list(prop.options) == ["start", "end"]

    @pytest.mark.parametrize("name", ["horizontal", "vertical"])
    def test_direction_props_are_toggles_that_name_the_breakpoint_form(
        self, parsed, name
    ):
        prop = next(p for p in parsed.props if p.clean_name == name)

        assert prop.type == "boolean"
        assert "breakpoint" in prop.description

    def test_the_old_position_prop_is_gone(self, parsed):
        assert "position" not in {p.clean_name for p in parsed.props}

    def test_text_role_and_class_are_documented(self, parsed):
        assert {"text", "role", "class"} <= {p.clean_name for p in parsed.props}

    def test_the_default_slot_is_the_only_slot(self, parsed):
        assert len(parsed.slots) == 1
