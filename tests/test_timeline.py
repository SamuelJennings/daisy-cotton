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


class TestTimelineItemRoot:
    """US8-2: <c-timeline.item> renders an <li> carrying group/item."""

    def test_root_is_li_carrying_group_item(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-timeline.item start="1984" end="First Macintosh" />'
        )

        root = soup.find("li", class_="group/item")
        assert root is not None


class TestTimelineItemParts:
    """FR-030, US8-2: start and end (attribute or slot) sit in
    timeline-start/timeline-end, and a middle slot sits in
    timeline-middle."""

    def test_start_and_end_attributes_render_in_their_parts(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-timeline.item start="1984" end="First Macintosh" />'
        )

        start = soup.find("div", class_="timeline-start")
        end = soup.find("div", class_="timeline-end")
        assert start is not None and start.get_text(strip=True) == "1984"
        assert end is not None and end.get_text(strip=True) == "First Macintosh"

    def test_middle_slot_renders_in_timeline_middle(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-timeline.item>"
            '<c-slot name="middle"><i class="bi bi-check" aria-hidden="true"></i></c-slot>'
            "</c-timeline.item>"
        )

        middle = soup.find("div", class_="timeline-middle")
        assert middle is not None
        assert middle.find("i", class_="bi bi-check") is not None

    def test_start_and_end_slots_fill_the_matching_part(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-timeline.item>"
            '<c-slot name="start">1984</c-slot>'
            '<c-slot name="end">First Macintosh</c-slot>'
            "</c-timeline.item>"
        )

        start = soup.find("div", class_="timeline-start")
        end = soup.find("div", class_="timeline-end")
        assert start is not None and start.get_text(strip=True) == "1984"
        assert end is not None and end.get_text(strip=True) == "First Macintosh"


class TestTimelineItemEmptyParts:
    """US8-3: start, end or middle left out is not emitted."""

    def test_no_start_emits_no_timeline_start(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-timeline.item end="First Macintosh" />')
        assert soup.find("div", class_="timeline-start") is None

    def test_no_end_emits_no_timeline_end(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-timeline.item start="1984" />')
        assert soup.find("div", class_="timeline-end") is None

    def test_no_middle_emits_no_timeline_middle(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-timeline.item start="1984" />')
        assert soup.find("div", class_="timeline-middle") is None


class TestTimelineItemBox:
    """FR-031, US8-4: box puts timeline-box on the end part, and
    box="start" on the start part instead."""

    def test_box_adds_timeline_box_to_the_end_part(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-timeline.item start="1984" end="First Macintosh" box />'
        )

        end = soup.find("div", class_="timeline-end")
        start = soup.find("div", class_="timeline-start")
        assert end is not None and "timeline-box" in end.get("class", [])
        assert start is not None and "timeline-box" not in start.get("class", [])

    def test_box_start_adds_timeline_box_to_the_start_part_instead(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-timeline.item start="1984" end="First Macintosh" box="start" />'
        )

        start = soup.find("div", class_="timeline-start")
        end = soup.find("div", class_="timeline-end")
        assert start is not None and "timeline-box" in start.get("class", [])
        assert end is not None and "timeline-box" not in end.get("class", [])

    def test_box_end_adds_timeline_box_to_the_end_part(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-timeline.item start="1984" end="First Macintosh" box="end" />'
        )

        start = soup.find("div", class_="timeline-start")
        end = soup.find("div", class_="timeline-end")
        assert end is not None and "timeline-box" in end.get("class", [])
        assert start is not None and "timeline-box" not in start.get("class", [])


class TestTimelineItemConnectors:
    """FR-032, US8-6: a leading and a trailing hr, both hidden from
    assistive technology, bracket every item so consecutive events join
    and the line does not extend past the first or last item."""

    def test_item_has_a_leading_and_a_trailing_hr_both_aria_hidden(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-timeline.item start="1984" end="First Macintosh" />'
        )

        root = soup.find("li", class_="group/item")
        hrs = root.find_all("hr", recursive=False)
        assert len(hrs) == 2
        assert "group-first/item:hidden" in hrs[0].get("class", [])
        assert hrs[0].get("aria-hidden") == "true"
        assert "group-last/item:hidden" in hrs[1].get("class", [])
        assert hrs[1].get("aria-hidden") == "true"

    def test_leading_hr_precedes_and_trailing_hr_follows_the_parts(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-timeline.item start="1984" end="First Macintosh" />'
        )

        root = soup.find("li", class_="group/item")
        children = root.find_all(recursive=False)
        assert children[0].name == "hr"
        assert children[-1].name == "hr"
        start = root.find("div", class_="timeline-start")
        end = root.find("div", class_="timeline-end")
        assert children.index(children[0]) < children.index(start)
        assert children.index(end) < children.index(children[-1])


class TestTimelineItemClassAndAttrs:
    """class merges into the item's single class list, and other
    attributes reach the root."""

    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-timeline.item class="my-item" data-test="x" />')

        root_classes = _class_attrs_on(html, "li")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "group/item" in root_classes[0]
        assert "my-item" in root_classes[0]

        attrs = _attrs_on(html, "li")
        assert _attr_value(attrs, "data-test") == "x"


class TestTimelineItemPageContextDoesNotLeak:
    """A page variable sharing a declared name never fills an empty item's
    parts."""

    def test_page_context_start_and_end_do_not_leak_in(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-timeline.item />",
            context={"start": "Leaked start", "end": "Leaked end"},
        )

        assert soup.find("div", class_="timeline-start") is None
        assert soup.find("div", class_="timeline-end") is None
