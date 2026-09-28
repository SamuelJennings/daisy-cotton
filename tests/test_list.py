"""Tests for <c-list> and <c-list.row>: daisyUI's list markup — a vertical
list of rows, such as people, files or songs, each row holding an image, the
main text and actions.

A row's children reach list-col-grow and list-col-wrap through their own
class attribute; the row itself declares nothing for either (FR-028).
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


class TestListRoot:
    def test_root_is_ul_carrying_list_holding_rows(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-list><c-list.row>Row one</c-list.row></c-list>"
        )

        root = soup.find("ul", class_="list")
        assert root is not None

        rows = root.find_all("li", class_="list-row")
        assert len(rows) == 1
        assert rows[0].get_text(strip=True) == "Row one"


class TestListRowRoot:
    def test_row_is_li_carrying_list_row(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-list.row>Row content</c-list.row>")

        row = soup.find("li", class_="list-row")
        assert row is not None
        assert row.get_text(strip=True) == "Row content"


class TestListClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-list class="shadow" data-test="x"></c-list>')

        root_classes = _class_attrs_on(html, "ul")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "list" in root_classes[0]
        assert "shadow" in root_classes[0]

        attrs = _attrs_on(html, "ul")
        assert _attr_value(attrs, "data-test") == "x"


class TestListRowClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-list.row class="my-row" data-test="x">Row</c-list.row>'
        )

        root_classes = _class_attrs_on(html, "li")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        assert "list-row" in root_classes[0]
        assert "my-row" in root_classes[0]

        attrs = _attrs_on(html, "li")
        assert _attr_value(attrs, "data-test") == "x"


class TestListPageContextDoesNotLeak:
    def test_page_context_class_does_not_leak_in(self, cotton_render_string):
        html = cotton_render_string(
            "<c-list></c-list>", context={"class": "leaked-class"}
        )

        root_classes = _class_attrs_on(html, "ul")
        assert len(root_classes) == 1
        assert "leaked-class" not in root_classes[0]


class TestListRowPageContextDoesNotLeak:
    def test_page_context_class_does_not_leak_in(self, cotton_render_string):
        html = cotton_render_string(
            "<c-list.row></c-list.row>", context={"class": "leaked-class"}
        )

        root_classes = _class_attrs_on(html, "li")
        assert len(root_classes) == 1
        assert "leaked-class" not in root_classes[0]
