"""``<c-footer>`` and ``<c-footer.nav>``: the footer landmark and its groups."""

from html.parser import HTMLParser
from pathlib import Path

import pytest
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

FOOTER_DIR = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "footer"
)


class _RootAttrs(HTMLParser):
    """Every attribute name on the first start tag, duplicates included."""

    def __init__(self):
        super().__init__()
        self.names = None

    def handle_starttag(self, tag, attrs):
        if self.names is None:
            self.names = [name for name, _ in attrs]


def root_attribute_names(html):
    parser = _RootAttrs()
    parser.feed(html)
    return parser.names


def footer(soup):
    return soup.find("footer")


class TestFooterRoot:
    def test_the_root_is_a_footer_element_with_the_footer_class(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-footer>Body</c-footer>")

        assert footer(soup) is not None
        assert footer(soup)["class"] == ["footer"]

    def test_caller_classes_and_attributes_reach_the_root(self, cotton_render_string):
        html = cotton_render_string('<c-footer class="p-10" data-x="1" />')

        assert root_attribute_names(html).count("class") == 1
        assert "p-10" in html
        assert 'data-x="1"' in html

    def test_free_form_content_passes_through_unchanged(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-footer><aside><p>Copyright</p></aside></c-footer>"
        )

        assert footer(soup).find("aside").find("p").get_text() == "Copyright"

    def test_a_footer_with_no_nav_renders_its_content(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-footer>Just text</c-footer>")

        assert footer(soup).get_text() == "Just text"
        assert footer(soup).find("nav") is None

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string("<c-footer>Body</c-footer>")

        assert "<script" not in html
        assert " on" not in html.replace("\n", " ").split(">")[0]


class TestFooterDirection:
    def test_horizontal_takes_a_breakpoint(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-footer horizontal="sm" />')

        assert "sm:footer-horizontal" in footer(soup)["class"]
        assert "footer-horizontal" not in footer(soup)["class"]

    def test_bare_horizontal_emits_footer_horizontal(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-footer horizontal />")

        assert "footer-horizontal" in footer(soup)["class"]

    def test_vertical_emits_footer_vertical(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-footer vertical />")

        assert "footer-vertical" in footer(soup)["class"]
        assert "footer-horizontal" not in footer(soup)["class"]

    def test_vertical_with_a_horizontal_breakpoint(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-footer vertical horizontal="sm" />')

        assert "footer-vertical" in footer(soup)["class"]
        assert "sm:footer-horizontal" in footer(soup)["class"]

    def test_an_unknown_breakpoint_adds_no_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-footer horizontal="huge" vertical="x" />')

        assert footer(soup)["class"] == ["footer"]


class TestFooterPlacement:
    def test_center_emits_footer_center(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-footer placement="center" />')

        assert "footer-center" in footer(soup)["class"]

    def test_an_unknown_placement_adds_nothing(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-footer placement="left" />')

        assert footer(soup)["class"] == ["footer"]


class TestFooterNav:
    def test_each_group_is_a_nav_named_by_its_title(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-footer>"
            '<c-footer.nav title="Company"><a>About</a></c-footer.nav>'
            '<c-footer.nav title="Legal"><a>Terms</a></c-footer.nav>'
            "</c-footer>"
        )

        navs = footer(soup).find_all("nav")
        assert [nav["aria-label"] for nav in navs] == ["Company", "Legal"]

    def test_the_title_is_a_span_before_the_slot(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-footer.nav title="Company"><a>About</a></c-footer.nav>'
        )

        nav = soup.find("nav")
        children = nav.find_all(recursive=False)
        assert children[0].name == "span"
        assert children[0]["class"] == ["footer-title"]
        assert children[0].get_text() == "Company"
        assert children[1].name == "a"

    def test_without_a_title_there_is_no_label_and_no_title_span(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-footer.nav><a>About</a></c-footer.nav>")

        nav = soup.find("nav")
        assert not nav.has_attr("aria-label")
        assert nav.find(class_="footer-title") is None
        assert nav.find("a") is not None

    def test_class_and_attributes_reach_the_nav_once(self, cotton_render_string):
        html = cotton_render_string('<c-footer.nav class="gap-2" data-x="1" />')

        assert root_attribute_names(html).count("class") == 1
        assert "gap-2" in html
        assert 'data-x="1"' in html

    def test_the_title_is_not_a_heading(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-footer.nav title="Company" />')

        assert soup.find(["h1", "h2", "h3", "h4", "h5", "h6"]) is None

    def test_no_script_or_event_handler(self, cotton_render_string):
        html = cotton_render_string('<c-footer.nav title="Company" />')

        assert "<script" not in html


class TestFooterIgnoresPageContext:
    def test_footer_ignores_the_pages_placement_and_direction(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-footer />",
            {"placement": "center", "horizontal": True, "vertical": True},
        )

        assert footer(soup)["class"] == ["footer"]

    def test_nav_ignores_the_pages_title(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-footer.nav />", {"title": "Leaked page title"}
        )

        nav = soup.find("nav")
        assert not nav.has_attr("aria-label")
        assert "Leaked" not in soup.get_text()


class TestFooterAnnotations:
    @pytest.fixture
    def footer_parsed(self):
        return AnnotationParser().parse((FOOTER_DIR / "index.html").read_text())

    @pytest.fixture
    def nav_parsed(self):
        return AnnotationParser().parse((FOOTER_DIR / "nav.html").read_text())

    @pytest.mark.parametrize("name", ["horizontal", "vertical"])
    def test_direction_props_are_toggles_that_name_the_breakpoint_form(
        self, footer_parsed, name
    ):
        prop = next(p for p in footer_parsed.props if p.clean_name == name)

        assert prop.type == "boolean"
        assert "breakpoint" in prop.description

    def test_placement_offers_center(self, footer_parsed):
        prop = next(p for p in footer_parsed.props if p.clean_name == "placement")

        assert prop.type == "select"
        assert list(prop.options) == ["center"]

    def test_the_footer_slot_shows_a_copyright_line_and_two_nav_groups(
        self, footer_parsed
    ):
        assert len(footer_parsed.slots) == 1
        content = footer_parsed.slots[0].content
        assert content.count("<c-footer.nav") == 2
        assert "Copyright" in content
        assert " — " not in content

    def test_nav_documents_title_and_class(self, nav_parsed):
        assert {"title", "class"} <= {p.clean_name for p in nav_parsed.props}
        assert len(nav_parsed.slots) == 1
