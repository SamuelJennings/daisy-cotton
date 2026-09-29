"""Tests for <c-form.toggle>: daisyUI's switch, rendered as a checkbox.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""


class TestToggle:
    def test_name_and_size_render_native_switch(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.toggle name="dark_mode" size="lg" variant="primary" />'
        )

        toggles = soup.find_all("input", attrs={"role": "switch"})
        assert len(toggles) == 1
        toggle = toggles[0]
        assert toggle["type"] == "checkbox"
        assert "toggle" in toggle["class"]
        assert "toggle-lg" in toggle["class"]
        assert "toggle-primary" in toggle["class"]
        assert toggle["name"] == "dark_mode"

    def test_disabled_is_native(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.toggle name="dark_mode" disabled />')

        toggle = soup.find("input", attrs={"role": "switch"})
        assert toggle.get("disabled") is not None

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.toggle variant="rainbow" />')

        assert (
            "toggle-rainbow"
            not in soup.find("input", attrs={"role": "switch"})["class"]
        )

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.toggle size="xxl" />')

        assert "toggle-xxl" not in soup.find("input", attrs={"role": "switch"})["class"]

    def test_class_merges_with_the_modifier_classes(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.toggle class="join-item" />')

        assert "join-item" in soup.find("input", attrs={"role": "switch"})["class"]
