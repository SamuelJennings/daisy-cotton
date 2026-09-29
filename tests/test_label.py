"""Tests for <c-form.label>: daisyUI's label, above a control, wrapping one, or floating.

Sources render through the Cotton compiler as a caller's template would, so
attributes and named slots reach the component the way they do in a real page.
"""


class TestLabelAboveControl:
    def test_for_and_text_render_a_label_naming_the_control(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.label for="id_email" text="Email" />')

        label = soup.find("label")
        assert label is not None
        assert "label" in label["class"]
        assert label["for"] == "id_email"
        assert label.get_text() == "Email"

    def test_no_floating_label_class_when_not_floating(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.label for="id_email" text="Email" />')

        label = soup.find("label")
        assert "floating-label" not in label["class"]

    def test_class_merges_and_extra_attribute_passes_through(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.label text="Email" class="my-label" data-testid="email-label" />'
        )

        label = soup.find("label")
        assert "label" in label["class"]
        assert "my-label" in label["class"]
        assert label["data-testid"] == "email-label"


class TestLabelWrappingControl:
    def test_checkbox_is_inside_the_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.label text="Remember me">'
            '<input type="checkbox" class="checkbox" />'
            "</c-form.label>"
        )

        label = soup.find("label")
        assert label.find("input", type="checkbox") is not None

    def test_wrapped_control_comes_before_the_text(self, cotton_render_string):
        html = cotton_render_string(
            '<c-form.label text="Remember me">'
            '<input type="checkbox" class="checkbox" />'
            "</c-form.label>"
        )

        assert html.index('type="checkbox"') < html.index("Remember me")

    def test_c_checkbox_is_inside_the_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.label text="Remember me"><c-form.checkbox name="remember" /></c-form.label>'
        )

        label = soup.find("label")
        checkbox = label.find("input", type="checkbox")
        assert checkbox is not None
        assert checkbox["name"] == "remember"

    def test_c_checkbox_comes_before_the_text(self, cotton_render_string):
        html = cotton_render_string(
            '<c-form.label text="Remember me"><c-form.checkbox name="remember" /></c-form.label>'
        )

        assert html.index('name="remember"') < html.index("Remember me")


class TestLabelFloating:
    def test_floating_wraps_the_input_then_a_span_with_the_text(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.label text="Email" floating><c-form.input placeholder="Email" /></c-form.label>'
        )

        label = soup.find("label")
        assert "floating-label" in label["class"]
        children = [c for c in label.children if getattr(c, "name", None)]
        assert [c.name for c in children] == ["input", "span"]
        assert children[1].get_text() == "Email"

    def test_no_label_class_when_floating(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.label text="Email" floating><c-form.input placeholder="Email" /></c-form.label>'
        )

        label = soup.find("label")
        assert "label" not in label["class"]
