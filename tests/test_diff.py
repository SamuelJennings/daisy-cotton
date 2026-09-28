"""Tests for the <c-diff> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestDiffRoot:
    """The diff is a figure holding both items and an empty resizer, in order."""

    def test_root_carries_diff_class_and_tabindex(self, cotton_render_string):
        html = cotton_render_string(
            "<c-diff>"
            '<c-slot name="item_1">A</c-slot>'
            '<c-slot name="item_2">B</c-slot>'
            "</c-diff>"
        )
        figure = parse(html).figure
        assert figure["class"] == ["diff"]
        assert figure["tabindex"] == "0"

    def test_children_are_diff_item_1_diff_item_2_and_diff_resizer_in_order(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            "<c-diff>"
            '<c-slot name="item_1">A</c-slot>'
            '<c-slot name="item_2">B</c-slot>'
            "</c-diff>"
        )
        children = parse(html).figure.find_all("div", recursive=False)
        assert [child["class"] for child in children] == [
            ["diff-item-1"],
            ["diff-item-2"],
            ["diff-resizer"],
        ]

    def test_item_1_carries_tabindex_and_holds_its_content(self, cotton_render_string):
        html = cotton_render_string(
            "<c-diff>"
            '<c-slot name="item_1"><b>A</b></c-slot>'
            '<c-slot name="item_2">B</c-slot>'
            "</c-diff>"
        )
        item_1 = parse(html).find(class_="diff-item-1")
        assert item_1["tabindex"] == "0"
        assert item_1.b.get_text() == "A"

    def test_item_2_holds_its_content_and_carries_no_tabindex(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            "<c-diff>"
            '<c-slot name="item_1">A</c-slot>'
            '<c-slot name="item_2"><b>B</b></c-slot>'
            "</c-diff>"
        )
        item_2 = parse(html).find(class_="diff-item-2")
        assert not item_2.has_attr("tabindex")
        assert item_2.b.get_text() == "B"

    def test_diff_resizer_is_empty(self, cotton_render_string):
        html = cotton_render_string(
            "<c-diff>"
            '<c-slot name="item_1">A</c-slot>'
            '<c-slot name="item_2">B</c-slot>'
            "</c-diff>"
        )
        resizer = parse(html).find(class_="diff-resizer")
        assert resizer.get_text() == ""
        assert len(resizer.contents) == 0

    def test_aria_label_is_written_once_when_given(self, cotton_render_string):
        html = cotton_render_string('<c-diff aria-label="Before and after">x</c-diff>')
        assert html.count("aria-label=") == 1
        assert parse(html).figure["aria-label"] == "Before and after"

    def test_no_aria_label_emits_none(self, cotton_render_string):
        html = cotton_render_string("<c-diff>x</c-diff>")
        assert "aria-label=" not in html

    def test_class_and_data_id_land_on_the_figure(self, cotton_render_string):
        figure = parse(
            cotton_render_string('<c-diff class="aspect-16/9" data-id="7">x</c-diff>')
        ).figure
        assert "aspect-16/9" in figure["class"]
        assert figure["data-id"] == "7"


class TestDiffNoRoleOrAriaHidden:
    """Both items stay in the accessibility tree (research R4, D1)."""

    def test_no_element_carries_role_img(self, cotton_render_string):
        html = cotton_render_string(
            "<c-diff>"
            '<c-slot name="item_1">A</c-slot>'
            '<c-slot name="item_2">B</c-slot>'
            "</c-diff>"
        )
        assert parse(html).find(attrs={"role": "img"}) is None

    def test_no_element_carries_aria_hidden(self, cotton_render_string):
        html = cotton_render_string(
            "<c-diff>"
            '<c-slot name="item_1">A</c-slot>'
            '<c-slot name="item_2">B</c-slot>'
            "</c-diff>"
        )
        assert parse(html).find(attrs={"aria-hidden": True}) is None


class TestDiffPageContext:
    """Page variables named like the diff's props never leak in."""

    def test_page_item_1_item_2_and_aria_label_do_not_leak(self, cotton_render_string):
        html = cotton_render_string(
            "<c-diff>x</c-diff>",
            {
                "item_1": "Leaked",
                "item_2": "Leaked",
                "aria_label": "Leaked",
            },
        )
        soup = parse(html)
        assert not soup.find(class_="diff-item-1").get_text()
        assert not soup.find(class_="diff-item-2").get_text()
        assert not soup.figure.has_attr("aria-label")
