"""Tests for the <c-button> component's classes.

Rewritten under decisions.md D2 for the new attribute vocabulary (FR-008,
FR-011): every daisyUI colour and size, one class per style/behaviour/
modifier boolean, and the removed `align`, `reverse`, `condition` and `full`
attributes (`block` replaces `full`).
"""

import re
from pathlib import Path

import pytest
from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler
from django_cotton_gallery.core.annotations import AnnotationParser

import daisy_cotton

compiler = CottonCompiler()

BUTTON_TEMPLATE = (
    Path(next(iter(daisy_cotton.__path__))).resolve()
    / "templates"
    / "cotton"
    / "button.html"
)


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


class TestButtonClasses:
    def test_variant_size_and_a_style_boolean_all_apply(self):
        html = render('<c-button variant="primary" size="xl" soft>Save</c-button>')
        assert "btn" in html
        assert "btn-primary" in html
        assert "btn-xl" in html
        assert "btn-soft" in html
        assert "Save" in html

    def test_two_style_booleans_together_both_apply(self):
        html = render("<c-button outline ghost>Save</c-button>")
        assert "btn-outline" in html
        assert "btn-ghost" in html

    def test_class_and_extra_attributes_land_on_the_element(self):
        html = render('<c-button class="mt-4" data-test="x">Save</c-button>')
        assert "mt-4" in html
        assert 'data-test="x"' in html


class TestButtonUnknownValues:
    def test_an_unknown_variant_emits_no_class_and_does_not_raise(self):
        html = render('<c-button variant="rainbow">Save</c-button>')
        assert "btn-rainbow" not in html
        assert "<button" in html

    def test_an_unknown_size_emits_no_class_and_does_not_raise(self):
        html = render('<c-button size="huge">Save</c-button>')
        assert "btn-huge" not in html
        assert "<button" in html


class TestButtonElement:
    def test_href_renders_a_link_carrying_the_href_and_btn_class(self):
        html = render('<c-button href="/next" text="Next" />')
        assert "<a" in html
        assert 'href="/next"' in html
        assert "btn" in html
        assert "<button" not in html

    def test_no_href_renders_a_plain_button(self):
        html = render('<c-button text="Next" />')
        assert "<button" in html
        assert "<a" not in html

    def test_disabled_renders_the_native_attribute_on_a_button(self):
        html = render("<c-button disabled>Save</c-button>")
        assert "<button" in html
        assert "disabled" in html

    def test_disabled_href_renders_the_link_as_disabled_without_the_disabled_attribute(
        self,
    ):
        html = render('<c-button href="/next" disabled>Save</c-button>')
        assert "<a" in html
        assert "btn-disabled" in html
        assert 'aria-disabled="true"' in html
        assert 'role="button"' in html
        assert 'tabindex="-1"' in html
        assert " disabled" not in html.split(">")[0]

    def test_icon_is_hidden_from_assistive_technology(self):
        html = render('<c-button icon="bi bi-plus" circle aria-label="Add"></c-button>')
        assert 'aria-hidden="true"' in html
        assert 'aria-label="Add"' in html


class TestButtonGalleryAnnotations:
    @staticmethod
    def _parsed():
        return AnnotationParser().parse(BUTTON_TEMPLATE.read_text())

    def test_variant_is_a_select_of_the_eight_colours(self):
        prop = next(p for p in self._parsed().props if p.clean_name == "variant")
        assert prop.type == "select"
        assert set(prop.options) == {
            "neutral",
            "primary",
            "secondary",
            "accent",
            "info",
            "success",
            "warning",
            "error",
        }

    def test_size_is_a_select_of_the_five_sizes(self):
        prop = next(p for p in self._parsed().props if p.clean_name == "size")
        assert prop.type == "select"
        assert set(prop.options) == {"xs", "sm", "md", "lg", "xl"}

    @pytest.mark.parametrize(
        "name",
        [
            "outline",
            "dash",
            "soft",
            "ghost",
            "link",
            "active",
            "disabled",
            "wide",
            "block",
            "square",
            "circle",
        ],
    )
    def test_every_boolean_has_its_own_prop(self, name):
        prop = next(p for p in self._parsed().props if p.clean_name == name)
        assert prop.type == "boolean"

    def test_the_default_slot_has_an_example(self):
        [slot] = [s for s in self._parsed().slots if s.name is None]
        assert slot.content


class TestButtonContextLeak:
    def test_a_page_context_href_text_and_variant_do_not_leak_in(self):
        html = render(
            "<c-button>Save</c-button>",
            href="/somewhere",
            text="Leaked",
            variant="primary",
        )
        assert "<button" in html
        assert "<a" not in html
        assert "Leaked" not in html
        assert "btn-primary" not in html

    def test_icon_does_not_carry_a_class_given_to_the_button(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-button icon="bi bi-plus" class="w-full">Add</c-button>'
        )

        assert "w-full" in soup.button["class"]
        assert "w-full" not in soup.button.find("i")["class"]


class TestButtonVocabulary:
    @pytest.mark.parametrize(
        "name",
        [
            "outline",
            "dash",
            "soft",
            "ghost",
            "link",
            "active",
            "wide",
            "block",
            "square",
            "circle",
        ],
    )
    def test_each_boolean_emits_its_class(self, name):
        html = render(f"<c-button {name}>Save</c-button>")
        opening = html.split(">", 1)[0]
        assert f"btn-{name}" in opening

    @pytest.mark.parametrize(
        "variant",
        [
            "neutral",
            "primary",
            "secondary",
            "accent",
            "info",
            "success",
            "warning",
            "error",
        ],
    )
    def test_each_variant_emits_its_class(self, variant):
        html = render(f'<c-button variant="{variant}">Save</c-button>')
        assert f"btn-{variant}" in html.split(">", 1)[0]

    @pytest.mark.parametrize("size", ["xs", "sm", "md", "lg", "xl"])
    def test_each_size_emits_its_class(self, size):
        html = render(f'<c-button size="{size}">Save</c-button>')
        assert f"btn-{size}" in html.split(">", 1)[0]

    def test_full_is_not_a_modifier(self):
        html = render("<c-button full>Save</c-button>")
        assert "btn-full" not in html
        assert "btn-block" not in html

    def test_disabled_button_carries_a_bare_native_attribute(self):
        html = render("<c-button disabled>Save</c-button>")
        assert re.search(r"<button[^>]*\sdisabled[\s>]", html)
        assert "aria-disabled" not in html

    def test_an_undeclared_small_attribute_does_not_size_the_button(self):
        html = render('<c-button text="Save" small />')
        assert "btn-sm" not in html
        assert re.search(r"<button[^>]*\bsmall\b[^>]*>", html)
