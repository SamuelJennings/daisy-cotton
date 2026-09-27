"""Regression test: ``c-breadcrumbs.item`` renders ``href`` twice.

``breadcrumbs/item.html`` renders an explicit ``href="{{ href }}"`` on its
anchor and also spreads ``{{ attrs }}`` on the same element. Cotton only
strips a variable out of ``attrs`` when it is declared in ``<c-vars>``;
``href`` was not declared, so it stayed in ``attrs`` and was written a
second time, verbatim and unrendered.

Sources are compiled through the Cotton compiler (mirroring
``test_class_attribute_merge.py``) so the test exercises the component
exactly as a template invocation would — rendering the component's own
template file directly, as ``test_render_all.py`` does, never triggers
Cotton's c-vars / ``attrs`` extraction and would not reproduce this bug.
"""

from html.parser import HTMLParser

from bs4 import BeautifulSoup
from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first `<tag>` start tag.

    HTMLParser respects attribute quoting and — unlike a browser — reports
    every occurrence of a repeated attribute rather than silently dropping
    it, which is exactly what this bug needs to be caught.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def attrs_named_on(html, tag, name):
    """Every value found under ``name`` on the first ``<tag ...>`` open tag."""
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return [value for attr_name, value in parser.attrs if attr_name == name]


class TestBreadcrumbItemHrefAttribute:
    """A breadcrumb item's ``href`` is written once, not duplicated."""

    def test_href_appears_once(self):
        html = render(
            '<c-breadcrumbs.item text="Account Center" href="/account-center/" />'
        )
        hrefs = attrs_named_on(html, "a", "href")
        assert len(hrefs) == 1, f"expected one href attribute, found {hrefs}"
        assert hrefs[0] == "/account-center/"

    def test_item_without_href_has_no_anchor(self):
        html = render('<c-breadcrumbs.item text="Current Page" />')
        assert "<a" not in html
        assert "Current Page" in html


class TestTheItemTextSpan:
    """The crumb's text sits in a bare span, before the slot, so the current
    step has an element to carry ``aria-current``."""

    def test_the_link_branch_shows_its_text_inside_the_link(self):
        html = render('<c-breadcrumbs.item text="Products" href="/products/" />')
        soup = BeautifulSoup(html, "html.parser")
        assert soup.a.get_text(strip=True) == "Products"
        assert soup.a.find("span", class_="daisy-cotton-breadcrumb-text") is None

    def test_the_non_link_branch_shows_its_text_in_a_span(self):
        html = render('<c-breadcrumbs.item text="Current Page" />')
        span = BeautifulSoup(html, "html.parser").li.span
        assert span.get_text(strip=True) == "Current Page"
        assert not span.has_attr("class")

    def test_the_slot_follows_the_text(self):
        html = render(
            '<c-breadcrumbs.item text="Products" href="/products/">'
            "<b>marker</b>"
            "</c-breadcrumbs.item>"
        )
        assert html.index("Products") < html.index("<b>marker</b>")

    def test_href_stays_on_the_link_and_class_and_attrs_land_on_the_item(self):
        html = render(
            '<c-breadcrumbs.item text="Products" href="/products/" '
            'class="foo" data-x="1" />'
        )
        assert attrs_named_on(html, "a", "href") == ["/products/"]
        assert attrs_named_on(html, "li", "class") == ["foo"]
        assert attrs_named_on(html, "li", "data-x") == ["1"]
        assert attrs_named_on(html, "a", "data-x") == []


class TestTheCurrentItem:
    """An item with no ``href`` is the current page."""

    def test_an_item_without_href_is_marked_current(self):
        html = render('<c-breadcrumbs.item text="Current Page" />')
        soup = BeautifulSoup(html, "html.parser")
        assert soup.li.span["aria-current"] == "page"
        assert soup.a is None

    def test_an_item_with_href_is_not_marked_current(self):
        html = render('<c-breadcrumbs.item text="Products" href="/products/" />')
        assert "aria-current" not in html


class TestTheTrailLandmark:
    """The trail is a named navigation landmark carrying only daisyUI's class."""

    def test_root_is_a_nav_named_breadcrumbs(self):
        html = render('<c-breadcrumbs :items="items" />', items=[{"text": "Home"}])
        nav = BeautifulSoup(html, "html.parser").find("nav")
        assert nav["aria-label"] == "Breadcrumbs"
        assert nav["class"] == ["breadcrumbs"]

    def test_caller_class_is_added_to_the_root_class_list(self):
        html = render(
            '<c-breadcrumbs class="text-sm" :items="items" />',
            items=[{"text": "Home"}],
        )
        assert BeautifulSoup(html, "html.parser").nav["class"] == [
            "breadcrumbs",
            "text-sm",
        ]

    def test_caller_aria_label_replaces_the_default_once(self):
        html = render(
            '<c-breadcrumbs aria-label="You are here" :items="items" />',
            items=[{"text": "Home"}],
        )
        assert html.count("aria-label=") == 1
        assert BeautifulSoup(html, "html.parser").nav["aria-label"] == "You are here"

    def test_other_attributes_reach_the_root(self):
        html = render(
            '<c-breadcrumbs id="trail" :items="items" />', items=[{"text": "Home"}]
        )
        assert BeautifulSoup(html, "html.parser").nav["id"] == "trail"


class TestTheTrailShapes:
    """A trail built from ``items`` matches the same trail written in the slot."""

    ITEMS = [
        {"text": "Home", "href": "/"},
        {"text": "Products", "href": "/products/"},
        {"text": "Widget"},
    ]

    def test_items_and_slotted_trails_are_equal_after_whitespace_normalisation(self):
        built = render('<c-breadcrumbs :items="items" />', items=self.ITEMS)
        slotted = render(
            "<c-breadcrumbs>"
            '<c-breadcrumbs.item text="Home" href="/" />'
            '<c-breadcrumbs.item text="Products" href="/products/" />'
            '<c-breadcrumbs.item text="Widget" />'
            "</c-breadcrumbs>"
        )
        assert " ".join(built.split()) == " ".join(slotted.split())

    def test_only_the_last_item_of_a_built_trail_is_current(self):
        html = render('<c-breadcrumbs :items="items" />', items=self.ITEMS)
        current = BeautifulSoup(html, "html.parser").find_all(
            attrs={"aria-current": "page"}
        )
        assert len(current) == 1
        assert current[0].get_text(strip=True) == "Widget"

    def test_a_single_item_trail_renders_it_as_current(self):
        html = render('<c-breadcrumbs :items="items" />', items=[{"text": "Home"}])
        soup = BeautifulSoup(html, "html.parser")
        assert len(soup.find_all("li")) == 1
        assert soup.li.span["aria-current"] == "page"


class TestTheTrailsClassStaysOnTheTrail:
    """A class given to ``c-breadcrumbs`` styles the trail, not its items.

    The trail and its items both declare a ``class`` prop, and a Cotton child
    rendered without ``only`` reads a prop it was not given out of the
    surrounding scope. So the trail's own class was written onto every ``<li>``
    inside it as well — invisible until the class was one that changes layout.
    """

    def test_a_class_on_the_trail_does_not_reach_its_items(self):
        html = render(
            '<c-breadcrumbs class="overflow-x-auto" :items="items" />',
            items=[{"text": "Home", "href": "/"}, {"text": "Products"}],
        )
        assert "overflow-x-auto" in attrs_named_on(html, "nav", "class")[0]
        for value in attrs_named_on(html, "li", "class"):
            assert "overflow-x-auto" not in value

    def test_the_items_still_render(self):
        """The isolation must not cost the items the attributes they are
        given: `:attrs` is an explicit prop and passes through `only`."""
        html = render(
            '<c-breadcrumbs :items="items" />',
            items=[{"text": "Home", "href": "/"}, {"text": "Products"}],
        )
        assert attrs_named_on(html, "a", "href") == ["/"]
        assert "Products" in html
