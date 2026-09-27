"""Tests for the <c-modal> component's structure.

Rewritten under decisions.md D2 for daisyUI's own modal shape (FR-012,
FR-014, FR-016): a dialog holding a plain modal-box (no inner card), an
`actions` slot in daisyUI's actions row, `placement` replacing `position`,
and `content_class` for the box. `size`, `position`, `icon`, `footer` and
`footer_end` are removed.
"""

from pathlib import Path

import pytest
from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

compiler = CottonCompiler()

MODAL_TEMPLATE = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "modal.html"
)


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
        assert "modal-box w-11/12" in html


class TestModalNaming:
    """Scenario 1 (naming half): `title` names the dialog for assistive
    technology (FR-013).
    """

    def test_title_renders_as_a_heading_that_names_the_dialog(self):
        html = render('<c-modal id="confirm" title="Delete item?">Body</c-modal>')
        assert '<h2 id="confirm-title"' in html
        assert "Delete item?" in html
        assert 'aria-labelledby="confirm-title"' in html

    def test_no_title_means_no_aria_labelledby(self):
        html = render('<c-modal id="confirm">Body</c-modal>')
        assert "aria-labelledby" not in html

    def test_a_callers_aria_label_reaches_the_dialog_with_no_title(self):
        html = render('<c-modal id="confirm" aria-label="Delete item?">Body</c-modal>')
        assert 'aria-label="Delete item?"' in html

    def test_two_modals_with_different_ids_get_different_heading_ids(self):
        first = render('<c-modal id="one" title="First">Body</c-modal>')
        second = render('<c-modal id="two" title="Second">Body</c-modal>')
        assert '<h2 id="one-title"' in first
        assert '<h2 id="two-title"' in second


class TestModalClosable:
    """Scenario 4: `closable` adds a close button that closes without script."""

    def test_closable_adds_a_close_button_with_the_translatable_name(self):
        html = render('<c-modal id="confirm" closable>Body</c-modal>')
        assert '<form method="dialog"' in html
        assert 'aria-label="Close"' in html
        assert 'aria-hidden="true"' in html

    def test_without_closable_there_is_no_close_button(self):
        html = render('<c-modal id="confirm">Body</c-modal>')
        assert 'aria-label="Close"' not in html


class TestModalTranslatableStrings:
    """Both "Close" strings sit inside {% trans %} in the template source."""

    def test_both_close_strings_are_wrapped_in_trans(self):
        source = MODAL_TEMPLATE.read_text()
        assert source.count('{% trans "Close"') == 2


class TestModalGalleryAnnotations:
    """Article XVI, read through the gallery's own `AnnotationParser` (T006)."""

    @staticmethod
    def _parsed():
        return AnnotationParser().parse(MODAL_TEMPLATE.read_text())

    def test_id_is_required_with_no_default(self):
        prop = next(p for p in self._parsed().props if p.clean_name == "id")
        assert prop.required is True
        assert prop.has_default is False

    def test_placement_is_a_select_of_the_five_placements(self):
        prop = next(p for p in self._parsed().props if p.clean_name == "placement")
        assert prop.type == "select"
        assert set(prop.options) == {"top", "middle", "bottom", "start", "end"}

    def test_open_description_says_it_is_not_modal_and_the_trigger_cannot_reopen_it(
        self,
    ):
        prop = next(p for p in self._parsed().props if p.clean_name == "open")
        assert "not modal" in prop.description
        assert "cannot" in prop.description

    def test_description_says_to_give_title_or_aria_label(self):
        assert "title" in self._parsed().description
        assert "aria-label" in self._parsed().description

    def test_the_default_slot_has_a_body_copy_example(self):
        [slot] = [s for s in self._parsed().slots if s.name is None]
        assert slot.content

    def test_the_actions_slot_example_shows_a_form_with_a_button(self):
        slot = next(s for s in self._parsed().slots if s.name == "actions")
        assert '<form method="dialog">' in slot.content
        assert "<c-button" in slot.content

    def test_the_trigger_calls_showmodal_on_demo_modal(self):
        parsed = self._parsed()
        assert "demo_modal.showModal()" in parsed.trigger
        assert "<c-button" in parsed.trigger

    def test_the_description_tells_the_viewer_to_set_id_and_switch_open_on(self):
        description = self._parsed().description
        assert "demo_modal" in description
        assert "open" in description


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
