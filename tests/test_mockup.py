"""``<c-mockup.browser>``, ``<c-mockup.phone>`` and ``<c-mockup.window>``.

Every mockup merges a caller's ``class`` into its root, passes further
attributes to it, and imposes no layout or literal colour on the content.
"""

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

import daisy_cotton

COTTON_DIR = Path(next(iter(daisy_cotton.__path__))).resolve() / "templates" / "cotton"

# A Tailwind palette colour such as bg-neutral-900 or text-white, which
# ignores the active theme.
LITERAL_COLOUR = re.compile(
    r"\b(?:bg|text|border)-(?:white|black|(?:slate|gray|zinc|neutral|stone|red|orange|amber|"
    r"yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d+)\b"
)

ROOTS = {
    "mockup.browser": "mockup-browser",
    "mockup.phone": "mockup-phone",
    "mockup.window": "mockup-window",
}


class _RootAttrs(HTMLParser):
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


def element_children(tag):
    return [child for child in tag.children if getattr(child, "name", None)]


class TestMockupRoot:
    @pytest.mark.parametrize(("component", "root_class"), ROOTS.items())
    def test_class_is_merged_into_the_root(
        self, cotton_render_string, cotton_render_string_soup, component, root_class
    ):
        source = f'<c-{component} class="my-8">Hi</c-{component}>'

        soup = cotton_render_string_soup(source)

        assert {root_class, "my-8"} <= set(soup.find("div")["class"])
        assert root_attribute_names(cotton_render_string(source)).count("class") == 1

    @pytest.mark.parametrize("component", ROOTS)
    def test_an_extra_attribute_reaches_the_root(
        self, cotton_render_string_soup, component
    ):
        soup = cotton_render_string_soup(
            f'<c-{component} id="preview" data-x="1">Hi</c-{component}>'
        )

        root = soup.find("div")
        assert root["id"] == "preview"
        assert root["data-x"] == "1"

    @pytest.mark.parametrize("component", ROOTS)
    def test_the_slot_is_rendered(self, cotton_render_string_soup, component):
        soup = cotton_render_string_soup(
            f"<c-{component}><p id='body'>Hi</p></c-{component}>"
        )

        assert soup.find(id="body").get_text() == "Hi"

    @pytest.mark.parametrize("component", ROOTS)
    def test_no_script_or_event_handler(self, cotton_render_string, component):
        html = cotton_render_string(f"<c-{component}>Hi</c-{component}>")

        assert "<script" not in html
        assert not re.search(r"\son\w+=", html)

    def test_no_mockup_template_uses_a_literal_colour(self):
        offenders = {
            str(path.relative_to(COTTON_DIR)): LITERAL_COLOUR.findall(path.read_text())
            for path in (COTTON_DIR / "mockup").rglob("*.html")
            if LITERAL_COLOUR.search(path.read_text())
        }

        assert offenders == {}


class TestMockupPhone:
    def test_the_display_follows_the_theme(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-mockup.phone>Hi</c-mockup.phone>")

        display = soup.find(class_="mockup-phone-display")
        assert {"bg-base-100", "text-base-content"} <= set(display["class"])

    def test_the_display_imposes_no_layout_or_literal_colour(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-mockup.phone>Hi</c-mockup.phone>")

        display_classes = set(soup.find(class_="mockup-phone-display")["class"])
        assert not display_classes & {
            "text-white",
            "bg-neutral-900",
            "grid",
            "place-content-center",
        }

    def test_the_camera_is_hidden_from_assistive_technology(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-mockup.phone>Hi</c-mockup.phone>")

        assert soup.find(class_="mockup-phone-camera")["aria-hidden"] == "true"


class TestMockupWindow:
    def test_the_content_sits_in_one_bare_div(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-mockup.window><p id='body'>Hi</p></c-mockup.window>"
        )

        wrappers = element_children(soup.find(class_="mockup-window"))
        assert len(wrappers) == 1
        assert wrappers[0].name == "div"
        assert not wrappers[0].attrs
        assert wrappers[0].find(id="body")

    def test_the_content_area_is_not_sized_or_centred(self, cotton_render_string):
        html = cotton_render_string("<c-mockup.window>Hi</c-mockup.window>")

        for imposed in ("h-80", "grid", "place-content-center"):
            assert imposed not in html


class TestMockupBrowser:
    def test_the_url_shows_in_the_toolbar(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-mockup.browser url="https://example.com">Hi</c-mockup.browser>'
        )

        field = soup.find(class_="mockup-browser-toolbar").find(class_="input")
        assert field.get_text().strip() == "https://example.com"

    def test_the_url_is_not_hidden_from_assistive_technology(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-mockup.browser url="https://example.com">Hi</c-mockup.browser>'
        )

        field = soup.find(class_="input")
        hidden = [
            el for el in [field, *field.parents] if el.get("aria-hidden") == "true"
        ]
        assert hidden == []

    def test_the_content_follows_the_toolbar_in_a_bare_div(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-mockup.browser><p id='body'>Hi</p></c-mockup.browser>"
        )

        toolbar, content = element_children(soup.find(class_="mockup-browser"))
        assert "mockup-browser-toolbar" in toolbar["class"]
        assert content.name == "div"
        assert not content.attrs
        assert content.find(id="body")

    def test_a_page_url_does_not_leak_into_the_address_bar(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-mockup.browser>Hi</c-mockup.browser>", {"url": "/private/"}
        )

        assert soup.find(class_="input").get_text().strip() == ""


class TestMockupAnnotations:
    @pytest.fixture
    def slot_examples(self):
        from django_cotton_gallery.core.annotations import AnnotationParser

        parser = AnnotationParser()
        return {
            path.relative_to(COTTON_DIR / "mockup").as_posix(): next(
                slot.content
                for slot in parser.parse(path.read_text()).slots
                if not slot.name
            )
            for path in (COTTON_DIR / "mockup").rglob("*.html")
        }

    def test_every_mockup_has_a_default_slot_example(self, slot_examples):
        assert sorted(slot_examples) == [
            "browser.html",
            "code/index.html",
            "code/line.html",
            "phone.html",
            "window.html",
        ]
        assert all(slot_examples.values())

    def test_the_code_example_has_a_prompt_line_and_an_output_line(self, slot_examples):
        example = slot_examples["code/index.html"]

        assert 'prefix="$"' in example
        lines = re.findall(r"<c-mockup\.code\.line[^>]*>", example)
        assert len(lines) == 2
        assert sum("prefix=" in line for line in lines) == 1

    def test_every_mockup_declares_class(self):
        from django_cotton_gallery.core.annotations import AnnotationParser

        parser = AnnotationParser()
        for path in (COTTON_DIR / "mockup").rglob("*.html"):
            names = {prop.clean_name for prop in parser.parse(path.read_text()).props}
            assert "class" in names, path.name
