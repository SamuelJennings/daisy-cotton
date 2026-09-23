"""Tests for the <c-dropdown> component's rendered markup.

Positioning is entirely daisyUI's own CSS — this package layers no JS
placement enhancement on top (README, Scope & philosophy). The classes below
are asserted literally rather than sampled, since they are the whole
positioning contract: a class quietly dropped is a dropdown that opens in
the wrong place with nothing else to catch it.
"""

import pytest
from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


PANEL = '<ul class="menu"><li>an item</li></ul>'

# Every halign/valign pair the component accepts.
PLACEMENTS = [
    ("bottom", "start"),
    ("bottom", "center"),
    ("bottom", "end"),
    ("top", "start"),
    ("top", "center"),
    ("top", "end"),
    ("left", "start"),
    ("left", "center"),
    ("left", "end"),
    ("right", "start"),
    ("right", "center"),
    ("right", "end"),
]

every_pair = pytest.mark.parametrize(
    "valign,halign",
    PLACEMENTS,
    ids=[f"{valign}-{halign}" for valign, halign in PLACEMENTS],
)


class TestDropdownDaisyUIMarkup:
    """The wrapper and panel carry exactly today's daisyUI classes."""

    def test_the_wrapper_renders_todays_classes(self):
        html = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        assert 'class="dropdown dropdown-bottom dropdown-start "' in html

    def test_the_panel_renders_todays_classes(self):
        html = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        assert (
            'class="dropdown-content bg-base-100 rounded-box z-50 min-w-52'
            ' shadow-lg border border-base-300 "'
        ) in html

    @every_pair
    def test_every_accepted_pair_emits_its_daisyui_classes(self, valign, halign):
        html = render(
            f'<c-dropdown valign="{valign}" halign="{halign}">{PANEL}</c-dropdown>'
        )

        assert f'class="dropdown dropdown-{valign} dropdown-{halign} "' in html

    def test_there_is_exactly_one_panel(self):
        html = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        assert html.count("dropdown-content") == 1


class TestDropdownProps:
    """``full``, ``hover``, ``class`` and ``content_class``."""

    def test_full_stretches_the_panel_to_the_trigger(self):
        html = render(f"<c-dropdown full>{PANEL}</c-dropdown>")

        assert "min-w-52 w-full shadow-lg" in html

    def test_without_full_the_panel_sizes_to_its_content(self):
        html = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        assert "w-full" not in html

    def test_hover_marks_the_wrapper(self):
        html = render(f"<c-dropdown hover>{PANEL}</c-dropdown>")

        assert 'class="dropdown dropdown-bottom dropdown-start dropdown-hover "' in html

    def test_without_hover_the_wrapper_is_not_marked(self):
        html = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        assert "dropdown-hover" not in html

    def test_class_lands_on_the_wrapper(self):
        html = render(f'<c-dropdown class="w-full mt-2">{PANEL}</c-dropdown>')

        assert 'class="dropdown dropdown-bottom dropdown-start w-full mt-2"' in html

    def test_content_class_lands_on_the_panel(self):
        html = render(f'<c-dropdown content_class="w-56 mt-4">{PANEL}</c-dropdown>')

        assert "border border-base-300 w-56 mt-4" in html


class TestDropdownTrigger:
    """Both trigger paths, and where extra attributes go in each."""

    def test_extra_attributes_configure_the_default_inner_button(self):
        html = render(
            f'<c-dropdown text="Options" icon="bi bi-gear" variant="primary">{PANEL}'
            "</c-dropdown>"
        )

        assert (
            '<button class="btn btn-primary  inline-flex items-center '
            'justify-center gap-2 " tabindex="0" role="button">'
        ) in html
        assert "<span>Options</span>" in html
        assert 'class="bi bi-gear "' in html
        assert "text=" not in html, (
            "trigger attributes configure the button, so none of them may be "
            "written onto the wrapper as raw HTML"
        )

    def test_a_slot_trigger_is_rendered_as_given(self):
        html = render(
            '<c-dropdown><c-slot name="button">'
            '<div tabindex="0" role="button" class="btn">Menu</div>'
            f"</c-slot>{PANEL}</c-dropdown>"
        )

        assert '<div tabindex="0" role="button" class="btn">Menu</div>' in html
        assert "<button" not in html, (
            "the slot replaces the default trigger rather than adding to it"
        )

    def test_with_a_slot_trigger_extra_attributes_fall_through_to_the_wrapper(self):
        html = render(
            '<c-dropdown id="sort" x-data="{value: 1}">'
            '<c-slot name="button"><button type="button">Sort</button></c-slot>'
            f"{PANEL}</c-dropdown>"
        )

        assert 'id="sort" x-data="{value: 1}">' in html
