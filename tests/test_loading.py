"""Tests for <c-loading>: daisyUI's loading indicator, named for assistive
technology and merged into any element that hosts it (such as a button).
"""

from html.parser import HTMLParser

import pytest
from django.template import base as template_base


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


class TestLoadingRoot:
    def test_renders_a_span_carrying_loading_with_role_status(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-loading />")

        span = soup.find("span", class_="loading")
        assert span is not None
        assert span["role"] == "status"


class TestLoadingAnimation:
    @pytest.mark.parametrize(
        "attr,css_class",
        [
            ("spinner", "loading-spinner"),
            ("dots", "loading-dots"),
            ("ring", "loading-ring"),
            ("ball", "loading-ball"),
            ("bars", "loading-bars"),
            ("infinity", "loading-infinity"),
        ],
    )
    def test_each_animation_maps_to_its_daisyui_class(
        self, cotton_render_string_soup, attr, css_class
    ):
        soup = cotton_render_string_soup(f"<c-loading {attr} />")

        assert css_class in soup.span["class"]

    def test_no_animation_given_emits_no_style_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-loading />")

        classes = soup.span["class"]
        assert classes == ["loading"]

    def test_two_animations_given_emit_both(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-loading spinner dots />")

        assert "loading-spinner" in soup.span["class"]
        assert "loading-dots" in soup.span["class"]


class TestLoadingSize:
    @pytest.mark.parametrize("size", ["xs", "sm", "md", "lg", "xl"])
    def test_each_size_maps_to_its_daisyui_class(self, cotton_render_string_soup, size):
        soup = cotton_render_string_soup(f'<c-loading size="{size}" />')

        assert f"loading-{size}" in soup.span["class"]

    def test_an_unknown_size_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-loading size="huge" />')

        assert not any("huge" in cls for cls in soup.span["class"])


class TestLoadingLabel:
    def test_given_label_is_used_as_the_aria_label(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-loading label="Saving" />')

        assert soup.span["aria-label"] == "Saving"

    def test_no_label_falls_back_to_the_translatable_loading(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-loading />")

        assert soup.span["aria-label"] == "Loading"


class TestLoadingTranslation:
    def test_default_label_is_resolved_through_gettext(
        self, cotton_render_string, monkeypatch
    ):
        monkeypatch.setattr(
            template_base, "gettext_lazy", lambda message: f"[t]{message}[/t]"
        )
        html = cotton_render_string("<c-loading />")

        attrs = _attrs_on(html, "span")
        assert _attr_value(attrs, "aria-label") == "[t]Loading[/t]"

    def test_default_label_fails_against_a_hard_coded_string(
        self, cotton_render_string, monkeypatch
    ):
        monkeypatch.setattr(
            template_base, "gettext_lazy", lambda message: f"[t]{message}[/t]"
        )
        html = cotton_render_string("<c-loading />")

        attrs = _attrs_on(html, "span")
        assert _attr_value(attrs, "aria-label") != "Loading"


class TestLoadingClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-loading class="text-primary" data-test="x" />'
        )

        span = soup.span
        assert "text-primary" in span["class"]
        assert "loading" in span["class"]
        assert span["data-test"] == "x"


class TestLoadingInsideAButton:
    def test_loading_sits_inside_the_button_slot(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            '<c-button type="button">Add to cart <c-loading size="sm" /></c-button>'
        )

        button = soup.find("button")
        assert button is not None
        assert button.find("span", class_="loading") is not None


class TestLoadingPageContextDoesNotLeak:
    def test_page_context_does_not_leak_into_the_loading(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            "<c-loading />",
            context={
                "label": "Leaked",
                "size": "xs",
                "dots": True,
            },
        )

        span = soup.span
        assert span["aria-label"] == "Loading"
        assert not any("xs" in cls for cls in span["class"])
        assert "loading-dots" not in span["class"]
