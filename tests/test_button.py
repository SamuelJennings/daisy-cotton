"""Tests for the <c-button> component's classes.

Rewritten under decisions.md D2 for the new attribute vocabulary (FR-008,
FR-011): every daisyUI colour and size, one class per style/behaviour/
modifier boolean, and the removed `align`, `reverse`, `condition` and `full`
attributes (`block` replaces `full`).
"""

from django import template
from django.template.context import Context
from django_cotton.compiler_regex import CottonCompiler

compiler = CottonCompiler()


def render(source, **context):
    """Compile a Cotton source string and render it."""
    return template.Template(compiler.process(source)).render(Context(context))


class TestButtonClasses:
    """Scenario 1: variant, size and a style boolean all apply together."""

    def test_variant_size_and_a_style_boolean_all_apply(self):
        html = render('<c-button variant="primary" size="xl" soft>Save</c-button>')
        assert "btn" in html
        assert "btn-primary" in html
        assert "btn-xl" in html
        assert "btn-soft" in html
        assert "Save" in html

    def test_two_style_booleans_together_both_apply(self):
        """The component does not pick between style booleans (Edge Cases)."""
        html = render("<c-button outline ghost>Save</c-button>")
        assert "btn-outline" in html
        assert "btn-ghost" in html

    def test_class_and_extra_attributes_land_on_the_element(self):
        """Scenario 6: `class` merges in and undeclared attributes pass through."""
        html = render('<c-button class="mt-4" data-test="x">Save</c-button>')
        assert "mt-4" in html
        assert 'data-test="x"' in html


class TestButtonUnknownValues:
    """An unknown `variant` or `size` emits no class and does not raise (Edge Cases)."""

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(self):
        html = render('<c-button variant="rainbow">Save</c-button>')
        assert "btn-rainbow" not in html
        assert "<button" in html

    def test_an_unknown_size_emits_no_class_and_does_not_raise(self):
        html = render('<c-button size="huge">Save</c-button>')
        assert "btn-huge" not in html
        assert "<button" in html


class TestButtonElement:
    """Scenarios 2-5: the element chosen, its disabled state, and the icon."""

    def test_href_renders_a_link_carrying_the_href_and_btn_class(self):
        """Scenario 2."""
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
        """Scenario 3."""
        html = render("<c-button disabled>Save</c-button>")
        assert "<button" in html
        assert "disabled" in html

    def test_disabled_href_renders_the_link_as_disabled_without_the_disabled_attribute(
        self,
    ):
        """Scenario 4."""
        html = render('<c-button href="/next" disabled>Save</c-button>')
        assert "<a" in html
        assert "btn-disabled" in html
        assert 'aria-disabled="true"' in html
        assert 'role="button"' in html
        assert 'tabindex="-1"' in html
        assert " disabled" not in html.split(">")[0]

    def test_icon_is_hidden_from_assistive_technology(self):
        """Scenario 5: the icon is decorative; aria-label names the button."""
        html = render(
            '<c-button icon="bi bi-plus" circle aria-label="Add"></c-button>'
        )
        assert 'aria-hidden="true"' in html
        assert 'aria-label="Add"' in html


class TestButtonContextLeak:
    """A page variable of the same name as a declared prop never leaks in
    (research R5, D6): every declared name gets an empty default.
    """

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
