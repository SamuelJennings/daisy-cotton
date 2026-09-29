"""Tests for <c-form.calendar>: Cally's calendar elements carrying daisyUI's
cally class, with the paging buttons named through slotted content.

Sources render through the Cotton compiler as a caller's template would, so
attributes reach the component the way they do in a real page.
"""

from html.parser import HTMLParser

import pytest

ROOTS = ("calendar-date", "calendar-range")


class _RootAttrs(HTMLParser):
    """Collect the raw attribute list of the first calendar root start tag.

    HTMLParser reports a repeated attribute every time it occurs, where a
    browser (and BeautifulSoup) keep only one.
    """

    def __init__(self):
        super().__init__()
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag in ROOTS:
            self.attrs = attrs


def _root_attr_names(html):
    parser = _RootAttrs()
    parser.feed(html)
    assert parser.attrs is not None, "no calendar root found in rendered output"
    return [name for name, _ in parser.attrs]


def _root(soup):
    return soup.find(ROOTS)


def _months(soup):
    return _root(soup).find_all("calendar-month", recursive=False)


def _slot(soup, name):
    return _root(soup).find(attrs={"slot": name}, recursive=False)


class TestCalendarRoot:
    def test_renders_a_calendar_date_carrying_cally_with_one_month(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.calendar />")

        root = soup.find("calendar-date")
        assert root is not None
        assert "cally" in root["class"]
        assert soup.find("calendar-range") is None
        assert len(_months(soup)) == 1

    def test_range_renders_a_calendar_range_carrying_cally(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.calendar range />")

        root = soup.find("calendar-range")
        assert root is not None
        assert "cally" in root["class"]
        assert soup.find("calendar-date") is None
        assert len(_months(soup)) == 1

    def test_the_root_wraps_the_paging_slots_and_then_the_months(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-form.calendar />")

        children = [child.name for child in _root(soup).find_all(True, recursive=False)]
        assert children == ["span", "span", "calendar-month"]

    def test_the_calendar_is_a_single_root(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.calendar />")

        assert len(soup.find_all(ROOTS)) == 1


class TestCalendarMonths:
    def test_two_months_give_two_month_elements_the_second_offset_by_one(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.calendar months="2" />')

        months = _months(soup)
        assert len(months) == 2
        assert not months[0].has_attr("offset")
        assert months[1]["offset"] == "1"

    def test_three_months_offset_by_one_more_each(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.calendar months="3" />')

        months = _months(soup)
        assert [month.get("offset") for month in months] == [None, "1", "2"]

    def test_more_than_one_month_is_written_on_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.calendar months="2" />')

        assert _root(soup)["months"] == "2"

    def test_a_range_with_two_months_writes_the_count_on_its_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.calendar range months="2" />')

        assert soup.find("calendar-range")["months"] == "2"
        assert len(_months(soup)) == 2

    def test_one_month_writes_no_months_attribute(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.calendar />")

        assert not _root(soup).has_attr("months")

    def test_months_is_written_once_on_the_root(self, cotton_render_string):
        html = cotton_render_string('<c-form.calendar months="2" />')

        assert _root_attr_names(html).count("months") == 1

    @pytest.mark.parametrize("months", ["many", "0", "-2", "2.5", ""])
    def test_a_non_number_or_non_positive_months_gives_one_month(
        self, cotton_render_string_soup, months
    ):
        soup = cotton_render_string_soup(f'<c-form.calendar months="{months}" />')

        assert len(_months(soup)) == 1
        assert not _root(soup).has_attr("months")


class TestCalendarCallyAttributes:
    def test_cally_attributes_reach_the_root_unchanged(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-form.calendar value="2026-09-29" min="2026-09-01" max="2026-09-30" '
            'locale="en-GB" first-day-of-week="1" />'
        )

        root = _root(soup)
        assert root["value"] == "2026-09-29"
        assert root["min"] == "2026-09-01"
        assert root["max"] == "2026-09-30"
        assert root["locale"] == "en-GB"
        assert root["first-day-of-week"] == "1"

    def test_cally_attributes_reach_a_range_root_unchanged(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.calendar range value="2026-09-01/2026-09-07" min="2026-09-01" />'
        )

        root = soup.find("calendar-range")
        assert root["value"] == "2026-09-01/2026-09-07"
        assert root["min"] == "2026-09-01"

    def test_other_attributes_reach_the_root_and_nothing_else(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.calendar id="delivery" data-testid="cal" />'
        )

        assert _root(soup)["id"] == "delivery"
        assert _root(soup)["data-testid"] == "cal"
        assert len(soup.find_all(id="delivery")) == 1

    def test_range_is_not_written_as_an_attribute(self, cotton_render_string):
        html = cotton_render_string("<c-form.calendar range />")

        assert "range" not in _root_attr_names(html)


class TestCalendarPagingSlots:
    @pytest.mark.parametrize("name", ["previous", "next"])
    def test_the_slot_element_holds_a_hidden_icon_and_a_visually_hidden_name(
        self, cotton_render_string_soup, name
    ):
        soup = cotton_render_string_soup("<c-form.calendar />")

        slot = _slot(soup, name)
        assert slot is not None
        icon = slot.find("i")
        assert icon is not None
        assert icon["aria-hidden"] == "true"
        hidden_name = slot.find(class_="sr-only")
        assert hidden_name is not None
        assert hidden_name.get_text(strip=True)

    def test_the_two_slots_carry_different_names(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.calendar />")

        previous = _slot(soup, "previous").find(class_="sr-only").get_text(strip=True)
        following = _slot(soup, "next").find(class_="sr-only").get_text(strip=True)

        assert previous != following

    def test_the_icons_default_to_chevrons(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-form.calendar />")

        assert "chevron-left" in _slot(soup, "previous").find("i")["class"]
        assert "chevron-right" in _slot(soup, "next").find("i")["class"]

    def test_previous_icon_and_next_icon_reach_their_icons(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-form.calendar previous_icon="bi bi-arrow-left" '
            'next_icon="bi bi-arrow-right" />'
        )

        previous = _slot(soup, "previous").find("i")
        following = _slot(soup, "next").find("i")
        assert {"bi", "bi-arrow-left"} <= set(previous["class"])
        assert {"bi", "bi-arrow-right"} <= set(following["class"])
        assert "bi-arrow-right" not in previous["class"]
        assert "bi-arrow-left" not in following["class"]


class TestCalendarClass:
    def test_class_merges_into_the_root_after_cally(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.calendar class="mb-4 shadow" />')

        assert _root(soup)["class"] == ["cally", "mb-4", "shadow"]

    def test_class_reaches_a_range_root(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-form.calendar range class="mb-4" />')

        assert "mb-4" in soup.find("calendar-range")["class"]

    def test_class_is_written_once_on_the_root(self, cotton_render_string):
        html = cotton_render_string('<c-form.calendar class="mb-4" />')

        assert _root_attr_names(html).count("class") == 1

    def test_class_does_not_reach_either_icon_or_a_month(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-form.calendar class="mb-4" />')

        for icon in _root(soup).find_all("i"):
            assert "mb-4" not in icon["class"]
        for month in _months(soup):
            assert not month.has_attr("class")
