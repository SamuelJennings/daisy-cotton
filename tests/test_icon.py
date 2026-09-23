"""``<c-icon>`` is a basic primitive: ``name`` is a literal CSS class string,
merged with any caller-supplied ``class``, and every other attribute passes
straight through.

This package resolves no icon pack of its own — a project wanting name-based
resolution provides its own ``cotton/icon.html`` override (CONSTITUTION.md
Article XII). These tests hold the pass-through contract in place, since
nothing else in the package would notice if a future ``<c-vars>`` line
started intercepting an attribute on its way to the ``<i>``.
"""


class TestIconAttributePassThrough:
    def test_name_becomes_the_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-icon name="bi bi-plus-circle" />')

        assert soup.find("i", class_="bi-plus-circle") is not None

    def test_a_caller_class_joins_the_name_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-icon name="bi bi-plus-circle" class="size-6" />'
        )
        rendered = soup.find("i")

        assert "size-6" in rendered["class"]
        assert "bi-plus-circle" in rendered["class"]

    def test_any_other_attribute_reaches_the_icon(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-icon name="bi bi-plus-circle" aria-hidden="true" />'
        )

        assert soup.find("i")["aria-hidden"] == "true"
