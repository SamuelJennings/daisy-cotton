"""Tests for <c-radial-progress>: daisyUI's radial progress ring, whose
value is required with an empty default so a page variable named value can
never leak in, and whose slot is tested for whitespace before it is trusted
to replace the visible percentage.
"""


class TestRadialProgressRoot:
    def test_renders_a_div_carrying_radial_progress_and_role_progressbar(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-radial-progress value="70" />')

        div = soup.find("div", class_="radial-progress")
        assert div is not None
        assert div["role"] == "progressbar"


class TestRadialProgressStyle:
    def test_style_begins_with_value_custom_property(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-radial-progress value="70" />')

        assert soup.div["style"].startswith("--value:70;")

    def test_caller_style_is_appended_after_value(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-radial-progress value="70" style="color:red;" />'
        )

        assert soup.div["style"] == "--value:70; color:red;"

    def test_value_holding_quote_and_angle_bracket_is_escaped_inside_style(
        self, cotton_render_string
    ):
        html = cotton_render_string(
            '<c-radial-progress :value="hostile" />',
            context={"hostile": '"><script>'},
        )

        assert "<script>" not in html
        assert 'style="--value:&quot;&gt;&lt;script&gt;;"' in html


class TestRadialProgressValue:
    def test_no_value_given_emits_no_aria_valuenow(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-radial-progress />")

        assert soup.div.get("aria-valuenow") is None

    def test_given_value_emits_aria_valuenow(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-radial-progress value="70" />')

        assert soup.div["aria-valuenow"] == "70"

    def test_aria_valuemin_and_valuemax_are_always_present(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-radial-progress />")

        assert soup.div["aria-valuemin"] == "0"
        assert soup.div["aria-valuemax"] == "100"


class TestRadialProgressVisibleText:
    def test_no_slot_shows_the_value_as_a_percentage(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-radial-progress value="70" />')

        assert soup.div.get_text(strip=True) == "70%"

    def test_no_slot_and_no_value_shows_nothing(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-radial-progress />")

        assert soup.div.get_text(strip=True) == ""

    def test_whitespace_only_slot_still_shows_the_percentage(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-radial-progress value="70">   </c-radial-progress>'
        )

        assert soup.div.get_text(strip=True) == "70%"

    def test_non_empty_slot_replaces_the_percentage(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-radial-progress value="70"><i class="bi bi-cloud-upload" aria-hidden="true"></i></c-radial-progress>'
        )

        assert soup.div.find("i") is not None
        assert "70%" not in soup.div.get_text()
        assert soup.div["aria-valuenow"] == "70"
        assert "--value:70;" in soup.div["style"]

    def test_value_bound_to_zero_is_written_and_shown(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-radial-progress :value="done" />', {"done": 0}
        )

        assert soup.div["aria-valuenow"] == "0"
        assert soup.div.get_text(strip=True) == "0%"


class TestRadialProgressLabel:
    def test_given_label_is_used_as_the_aria_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-radial-progress value="70" label="Upload progress" />'
        )

        assert soup.div["aria-label"] == "Upload progress"

    def test_no_label_emits_no_aria_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-radial-progress value="70" />')

        assert soup.div.get("aria-label") is None


class TestRadialProgressClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-radial-progress value="70" class="mt-4" data-test="x" />'
        )

        div = soup.div
        assert "mt-4" in div["class"]
        assert "radial-progress" in div["class"]
        assert div["data-test"] == "x"


class TestRadialProgressPageContextDoesNotLeak:
    def test_page_context_does_not_leak_into_the_radial_progress(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-radial-progress />",
            context={
                "value": 90,
                "label": "Leaked",
                "style": "color:red;",
            },
        )

        div = soup.div
        assert div.get("aria-valuenow") is None
        assert div.get("aria-label") is None
        assert div["style"] == "--value:;"
