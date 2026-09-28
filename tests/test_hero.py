"""``<c-hero>``: the hero container, with an optional overlay."""

from html.parser import HTMLParser
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

HERO = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "hero.html"
)


class _RootAttrs(HTMLParser):
    """Every attribute on the first start tag, duplicates included."""

    def __init__(self):
        super().__init__()
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None:
            self.attrs = attrs


def root_attributes(html):
    parser = _RootAttrs()
    parser.feed(html)
    return parser.attrs


def root(soup):
    return soup.find(class_="hero")


class TestHeroStructure:
    def test_the_root_is_a_hero_and_the_slot_is_inside_hero_content(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-hero><h1>Hello</h1><p>Copy</p></c-hero>")

        content = root(soup).find(class_="hero-content")
        assert content.parent is root(soup)
        assert content.find("h1").get_text() == "Hello"
        assert content.find("p").get_text() == "Copy"

    def test_the_content_is_only_inside_hero_content(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-hero><h1>Hello</h1></c-hero>")

        assert [c.name for c in root(soup).find_all(recursive=False)] == ["div"]

    def test_class_and_attributes_reach_the_root_once(self, cotton_render_string):
        html = cotton_render_string(
            '<c-hero class="min-h-screen" data-x="1">Hi</c-hero>'
        )

        names = [name for name, _ in root_attributes(html)]
        assert names.count("class") == 1
        assert "min-h-screen" in html
        assert 'data-x="1"' in html

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string("<c-hero overlay>Hi</c-hero>")

        assert "<script" not in html
        assert " on" not in html.replace("\n", " ").split(">")[0]


class TestHeroOverlay:
    def test_overlay_adds_a_hidden_overlay_before_the_content(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-hero overlay><h1>Hello</h1></c-hero>")

        children = root(soup).find_all(recursive=False)
        assert [c["class"] for c in children] == [["hero-overlay"], ["hero-content"]]
        assert children[0]["aria-hidden"] == "true"

    def test_no_overlay_gives_none(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-hero><h1>Hello</h1></c-hero>")

        assert soup.find(class_="hero-overlay") is None


class TestHeroBackground:
    def test_a_style_attribute_reaches_the_root_unchanged(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-hero style="background-image: url(x.jpg)">Hi</c-hero>'
        )

        assert root(soup)["style"] == "background-image: url(x.jpg)"


class TestHeroIgnoresPageContext:
    def test_page_context_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-hero>Hi</c-hero>", {"overlay": True})

        assert soup.find(class_="hero-overlay") is None


class TestHeroAnnotations:
    @pytest.fixture
    def parsed(self):
        return AnnotationParser().parse(HERO.read_text())

    def test_overlay_is_a_toggle(self, parsed):
        prop = next(p for p in parsed.props if p.clean_name == "overlay")

        assert prop.type == "boolean"

    def test_class_is_documented(self, parsed):
        assert "class" in {p.clean_name for p in parsed.props}

    def test_the_default_slot_holds_a_heading_copy_and_a_button(self, parsed):
        assert len(parsed.slots) == 1
        content = parsed.slots[0].content
        assert "<h1" in content
        assert "<p" in content
        assert "btn" in content
