"""Tests for <c-form.filter>: daisyUI's filter, a group of radio buttons with a
reset radio, written without a <form> so it can sit inside a larger one.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""

import re
from html.parser import HTMLParser

import pytest

OPTIONS = ["Open", "Closed"]
PAIRS = [("o", "Open"), ("c", "Closed")]


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


def _wrapper(soup):
    return soup.find("div", class_="filter")


def _radios(soup):
    return _wrapper(soup).find_all("input", type="radio")


def _reset(soup):
    return _wrapper(soup).find("input", class_="filter-reset")


def _option_radios(soup):
    return [radio for radio in _radios(soup) if "filter-reset" not in radio["class"]]


class TestFilterStructure:
    def test_renders_a_wrapper_carrying_filter_with_no_form(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        assert _wrapper(soup) is not None
        assert soup.find("form") is None

    def test_the_reset_comes_first_and_carries_btn_and_filter_reset(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        first = _radios(soup)[0]
        assert "btn" in first["class"]
        assert "filter-reset" in first["class"]

    def test_each_option_is_a_radio_carrying_btn_after_the_reset(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        options = _option_radios(soup)
        assert [radio["value"] for radio in options] == OPTIONS
        assert all("btn" in radio["class"] for radio in options)
        assert len(_radios(soup)) == len(OPTIONS) + 1

    def test_every_radio_shares_the_given_name(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        assert {radio["name"] for radio in _radios(soup)} == {"status"}

    def test_the_wrapper_is_a_radiogroup(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        assert _wrapper(soup)["role"] == "radiogroup"


class TestFilterOptionValues:
    def test_a_pair_gives_the_value_and_the_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": PAIRS}
        )

        options = _option_radios(soup)
        assert [radio["value"] for radio in options] == ["o", "c"]
        assert [radio["aria-label"] for radio in options] == ["Open", "Closed"]

    def test_a_plain_value_is_its_own_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        options = _option_radios(soup)
        assert [radio["aria-label"] for radio in options] == OPTIONS

    def test_value_checks_the_matching_option_and_no_other(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" value="Closed" :options="options" />',
            {"options": OPTIONS},
        )

        checked = [radio for radio in _radios(soup) if radio.has_attr("checked")]
        assert [radio["value"] for radio in checked] == ["Closed"]

    def test_no_radio_is_checked_without_a_value(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        assert not any(radio.has_attr("checked") for radio in _radios(soup))

    def test_no_radio_is_checked_when_value_matches_no_option(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" value="Archived" :options="options" />',
            {"options": OPTIONS},
        )

        assert not any(radio.has_attr("checked") for radio in _radios(soup))

    def test_an_empty_options_list_renders_only_the_reset(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": []}
        )

        radios = _radios(soup)
        assert len(radios) == 1
        assert "filter-reset" in radios[0]["class"]

    def test_no_options_at_all_renders_only_the_reset(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.filter name="status" />')

        assert len(_radios(soup)) == 1


class TestFilterReset:
    def test_the_reset_submits_an_empty_value(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        assert _reset(soup)["value"] == ""

    def test_the_reset_shows_a_cross_and_is_named_through_labelledby(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        reset = _reset(soup)
        assert reset["aria-label"] == "\u00d7"
        target = soup.find(id=reset["aria-labelledby"])
        assert target is not None
        assert target.get_text(strip=True) != ""

    def test_the_labelledby_target_is_hidden_and_unique(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        reset_id = _reset(soup)["aria-labelledby"]
        assert len(soup.find_all(id=reset_id)) == 1
        assert soup.find(id=reset_id).has_attr("hidden")

    def test_reset_label_changes_the_names_text_and_nothing_else(
        self, cotton_render_string_soup
    ):
        default = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )
        renamed = cotton_render_string_soup(
            '<c-form.filter name="status" reset_label="Zurücksetzen" '
            ':options="options" />',
            {"options": OPTIONS},
        )

        def normalised(soup):
            target = soup.find(id=_reset(soup)["aria-labelledby"])
            text = target.get_text(strip=True)
            target.string = ""
            return re.sub(r"filter-reset-[0-9a-f]{8}", "ID", str(soup)), text

        default_html, default_text = normalised(default)
        renamed_html, renamed_text = normalised(renamed)
        assert renamed_text == "Zurücksetzen"
        assert default_text != renamed_text
        assert default_html == renamed_html

    def test_two_filters_get_different_reset_name_ids(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter :options="options" /><c-form.filter :options="options" />',
            {"options": OPTIONS},
        )

        resets = soup.find_all("input", class_="filter-reset")
        assert resets[0]["aria-labelledby"] != resets[1]["aria-labelledby"]


class TestFilterName:
    def test_two_filters_without_a_name_each_share_their_own_generated_name(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter :options="options" /><c-form.filter :options="options" />',
            {"options": OPTIONS},
        )

        first, second = soup.find_all("div", class_="filter")
        first_names = {radio["name"] for radio in first.find_all("input")}
        second_names = {radio["name"] for radio in second.find_all("input")}
        assert len(first_names) == 1
        assert len(second_names) == 1
        assert first_names != second_names
        assert "" not in first_names | second_names

    def test_a_given_name_is_used_in_place_of_a_generated_one(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        assert not any(radio["name"].startswith("filter") for radio in _radios(soup))


class TestFilterGroupLabel:
    def test_label_is_the_wrappers_aria_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" label="Status" :options="options" />',
            {"options": OPTIONS},
        )

        wrapper = _wrapper(soup)
        assert wrapper["role"] == "radiogroup"
        assert wrapper["aria-label"] == "Status"

    def test_without_a_label_the_wrapper_has_no_aria_label(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        assert not _wrapper(soup).has_attr("aria-label")

    def test_label_does_not_reach_a_radio(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" label="Status" :options="options" />',
            {"options": OPTIONS},
        )

        assert "Status" not in [radio.get("aria-label") for radio in _radios(soup)]


class TestFilterSharedAttributes:
    def test_required_disabled_and_form_land_on_every_radio(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" required disabled form="search" '
            ':options="options" />',
            {"options": OPTIONS},
        )

        radios = _radios(soup)
        assert len(radios) == len(OPTIONS) + 1
        for radio in radios:
            assert radio.has_attr("required")
            assert radio.has_attr("disabled")
            assert radio["form"] == "search"

    def test_required_disabled_and_form_do_not_reach_the_wrapper(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" required disabled form="search" '
            ':options="options" />',
            {"options": OPTIONS},
        )

        wrapper = _wrapper(soup)
        assert not wrapper.has_attr("required")
        assert not wrapper.has_attr("disabled")
        assert not wrapper.has_attr("form")

    def test_none_of_them_appear_when_not_given(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        for radio in _radios(soup):
            assert not radio.has_attr("required")
            assert not radio.has_attr("disabled")
            assert not radio.has_attr("form")


class TestFilterAttributeRouting:
    def test_id_and_an_extra_attribute_reach_the_wrapper_only(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" id="status-filter" data-testid="f" '
            ':options="options" />',
            {"options": OPTIONS},
        )

        wrapper = _wrapper(soup)
        assert wrapper["id"] == "status-filter"
        assert wrapper["data-testid"] == "f"
        for radio in _radios(soup):
            assert not radio.has_attr("data-testid")
            assert radio.get("id") is None

    def test_class_merges_into_the_wrapper_once(
        self, cotton_render_string, cotton_render_string_soup
    ):
        source = '<c-form.filter name="status" class="mb-4" :options="options" />'

        soup = cotton_render_string_soup(source, {"options": OPTIONS})
        html = cotton_render_string(source, {"options": OPTIONS})

        assert {"filter", "mb-4"} <= set(_wrapper(soup)["class"])
        assert _attr_names_on(html, "div").count("class") == 1
        assert not any("mb-4" in radio["class"] for radio in _radios(soup))


class TestFilterModifiers:
    def test_variant_and_size_reach_every_option_and_the_reset(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" variant="primary" size="sm" '
            ':options="options" />',
            {"options": OPTIONS},
        )

        for radio in _radios(soup):
            assert "btn-primary" in radio["class"]
            assert "btn-sm" in radio["class"]

    def test_no_modifier_is_emitted_without_variant_or_size(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" :options="options" />', {"options": OPTIONS}
        )

        for radio in _radios(soup):
            assert not [name for name in radio["class"] if name.startswith("btn-")]

    def test_an_unknown_variant_and_size_emit_no_modifier_and_do_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.filter name="status" variant="rainbow" size="huge" '
            ':options="options" />',
            {"options": OPTIONS},
        )

        for radio in _radios(soup):
            assert not [name for name in radio["class"] if name.startswith("btn-")]
            assert {"btn"} <= set(radio["class"])

    @pytest.mark.parametrize(
        "variant",
        [
            "neutral",
            "primary",
            "secondary",
            "accent",
            "info",
            "success",
            "warning",
            "error",
        ],
    )
    def test_each_variant_maps_to_its_daisyui_class(
        self, cotton_render_string_soup, variant
    ):
        soup = cotton_render_string_soup(
            f'<c-form.filter name="status" variant="{variant}" :options="options" />',
            {"options": OPTIONS},
        )

        assert all(f"btn-{variant}" in radio["class"] for radio in _radios(soup))
