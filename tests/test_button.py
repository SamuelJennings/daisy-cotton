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
