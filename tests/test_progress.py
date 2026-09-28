"""Tests for <c-progress>: daisyUI's native progress bar, whose value must
be emitted for emptiness rather than truthiness so a bound zero still shows.
"""

from html.parser import HTMLParser

import pytest


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser.
    """

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        if self.attrs is None and tag == self.tag:
            self.attrs = attrs


def _attrs_on(html, tag):
    parser = _FirstTagAttrs(tag)
    parser.feed(html)
    assert parser.attrs is not None, f"no <{tag}> tag found in rendered output"
    return parser.attrs


def _attr_value(attrs, name):
    for attr_name, value in attrs:
        if attr_name == name:
            return value
    return None


class TestProgressRoot:
    def test_renders_a_progress_element_carrying_progress(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-progress />")

        progress = soup.find("progress")
        assert progress is not None
        assert "progress" in progress["class"]


class TestProgressValue:
    def test_no_value_given_emits_no_value_attribute(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-progress />")

        assert soup.progress.get("value") is None

    def test_bound_zero_still_renders_value_zero(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-progress :value="0" />')

        assert soup.progress["value"] == "0"

    def test_bound_none_emits_no_value_attribute(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-progress :value="missing" />', context={"missing": None}
        )

        assert soup.progress.get("value") is None

    def test_given_value_is_emitted(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-progress value="40" />')

        assert soup.progress["value"] == "40"


class TestProgressMax:
    def test_default_max_is_100(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-progress />")

        assert soup.progress["max"] == "100"

    def test_given_max_replaces_the_default(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-progress max="50" />')

        assert soup.progress["max"] == "50"


class TestProgressVariant:
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
        soup = cotton_render_string_soup(f'<c-progress variant="{variant}" />')

        assert f"progress-{variant}" in soup.progress["class"]

    def test_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-progress variant="rainbow" />')

        assert not any("rainbow" in cls for cls in soup.progress["class"])


class TestProgressLabel:
    def test_given_label_is_used_as_the_aria_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-progress label="Upload progress" />')

        assert soup.progress["aria-label"] == "Upload progress"

    def test_no_label_emits_no_aria_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-progress />")

        assert soup.progress.get("aria-label") is None


class TestProgressClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-progress class="mt-4" data-test="x" />')

        progress = soup.progress
        assert "mt-4" in progress["class"]
        assert "progress" in progress["class"]
        assert progress["data-test"] == "x"


class TestProgressPageContextDoesNotLeak:
    def test_page_context_does_not_leak_into_the_progress(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-progress />",
            context={
                "value": 75,
                "max": 50,
                "variant": "error",
                "label": "Leaked",
            },
        )

        progress = soup.progress
        assert progress.get("value") is None
        assert progress["max"] == "100"
        assert not any("error" in cls for cls in progress["class"])
        assert progress.get("aria-label") is None
