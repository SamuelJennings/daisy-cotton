"""Tests for <c-collapse> and <c-accordion>: daisyUI's collapse built on
<details>/<summary>, with no script, and the accordion that draws itself as
a collapse and forwards every collapse attribute and slot.

Grouped opening/closing (an accordion's items sharing a ``name`` forming an
exclusive group) is the browser's own ``<details name="...">`` behaviour —
these tests assert the markup that behaviour depends on, not the browser
behaviour itself.
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
    """The value of the first attribute named ``name``, or ``None``."""
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


def _class_attrs_on(html, tag):
    """Every ``class="..."`` value found on the first ``<tag ...>`` open tag."""
    return [
        name_value[1] for name_value in _attrs_on(html, tag) if name_value[0] == "class"
    ]


class TestCollapseStructure:
    """AS1: a root carrying ``collapse``, a ``<summary>`` carrying
    ``collapse-title`` holding ``title``, and the default slot in
    ``collapse-content``."""

    def test_title_and_content_render_in_their_parts(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-collapse title="Details">Content</c-collapse>'
        )

        root = soup.find("details", class_="collapse")
        assert root is not None

        summary = root.find("summary", class_="collapse-title", recursive=False)
        assert summary is not None
        assert summary.get_text(strip=True) == "Details"

        content = root.find("div", class_="collapse-content", recursive=False)
        assert content is not None
        assert content.get_text(strip=True) == "Content"


class TestCollapseTitleSlot:
    """AS5: a ``title`` slot fills the summary."""

    def test_title_slot_fills_the_summary(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-collapse><c-slot name="title">'
            '<i class="bi bi-star"></i><span class="badge">New</span>'
            "</c-slot>Content</c-collapse>"
        )

        summary = soup.find("summary", class_="collapse-title")
        assert summary is not None
        assert summary.find("i", class_="bi bi-star") is not None
        assert summary.find("span", class_="badge") is not None


class TestCollapseOpen:
    """AS3: ``open`` renders the collapse initially expanded through the
    browser's native ``open`` attribute, never daisyUI's state-locking
    ``collapse-open``/``collapse-close`` classes (SC-001)."""

    def test_open_renders_the_native_open_attribute(self, cotton_render_string):
        html = cotton_render_string(
            '<c-collapse title="Details" open>Content</c-collapse>'
        )
        attrs = _attrs_on(html, "details")
        assert any(name == "open" for name, _ in attrs)

    def test_without_open_no_open_attribute_is_rendered(self, cotton_render_string):
        html = cotton_render_string('<c-collapse title="Details">Content</c-collapse>')
        attrs = _attrs_on(html, "details")
        assert all(name != "open" for name, _ in attrs)

    def test_open_never_renders_the_locking_classes(self, cotton_render_string):
        html = cotton_render_string(
            '<c-collapse title="Details" open>Content</c-collapse>'
        )
        root_classes = _class_attrs_on(html, "details")
        assert "collapse-open" not in root_classes[0]
        assert "collapse-close" not in root_classes[0]


class TestCollapseModifiers:
    """AS4: ``arrow`` and ``plus`` map to ``collapse-arrow`` and ``collapse-plus``."""

    def test_arrow_adds_collapse_arrow(self, cotton_render_string):
        html = cotton_render_string(
            '<c-collapse title="Details" arrow>Content</c-collapse>'
        )
        root_classes = _class_attrs_on(html, "details")
        assert "collapse-arrow" in root_classes[0]

    def test_plus_adds_collapse_plus(self, cotton_render_string):
        html = cotton_render_string(
            '<c-collapse title="Details" plus>Content</c-collapse>'
        )
        root_classes = _class_attrs_on(html, "details")
        assert "collapse-plus" in root_classes[0]


class TestCollapseNamePassthrough:
    """``name`` is not declared, so it passes through ``{{ attrs }}`` to
    ``<details>`` — how an accordion's group is formed."""

    def test_name_reaches_the_details_element(self, cotton_render_string):
        html = cotton_render_string(
            '<c-collapse title="Details" name="faq">Content</c-collapse>'
        )
        attrs = _attrs_on(html, "details")
        assert _attr_value(attrs, "name") == "faq"


class TestCollapsePageContextDoesNotLeak:
    """A page variable sharing a declared name never fills an empty collapse part."""

    def test_page_context_title_and_open_do_not_leak_in(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-collapse>Content</c-collapse>",
            context={"title": "Page title", "open": True},
        )

        summary = soup.find("summary", class_="collapse-title")
        assert summary is not None
        assert summary.get_text(strip=True) == ""

        root = soup.find("details", class_="collapse")
        assert root.get("open") is None
