"""Tests for <c-card>'s daisyUI structure: root, figure, body, title, actions,
and the size/border/dash/side/image-full modifiers.

The card renders only the parts it is given: a figure before the body, a
``card-title`` heading from ``title`` (attribute or slot), and a
``card-actions`` row at the foot of the body from the ``actions`` slot. A
card given none of these emits just the root and the body.
"""

from html.parser import HTMLParser

import pytest


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


def _class_attrs_on(html, tag):
    """Every ``class="..."`` value found on the first ``<tag ...>`` open tag."""
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return [value for name, value in parser.attrs if name == "class"]


class TestCardTitle:
    """``title``, as an attribute or a named slot, is a ``card-title`` heading."""

    def test_title_attribute_renders_a_card_title_heading(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-card title="Plan">Body</c-card>')

        heading = soup.find("h2", class_="card-title")
        assert heading is not None
        assert heading.get_text(strip=True) == "Plan"

    def test_title_slot_fills_the_card_title_heading(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-card><c-slot name="title">'
            '<i class="bi bi-star"></i><span class="badge">New</span>'
            "</c-slot>Body</c-card>"
        )

        heading = soup.find("h2", class_="card-title")
        assert heading is not None
        assert heading.find("i", class_="bi bi-star") is not None
        assert heading.find("span", class_="badge") is not None


class TestCardFigure:
    """A ``figure`` slot renders in a ``<figure>`` before the body."""

    def test_figure_slot_renders_in_a_figure_before_the_body(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-card><c-slot name="figure"><img src="cat.jpg" alt="A cat" /></c-slot>Body</c-card>'
        )

        root = soup.find("div", class_="card")
        figure = root.find("figure", recursive=False)
        assert figure is not None
        assert figure.find("img")["alt"] == "A cat"

        children = root.find_all(recursive=False)
        assert children[0] is figure, "the figure must come before the body"


class TestCardActions:
    """An ``actions`` slot renders in ``card-actions`` at the foot of the body."""

    def test_actions_slot_renders_in_card_actions_at_the_foot(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-card>Body<c-slot name="actions"><button>Buy</button></c-slot></c-card>'
        )

        body = soup.find("div", class_="card-body")
        actions = body.find("div", class_="card-actions")
        assert actions is not None
        assert actions.find("button").get_text() == "Buy"

        children = body.find_all(recursive=False)
        assert children[-1] is actions, "actions must be the last part of the body"


class TestCardEmptyParts:
    """A card given no title, figure or actions emits only the root and the body."""

    def test_no_empty_heading_figure_or_actions_row(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-card>Body</c-card>")

        assert soup.find("h2") is None
        assert soup.find("figure") is None
        assert soup.find("div", class_="card-actions") is None

        root = soup.find("div", class_="card")
        body = root.find("div", class_="card-body")
        assert body is not None
        assert "Body" in body.get_text()


class TestCardClasses:
    """``class`` and ``content_class`` each merge into a single class list."""

    def test_class_and_content_class_merge_into_one_class_list_each(
        self, cotton_render_string, cotton_render_string_soup
    ):
        source = '<c-card class="bg-base-100 shadow-sm w-96" content_class="gap-4">Body</c-card>'

        html = cotton_render_string(source)
        root_classes = _class_attrs_on(html, "div")
        assert len(root_classes) == 1, (
            f"expected one class attribute, found {root_classes}"
        )
        for token in ("card", "bg-base-100", "shadow-sm", "w-96"):
            assert token in root_classes[0]

        soup = cotton_render_string_soup(source)
        body = soup.find("div", class_="card-body")
        assert "gap-4" in body["class"]

    def test_extra_attributes_reach_the_root(self, cotton_render_string):
        html = cotton_render_string('<c-card id="summary">Body</c-card>')
        root_classes = _class_attrs_on(html, "div")
        assert len(root_classes) == 1
        assert 'id="summary"' in html


class TestCardPageContextDoesNotLeak:
    """A page variable sharing a declared name never fills an empty card part."""

    def test_page_context_title_figure_and_actions_do_not_leak_in(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-card>Body</c-card>",
            context={
                "title": "Page title",
                "figure": "<img src='leak.jpg'>",
                "actions": "<button>Leaked</button>",
            },
        )

        assert soup.find("h2") is None
        assert soup.find("figure") is None
        assert soup.find("div", class_="card-actions") is None


class TestCardSize:
    """``size`` maps xs-xl to daisyUI's ``card-<size>`` class."""

    @pytest.mark.parametrize("size", ["xs", "sm", "md", "lg", "xl"])
    def test_each_size_maps_to_its_daisyui_class(self, cotton_render_string, size):
        html = cotton_render_string(f'<c-card size="{size}">Body</c-card>')
        root_classes = _class_attrs_on(html, "div")
        assert f"card-{size}" in root_classes[0]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-card size="xxl">Body</c-card>')
        root_classes = _class_attrs_on(html, "div")
        assert "card-xxl" not in root_classes[0]


class TestCardModifiers:
    """``border``, ``dash``, ``side`` and ``image-full`` map to their daisyUI classes."""

    def test_border_adds_card_border(self, cotton_render_string):
        html = cotton_render_string("<c-card border>Body</c-card>")
        root_classes = _class_attrs_on(html, "div")
        assert "card-border" in root_classes[0]

    def test_dash_adds_card_dash(self, cotton_render_string):
        html = cotton_render_string("<c-card dash>Body</c-card>")
        root_classes = _class_attrs_on(html, "div")
        assert "card-dash" in root_classes[0]

    def test_side_true_adds_the_bare_class(self, cotton_render_string):
        html = cotton_render_string("<c-card side>Body</c-card>")
        root_classes = _class_attrs_on(html, "div")
        assert "card-side" in root_classes[0]
        assert "sm:card-side" not in root_classes[0]

    def test_side_breakpoint_adds_the_prefixed_class(self, cotton_render_string):
        html = cotton_render_string('<c-card side="sm">Body</c-card>')
        root_classes = _class_attrs_on(html, "div")
        assert "sm:card-side" in root_classes[0]

    def test_side_not_a_breakpoint_emits_nothing(self, cotton_render_string):
        html = cotton_render_string('<c-card side="left">Body</c-card>')
        root_classes = _class_attrs_on(html, "div")
        assert "card-side" not in root_classes[0]

    def test_image_full_adds_the_class(self, cotton_render_string):
        html = cotton_render_string("<c-card image-full>Body</c-card>")
        root_classes = _class_attrs_on(html, "div")
        assert "image-full" in root_classes[0]

    def test_image_full_never_reaches_the_root_as_a_raw_attribute(
        self, cotton_render_string
    ):
        html = cotton_render_string("<c-card image-full>Body</c-card>")
        root = html[: html.index(">") + 1]
        assert "image-full=" not in root
