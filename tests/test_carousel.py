"""Tests for the <c-carousel> and <c-carousel.item> components.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup
from django.template import base as template_base


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestCarouselRoot:
    """The carousel is a focusable, named region carrying daisyUI's class only."""

    def test_root_is_a_region_with_carousel_class_and_tabindex(
        self, cotton_render_string
    ):
        div = parse(
            cotton_render_string('<c-carousel aria-label="Photos">x</c-carousel>')
        ).div
        assert div["class"] == ["carousel"]
        assert div["role"] == "region"
        assert div["tabindex"] == "0"

    def test_root_has_the_carousel_roledescription(self, cotton_render_string):
        div = parse(
            cotton_render_string('<c-carousel aria-label="Photos">x</c-carousel>')
        ).div
        assert div["aria-roledescription"] == "carousel"

    def test_aria_label_is_written_when_given(self, cotton_render_string):
        html = cotton_render_string('<c-carousel aria-label="Photos">x</c-carousel>')
        assert html.count("aria-label=") == 1
        assert parse(html).div["aria-label"] == "Photos"

    def test_dynamic_aria_label_is_written_once(self, cotton_render_string):
        html = cotton_render_string(
            '<c-carousel :aria-label="title">x</c-carousel>', {"title": "Photos"}
        )
        assert html.count("aria-label=") == 1
        assert parse(html).div["aria-label"] == "Photos"

    def test_no_aria_label_emits_none(self, cotton_render_string):
        html = cotton_render_string("<c-carousel>x</c-carousel>")
        assert "aria-label=" not in html

    def test_children_carry_carousel_item_role_group_and_roledescription(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-carousel aria-label="Photos">'
            "<c-carousel.item>1</c-carousel.item>"
            "<c-carousel.item>2</c-carousel.item>"
            "<c-carousel.item>3</c-carousel.item>"
            "</c-carousel>"
        )
        items = parse(html).find_all(attrs={"role": "group"})
        assert len(items) == 3
        for item in items:
            assert "carousel-item" in item["class"]
            assert item["aria-roledescription"] == "slide"

    def test_single_slide_carousel_is_still_focusable_and_named(
        self, cotton_render_string
    ):
        div = parse(
            cotton_render_string(
                '<c-carousel aria-label="Photo">'
                "<c-carousel.item>1</c-carousel.item>"
                "</c-carousel>"
            )
        ).div
        assert div["tabindex"] == "0"
        assert div["aria-label"] == "Photo"

    def test_slot_content_is_rendered_inside(self, cotton_render_string):
        div = parse(cotton_render_string("<c-carousel><b>marker</b></c-carousel>")).div
        assert div.b.get_text() == "marker"


class TestCarouselSnap:
    """``snap`` maps to daisyUI's alignment classes."""

    def test_start_maps_to_carousel_start(self, cotton_render_string):
        div = parse(cotton_render_string('<c-carousel snap="start">x</c-carousel>')).div
        assert div["class"] == ["carousel", "carousel-start"]

    def test_center_maps_to_carousel_center(self, cotton_render_string):
        div = parse(
            cotton_render_string('<c-carousel snap="center">x</c-carousel>')
        ).div
        assert div["class"] == ["carousel", "carousel-center"]

    def test_end_maps_to_carousel_end(self, cotton_render_string):
        div = parse(cotton_render_string('<c-carousel snap="end">x</c-carousel>')).div
        assert div["class"] == ["carousel", "carousel-end"]

    def test_unknown_snap_adds_no_class(self, cotton_render_string):
        div = parse(
            cotton_render_string('<c-carousel snap="middle">x</c-carousel>')
        ).div
        assert div["class"] == ["carousel"]


class TestCarouselDirection:
    """``horizontal`` and ``vertical`` go through the ``responsive`` tag."""

    def test_bare_vertical_gives_the_class(self, cotton_render_string):
        div = parse(cotton_render_string("<c-carousel vertical>x</c-carousel>")).div
        assert div["class"] == ["carousel", "carousel-vertical"]

    def test_bare_horizontal_gives_the_class(self, cotton_render_string):
        div = parse(cotton_render_string("<c-carousel horizontal>x</c-carousel>")).div
        assert div["class"] == ["carousel", "carousel-horizontal"]

    def test_horizontal_breakpoint_gives_the_responsive_class(
        self, cotton_render_string
    ):
        div = parse(
            cotton_render_string('<c-carousel horizontal="md">x</c-carousel>')
        ).div
        assert div["class"] == ["carousel", "md:carousel-horizontal"]

    def test_vertical_left_adds_no_class(self, cotton_render_string):
        div = parse(
            cotton_render_string('<c-carousel vertical="left">x</c-carousel>')
        ).div
        assert div["class"] == ["carousel"]


class TestCarouselTranslation:
    """The roledescriptions are wrapped for translation, not hard-coded strings.

    ``{% trans %}`` marks its argument for translation by setting
    ``FilterExpression.translate`` and resolving it through
    ``django.template.base.gettext_lazy`` (see ``FilterExpression.resolve``).
    Patching that name, with no .po/.mo catalog involved, proves the
    roledescriptions are template-tag output rather than a literal string:
    a hard-coded ``aria-roledescription="carousel"`` would still read
    "carousel" here, not the patched marker.
    """

    def test_roledescriptions_are_resolved_through_gettext(
        self, cotton_render_string, monkeypatch
    ):
        monkeypatch.setattr(
            template_base, "gettext_lazy", lambda message: f"[t]{message}[/t]"
        )
        html = cotton_render_string(
            '<c-carousel aria-label="Photos">'
            "<c-carousel.item>1</c-carousel.item>"
            "</c-carousel>"
        )
        soup = parse(html)
        assert soup.div["aria-roledescription"] == "[t]carousel[/t]"
        assert soup.find(attrs={"role": "group"})["aria-roledescription"] == (
            "[t]slide[/t]"
        )


class TestCarouselPageContext:
    """Page variables named like the carousel's props never leak in."""

    def test_page_snap_vertical_and_aria_label_do_not_leak(self, cotton_render_string):
        html = cotton_render_string(
            "<c-carousel>x</c-carousel>",
            {"snap": "center", "vertical": True, "aria_label": "Leaked"},
        )
        div = parse(html).div
        assert div["class"] == ["carousel"]
        assert not div.has_attr("aria-label")


class TestCarouselItem:
    """The item is a carousel-item group carrying the slide roledescription."""

    def test_root_carries_carousel_item_and_role_group(self, cotton_render_string):
        item = parse(cotton_render_string("<c-carousel.item>x</c-carousel.item>")).div
        assert item["class"] == ["carousel-item"]
        assert item["role"] == "group"

    def test_root_has_the_slide_roledescription(self, cotton_render_string):
        item = parse(cotton_render_string("<c-carousel.item>x</c-carousel.item>")).div
        assert item["aria-roledescription"] == "slide"

    def test_id_and_class_land_on_the_slide(self, cotton_render_string):
        item = parse(
            cotton_render_string(
                '<c-carousel.item id="slide2" class="w-full">x</c-carousel.item>'
            )
        ).div
        assert item["id"] == "slide2"
        assert "w-full" in item["class"]

    def test_slot_content_is_rendered_inside(self, cotton_render_string):
        item = parse(
            cotton_render_string("<c-carousel.item><b>marker</b></c-carousel.item>")
        ).div
        assert item.b.get_text() == "marker"
