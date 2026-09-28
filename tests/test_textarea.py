"""Tests for <c-textarea>: daisyUI's multi-line text box.

Sources render through the Cotton compiler as a caller's template would, so
attributes and the default slot reach the component the way they do in a real
page.
"""


class TestTextarea:
    def test_slot_becomes_the_value_with_nothing_added_around_it(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-textarea name="bio" rows="3" variant="secondary" size="sm">'
            "Hello"
            "</c-textarea>"
        )

        textareas = soup.find_all("textarea")
        assert len(textareas) == 1
        textarea = textareas[0]
        for token in ("textarea", "textarea-secondary", "textarea-sm"):
            assert token in textarea["class"]
        assert textarea["name"] == "bio"
        assert textarea["rows"] == "3"
        assert textarea.get_text() == "Hello"
        assert soup.find("label") is None

    def test_ghost_adds_the_ghost_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-textarea ghost>Hi</c-textarea>")

        assert "textarea-ghost" in soup.find("textarea")["class"]

    def test_variant_error_and_aria_invalid_carry_through(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-textarea variant="error" aria-invalid="true" />'
        )

        textarea = soup.find("textarea")
        assert "textarea-error" in textarea["class"]
        assert textarea["aria-invalid"] == "true"

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-textarea variant="rainbow" />')

        assert "textarea-rainbow" not in soup.find("textarea")["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-textarea size="xxl" />')

        assert "textarea-xxl" not in soup.find("textarea")["class"]

    def test_class_merges_with_the_modifier_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-textarea class="join-item" />')

        assert "join-item" in soup.find("textarea")["class"]
