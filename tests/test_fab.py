"""Tests for the <c-fab> component's rendered markup (FR-025-FR-027).

A floating action button: a wrapper carrying `fab`, a large circular
trigger drawn by `<c-button>`, and further actions as its default slot's
direct children.
"""

import re
from pathlib import Path

from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

FAB_TEMPLATE = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "fab.html"
)

ACTIONS = (
    '<c-button circle icon="bi bi-envelope" aria-label="Mail" />'
    '<c-button circle icon="bi bi-bell" aria-label="Notifications" />'
)


class TestFabTrigger:
    """Scenario 1: the wrapper, its default trigger and the actions."""

    def test_renders_the_wrapper_trigger_and_actions(self, cotton_render_string):
        html = cotton_render_string(
            f'<c-fab icon="bi bi-plus-lg" aria-label="Actions">{ACTIONS}</c-fab>'
        )

        wrapper_open_tag = html.split(">")[0]
        assert "fab" in wrapper_open_tag
        assert '<button class="btn  btn-lg btn-circle "' in html
        assert 'tabindex="0"' in html
        assert 'type="button"' in html
        assert 'class="bi bi-plus-lg "' in html
        assert 'aria-label="Actions"' in html
        assert "Mail" in html or 'aria-label="Mail"' in html
        assert 'aria-label="Notifications"' in html

    def test_a_callers_size_and_variant_override_the_default_trigger(
        self, cotton_render_string
    ):
        """research R4: :attrs wins over the literals written before it."""
        html = cotton_render_string('<c-fab size="md" variant="primary" />')

        assert "btn-md" in html
        assert "btn-lg" not in html
        assert "btn-primary" in html


class TestFabNoActions:
    """Scenario 3: a FAB with no actions is a single floating button."""

    def test_a_fab_with_no_actions_is_only_the_trigger(self, cotton_render_string):
        html = cotton_render_string("<c-fab />")

        assert "<button" in html
        assert "fab-close" not in html
        assert "fab-main-action" not in html


class TestFabFlower:
    """Scenario 4: flower maps to fab-flower on the wrapper."""

    def test_flower_applies_to_the_wrapper(self, cotton_render_string):
        html = cotton_render_string("<c-fab flower />")
        assert "fab-flower" in html

    def test_no_flower_emits_no_class(self, cotton_render_string):
        html = cotton_render_string("<c-fab />")
        assert "fab-flower" not in html


class TestFabCloseAndMainAction:
    """Scenario 5: close and main_action slots render in their own divs,
    only when given."""

    def test_close_slot_renders_in_its_own_div(self, cotton_render_string):
        html = cotton_render_string(
            '<c-fab><c-slot name="close">'
            '<c-button circle icon="bi bi-x-lg" aria-label="Close" />'
            "</c-slot></c-fab>"
        )
        assert '<div class="fab-close">' in html
        assert 'aria-label="Close"' in html

    def test_main_action_slot_renders_in_its_own_div(self, cotton_render_string):
        html = cotton_render_string(
            '<c-fab><c-slot name="main_action">'
            '<div>Compose <c-button circle icon="bi bi-pencil" aria-label="Compose" /></div>'
            "</c-slot></c-fab>"
        )
        assert '<div class="fab-main-action">' in html
        assert "Compose" in html


class TestFabCustomTrigger:
    """Scenario 6: a button slot replaces the default trigger."""

    def test_a_slot_trigger_replaces_the_default_trigger(self, cotton_render_string):
        html = cotton_render_string(
            '<c-fab><c-slot name="button">'
            '<div tabindex="0" role="button" class="btn btn-circle btn-lg">Menu</div>'
            "</c-slot></c-fab>"
        )

        assert (
            '<div tabindex="0" role="button" class="btn btn-circle btn-lg">Menu</div>'
            in html
        )
        assert "<button" not in html

    def test_with_a_slot_trigger_extra_attributes_fall_through_to_the_wrapper(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-fab x-data="{open: false}">'
            '<c-slot name="button"><button type="button" tabindex="0">Menu</button></c-slot>'
            "</c-fab>"
        )
        assert 'x-data="{open: false}"' in html.split(">")[0]


class TestFabClassAndWrapper:
    """D6: the FAB's own class never reaches the trigger it draws."""

    def test_class_lands_on_the_wrapper_and_not_on_the_default_trigger(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-fab class="bottom-4 end-4" />')

        wrapper_open_tag = html.split(">")[0]
        assert "bottom-4 end-4" in wrapper_open_tag
        button_open_tag = re.search(r"<button[^>]*>", html).group(0)
        assert "bottom-4 end-4" not in button_open_tag


class TestFabGalleryAnnotations:
    """Article XVI, read through the gallery's own `AnnotationParser`."""

    @staticmethod
    def _parsed():
        return AnnotationParser().parse(FAB_TEMPLATE.read_text())

    def test_every_declared_name_has_its_own_prop(self):
        names = {p.clean_name for p in self._parsed().props}
        assert names == {"flower", "close", "main_action", "button", "class"}

    def test_close_main_action_and_button_each_have_a_named_slot(self):
        slots = {s.name: s for s in self._parsed().slots}
        assert {"close", "main_action", "button"} <= set(slots)

    def test_close_and_main_action_have_no_example_and_give_the_markup(self):
        slots = {s.name: s for s in self._parsed().slots}
        assert slots["close"].content == ""
        assert "c-button" in slots["close"].description
        assert slots["main_action"].content == ""
        assert "c-button" in slots["main_action"].description

    def test_the_button_slot_names_the_focusability_contract(self):
        slot = next(s for s in self._parsed().slots if s.name == "button")
        assert "focusable" in slot.description
        assert "tabindex" in slot.description

    def test_the_default_slot_has_three_action_examples(self):
        [slot] = [s for s in self._parsed().slots if s.name is None]
        assert slot.content.count("<c-button") == 3

    def test_the_description_tells_the_viewer_to_type_the_trigger_attributes(self):
        assert 'icon="bi bi-plus-lg"' in self._parsed().description
        assert 'aria-label="Actions"' in self._parsed().description


class TestFabContextLeak:
    """A page variable of the same name as a declared prop never leaks in
    (research R5, D6): every declared name gets an empty default."""

    def test_a_page_context_close_main_action_and_button_do_not_leak_in(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            "<c-fab />",
            context={
                "close": "<div>Leaked close</div>",
                "main_action": "<div>Leaked main action</div>",
                "button": "<div>Leaked button</div>",
            },
        )

        assert "Leaked close" not in html
        assert "Leaked main action" not in html
        assert "Leaked button" not in html
