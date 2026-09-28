"""Tests for the <c-hover-gallery> component.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestHoverGalleryRoot:
    """The gallery is a figure holding the slotted images in order, with no width of its own."""

    def test_root_carries_hover_gallery_class_and_the_callers_class(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-hover-gallery class="max-w-60">'
            '<img src="/a.jpg" alt="A">'
            '<img src="/b.jpg" alt="B">'
            "</c-hover-gallery>"
        )
        figure = parse(html).figure
        assert figure["class"] == ["hover-gallery", "max-w-60"]

    def test_root_adds_no_width_class_of_its_own(self, cotton_render_string):
        html = cotton_render_string(
            '<c-hover-gallery><img src="/a.jpg" alt="A"></c-hover-gallery>'
        )
        figure = parse(html).figure
        assert figure["class"] == ["hover-gallery"]

    def test_slotted_images_render_in_order(self, cotton_render_string):
        html = cotton_render_string(
            "<c-hover-gallery>"
            '<img src="/a.jpg" alt="A">'
            '<img src="/b.jpg" alt="B">'
            '<img src="/c.jpg" alt="C">'
            "</c-hover-gallery>"
        )
        images = parse(html).figure.find_all("img")
        assert [img["alt"] for img in images] == ["A", "B", "C"]

    def test_class_and_data_id_land_on_the_figure(self, cotton_render_string):
        figure = parse(
            cotton_render_string(
                '<c-hover-gallery class="max-w-60" data-id="7">'
                '<img src="/a.jpg" alt="A"></c-hover-gallery>'
            )
        ).figure
        assert "max-w-60" in figure["class"]
        assert figure["data-id"] == "7"


class TestHoverGalleryNoAriaHidden:
    """Every image stays in the accessibility tree; only the hover effect needs a pointer."""

    def test_figure_carries_no_aria_hidden(self, cotton_render_string):
        html = cotton_render_string(
            '<c-hover-gallery><img src="/a.jpg" alt="A"></c-hover-gallery>'
        )
        assert not parse(html).figure.has_attr("aria-hidden")

    def test_no_image_carries_aria_hidden(self, cotton_render_string):
        html = cotton_render_string(
            "<c-hover-gallery>"
            '<img src="/a.jpg" alt="A">'
            '<img src="/b.jpg" alt="B">'
            "</c-hover-gallery>"
        )
        assert parse(html).find("img", attrs={"aria-hidden": True}) is None


class TestHoverGalleryPageContext:
    """A page variable named class never leaks into the gallery."""

    def test_page_class_does_not_leak(self, cotton_render_string):
        html = cotton_render_string(
            '<c-hover-gallery><img src="/a.jpg" alt="A"></c-hover-gallery>',
            {"class": "Leaked"},
        )
        figure = parse(html).figure
        assert "Leaked" not in figure["class"]
