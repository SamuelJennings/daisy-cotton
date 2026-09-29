"""Tests for <c-select>: daisyUI's select, wrapped when start or end is filled.

Sources render through the Cotton compiler as a caller's template would, so
attributes and named slots reach the component the way they do in a real page.
"""


class TestSelectUnwrapped:
    def test_bare_select_renders_one_select_holding_its_options(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-select name="plan" ghost>'
            '<option value="a">A</option><option value="b">B</option>'
            "</c-select>"
        )

        selects = soup.find_all("select")
        assert len(selects) == 1
        select = selects[0]
        assert "select" in select["class"]
        assert "select-ghost" in select["class"]
        assert select["name"] == "plan"
        assert [o.get_text() for o in select.find_all("option")] == ["A", "B"]
        assert soup.find("label") is None

    def test_variant_and_size_combine_in_one_class_list(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-select variant="primary" size="lg" />')

        select = soup.find("select")
        for token in ("select", "select-primary", "select-lg"):
            assert token in select["class"]

    def test_variant_error_and_aria_invalid_carry_through(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-select variant="error" aria-invalid="true" />'
        )

        select = soup.find("select")
        assert "select-error" in select["class"]
        assert select["aria-invalid"] == "true"

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-select variant="rainbow" />')

        assert "select-rainbow" not in soup.find("select")["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-select size="xxl" />')

        assert "select-xxl" not in soup.find("select")["class"]


class TestSelectWrapped:
    def test_modifiers_land_on_the_wrapper_not_the_select(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-select variant="primary" size="lg" ghost>'
            '<c-slot name="start"><span class="label">Plan</span></c-slot>'
            "<option>A</option>"
            "</c-select>"
        )

        label = soup.find("label")
        assert {"select", "select-primary", "select-lg", "select-ghost"} <= set(
            label["class"]
        )
        assert soup.find("select").get("class") is None

    def test_start_and_end_wrap_the_select_in_order(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-select name="plan">'
            '<c-slot name="start"><span class="label">Plan</span></c-slot>'
            '<c-slot name="end"><kbd class="kbd">P</kbd></c-slot>'
            "<option>A</option>"
            "</c-select>"
        )

        label = soup.find("label")
        children = [c for c in label.children if getattr(c, "name", None)]
        assert [c.name for c in children] == ["span", "select", "kbd"]

    def test_start_filled_wraps_the_select_in_order(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-select name="plan">'
            '<c-slot name="start"><span class="label">Plan</span></c-slot>'
            '<option value="a">A</option>'
            "</c-select>"
        )

        label = soup.find("label")
        assert label is not None
        assert "select" in label["class"]
        select = soup.find("select")
        assert select["name"] == "plan"
        children = [c for c in label.children if getattr(c, "name", None)]
        assert [c.name for c in children] == ["span", "select"]

    def test_only_end_filled_chooses_the_wrapped_form(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-select><c-slot name="end">.00</c-slot>'
            '<option value="a">A</option></c-select>'
        )

        assert soup.find("label") is not None

    def test_wrapper_carries_class_and_select_carries_name(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-select class="w-full" name="plan">'
            '<c-slot name="start">$</c-slot>'
            "</c-select>"
        )

        label = soup.find("label")
        assert "w-full" in label["class"]
        select = soup.find("select")
        assert select["name"] == "plan"

    def test_inner_select_carries_no_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-select class="w-full"><c-slot name="start">$</c-slot></c-select>'
        )

        assert soup.find("select").get("class") is None
