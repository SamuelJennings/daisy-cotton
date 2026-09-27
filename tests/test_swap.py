"""Tests for the <c-swap> component's rendered markup (FR-021-FR-023).

A checkbox-driven swap: a wrapper carrying `swap`, a checkbox that carries
the control's state, form attributes and accessible name, and `on`/`off`/
`indeterminate` slots in `swap-on`/`swap-off`/`swap-indeterminate`.
"""

from pathlib import Path

from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

SWAP_TEMPLATE = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "swap.html"
)


def _checkbox_tag(html):
    start = html.index("<input")
    end = html.index("/>", start) + 2
    return html[start:end]


class TestSwapStructure:
    """Scenario 1: the wrapper, checkbox and on/off slots."""

    def test_renders_the_wrapper_checkbox_and_on_off_slots(self, cotton_render_string):
        html = cotton_render_string(
            '<c-swap label="Dark mode"><c-slot name="on">🌙</c-slot>'
            '<c-slot name="off">☀️</c-slot></c-swap>'
        )

        assert "<label" in html
        assert "swap" in html
        assert "<input" in html
        assert 'type="checkbox"' in _checkbox_tag(html)
        assert 'aria-label="Dark mode"' in _checkbox_tag(html)
        assert '<div class="swap-on">🌙</div>' in html
        assert '<div class="swap-off">☀️</div>' in html


class TestSwapModifiers:
    """Scenarios 3-4: rotate, flip and active map to their wrapper classes."""

    def test_rotate_applies_to_the_wrapper(self, cotton_render_string):
        html = cotton_render_string("<c-swap rotate />")
        assert "swap-rotate" in html

    def test_flip_applies_to_the_wrapper(self, cotton_render_string):
        html = cotton_render_string("<c-swap flip />")
        assert "swap-flip" in html

    def test_active_applies_to_the_wrapper(self, cotton_render_string):
        html = cotton_render_string("<c-swap active />")
        assert "swap-active" in html

    def test_none_of_these_apply_without_being_given(self, cotton_render_string):
        html = cotton_render_string("<c-swap />")
        assert "swap-rotate" not in html
        assert "swap-flip" not in html
        assert "swap-active" not in html


class TestSwapIndeterminate:
    """Scenario 5: the indeterminate slot sits in swap-indeterminate, and only
    when given."""

    def test_indeterminate_slot_renders_in_its_own_div(self, cotton_render_string):
        html = cotton_render_string(
            '<c-swap><c-slot name="indeterminate">-</c-slot></c-swap>'
        )
        assert '<div class="swap-indeterminate">-</div>' in html

    def test_no_indeterminate_slot_renders_no_indeterminate_div(
        self, cotton_render_string
    ):
        html = cotton_render_string("<c-swap />")
        assert "swap-indeterminate" not in html


class TestSwapCheckboxAttributes:
    """Scenario 6: checked, name, value and disabled land on the checkbox,
    never the wrapper; anything else lands on the wrapper."""

    def test_checked_name_and_value_land_on_the_checkbox(self, cotton_render_string):
        html = cotton_render_string('<c-swap checked name="theme" value="dark" />')
        checkbox = _checkbox_tag(html)

        assert "checked" in checkbox
        assert 'name="theme"' in checkbox
        assert 'value="dark"' in checkbox

    def test_disabled_lands_on_the_checkbox(self, cotton_render_string):
        html = cotton_render_string("<c-swap disabled />")
        assert "disabled" in _checkbox_tag(html)

    def test_input_class_lands_on_the_checkbox(self, cotton_render_string):
        html = cotton_render_string('<c-swap input_class="theme-controller" />')
        assert "theme-controller" in _checkbox_tag(html)

    def test_name_and_value_never_reach_the_wrapper(self, cotton_render_string):
        html = cotton_render_string('<c-swap name="theme" value="dark" />')
        wrapper_open_tag = html.split(">")[0]

        assert "theme" not in wrapper_open_tag
        assert "dark" not in wrapper_open_tag

    def test_an_undeclared_attribute_lands_on_the_wrapper(self, cotton_render_string):
        html = cotton_render_string('<c-swap data-test="x" />')
        wrapper_open_tag = html.split(">")[0]

        assert 'data-test="x"' in wrapper_open_tag
        assert "data-test" not in _checkbox_tag(html)


class TestSwapGalleryAnnotations:
    """Article XVI, read through the gallery's own `AnnotationParser`."""

    @staticmethod
    def _parsed():
        return AnnotationParser().parse(SWAP_TEMPLATE.read_text())

    def test_every_declared_name_has_its_own_prop(self):
        names = {p.clean_name for p in self._parsed().props}
        assert names == {
            "label",
            "rotate",
            "flip",
            "active",
            "checked",
            "disabled",
            "name",
            "value",
            "input_class",
            "on",
            "off",
            "indeterminate",
            "class",
        }

    def test_on_off_and_indeterminate_each_have_a_named_slot(self):
        names = {s.name for s in self._parsed().slots}
        assert {"on", "off", "indeterminate"} <= names


class TestSwapContextLeak:
    """A page variable of the same name as a declared prop never leaks in
    (research R5, D6): every declared name gets an empty default."""

    def test_a_page_context_on_off_and_label_do_not_leak_in(self, cotton_render_string):
        html = cotton_render_string(
            "<c-swap />",
            context={
                "on": "Leaked on",
                "off": "Leaked off",
                "label": "Leaked label",
            },
        )

        assert "Leaked on" not in html
        assert "Leaked off" not in html
        assert "Leaked label" not in html
