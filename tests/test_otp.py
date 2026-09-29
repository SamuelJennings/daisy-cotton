"""Tests for <c-form.otp>: daisyUI's one-time code field, a label of empty boxes
followed by one text input and a visually hidden name.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""

from html.parser import HTMLParser

import pytest


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports a repeated attribute every time it occurs, where a
    browser (and BeautifulSoup) keep only one.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _attr_names_on(html, tag):
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return [name for name, _ in parser.attrs]


def _label(soup):
    return soup.find("label")


def _input(soup):
    return soup.find("input")


def _boxes(soup):
    return _label(soup).find_all("span", recursive=False)


class TestOtpStructure:
    def test_renders_a_label_carrying_otp_around_the_boxes_and_the_input(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.otp name="code" />')

        label = _label(soup)
        assert "otp" in label["class"]
        assert len(soup.find_all("label")) == 1
        assert label.find_all("input") == [_input(soup)]

    def test_six_empty_boxes_come_first_then_the_input_then_the_hidden_name(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.otp name="code" />')

        children = [
            child.name for child in _label(soup).find_all(True, recursive=False)
        ]
        assert children == ["span"] * 6 + ["input", "small"]
        for box in _boxes(soup):
            assert box.get_text() == ""
            assert not box.attrs

    def test_the_input_is_a_text_input_for_one_time_digits(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.otp name="code" />')

        field = _input(soup)
        assert field["type"] == "text"
        assert field["name"] == "code"
        assert field["maxlength"] == "6"
        assert field["pattern"] == "[0-9]{6}"
        assert field["inputmode"] == "numeric"
        assert field["autocomplete"] == "one-time-code"


class TestOtpLength:
    @pytest.mark.parametrize("length", ["4", "5"])
    def test_length_sets_the_boxes_maxlength_and_pattern(
        self, cotton_render_string_soup, length
    ):
        soup = cotton_render_string_soup(f'<c-form.otp length="{length}" />')

        assert len(_boxes(soup)) == int(length)
        assert _input(soup)["maxlength"] == length
        assert _input(soup)["pattern"] == "[0-9]{" + length + "}"

    @pytest.mark.parametrize("length", ["many", "0", "-3", "2.5"])
    def test_a_length_that_is_not_a_positive_whole_number_gives_six_boxes(
        self, cotton_render_string_soup, length
    ):
        soup = cotton_render_string_soup(f'<c-form.otp length="{length}" />')

        assert len(_boxes(soup)) == 6
        assert _input(soup)["maxlength"] == "6"
        assert _input(soup)["pattern"] == "[0-9]{6}"


class TestOtpModifiers:
    def test_variant_size_and_joined_land_on_the_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.otp variant="error" size="lg" joined />'
        )

        assert {"otp", "otp-error", "otp-lg", "otp-joined"} <= set(
            _label(soup)["class"]
        )
        assert not [
            name for name in _input(soup).get("class", []) if name.startswith("otp")
        ]

    def test_no_modifier_is_emitted_without_variant_size_or_joined(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.otp />")

        assert [name for name in _label(soup)["class"] if name.startswith("otp-")] == []

    @pytest.mark.parametrize("variant", ["neutral", "primary", "error"])
    def test_each_known_variant_maps_to_its_class(
        self, cotton_render_string_soup, variant
    ):
        soup = cotton_render_string_soup(f'<c-form.otp variant="{variant}" />')

        assert f"otp-{variant}" in _label(soup)["class"]

    @pytest.mark.parametrize("size", ["xs", "sm", "md", "xl"])
    def test_each_known_size_maps_to_its_class(self, cotton_render_string_soup, size):
        soup = cotton_render_string_soup(f'<c-form.otp size="{size}" />')

        assert f"otp-{size}" in _label(soup)["class"]

    def test_an_unknown_variant_and_size_emit_no_modifier_and_do_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.otp variant="rainbow" size="huge" />')

        assert [name for name in _label(soup)["class"] if name.startswith("otp-")] == []
        assert "otp" in _label(soup)["class"]


class TestOtpHiddenName:
    def test_the_name_is_a_small_sr_only_element_after_the_input(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.otp />")

        field = _input(soup)
        name = field.find_next_sibling()
        assert name.name == "small"
        assert "sr-only" in name["class"]
        assert name.get_text(strip=True)
        assert field.find_previous_sibling("small") is None

    def test_the_name_is_never_a_span_so_only_the_boxes_are_counted(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.otp label="Code" />')

        assert len(_boxes(soup)) == 6
        assert _label(soup).find("small").find_parent("label") is _label(soup)

    def test_label_changes_the_hidden_text(self, cotton_render_string_soup):
        default = cotton_render_string_soup("<c-form.otp />")
        named = cotton_render_string_soup(
            '<c-form.otp label="Code from your authenticator app" />'
        )

        assert (
            named.find("small").get_text(strip=True)
            == "Code from your authenticator app"
        )
        assert default.find("small").get_text(strip=True) != named.find(
            "small"
        ).get_text(strip=True)


class TestOtpAttributeRouting:
    def test_required_disabled_id_and_name_land_on_the_input_only(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.otp name="code" id="otp-code" required disabled />'
        )

        field = _input(soup)
        assert field["id"] == "otp-code"
        assert field["name"] == "code"
        assert field.has_attr("required")
        assert field.has_attr("disabled")
        label = _label(soup)
        for name in ("id", "name", "required", "disabled"):
            assert not label.has_attr(name)

    def test_value_autofocus_form_and_an_extra_attribute_reach_the_input(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.otp value="123456" autofocus form="verify" data-testid="otp" />'
        )

        field = _input(soup)
        assert field["value"] == "123456"
        assert field.has_attr("autofocus")
        assert field["form"] == "verify"
        assert field["data-testid"] == "otp"
        label = _label(soup)
        for name in ("value", "autofocus", "form", "data-testid"):
            assert not label.has_attr(name)

    def test_class_merges_into_the_label_once_and_not_the_input(
        self, cotton_render_string, cotton_render_string_soup
    ):
        source = '<c-form.otp class="mb-4" />'

        soup = cotton_render_string_soup(source)
        html = cotton_render_string(source)

        assert {"otp", "mb-4"} <= set(_label(soup)["class"])
        assert "mb-4" not in _input(soup).get("class", [])
        assert _attr_names_on(html, "label").count("class") == 1

    def test_input_class_lands_on_the_input_once_and_not_the_label(
        self, cotton_render_string, cotton_render_string_soup
    ):
        source = '<c-form.otp input_class="validator" />'

        soup = cotton_render_string_soup(source)
        html = cotton_render_string(source)

        assert "validator" in _input(soup)["class"]
        assert "validator" not in _label(soup)["class"]
        assert _attr_names_on(html, "input").count("class") == 1

    def test_no_class_attribute_is_written_on_the_input_without_input_class(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.otp />")

        assert not _input(soup).has_attr("class")


class TestOtpPatternAndInputmode:
    def test_pattern_and_inputmode_replace_the_defaults_with_one_of_each(
        self, cotton_render_string, cotton_render_string_soup
    ):
        source = '<c-form.otp pattern="[A-Z0-9]{6}" inputmode="text" />'

        soup = cotton_render_string_soup(source)
        html = cotton_render_string(source)

        assert _input(soup)["pattern"] == "[A-Z0-9]{6}"
        assert _input(soup)["inputmode"] == "text"
        names = _attr_names_on(html, "input")
        assert names.count("pattern") == 1
        assert names.count("inputmode") == 1

    def test_the_defaults_are_written_once_each(self, cotton_render_string):
        names = _attr_names_on(cotton_render_string("<c-form.otp />"), "input")

        for name in ("type", "maxlength", "pattern", "inputmode", "autocomplete"):
            assert names.count(name) == 1
