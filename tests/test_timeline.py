"""Tests for <c-timeline> and <c-timeline.item>: daisyUI's timeline markup —
events in order, vertically or horizontally, each with a date or label, an
icon on the line, and a description, optionally in a box.
"""

from html.parser import HTMLParser


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser — which is what a duplicate
    ``class`` attribute needs to be caught.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _attrs_on(html, tag):
    """The raw ``(name, value)`` attribute list of the first ``<tag ...>`` open tag."""
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return parser.attrs


def _attr_value(attrs, name):
    """The value of the first attribute named ``name``, or ``None`` if absent."""
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


def _class_attrs_on(html, tag):
    """Every ``class="..."`` value found on the first ``<tag ...>`` open tag."""
    return [
        name_value[1] for name_value in _attrs_on(html, tag) if name_value[0] == "class"
    ]


class TestTimelineRoot:
    """US8-1: <c-timeline> renders a <ul> carrying timeline, holding the
    default slot."""

    def test_root_is_ul_carrying_timeline_holding_slot(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-timeline><li>Item</li></c-timeline>")

        root = soup.find("ul", class_="timeline")
        assert root is not None
        assert root.find("li").get_text(strip=True) == "Item"


class TestTimelineModifiers:
    """FR-029, US8-5: vertical/horizontal (each a boolean or a breakpoint),
    compact and snap-icon map to their daisyUI classes."""

    def test_vertical_true_adds_the_bare_class(self, cotton_render_string):
        html = cotton_render_string("<c-timeline vertical></c-timeline>")
        root_classes = _class_attrs_on(html, "ul")
        assert "timeline-vertical" in root_classes[0]

    def test_horizontal_true_adds_the_bare_class(self, cotton_render_string):
        html = cotton_render_string("<c-timeline horizontal></c-timeline>")
        root_classes = _class_attrs_on(html, "ul")
        assert "timeline-horizontal" in root_classes[0]

    def test_horizontal_breakpoint_adds_the_prefixed_class(self, cotton_render_string):
        html = cotton_render_string('<c-timeline horizontal="md"></c-timeline>')
        root_classes = _class_attrs_on(html, "ul")
        assert "md:timeline-horizontal" in root_classes[0]

    def test_horizontal_unknown_breakpoint_emits_nothing(self, cotton_render_string):
        html = cotton_render_string('<c-timeline horizontal="left"></c-timeline>')
        root_classes = _class_attrs_on(html, "ul")
        assert "timeline-horizontal" not in root_classes[0]
        assert "left:timeline-horizontal" not in root_classes[0]

    def test_compact_adds_the_class(self, cotton_render_string):
        html = cotton_render_string("<c-timeline compact></c-timeline>")
        root_classes = _class_attrs_on(html, "ul")
        assert "timeline-compact" in root_classes[0]

    def test_snap_icon_adds_the_class(self, cotton_render_string):
        html = cotton_render_string("<c-timeline snap-icon></c-timeline>")
        root_classes = _class_attrs_on(html, "ul")
        assert "timeline-snap-icon" in root_classes[0]

    def test_snap_icon_never_reaches_the_root_as_a_raw_attribute(
        self, cotton_render_string
    ):
        html = cotton_render_string("<c-timeline snap-icon></c-timeline>")
        root = html[: html.index(">") + 1]
        assert "snap-icon=" not in root


class TestTimelineClassAndAttrs:
    """class merges into the timeline's single class list, and other
    attributes reach the root."""

    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-timeline class="my-timeline" data-test="x"></c-timeline>'
        )

        root_classes = _class_attrs_on(html, "ul")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "timeline" in root_classes[0]
        assert "my-timeline" in root_classes[0]

        attrs = _attrs_on(html, "ul")
        assert _attr_value(attrs, "data-test") == "x"


class TestTimelinePageContextDoesNotLeak:
    """A page variable named ``class`` never fills an empty timeline's class
    list."""

    def test_page_context_class_does_not_leak_in(self, cotton_render_string):
        html = cotton_render_string(
            "<c-timeline></c-timeline>", context={"class": "leaked-class"}
        )

        root_classes = _class_attrs_on(html, "ul")
        assert len(root_classes) == 1
        assert "leaked-class" not in root_classes[0]
