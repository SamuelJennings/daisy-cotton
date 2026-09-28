"""``<c-indicator>`` and ``<c-indicator.item>``: a badge pinned to a corner."""

from html.parser import HTMLParser
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

INDICATOR_DIR = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "indicator"
)

CORNERS = [
    f"{row} {column}"
    for row in ("top", "middle", "bottom")
    for column in ("start", "center", "end")
]

PLACEMENT_WORDS = ("start", "center", "end", "top", "middle", "bottom")


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
    return soup.find(class_="indicator")


def placement_classes(element):
    return {f"indicator-{word}" for word in PLACEMENT_WORDS} & set(element["class"])


BADGE = '<c-indicator.item class="badge badge-primary">12</c-indicator.item>'


class TestIndicatorRoot:
    def test_the_root_is_an_indicator(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-indicator><button>Inbox</button></c-indicator>"
        )

        assert root(soup) is not None
        assert root(soup).find("button").get_text() == "Inbox"

    def test_class_is_merged_into_one_class_attribute(self, cotton_render_string):
        html = cotton_render_string('<c-indicator class="my-4" data-x="1" />')

        assert root_attribute_names(html).count("class") == 1
        assert "my-4" in html
        assert 'data-x="1"' in html

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string(f"<c-indicator>{BADGE}</c-indicator>")

        assert "<script" not in html
        assert " on" not in html.replace("\n", " ").split(">")[0]


class TestIndicatorItems:
    def test_items_come_before_the_content_when_written_after_it(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-indicator><button>Inbox</button>"
            f'<c-slot name="items">{BADGE}</c-slot></c-indicator>'
        )

        children = root(soup).find_all(recursive=False)
        assert [child.name for child in children] == ["span", "button"]

    def test_items_come_before_the_content_when_written_first(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            f'<c-indicator><c-slot name="items">{BADGE}</c-slot>'
            "<button>Inbox</button></c-indicator>"
        )

        children = root(soup).find_all(recursive=False)
        assert [child.name for child in children] == ["span", "button"]

    def test_an_item_is_a_span_with_indicator_item(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(BADGE)

        item = soup.find("span")
        assert "indicator-item" in item["class"]
        assert "badge" in item["class"]
        assert "badge-primary" in item["class"]
        assert item.get_text() == "12"

    def test_several_items_each_keep_their_own_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-indicator><button>Inbox</button>"
            '<c-slot name="items">'
            '<c-indicator.item placement="top start" class="badge">A</c-indicator.item>'
            '<c-indicator.item placement="bottom end" class="badge-info">B</c-indicator.item>'
            "</c-slot></c-indicator>"
        )

        first, second = root(soup).find_all("span", recursive=False)
        assert {"indicator-top", "indicator-start", "badge"} <= set(first["class"])
        assert {"indicator-bottom", "indicator-end", "badge-info"} <= set(
            second["class"]
        )
        assert "badge-info" not in first["class"]
        assert "badge" not in second["class"]

    def test_an_indicator_with_no_items_renders_its_content_unchanged(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-indicator><button>Inbox</button></c-indicator>"
        )

        children = root(soup).find_all(recursive=False)
        assert [child.name for child in children] == ["button"]
        assert not soup.find(class_="indicator-item")


class TestIndicatorItemPlacement:
    def test_no_placement_gives_no_placement_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(BADGE)

        assert placement_classes(soup.find("span")) == set()

    def test_a_two_word_placement_gives_both_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-indicator.item placement="bottom start">1</c-indicator.item>'
        )

        assert placement_classes(soup.find("span")) == {
            "indicator-bottom",
            "indicator-start",
        }

    @pytest.mark.parametrize("word", PLACEMENT_WORDS)
    def test_each_single_word_gives_its_class(self, cotton_render_string_soup, word):
        soup = cotton_render_string_soup(
            f'<c-indicator.item placement="{word}">1</c-indicator.item>'
        )

        assert placement_classes(soup.find("span")) == {f"indicator-{word}"}

    def test_an_unknown_word_adds_no_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-indicator.item placement="left">1</c-indicator.item>'
        )

        assert placement_classes(soup.find("span")) == set()
        assert "indicator-left" not in soup.find("span")["class"]

    def test_an_unknown_word_does_not_hide_a_known_one(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-indicator.item placement="left top">1</c-indicator.item>'
        )

        assert placement_classes(soup.find("span")) == {"indicator-top"}

    def test_class_is_merged_into_one_class_attribute(self, cotton_render_string):
        html = cotton_render_string(
            '<c-indicator.item placement="top end" class="badge" data-x="1">1</c-indicator.item>'
        )

        assert root_attribute_names(html).count("class") == 1
        assert 'data-x="1"' in html


class TestIndicatorIgnoresPageContext:
    def test_page_context_does_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-indicator.item>1</c-indicator.item>",
            {"placement": "bottom end"},
        )

        assert placement_classes(soup.find("span")) == set()

    def test_a_page_items_variable_is_not_rendered(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-indicator>Inbox</c-indicator>", {"items": "PAGE-ITEMS"}
        )

        assert soup.find("div").get_text() == "Inbox"

    def test_an_items_slot_still_renders(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-indicator>Inbox<c-slot name="items">'
            "<c-indicator.item>3</c-indicator.item></c-slot></c-indicator>",
            {"items": "PAGE-ITEMS"},
        )

        assert soup.find(class_="indicator-item").get_text() == "3"
        assert "PAGE-ITEMS" not in soup.get_text()


class TestIndicatorAnnotations:
    @pytest.fixture
    def indicator(self):
        return AnnotationParser().parse((INDICATOR_DIR / "index.html").read_text())

    @pytest.fixture
    def item(self):
        return AnnotationParser().parse((INDICATOR_DIR / "item.html").read_text())

    def test_the_items_slot_hides_the_count_and_speaks_it_visually_hidden(
        self, indicator, cotton_render_string_soup
    ):
        content = next(s for s in indicator.slots if s.name == "items").content

        soup = cotton_render_string_soup(f"<c-indicator>{content}</c-indicator>")

        item = soup.find(class_="indicator-item")
        hidden_count = item.find(attrs={"aria-hidden": "true"})
        spoken = item.find(class_="sr-only")
        assert hidden_count is not None
        assert hidden_count.get_text(strip=True).isdigit()
        assert spoken is not None
        assert spoken.get_text(strip=True)
        assert hidden_count.find_next(class_="sr-only") is spoken

    def test_placement_offers_the_nine_corners(self, item):
        prop = next(p for p in item.props if p.clean_name == "placement")

        assert prop.type == "select"
        assert list(prop.options) == CORNERS
        assert not prop.default

    @pytest.mark.parametrize("template", ["indicator", "item"])
    def test_class_is_documented(self, indicator, item, template):
        parsed = {"indicator": indicator, "item": item}[template]

        assert "class" in {p.clean_name for p in parsed.props}

    def test_the_item_has_a_default_slot(self, item):
        assert [s.name for s in item.slots] == [None]
