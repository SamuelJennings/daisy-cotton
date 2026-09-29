"""Tests for <c-form.input>: daisyUI's text input, wrapped when start or end is filled.

Sources render through the Cotton compiler as a caller's template would, so
attributes and named slots reach the component the way they do in a real page.
"""

import re


def _first_input_tag(html):
    start = html.index("<input")
    end = html.index(">", start) + 1
    return html[start:end]


class TestInputUnwrapped:
    def test_bare_input_renders_one_text_input_with_its_attributes(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.input name="q" placeholder="Search" />'
        )

        inputs = soup.find_all("input")
        assert len(inputs) == 1
        input_ = inputs[0]
        assert input_["type"] == "text"
        assert "input" in input_["class"]
        assert input_["name"] == "q"
        assert input_["placeholder"] == "Search"
        assert soup.find("label") is None

    def test_type_variant_size_and_ghost_combine_in_one_class_list(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.input type="email" variant="primary" size="lg" ghost />'
        )

        input_ = soup.find("input")
        assert input_["type"] == "email"
        for token in ("input", "input-primary", "input-lg", "input-ghost"):
            assert token in input_["class"]

    def test_class_join_item_renders_one_element(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.input class="join-item" />')

        inputs = soup.find_all("input")
        assert len(inputs) == 1
        assert soup.find("label") is None
        assert "join-item" in inputs[0]["class"]

    def test_variant_error_and_aria_invalid_carry_through(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.input variant="error" aria-invalid="true" />'
        )

        input_ = soup.find("input")
        assert "input-error" in input_["class"]
        assert input_["aria-invalid"] == "true"

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.input variant="rainbow" />')

        assert "input-rainbow" not in soup.find("input")["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.input size="xxl" />')

        assert "input-xxl" not in soup.find("input")["class"]

    def test_bare_required_and_disabled_reach_the_input_as_bare_attributes(
        self, cotton_render_string
    ):
        html = cotton_render_string("<c-form.input required disabled />")
        tag = _first_input_tag(html)

        assert re.search(r"\srequired[\s>]", tag)
        assert re.search(r"\sdisabled[\s>]", tag)


class TestInputWrapped:
    def test_modifiers_land_on_the_wrapper_not_the_input(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.input variant="primary" size="lg" ghost>'
            '<c-slot name="start"><span class="label">https://</span></c-slot>'
            "</c-form.input>"
        )

        label = soup.find("label")
        assert {"input", "input-primary", "input-lg", "input-ghost"} <= set(
            label["class"]
        )
        assert soup.find("input").get("class") is None

    def test_start_and_end_wrap_the_input_in_order(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-form.input>"
            '<c-slot name="start"><span class="label">$</span></c-slot>'
            '<c-slot name="end"><kbd>Enter</kbd></c-slot>'
            "</c-form.input>"
        )

        label = soup.find("label")
        assert label is not None
        assert "input" in label["class"]
        children = [c for c in label.children if getattr(c, "name", None)]
        assert [c.name for c in children] == ["span", "input", "kbd"]

    def test_only_start_filled_chooses_the_wrapped_form(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.input><c-slot name="start">$</c-slot></c-form.input>'
        )
        assert soup.find("label") is not None

    def test_only_end_filled_chooses_the_wrapped_form(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.input><c-slot name="end">.00</c-slot></c-form.input>'
        )
        assert soup.find("label") is not None

    def test_wrapper_carries_class_and_input_carries_name_and_required(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.input class="w-full" name="site" required>'
            '<c-slot name="start">$</c-slot>'
            "</c-form.input>"
        )

        label = soup.find("label")
        assert "w-full" in label["class"]
        input_ = soup.find("input")
        assert input_["name"] == "site"
        assert input_.has_attr("required")

    def test_inner_input_carries_no_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.input class="w-full"><c-slot name="start">$</c-slot></c-form.input>'
        )

        assert soup.find("input").get("class") is None

    def test_id_and_aria_describedby_land_on_the_input_not_the_wrapper(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.input id="site" aria-describedby="site-errors">'
            '<c-slot name="start">$</c-slot>'
            "</c-form.input>"
        )

        label = soup.find("label")
        assert not label.has_attr("id")
        assert not label.has_attr("aria-describedby")
        input_ = soup.find("input")
        assert input_["id"] == "site"
        assert input_["aria-describedby"] == "site-errors"
