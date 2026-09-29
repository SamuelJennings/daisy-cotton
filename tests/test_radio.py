"""Tests for <c-form.radio>: daisyUI's native one-of-many control.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""


class TestRadio:
    def test_name_value_and_variant_render_native_radio(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.radio name="shipping" value="standard" variant="accent" />'
        )

        radios = soup.find_all("input", type="radio")
        assert len(radios) == 1
        radio = radios[0]
        assert "radio" in radio["class"]
        assert "radio-accent" in radio["class"]
        assert radio["name"] == "shipping"
        assert radio["value"] == "standard"

    def test_disabled_is_native(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.radio name="shipping" disabled />')

        radio = soup.find("input", type="radio")
        assert radio.get("disabled") is not None

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.radio variant="rainbow" />')

        assert "radio-rainbow" not in soup.find("input", type="radio")["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.radio size="xxl" />')

        assert "radio-xxl" not in soup.find("input", type="radio")["class"]

    def test_class_merges_with_the_modifier_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.radio class="join-item" />')

        assert "join-item" in soup.find("input", type="radio")["class"]
