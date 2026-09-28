"""Tests for <c-stat> and <c-stat.group>: daisyUI's stat markup — a title,
a value and a description read in that order, with an optional figure such
as an icon and optional actions, laid out in a row that stacks on small
screens.

A stat's value is falsy when given as the number ``0``, so the template
guards it with ``value == 0`` as well as truthiness (D5, SPEC-003): a
dynamic ``:value="0"`` must still render.
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


class TestStatParts:
    def test_title_value_desc_attributes_render_in_that_order(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-stat title="Downloads" value="31K" desc="Jan 1st" />'
        )

        root = soup.find("div", class_="stat")
        assert root is not None

        title = root.find("div", class_="stat-title")
        value = root.find("div", class_="stat-value")
        desc = root.find("div", class_="stat-desc")
        assert title is not None and title.get_text(strip=True) == "Downloads"
        assert value is not None and value.get_text(strip=True) == "31K"
        assert desc is not None and desc.get_text(strip=True) == "Jan 1st"

        children = root.find_all(recursive=False)
        assert children.index(title) < children.index(value) < children.index(desc)

    def test_title_value_desc_slots_fill_the_matching_part(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-stat>"
            '<c-slot name="title"><span class="badge">Downloads</span></c-slot>'
            '<c-slot name="value">31K</c-slot>'
            '<c-slot name="desc">Jan 1st</c-slot>'
            "</c-stat>"
        )

        title = soup.find("div", class_="stat-title")
        value = soup.find("div", class_="stat-value")
        desc = soup.find("div", class_="stat-desc")
        assert title is not None and title.find("span", class_="badge") is not None
        assert value is not None and value.get_text(strip=True) == "31K"
        assert desc is not None and desc.get_text(strip=True) == "Jan 1st"

    def test_value_zero_renders_stat_value_holding_zero(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-stat :value="0" />')

        value = soup.find("div", class_="stat-value")
        assert value is not None
        assert value.get_text(strip=True) == "0"


class TestStatFigure:
    def test_figure_slot_renders_in_stat_figure_before_the_title(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-stat title="Downloads">'
            '<c-slot name="figure"><i class="bi bi-download" aria-hidden="true"></i></c-slot>'
            "</c-stat>"
        )

        root = soup.find("div", class_="stat")
        figure = root.find("div", class_="stat-figure")
        title = root.find("div", class_="stat-title")
        assert figure is not None
        assert figure.find("i", class_="bi bi-download") is not None

        children = root.find_all(recursive=False)
        assert children.index(figure) < children.index(title)


class TestStatActions:
    def test_actions_slot_renders_in_stat_actions(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-stat title="Balance">'
            '<c-slot name="actions"><button class="btn btn-sm">Withdraw</button></c-slot>'
            "</c-stat>"
        )

        actions = soup.find("div", class_="stat-actions")
        assert actions is not None
        assert actions.find("button").get_text(strip=True) == "Withdraw"


class TestStatEmptyParts:
    def test_no_empty_desc_figure_or_actions(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-stat title="Downloads" value="31K" />')

        root = soup.find("div", class_="stat")
        assert root.find("div", class_="stat-desc") is None
        assert root.find("div", class_="stat-figure") is None
        assert root.find("div", class_="stat-actions") is None

    def test_empty_stat_emits_only_the_root(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-stat />")

        root = soup.find("div", class_="stat")
        assert root is not None
        assert root.find(True) is None


class TestStatClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-stat title="Downloads" class="shadow" data-test="x" />'
        )

        root_classes = _class_attrs_on(html, "div")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "stat" in root_classes[0]
        assert "shadow" in root_classes[0]

        attrs = _attrs_on(html, "div")
        assert _attr_value(attrs, "data-test") == "x"


class TestStatPageContextDoesNotLeak:
    def test_page_context_title_value_and_desc_do_not_leak_in(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-stat />",
            context={
                "title": "Leaked title",
                "value": "Leaked value",
                "desc": "Leaked desc",
            },
        )

        root = soup.find("div", class_="stat")
        assert root is not None
        assert root.find("div", class_="stat-title") is None
        assert root.find("div", class_="stat-value") is None
        assert root.find("div", class_="stat-desc") is None


class TestStatGroup:
    def test_group_root_carries_stats_holding_stats_inside(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-stat.group>"
            '<c-stat title="Downloads" value="31K" />'
            '<c-stat title="New Users" value="4,200" />'
            "</c-stat.group>"
        )

        root = soup.find("div", class_="stats")
        assert root is not None

        stats = root.find_all("div", class_="stat")
        assert len(stats) == 2

    def test_group_class_and_extra_attributes_reach_the_root(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-stat.group class="shadow" data-test="x">'
            '<c-stat title="Downloads" value="31K" />'
            "</c-stat.group>"
        )

        root_classes = _class_attrs_on(html, "div")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "stats" in root_classes[0]
        assert "shadow" in root_classes[0]

        attrs = _attrs_on(html, "div")
        assert _attr_value(attrs, "data-test") == "x"


class TestStatGroupResponsive:
    def test_vertical_true_adds_the_bare_class(self, cotton_render_string):
        html = cotton_render_string("<c-stat.group vertical></c-stat.group>")
        root_classes = _class_attrs_on(html, "div")
        assert "stats-vertical" in root_classes[0]

    def test_horizontal_true_adds_the_bare_class(self, cotton_render_string):
        html = cotton_render_string("<c-stat.group horizontal></c-stat.group>")
        root_classes = _class_attrs_on(html, "div")
        assert "stats-horizontal" in root_classes[0]

    def test_vertical_and_horizontal_breakpoint_combine(self, cotton_render_string):
        html = cotton_render_string(
            '<c-stat.group vertical horizontal="lg"></c-stat.group>'
        )
        root_classes = _class_attrs_on(html, "div")
        assert "stats-vertical" in root_classes[0]
        assert "lg:stats-horizontal" in root_classes[0]

    def test_horizontal_unknown_breakpoint_emits_nothing(self, cotton_render_string):
        html = cotton_render_string('<c-stat.group horizontal="left"></c-stat.group>')
        root_classes = _class_attrs_on(html, "div")
        assert "stats-horizontal" not in root_classes[0]
        assert "left:stats-horizontal" not in root_classes[0]


class TestStatGroupPageContextDoesNotLeak:
    def test_page_context_class_does_not_leak_in(self, cotton_render_string):
        html = cotton_render_string(
            "<c-stat.group></c-stat.group>",
            context={"class": "leaked-class"},
        )

        root_classes = _class_attrs_on(html, "div")
        assert len(root_classes) == 1
        assert "leaked-class" not in root_classes[0]
