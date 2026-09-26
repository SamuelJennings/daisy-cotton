"""Tests for the <c-steps> and <c-steps.step> components.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach ``<c-vars>`` the way they do in a real page.
"""

from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, "html.parser")


class TestStepsRoot:
    """The root is an ordered list carrying daisyUI's steps classes."""

    def test_bare_root_is_an_ol_with_the_steps_class(self, cotton_render_string):
        ol = parse(cotton_render_string("<c-steps>x</c-steps>")).find("ol")
        assert ol is not None
        assert ol["class"] == ["steps"]

    def test_vertical_adds_steps_vertical(self, cotton_render_string):
        ol = parse(cotton_render_string("<c-steps vertical>x</c-steps>")).ol
        assert ol["class"] == ["steps", "steps-vertical"]

    def test_vertical_with_a_horizontal_breakpoint(self, cotton_render_string):
        ol = parse(
            cotton_render_string('<c-steps vertical horizontal="lg">x</c-steps>')
        ).ol
        assert ol["class"] == ["steps", "steps-vertical", "lg:steps-horizontal"]

    def test_horizontal_alone_adds_steps_horizontal(self, cotton_render_string):
        ol = parse(cotton_render_string("<c-steps horizontal>x</c-steps>")).ol
        assert ol["class"] == ["steps", "steps-horizontal"]

    def test_direction_classes_are_absent_by_default(self, cotton_render_string):
        html = cotton_render_string("<c-steps>x</c-steps>")
        assert "steps-vertical" not in html
        assert "steps-horizontal" not in html

    def test_class_and_attributes_reach_the_root(self, cotton_render_string):
        ol = parse(
            cotton_render_string('<c-steps class="mine" id="s" data-x="1">x</c-steps>')
        ).ol
        assert ol["class"] == ["steps", "mine"]
        assert ol["id"] == "s"
        assert ol["data-x"] == "1"

    def test_the_slot_is_rendered_inside(self, cotton_render_string):
        ol = parse(cotton_render_string("<c-steps><li>marker</li></c-steps>")).ol
        assert ol.li.get_text() == "marker"


class TestStep:
    """One step is a list item with a colour, a current marker and content."""

    def test_bare_step_is_a_li_with_the_step_class(self, cotton_render_string):
        li = parse(cotton_render_string('<c-steps.step text="Cart" />')).li
        assert li["class"] == ["step"]
        assert li.get_text(strip=True) == "Cart"

    def test_variant_adds_its_colour_class(self, cotton_render_string):
        li = parse(
            cotton_render_string('<c-steps.step variant="primary" text="A" />')
        ).li
        assert li["class"] == ["step", "step-primary"]

    def test_every_daisyui_colour_is_accepted(self, cotton_render_string):
        for colour in (
            "neutral",
            "primary",
            "secondary",
            "accent",
            "info",
            "success",
            "warning",
            "error",
        ):
            li = parse(
                cotton_render_string(f'<c-steps.step variant="{colour}" text="A" />')
            ).li
            assert f"step-{colour}" in li["class"]

    def test_unknown_variant_adds_no_class(self, cotton_render_string):
        li = parse(
            cotton_render_string('<c-steps.step variant="purple" text="A" />')
        ).li
        assert li["class"] == ["step"]

    def test_current_marks_the_step(self, cotton_render_string):
        on = parse(cotton_render_string('<c-steps.step text="A" current />')).li
        off = parse(cotton_render_string('<c-steps.step text="A" />')).li
        assert on["aria-current"] == "step"
        assert not off.has_attr("aria-current")

    def test_content_becomes_data_content_only_when_given(self, cotton_render_string):
        with_content = parse(
            cotton_render_string('<c-steps.step text="A" content="★" />')
        ).li
        without = parse(cotton_render_string('<c-steps.step text="A" />')).li
        assert with_content["data-content"] == "★"
        assert not without.has_attr("data-content")

    def test_icon_sits_in_a_step_icon_span_hidden_from_assistive_tech(
        self, cotton_render_string
    ):
        li = parse(cotton_render_string('<c-steps.step text="A" icon="fa-check" />')).li
        holder = li.find("span", class_="step-icon")
        assert holder is not None
        icon = holder.find(class_="fa-check")
        assert icon is not None
        assert icon["aria-hidden"] == "true"

    def test_no_icon_span_without_an_icon(self, cotton_render_string):
        html = cotton_render_string('<c-steps.step text="A" />')
        assert "step-icon" not in html

    def test_the_step_class_does_not_reach_the_icon(self, cotton_render_string):
        li = parse(
            cotton_render_string(
                '<c-steps.step text="A" icon="fa-check" class="mine" />'
            )
        ).li
        assert "mine" in li["class"]
        assert "mine" not in li.find(class_="fa-check")["class"]

    def test_attributes_reach_the_li(self, cotton_render_string):
        li = parse(cotton_render_string('<c-steps.step text="A" data-x="1" />')).li
        assert li["data-x"] == "1"

    def test_the_slot_follows_the_text(self, cotton_render_string):
        li = parse(
            cotton_render_string('<c-steps.step text="A"><b>m</b></c-steps.step>')
        ).li
        assert li.b.get_text() == "m"

    def test_a_step_sits_inside_the_list(self, cotton_render_string):
        ol = parse(
            cotton_render_string('<c-steps><c-steps.step text="A" /></c-steps>')
        ).ol
        assert ol.li["class"] == ["step"]
