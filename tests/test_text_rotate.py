"""Tests for the <c-text-rotate> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestTextRotateRoot:
    def test_root_carries_text_rotate_class_and_the_callers_class(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-text-rotate class="text-5xl">'
            "<span>One</span><span>Two</span><span>Three</span>"
            "</c-text-rotate>"
        )
        root = parse(html).find("span", class_="text-rotate")
        assert root["class"] == ["text-rotate", "text-5xl"]

    def test_inner_span_holds_the_lines_in_order(self, cotton_render_string):
        html = cotton_render_string(
            "<c-text-rotate>"
            "<span>One</span><span>Two</span><span>Three</span>"
            "</c-text-rotate>"
        )
        root = parse(html).find("span", class_="text-rotate")
        inner = root.find("span", recursive=False)
        lines = inner.find_all("span", recursive=False)
        assert [line.get_text() for line in lines] == ["One", "Two", "Three"]

    def test_content_class_lands_on_the_inner_span(self, cotton_render_string):
        html = cotton_render_string(
            '<c-text-rotate content_class="justify-items-center">'
            "<span>One</span><span>Two</span>"
            "</c-text-rotate>"
        )
        root = parse(html).find("span", class_="text-rotate")
        inner = root.find("span", recursive=False)
        assert inner["class"] == ["justify-items-center"]

    def test_inner_span_has_no_class_attribute_without_content_class(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            "<c-text-rotate><span>One</span><span>Two</span></c-text-rotate>"
        )
        root = parse(html).find("span", class_="text-rotate")
        inner = root.find("span", recursive=False)
        assert not inner.has_attr("class")

    def test_class_and_data_id_land_on_the_root(self, cotton_render_string):
        root = parse(
            cotton_render_string(
                '<c-text-rotate class="text-5xl" data-id="7">'
                "<span>One</span><span>Two</span>"
                "</c-text-rotate>"
            )
        ).find("span", class_="text-rotate")
        assert "text-5xl" in root["class"]
        assert root["data-id"] == "7"


class TestTextRotateNoAriaHidden:
    def test_no_element_carries_aria_hidden(self, cotton_render_string):
        html = cotton_render_string(
            "<c-text-rotate><span>One</span><span>Two</span></c-text-rotate>"
        )
        assert parse(html).find(attrs={"aria-hidden": True}) is None


class TestTextRotatePageContext:
    def test_page_content_class_does_not_leak(self, cotton_render_string):
        html = cotton_render_string(
            "<c-text-rotate><span>One</span><span>Two</span></c-text-rotate>",
            {"content_class": "Leaked"},
        )
        root = parse(html).find("span", class_="text-rotate")
        inner = root.find("span", recursive=False)
        assert not inner.has_attr("class")

    def test_page_class_does_not_leak(self, cotton_render_string):
        html = cotton_render_string(
            "<c-text-rotate><span>One</span><span>Two</span></c-text-rotate>",
            {"class": "Leaked"},
        )
        root = parse(html).find("span", class_="text-rotate")
        assert "Leaked" not in root["class"]
