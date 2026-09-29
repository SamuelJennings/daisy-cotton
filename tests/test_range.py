"""Tests for <c-form.range>: daisyUI's native slider, whose min and max are
always emitted (the browser's own defaults, 0 and 100) so the element is
never left without bounds.
"""

from html.parser import HTMLParser


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser — which is what min and max being
    emitted exactly once needs to be caught.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _attrs_on(html, tag):
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return parser.attrs


def _attr_count(attrs, name):
    return sum(1 for attr_name, _ in attrs if attr_name == name)


def _attr_value(attrs, name):
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


class TestRange:
    def test_name_value_and_modifiers_render_native_range_with_default_bounds(
        self, cotton_render_string, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.range name="volume" value="40" variant="success" size="xs" />'
        )

        ranges = soup.find_all("input", type="range")
        assert len(ranges) == 1
        range_input = ranges[0]
        for token in ("range", "range-success", "range-xs"):
            assert token in range_input["class"]
        assert range_input["name"] == "volume"
        assert range_input["value"] == "40"
        assert range_input["min"] == "0"
        assert range_input["max"] == "100"

        attrs = _attrs_on(
            cotton_render_string('<c-form.range name="volume" value="40" />'), "input"
        )
        assert _attr_count(attrs, "min") == 1
        assert _attr_count(attrs, "max") == 1

    def test_min_and_max_replace_the_defaults(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.range name="volume" min="10" max="20" step="2" />'
        )

        range_input = soup.find("input", type="range")
        assert range_input["min"] == "10"
        assert range_input["max"] == "20"
        assert range_input["step"] == "2"

    def test_min_bound_to_integer_zero_still_renders(self, cotton_render_string):
        attrs = _attrs_on(cotton_render_string('<c-form.range :min="0" />'), "input")

        assert _attr_value(attrs, "min") == "0"

    def test_vertical_renders_range_vertical(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.range vertical />")

        assert "range-vertical" in soup.find("input", type="range")["class"]

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.range variant="rainbow" />')

        assert "range-rainbow" not in soup.find("input", type="range")["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.range size="xxl" />')

        assert "range-xxl" not in soup.find("input", type="range")["class"]

    def test_class_merges_with_the_modifier_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.range class="join-item" />')

        assert "join-item" in soup.find("input", type="range")["class"]
