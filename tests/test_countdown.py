"""Tests for the <c-countdown> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from html.parser import HTMLParser
from pathlib import Path

from bs4 import BeautifulSoup
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"


class _StartTags(HTMLParser):
    """Record every start tag with its raw attribute list, duplicates included."""

    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, attrs))


def start_tags(html):
    parser = _StartTags()
    parser.feed(html)
    return parser.tags


def countdown_and_copy(soup):
    """The countdown span and the visually hidden copy that follows it."""
    root = soup.find("span", class_="countdown")
    return root, root.find_next_sibling("span")


class TestCountdownMarkup:
    """The countdown is an animated span plus a visually hidden copy beside it."""

    def test_root_wraps_one_inner_span_carrying_the_value(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-countdown value="42" />')
        root, _ = countdown_and_copy(soup)
        inner = root.find("span", recursive=False)
        assert root.name == "span"
        assert inner["style"] == "--value:42;"
        assert inner.get_text() == "42"
        assert inner["aria-hidden"] == "true"

    def test_hidden_copy_follows_the_countdown_span_outside_it(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-countdown value="42" />')
        root, copy = countdown_and_copy(soup)
        assert copy["class"] == ["sr-only"]
        assert copy.get_text() == "42"
        assert copy.find_parent("span", class_="countdown") is None
        assert root.find("span", class_="sr-only") is None

    def test_hidden_copy_is_not_hidden_from_assistive_technology(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-countdown value="42" />')
        _, copy = countdown_and_copy(soup)
        assert not copy.has_attr("aria-hidden")

    def test_nothing_carries_aria_live_or_aria_label(self, cotton_render_string):
        html = cotton_render_string('<c-countdown value="42" />')
        assert "aria-live" not in html
        assert "aria-label" not in html


class TestCountdownRootAttributes:
    """class merges into the root and further attributes are spread on it."""

    def test_class_merges_into_the_countdown_span(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-countdown value="42" class="font-mono text-4xl" />'
        )
        root, copy = countdown_and_copy(soup)
        assert root["class"] == ["countdown", "font-mono", "text-4xl"]
        assert "font-mono" not in copy["class"]

    def test_class_attribute_appears_once_on_the_root(self, cotton_render_string):
        html = cotton_render_string('<c-countdown value="42" class="font-mono" />')
        tag, attrs = next(t for t in start_tags(html) if t[0] == "span")
        assert [name for name, _ in attrs].count("class") == 1

    def test_extra_attributes_land_on_the_root(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-countdown value="42" data-id="clock" id="seconds" />'
        )
        root, copy = countdown_and_copy(soup)
        assert root["data-id"] == "clock"
        assert root["id"] == "seconds"
        assert not copy.has_attr("data-id")


class TestCountdownValues:
    """value is rendered as given, escaped, in all three places."""

    def test_value_above_the_range_is_rendered_in_all_three_places(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-countdown value="1000" />')
        root, copy = countdown_and_copy(soup)
        inner = root.find("span", recursive=False)
        assert inner["style"] == "--value:1000;"
        assert inner.get_text() == "1000"
        assert copy.get_text() == "1000"

    def test_non_numeric_value_is_rendered_in_all_three_places(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-countdown value="abc" />')
        root, copy = countdown_and_copy(soup)
        inner = root.find("span", recursive=False)
        assert inner["style"] == "--value:abc;"
        assert inner.get_text() == "abc"
        assert copy.get_text() == "abc"

    def test_quote_cannot_close_the_style_attribute(self, cotton_render_string):
        html = cotton_render_string("<c-countdown value='1\" onmouseover=\"x' />")
        spans = [attrs for tag, attrs in start_tags(html) if tag == "span"]
        inner_attrs = dict(spans[1])
        assert list(inner_attrs) == ["style", "aria-hidden"]
        assert inner_attrs["style"] == '--value:1" onmouseover="x;'

    def test_angle_bracket_is_escaped_in_the_visible_text_and_the_hidden_copy(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-countdown :value="typed" />', {"typed": "<b>9"}
        )
        root, copy = countdown_and_copy(soup)
        inner = root.find("span", recursive=False)
        assert soup.find("b") is None
        assert inner.get_text() == "<b>9"
        assert copy.get_text() == "<b>9"

    def test_bare_countdown_renders_zero(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-countdown />")
        root, copy = countdown_and_copy(soup)
        inner = root.find("span", recursive=False)
        assert inner["style"] == "--value:0;"
        assert inner.get_text() == "0"
        assert copy.get_text() == "0"


class TestCountdownPageContext:
    """A page variable named value or class never leaks into the countdown."""

    def test_page_value_does_not_leak(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-countdown />", {"value": "Leaked"})
        root, copy = countdown_and_copy(soup)
        inner = root.find("span", recursive=False)
        assert inner.get_text() == "0"
        assert copy.get_text() == "0"
        assert "Leaked" not in inner["style"]

    def test_page_class_does_not_leak(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-countdown />", {"class": "Leaked"})
        root, _ = countdown_and_copy(soup)
        assert "Leaked" not in root["class"]


class TestCountdownGalleryAnnotations:
    """The gallery entry, read through the gallery's own ``AnnotationParser``."""

    @staticmethod
    def _parsed():
        return AnnotationParser().parse((COTTON_DIR / "countdown.html").read_text())

    def test_the_value_prop_is_text_with_a_default_of_zero(self):
        value = next(p for p in self._parsed().props if p.clean_name == "value")
        assert value.type == "text"
        assert value.default == "0"

    def test_the_component_has_no_slot(self):
        assert self._parsed().slots == ()

    def test_the_description_states_the_range_and_what_a_screen_reader_reads(self):
        description = self._parsed().description
        assert "0 through 999" in description
        assert "screen reader reads the number as rendered" in description

    def test_the_description_names_the_three_things_a_script_updates_together(self):
        description = self._parsed().description
        assert "--value" in description
        assert "visible text" in description
        assert "hidden copy" in description

    def test_the_description_says_zero_padding_needs_an_override(self):
        description = self._parsed().description
        assert "--digits" in description
        assert "override" in description

    def test_the_description_warns_that_the_value_must_be_a_number(self):
        description = self._parsed().description
        assert "never unvalidated user input" in description
        assert "semicolon" in description

    def test_the_description_names_the_hero_entry_for_a_clock(self):
        assert "hero entry" in self._parsed().description


class TestHeroCountdownClock:
    """The hero entry's default slot shows a labelled days, hours, minutes and seconds clock."""

    @staticmethod
    def _rendered_slot(cotton_render_string):
        slot = AnnotationParser().parse((COTTON_DIR / "hero.html").read_text()).slots[0]
        return BeautifulSoup(cotton_render_string(slot.content), "html.parser")

    def test_the_clock_is_four_countdowns_each_with_a_visible_label(
        self, cotton_render_string
    ):
        soup = self._rendered_slot(cotton_render_string)
        clock = []
        for countdown in soup.find_all("span", class_="countdown"):
            labels = countdown.parent.find_all(string=True, recursive=False)
            clock.append(
                (
                    countdown.get_text(),
                    "".join(labels).strip(),
                )
            )
        assert clock == [
            ("15", "days"),
            ("10", "hours"),
            ("24", "min"),
            ("59", "sec"),
        ]

    def test_each_clock_countdown_has_its_hidden_copy(self, cotton_render_string):
        soup = self._rendered_slot(cotton_render_string)
        copies = [
            countdown.find_next_sibling("span", class_="sr-only").get_text()
            for countdown in soup.find_all("span", class_="countdown")
        ]
        assert copies == ["15", "10", "24", "59"]

    def test_the_rotating_heading_sentence_and_call_to_action_remain(
        self, cotton_render_string
    ):
        soup = self._rendered_slot(cotton_render_string)
        assert len(soup.select("h1 .text-rotate")) == 1
        assert len(soup.select("p .text-rotate")) == 1
        assert soup.select_one(".btn.btn-primary").get_text() == "Get started"
