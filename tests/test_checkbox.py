"""Tests for <c-checkbox>: daisyUI's native on-off control.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""


class TestCheckbox:
    def test_checked_renders_native_checkbox_with_modifiers(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-checkbox name="terms" variant="primary" size="sm" checked />'
        )

        checkboxes = soup.find_all("input", type="checkbox")
        assert len(checkboxes) == 1
        checkbox = checkboxes[0]
        for token in ("checkbox", "checkbox-primary", "checkbox-sm"):
            assert token in checkbox["class"]
        assert checkbox["name"] == "terms"
        assert checkbox.get("checked") is not None

    def test_disabled_is_native(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-checkbox name="terms" disabled />')

        checkbox = soup.find("input", type="checkbox")
        assert checkbox.get("disabled") is not None

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-checkbox variant="rainbow" />')

        assert "checkbox-rainbow" not in soup.find("input", type="checkbox")["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-checkbox size="xxl" />')

        assert "checkbox-xxl" not in soup.find("input", type="checkbox")["class"]

    def test_class_merges_with_the_modifier_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-checkbox class="join-item" />')

        assert "join-item" in soup.find("input", type="checkbox")["class"]
