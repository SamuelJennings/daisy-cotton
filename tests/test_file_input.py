"""Tests for <c-file-input>: daisyUI's native file picker.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""


class TestFileInput:
    def test_name_accept_and_modifiers_render_native_file_input(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-file-input name="resume" accept=".pdf" variant="info" ghost />'
        )

        file_inputs = soup.find_all("input", type="file")
        assert len(file_inputs) == 1
        file_input = file_inputs[0]
        for token in ("file-input", "file-input-info", "file-input-ghost"):
            assert token in file_input["class"]
        assert file_input["name"] == "resume"
        assert file_input["accept"] == ".pdf"

    def test_disabled_is_native(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-file-input name="resume" disabled />')

        file_input = soup.find("input", type="file")
        assert file_input.get("disabled") is not None

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-file-input variant="rainbow" />')

        assert "file-input-rainbow" not in soup.find("input", type="file")["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-file-input size="xxl" />')

        assert "file-input-xxl" not in soup.find("input", type="file")["class"]

    def test_class_merges_with_the_modifier_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-file-input class="join-item" />')

        assert "join-item" in soup.find("input", type="file")["class"]
