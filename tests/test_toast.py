"""Tests for <c-toast>: daisyUI's positioning wrapper for one or more
alerts, carrying no role or live region of its own.
"""

import pytest


class TestToastRoot:
    def test_renders_a_wrapper_carrying_toast_around_two_alerts_in_order(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-toast>"
            '<c-alert variant="success">Saved.</c-alert>'
            '<c-alert variant="error">Failed.</c-alert>'
            "</c-toast>"
        )

        div = soup.find("div", class_="toast")
        assert div is not None
        alerts = div.find_all("div", class_="alert")
        assert len(alerts) == 2
        assert "Saved." in alerts[0].get_text()
        assert "Failed." in alerts[1].get_text()

    def test_each_alert_keeps_its_own_role(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-toast>"
            '<c-alert variant="success">Saved.</c-alert>'
            '<c-alert variant="success" role="status">Also saved.</c-alert>'
            "</c-toast>"
        )

        alerts = soup.find("div", class_="toast").find_all("div", class_="alert")
        assert alerts[0]["role"] == "alert"
        assert alerts[1]["role"] == "status"

    def test_empty_toast_renders_an_empty_wrapper(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-toast></c-toast>")

        div = soup.find("div", class_="toast")
        assert div is not None
        assert div.find(True) is None


class TestToastPlacement:
    @pytest.mark.parametrize(
        "placement,classes",
        [
            ("top", ["toast-top"]),
            ("middle", ["toast-middle"]),
            ("bottom", ["toast-bottom"]),
            ("start", ["toast-start"]),
            ("center", ["toast-center"]),
            ("end", ["toast-end"]),
            ("top center", ["toast-top", "toast-center"]),
            ("bottom start", ["toast-bottom", "toast-start"]),
        ],
    )
    def test_each_placement_word_maps_to_its_daisyui_class(
        self, cotton_render_string_soup, placement, classes
    ):
        soup = cotton_render_string_soup(f'<c-toast placement="{placement}"></c-toast>')

        for css_class in classes:
            assert css_class in soup.div["class"]

    def test_unknown_placement_word_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-toast placement="diagonal"></c-toast>'
        )

        assert not any("diagonal" in cls for cls in soup.div["class"])


class TestToastNoRoleOrLiveRegion:
    def test_root_carries_no_role_or_aria_live(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-toast><c-alert>Saved.</c-alert></c-toast>'
        )

        div = soup.find("div", class_="toast")
        assert div.get("role") is None
        assert div.get("aria-live") is None


class TestToastClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-toast class="mt-4" data-test="x"></c-toast>'
        )

        div = soup.div
        assert "mt-4" in div["class"]
        assert "toast" in div["class"]
        assert div["data-test"] == "x"


class TestToastPageContextDoesNotLeak:
    def test_page_context_does_not_leak_into_the_toast(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-toast></c-toast>",
            context={"placement": "top center"},
        )

        div = soup.div
        assert not any("top" in cls for cls in div["class"])
        assert not any("center" in cls for cls in div["class"])
