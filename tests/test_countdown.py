"""Tests for the <c-countdown> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from html.parser import HTMLParser


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
