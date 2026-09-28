"""Tests for <c-alert>: daisyUI's alert banner, rebuilt on the attribute
vocabulary and the accessibility bar.
"""

from html.parser import HTMLParser

import pytest
from django.template import base as template_base


class _FirstTagAttrs(HTMLParser):
    """Collect the raw attribute list of the first ``<tag>`` start tag.

    HTMLParser reports every occurrence of a repeated attribute rather than
    silently dropping it, unlike a browser — which is what proving a single
    ``role`` attribute needs.
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


def _attr_values(attrs, name):
    return [value for attr_name, value in attrs if attr_name == name]


def _attr_value(attrs, name):
    values = _attr_values(attrs, name)
    return values[0] if values else None


class TestAlertRoot:
    def test_renders_a_div_carrying_alert_with_role_alert_by_default(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-alert>Saved.</c-alert>")

        div = soup.find("div", class_="alert")
        assert div is not None
        assert div["role"] == "alert"

    def test_slot_content_is_rendered_inside(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert>Saved.</c-alert>")

        assert soup.div.get_text(strip=True) == "Saved."


class TestAlertVariant:
    @pytest.mark.parametrize("variant", ["info", "success", "warning", "error"])
    def test_each_variant_maps_to_its_daisyui_class(
        self, cotton_render_string_soup, variant
    ):
        soup = cotton_render_string_soup(f'<c-alert variant="{variant}">x</c-alert>')

        assert f"alert-{variant}" in soup.div["class"]

    def test_an_unknown_variant_emits_no_class_and_does_not_raise(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-alert variant="rainbow">x</c-alert>')

        assert not any("rainbow" in cls for cls in soup.div["class"])

    def test_scenario_1_success_soft_emits_alert_alert_success_alert_soft(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-alert variant="success" soft>Saved.</c-alert>'
        )

        div = soup.div
        for token in ("alert", "alert-success", "alert-soft"):
            assert token in div["class"]
        assert div["role"] == "alert"
        assert div.get_text(strip=True) == "Saved."


class TestAlertStyle:
    def test_outline_emits_alert_outline(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert outline>x</c-alert>")
        assert "alert-outline" in soup.div["class"]

    def test_dash_emits_alert_dash(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert dash>x</c-alert>")
        assert "alert-dash" in soup.div["class"]

    def test_soft_and_outline_both_emit(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert soft outline>x</c-alert>")
        assert "alert-soft" in soup.div["class"]
        assert "alert-outline" in soup.div["class"]


class TestAlertDirection:
    def test_bare_vertical_emits_alert_vertical(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert vertical>x</c-alert>")
        assert "alert-vertical" in soup.div["class"]

    def test_vertical_with_horizontal_breakpoint_emits_both(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-alert vertical horizontal="sm">x</c-alert>'
        )
        assert "alert-vertical" in soup.div["class"]
        assert "sm:alert-horizontal" in soup.div["class"]

    def test_horizontal_left_emits_no_class(self, cotton_render_string_soup):
        soup = cotton_render_string_soup('<c-alert horizontal="left">x</c-alert>')
        assert not any("horizontal" in cls for cls in soup.div["class"])


class TestAlertRole:
    def test_caller_role_replaces_the_default_and_only_one_role_is_emitted(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-alert role="status">x</c-alert>')

        attrs = _attrs_on(html, "div")
        role_values = _attr_values(attrs, "role")
        assert role_values == ["status"]


class TestAlertIcon:
    def test_icon_draws_c_icon_before_content_hidden_from_assistive_technology(
        self, cotton_render_string
    ):
        html = cotton_render_string('<c-alert icon="bi bi-check">Saved.</c-alert>')

        assert html.index("bi-check") < html.index("Saved.")
        assert 'aria-hidden="true"' in html
        icon_tag = html[html.index("<i ") : html.index("</i>")]
        assert "bi" in icon_tag and "bi-check" in icon_tag

    def test_variant_with_no_icon_draws_c_icon_named_after_the_variant(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup('<c-alert variant="success">Saved.</c-alert>')

        icon = soup.div.find("i")
        assert icon is not None
        assert "success" in icon["class"]
        assert icon["aria-hidden"] == "true"

    def test_no_icon_and_no_variant_draws_no_icon(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert>x</c-alert>")
        assert soup.div.find("i") is None


class TestAlertDismiss:
    def test_dismissible_renders_a_dismiss_button_after_the_content(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-alert dismissible>Saved.</c-alert>")

        div = soup.div
        button = div.find("button")
        assert button is not None
        assert button["type"] == "button"
        assert "btn" in button["class"]

        children = [
            child
            for child in div.children
            if getattr(child, "name", None) is not None or str(child).strip()
        ]
        assert children.index(button) == len(children) - 1

    def test_dismiss_button_glyph_is_hidden_from_assistive_technology(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup("<c-alert dismissible>x</c-alert>")

        button = soup.div.find("button")
        glyph = button.find("span")
        assert glyph is not None
        assert glyph["aria-hidden"] == "true"
        assert glyph.get_text(strip=True)

    def test_dismissible_root_carries_alpine_attributes(self, cotton_render_string):
        html = cotton_render_string("<c-alert dismissible>x</c-alert>")

        attrs = _attrs_on(html, "div")
        assert _attr_value(attrs, "x-data") == "{ show: true }"
        assert _attr_value(attrs, "x-show") == "show"
        assert _attr_value(attrs, "x-transition") is None
        assert "x-transition" in [name for name, _ in attrs]

    def test_dismiss_button_carries_x_on_click(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert dismissible>x</c-alert>")

        button = soup.div.find("button")
        assert button["x-on:click"] == "show = false"

    def test_no_dismissible_renders_no_button(self, cotton_render_string_soup):
        soup = cotton_render_string_soup("<c-alert>x</c-alert>")
        assert soup.div.find("button") is None


class TestAlertDismissTranslation:
    def test_dismiss_label_is_resolved_through_gettext(
        self, cotton_render_string_soup, monkeypatch
    ):
        monkeypatch.setattr(
            template_base, "gettext_lazy", lambda message: f"[t]{message}[/t]"
        )
        soup = cotton_render_string_soup("<c-alert dismissible>x</c-alert>")

        button = soup.div.find("button")
        assert button["aria-label"] == "[t]Dismiss[/t]"

    def test_dismiss_label_fails_against_a_hard_coded_string(
        self, cotton_render_string_soup, monkeypatch
    ):
        monkeypatch.setattr(
            template_base, "gettext_lazy", lambda message: f"[t]{message}[/t]"
        )
        soup = cotton_render_string_soup("<c-alert dismissible>x</c-alert>")

        button = soup.div.find("button")
        assert button["aria-label"] != "Dismiss"


class TestAlertDelay:
    def test_numeric_delay_reaches_x_init_through_add_zero(self, cotton_render_string):
        html = cotton_render_string('<c-alert dismissible delay="4000">x</c-alert>')

        attrs = _attrs_on(html, "div")
        x_init = _attr_value(attrs, "x-init")
        assert x_init == "setTimeout(() => show = false, 4000)"

    @pytest.mark.parametrize("delay", ["soon", "5s", "1500.5"])
    def test_non_numeric_delay_adds_no_x_init(self, cotton_render_string, delay):
        html = cotton_render_string(f'<c-alert dismissible delay="{delay}">x</c-alert>')

        attrs = _attrs_on(html, "div")
        assert _attr_value(attrs, "x-init") is None
        assert _attr_value(attrs, "x-data") is not None

    def test_delay_without_dismissible_adds_no_x_init(self, cotton_render_string):
        html = cotton_render_string('<c-alert delay="4000">x</c-alert>')

        attrs = _attrs_on(html, "div")
        assert _attr_value(attrs, "x-init") is None


class TestAlertClassAndAttrs:
    def test_class_merges_and_extra_attributes_reach_the_root(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-alert class="mt-4" data-test="x">x</c-alert>'
        )

        div = soup.div
        assert "mt-4" in div["class"]
        assert "alert" in div["class"]
        assert div["data-test"] == "x"


class TestAlertPageContextDoesNotLeak:
    def test_page_context_does_not_leak_into_the_alert(self, cotton_render_string_soup):
        soup = cotton_render_string_soup(
            "<c-alert>x</c-alert>",
            context={
                "variant": "error",
                "icon": "bi bi-leak",
                "role": "status",
                "delay": "1",
                "dismissible": True,
            },
        )

        div = soup.div
        assert div["role"] == "alert"
        assert not any("error" in cls for cls in div["class"])
        assert div.find("i") is None
        assert div.find("button") is None


class TestAlertIconClass:
    def test_icon_does_not_carry_a_class_given_to_the_alert(
        self, cotton_render_string_soup
    ):
        soup = cotton_render_string_soup(
            '<c-alert variant="success" class="mt-4">Saved.</c-alert>'
        )

        assert "mt-4" in soup.div["class"]
        assert "mt-4" not in soup.div.find("i")["class"]
