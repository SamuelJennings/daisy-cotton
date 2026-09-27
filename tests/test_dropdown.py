"""Tests for the <c-dropdown> component's rendered markup.

Rewritten under decisions.md D2 for daisyUI's popover method (FR-017-FR-020):
a `<c-button>` trigger targets a popover panel through `popovertarget` and
CSS anchor positioning, `placement` replaces `valign`/`halign`, and `full`
and `hover` are removed (the popover method offers neither).
"""

import re

import pytest
from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


PANEL = '<ul class="menu"><li>an item</li></ul>'

# Every side/alignment pair the component accepts.
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
    "side,alignment",
    PLACEMENTS,
    ids=[f"{side}-{alignment}" for side, alignment in PLACEMENTS],
)


def popovertarget_of(html):
    match = re.search(r'popovertarget="([^"]+)"', html)
    assert match, f"no popovertarget found in {html!r}"
    return match.group(1)


def panel_ids(html):
    return re.findall(r'<div id="([^"]+)"\s+popover', html)


class TestDropdownTrigger:
    """Scenario 1: the default trigger is a `<c-button>` targeting the panel."""

    def test_extra_attributes_configure_the_default_inner_button(self):
        html = render(
            f'<c-dropdown text="Options" icon="bi bi-gear" variant="primary">{PANEL}'
            "</c-dropdown>"
        )

        assert '<button class="btn btn-primary  " type="button"' in html
        assert "<span>Options</span>" in html
        assert 'class="bi bi-gear "' in html
        assert "text=" not in html, (
            "trigger attributes configure the button, so none of them may be "
            "written onto the wrapper as raw HTML"
        )

    def test_the_trigger_targets_the_panel_holding_the_slot(self):
        html = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        [panel_id] = panel_ids(html)
        assert popovertarget_of(html) == panel_id
        assert "an item" in html

    def test_a_slot_trigger_replaces_the_default_trigger(self):
        """Scenario 6."""
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
        """`id` is the panel identifier, not a generic passthrough attribute
        under the new contract, so a genuinely undeclared attribute
        (`x-data`) demonstrates the fall-through instead.
        """
        html = render(
            '<c-dropdown x-data="{value: 1}">'
            '<c-slot name="button"><button type="button">Sort</button></c-slot>'
            f"{PANEL}</c-dropdown>"
        )

        assert 'x-data="{value: 1}"' in html.split(">")[0]


class TestDropdownPanelIdentity:
    """Scenario 2: each dropdown links its own trigger to its own panel."""

    def test_two_dropdowns_with_no_id_get_different_panel_ids(self):
        first = render(f"<c-dropdown>{PANEL}</c-dropdown>")
        second = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        [first_panel_id] = panel_ids(first)
        [second_panel_id] = panel_ids(second)
        assert first_panel_id != second_panel_id
        assert popovertarget_of(first) == first_panel_id
        assert popovertarget_of(second) == second_panel_id

    def test_a_callers_id_becomes_the_panel_id(self):
        html = render(f'<c-dropdown id="account-menu">{PANEL}</c-dropdown>')

        assert panel_ids(html) == ["account-menu"]
        assert popovertarget_of(html) == "account-menu"
        assert 'style="anchor-name: --account-menu"' in html
        assert 'style="position-anchor: --account-menu"' in html


class TestDropdownPlacement:
    """Scenario 5: `placement` maps to daisyUI's dropdown placement classes."""

    @every_pair
    def test_every_side_and_alignment_pair_emits_its_daisyui_classes(
        self, side, alignment
    ):
        html = render(
            f'<c-dropdown placement="{side} {alignment}">{PANEL}</c-dropdown>'
        )

        assert f"dropdown-{side}" in html
        assert f"dropdown-{alignment}" in html

    def test_an_unknown_placement_word_emits_no_class_and_does_not_raise(self):
        html = render(f'<c-dropdown placement="diagonal">{PANEL}</c-dropdown>')

        assert "dropdown-diagonal" not in html
        assert "dropdown" in html

    def test_there_is_exactly_one_panel(self):
        html = render(f"<c-dropdown>{PANEL}</c-dropdown>")

        assert len(panel_ids(html)) == 1


class TestDropdownStyleAnchor:
    """SPEC-003: a caller's `style` cannot remove the default trigger's anchor."""

    def test_a_callers_style_leaves_the_anchor_in_place(self):
        html = render(f'<c-dropdown style="color:red">{PANEL}</c-dropdown>')

        [panel_id] = panel_ids(html)
        assert f'style="anchor-name: --{panel_id}"' in html


class TestDropdownClassAndContentClass:
    """D6: the dropdown's own `class` never reaches the trigger it draws."""

    def test_class_lands_on_the_wrapper_and_not_on_the_default_trigger(self):
        html = render(f'<c-dropdown class="mt-4">{PANEL}</c-dropdown>')

        wrapper_open_tag = html.split(">")[0]
        assert "mt-4" in wrapper_open_tag
        button_open_tag = re.search(r"<button[^>]*>", html).group(0)
        assert "mt-4" not in button_open_tag

    def test_content_class_lands_on_the_panel(self):
        html = render(f'<c-dropdown content_class="w-56 mt-4">{PANEL}</c-dropdown>')

        assert "min-w-52 shadow-sm w-56 mt-4" in html


class TestDropdownContextLeak:
    """A page variable of the same name as a declared prop never leaks in
    (research R5, D6).
    """

    def test_a_page_context_button_id_and_placement_do_not_leak_in(self):
        html = render(
            f"<c-dropdown>{PANEL}</c-dropdown>",
            button="<div>Leaked</div>",
            id="leaked-id",
            placement="top",
        )

        assert "Leaked" not in html
        assert "leaked-id" not in html
        assert "dropdown-top" not in html
