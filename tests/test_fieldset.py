"""Tests for <c-form.fieldset>: daisyUI's fieldset, with a legend, a description and errors.

Sources render through the Cotton compiler as a caller's template would, so
attributes and named slots reach the component the way they do in a real page.
"""

from html.parser import HTMLParser

import pytest
from django.forms.utils import ErrorList


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser — which is what a duplicate ``id``
    attribute needs to be caught.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _id_attrs_on(html, tag):
    """Every ``id="..."`` value found on the first ``<tag ...>`` open tag."""
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return [value for name, value in parser.attrs if name == "id"]


class TestFieldsetStructure:
    def test_bare_fieldset_carries_the_fieldset_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.fieldset>Body</c-form.fieldset>")

        fieldset = soup.find("fieldset")
        assert fieldset is not None
        assert "fieldset" in fieldset["class"]

    def test_legend_is_the_first_child_and_carries_its_class(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.fieldset legend="Shipping">Body</c-form.fieldset>'
        )

        fieldset = soup.find("fieldset")
        first_child = next(c for c in fieldset.children if getattr(c, "name", None))
        assert first_child.name == "legend"
        assert "fieldset-legend" in first_child["class"]
        assert first_child.get_text() == "Shipping"

    def test_no_legend_element_when_legend_is_not_given(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.fieldset>Body</c-form.fieldset>")

        assert soup.find("legend") is None


class TestFieldsetDescription:
    def test_description_renders_after_the_slot(self, cotton_render_string):
        html = cotton_render_string(
            '<c-form.fieldset description="We never share it.">Body</c-form.fieldset>'
        )

        assert html.index("Body") < html.index("We never share it.")

    def test_description_carries_the_label_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.fieldset description="We never share it.">Body</c-form.fieldset>'
        )

        description_p = next(
            p for p in soup.find_all("p") if p.get_text() == "We never share it."
        )
        assert "label" in description_p["class"]

    def test_no_description_element_when_description_is_empty(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.fieldset>Body</c-form.fieldset>")

        assert soup.find("p") is None


class TestFieldsetErrors:
    def test_string_errors_renders_one_error_coloured_line(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.fieldset errors="Pick a shipping option.">Body</c-form.fieldset>'
        )

        wrapper = soup.find("div", class_="grid")
        assert wrapper is not None
        lines = wrapper.find_all("p")
        assert len(lines) == 1
        assert "label" in lines[0]["class"]
        assert "text-error" in lines[0]["class"]
        assert lines[0].get_text() == "Pick a shipping option."

    def test_list_errors_renders_one_line_per_item_inside_one_wrapper(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.fieldset :errors="messages">Body</c-form.fieldset>',
            {"messages": ["Pick a shipping option.", "Address is required."]},
        )

        wrapper = soup.find("div", class_="grid")
        lines = wrapper.find_all("p")
        assert [line.get_text() for line in lines] == [
            "Pick a shipping option.",
            "Address is required.",
        ]

    def test_django_error_list_renders_one_line_per_item(
        self, cotton_render_string_soup
    ):
        from django.forms.utils import ErrorList

        soup = cotton_render_string_soup(
            '<c-form.fieldset :errors="messages">Body</c-form.fieldset>',
            {"messages": ErrorList(["Required."])},
        )

        wrapper = soup.find("div", class_="grid")
        lines = wrapper.find_all("p")
        assert [line.get_text() for line in lines] == ["Required."]

    @pytest.mark.parametrize(
        ("source", "context"),
        [
            (
                '<c-form.fieldset errors="Enter a <b>valid</b> value.">Body</c-form.fieldset>',
                {},
            ),
            (
                '<c-form.fieldset :errors="errs">Body</c-form.fieldset>',
                {"errs": ErrorList(["Enter a <b>valid</b> value."])},
            ),
            (
                '<c-form.fieldset description="Enter a <b>valid</b> value.">Body</c-form.fieldset>',
                {},
            ),
        ],
        ids=["errors-string", "errors-list", "description"],
    )
    def test_markup_in_a_message_is_escaped(
        self, cotton_render_string, source, context
    ):
        html = cotton_render_string(source, context)

        assert "<b>valid</b>" not in html
        assert "&lt;b&gt;valid&lt;/b&gt;" in html

    def test_empty_string_errors_renders_no_errors_element(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.fieldset errors="">Body</c-form.fieldset>'
        )

        assert soup.find("div", class_="grid") is None

    def test_empty_list_errors_renders_no_errors_element(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.fieldset :errors="messages">Body</c-form.fieldset>',
            {"messages": []},
        )

        assert soup.find("div", class_="grid") is None


class TestFieldsetIds:
    def test_fieldset_carries_the_given_id_exactly_once(self, cotton_render_string):
        html = cotton_render_string(
            '<c-form.fieldset id="shipping">Body</c-form.fieldset>'
        )

        assert _id_attrs_on(html, "fieldset") == ["shipping"]

    def test_description_and_errors_ids_derive_from_the_fieldset_id(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.fieldset id="shipping" description="We never share it." '
            'errors="Pick a shipping option.">Body</c-form.fieldset>'
        )

        description_p = next(
            p for p in soup.find_all("p") if p.get_text() == "We never share it."
        )
        assert description_p["id"] == "shipping-description"
        wrapper = soup.find("div", class_="grid")
        assert wrapper["id"] == "shipping-errors"

    def test_no_derived_ids_without_a_fieldset_id(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.fieldset description="We never share it." '
            'errors="Pick a shipping option.">Body</c-form.fieldset>'
        )

        assert soup.find("fieldset").get("id") is None
        description_p = next(
            p for p in soup.find_all("p") if p.get_text() == "We never share it."
        )
        assert description_p.get("id") is None
        wrapper = soup.find("div", class_="grid")
        assert wrapper.get("id") is None


class TestFieldsetNamedSlots:
    def test_legend_description_and_errors_fillable_as_named_slots(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-form.fieldset>"
            '<c-slot name="legend">Shipping</c-slot>'
            "Body"
            '<c-slot name="description">We never share it.</c-slot>'
            '<c-slot name="errors">Pick a shipping option.</c-slot>'
            "</c-form.fieldset>"
        )

        assert soup.find("legend").get_text() == "Shipping"
        description_p = next(
            p for p in soup.find_all("p") if p.get_text() == "We never share it."
        )
        assert description_p is not None
        wrapper = soup.find("div", class_="grid")
        assert wrapper.find("p").get_text() == "Pick a shipping option."

    def test_element_order_is_legend_slot_description_errors(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-form.fieldset legend="Shipping" description="We never share it." '
            'errors="Pick a shipping option.">Slot content</c-form.fieldset>'
        )

        assert (
            html.index("Shipping")
            < html.index("Slot content")
            < html.index("We never share it.")
            < html.index("Pick a shipping option.")
        )


class TestFieldsetRadioGroup:
    def test_labelled_radios_share_a_name_under_the_legend(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.fieldset legend="Shipping method">'
            '<c-form.label text="Standard">'
            '<c-form.radio name="shipping" value="standard" /></c-form.label>'
            '<c-form.label text="Express">'
            '<c-form.radio name="shipping" value="express" /></c-form.label>'
            '<c-form.label text="Overnight">'
            '<c-form.radio name="shipping" value="overnight" /></c-form.label>'
            "</c-form.fieldset>"
        )

        fieldset = soup.find("fieldset")
        first_child = next(c for c in fieldset.children if getattr(c, "name", None))
        assert first_child.name == "legend"
        labels = fieldset.find_all("label")
        assert len(labels) == 3
        radios = [label.find("input", type="radio") for label in labels]
        assert all(radio is not None for radio in radios)
        assert {radio["name"] for radio in radios} == {"shipping"}
        assert [radio["value"] for radio in radios] == [
            "standard",
            "express",
            "overnight",
        ]

    def test_each_radio_is_inside_its_own_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.fieldset legend="Shipping method">'
            '<c-form.label text="Standard">'
            '<c-form.radio name="shipping" value="standard" /></c-form.label>'
            '<c-form.label text="Express">'
            '<c-form.radio name="shipping" value="express" /></c-form.label>'
            "</c-form.fieldset>"
        )

        for label in soup.find_all("label"):
            assert label.find("input", type="radio") is not None
