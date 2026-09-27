"""Tests for the <c-modal> component's structure.

Rewritten under decisions.md D2 for daisyUI's own modal shape (FR-012,
FR-014, FR-016): a dialog holding a plain modal-box (no inner card), an
`actions` slot in daisyUI's actions row, `placement` replacing `position`,
and `content_class` for the box. `size`, `position`, `icon`, `footer` and
`footer_end` are removed.
"""

import pytest
from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


PLACEMENTS = ["top", "middle", "bottom", "start", "end"]


class TestModalStructure:
    """Scenario 1 (structure half): a dialog with the caller's id and class,
    its box holding the body.
    """

    def test_dialog_carries_the_callers_id_and_the_modal_class(self):
        html = render('<c-modal id="confirm">Body</c-modal>')
        assert '<dialog id="confirm"' in html
        assert 'class="modal ' in html

    def test_the_box_holds_the_default_slot(self):
        html = render('<c-modal id="confirm">Delete item?</c-modal>')
        assert "modal-box" in html
        assert "Delete item?" in html


class TestModalActions:
    """Scenario 2: an `actions` slot renders in daisyUI's trailing actions row."""

    def test_actions_slot_renders_in_the_actions_row(self):
        html = render(
            '<c-modal id="confirm">Body<c-slot name="actions">'
            "<button>OK</button></c-slot></c-modal>"
        )
        assert '<div class="modal-action">' in html
        assert "<button>OK</button>" in html

    def test_no_actions_given_renders_no_actions_row(self):
        html = render('<c-modal id="confirm">Body</c-modal>')
        assert "modal-action" not in html


class TestModalPlacement:
    """Scenario 3: `placement` maps to daisyUI's modal placement classes."""

    @pytest.mark.parametrize("placement", PLACEMENTS)
    def test_every_placement_emits_its_daisyui_class(self, placement):
        html = render(f'<c-modal id="confirm" placement="{placement}">Body</c-modal>')
        assert f"modal-{placement}" in html

    def test_an_unknown_placement_emits_no_class_and_does_not_raise(self):
        html = render('<c-modal id="confirm" placement="diagonal">Body</c-modal>')
        assert "modal-diagonal" not in html
        assert "<dialog" in html


class TestModalOpen:
    """Scenario 6: `open` renders the dialog already shown."""

    def test_open_renders_the_open_attribute(self):
        html = render('<c-modal id="confirm" open>Body</c-modal>')
        assert "<dialog" in html
        assert " open" in html.split(">")[0]

    def test_without_open_the_dialog_is_not_shown(self):
        html = render('<c-modal id="confirm">Body</c-modal>')
        assert " open" not in html.split(">")[0]


class TestModalClassAndContentClass:
    def test_class_lands_on_the_dialog(self):
        html = render('<c-modal id="confirm" class="my-modal">Body</c-modal>')
        assert "my-modal" in html.split(">")[0]

    def test_content_class_lands_on_the_box(self):
        html = render('<c-modal id="confirm" content_class="w-11/12">Body</c-modal>')
        assert 'modal-box w-11/12' in html


class TestModalContextLeak:
    """A page variable of the same name as a declared prop never leaks in
    (research R5, D6).
    """

    def test_a_page_context_title_actions_and_open_do_not_leak_in(self):
        html = render(
            '<c-modal id="confirm">Body</c-modal>',
            title="Leaked heading",
            actions="<button>Leaked</button>",
            open=True,
        )
        assert "Leaked heading" not in html
        assert "Leaked" not in html
        assert " open" not in html.split(">")[0]
