"""Tests for <c-form.rating>: daisyUI's rating, a group of radio items or, read
only, a row of <div> items.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""

from html.parser import HTMLParser

import pytest

SHAPES = ["star", "star-2", "heart"]
VARIANTS = ["neutral", "primary", "secondary", "accent", "info", "success"]
SIZES = ["xs", "sm", "md", "lg", "xl"]


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
    return soup.find("div", class_="rating")


def _radios(soup):
    return _wrapper(soup).find_all("input", type="radio")


def _items(soup):
    return [radio for radio in _radios(soup) if "mask" in radio["class"]]


def _read_only_items(soup):
    return _wrapper(soup).find_all("div", recursive=False)


def _prefixed(element, prefix):
    return [name for name in element["class"] if name.startswith(prefix)]


class TestRatingStructure:
    def test_renders_a_wrapper_carrying_rating_around_five_radios(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" />')

        assert len(soup.find_all("div", class_="rating")) == 1
        assert len(_radios(soup)) == 5

    def test_nothing_but_items_sits_inside_the_wrapper(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.rating name="score" label="Your rating" clearable />'
        )

        assert _wrapper(soup).find_all(True) == _radios(soup)

    def test_the_radios_share_the_name_and_run_from_one_to_five(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" />')

        assert {radio["name"] for radio in _radios(soup)} == {"score"}
        assert [radio["value"] for radio in _radios(soup)] == ["1", "2", "3", "4", "5"]

    def test_every_item_carries_mask_and_the_star_shape(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" />')

        for radio in _radios(soup):
            assert {"mask", "mask-star"} <= set(radio["class"])

    def test_the_wrapper_is_a_radiogroup_named_by_label(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating name="score" label="Your rating" />'
        )

        assert _wrapper(soup)["role"] == "radiogroup"
        assert _wrapper(soup)["aria-label"] == "Your rating"

    def test_without_a_label_the_wrapper_has_no_aria_label(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" />')

        assert _wrapper(soup)["role"] == "radiogroup"
        assert not _wrapper(soup).has_attr("aria-label")

    def test_label_does_not_reach_a_radio(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.rating name="score" label="Your rating" />'
        )

        for radio in _radios(soup):
            assert radio["aria-label"] != "Your rating"

    def test_no_radio_is_checked_without_a_value(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating name="score" />')

        assert not [radio for radio in _radios(soup) if radio.has_attr("checked")]


class TestRatingValue:
    def test_max_and_value_give_ten_radios_and_check_the_seventh(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating max="10" value="7" />')

        radios = _radios(soup)
        assert len(radios) == 10
        assert [radio["value"] for radio in radios if radio.has_attr("checked")] == [
            "7"
        ]
        assert radios[6].has_attr("checked")

    def test_a_max_that_is_not_a_positive_whole_number_gives_five(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating max="many" />')

        assert len(_radios(soup)) == 5

    @pytest.mark.parametrize("value", ["6", "0", "-1", "abc", "2.5"])
    def test_a_value_above_max_below_one_off_step_or_not_a_number_checks_nothing(
        self, cotton_render_string_soup, value
    ):
        soup = cotton_render_string_soup(f'<c-form.rating value="{value}" />')

        assert len(_radios(soup)) == 5
        assert not [radio for radio in _radios(soup) if radio.has_attr("checked")]

    @pytest.mark.parametrize("value", ["6", "-1", "2.3", "abc"])
    def test_a_half_rating_value_out_of_range_or_off_step_checks_nothing(
        self, cotton_render_string_soup, value
    ):
        soup = cotton_render_string_soup(f'<c-form.rating half value="{value}" />')

        assert not [radio for radio in _radios(soup) if radio.has_attr("checked")]


class TestRatingItemNames:
    def test_every_radio_has_a_name_that_differs_from_every_other(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" />')

        names = [radio["aria-label"] for radio in _radios(soup)]
        assert all(names)
        assert len(set(names)) == len(names)

    def test_half_radios_have_names_that_all_differ(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating name="score" half />')

        names = [radio["aria-label"] for radio in _radios(soup)]
        assert len(names) == 10
        assert all(names)
        assert len(set(names)) == len(names)

    @pytest.mark.parametrize("attributes", ['value="3"', 'half value="3"'])
    def test_a_rating_value_does_not_leak_into_the_item_names(
        self, cotton_render_string_soup, attributes
    ):
        soup = cotton_render_string_soup(f'<c-form.rating {attributes} max="4" />')

        names = [radio["aria-label"] for radio in _radios(soup)]
        assert len(set(names)) == len(names)

    def test_the_name_of_a_single_star_differs_in_form_from_the_plural(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.rating />")

        first, second = (radio["aria-label"] for radio in _radios(soup)[:2])
        assert first.replace("1", "2") != second


class TestRatingClearable:
    def test_a_first_radio_carries_rating_hidden_with_an_empty_value(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" clearable />')

        radios = _radios(soup)
        assert len(radios) == 6
        assert "rating-hidden" in radios[0]["class"]
        assert "mask" not in radios[0]["class"]
        assert radios[0]["value"] == ""
        assert radios[0]["name"] == "score"
        assert radios[0]["aria-label"]
        assert radios[0]["aria-label"] not in {
            radio["aria-label"] for radio in radios[1:]
        }

    def test_the_hidden_radio_is_checked_without_a_value(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.rating clearable />")

        assert [radio.has_attr("checked") for radio in _radios(soup)] == [
            True,
            False,
            False,
            False,
            False,
            False,
        ]

    def test_the_hidden_radio_is_unchecked_when_a_value_is_given(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating clearable value="3" />')

        radios = _radios(soup)
        assert not radios[0].has_attr("checked")
        assert [radio["value"] for radio in radios if radio.has_attr("checked")] == [
            "3"
        ]

    def test_without_clearable_there_is_no_hidden_radio(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.rating />")

        assert len(_radios(soup)) == 5
        assert not soup.find(class_="rating-hidden")

    def test_a_read_only_rating_is_never_clearable(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.rating readonly clearable />")

        assert not soup.find("input")
        assert not soup.find(class_="rating-hidden")


class TestRatingHalf:
    def test_the_wrapper_carries_rating_half_and_ten_radios_alternate_the_halves(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" half />')

        assert "rating-half" in _wrapper(soup)["class"]
        radios = _radios(soup)
        assert len(radios) == 10
        for index, radio in enumerate(radios):
            expected = "mask-half-1" if index % 2 == 0 else "mask-half-2"
            assert expected in radio["class"]
            assert not set(radio["class"]) >= {"mask-half-1", "mask-half-2"}

    def test_the_values_run_from_a_half_to_max_in_half_steps(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.rating half />")

        assert [radio["value"] for radio in _radios(soup)] == [
            "0.5",
            "1",
            "1.5",
            "2",
            "2.5",
            "3",
            "3.5",
            "4",
            "4.5",
            "5",
        ]

    def test_a_half_value_checks_the_half_radio(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating half value="2.5" />')

        assert [
            radio["value"] for radio in _radios(soup) if radio.has_attr("checked")
        ] == ["2.5"]

    def test_a_whole_rating_has_neither_rating_half_nor_half_masks(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.rating />")

        assert "rating-half" not in _wrapper(soup)["class"]
        for radio in _radios(soup):
            assert not _prefixed(radio, "mask-half")


class TestRatingModifiers:
    def test_shape_variant_and_size_land_on_the_items_and_the_wrapper(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating shape="heart" variant="warning" size="lg" />'
        )

        for radio in _radios(soup):
            assert {"mask", "mask-heart", "bg-warning"} <= set(radio["class"])
            assert "rating-lg" not in radio["class"]
        assert "rating-lg" in _wrapper(soup)["class"]
        assert "bg-warning" not in _wrapper(soup)["class"]

    def test_the_default_shape_is_a_star_and_no_colour_or_size_is_emitted(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.rating />")

        for radio in _radios(soup):
            assert _prefixed(radio, "mask-") == ["mask-star"]
            assert not _prefixed(radio, "bg-")
        assert _prefixed(_wrapper(soup), "rating-") == []

    @pytest.mark.parametrize("shape", SHAPES)
    def test_each_shape_maps_to_its_mask_class(self, cotton_render_string_soup, shape):
        soup = cotton_render_string_soup(f'<c-form.rating shape="{shape}" />')

        for radio in _radios(soup):
            assert _prefixed(radio, "mask-") == [f"mask-{shape}"]

    @pytest.mark.parametrize("variant", VARIANTS)
    def test_each_variant_maps_to_a_background_class(
        self, cotton_render_string_soup, variant
    ):
        soup = cotton_render_string_soup(f'<c-form.rating variant="{variant}" />')

        for radio in _radios(soup):
            assert f"bg-{variant}" in radio["class"]

    @pytest.mark.parametrize("size", SIZES)
    def test_each_size_maps_to_a_wrapper_class(self, cotton_render_string_soup, size):
        soup = cotton_render_string_soup(f'<c-form.rating size="{size}" />')

        assert f"rating-{size}" in _wrapper(soup)["class"]

    def test_an_unknown_shape_variant_and_size_emit_nothing_and_do_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating shape="cube" variant="rainbow" size="huge" />'
        )

        assert len(_radios(soup)) == 5
        for radio in _radios(soup):
            assert _prefixed(radio, "mask-") == []
            assert _prefixed(radio, "bg-") == []
        assert _prefixed(_wrapper(soup), "rating-") == []

    def test_modifiers_reach_a_read_only_rating_too(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.rating readonly value="3" shape="heart" variant="warning" '
            'size="lg" />'
        )

        assert "rating-lg" in _wrapper(soup)["class"]
        for item in _read_only_items(soup):
            assert {"mask", "mask-heart", "bg-warning"} <= set(item["class"])


class TestRatingReadOnly:
    def test_the_items_are_divs_not_inputs(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating readonly value="3" />')

        assert not soup.find("input")
        items = _read_only_items(soup)
        assert len(items) == 5
        for item in items:
            assert {"mask", "mask-star"} <= set(item["class"])
        assert _wrapper(soup).find_all(True) == items

    def test_only_the_matching_item_is_current(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating readonly value="3" />')

        current = [item.has_attr("aria-current") for item in _read_only_items(soup)]
        assert current == [False, False, True, False, False]
        assert _read_only_items(soup)[2]["aria-current"] == "true"

    def test_the_wrapper_is_an_image_with_a_name_and_no_radiogroup(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating readonly value="3" />')

        assert _wrapper(soup)["role"] == "img"
        assert "3" in _wrapper(soup)["aria-label"]
        assert "5" in _wrapper(soup)["aria-label"]

    def test_the_name_follows_value_and_max(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating readonly value="4" max="8" />')

        assert "4" in _wrapper(soup)["aria-label"]
        assert "8" in _wrapper(soup)["aria-label"]
        assert "3" not in _wrapper(soup)["aria-label"]

    def test_a_max_that_is_not_a_number_is_named_as_five(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating readonly value="3" max="many" />'
        )

        assert "many" not in _wrapper(soup)["aria-label"]
        assert "5" in _wrapper(soup)["aria-label"]

    def test_without_a_value_the_name_reads_zero_and_no_item_is_current(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.rating readonly />")

        assert "0" in _wrapper(soup)["aria-label"]
        assert "None" not in _wrapper(soup)["aria-label"]
        assert not [
            item for item in _read_only_items(soup) if item.has_attr("aria-current")
        ]

    def test_the_items_carry_no_name_of_their_own(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating readonly value="3" />')

        for item in _read_only_items(soup):
            assert not item.has_attr("aria-label")

    def test_a_half_value_marks_the_half_item_current(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating readonly half value="2.5" />')

        items = _read_only_items(soup)
        assert len(items) == 10
        assert [
            index for index, item in enumerate(items) if item.has_attr("aria-current")
        ] == [4]
        assert "rating-half" in _wrapper(soup)["class"]
        assert "mask-half-1" in items[0]["class"]
        assert "mask-half-2" in items[1]["class"]

    def test_a_value_above_max_marks_no_item_current(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.rating readonly value="9" />')

        assert not [
            item for item in _read_only_items(soup) if item.has_attr("aria-current")
        ]

    def test_an_interactive_rating_has_no_aria_current_and_no_image_role(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating value="3" />')

        assert not soup.find(attrs={"aria-current": True})
        assert _wrapper(soup)["role"] == "radiogroup"

    def test_form_attributes_are_not_written_on_a_read_only_rating(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating readonly value="3" name="score" required disabled '
            'form="review" />'
        )

        for element in [_wrapper(soup), *_read_only_items(soup)]:
            for name in ("name", "required", "disabled", "form"):
                assert not element.has_attr(name)


class TestRatingName:
    def test_two_ratings_without_a_name_each_share_their_own_generated_name(
        self, cotton_render_string_soup
    ):
        first = cotton_render_string_soup("<c-form.rating />")
        second = cotton_render_string_soup("<c-form.rating />")

        first_names = {radio["name"] for radio in _radios(first)}
        second_names = {radio["name"] for radio in _radios(second)}
        assert len(first_names) == 1
        assert len(second_names) == 1
        assert first_names != second_names
        assert "" not in first_names

    def test_a_given_name_is_used_in_place_of_a_generated_one(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.rating name="score" clearable />')

        assert {radio["name"] for radio in _radios(soup)} == {"score"}


class TestRatingSharedAttributes:
    def test_required_disabled_and_form_land_on_every_radio(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating name="score" clearable required disabled form="review" />'
        )

        radios = _radios(soup)
        assert len(radios) == 6
        for radio in radios:
            assert radio.has_attr("required")
            assert radio.has_attr("disabled")
            assert radio["form"] == "review"

    def test_required_disabled_and_form_do_not_reach_the_wrapper(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating required disabled form="review" />'
        )

        for name in ("required", "disabled", "form"):
            assert not _wrapper(soup).has_attr(name)

    def test_none_of_them_appear_when_not_given(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.rating />")

        for radio in _radios(soup):
            for name in ("required", "disabled", "form"):
                assert not radio.has_attr(name)

    def test_each_is_written_once_per_radio(self, cotton_render_string):
        html = cotton_render_string(
            '<c-form.rating name="score" required disabled form="review" />'
        )

        names = _attr_names_on(html, "input")
        for name in ("name", "required", "disabled", "form", "value", "type"):
            assert names.count(name) == 1


class TestRatingAttributeRouting:
    def test_id_and_an_extra_attribute_reach_the_wrapper_only(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating id="review-rating" data-testid="rating" />'
        )

        assert _wrapper(soup)["id"] == "review-rating"
        assert _wrapper(soup)["data-testid"] == "rating"
        for radio in _radios(soup):
            assert not radio.has_attr("id")
            assert not radio.has_attr("data-testid")

    def test_id_and_an_extra_attribute_reach_a_read_only_wrapper(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.rating readonly id="review-rating" data-testid="rating" />'
        )

        assert _wrapper(soup)["id"] == "review-rating"
        assert _wrapper(soup)["data-testid"] == "rating"

    @pytest.mark.parametrize("attributes", ["", "readonly"])
    def test_class_merges_into_the_wrapper_once_and_not_the_items(
        self, cotton_render_string, cotton_render_string_soup, attributes
    ):
        source = f'<c-form.rating {attributes} class="mb-4" />'

        soup = cotton_render_string_soup(source)
        html = cotton_render_string(source)

        assert {"rating", "mb-4"} <= set(_wrapper(soup)["class"])
        assert _attr_names_on(html, "div").count("class") == 1
        for item in _wrapper(soup).find_all(True):
            assert "mb-4" not in item["class"]

    def test_the_wrapper_writes_its_own_attributes_once(self, cotton_render_string):
        html = cotton_render_string('<c-form.rating label="Your rating" id="r" />')

        names = _attr_names_on(html, "div")
        for name in ("class", "role", "aria-label", "id"):
            assert names.count(name) == 1
